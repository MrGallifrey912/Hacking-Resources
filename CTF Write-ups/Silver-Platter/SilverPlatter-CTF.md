# SilverPlatter THM
## Enumeration
Waited 5min for all services. then ran a nmap scan on all ports
`sudo nmap -sS -sV -T5 -vv Target_IP -allports`
which returned
```
PORT     STATE SERVICE    REASON         VERSION
22/tcp   open  ssh        syn-ack ttl 61 OpenSSH 8.9p1 Ubuntu 3ubuntu0.4 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http       syn-ack ttl 61 nginx 1.18.0 (Ubuntu)
8080/tcp open  http-proxy syn-ack ttl 60
```
I then ran GoBuster to find directories. Scanning on port 80 I only found /images and /assets, not to useful.
Navigated to the website on port 80 and started exploring, nothing of real interest until you get to the contact card. which shows:
'If you'd like to get in touch with us, please reach out to our project manager on Silverpeas. His username is "scr1ptkiddy".'
#### **the proxy**
Started scanning on port 8080 and found /website, /console and /silverpeas after some research into what silverpeas was. Silverpeas seems to be a github type application or a website console.  
So I entered in /silverpeas and was brought to a login page: 
http://Target_IP:8080/silverpeas

#### **Login exploit**
After some searching, I found a simple exploit of the console. If you omit the password field using super admin credentials you bypass authentication.

reference: https://github.com/advisories/GHSA-4w54-wwc9-x62c

I captured the Login process in Burpsuite after finding the super admin credentials of "SilverAdmin" in the documentation on their website. ![SilverPeas defaults](https://github.com/MrGallifrey912/Hacking-Resources/blob/e8ec3ae58c6ee8893d68e77ec239cbc911892273/CTF%20Write-ups/Silver-Platter/images/Pasted%20image%2020250128134634.png))

I then deleted the password field in the request and forwarded all remaining packages. 
![BurpSuite](https://github.com/MrGallifrey912/Hacking-Resources/blob/fe5c27b65102160618584e7cd87bb997ab4ad48c/CTF%20Write-ups/Silver-Platter/images/Screenshot%202025-01-28%20134440.png)

reference: https://www.silverpeas.org/installation/installationV6.html
#### ***Succès, j'en suis !***

I am no language expert but the landing page seems to be in french. I used ChatGPT to translate some of the interesting points of the UI. 
- **Mes agendas** – My calendars
- **Mes tâches** – My tasks
- **Mes notifications** – My notifications
- **Mes abonnements** – My subscriptions
- **Mes requêtes favorites** – My favorite requests
- **Mes favoris** – My favorites
- **Trouver une date** – Find a date
- **Mon profil** – My profile
- **Ecrire aux administrateurs** – Write to the administrators
- **Presse-papier** – Clipboard
- **Ajouter une application...** – Add an application...
in the upper right are three tabs.
- **Boîte de notifications** – Notification box
- **Notifications envoyées** – Sent notifications
- **Paramétrage** – Settings (or Configuration)
I navigated through and found in the Sent Notifications tab a notification for SSH...
the message reads:
```
Dude how do you always forget the SSH password? Use a password manager and quit using your silly sticky notes. 

Username: tim

Password: cm0nt!md0ntf0rg3tth!spa$$w0rdagainlol
```

LMAO, that password has me dying. Now we can SSH in to the webserver.

#### **SSH in**
So I logged in as tim, and ran the 'ls' command and returned a user.txt
```
tim@silver-platter:~$ ls
user.txt
tim@silver-platter:~$ cat user.txt
```
So that is the User flag, nice.

Now to find out who else is on the machine. I ran a 'cat etc/passwd' 
```
tyler:x:1000:1000:root:/home/tyler:/bin/bash
lxd:x:999:100::/var/snap/lxd/common/lxd:/bin/false
tim:x:1001:1001::/home/tim:/bin/bash
```
well hello tyler, lets see if I can get your password.

#### **Pivoting**
I tried to use tims shell access to see what I could access, after poking around I found some auth logs in /var/log.
auth.log, auth.log.1 and auth.log.2.
Iterated through by 'cat /car/log/auth.log' and found a DB_PASSWORD. Im curious if this is also tylers password on this machine.

DB_PASSWORD=_Zd_zx7N823/

ran 'su tyler' to change users and copied the db_password found into the prompt. success.
although I am user tyler now I still cannot access root directly.  I then checked permissions of 'tyler' with 'id':
```
tyler@silver-platter:/$ id                                                                                                                         
uid=1000(tyler) gid=1000(tyler) groups=1000(tyler),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),110(lxd)
```
I see he can 'sudo' but what can he 'sudo':
```
tyler@silver-platter:/$ sudo -l                                                                                                                    
[sudo] password for tyler:                                                                                                                         
Matching Defaults entries for tyler on silver-platter:                                                                                             
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty                     
                                                                                                                                                   
User tyler may run the following commands on silver-platter:                                                                                       
    (ALL : ALL) ALL 
```
Tyler can do it all, I then tried to sudo to root.
```
tyler@silver-platter:/$ sudo su
root@silver-platter:/# cd root
root@silver-platter:~# ls
root.txt  snap  start_docker_containers.sh
root@silver-platter:~# cat root.txt
```
since this was successful I was then able to get to the root directory and retrieve the root.txt flag.

### Conclusion
This was a fun room from one of my favorite red-team streamer. I had to give this a shot and truly enjoyed the box he made. In this CTF room, we utilized recon on a webserver with the use of nmap and gobuster. Leveraged a password stored in plain text on the webserver console that was sent in a message to gain SSH to the webserver. Finally, was able to escalate privileges by finding a database password stored in logs. 

You can prevent these vulnerabilities by securing the web console further by performing regular updates and changing the defaults. Next, be cautious of what information is passed in plain text in emails and messaging apps. Lastly, perform regular audits on logs and encrypt any sensitive files.



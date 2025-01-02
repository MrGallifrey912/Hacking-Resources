In today's world, email is an essential communication tool and is used by individuals and organizations around the globe. Since it is used so widely, this means that it is one of the most exploited attack vectors for threat actors, if not, the primary method of exploitation. After doing some research it turns out that somewhere in the ballpark of 85% - 91% of cyberattacks begin with a phishing email.

In this post I will guide us through exploring how email is leveraged as the initial vector for attackers, the types of emails threat actors manipulate and strategies to bolster email security and mitigate these risks.

## #1 Attack Vector: Email

Let's go back to that figure of 85% - 91% of cyberattacks begin with a phish. I found some articles dating back to just under a decade ago discussing these numbers. According to a Dark Reading article published in December 2016, the figure of 91% comes from a PhishMe report. The report breaks down additional findings such as the top reasons people get got by phishing emails. The top reasons at the time are "curiosity (13.7%), fear (13.4%), and urgency (13.2%), followed by reward/recognition, social, entertainment, and opportunity".  That was back in 2016 let's now look at 2024.

According to a Cofense (formerly known as PhishMe) report released in February 2024, "Email is still the #1 threat vector for cybercrime with 90% of data breaches starting with a phish".  Now there is more details in this report, however its apparent that email phishing will not slow down or decrease as an attack vector. In fact, Here is some stark news as well. Email Phishing has been evolving already for at least two years in my findings. New methods and tactics are being leveraged such as, QR codes and the utilization of LLM (Large Language Models) to capitalize and refine the phish.  

Attackers also target email because they rely on fundamental human flaws such as trust, fear and opportunities.  These can manifest in a way that make the user believe that they urgently need to interact with the lure at the risk of job loss. They can also capitalize on trust by spoofing a higher up or a coworker and gain access that way, especially if you are in IT or another critical role. The last is opportunistic led, this can come in the form of promotion, prizes or winnings and simply put, to good to be true offers. I experienced this last one personally and caught on before I gave out any of my financial information. I truly believe that ANYONE can fall for a phish no matter your background, you can be the president of the United States, PhD in cybersecurity or a IT person working in healthcare. Never say I never fall for a phish, cause you are asking for a FAFO learning experience.

## Types of Email attacks

Through carefully curated and manipulative messages the goal of the threat actor is to prey upon our flaws and deceive recipients into:
* clicking malicious URLS or links
* downloading malware infected attachments (e.g. .xls, .docx, .pdf)
* Sharing sensitive information such as passwords or financial data

With a single compromise of one email account, threat actors can gain a further foothold in an organizations network. This can lead to data breaches, ransomware and Business Email Compromise (BEC). All of which can start from a single email attack such as:
#### 1) Phishing Emails
These are designed to gather credentials and other sensitive information. This type email often impersonates a trusted entity such as banks, service providers, internal departments and even third party vendors. Imagine getting a spoofed email from someone claiming to "IT Support" asking for you to update your password using a fake link.

#### 2) Spear Phishing
This is a slightly more targeted approach, meaning they have already collected some insight and are leveraging it to attack a specific target. These are highly convincing messages crafted around roles and habits typically. This would look like a CFO gets an email, seemingly from the CEO, requesting an urgent approval of a wire transfer of large sum of money.

#### 3) Business Email Compromise (BEC)
This involves high ranking officials or trusted vendors manipulating an employees into transferring money or sharing sensitive data. A "vendor" sends an invoice requesting immediate payment, however the payment details have been manipulated to route to the attackers account.

#### 4) Malicious Attachments
These emails contain seemingly benign attachments such as PDFs, Word Documents etc. These contain embedded malware or scripts to execute when opened or downloaded. these can be combined with BEC to initiate malware deployment on an organizations network. Such as a malicious invoice, PDF or word doc.

#### 5) Scareware
These emails leverage fear to manipulate users to engage, such as fake warnings or emergencies about account compromise or unpaid bills. These would say something like "Your account has been locked! click here to verify this was you". I have seen a trend of attackers faking social media email comms for this like X, Facebook and Instagram. These can be almost identical to the entity they are imitating.

## Why Email Attacks Are Successful

If you are like me, you have to think why the hell are these successful in the first place? lets look at this together, shall we?

1) **Social engineering**: Attackers exploit our basic psychology. They leverage emotion to break us out of logical decision making and reasoning. Like discussed above they pressure you to make an urgent decision or gain trust by claiming they are some one you trust and exploit you that way. 

2) **Lacking awareness**: Lets face it, many people are not properly trained in detecting suspicious emails. This can be due to poor employee practices in and outside of the work place. If you are clicking on sus emails outside of work and bringing that behavior to the place of business, its only a matter of time. You are effectively a ticking risk bomb for your company. I'll restate that it not exclusive to general employees, this includes all of you in the C-Suite. Awareness is key!

3) **Weak Email Configurations**: Improperly configured email systems will drop the defenses for detecting and blocking malicious emails. This can be the result of running on defaults through your firewall and email gateways. Without enabling the appropriate protocols you leave yourself vulnerable to this attack vector.

## How to Defend Against the Phish

Now that we know what we are facing, how do we defend against email attacks? First we have to face reality, obtaining 100% defense against email attacks is practically impossible. However you can have a strong defense against it through training and preparing for the worse case scenario. 

#### **1) Implement Strong Email Security Protocols:**
* **Enable Multi-Factor Authentication** 
* **Utilize Email Filters**
* **Adopt DMARC, SPF, and DKIM Protocols**
#### **2) Train Employees**
* Regularly educate employees about identifying and reporting phishing emails, malicious links
* This can be bland if done by the book, explore bounties out internally and reward employees for reporting suspicious behavior. 
* Employees who are properly trained can reduce susceptibility by almost 20% after a failed simulation and can significantly reduce your organizations standard time for detection of a breach. the current 2024 mean is 194 Days. 
* Quarterly simulation campaigns can give greater insights to what users respond to, providing valuable data for your security team.
#### **3) Regular Software Updates**
* Ensure all email servers, endpoints, and security tools are updated to patch known vulnerabilities.
* Follow media outlets and vendors for current vulnerabilities out in the wild.
#### **4) Monitor and Respond**
* Utilize Security Information and Event Management (SIEM) tools to detect anomalies in email activity.
* Respond accordingly if a user falls for a phish, it doesn't help to respond with negative emotions. I believe its better to educate and enforce than to punish and victim shame. If you do the latter, just remember you are also a victim. 
#### **5) Backup Data**
* As mentioned before you cannot defend absolutely against email attacks, yet. So it is imperative to perform regular backups.
* Test your backup procedures and ensure that in the event of a cyberattack or even a natural disaster, your backups can be deployed and retore operations.
* Store backup data off-site and or off network so in the event of a breach or ransomware attack you don't also lose your backups

## Closing Thoughts

Email security is a critical line of defense against cyberattacks. By understanding the methodology and tactics threat actors use and taking proactive measures, individuals and organizations can significantly reduce their risk. The key is vigilance, ongoing education, and leveraging the right technologies to secure this vulnerable communication channel. 
 
 If you'd like to learn more about email security or discuss strategies to protect your organization, feel free to reach out to me. 

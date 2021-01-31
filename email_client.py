import os
import re
import ssl
import datetime
import mailparser
import imapclient 
import smtplib
import json
from ping3 import ping, verbose_ping

class Authentication:
    def __init__(self, imap, smtp, username, password):
        self.imap = imap
        self.smtp = smtp
        self.username = username
        self.password = password

class Message:
    def __init__(self, uid, timestamp, origin, destination, subject, body):
        self.uid = uid
        self.timestamp = timestamp
        self.origin = origin
        self.destination = destination
        self.subject = subject
        self.body = body

# Input: Instance of Message object and Authentication object
# Output: Boolean based on sending success or not
def send_message(auth, mess):
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(auth.smtp, 465, context=context) as server: #465 is smtp port
            server.login(auth.username, auth.password)
            server.sendmail(auth.username, mess.destination, mess.body)
            return True
    except:
        return False

# Input: Instance of Autentication object
# Output: List of Message objects
def download_messages(auth, folder):
    with imapclient.IMAPClient(auth.imap) as server:
        server.login(auth.username, auth.password)
        server.select_folder(folder, readonly=True)
        messages = server.search('ALL')
        email_message_list = []
        for uid, message_data in server.fetch(messages, 'RFC822').items():
            email_message = mailparser.parse_from_bytes(message_data[b'RFC822'])
            m = Message(uid, email_message.date, email_message.from_[0][1], 'inbox', email_message.subject, email_message.body)
            email_message_list.append(m)
        return email_message_list

# Input: string email adres
# Output: True if email is valid 
def check_email(em):
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    if(re.search(regex,em)):  
        return True
    else:  
        return False

# Input: string domain name
# Output: True if domain is up
def check_domain(dom):
    response = os.system("ping -c 1 " + dom)
    if response == 0:
        return True
    else:  
        return False
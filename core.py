import email_client
import web_api
import datetime

# DEBUG DEBUG
demo_authentication = email_client.Authentication('imap.mail.yahoo.com','smtp.mail.yahoo.com', 'EMAIL@yahoo.com', 'PASSWORD')
demo_message = email_client.Message(21, '2020-09-20 14:21:40', demo_authentication.username, demo_authentication.username, 'nieuw titel niuewe mail.', 'Subject: nieuw titel niuewe mail.\n\n een teste')

now = datetime.datetime.now()
current_time = now.strftime("%H:%M:%S")

print('Welcome! The time is', current_time)

txt0 = input("Print inbox (y/n): ")
if txt0  == 'y':
    for email in email_client.download_messages(demo_authentication,'INBOX'):
        print(email.uid)
        print(email.timestamp)
        print(email.body)
        print('')

txt1 = input("Send an email (y/n): ")
if txt1 == 'y':
    to = input("To: ")
    subject = input('Subject: ')
    message = input('Message: ')
    email = 'Subject: %s \n\n %s ' % (subject, message)
    new_message = email_client.Message(21, current_time, demo_authentication.username, to, email)
    email_client.send_message(demo_authentication, new_message)

txt2 = input("Print JSON (y/n): ")
if txt2 == 'y':
    print(web_api.object_to_json(email_client.download_messages(demo_authentication, 'INBOX')))

print('quit')

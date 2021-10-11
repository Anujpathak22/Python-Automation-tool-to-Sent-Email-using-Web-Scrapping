from email.mime import text

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime
now = datetime.datetime.now()

content = ''

def extract_NEWS(url):
    print("Extracting new Stories from your fav website")
    cnt = ''
    cnt += ('<b>  Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content,'html.parser')
    for i, tag in enumerate(soup.find_all('td',attrs={'class':'title' , 'valign':''})):
        cnt += ((str(i+1)+ ' :: '+tag.text + "\n" + '<br>') if tag.text != 'More' else '')
    return cnt


cnt = extract_NEWS('https://news.ycombinator.com/')
content+= cnt
content+=('<br>--------<br>')
content+=('<br><br>End of the message')

# lets send email;

print('composing email')

SERVER = 'smtp.gmail.com' # "your smtp server"
PORT = 587 # your port number
FROM =  'Senders gmail' # "your from email id"
TO = 'Recievers gmail' # "your to email ids"  # can be a list
PASS = '******' # "your email id's password"

msg = MIMEMultipart()

msg['Subject'] = 'Top News Stories of HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg ['From'] = FROM
msg['TO'] = TO

msg.attach(MIMEText(content, 'html'))

print('initialzing server....')

server = smtplib.SMTP(SERVER, PORT)
# server = smtplib.SMTP_SSL('smtp.gmail.com',465)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM,PASS)
server.sendmail(FROM, TO, msg.as_string())


print('Email Sent....')
server.quit()
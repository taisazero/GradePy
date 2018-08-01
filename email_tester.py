import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

email_user = 'odysseyoutreach@gmail.com'
email_password = 'yrnamessohard'
email_send = ['ddesai14@uncc.edu','ealhossa@uncc.edu', 'abenedi3@uncc.edu','abenedi4@uncc.edu','rcalcamo@uncc.edu','rduane@uncc.edu','jlaivins@uncc.edu','jhutch50@uncc.edu','elayer@uncc.edu','jjenki70@uncc.edu','tobarows@uncc.edu','tpatil@uncc.edu','ssefidid@uncc.edu','rcolli27@uncc.edu','lfrazi18@uncc.edu','gbrown57@uncc.edu','ipoliako@uncc.edu','hwei3@uncc.edu','swiktor@uncc.edu','sdybka@uncc.edu','akenne36@uncc.edu','voza@uncc.edu','ywang131@uncc.edu','cbehdani@uncc.edu','qscott3@uncc.edu','cwisnie1@uncc.edu','ysaleh@uncc.edu','msalad@uncc.edu']

subject = 'Odyssey Outreach Bot: Odyssey Hack'

msg = MIMEMultipart()
msg['From'] = 'odysseyoutreach@gmail.com'
msg['To']= 'ealhossa@uncc.edu'
msg['Bcc'] = ", ".join(email_send)
msg['Subject'] = subject
print(len(email_send))
print(", ".join(email_send))
body = 'Hi there, This is an auto-generated message from Odyssey Outreach Bot.\n The following is a message from Erfan Al-Hossami, The President of Odyssey Outreach at UNC Charlotte.\n Please be sure to join us this Friday for Odyssey Outreach\'s: Odyssey Hack! \n More information can be found in the attached flyer. \nTo RSVP please be sure to join the following Discord server:  https://discord.gg/9wRhYMB '+ '\n If you have any questions please do not hesistate to contact us at: odysseyoutreach@gmail.com!\n Regards,\nOdyssey Bot'
msg.attach(MIMEText(body,'plain'))

filename='C:\\Users\\Zero\\Downloads\\odyssey hack.pdf'
attachment  =open(filename,'rb')

part = MIMEBase('application','octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition',"attachment; filename= "+'flyer.pdf')

msg.attach(part)
text = msg.as_string()
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_user,email_password)


server.sendmail(email_user,email_send,text)
server.quit()
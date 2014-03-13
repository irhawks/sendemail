#!/usr/bin/env python
# -*- coding: utf-8 -*-

# send email via my accont on the Internet.

import smtplib
import os 
import mimetypes
import argparse

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--subject", dest="subject",
		type=str, required=True, help="Subject of email.")
parser.add_argument("-c", "--content", dest="content",
		type=str, required=True, help="Content of email.")
parser.add_argument("-a", "--attachment", nargs="+", dest="attach_files",
		help="Attachment file.")
parser.add_argument("-t", "--to", nargs="+", dest="sendto_list",
		required=True, help="Destination.")

args = parser.parse_args()

from_addr = 'istahawk@gmail.com'
to_addrs = args.sendto_list
date = formatdate(localtime=True)
subject = args.subject

message = MIMEMultipart()
message['From'] = from_addr
message['To'] = COMMASPACE.join(to_addrs)
message['Date'] = date
message['Subject'] = subject

print args.content
body = MIMEText(args.content, 'plain', 'utf-8')
message.attach(body)

for f in args.attach_files:
	guessed = mimetypes.guess_type(f)[0]
	if guessed != None:
		attachment = MIMEBase(guessed.split('/')[0], guessed.split('/')[1])
		attachment.set_payload(open(f, 'rb').read())
		Encoders.encode_base64(attachment)
		attachment.add_header('Content-Disposition',
				'attachment; filename="%s"' % os.path.basename(f))
		message.attach(attachment)

print "Begin to send email."
session = smtplib.SMTP_SSL('smtp.gmail.com')
session.login('istahawk', 'yourpasswordhere')
session.sendmail(from_addr, to_addrs, message.as_string())
session.close()

print "Done"

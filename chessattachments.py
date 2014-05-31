#first we get the libraries that will be needed
import email,getpass,imaplib,os

#folder where the attachments will be downloaded to 	
detach_dir = "."

username = raw_input("Please enter your gmail username : ")
password = getpass.getpass("Please enter your gmail password: ")

m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(username,password)


m.select("[Gmail]/All Mail")
resp,items = m.search(None,'FROM','"Chess.com"')
items = items[0].split()
for emailid in items:
	resp,data = m.fetch(emailid,"(RFC822)")
	email_body = data[0][1]
	mail = email.message_from_string(email_body)

	if mail.get_content_maintype() != 'multipart':
		continue

	print "["+mail["From"]+"]:" + mail["Subject"]

	for part in mail.walk():
		if part.get_content_maintype() == 'multipart':
			continue

		if part.get('Content-Disposition') is None:
			continue

		filename = part.get_filename()
		counter = 1

		if not filename:
			filename = 'part-%03d%s' % (counter,'bin')
			counter += 1
		att_path = os.path.join(detach_dir,filename)

		if not os.path.isfile(att_path):
			fp = open(att_path,'wb')
			fp.write(part.get_payload(decode=True))
			fp.close()

		 

#get the libraries that will be needed.imaplib implements a client for the gmail IMAP4 servers.
import email,getpass,imaplib,os

#folder where the attachments will be downloaded to.Defaults to the current folder.
detach_dir = "."

#get the user account details
hostname = "imap.gmail.com"
username = raw_input("Please enter your gmail username : ")
password = getpass.getpass("Please enter your gmail password: ")

#connect to the gmail imap server
m = imaplib.IMAP4_SSL(hostname)
m.login(username,password)

#Select a mailbox to act on e.g "INBOX".Returned data is the count of messages in mailbox.This selects all mail(duh).
#You can use m.list to view all other mailboxes.
m.select("[Gmail]/All Mail")

#Search the mailbox for messages matching the criteria.Returns count of messages as well.
#To view various imap search criteria check here:	http://www.example-code.com/csharp/imap-search-critera.asp
resp,items = m.search(None,'FROM','"Chess.com"')
#*********What does m.search return?
#*********split function
items = items[0].split()
for emailid in items:
	#The RFC822 means get everything in the mail.Headers/Content/Attachments etc
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

		 

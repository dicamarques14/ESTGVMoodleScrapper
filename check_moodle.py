import cookielib
import urllib
import urllib2
import ssl
import bs4
import time
from bs4 import BeautifulSoup as soup
import smtplib
from urlparse import urlparse

courselist = ["4224","4251","4402","4226","4280","4248","4218"]

# MOODLE PASSWORD
payload = {
  'username': 'estgvXXXXX',
  'password': 'CHANGEME' 
  }

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
	# Store the cookies and create an opener that will hold them
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx),urllib2.HTTPCookieProcessor(cj))

	# Add our headers
	opener.addheaders = [('User-agent', 'MoodleTesting')]

	# Install our opener (note that this changes the global opener to the one
	# we just made, but you can also just call opener.open() if you want)
	urllib2.install_opener(opener)

	# The action/ target from the form
	authentication_url = 'https://moodle.estgv.ipv.pt/201718/login/index.php'


	# Use urllib to encode the payload
	data = urllib.urlencode(payload)

	# Build our Request object (supplying 'data' makes it a POST)
	req = urllib2.Request(authentication_url, data)


	print("Checking...")
	resp = urllib2.urlopen(req)
	contents = resp.read()
	message = "Cadeiras com novidades: \n "

	for id in courselist:
		course_url = 'https://moodle.estgv.ipv.pt/201718/course/view.php?id=' + id

		# Build our Request object (supplying 'data' makes it a POST)
		req = urllib2.Request(course_url)

		# Make the request and read the response
		resp = urllib2.urlopen(req)
		contents = resp.read()
		page_soup = soup(contents, "html.parser")

		title = page_soup.findAll("title")[0].get_text()
		containers = page_soup.findAll("h3",{"class":"main"})
		print(title + " = " + str(len(containers)))
		#print(page_soup.findAll("div",{"class":"activityhead"})[0].get_text())
		#print(containers)
		#If it finds new activity
		if len(containers) > 0 :
			#debug = containers[0]
			#print(debug)
			#print(page_soup.findAll("div",{"class":"activityhead"})[0])
			#List all new act.
			updates = page_soup.findAll("p",{"class":"activity"})
			if len(updates) > 0:
				message = message + title +"\n"
				for update in updates:
					message = message+update.a.get_text()+"\n"
					print(update.a.get_text())
				
	print(message)	
	message = " "
	print("bye")
	time.sleep(300)


#Load Libraries
from __future__ import division
import csv, os, re, urllib2, urllib, requests, cookielib, mechanize, robotparser, time
from bs4 import BeautifulSoup

#Move to Work
os.chdir("C:\Users\lconsidine\Desktop\grcourt\grcourt")
print "We are in the right spot"

#Our source
gr_url = 'http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1'
nmax = 891429

#Get Cookie
r = requests.get('http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1')
headers = r.headers['set-cookie']
print headers

#Initialize opener add cookie
opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', headers))

#Recursive Tag Stripper for Later
def strip_tags(html, invalid_tags):
	soup = BeautifulSoup(html)
	for tag in soup.findAll(True):
		if tag.name in invalid_tags:
			s = ""
			for c in tag.contents:
				if not isinstance(c, NavigableString):
					c = strip_tags(c, invalid_tags)
				s += unicode(c)
			tag.replaceWith(s)
		return soup

invalid_tags = ["td"]


#Regular Expressions for Comments:
#<!-- DEFENDANT -->
#<!-- CHARGES --> 
#<!-- SENTENCE --> 
#<!-- BONDS --> 
#<!-- Register of Actions -->
#<!-- Case History -->

re_defendant = re.compile('<!-- DEFENDANT -->'(.*)'<!-- CHARGES -->')

def parse_gr(bsoup):
	data_medium = bsoup.find_all(class_="medium")
	for x in data_medium:
		for y in x.find_all("td"):
			print y.get_text(strip=True)

#StupidCrawl
count = 100012
while count < 100016:
	print 'On Case #:', count

	#Request Page
	f = opener.open('http://grcourt.org/CourtPayments/loadCase.do?caseSequence=' + str(count))
	soup = BeautifulSoup(f.read())
	
	#Storing the first b tag inside body to data_ccsort 
	data_ccsort = soup.body.b
	
	#If statement that sorts out civil cases 
	if data_ccsort.string == u'Civil Case View':
		print "Civil Case"
	   
	#Run Parser Function here:
		
		parse_gr(soup)
		
		with open("civil_out.csv", 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
			#writer.writerow([], [], [], []) choose fields here
			#writer.writerow() write 
			count +=1
			csvfile.close()
			time.sleep(2.5)
	else:
		print "Criminal Case"
	
	#Run Parser Function here
		
		parse_gr(soup)
		
		with open("criminal_out.csv", 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
			#writer.writerow([], [], [], []) choose fields here
			#writer.writerow() write returned values from parse_gr
		
		
		
			count +=1
			
			time.sleep(2.5)
	#print type(data_medium)

	#for data in data_medium:
	#  print (data.prettify())

########################################################################################
# Parse Robots:
# rp = robotparser.RobotFileParser()
# rp.set_url("http://neuro.compute.dtu.dk/robots.txt")
# rp.read()
# rp.can_fetch("*", "http://neuro.compute.dtu.dk/wiki/Special:Search")

# Mechanize Library #
# url = "http://www.grcourt.org/CourtPayments/loadCase.do?caseSequence=11"
# br = mechanize.Browser()
# #br.set_all_readonly(False)    # allow everything to be written to
# br.set_handle_robots(False)   # ignore robots
# br.set_handle_refresh(False)  # can sometimes hang without this
# br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]           # [('User-agent', 'Firefox')]
# response = br.open(url)
# print response.read()      # the text of the page
# response1 = br.response()  # get the response again
# print response1.read()     # can apply lxml.html.fromstring()

# user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
# headers = { 'JSESSIONID' : 'aaa1sKrRjU2bs7NGIotFu' }
# req = urllib2.Request("http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1", None, headers)
# response = urllib2.urlopen(req)
# page = response.read()
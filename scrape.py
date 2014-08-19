import csv, os, re, urllib2, urllib, requests, cookielib, mechanize, robotparser
#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
os.chdir("C:\Users\lconsidine\Desktop\grcourt\grcourt")
print "We are in the right spot"

#Raw Cookie:
#grcourt.org	FALSE	/	FALSE	0	JSESSIONID	aaaW_77Tib_t2cdMIotFu

opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', 'JSESSIONID=aaaW_77Tib_t2cdMIotFu'))
f = opener.open('http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1')
print f.read()

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
#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import csv, os, re, urllib2, urllib, requests, cookielib, mechanize, robotparser, time, random, string, sys, sqlite3, codecs
from bs4 import BeautifulSoup

conn = sqlite3.connect('example.db')
c = conn.cursor()
	
c.execute('DROP TABLE IF EXISTS defendant')
c.execute('DROP TABLE IF EXISTS case_info')
c.execute('DROP TABLE IF EXISTS charge')
c.execute('DROP TABLE IF EXISTS sentence')
c.execute('DROP TABLE IF EXISTS bonds')
c.execute('DROP TABLE IF EXISTS roa')

c.execute('CREATE TABLE defendant (defendant_id INTEGER PRIMARY KEY, Name_Full TEXT, Case_Number TEXT, Language TEXT, Mailing_Address TEXT, Race TEXT, Sex TEXT, Height TEXT, DOB TEXT, Weight TEXT, Hair TEXT, Eyes TEXT, Attorney TEXT, Firm TEXT, Attorney_Phone TEXT, Judge TEXT)')
c.execute('CREATE TABLE case_info (defendant_id INTEGER, Case_Number TEXT, Attorney TEXT, Firm TEXT, Attorney_Phone TEXT, Judge TEXT, FOREIGN KEY(defendant_id) REFERENCES defendant(defendant_id))')
c.execute('CREATE TABLE charge (charges_id INTEGER PRIMARY KEY, Case_Number TEXT, Offense_Date TEXT, Date_Closed TEXT, Offense TEXT, Description TEXT, Disposition TEXT, Disposition_Date, FOREIGN KEY(Case_Number) REFERENCES case_info(Case_Number))')
c.execute('CREATE TABLE sentence (sentence_id INTEGER PRIMARY KEY, Case_Number TEXT, Fines TEXT, Jail_Days TEXT, Probation TEXT, Balance_Due TEXT, FOREIGN KEY(Case_Number) REFERENCES case_info(Case_Number))')
c.execute('CREATE TABLE bonds (bonds_id INTEGER PRIMARY KEY, Case_Number TEXT, Date_Issued TEXT, Type TEXT, Amount TEXT, Posted_Date TEXT, FOREIGN KEY(Case_Number) REFERENCES case_info(Case_Number))')
c.execute('CREATE TABLE roa (Case_Number TEXT, Date_Issued TEXT, Action TEXT, Judge TEXT, FOREIGN KEY(Case_Number) REFERENCES case_info(Case_Number))')

conn.commit()

print"AM IAM HERE ========, ",  os.getcwd()
try:
	os.remove("criminal_out.csv")
except OSError:
	pass

#Our source
# gr_url = 'http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1'
# nmax = 891429

#Get Cookie
# r = requests.get('http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1')
# headers = r.headers['set-cookie']
# print headers

#Initialize opener add cookie
# opener = urllib2.build_opener()
# opener.addheaders.append(('Cookie', headers))

#Initialize 
# criminal_out = open("criminal_out.csv", 'ab')
# with criminal_out as csvfile:
	# writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
	# writer.writerow(["Defendant", "Case Number", "Language", "Mailing Address", "Race", "Sex", "Height", "DOB", "Weight", "Hair", "Eyes", "Attorney", "Firm", "Attorney Phone", "Judge", "OffenseDate", "DateClosed", "OffenseDescription", "Disposition", "DispositionDate", "Fines", "Jail Days", "Probation", "Balance Due", "Bench Warrant Issued", "DateIssued", "Type", "Amount", "PostedDate"])


def stable_table(regex_return, sec_list):		
	for item in regex_return:
		item = item.replace('\xa0', '')
		item = item.replace('\xc2', '')
		table_soup = BeautifulSoup(item)
		for x in table_soup.find_all(class_="medium"):
			for td_tag in x.find_all("td"):
				sec_list.append(str(td_tag.get_text(strip=True)))
		return sec_list

def stable_table_address(regex_return, sec_list):		
	for item in regex_return:
		item = item.replace('<br/>', ' ')
		table_soup = BeautifulSoup(item)
		for x in table_soup.find_all(class_="medium"):
			for td_tag in x.find_all("td"):
				sec_list.append(str(td_tag.get_text(strip=True)))
		return sec_list			
				
def handle_mult(section_inf, next_list, fields):
	numb = int(len(section_inf)/fields)
	s_index = 0
	e_index = fields
	next_list = []
	for case in range(numb):
		next_list.append(tuple(section_inf[s_index:e_index]))
		s_index += fields
		e_index += fields
	return next_list				
		
count = 1
		
while count < 5:
	print 'On Case #:', count
	#criminal_out = open("criminal_out.csv", 'ab')
	#Request Page
	f = codecs.open("./DataMob/" + str(count) + ".html", "r",encoding='utf-8')
	bsoup = BeautifulSoup(f.read())
	#global problems
	#problems = []
	#Storing the first b tag inside body to data_ccsort 
	data_ccsort = bsoup.body.b
	
	#If statement that sorts out civil cases 
	if data_ccsort.string == u'Civil Case View':
		print "Civil Case Continue..." 
		count +=1
		print "ZZZZZZZ..."
		time.sleep(2.5)
	elif data_ccsort.string == 'Unable to load case data':
		print "Unable to load case data"
		count +=1
		print "ZZZZZZZ..."
		time.sleep(2.5)
	else:
		print "Criminal Case"
	
	#Run Parser Function here
		#Possible Solution for clearing &nbsp
		#soup = soup.prettify(formatter=lambda s: s.replace(u'\xa0', ' '))
		#soup = soup.prettify(formatter=lambda s: s.replace(u'\xc2', ''))
	
		data_medium = bsoup.find_all(class_="medium")
		data_XLheader = bsoup.find_all(class_="extralarge")
		data_ccsort = bsoup.body.b
		print data_ccsort.string
		
		print "+++++++++DEFENDANT+++++++++++++++"		
		def_list = []
		regex_defendant = re.compile(r'.*<!-- DEFENDANT -->(.*)<!-- CHARGES -->.*', re.DOTALL)
		sec_defendant = regex_defendant.findall(str(bsoup))
		section_defendant = stable_table_address(sec_defendant, def_list)
		str_def = str(section_defendant[3]).replace('\n', ' ')
		section_defendant[3] = ' '.join(str_def.split())
		print section_defendant, '\n'
		sdef_t = (count, section_defendant[0], section_defendant[1], section_defendant[2], section_defendant[3], section_defendant[4], section_defendant[5], section_defendant[6], section_defendant[7], section_defendant[8], section_defendant[9], section_defendant[10], section_defendant[11], section_defendant[12], section_defendant[13], section_defendant[14])
		
		print "TUPLE ---- **********CHARGES******************** ---- TUPLE"
		charge_list = []
		regex_charges = re.compile(r'.*<!-- CHARGES -->(.*)<!-- SENTENCE -->.*', re.DOTALL)
		sec_charges = regex_charges.findall(str(bsoup))
		section_charges = stable_table(sec_charges, charge_list)
		section_charges = handle_mult(section_charges, [], 5)
		print section_charges, '\n'
			
		
		print "+++++++++++++++++SENTENCE+++++++++++++++"
		sen_list = []
		regex_sentence = re.compile(r'.*<!-- SENTENCE -->(.*)<!-- BONDS -->.*', re.DOTALL)
		sec_sentence = regex_sentence.findall(str(bsoup))
		section_sentence = stable_table(sec_sentence, sen_list)
		count_fields = 0
		for x in section_sentence:
			x = str(x).replace('\n', ' ')
			x = ' '.join(x.split())
			section_sentence[count_fields] = x
			count_fields += 1
		print section_sentence, '\n'	
		
		print "TUPLE ---- +++++++++++++BONDS+++++++++++++++++++++ ---- TUPLE"
		bonds_list = []
		regex_bonds = re.compile(r'.*<!-- BONDS -->(.*)<!-- Register of Actions -->.*', re.DOTALL)
		sec_bonds = regex_bonds.findall(str(bsoup))
		section_bonds = stable_table(sec_bonds, bonds_list)
		count_fields = 0
		for x in section_bonds:
			x = str(x).replace('\n', ' ')
			x = ' '.join(x.split())
			section_bonds[count_fields] = x
			count_fields += 1
		section_bonds = handle_mult(section_bonds, [], 4)
		print handle_mult(section_bonds, [], 4), '\n'
		
		print "TUPLE ---- +++++++++++++Case History+++++++++++++++++++++ ---- TUPLE"
		case_list = []
		regex_casehist = re.compile(r'.*<!-- Case History -->(.*)<!-- END Main -->.*', re.DOTALL)
		sec_casehist = regex_casehist.findall(str(bsoup))
		section_casehist = stable_table(sec_casehist, case_list)
		section_casehist = handle_mult(section_casehist, [], 4)
		print section_casehist, '\n'
		
		# with criminal_out as csvfile:
			# writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
			# try: 
		
		# run select defendant_id from defendant based on Defendant name, addr, dob
		# store id in a variable
		# if id var not > 0
		# insert into
		# get the id from insert and store in id variable
		
		c.execute('INSERT INTO defendant VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', sdef_t)
		c.execute('INSERT INTO case_info VALUES (?,?,?,?,?,?,?,?,?,?,?)', cinfo_t)
		conn.commit()
		#id = c.commit();
		# c.execute('INSERT INTO charges VALUES (?,?,?,?)', 
		
		
		
		count += 1
		print count
		time.sleep(2.5)
#print problems, "Problem child?"
#criminal_out.close()

# -*- coding: utf-8 -*

import scraperwiki
import mechanize
import lxml.html
import re
import time
import datetime

today_date = str(datetime.date.today())

#
#update_statement= 'update names SET last_scraped="2011-05-13" WHERE id=107041'
#scraperwiki.sqlite.execute(update_statement)
#scraperwiki.sqlite.commit()
#exit()

#record = {}
#record['last_name_collection'] = today_date
#scraperwiki.sqlite.save(['last_name_collection'], data=record, table_name='runtime_info')
#exit()

days_between_name_collection = int(30)
days_between_info_collection = int(7) #for now - will change to 7 when everything has been done once
compare_date= scraperwiki.sqlite.select('last_name_collection from runtime_info')
compare_date = str(compare_date[0]['last_name_collection'])

starturl = 'http://www.europarl.europa.eu/members/public/yourMep/search.do?name=*&partNumber=1&language=EN'
regex_id = re.compile("id=(\d.*)")
regex_id2 = re.compile("&id=(\d.*)")
regex_page_number = re.compile("&partNumber=(\d+)")
regex_birth_date = re.compile("Born on (.*),")
regex_birth_place = re.compile(", (.*)")

print "The date is", today_date

# TIME STUFF
y1, m1, d1 = (int(x) for x in compare_date.split('-'))
y2, m2, d2 = (int(x) for x in today_date.split('-'))
date1 = datetime.date(y1, m1, d1)
date2 = datetime.date(y2, m2, d2)
dateDiff = date2 - date1

#MEP NAME COLLECTION
def name_collection(page):
    print 'Processing page: ', regex_page_number.findall(page)[0]
    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
    response = br.open(page)
    html = response.read()
    root = lxml.html.fromstring(html)
    mps = root.xpath ('//td[contains(@class,"listcontentlight_left")]/. | //td[contains(@class,"listcontentdark_left")]/.')
    for mp in mps:
        record = {}
        name = mp[0].text_content().split(',')
        record['lastname'] = name[0]
        record['firstname'] = name[1]
        url = mp[0].get('href')
        id = regex_id2.findall(url)
        url = 'http://www.europarl.europa.eu/members/public/yourMep/view.do?id=' + id[0]
        record['detail_url'] = url
        record['id'] = id[0]
        record['last_scraped'] = today_date
        scraperwiki.sqlite.save(['id'], data=record, table_name='names')
    next_page_link = root.xpath('/html/body/table[@class="printablecontent" and position()=2]/tr/td[2]/table[3]//*[preceding-sibling::span[@class="alpha_selected"]][1]')
    if not next_page_link:
        print 'This was the last result page. Quitting the MEP name collection'
        update_statement= 'update runtime_info SET last_name_collection=' + '"' + today_date + '"'
        scraperwiki.sqlite.execute(update_statement)
        scraperwiki.sqlite.commit()
        return
    else:
        next_page_link = next_page_link[0].get('href')
        next_page_link = 'http://www.europarl.europa.eu' + next_page_link
        name_collection(next_page_link)

# QUESTIONS COLLECTION
def question_collection(activity_url,id,firstname,lastname):
    html = scraperwiki.scrape(activity_url)
    root = lxml.html.fromstring(html)
    questions = root.xpath ('//table[@class="longlistdark"] | //table[@class="longlistlight"]')
    for q in questions:
        questions_record = {}
        questions_record['subject'] = q[1][0].text.strip()
        questions_record['date'] = q[2][0].text.strip()
        questions_record['detail_url'] = 'http://www.europarl.europa.eu' +q[2][1][0][0][0][0].get('href') 
        questions_record['mep_last_name'] = lastname
        questions_record['mep_first_name'] = firstname
        questions_record['id'] = id        
        scraperwiki.sqlite.save(['id', 'subject'], data=questions_record, table_name='questions')

    current_page = root.xpath ('//a[@class="selector_selected"]')
    if current_page:
        next_page_number = int(current_page[0].text)+1
        xpath='//a[@class="selector_lnk" and contains(text(),"'+str(next_page_number)+'")]'
        next_page_link = root.xpath (xpath)
        next_page_link2 = root.xpath('//img[@src="/img/cont/activities/navigation/navi_next_activities.gif"]') #more than 15 result pages
        if next_page_link:
            next_page_link = 'http://www.europarl.europa.eu' + next_page_link[0].get('href') 
            question_collection(next_page_link,id,firstname,lastname)
        elif next_page_link2:
            next_page_link = root.xpath ('//img[@src="/img/cont/activities/navigation/navi_next_activities.gif"]/../..')
            next_page_link = 'http://www.europarl.europa.eu' + next_page_link[0][0].get('href') 
            question_collection(next_page_link,id,firstname,lastname)
        else:
            return

#OPINIONS COLLECTION
def opinion_collection(activity_url,id,firstname,lastname):
    html = scraperwiki.scrape(activity_url)
    root = lxml.html.fromstring(html)
    opinions = root.xpath ('//table[@class="longlistdark"] | //table[@class="longlistlight"]')
    for o in opinions:
        opinions_record = {}
        opinions_record['subject'] = o[4][0].text.strip()
        opinions_record['committee'] = o[5][0].text.strip()
        opinions_record['date'] = o[2][0].text.strip()
        opinions_record['word_url'] = 'http://www.europarl.europa.eu' + o[2][1][0][0][1][0].get('href') #oh isn´t this a fun way!
        opinions_record['pdf_url'] = 'http://www.europarl.europa.eu' + o[2][1][0][0][1][0].get('href').replace('+WORD+','+PDF+')
        opinions_record['mep_last_name'] = lastname
        opinions_record['mep_first_name'] = firstname
        opinions_record['id'] = id        
        scraperwiki.sqlite.save(['id', 'subject'], data=opinions_record, table_name='opinions')

    current_page = root.xpath ('//a[@class="selector_selected"]')
    if current_page:
        next_page_number = int(current_page[0].text)+1
        xpath='//a[@class="selector_lnk" and contains(text(),"'+str(next_page_number)+'")]'
        next_page_link = root.xpath (xpath)
        next_page_link2 = root.xpath('//img[@src="/img/cont/activities/navigation/navi_next_activities.gif"]') #more than 15 result pages
        if next_page_link:
            next_page_link = 'http://www.europarl.europa.eu' + next_page_link[0].get('href') 
            opinion_collection(next_page_link,id,firstname,lastname)
        elif next_page_link2:
            next_page_link = root.xpath ('//img[@src="/img/cont/activities/navigation/navi_next_activities.gif"]/../..')
            next_page_link = 'http://www.europarl.europa.eu' + next_page_link[0][0].get('href') 
            opinion_collection(next_page_link,id,firstname,lastname)
        else:
            return

#SPEECHES COLLECTION
def speeches_collection(activity_url,id,firstname,lastname):
    html = scraperwiki.scrape(activity_url)
    root = lxml.html.fromstring(html)
    speeches = root.xpath ('//table[@class="longlistdark"] | //table[@class="longlistlight"]')
    for s in speeches:
        speeches_record = {}
        speeches_record['subject'] = s[1][0].text.strip()
        speeches_record['date'] = s[2][0].text.strip()
        speeches_record['detail_url'] = 'http://www.europarl.europa.eu' +s[2][1][0][0][0][0].get('href') 
        speeches_record['mep_last_name'] = lastname
        speeches_record['mep_first_name'] = firstname
        speeches_record['id'] = id        

        scraperwiki.sqlite.save(['id', 'subject'], data=speeches_record, table_name='speeches')

    current_page = root.xpath ('//a[@class="selector_selected"]')
    if current_page:
        next_page_number = int(current_page[0].text)+1
        xpath='//a[@class="selector_lnk" and contains(text(),"'+str(next_page_number)+'")]'
        next_page_link = root.xpath (xpath)
        next_page_link2 = root.xpath('//img[@src="/img/cont/activities/navigation/navi_next_activities.gif"]') #more than 15 result pages
        if next_page_link:
            next_page_link = 'http://www.europarl.europa.eu' + next_page_link[0].get('href') 
            speeches_collection(next_page_link,id,firstname,lastname)
        elif next_page_link2:
            next_page_link = root.xpath ('//img[@src="/img/cont/activities/navigation/navi_next_activities.gif"]/../..')
            next_page_link = 'http://www.europarl.europa.eu' + next_page_link[0][0].get('href') 
            speeches_collection(next_page_link,id,firstname,lastname)
        else:
            return
        
#REPORTS COLLECTION
def reports_collection(activity_url,id,firstname,lastname):
    html = scraperwiki.scrape(activity_url)
    root = lxml.html.fromstring(html)
    reports = root.xpath ('//table[@class="longlistdark"] | //table[@class="longlistlight"]')
    for r in reports:
        reports_record = {}
        reports_record['subject'] = r[4][0].text.strip()
        reports_record['committee'] = r[3][0].text.strip()
        reports_record['date'] = r[2][0].text.strip()
        reports_record['word_url'] = 'http://www.europarl.europa.eu' + r[2][1][0][0][1][0].get('href') #oh isn´t this a fun way!
        reports_record['pdf_url'] = 'http://www.europarl.europa.eu' + r[2][1][0][0][1][0].get('href').replace('+WORD+','+PDF+')
        reports_record['mep_last_name'] = lastname
        reports_record['mep_first_name'] = firstname
        reports_record['id'] = id        
        scraperwiki.sqlite.save(['id', 'subject'], data=reports_record, table_name='reports')

    current_page = root.xpath ('//a[@class="selector_selected"]')
    if current_page:
        next_page_number = int(current_page[0].text)+1
        xpath='//a[@class="selector_lnk" and contains(text(),"'+str(next_page_number)+'")]'
        next_page_link = root.xpath (xpath)
        next_page_link2 = root.xpath('//img[@src="/img/cont/activities/navigation/navi_next_activities.gif"]') #more than 15 result pages
        if next_page_link:
            next_page_link = 'http://www.europarl.europa.eu' + next_page_link[0].get('href') 
            reports_collection(next_page_link,id,firstname,lastname)
        elif next_page_link2:
            next_page_link = root.xpath ('//img[@src="/img/cont/activities/navigation/navi_next_activities.gif"]/../..')
            next_page_link = 'http://www.europarl.europa.eu' + next_page_link[0][0].get('href') 
            reports_collection(next_page_link,id,firstname,lastname)
        else:
            return

#MEP INDIVIDUAL INFO COLLECTION
def info_collection(url,firstname,lastname,id):
    record = {}
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    party = root.xpath ('//span[contains(@class,"titlemep")]/.')
    country = root.xpath ('//td[contains(@style,"width: 91%")]/text()')
    record['id'] = id
    record['detail_url'] = url
    record['firstname'] = firstname
    record['lastname'] = lastname
    record['country'] = country[0].strip()
    record['en_party_name'] = party[0].text_content().strip()
    record['en_party_role'] = party[1].text_content().strip()
    national_party_birth = root.xpath ('//comment()[.=" birth date, birth place"]//../text()')
    birth_place = national_party_birth[2].partition(',')[2].strip()
    birth_date = regex_birth_date.findall(national_party_birth[2].strip())
    record['birth_date'] = birth_date[0]
    record['birth_place'] = birth_place
    record['national_party_name'] = national_party_birth[1].strip() #.encode('ISO-8859-1')
    #print national_party[0].strip()   #.encode('ISO-8859-1') ??????
    member = root.xpath ('//td [contains(text(),"Member") and @colspan="2"]/../..//td[contains(@style,"width: 98%")]')
    if member:
        committee_member = []
        for m in member:
            committee_member.append(m.text.strip())
        record['committee_member'] = committee_member
    substitute = root.xpath ('//td [contains(text(),"Substitute") and @colspan="2"]/../..//td[contains(@style,"width: 98%")]')
    if substitute:
        substitute_member = []
        for s in substitute:
            substitute_member.append(s.text.strip())
        record['substitute_member'] = substitute_member
    activities = root.xpath ('//td [contains(text(),"Parliamentary activities") and @colspan="2"]/../..//td[contains(@style,"width: 98%")]')
    activities_list = []
    if activities:
        activities_list = []
        for a in activities:
            activity = a.text.strip()
            activities_list.append(activity)
            activity_url = 'http://www.europarl.europa.eu' + a[0].get('href')
            if activity.strip() == 'Questions':
                question_collection(activity_url,id,firstname,lastname)
                print 'Questions for ', firstname, ' ', lastname, ' have been processed'
            if activity.strip() == 'Opinions':
                opinion_collection(activity_url,id,firstname,lastname)
                print 'Opinions for ', firstname, ' ', lastname, ' have been processed'
            if activity.strip() == 'Speeches in plenary':
                speeches_collection(activity_url,id,firstname,lastname)
                print 'Speeches for ', firstname, ' ', lastname, ' have been processed'
            if activity.strip() == 'Reports':
                reports_collection(activity_url,id,firstname,lastname)
                print 'Reports for ', firstname, ' ', lastname, ' have been processed'
    else:
            activities_list = ''
    record['activitites'] = activities_list    
    scraperwiki.sqlite.save(['id'], data=record, table_name='meps')
    update_statement= 'UPDATE names SET last_scraped=' + '"' + today_date + '"' + ' WHERE id='+ '"' + id + '"'
    scraperwiki.sqlite.execute(update_statement)
    scraperwiki.sqlite.commit()
    print firstname, ' ', lastname, ' has been processed! On to the next one!'


# START
print 'Last name collection was %d days ago' % dateDiff.days

if int(dateDiff.days) < days_between_name_collection:
    print "No name collection today. Next name collection in" , 30 - dateDiff.days, " day(s)"
    print 
    print 'Get MEPs that have not been updated in 7+ days (or so) and fetch their info'
    selection_statement = '* from names'
    #selection_statement = '* from names where id=96846' #debug

    names = scraperwiki.sqlite.select(selection_statement)
    for name in names:
        compare_date = name['last_scraped']
        y1, m1, d1 = (int(x) for x in compare_date.split('-'))
        y2, m2, d2 = (int(x) for x in today_date.split('-'))
        date1 = datetime.date(y1, m1, d1)
        date2 = datetime.date(y2, m2, d2)
        dateDiff = date2 - date1
        if int(dateDiff.days) < days_between_info_collection: #correct
        #if int(dateDiff.days) > days_between_info_collection: # wrong but used for initial run

            print name['firstname'], name['lastname'],  " is up to date. On to the next one"
        else:
            print name['firstname'], name['lastname'],  " Is not up to date. Let's process ..."
            info_collection(name['detail_url'],name['firstname'],name['lastname'],name['id'])
else:

    print "Yay! Name collection day! Let's go"
    name_collection(starturl)

import scraperwiki
import sys, httplib2, urllib, re, random, mechanize
from lxml import etree
import lxml.html

url = "http://business.gwu.edu/faculty/"
br = mechanize.Browser()
br.set_handle_robots(False)  # bypass robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Firefox')]  # Some websites demand a user-agent that isn't a robot

response = br.open(url)     
links = list(br.links(url_regex=".*\.cfm"))

def scrape(response):
        for link in links:
            resp = br.follow_link(link)
            resp2 = resp.get_data()
            doc = lxml.html.document_fromstring(resp2)
            records = doc.cssselect('div#moduleCM22')   #that's where all information is stored
            for r in records:
                data = {}
                data['key'] = random.random()
                for item1 in r.cssselect('div#moduleCM22 h3'): #name
                    data['name'] = item1.text
                for item2 in r.cssselect('div#moduleCM22'):    #to retrieve all items except the last item on page as bad html structure
                    item5 = lxml.html.tostring(item2)
                    str_h1 = re.findall(r'<strong>(.*?:.*?)</strong>', item5)       #will retrieve all items in bold
                    del str_h1[-1]     #to make lists even
                    str333 = ":"   
                    str_h1 = [string2 for string2 in str_h1 if string2 != str333] #remove strings with only colon (bad structure website)
                    #str555 = "<strong></strong>"
                    #str_h1 = [string3 for string3 in str_h1 if string3 != str555] #remove empty strings (bad structure website)
                    #str100 = "<strong> </strong>"
                    #str_h1 = [string10 for string10 in str_h1 if string10 != str100] #remove empty string with whitespace (bad structure website)
                    str_h2 = re.findall(':.*?</strong>(.*?)<strong>', item5, re.DOTALL)       #will retrieve all items except last one
                    for num in range(len(str_h1)):
                        check = str_h1[num]
                        res4 = re.compile('<.*?>|,.*|:.*?|&.*', re.DOTALL)       # get rid of everything except text
                        res5 = res4.sub('', check)
                        str106 = re.compile('^[\W_]+|[\W_]+$')
                        res5 = str106.sub('', res5)
                        text = str_h2[num]
                        str444 = re.compile('<.*?>|\n|\t|\r|\f|&#\d+;|"')
                        text2 = str444.sub('', text)
                        str101 = re.compile(r'&amp;')
                        text2 = str101.sub('and', text2)
                        text2 = str106.sub('', text2)
                        data[res5] = text2
                for item3 in r.cssselect('div#moduleCM22'):    #to retrieve the last item on page
                    item6 = lxml.html.tostring(item3)
                    str_h3 = re.search(r'<strong>.*', item6, re.DOTALL)
                    str_h3 = str_h3.group()
                    str_h4 = re.compile(r'<strong>.*<strong>', re.DOTALL)
                    str_h3 = str_h4.sub('', str_h3) 
                    strongTitle = re.search('.*</strong>', str_h3, re.DOTALL)
                    strongTitle2 = strongTitle.group()
                    str888 = re.compile(r':.*<.*?>|<.*?>', re.DOTALL)
                    strongName = str888.sub('', strongTitle2)
                    str105 = re.compile('^[\W_]+|[\W_]+$')
                    strongName = str105.sub('', strongName)
                    textL = re.search(r'</strong>.*', str_h3, re.DOTALL)
                    textL = textL.group()
                    str999 = re.compile('<.*?>|\n|\t|\r|\f|&#\d+;|"')
                    textLast = str999.sub('', textL)
                    str102 = re.compile(r'&amp;')
                    textLast = str102.sub('and', textLast)
                    textLast = str105.sub('', textLast)
                    data[strongName] = textLast
                
                scraperwiki.sqlite.save(["key"], data) #Store data in sqlite database
            #br.back()

scrape(response)
import scraperwiki
import sys, httplib2, urllib, re, random, mechanize
from lxml import etree
import lxml.html

url = "http://business.gwu.edu/faculty/"
br = mechanize.Browser()
br.set_handle_robots(False)  # bypass robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Firefox')]  # Some websites demand a user-agent that isn't a robot

response = br.open(url)     
links = list(br.links(url_regex=".*\.cfm"))

def scrape(response):
        for link in links:
            resp = br.follow_link(link)
            resp2 = resp.get_data()
            doc = lxml.html.document_fromstring(resp2)
            records = doc.cssselect('div#moduleCM22')   #that's where all information is stored
            for r in records:
                data = {}
                data['key'] = random.random()
                for item1 in r.cssselect('div#moduleCM22 h3'): #name
                    data['name'] = item1.text
                for item2 in r.cssselect('div#moduleCM22'):    #to retrieve all items except the last item on page as bad html structure
                    item5 = lxml.html.tostring(item2)
                    str_h1 = re.findall(r'<strong>(.*?:.*?)</strong>', item5)       #will retrieve all items in bold
                    del str_h1[-1]     #to make lists even
                    str333 = ":"   
                    str_h1 = [string2 for string2 in str_h1 if string2 != str333] #remove strings with only colon (bad structure website)
                    #str555 = "<strong></strong>"
                    #str_h1 = [string3 for string3 in str_h1 if string3 != str555] #remove empty strings (bad structure website)
                    #str100 = "<strong> </strong>"
                    #str_h1 = [string10 for string10 in str_h1 if string10 != str100] #remove empty string with whitespace (bad structure website)
                    str_h2 = re.findall(':.*?</strong>(.*?)<strong>', item5, re.DOTALL)       #will retrieve all items except last one
                    for num in range(len(str_h1)):
                        check = str_h1[num]
                        res4 = re.compile('<.*?>|,.*|:.*?|&.*', re.DOTALL)       # get rid of everything except text
                        res5 = res4.sub('', check)
                        str106 = re.compile('^[\W_]+|[\W_]+$')
                        res5 = str106.sub('', res5)
                        text = str_h2[num]
                        str444 = re.compile('<.*?>|\n|\t|\r|\f|&#\d+;|"')
                        text2 = str444.sub('', text)
                        str101 = re.compile(r'&amp;')
                        text2 = str101.sub('and', text2)
                        text2 = str106.sub('', text2)
                        data[res5] = text2
                for item3 in r.cssselect('div#moduleCM22'):    #to retrieve the last item on page
                    item6 = lxml.html.tostring(item3)
                    str_h3 = re.search(r'<strong>.*', item6, re.DOTALL)
                    str_h3 = str_h3.group()
                    str_h4 = re.compile(r'<strong>.*<strong>', re.DOTALL)
                    str_h3 = str_h4.sub('', str_h3) 
                    strongTitle = re.search('.*</strong>', str_h3, re.DOTALL)
                    strongTitle2 = strongTitle.group()
                    str888 = re.compile(r':.*<.*?>|<.*?>', re.DOTALL)
                    strongName = str888.sub('', strongTitle2)
                    str105 = re.compile('^[\W_]+|[\W_]+$')
                    strongName = str105.sub('', strongName)
                    textL = re.search(r'</strong>.*', str_h3, re.DOTALL)
                    textL = textL.group()
                    str999 = re.compile('<.*?>|\n|\t|\r|\f|&#\d+;|"')
                    textLast = str999.sub('', textL)
                    str102 = re.compile(r'&amp;')
                    textLast = str102.sub('and', textLast)
                    textLast = str105.sub('', textLast)
                    data[strongName] = textLast
                
                scraperwiki.sqlite.save(["key"], data) #Store data in sqlite database
            #br.back()

scrape(response)

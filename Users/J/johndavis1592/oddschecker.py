def frac2dec(odds):
    if odds.find('.') > 0: return odds
    
    try:
        odds = float(odds.split('/')[0])/float(odds.split('/')[1]) + 1
    except:
        odds = float(odds) + 1
    return odds

import scraperwiki
import re

#html = scraperwiki.scrape('http://www.oddschecker.com/football/english/championship/barnsley-v-cardiff-city/over-under-0.5')
import urllib
html = urllib.urlopen("http://www.oddschecker.com/football/english/championship/barnsley-v-cardiff-city/over-under-0.5").read()
#print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object

#headline = [el.text for el in root.xpath('//script[contains(@headline,"Under")]/text()"]')]
#scripts = root.cssselect('div.pg1 module') # get all the <td> tags
#for el.text in scripts: print el.text
#for headline in scripts print headline.text_content()

#type = list()
for elem in root.iter():
    if elem.tag == 'script':
        for ii in elem.items():
            if (ii[0].lower() == 'type'):
                type = re.findall(r'headline: \"(.*?)\"',elem.text_content())

type = filter(None, type) # fastest

print type

#for i in range(0, len(tmp)): print tmp[i]
#print tmp.text_content()
#print re.findall(r'headline: \"(.*?)\"',types[5])

#print type

bets = [el.text for el in root.xpath('//td[contains(@id,"name")]')]
#print bets

bet365 = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"B3")]/text()')]
skybet = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"SK")]/text()')]
totesport = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"BX")]/text()')]
boylesports = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"BY")]/text()')]
betfred = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"FR")]/text()')]
sportingbet = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"SO")]/text()')]
betvictor = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"VC")]/text()')]
bluesq = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"BS")]/text()')]
paddypower = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"PP")]/text()')]
stanjames = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"SJ")]/text()')]
eightbet = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"EE")]/text()')]
bwin = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"BW")]/text()')]
ladbrokes = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"LB")]/text()')]
oneeightbet = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"EB")]/text()')]
coral = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"CE")]/text()')]
williamhill = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"WH")]/text()')]
youwin = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"YW")]/text()')]
pinnacle = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"PN")]/text()')]
thirtytwored = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"RD")]/text()')]
betfair = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"BF")]/text()')]
wbx = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"WB")]/text()')]
betdaq = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"BD")]/text()')]
sportingindex = [frac2dec(el.rstrip()) for el in root.xpath('//td[contains(@id,"SI")]/text()')]

#print bet365
#print betvictor

if 'Under' in bets: overunder = True

for i in range(0, len(bets)):
    if overunder == True: j = i * 2 +1
    else: j = i
    
    data = {}
    data['bets'] = bets[i]
    if len(bet365) == 0: data['bet365'] = None 
    else: data['bet365'] = bet365[j]
    
    if len(skybet) == 0: data['skybet'] = None 
    else: data['skybet'] = skybet[j]

    if len(totesport) == 0: data['totesport'] = None 
    else: data['totesport'] = totesport[j]

    if len(boylesports) == 0: data['boylesports'] = None 
    else: data['boylesports'] = boylesports[j]

    if len(betfred) == 0: data['betfred'] = None 
    else: data['betfred'] = betfred[j]

    scraperwiki.sqlite.save(unique_keys = ['bets'], data = data) 
    

#for i in range(0, len(bets)):
    #data = {}
    #data['bet365'] = bet365[i]
    #data['skybet'] = skybet[i]
    #data['betfred'] = betfred[i]
    #data['winner'] = names[i]

    #scraperwiki.sqlite.save(unique_keys = ['winner'], data = data) 

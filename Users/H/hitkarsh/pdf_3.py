import scraperwiki
import lxml.html

url="http://dahd.nic.in/DistrictWiseReport/HTML/"
states=['Jammu and Kashmir.htm','Himachal Pradesh.htm','Punjab.htm','Chandigarh.htm','Uttarakhand.htm','Haryana.htm','Delhi.htm','Rajasthan.htm','Uttar Pradesh.htm','Bihar.htm','Sikkim.htm','Arunachal Pradesh.htm','Nagaland.htm','Manipur.htm','Mizoram.htm','Tripura.htm','Meghalaya.htm','Assam.htm','West Bengal.htm','Jharkhand.htm','Orissa.htm','Chattisgarh.htm','Madhya Pradesh.htm','Gujarat.htm','Daman.htm','Dadar.htm','Maharashtra.htm','Andhra Pradesh.htm','Karnatka.htm','Goa.htm','Lakhshdweep.htm','Kerela.htm','Tamilnadu.htm','Pondichery.htm','Andaman & Nicobar Islands.htm']
for i in states:
    print url+i
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
print url

for a in root.cssselect("tr"):
    tds = a.cssselect("td")
    if len(tds)==12:
        data = {
            '' : tds[0].text_content()
        }
        print data


import scraperwiki
import lxml.html

url="http://dahd.nic.in/DistrictWiseReport/HTML/"
states=['Jammu and Kashmir.htm','Himachal Pradesh.htm','Punjab.htm','Chandigarh.htm','Uttarakhand.htm','Haryana.htm','Delhi.htm','Rajasthan.htm','Uttar Pradesh.htm','Bihar.htm','Sikkim.htm','Arunachal Pradesh.htm','Nagaland.htm','Manipur.htm','Mizoram.htm','Tripura.htm','Meghalaya.htm','Assam.htm','West Bengal.htm','Jharkhand.htm','Orissa.htm','Chattisgarh.htm','Madhya Pradesh.htm','Gujarat.htm','Daman.htm','Dadar.htm','Maharashtra.htm','Andhra Pradesh.htm','Karnatka.htm','Goa.htm','Lakhshdweep.htm','Kerela.htm','Tamilnadu.htm','Pondichery.htm','Andaman & Nicobar Islands.htm']
for i in states:
    print url+i
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
print url

for a in root.cssselect("tr"):
    tds = a.cssselect("td")
    if len(tds)==12:
        data = {
            '' : tds[0].text_content()
        }
        print data



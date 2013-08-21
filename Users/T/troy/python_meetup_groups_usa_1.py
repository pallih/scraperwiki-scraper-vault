import scraperwiki
import lxml.html
import re

html = scraperwiki.scrape("http://referrals.meetup.com/all/")
root = lxml.html.fromstring(html)
ldata = [ ]
for li in root.cssselect('div.D_boxsection')[1].cssselect('li.vcard'):
    link = li.cssselect("div a")[0]
    data = {"name":link.text.strip(), "link":link.attrib.get('href')}
    smembers = li.cssselect("div.D_less span.note")[0].text.strip()
    mmembers = re.match("(\d+)\s+members", smembers)
    assert mmembers, smembers
    data["members"] = int(mmembers.group(1))

        # to do: separate the name into country code and state properly
    data["adr"] = li.cssselect("span.adr")[0].text_content().strip()
    #<span class="adr"><span class="locality">Seattle</span>, <span class="region">WA</span><span class="displaynone country-name">us</span></span>; <span class="note">147 members</span>

    data["latitude"] = float(li.cssselect("span.latitude")[0].text.strip())
    data["longitude"] = float(li.cssselect("span.longitude")[0].text.strip())
    ldata.append(data)

scraperwiki.sqlite.save(['name'], ldata, "newtable")


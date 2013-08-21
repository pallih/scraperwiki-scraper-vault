import scraperwiki

siteUrl = "http://www.legacyfundraising.com.au/nedlands_angry_nerds"

import lxml.html
import re
import urllib2

def getHtml(url):
    html = urllib2.urlopen(url)
    page = lxml.html.fromstring(html.read())
    html.close()

    return page

def processPage(url):
    html = getHtml(url)
    
    saveMembers(html)

    saveDonations(html)

def saveMembers(html):
    members = html.cssselect("div[id='team-members'] tr")

    for member in members:
        data = member.cssselect("td")

        name = data[0].text_content()
        total = cleanDollar(data[1].text_content())
    
        memberData = {'name': name,
                'total': total }

        scraperwiki.sqlite.save(unique_keys=['name'], data=memberData, table_name='team_members')

def saveDonations(html):
    donations = html.cssselect("table[id='hp-donations-table'] tr")

    for donation in donations:
        data = donation.cssselect("td")
        donationData = {'name': data[0].text_content().strip(),
                        'date': data[1].text_content().strip(),
                        'type': data[2].text_content().strip(),
                        'amount': cleanDollar(data[3].text_content()),
                        'message': data[4].text_content().strip() }

        print donationData

        scraperwiki.sqlite.save(unique_keys=['name', 'date', 'amount'], data=donationData, table_name='donations')
        

def cleanDollar(unclean):
    unclean = unclean.replace('$','')
    clean = unclean.replace('AUD','')
    return float(clean)

# Start the scrape
processPage(siteUrl)

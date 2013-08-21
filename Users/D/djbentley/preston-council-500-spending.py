import scraperwiki
import urllib
import re
import datetime
import csv
import mechanize


def cleanupdata(data):
    assert data['NET_Amount'][:1] == '\xa3', data['NET_Amount']
    data['NET_Amount'] = float(re.sub(',', '', data['NET_Amount'][1:]))
    mdate = re.match('(\d\d)/(\d\d)/(\d\d\d\d)$', data['Date Paid'])
    assert mdate, data['Date Paid']
    data['Date Paid'] = datetime.datetime(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))


br = mechanize.Browser()
br.open("http://www.preston.gov.uk/council-and-democracy/about-the-council/plans-and-spending/council-spending/")

accountlinks = [ ]
for link in br.links():
    if re.match('\w+ 20\d\d spending over \xc2\xa3500 \(csv\)', link.text):
        print len(accountlinks), link
        accountlinks.append(link)

for link in accountlinks:
    print "Doing link", link
    response = br.follow_link(link)
    clist = list(csv.reader(response.readlines()))
    headings = clist.pop(0)
    assert headings == ['Creditor Name', 'Voucher Ref', 'Date Paid', 'NET_Amount'], headings
    print "Number of rows:", len(clist)
    for row in clist:
        data = dict(zip(headings, row))
        cleanupdata(data)
        scraperwiki.datastore.save(unique_keys=['Voucher Ref'], data=data, date=data['Date Paid'])

    br.back()    



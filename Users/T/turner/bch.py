import scraperwiki
import lxml.html
import urllib
import json

def pass_row(root,token,role):
    results = []

    participants = root.cssselect("tr[id='%s_DRow']" % (token))

    for tr in participants:
        participant={}

        participant['role']=role

        name = tr.cssselect("div[id='%s_DName']" % (token))[0]
        participant['name'] = name.text_content().strip()

        email = tr.cssselect("div[id='%s_DEmail']" % (token))[0]
        participant['email'] = email.text_content().strip()

        country = tr.cssselect("div[id='%s_DCountry']" % (token))[0]
        participant['country'] = country.text_content().strip()

        org = tr.cssselect("div[id='%s_DOrganization']" % (token))[0]
        participant['org'] = org.text_content().strip()

        id = tr.cssselect("a[id='%s_DViewLink']" % (token))[0]
        participant['id'] = id.attrib['href'].split(",")[1].split("'")[1]

        scraperwiki.sqlite.save(unique_keys=["email"], data=participant)
        results.append(participant)
        #print participant
    return results


def pass_profile(id):
    html=scraperwiki.scrape("http://bch.cbd.int/database/record.shtml?documentID=%s" % (id))
    root = lxml.html.fromstring(html)
    reference_form = root.xpath("//td[text()='References']/ancestor-or-self::div[contains(@class, 'formSection')]")
    print "Reference form length: %d" % (len(reference_form))
    references = reference_form[0].cssselect("div[class='formElementContent'] table tr")
    print "References length: %d" % (len(references))
    references = map(lambda x: x.text_content().strip(), references)
    print list(set(references))
    for reference in list(set(references)):
        print reference
        
"""
/descendant::tr
html=scraperwiki.scrape("http://bch.cbd.int/onlineconferences/participants_ra.shtml")
root = lxml.html.fromstring(html)

pass_row(root,"ctl15_W34520","party")
pass_row(root,"ctl17_W36431","non-party")

observers = pass_row(root,"ctl19_W34519","observer")
for observer in observers:
    pass_profile(observer['id'])
"""

pass_profile("100122")
pass_profile("104567")


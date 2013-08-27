import scraperwiki
import simplejson
import urllib2
from bs4 import BeautifulSoup
import datetime
import time


def main():
    congress_number = [str(x) for x in range(110,112)]
    chamber = ['house','senate']
    bill_type = ['introduced','updated','passed']

    for congress in congress_number:
        for chamb in chamber:
            for bill_t in bill_type:
                api_call = 'http://api.nytimes.com/svc/politics/v3/us/legislative/congress/%s/%s/bills/%s.json?api-key=c886aef674b84bc2ce2f20439b7fff9c:12:66229250' % (congress,chamb,bill_t)
                time.sleep(1)
                congress_scrape(api_call,congress,chamb,bill_t)
                


def congress_scrape(api_call, congress, chamber,bill_type):
    results = simplejson.loads(scraperwiki.scrape(api_call))
    results = results['results'][0]['bills']
    for bill in results:
        bill_uri = bill['bill_uri']
        bill_number = bill['number']
        title = bill['title']
        committees = bill['committees']
        num_cosponsors = bill['cosponsors']
        last_action = bill['latest_major_action']
        date_last_action = bill['latest_major_action_date']
        time.sleep(1)
        if int(num_cosponsors) > 0:
            cosponsor_call = 'http://api.nytimes.com/svc/politics/v3/us/legislative/congress/%s/bills/%s/cosponsors.json?api-key=c886aef674b84bc2ce2f20439b7fff9c:12:66229250' % (congress, bill_number.replace(".",""))
            time.sleep(2)
            print cosponsor_call
            cosponsor_results = simplejson.loads(scraperwiki.scrape(cosponsor_call))['results'][0]
            sponsor = cosponsor_results['sponsor']
            sponsor_id = cosponsor_results['sponsor_id']
            #Cosponsers: List of dictionaries
            cosponsors = cosponsor_results['cosponsors']
            for cosponsor in cosponsors:
                dict_results = {"Bill_number":bill_number,'Title':title, 'Committee':committees,'Last_action':last_action, "Date_Last_action":date_last_action, "Sponsor":sponsor, "Sponsor_ID":sponsor_id, "Congress_Number":congress,"Chamber": chamber}
                cosponsor_id = cosponsor['cosponsor_id']
                cosponsor_name = cosponsor['name']
                dict_results['Cosponsor_ID'] = cosponsor_id
                dict_results["Cosponsor_Name"] = cosponsor_name
                dict_results["Unique"] = bill_number+cosponsor_id
                scraperwiki.sqlite.save(unique_keys=['Unique'], data = dict_results)
                    
    
main()
    import scraperwiki
import simplejson
import urllib2
from bs4 import BeautifulSoup
import datetime
import time


def main():
    congress_number = [str(x) for x in range(110,112)]
    chamber = ['house','senate']
    bill_type = ['introduced','updated','passed']

    for congress in congress_number:
        for chamb in chamber:
            for bill_t in bill_type:
                api_call = 'http://api.nytimes.com/svc/politics/v3/us/legislative/congress/%s/%s/bills/%s.json?api-key=c886aef674b84bc2ce2f20439b7fff9c:12:66229250' % (congress,chamb,bill_t)
                time.sleep(1)
                congress_scrape(api_call,congress,chamb,bill_t)
                


def congress_scrape(api_call, congress, chamber,bill_type):
    results = simplejson.loads(scraperwiki.scrape(api_call))
    results = results['results'][0]['bills']
    for bill in results:
        bill_uri = bill['bill_uri']
        bill_number = bill['number']
        title = bill['title']
        committees = bill['committees']
        num_cosponsors = bill['cosponsors']
        last_action = bill['latest_major_action']
        date_last_action = bill['latest_major_action_date']
        time.sleep(1)
        if int(num_cosponsors) > 0:
            cosponsor_call = 'http://api.nytimes.com/svc/politics/v3/us/legislative/congress/%s/bills/%s/cosponsors.json?api-key=c886aef674b84bc2ce2f20439b7fff9c:12:66229250' % (congress, bill_number.replace(".",""))
            time.sleep(2)
            print cosponsor_call
            cosponsor_results = simplejson.loads(scraperwiki.scrape(cosponsor_call))['results'][0]
            sponsor = cosponsor_results['sponsor']
            sponsor_id = cosponsor_results['sponsor_id']
            #Cosponsers: List of dictionaries
            cosponsors = cosponsor_results['cosponsors']
            for cosponsor in cosponsors:
                dict_results = {"Bill_number":bill_number,'Title':title, 'Committee':committees,'Last_action':last_action, "Date_Last_action":date_last_action, "Sponsor":sponsor, "Sponsor_ID":sponsor_id, "Congress_Number":congress,"Chamber": chamber}
                cosponsor_id = cosponsor['cosponsor_id']
                cosponsor_name = cosponsor['name']
                dict_results['Cosponsor_ID'] = cosponsor_id
                dict_results["Cosponsor_Name"] = cosponsor_name
                dict_results["Unique"] = bill_number+cosponsor_id
                scraperwiki.sqlite.save(unique_keys=['Unique'], data = dict_results)
                    
    
main()
    import scraperwiki
import simplejson
import urllib2
from bs4 import BeautifulSoup
import datetime
import time


def main():
    congress_number = [str(x) for x in range(110,112)]
    chamber = ['house','senate']
    bill_type = ['introduced','updated','passed']

    for congress in congress_number:
        for chamb in chamber:
            for bill_t in bill_type:
                api_call = 'http://api.nytimes.com/svc/politics/v3/us/legislative/congress/%s/%s/bills/%s.json?api-key=c886aef674b84bc2ce2f20439b7fff9c:12:66229250' % (congress,chamb,bill_t)
                time.sleep(1)
                congress_scrape(api_call,congress,chamb,bill_t)
                


def congress_scrape(api_call, congress, chamber,bill_type):
    results = simplejson.loads(scraperwiki.scrape(api_call))
    results = results['results'][0]['bills']
    for bill in results:
        bill_uri = bill['bill_uri']
        bill_number = bill['number']
        title = bill['title']
        committees = bill['committees']
        num_cosponsors = bill['cosponsors']
        last_action = bill['latest_major_action']
        date_last_action = bill['latest_major_action_date']
        time.sleep(1)
        if int(num_cosponsors) > 0:
            cosponsor_call = 'http://api.nytimes.com/svc/politics/v3/us/legislative/congress/%s/bills/%s/cosponsors.json?api-key=c886aef674b84bc2ce2f20439b7fff9c:12:66229250' % (congress, bill_number.replace(".",""))
            time.sleep(2)
            print cosponsor_call
            cosponsor_results = simplejson.loads(scraperwiki.scrape(cosponsor_call))['results'][0]
            sponsor = cosponsor_results['sponsor']
            sponsor_id = cosponsor_results['sponsor_id']
            #Cosponsers: List of dictionaries
            cosponsors = cosponsor_results['cosponsors']
            for cosponsor in cosponsors:
                dict_results = {"Bill_number":bill_number,'Title':title, 'Committee':committees,'Last_action':last_action, "Date_Last_action":date_last_action, "Sponsor":sponsor, "Sponsor_ID":sponsor_id, "Congress_Number":congress,"Chamber": chamber}
                cosponsor_id = cosponsor['cosponsor_id']
                cosponsor_name = cosponsor['name']
                dict_results['Cosponsor_ID'] = cosponsor_id
                dict_results["Cosponsor_Name"] = cosponsor_name
                dict_results["Unique"] = bill_number+cosponsor_id
                scraperwiki.sqlite.save(unique_keys=['Unique'], data = dict_results)
                    
    
main()
    
###############################################################################
# Eyjan fréttir - Allar fréttir á eyjan.is og fjöldi kommenta
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re


def scrape_manudur(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    soup.prettify()
    print soup
    frett = {}
    last_seen_date = None
    ar = soup.find('h3', 'yyyymm')
    ar =ar.text[:4]
    #ar = re.compile(r"/d.*")
    print ar
    soup.find('table', 'eyjan_news')
    tr = soup.findAll('tr') 
    for tr in tr:
        dagsetning = tr.find('td', 'news_header dddd')
        if dagsetning is None:
            td = tr.find('td', 'news_category')
            flokkur = td.text
            #print flokkur
            frett['flokkur'] = td.text  
            td = tr.find('td', 'news_title')
            #print "Titill: " + td.text + " - " + last_seen_date
            frett['dagsetning'] = last_seen_date
            frett['titill'] = td.text
            tengill = tr.find('a', href = re.compile(r".*comments.*"))
            #print 'Hlekkur: ' + tengill['href']
            frett['url'] = tengill['href'][:-9]
            #print "Komment: " + tengill.text
            frett['kommentafjoldi'] = tengill.text
            #print "Vistum frettina: " + frett['titill']
            scraperwiki.datastore.save(["titill"], frett)

        else:                   # get new date
            last_seen_date = dagsetning.text
            last_seen_date = re.sub("[^0-9,/]",'',last_seen_date)
            last_seen_date = re.sub("/",'.', last_seen_date)
            last_seen_date = last_seen_date + "." + ar

                   

        


def start(url):
    #starting_url = 'http://eyjan.is/frettir/sarpur/'
    html = scraperwiki.scrape(url)
    print html
    soup = BeautifulSoup(html)
    soup.prettify()


    manudir = soup.findAll('a', href = re.compile(r".*mnth.*"))
    #manudir = soup.findAll('a')
    for a in manudir:
        manadar_tengill = a['href']
        if re.match(r"http://eyjan.is.*", manadar_tengill, re.VERBOSE): 
            manadar_tengill = manadar_tengill
        else:
            manadar_tengill = "http://eyjan.is/frettir/sarpur/" + manadar_tengill
    
        print "Saekjum: " + manadar_tengill

        scrape_manudur(manadar_tengill)


start('http://eyjan.is/frettir/sarpur/')###############################################################################
# Eyjan fréttir - Allar fréttir á eyjan.is og fjöldi kommenta
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re


def scrape_manudur(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    soup.prettify()
    print soup
    frett = {}
    last_seen_date = None
    ar = soup.find('h3', 'yyyymm')
    ar =ar.text[:4]
    #ar = re.compile(r"/d.*")
    print ar
    soup.find('table', 'eyjan_news')
    tr = soup.findAll('tr') 
    for tr in tr:
        dagsetning = tr.find('td', 'news_header dddd')
        if dagsetning is None:
            td = tr.find('td', 'news_category')
            flokkur = td.text
            #print flokkur
            frett['flokkur'] = td.text  
            td = tr.find('td', 'news_title')
            #print "Titill: " + td.text + " - " + last_seen_date
            frett['dagsetning'] = last_seen_date
            frett['titill'] = td.text
            tengill = tr.find('a', href = re.compile(r".*comments.*"))
            #print 'Hlekkur: ' + tengill['href']
            frett['url'] = tengill['href'][:-9]
            #print "Komment: " + tengill.text
            frett['kommentafjoldi'] = tengill.text
            #print "Vistum frettina: " + frett['titill']
            scraperwiki.datastore.save(["titill"], frett)

        else:                   # get new date
            last_seen_date = dagsetning.text
            last_seen_date = re.sub("[^0-9,/]",'',last_seen_date)
            last_seen_date = re.sub("/",'.', last_seen_date)
            last_seen_date = last_seen_date + "." + ar

                   

        


def start(url):
    #starting_url = 'http://eyjan.is/frettir/sarpur/'
    html = scraperwiki.scrape(url)
    print html
    soup = BeautifulSoup(html)
    soup.prettify()


    manudir = soup.findAll('a', href = re.compile(r".*mnth.*"))
    #manudir = soup.findAll('a')
    for a in manudir:
        manadar_tengill = a['href']
        if re.match(r"http://eyjan.is.*", manadar_tengill, re.VERBOSE): 
            manadar_tengill = manadar_tengill
        else:
            manadar_tengill = "http://eyjan.is/frettir/sarpur/" + manadar_tengill
    
        print "Saekjum: " + manadar_tengill

        scrape_manudur(manadar_tengill)


start('http://eyjan.is/frettir/sarpur/')
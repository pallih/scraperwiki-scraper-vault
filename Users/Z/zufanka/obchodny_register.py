# -*- coding: utf8 -*-

import scraperwiki
import urllib
import lxml.html
from lxml import etree
import re


def gimmeICO(www):

    path = www.xpath('//span[@class="ra"]')
    ICO = path[9].text.replace(" ", "")
    return ICO

def gimmefirmu(www):

    path = www.xpath('//span[@class="ra"]')
    firma = path[2].text
    return firma

def extract_name(string):                                        # clean the extracted names from garbage
    
    string = string.split('=')[1]
    name = string.split('&')[0]
    
    return name

def gimmeMeno(string):                                           # extract the given name

    meno = re.search('MENO=(.*)&SID', string).group(0)
    return str(extract_name(meno))

def gimmePriezvisko(string):                                     # extract the surname

    priezvisko = re.search('PR=(.*)&MENO', string).group(0)
    return str(extract_name(priezvisko))

def gimmeWWW(meno, priezvisko):                                  # extract the personal URL

    www = "http://orsr.sk/hladaj_osoba.asp?PR=" + urllib.quote(priezvisko) + "&amp;MENO=" + urllib.quote(meno) + "&amp;SID=0&amp;T=f0&amp;R=1"
    return str(www)

def gimmeCompaniesWWW(www):

    scrape = etree.HTML(scraperwiki.scrape(www))
    company_ref = scrape.xpath('//div[@class="bmk"]/a[2]/@href')
    
    i = 0
    
    while i < len(company_ref):
        company_www = "http://orsr.sk/" + str(company_ref[i])
        return company_www
        
        i += 1

def gimmeCompaniesNames(www):

    global meno

    scrape = etree.HTML(scraperwiki.scrape(www))
    line = scrape.xpath("//tr/td/div[@class='sbj']")

    i = 1    

    for l in line:
        i += 1
        if i % 2 == 0 and meno in l.text.encode('utf-8'):
            #print l.text
            return line[i-1].text   

firma = ['http://orsr.sk/vypis.asp?ID=67865&SID=4&P=1', 'http://orsr.sk/vypis.asp?ID=8363&SID=4&P=1', 'http://orsr.sk/vypis.asp?ID=63965&SID=5&P=1', 'http://orsr.sk/vypis.asp?ID=18285&SID=4&P=1', 'http://orsr.sk/vypis.asp?ID=20488&SID=2&P=1', 'http://orsr.sk/vypis.asp?ID=68401&SID=4&P=1','http://orsr.sk/vypis.asp?ID=68180&SID=3&P=1', 'http://orsr.sk/vypis.asp?ID=56986&SID=2&P=1']

id = 1

for i in firma:

    scrape = etree.HTML(scraperwiki.scrape(i))
    
    firma = gimmefirmu(scrape)
    ICO = gimmeICO(scrape)
    people = scrape.xpath('//a[@class="lnm"]/@href'.decode('windows-1250'))

    id +=1

    for person in people:
        person = person.encode('utf-8')

        priezvisko = gimmePriezvisko(person)
        meno = gimmeMeno(person)
    #osobna_stranka = gimmeWWW(meno, priezvisko)
    #companies_www = gimmeCompaniesWWW(osobna_stranka)    
    #companies_names = gimmeCompaniesNames(osobna_stranka)
    

        id += 1

        record = { "ID" : id , "Meno" : meno + ' ' + priezvisko, "firma" : firma, "ICO" : ICO } # column name and value
        scraperwiki.sqlite.save(["ID"], record) # save the records one by 
# -*- coding: utf8 -*-

import scraperwiki
import urllib
import lxml.html
from lxml import etree
import re


def gimmeICO(www):

    path = www.xpath('//span[@class="ra"]')
    ICO = path[9].text.replace(" ", "")
    return ICO

def gimmefirmu(www):

    path = www.xpath('//span[@class="ra"]')
    firma = path[2].text
    return firma

def extract_name(string):                                        # clean the extracted names from garbage
    
    string = string.split('=')[1]
    name = string.split('&')[0]
    
    return name

def gimmeMeno(string):                                           # extract the given name

    meno = re.search('MENO=(.*)&SID', string).group(0)
    return str(extract_name(meno))

def gimmePriezvisko(string):                                     # extract the surname

    priezvisko = re.search('PR=(.*)&MENO', string).group(0)
    return str(extract_name(priezvisko))

def gimmeWWW(meno, priezvisko):                                  # extract the personal URL

    www = "http://orsr.sk/hladaj_osoba.asp?PR=" + urllib.quote(priezvisko) + "&amp;MENO=" + urllib.quote(meno) + "&amp;SID=0&amp;T=f0&amp;R=1"
    return str(www)

def gimmeCompaniesWWW(www):

    scrape = etree.HTML(scraperwiki.scrape(www))
    company_ref = scrape.xpath('//div[@class="bmk"]/a[2]/@href')
    
    i = 0
    
    while i < len(company_ref):
        company_www = "http://orsr.sk/" + str(company_ref[i])
        return company_www
        
        i += 1

def gimmeCompaniesNames(www):

    global meno

    scrape = etree.HTML(scraperwiki.scrape(www))
    line = scrape.xpath("//tr/td/div[@class='sbj']")

    i = 1    

    for l in line:
        i += 1
        if i % 2 == 0 and meno in l.text.encode('utf-8'):
            #print l.text
            return line[i-1].text   

firma = ['http://orsr.sk/vypis.asp?ID=67865&SID=4&P=1', 'http://orsr.sk/vypis.asp?ID=8363&SID=4&P=1', 'http://orsr.sk/vypis.asp?ID=63965&SID=5&P=1', 'http://orsr.sk/vypis.asp?ID=18285&SID=4&P=1', 'http://orsr.sk/vypis.asp?ID=20488&SID=2&P=1', 'http://orsr.sk/vypis.asp?ID=68401&SID=4&P=1','http://orsr.sk/vypis.asp?ID=68180&SID=3&P=1', 'http://orsr.sk/vypis.asp?ID=56986&SID=2&P=1']

id = 1

for i in firma:

    scrape = etree.HTML(scraperwiki.scrape(i))
    
    firma = gimmefirmu(scrape)
    ICO = gimmeICO(scrape)
    people = scrape.xpath('//a[@class="lnm"]/@href'.decode('windows-1250'))

    id +=1

    for person in people:
        person = person.encode('utf-8')

        priezvisko = gimmePriezvisko(person)
        meno = gimmeMeno(person)
    #osobna_stranka = gimmeWWW(meno, priezvisko)
    #companies_www = gimmeCompaniesWWW(osobna_stranka)    
    #companies_names = gimmeCompaniesNames(osobna_stranka)
    

        id += 1

        record = { "ID" : id , "Meno" : meno + ' ' + priezvisko, "firma" : firma, "ICO" : ICO } # column name and value
        scraperwiki.sqlite.save(["ID"], record) # save the records one by 

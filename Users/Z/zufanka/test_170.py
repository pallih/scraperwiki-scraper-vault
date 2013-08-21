# -*- coding: utf8 -*-

import scraperwiki
import urllib
import lxml.html
from lxml import etree
import re
import codecs

id = 1
NULL = 0

#kees = urllib.urlopen('http://v3.sk/~naberacka/parlement-com/keess', 'r').readlines()
#jan = urllib.urlopen('http://v3.sk/~naberacka/parlement-com/jan', 'r').readlines()
#for i in kees:
#for i in jan:
    #www = "http://v3.sk/~naberacka/parlement-com/"+str(i).replace('\n','')
    #www = "http://v3.sk/~naberacka/parlement-com/test/"+str(i).replace('\n','')

cities = urllib.urlopen('http://v3.sk/~naberacka/parlement-com/nederlandse_steden', 'r').readlines()

#tweede_kamer = 'http://www.parlement.com/id/vhnnmt7ijayp/de_huidige_tweede_kamer' # huidige tweede kamer
tweede_kamer = "http://v3.sk/~naberacka/SelectiemenuTweedeKamerleden.html"         # tweede kamerleden vanaf 2002
scrape = etree.HTML(scraperwiki.scrape(tweede_kamer))

#personal_link = scrape.xpath('//div[@id="p1"]/following::ul/li/a/@href')          # scrape the personal link van de pagina van huidige tweede kamer
personal_link = scrape.xpath('//div[@class="seriekeuze seriekeuze_align"]/ul/li/a/@href')
print personal_link


for i in personal_link:

    #www = 'http://www.parlement.com'+str(i)
    www = str(i)

    website = str(www)
    scraped = etree.HTML(scraperwiki.scrape(www))

    def no_date_record(record):
        record.extend([NULL, NULL, NULL])

    def contains_digits(s):                                      # check if the string contains numbers
           return any(char.isdigit() for char in s)

    def extract_date(string):                                    # divide the string that contains date into a list element [day,month,year]
        date = []                                                # create an empty list

        string = string.split(' ')                               # split the string on whitespaces
        
        if len(string) == 3:                                     # if the list is 3 elements long (eg. 'van mei 2012') append 0 in place of the 'day'
            date.append(NULL)

        elif len(string) == 2:                                   # if the list is 2 elements long (eg. 'van 2012') append 0 in place of the 'day' and 'month'
            date.extend([NULL, NULL])
            
        for i in string:          
            if i.isdigit():                                      # if the element is a digit, check whether it is 2 or less characters long (day), otherwise make it 'year'
                if len(i) <= 2:   
                    day = i
                    date.append(day)
                else:
                    year = i
                    date.append(year)

            elif i != 'van' and i != 'vanaf' and i != 'tot':     # if the element is not a digit, and also not 'van' 'vanaf' or 'tot', append it as the month
                month = i
                date.append(month)
            else:
                continue

        return date


    def check_none(elem):
        return str(elem)
    


    for n in scraped.xpath("//*[@id='h1_top']".decode('utf-8')):          # get the name
        name = re.split('\(', n.text, maxsplit=1)                         # split it at the first "("
        entity1 = str(name[1].replace(")","").encode('utf-8'))            # erase the ")"    

    for loopbaan in scraped.xpath("//div[@id='p4']/following::ul[1]/li/div/div[2]".decode('utf-8')):  # get the Xpath to "loopbaan"
        content = loopbaan.text                                                       # get the text from between the divs
        content = content.replace(u'\xa0', u' ')                                      # replace the annoying \xa0 character
        toD = []
        fromD = []

        date = content.split(',')[-1]       # split the text on commas(,) and store the last column in variable 'date'
        if contains_digits(date):           # check if the variable contains numbers (to check whether the last element has any dates in it)

            fromD_match = re.search('van(af)?\s([0-9]{1,2})?\s?([A-Za-z]+\s)?[0-9]{4}', date) # match van/vanaf + optional number + optional word + year
            if fromD_match:
                fromD = extract_date(fromD_match.group(0))
            else:
                no_date_record(fromD)
            

            toD_match = re.search('tot\s([0-9]{1,2})?\s?([A-Za-z]+\s)?[0-9]{4}', date)        # match tot + optional number + optional word + year
            if toD_match:
                toD = extract_date(toD_match.group(0))
            else:
                no_date_record(toD)
        
        else:
            no_date_record(fromD)
            no_date_record(toD)

        part = re.split('([A-Z].*|50[pP].*)', content, maxsplit=1)   # split the text into two at the first upper case letter
                                                                     # (the institutions are in upper case letters), OR 50[pP] (50Plus party)
        function = part[0].split(',')[0]                             # split the first half of the text at the comma's. Some of the descriptions have multiple comma separated parts.
        relation = str(function.strip().encode('utf-8'))             # the function name is only the first part, *!* others are left out *!*
        
        if len(part) < 2:
             entity2 = 0       
        else:
            place = re.split(',\s[van|tot].*', part[1], maxsplit=1)    # split the second half of the text at the ", van" or ", tot" and store the first half 
            entity2 = str(place[0].encode('utf-8'))                       # give the name of the institution
               


        # this needs to be re-written so it can be edited nicely
        if entity2 == 0:
            pass

        elif "docent" in relation or "leraar" in relation or "niversiteit" in entity2 or "niversity" in entity2 or "onderwijzer" in relation:
            type2 = "onderwijs"
        elif "iekenhuis" in entity2 or "ospital" in entity2 or "MC" in entity2:
            type2 = "ziekenhuis"
        elif "kamer" in entity2 or "Kamer" in entity2:
            type2 = "parlement"
        elif "emeente" in relation or "emeente" in entity2 or "urgemeester" in relation or "ethouder" in relation or "echtbank" in relation or "inisterie" in entity2 or "rovincie" in entity2 or "inisterie" in entity2:
            type2 = "overheid"
        else:
            type2 = "bedrijf"

        
        id += 1
        #print id, entity1, relation , entity2, fromD, toD
        

        record = { "ID" : id , "Entiteit 1" : entity1 , "Entiteit 2" : entity2 , "Type Entiteit 1" : "persoon" , "Type Entiteit 2" : type2 , "Relatie" : relation , "Rationale" : "parlement.com", "Date 1 D" : check_none(fromD[0]) , "Date 1 M" : check_none(fromD[1]) , "Date 1 Y" : check_none(fromD[2]) , "Date 2 D" : check_none(toD[0]) , "Date 2 M": check_none(toD[1]) , "Date 2 Y" : check_none(toD[2]) , "URL" : website } # column name and value
        scraperwiki.sqlite.save(["ID"], record) # save the records one by one
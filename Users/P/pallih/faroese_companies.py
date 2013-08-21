# Blank Python

# -*- coding: utf-8 -*

import scraperwiki
import lxml.html
import urllib2
import time
import pprint



#url= 'http://skraseting.skraseting.fo/'
#url = 'http://skraseting.skraseting.fo/app/adv_soeg.htm'
#url = 'http://skraseting.skraseting.fo/Navi.htm'

#inital import of numbers for urls:

#url = 'http://data2.d8tabit.net/faroe-islands-initial-dump'
#req = urllib2.Request(url)
#response = urllib2.urlopen(req)
#numbers = response.read()
#csv_list = numbers.split(",")
#for number in csv_list:
#    record = {}
#    record['url_nr'] = number
#    record['done'] = 0
#    scraperwiki.sqlite.save(['url_nr'], data=record, table_name='url_numbers')

#end of initial import

baseurl = 'http://skraseting.skraseting.fo/app/tegning1.asp?id='

def process(html,number):
    #print html
    root = lxml.html.fromstring(html)
    #registration_number = root.xpath('/html/body/div/table/tr[2]/td[3]')
    #name = root.xpath('/html/body/div/table/tr[4]/td[3]')
    #print registration_number[0].text
    #print name[0].text
    results = root.xpath('//tr')
    trs = len(results)
    #print results[4][3].text
    counter = 1
    record = {}
    record['registration_url'] = baseurl+number
    record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())

    while (counter<trs):
        if results[counter][0].text_content() != None:
            field = results[counter][0].text_content().encode('utf-8').strip()
            #print counter, ' ', results[counter][0].text_content()
            if field == "Skrásetingar-nr.":
                #print '-- registration_number'
                record['registration_number'] = results[counter][2].text
            if field == "Navn:":
                #print '-- registration_number'
                record['name'] = results[counter][2].text 
            if field == "Adressa:":
                #print '-- registration_number'
                record['address'] = results[counter][2].text
            if field == "Kommuna:":
                #print '-- registration_number'
                record['municipality'] = results[counter][2].text 
            if field == "Hjanøvn:":
                #print '-- alternate names'
                # //td[@valign="top" and @colspan="3"]
                alternate_names_list = []
                alternate_names = root.xpath("//td[@valign='top' and @colspan='3']")
                for alternate_name in alternate_names[:-2]:
                    #print alternate_name.text
                    alternate_names_list.append(alternate_name.text)
                record['alternate_names'] = alternate_names_list
                #print results[counter][2].text_content()
            if field == "Stjórn:":
                #record['governance'] = results[counter][2].text
                if results[counter][2].text_content().encode('utf-8').strip() == "Stjóri":
                    record['manager'] = results[counter][4].text

            if field == "Endamál:":
                record['purpose'] = results[counter][2].text
            if field == "Partapeningur:":
                record['shares'] = results[counter][2].text
            #if field == "Nevnd:":
            #    record['board'] = results[counter][2].text
            #    if results[counter][2].text_content().encode('utf-8').strip() == "Nevndarformaður":
            #        record['chairman_of_the_board'] = results[counter][4].text



        #print counter, '[0] ', results[counter][0].text_content()
        #if results[counter][0].text_content() != None:
         #   print counter, '[0] ', results[counter][0].text_content()

        #if results[counter][2].text != None:
        #    print '-- first td? ', results[counter][2].text
        counter = counter+1
    #pprint.pprint(record)
    scraperwiki.sqlite.save(['registration_number'], data=record, table_name='faroese_companies')
    update_statement= 'update url_numbers SET done="1" WHERE url_nr='+ '"' + number + '"'
    scraperwiki.sqlite.execute(update_statement)
    scraperwiki.sqlite.commit()
    #print record

#print 'date scraped: ', results[0].text_content()
    #print 'registration_number: ', results[1][2].text
    #print '2: ', results[2].text_content()
    #print 'name: ', results[3][2].text
    #print '4: ', results[4].text_content()
    #print 'address: ', results[5][2].text
    #print 'town: ', results[6][2].text

    




    #for element in root.iter('td'):
    #    print("%s - %s" % (element.tag, element.text))
    #counter = 1
    #for el in results:           
    #    print el.tag, counter
    #    counter = counter+1
    #    for el2 in el:
    #        print "--", el2.tag, el2.text_content()
    
    #for td in results:
        #print 'number: ', td[4].tag
        #print 'name: ', td[4][3].text

    #for td in root.xpath('//tr'):
    #    print td[0][1].text_content()



def get_number(number):
    url = baseurl + str(number)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    html = response.read()
    process(html,number)



selection_statement = '* from url_numbers where done=0'
numbers = scraperwiki.sqlite.select(selection_statement)
print numbers
for number in numbers:
    print 'Processing number ', number['url_nr']
    get_number(number['url_nr'])

#get_number('134341')




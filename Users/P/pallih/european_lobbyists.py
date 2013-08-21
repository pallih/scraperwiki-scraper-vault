import scraperwiki,re
#from lxml import etree
import lxml.html
import time
import datetime

# Scrapes the registry of European lobbyists: http://europa.eu/transparency-register/index_en.htm

baseurl = 'http://ec.europa.eu/transparencyregister/public/consultation/listlobbyists.do?alphabetName='

urllist = ['LatinAlphabet', 'BulgarianAlphabet', 'GreekAlphabet']

def start_again():
    #drop runtime_info table to start again
    scraperwiki.sqlite.execute("drop table if exists runtime_info")
    for l in urllist:
        url = baseurl + l
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        results = root.xpath('//p/a/.')
        for r in results:
            record = {}
            record['letter'] = r.text.strip()
            record['last_page'] = '1'
            record ['done'] = 0
            scraperwiki.sqlite.save(['letter'], data=record, table_name='runtime_info')

def scrape(letter,page):
    url = 'http://ec.europa.eu/transparencyregister/public/consultation/listlobbyists.do?letter='+str(letter.encode('utf-8'))+'&d-7641134-p='+str(page)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    # //tbody/tr/.
    results = root.xpath('//tbody/tr/.')
    if results:
        print 'processing results for ' + str(letter.encode('utf-8')) + ' page ' + str(page)
        for m in results:
            record = {}
            record['id_nr'] = m[0].text_content()
            record['name'] =  m[1].text_content()
            record['detail_url'] = 'http://ec.europa.eu/' + m[2][0].get('href')
            #print record
            scraperwiki.sqlite.save(['id_nr'], data=record, table_name='european_lobbyists')
        next = root.xpath('//span[@class="pagelinks"]/a/img[@alt="Next"]')
        if next:
            print "there are more results - let's process (last page done was: " + str(page) + " of letter: "+ letter +" )"
            # update last page done
            update_statement= 'update runtime_info SET last_page=' + str(page) + ' WHERE letter='+ '"' + letter+ '"'
            scraperwiki.sqlite.execute(update_statement)
            scraperwiki.sqlite.commit()
            page = int(page)+1
            # scrape next page
            scrape(letter,page)
        else:
            print 'Last page of results - Done with letter: ' + letter
            #update last page and done field
            update_statement= 'update runtime_info SET last_page=' + str(page) + ', done=1 WHERE letter='+ '"' + letter+ '"'
            scraperwiki.sqlite.execute(update_statement)
            scraperwiki.sqlite.commit()
    else:
        print 'No results - Done with letter: ' + str(letter.encode('utf-8'))
        # update last page and done field
        update_statement= 'update runtime_info SET last_page=' + str(page) + ', done=1 WHERE letter='+ '"' + letter+ '"'
        scraperwiki.sqlite.execute(update_statement)
        scraperwiki.sqlite.commit()

def run():
    for letters in letters_todo:
        letter=letters['letter']
        page=letters['last_page']
        scrape(letter,page)

selection_statement = '* from runtime_info where done=0'
letters_todo = scraperwiki.sqlite.select(selection_statement)

if letters_todo:
    todo_list = []
    for letters in letters_todo:
        letter=letters['letter']
        todo_list.append(letter) 
    #print ",".join(str(states_todo)
    print 'there are ', len(todo_list), ' letters left to do - lets get going!'
    run()

else:
    print 'there are no letters left to do - now we drop the runtime_info table and start all over again'
    start_again()
    run()




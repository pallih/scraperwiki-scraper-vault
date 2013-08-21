# Blank Python
import scraperwiki
import BeautifulSoup
import math
import dateutil.parser

baseurl = 'http://www.dft.gov.uk/press/speechesstatements/speeches/?view=Filter&pg='

# get number of pages

html = scraperwiki.scrape(baseurl + "1")
soup = BeautifulSoup.BeautifulSoup(html)
summary = soup.findAll('p', {"class" : "searchSummary"})[0]
total = int(summary.findAll('strong')[1].text) # number of results
npages = math.ceil(total/10.0) # 10 results per page


#start scraping

page = 1

while page <= npages:
    html = scraperwiki.scrape(baseurl + str(page))
    soup = BeautifulSoup.BeautifulSoup(html)
    results = soup.find('ol', {'class' : 'results documents'})
    speeches = results.findAll('li')
    for speech in speeches:
        record = {}
        record['department'] = 'Department for Transport'
        titlehtml = speech.find('h2')
        record['title'] = titlehtml.text
        link = titlehtml.contents[0]['href']
        record['permalink'] = link
        speechhtml = scraperwiki.scrape(link)
        speechsoup = BeautifulSoup.BeautifulSoup(speechhtml, fromEncoding="windows-1252")
        print speechsoup.orginalEncoding
        details = speechsoup.findAll('dd', {'class' : 'speech'})
        record['minister_name'] = details[0].text
        record['given_on'] = details[1].text
        dateobj = dateutil.parser.parse(details[1].text)
        record['where'] = details[2].text
        if len(details) == 4:
            record['where'] = "%s, %s" % (record['where'], details[3].text)
        bodytags = speechsoup.find('div', {'id' : 'mainBody'})
        # clean up the header
        sstop = speechsoup.find('div', {'class' : 'speech-statement-top'})
        sstop.extract()
        # clean up embedded videos
        videos = speechsoup.findAll('object')
        for video in videos:
            # do something with the video link if you want
            #video.extract() #uncomment to strip videos
            pass
        record['body'] = bodytags.renderContents()
        try:
             for k, v in record.items():
                 record[k] = unicode(v.decode('utf-8'))
        except UnicodeDecodeError:
            print "Record %s, %s has encoding error" % (k,v)

        scraperwiki.sqlite.save(['permalink'], record, date=dateobj)
        print record
    page += 1


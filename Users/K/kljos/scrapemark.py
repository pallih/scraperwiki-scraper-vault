import scraperwiki
import scrapemark
from urllib2 import Request, urlopen, URLError, HTTPError       
import urllib, urllib2, urlparse
import re, os
from time import sleep

scraperwiki.sqlite.execute('DROP TABLE IF EXISTS int_studies;')
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS int_studies ( `pdf_title` VARCHAR, `pdf_url` VARCHAR PRIMARY KEY, `article_html` VARCHAR, `author` VARCHAR, `volume_url` VARCHAR, `volume_title` VARCHAR, `library_url` VARCHAR,  `agency_name` VARCHAR);')
pdf_title = []
pdf_url = []
volume_title = []
volume_url = []
agency_name = []

library_url="https://www.cia.gov/library/center-for-the-study-of-intelligence/csi-publications/csi-studies/index.html"
hosting_agency="Central Intelligence Agency"
internal_links=['fall00/index.html', 'fall_winter_2001/index.html', 'spring98/index.html', '97unclass/index.html', 'special-review-supplement/index.html', 'vol50no2/html_files/index.html', 'summer00/index.html', 'vol50no1/html_files/index.html', 'Vol49no2/index.html', 'vol46no2/index.html', 'vol46no4/index.html', 'vol47no2_2003/index.html', 'vol47no4/index.html', 'vol48no2/index.html', 'vol48no4/index.html', 'vol50no3/index.html', 'vol51no1/index.html', 'vol51no3/index.html', 'vol51no4/index.html', 'vol-52-no-1/index.html', 'vol52no3/index.html', 'vol-52-no-4/index.html', 'vol53no1/index.html', 'vol53no2/index.html', 'vol.-53-no.-3/index.html', 'vol53no4/index.html', 'volume-54-number-1/index.html', 'vol.-54-no.-2/index.html', 'vol.-54-no.-3/index.html', 'vol.-54-no.-4/Index.html', 'vol.-55-no.-1/index.html', 'vol.-55-no.-2/index.html', 'vol.-55-no.-3/index.html', 'vol.-55-no.-4/index.html', 'vol.-56-no.-1/index.html', 'vol.-56-no.-3/index.html', 'vol46no1/index.html', 'vol46no3/index.html', 'vol47no1/index.html', 'vol47no3/index.html', 'vol48no1/index.html', 'vol48no3/index.html', 'vol49no1/html_files/index.html', 'vol49no3/html_files/index.html', 'vol49no4/index.html', 'vol50no4/index.html', 'vol52no2/index.html', 'vol51no2/index.html', '96unclass/index.html', 'winter98_99/index.html', 'winter99-00/index.html', 'winter_spring01/index.htm']
urls = ['internal_links']
skips =['Contributors',"CIA.gov's YouTube Channel","external link disclaimer","Careers and Internships",'General Information','Skip to content.','List of Contributors', 'COMMENTARY','[Top of page]','Skip to navigation', 'CIA', 'Navigation', 'CIA Home', 'About CIA', 'Careers', 'Offices of CIA', 'News & Information','About CSI', 'Books and Monographs', 'CIA Museum', 'CIA Vision, Mission & Values', 'CSI Publications', 'Center for the Study of Intelligence', 'Contact CIA', 'Copyright', 'DNI.gov', 'FLU.gov', 'FOIA', 'Freedom of Information Act Electronic Reading Room', 'How to Obtain Publications','How to Submit Articles','Index of Declassified Articles','Intelligence Literature',"Kids' Page",'Kent Center Occasional Papers','Library','NoFEAR Act','Privacy','Publications','Related Links','Reports','Site Map', 'Site Policies','Studies Archive Indexes','Studies in Intelligence','US Intelligence Sites','Top of page','USA.gov','studies', 'www.adobe.com', 'Mobile', 'Extraordinary Fidelity', '']

for idx in urls:
    if idx == 'internal_links':
       for parent_page in internal_links:
          meta=scrapemark.scrape("""
                  {*
                        <title>{{ title }}</title>
                  *}
                  """,
                  url='https://www.cia.gov/library/center-for-the-study-of-intelligence/csi-publications/csi-studies/studies/' + parent_page)
          pdfs=scrapemark.scrape("""
                  {*
                        <a href="{{ [pdf].url }}">{{ [pdf].title }}</a>
                  *}
                  """,
                  url='https://www.cia.gov/library/center-for-the-study-of-intelligence/csi-publications/csi-studies/studies/' + parent_page)
          for ix in range(len(pdfs['pdf'])):
             record = {}
             record['pdf_url'] = 'https://www.cia.gov' + str(pdfs['pdf'][ix]['url'])
             record['pdf_title'] = pdfs['pdf'][ix]['title'].encode('utf-8')
             record['volume_title']=meta['title']
             record['volume_url']=str(parent_page)
             record['library_url']=library_url
             record['agency_name']=hosting_agency
             if pdfs['pdf'][ix]['title'] not in skips:
                 scraperwiki.sqlite.save(['pdf_url'], record, table_name='int_studies')
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS byurl ON int_studies (`pdf_url`)')      
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS bytitle ON int_studies (`pdf_title`)')
scraperwiki.sqlite.execute('ANALYZE')
scraperwiki.sqlite.commit()
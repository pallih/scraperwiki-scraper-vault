#Scraper for Burundi microfinance data from pdf file. Based on Scraperwiki's PDF example.
# Position visualizer is here: http://scraperwikiviews.com/run/pdf-to-html-preview-1/

import scraperwiki
import os
import tempfile
import sys
import string
import readline

#Code nicked from ScraperWiki's pdttotext example, which creates text version of the table with its columns separated  by tabs.
def pdftotext(pdfdata):
    """converts pdf file to text"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    textin = tempfile.NamedTemporaryFile(mode='r', suffix='.txt')
    tmptext = textin.name
    cmd = '/usr/bin/pdftotext -layout -enc UTF-8 "%s" "%s"' % (pdffout.name, tmptext)
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)
    pdffout.close()


    #convert table data into an array
    for line in textin:
        lv = line.split('\t')

        #SJF: need to ignore everything before the table starts.  Maybe we can ignore any lines that don't have tabs in them?
        if len(lv) > 2:
            #Dump data out to scraperwiki store
            data = { 'organisation' : lv[0], 'type' : lv[1], 'address' : lv[2] }
            scraperwiki.sqlite.save(unique_keys=['organisation'], data=data)
        else:
            print(line)

    textin.close()
    return 


pdfurl = "http://www.brb.bi/se/docs/emf_agrees.pdf"
a = scraperwiki.scrape(pdfurl)
rawtext = pdftotext(a)

#Scraper for Burundi microfinance data from pdf file. Based on Scraperwiki's PDF example.
# Position visualizer is here: http://scraperwikiviews.com/run/pdf-to-html-preview-1/

import scraperwiki
import os
import tempfile
import sys
import string
import readline

#Code nicked from ScraperWiki's pdttotext example, which creates text version of the table with its columns separated  by tabs.
def pdftotext(pdfdata):
    """converts pdf file to text"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    textin = tempfile.NamedTemporaryFile(mode='r', suffix='.txt')
    tmptext = textin.name
    cmd = '/usr/bin/pdftotext -layout -enc UTF-8 "%s" "%s"' % (pdffout.name, tmptext)
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)
    pdffout.close()


    #convert table data into an array
    for line in textin:
        lv = line.split('\t')

        #SJF: need to ignore everything before the table starts.  Maybe we can ignore any lines that don't have tabs in them?
        if len(lv) > 2:
            #Dump data out to scraperwiki store
            data = { 'organisation' : lv[0], 'type' : lv[1], 'address' : lv[2] }
            scraperwiki.sqlite.save(unique_keys=['organisation'], data=data)
        else:
            print(line)

    textin.close()
    return 


pdfurl = "http://www.brb.bi/se/docs/emf_agrees.pdf"
a = scraperwiki.scrape(pdfurl)
rawtext = pdftotext(a)


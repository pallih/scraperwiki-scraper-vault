import scraperwiki
from lxml import html, etree
import os, re, requests
import tempfile

def pdftoxml(pdfdata):
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
    text = textin.read()
    textin.close()
    return text

def fetch_page(url):
    res = requests.get(url)
    print res
    #embed = re.match('<iframe.*src=\"([^\"]*)"', htm)
    #embed = re.match('<iframe.*src="([^\"]*)">', htm, re.MULTILINE)
    frame = re.match('iframe.*src="([^"]*)">', res.content)
    print frame

fetch_page("http://www.london-gazette.co.uk/issues/54108/supplements/10057/page.pdf")

import scraperwiki
from lxml import html, etree
import os, re, requests
import tempfile

def pdftoxml(pdfdata):
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
    text = textin.read()
    textin.close()
    return text

def fetch_page(url):
    res = requests.get(url)
    print res
    #embed = re.match('<iframe.*src=\"([^\"]*)"', htm)
    #embed = re.match('<iframe.*src="([^\"]*)">', htm, re.MULTILINE)
    frame = re.match('iframe.*src="([^"]*)">', res.content)
    print frame

fetch_page("http://www.london-gazette.co.uk/issues/54108/supplements/10057/page.pdf")


'''Pulls data in from http://www.sasra.go.ke/downloads/licensedsaccos.pdf for Microfinance Information eXchange'''

#import BeautifulSoup
#import requests
import re
import json
#import scraperwiki  
import os           
import tempfile
from urllib2 import urlopen

def parse_record(str):
  str.rstrip()
  l=str.split("\t")

  out = {}
  out['name'] = l[0]
  out['address'] = l[1]
  out['date'] = l[2]
  return out


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
    text = textin.read()
    textin.close()
    return text


def main():
    url = 'http://www.sasra.go.ke/downloads/licensedsaccos.pdf'

    #a = scraperwiki.scrape(url)
    a = urlopen(url).read()
    text = pdftotext(a)
    f = open('temp22', 'w')
    f.write(text);
    f.close();
    
    cmd = "cat temp22 | perl -ne 'chomp; $_ =~ s/\r//g; $_ =~ s/^\s+//g; print \"$_\n\";' | perl -ne 'if ($_ =~ /^\d+/) { $_ =~ s/\ {2,}/\t/g; $_ =~ s/^\S+\s+//; print };' > testOut.txt"
    os.system(cmd)

    with open("testOut.txt") as f:
      content = f.readlines()

    out = map(parse_record, content)
    print(out)
    #outfile = open('sasra.json','w')
    #json.dump(out,outfile)

    os.remove("testOut.txt")
    os.remove("temp22")

if __name__ == "scraper":
    main()
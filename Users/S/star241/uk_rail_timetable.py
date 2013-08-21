import scraperwiki
import urllib, urllib2
import lxml.etree, lxml.html
import re, os
import zipfile, tempfile;
import random;


def Main(url) :
    tmpfile = tempfile.gettempdir()+"/45_networkrail.zip";
    tmpdir = tempfile.gettempdir()+"/45_networkrail"; #+str(random.randint(2, 1000000000));
    urllib.urlretrieve (url, tmpfile);

    with zipfile.ZipFile(tmpfile, 'r') as myzip:
        myzip.extractall(tmpdir);


    f = open(tmpdir+"/completeTimetable.pdf", 'r');
    pdfxml = scraperwiki.pdftoxml(f.read());
    #print(os.listdir(tmpdir));
    #print(pdfxml);
    root = lxml.etree.fromstring(pdfxml);
    print '<p>There are %d pages</p>' % len(root)
    print etree.tostring(root[0])


Main("http://www.networkrail.co.uk/browse%20documents/eNRT/May11/CompleteTimetable.zip?1");
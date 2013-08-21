import scraperwiki
import BeautifulSoup
import urllib2
import urllib
import cookielib
import datetime
import re

from scraperwiki import datastore

urlopen = urllib2.urlopen

cj = cookielib.LWPCookieJar()

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

Request = urllib2.Request

def post_form():
    url = "https://www3.prefeitura.sp.gov.br/sf8663/formsinternet/Principal.aspx"
    reqdata = {}
    reqdata = urllib.urlencode(reqdata)
    req = Request(url, reqdata)
    handle = urlopen(req)

    soup = BeautifulSoup.BeautifulSoup(handle.read())
    viewstate = soup.find('input', {'name' : '__VIEWSTATE'})['value']
    print viewstate


import urllib
import re

companiesfile = urllib.urlopen("https://dl.dropboxusercontent.com/u/7453595/symbols.txt")
companieslist = companiesfile.readlines()

i=0

while i<len(companieslist):
    url = "http://finance.yahoo.com/q?s="+companieslist[i]+"&ql=1"
    htmlfile = urllib.urlopen(url)
    htmltext = htmlfile.read()
    regex = '<span id="yfs_l84_[^.]*">(.+?)</span>'
    pattern = re.compile(regex)
    price = re.findall(pattern,htmltext)
    print companieslist[i],price
    i+=1

import urllib
import re

companiesfile = urllib.urlopen("https://dl.dropboxusercontent.com/u/7453595/symbols.txt")
companieslist = companiesfile.readlines()

i=0

while i<len(companieslist):
    url = "http://finance.yahoo.com/q?s="+companieslist[i]+"&ql=1"
    htmlfile = urllib.urlopen(url)
    htmltext = htmlfile.read()
    regex = '<span id="yfs_l84_[^.]*">(.+?)</span>'
    pattern = re.compile(regex)
    price = re.findall(pattern,htmltext)
    print companieslist[i],price
    i+=1


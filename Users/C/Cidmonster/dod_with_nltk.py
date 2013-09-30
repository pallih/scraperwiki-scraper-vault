import scraperwiki                  
import lxml.html
from lxml.html.clean import Cleaner # To get rid of unneeded HTML tags
import re                           # Gotta have my regex
import time                         # time is on my side. (date operations)
from decimal import *
import sys
import urllib
import datetime
import nltk
from nltk import TreebankWordTokenizer
from BeautifulSoup import BeautifulSoup
from nltk import tag as nltk_tag
from nltk import tokenize
def GetContractPage(x):
    url = 'http://www.defense.gov/contracts/contract.aspx?contractid=%d' % x
    html = urllib.urlopen(url).read()
    if re.search("The Official Home of the Department of Defense", html):
        return
    soup = BeautifulSoup(html)
    p_tags = soup.findAll("p")
    p_tags_text_list = [tag.text for tag in p_tags]

    tokenized_list = []

    for text in p_tags_text_list:
        tokenized_list = tokenize.word_tokenize(text)
        tokenized_list.append(nltk_tag.pos_tag(tokenized_list))
    tagged_list = tokenized_list[-1]

    data = {
        "url": url}

    for token in tagged_list[1:]:
        if token[1]=="NNP":
            data['entity'] = token[0]
            break
    

    for token in tagged_list[1:]:
        if token[1]=="CD":
            data['Amount'] = token[0]
            break

    print data

def Main():
    furl = 'http://www.defense.gov/contracts'
    html = urllib.urlopen(furl).read()
    lastcontracts = re.search('contractid=(\d{4,})', html)
    lastcontracts = int(lastcontracts.group(1))

    firstcontracts = scraperwiki.sqlite.get_var('last_page', 391)
    if firstcontracts >= lastcontracts:
        print "no new contracts"
        return

    for x in range(firstcontracts+1,lastcontracts+1)[:1]:
        GetContractPage(x)
        scraperwiki.sqlite.save_var('last_page', x)

Main()
import scraperwiki                  
import lxml.html
from lxml.html.clean import Cleaner # To get rid of unneeded HTML tags
import re                           # Gotta have my regex
import time                         # time is on my side. (date operations)
from decimal import *
import sys
import urllib
import datetime
import nltk
from nltk import TreebankWordTokenizer
from BeautifulSoup import BeautifulSoup
from nltk import tag as nltk_tag
from nltk import tokenize
def GetContractPage(x):
    url = 'http://www.defense.gov/contracts/contract.aspx?contractid=%d' % x
    html = urllib.urlopen(url).read()
    if re.search("The Official Home of the Department of Defense", html):
        return
    soup = BeautifulSoup(html)
    p_tags = soup.findAll("p")
    p_tags_text_list = [tag.text for tag in p_tags]

    tokenized_list = []

    for text in p_tags_text_list:
        tokenized_list = tokenize.word_tokenize(text)
        tokenized_list.append(nltk_tag.pos_tag(tokenized_list))
    tagged_list = tokenized_list[-1]

    data = {
        "url": url}

    for token in tagged_list[1:]:
        if token[1]=="NNP":
            data['entity'] = token[0]
            break
    

    for token in tagged_list[1:]:
        if token[1]=="CD":
            data['Amount'] = token[0]
            break

    print data

def Main():
    furl = 'http://www.defense.gov/contracts'
    html = urllib.urlopen(furl).read()
    lastcontracts = re.search('contractid=(\d{4,})', html)
    lastcontracts = int(lastcontracts.group(1))

    firstcontracts = scraperwiki.sqlite.get_var('last_page', 391)
    if firstcontracts >= lastcontracts:
        print "no new contracts"
        return

    for x in range(firstcontracts+1,lastcontracts+1)[:1]:
        GetContractPage(x)
        scraperwiki.sqlite.save_var('last_page', x)

Main()

import scraperwiki

import re
from bs4 import BeautifulSoup
import urllib
import sys

def main(argv):
    site =''.join(argv)
    html = urllib.urlopen(site).read()
    soup = BeautifulSoup(html)
    texts = soup.findAll(text=True)

    str1 = ''.join(texts)
    p = re.compile('[0-9]{1,4} (.){1,25}, (.){1,25} [a-zA-Z]{2} [0-9]{5}')

    m = p.search(str1).group()
    print m

    scraperwiki.sqlite.save(['tag'], m),
    
if __name__ == "__main__":
    main(sys.argv[1:])
import scraperwiki

import re
from bs4 import BeautifulSoup
import urllib
import sys

def main(argv):
    site =''.join(argv)
    html = urllib.urlopen(site).read()
    soup = BeautifulSoup(html)
    texts = soup.findAll(text=True)

    str1 = ''.join(texts)
    p = re.compile('[0-9]{1,4} (.){1,25}, (.){1,25} [a-zA-Z]{2} [0-9]{5}')

    m = p.search(str1).group()
    print m

    scraperwiki.sqlite.save(['tag'], m),
    
if __name__ == "__main__":
    main(sys.argv[1:])

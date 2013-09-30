from urllib import urlopen
from bs4 import BeautifulSoup
site = urlopen("https://www.google.co.uk/finance").read()
soup = BeautifulSoup(site)

text = (soup.get_text())

from collections import counter
cnt = counter(text)

from urllib import urlopen
from bs4 import BeautifulSoup
site = urlopen("https://www.google.co.uk/finance").read()
soup = BeautifulSoup(site)

text = (soup.get_text())

from collections import counter
cnt = counter(text)


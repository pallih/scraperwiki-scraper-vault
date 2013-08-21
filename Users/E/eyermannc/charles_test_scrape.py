import lxml.etree as ET
import urllib
import re
from urllib import urlopen
import scraperwiki

wikipedia_utils = scraperwiki.swimport("wikipedia_utils")

ntitle = wikipedia_utils.GetWikipediaCategoryRecurse("Category:Diseases_and_disorders")
scraperwiki.sqlite.save(["t.db"], ntitle, "DD_list")

print ntitle



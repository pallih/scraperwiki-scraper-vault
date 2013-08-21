import scraperwiki
import string

# Blank Python

from lxml import etree
import lxml.html
import dateutil.parser
import datetime

build_text_list = etree.XPath("//text()")

def index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
              return i
    return -1

html = scraperwiki.scrape("http://www.ichunddu.com/ich&du_dateien/ich&du_menueplan.htm")
root = lxml.html.fromstring(html)
text_list = build_text_list(root)
#print text_list
#print map(string.strip, text_list)

def index_containing_substring_textlist(substring):
    return index_containing_substring(text_list, substring)

weekdays = ["MONTAG", "DIENSTAG", "MITTWOCH", "DONNERSTAG", "FREI"]

indeces = map(index_containing_substring_textlist, weekdays)

date_index = index_containing_substring_textlist("vom")
date_monday = dateutil.parser.parse(text_list[date_index][len("vom"):string.find(text_list[date_index],' ')])

#menu = {'monday'    : string.join(text_list[indeces[0]+1:indeces[1]], ";"),
#        'tuesday'   : string.join(text_list[indeces[1]+1:indeces[2]], ";"),
#        'wednesday' : string.join(text_list[indeces[2]+1:indeces[3]], ";"),
#        'thursday'  : string.join(text_list[indeces[3]+1:indeces[4]], ";"),
#        'friday'    : string.join(text_list[indeces[4]+2:], ";"),
#}

#menu = {'monday'    :string.join(filter(None, map(string.strip, text_list[indeces[0]+1:indeces[1]])), ";"),
#        'tuesday'   : string.join(filter(None, map(string.strip, text_list[indeces[1]+1:indeces[2]])), ";"),
#        'wednesday' : string.join(filter(None, map(string.strip, text_list[indeces[2]+2:indeces[3]])), ";"),
#        'thursday'  : string.join(filter(None, map(string.strip, text_list[indeces[3]+1:indeces[4]])), ";"),
#        'friday'    : string.join(filter(None, map(string.strip, text_list[indeces[4]+2:])), ";"),
#}


menu = ( string.join(filter(None, map(string.strip, text_list[indeces[0]+1:indeces[1]])), ";"),
         string.join(filter(None, map(string.strip, text_list[indeces[1]+1:indeces[2]])), ";"),
         string.join(filter(None, map(string.strip, text_list[indeces[2]+2:indeces[3]])), ";"),
         string.join(filter(None, map(string.strip, text_list[indeces[3]+1:indeces[4]])), ";"),
         string.join(filter(None, map(string.strip, text_list[indeces[4]+2:])), ";")
)

for i, meal in enumerate(menu):
    data = {'meal' : meal,
            'date' : date_monday + datetime.timedelta(i),
            'restaurant' : "Ich und Du"
           }
    scraperwiki.sqlite.save(unique_keys=['date'], data=data)


#print menu
#print map(string.lstrip, menu)

#print(indeces)
#print(text_list)
#print(text_list[indeces[0]+2])
#print(text_list[indeces[0]+3])
#print(text_list[indeces[0]+4])

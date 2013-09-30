import urllib, urllib2

operations = """
[{
    "op":"core/text-transform",
    "description":"Text transform on cells in column city using expression grel:value.split(\",\")[0]",
    "engineConfig":{
      "facets":[],
      "mode":"row-based"
    },
    "columnName":"city",
    "expression":"grel:value.split(\",\")[0]",
    "onError":"set-to-blank",
    "repeat":false,
    "repeatCount":10
  },
  {
    "op":"core/text-transform",
    "description":"Text transform on cells in column venue using expression value.toUppercase()",
    "engineConfig":{
      "facets":[],
      "mode":"row-based"
    },
    "columnName":"venue",
    "expression":"value.toUppercase()",
    "onError":"keep-original",
    "repeat":false,
    "repeatCount":10
  }
]
"""

data = """
date,date_scraped,venue,city
02/10/2010,2010-04-13 11:54:42,Boettcher Concert Hall with Colorado Symphony,"Denver, CO"
24/07/2010,2010-04-13 11:54:42,Churchill Downs,"Louisville, KY"
16/05/2010,2010-04-13 11:54:41,Warfield Theatre,"San Francisco, CA"
14/05/2010,2010-04-13 11:54:41,House of Blues,"Anaheim, CA"
13/05/2010,2010-04-13 11:54:41,Henry Fonda Theatre,"Los Angeles, CA"
08/05/2010,2010-04-13 11:54:39,House of Blues,"Houston, TX"
"""

print urllib2.urlopen('http://rush.scraperwiki.com:8080/transform', urllib.urlencode({'format': 'csv',
                                                                           'operations-string': operations,
                                                                           'data-string': data,
                                                                           'data-filetype': 'text/plain',
                                                                           'data-filename': 'tom.txt'})).read()
import urllib, urllib2

operations = """
[{
    "op":"core/text-transform",
    "description":"Text transform on cells in column city using expression grel:value.split(\",\")[0]",
    "engineConfig":{
      "facets":[],
      "mode":"row-based"
    },
    "columnName":"city",
    "expression":"grel:value.split(\",\")[0]",
    "onError":"set-to-blank",
    "repeat":false,
    "repeatCount":10
  },
  {
    "op":"core/text-transform",
    "description":"Text transform on cells in column venue using expression value.toUppercase()",
    "engineConfig":{
      "facets":[],
      "mode":"row-based"
    },
    "columnName":"venue",
    "expression":"value.toUppercase()",
    "onError":"keep-original",
    "repeat":false,
    "repeatCount":10
  }
]
"""

data = """
date,date_scraped,venue,city
02/10/2010,2010-04-13 11:54:42,Boettcher Concert Hall with Colorado Symphony,"Denver, CO"
24/07/2010,2010-04-13 11:54:42,Churchill Downs,"Louisville, KY"
16/05/2010,2010-04-13 11:54:41,Warfield Theatre,"San Francisco, CA"
14/05/2010,2010-04-13 11:54:41,House of Blues,"Anaheim, CA"
13/05/2010,2010-04-13 11:54:41,Henry Fonda Theatre,"Los Angeles, CA"
08/05/2010,2010-04-13 11:54:39,House of Blues,"Houston, TX"
"""

print urllib2.urlopen('http://rush.scraperwiki.com:8080/transform', urllib.urlencode({'format': 'csv',
                                                                           'operations-string': operations,
                                                                           'data-string': data,
                                                                           'data-filetype': 'text/plain',
                                                                           'data-filename': 'tom.txt'})).read()

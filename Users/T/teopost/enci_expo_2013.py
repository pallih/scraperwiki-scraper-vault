# -*- coding: utf-8 -*-

import scraperwiki
import uuid
import re
#import sys
import string
from urllib import urlopen
from BeautifulSoup import BeautifulSoup, NavigableString

scraperwiki.sqlite.execute("drop table swdata")

for anno in [ 2013, 2014 ]:
  print 'Elaboro anno %s' % anno
  for tipo in [ 'internazionali', 'nazionali', 'regionali', 'raduni' ]:
    print 'Elaboro tipo %s' % tipo
    text = urlopen('http://enci.it/manifestazioni/%s.php?anno=%s' % (tipo, anno) ).read()
    soup = BeautifulSoup(text)
    token=soup.findAll('span')
    for item in token:
      testoIntero = item.parent.text.replace(item.text,'').replace('Comitato:','').encode('utf-8')
      data = {}
      data['id'] = uuid.uuid1()
      #data['testoIntero'] = item.parent.text.replace(item.text,'').replace('Comitato:','').encode('utf-8')

      location=re.search('(.*?)dal', item.text)
      if location is not None:
        data['location'] = '%s' % re.search('(.*?)dal', item.text).group(1).strip()

      datebegin=re.search('dal(.*?)al(.*?)$', item.text)
      if datebegin is not None:
        data['date_begin'] = '%s' % re.search('dal(.*?)al(.*?)$', item.text).group(1).strip()

      dateend=re.search('dal(.*?)al(.*?)$', item.text)
      if dateend is not None:
        data['date_end'] = '%s' % re.search('dal(.*?)al(.*?)$', item.text).group(2).strip()

      organization=re.search('(.*?)Tel.', testoIntero)
      if organization is not None:
        data['organization'] = '%s' % re.search('(.*?)Tel.', testoIntero).group(1).strip()

      phones=re.search('Tel.(.*?)$', testoIntero)
      if phones is not None:
        data['phones'] = '%s' % re.search('Tel.(.*?)$', testoIntero).group(1).strip()

      data['year'] = anno
      data['event_type'] = tipo
      scraperwiki.sqlite.save(["id"], data)




#print soup.title
#print soup.title.name
#print soup.title.string
#print soup.get_text()

#print soup.find(id="redstrong")

#print soup.findAll('span')

# -*- coding: utf-8 -*-

import scraperwiki
import uuid
import re
#import sys
import string
from urllib import urlopen
from BeautifulSoup import BeautifulSoup, NavigableString

scraperwiki.sqlite.execute("drop table swdata")

for anno in [ 2013, 2014 ]:
  print 'Elaboro anno %s' % anno
  for tipo in [ 'internazionali', 'nazionali', 'regionali', 'raduni' ]:
    print 'Elaboro tipo %s' % tipo
    text = urlopen('http://enci.it/manifestazioni/%s.php?anno=%s' % (tipo, anno) ).read()
    soup = BeautifulSoup(text)
    token=soup.findAll('span')
    for item in token:
      testoIntero = item.parent.text.replace(item.text,'').replace('Comitato:','').encode('utf-8')
      data = {}
      data['id'] = uuid.uuid1()
      #data['testoIntero'] = item.parent.text.replace(item.text,'').replace('Comitato:','').encode('utf-8')

      location=re.search('(.*?)dal', item.text)
      if location is not None:
        data['location'] = '%s' % re.search('(.*?)dal', item.text).group(1).strip()

      datebegin=re.search('dal(.*?)al(.*?)$', item.text)
      if datebegin is not None:
        data['date_begin'] = '%s' % re.search('dal(.*?)al(.*?)$', item.text).group(1).strip()

      dateend=re.search('dal(.*?)al(.*?)$', item.text)
      if dateend is not None:
        data['date_end'] = '%s' % re.search('dal(.*?)al(.*?)$', item.text).group(2).strip()

      organization=re.search('(.*?)Tel.', testoIntero)
      if organization is not None:
        data['organization'] = '%s' % re.search('(.*?)Tel.', testoIntero).group(1).strip()

      phones=re.search('Tel.(.*?)$', testoIntero)
      if phones is not None:
        data['phones'] = '%s' % re.search('Tel.(.*?)$', testoIntero).group(1).strip()

      data['year'] = anno
      data['event_type'] = tipo
      scraperwiki.sqlite.save(["id"], data)




#print soup.title
#print soup.title.name
#print soup.title.string
#print soup.get_text()

#print soup.find(id="redstrong")

#print soup.findAll('span')

# -*- coding: utf-8 -*-

import scraperwiki
import uuid
import re
#import sys
import string
from urllib import urlopen
from BeautifulSoup import BeautifulSoup, NavigableString

scraperwiki.sqlite.execute("drop table swdata")

for anno in [ 2013, 2014 ]:
  print 'Elaboro anno %s' % anno
  for tipo in [ 'internazionali', 'nazionali', 'regionali', 'raduni' ]:
    print 'Elaboro tipo %s' % tipo
    text = urlopen('http://enci.it/manifestazioni/%s.php?anno=%s' % (tipo, anno) ).read()
    soup = BeautifulSoup(text)
    token=soup.findAll('span')
    for item in token:
      testoIntero = item.parent.text.replace(item.text,'').replace('Comitato:','').encode('utf-8')
      data = {}
      data['id'] = uuid.uuid1()
      #data['testoIntero'] = item.parent.text.replace(item.text,'').replace('Comitato:','').encode('utf-8')

      location=re.search('(.*?)dal', item.text)
      if location is not None:
        data['location'] = '%s' % re.search('(.*?)dal', item.text).group(1).strip()

      datebegin=re.search('dal(.*?)al(.*?)$', item.text)
      if datebegin is not None:
        data['date_begin'] = '%s' % re.search('dal(.*?)al(.*?)$', item.text).group(1).strip()

      dateend=re.search('dal(.*?)al(.*?)$', item.text)
      if dateend is not None:
        data['date_end'] = '%s' % re.search('dal(.*?)al(.*?)$', item.text).group(2).strip()

      organization=re.search('(.*?)Tel.', testoIntero)
      if organization is not None:
        data['organization'] = '%s' % re.search('(.*?)Tel.', testoIntero).group(1).strip()

      phones=re.search('Tel.(.*?)$', testoIntero)
      if phones is not None:
        data['phones'] = '%s' % re.search('Tel.(.*?)$', testoIntero).group(1).strip()

      data['year'] = anno
      data['event_type'] = tipo
      scraperwiki.sqlite.save(["id"], data)




#print soup.title
#print soup.title.name
#print soup.title.string
#print soup.get_text()

#print soup.find(id="redstrong")

#print soup.findAll('span')

# -*- coding: utf-8 -*-

import scraperwiki
import uuid
import re
#import sys
import string
from urllib import urlopen
from BeautifulSoup import BeautifulSoup, NavigableString

scraperwiki.sqlite.execute("drop table swdata")

for anno in [ 2013, 2014 ]:
  print 'Elaboro anno %s' % anno
  for tipo in [ 'internazionali', 'nazionali', 'regionali', 'raduni' ]:
    print 'Elaboro tipo %s' % tipo
    text = urlopen('http://enci.it/manifestazioni/%s.php?anno=%s' % (tipo, anno) ).read()
    soup = BeautifulSoup(text)
    token=soup.findAll('span')
    for item in token:
      testoIntero = item.parent.text.replace(item.text,'').replace('Comitato:','').encode('utf-8')
      data = {}
      data['id'] = uuid.uuid1()
      #data['testoIntero'] = item.parent.text.replace(item.text,'').replace('Comitato:','').encode('utf-8')

      location=re.search('(.*?)dal', item.text)
      if location is not None:
        data['location'] = '%s' % re.search('(.*?)dal', item.text).group(1).strip()

      datebegin=re.search('dal(.*?)al(.*?)$', item.text)
      if datebegin is not None:
        data['date_begin'] = '%s' % re.search('dal(.*?)al(.*?)$', item.text).group(1).strip()

      dateend=re.search('dal(.*?)al(.*?)$', item.text)
      if dateend is not None:
        data['date_end'] = '%s' % re.search('dal(.*?)al(.*?)$', item.text).group(2).strip()

      organization=re.search('(.*?)Tel.', testoIntero)
      if organization is not None:
        data['organization'] = '%s' % re.search('(.*?)Tel.', testoIntero).group(1).strip()

      phones=re.search('Tel.(.*?)$', testoIntero)
      if phones is not None:
        data['phones'] = '%s' % re.search('Tel.(.*?)$', testoIntero).group(1).strip()

      data['year'] = anno
      data['event_type'] = tipo
      scraperwiki.sqlite.save(["id"], data)




#print soup.title
#print soup.title.name
#print soup.title.string
#print soup.get_text()

#print soup.find(id="redstrong")

#print soup.findAll('span')


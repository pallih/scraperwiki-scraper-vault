# BBC Radio 1 have released an API for their schedule, but Radio 4 has not; Scrape we must.
# 
# Ant Wilson 2013 

import scraperwiki 
import lxml.html 

class Data_entity(object):
    """class representing an entity (in this case a scheduled episode)"""
    
    # a dict of css selectors we want and human readable keys.
    # date-time is used to preserve uniqueness as days overlap on the website
    fields = { 'start-time' : 'abbr.start-time',
               'end-time'   : 'abbr.end_time', 
               'title'      : 'span.programme-object--title', 
               'subtitle'   : 'span.programme-object--subtitle',
               'synopsis'   : 'p.programme-object--synopsis',
               'date-time'  : 'abbr[content]'} 
    store = {}

    # when initialised, entity will parse for selectors and save resulting dict
    def __init__(self, element):
        self.element = element

        for key in self.fields:
            self.store[key] = self.get_value(self.fields[key])
            if len(self.store[key]) < 1:
                return

        scraperwiki.sqlite.save(unique_keys=["date-time"], data=self.store)

    # get text value 'worker'
    def get_value(self, css):
        value = ""
        tmp = self.element.cssselect(css)
        if len(tmp) > 0:
            if css == 'abbr[content]':
                value = tmp[0].attrib['content']
            else:
                value = tmp[0].text_content()
        return value

# main. Grabs schedule for feb. Splendid.
for day in range(1,29):
    html = scraperwiki.scrape("http://www.bbc.co.uk/radio4/programmes/schedules/fm/2013/02/%d" % day)
    root = lxml.html.fromstring(html)

    for element in root.cssselect("body li.broadcasts--group--item"):                
        Data_entity(element)# BBC Radio 1 have released an API for their schedule, but Radio 4 has not; Scrape we must.
# 
# Ant Wilson 2013 

import scraperwiki 
import lxml.html 

class Data_entity(object):
    """class representing an entity (in this case a scheduled episode)"""
    
    # a dict of css selectors we want and human readable keys.
    # date-time is used to preserve uniqueness as days overlap on the website
    fields = { 'start-time' : 'abbr.start-time',
               'end-time'   : 'abbr.end_time', 
               'title'      : 'span.programme-object--title', 
               'subtitle'   : 'span.programme-object--subtitle',
               'synopsis'   : 'p.programme-object--synopsis',
               'date-time'  : 'abbr[content]'} 
    store = {}

    # when initialised, entity will parse for selectors and save resulting dict
    def __init__(self, element):
        self.element = element

        for key in self.fields:
            self.store[key] = self.get_value(self.fields[key])
            if len(self.store[key]) < 1:
                return

        scraperwiki.sqlite.save(unique_keys=["date-time"], data=self.store)

    # get text value 'worker'
    def get_value(self, css):
        value = ""
        tmp = self.element.cssselect(css)
        if len(tmp) > 0:
            if css == 'abbr[content]':
                value = tmp[0].attrib['content']
            else:
                value = tmp[0].text_content()
        return value

# main. Grabs schedule for feb. Splendid.
for day in range(1,29):
    html = scraperwiki.scrape("http://www.bbc.co.uk/radio4/programmes/schedules/fm/2013/02/%d" % day)
    root = lxml.html.fromstring(html)

    for element in root.cssselect("body li.broadcasts--group--item"):                
        Data_entity(element)
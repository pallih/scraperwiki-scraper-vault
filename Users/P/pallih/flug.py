import scraperwiki
import lxml.html
import re
import tweepy

CONSUMER_KEY = 'WgouBfwNPC95npuAq8LzQ'
CONSUMER_SECRET = 'vfZ99E15bYpTfuNjG4BA4jhGTKgsiQQ4liPGWZA8iA'
ACCESS_TOKEN = '611299143-sFGeRQRrepvfCiFwtGjBK79fLcHWL1HoR35kEsCN'
ACCESS_SECRET = 'Wp0TXhNwDrp8CLAOKoysu4iH088emOOeY9miI9Yo'

html = scraperwiki.scrape('http://www.isavia.is')
to_regex = re.compile("Lent.*(\d\d:\d\d)",re.IGNORECASE)
from_regex = re.compile(".*\((.*)\)",re.IGNORECASE)

#print html
root = lxml.html.fromstring(html)
content = root.xpath ("//div [@class='content']/div[@class='item']")

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


for x in content:
    #print x.text_content()
    record = {}
    to = str(x.attrib['rel'])
    fromstring = str(x[0].text.encode('iso-8859-1'))
    
    #from string building
    if '(' in fromstring:
        
        from_code = from_regex.findall(fromstring)[0]
        for case in switch(from_code): 
            if case('RKV'):
                fromstring =' frá Reykjavík (' + from_code + ')'
                break
            if case('AEY'):
                fromstring = ' frá Akureyri (' + from_code  + ')'
                break
            if case('KEF'):
                fromstring = ' frá Keflavík (' + from_code  + ')'
                break
            if case('EGS'):
                fromstring = ' frá Egilsstöðum (' + from_code  + ')'
                break
            if case('IFJ'):
                fromstring = ' frá Ísafirði (' + from_code  + ')'
                break
            if case('VEY'):
                fromstring = ' frá Vestmannaeyjum (' + from_code  + ')'
                break
            if case('HFN'):
                fromstring = ' frá Hornafirði (' + from_code  + ')'
                break
            if case('GRY'):
                fromstring = ' frá Grímsey (' + from_code  + ')'
                break
            if case('BIU'):
                fromstring = ' frá Bíldudal (' + from_code  + ')'
                break
            if case('VPN'):
                fromstring = ' frá Vopnafirði (' + from_code  + ')'
                break
            if case('THO'):
                fromstring = ' frá Þórshöfn (' + from_code  + ')'
                break
            if case('TEY'):
                fromstring = ' frá Þingeyri (' + from_code  + ')'
                break
            if case('GJR'):
                fromstring = ' frá Gjögri (' + from_code  + ')'
                break
            if case(): # default, could also just omit condition or 'if True'
                fromstring = fromstring

    #to string buildin
    for case in switch(to):
        if case('RKV'):
            to=' í Reykjavík (' + to + ')'
            break
        if case('AEY'):
            to = ' á Akureyri (' + to  + ')'
            break
        if case('KEF'):
            to = ' í Keflavík (' + to  + ')'
            break
        if case('EGS'):
            to = ' á Egilsstöðum (' + to  + ')'
            break
        if case('IFJ'):
            to = ' á Ísafirði (' + to  + ')'
            break
        if case('VEY'):
            to = ' í Vestmannaeyjum (' + to  + ')'
            break
        if case('HFN'):
            to = ' á Hornafirði (' + to  + ')'
            break
        if case('GRY'):
            to = ' í Grímsey (' + to  + ')'
            break
        if case('BIU'):
            to = ' á Bíldudal (' + to  + ')'
            break
        if case('VPN'):
            to = ' á Vopnafirði (' + to  + ')'
            break
        if case('THO'):
            to = ' á Þórshöfn (' + to  + ')'
            break
        if case('TEY'):
            to = ' á Þingeyri (' + to  + ')'
            break
        if case('GJR'):
            to = ' á Gjögri (' + to  + ')'
            break
        if case(): # default, could also just omit condition or 'if True'
            to = to
    

    record['to'] = to
    #print x.text_content().encode('iso-8859-1') + ' --- ' + str(x.attrib)
    #record['from'] = x[0].text.encode('iso-8859-1')
    record['from'] = fromstring
    record['flightcode'] = x[0][0].text.encode('iso-8859-1')
    record['time'] = x[1].text.encode('iso-8859-1')
    record['date'] = x[1][0].text.encode('iso-8859-1')
    try:
        record['comment'] = x[2].text#.encode('utf-8')
    except AttributeError:
        pass 
    try:
        if 'Lent' in record['comment']:
            lent = to_regex.findall(record['comment'])
            tweet = 'Klukkan ' + lent[0] + ' lenti vél ('+record['flightcode']+') frá ' + record['from'] + record['to'] + ' - http://info.flightmapper.net/flight/'+record['flightcode'][:2]+'_'+record['flightcode'][2:]
            try:
                auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)  
                auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
                api = tweepy.API(auth)
                api.update_status(tweet)
            except Exception, e:
                print 'Failed to send tweet: %s' % tweet, e
    except TypeError:
        pass
    #print record
import scraperwiki
import lxml.html
import re
import tweepy

CONSUMER_KEY = 'WgouBfwNPC95npuAq8LzQ'
CONSUMER_SECRET = 'vfZ99E15bYpTfuNjG4BA4jhGTKgsiQQ4liPGWZA8iA'
ACCESS_TOKEN = '611299143-sFGeRQRrepvfCiFwtGjBK79fLcHWL1HoR35kEsCN'
ACCESS_SECRET = 'Wp0TXhNwDrp8CLAOKoysu4iH088emOOeY9miI9Yo'

html = scraperwiki.scrape('http://www.isavia.is')
to_regex = re.compile("Lent.*(\d\d:\d\d)",re.IGNORECASE)
from_regex = re.compile(".*\((.*)\)",re.IGNORECASE)

#print html
root = lxml.html.fromstring(html)
content = root.xpath ("//div [@class='content']/div[@class='item']")

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


for x in content:
    #print x.text_content()
    record = {}
    to = str(x.attrib['rel'])
    fromstring = str(x[0].text.encode('iso-8859-1'))
    
    #from string building
    if '(' in fromstring:
        
        from_code = from_regex.findall(fromstring)[0]
        for case in switch(from_code): 
            if case('RKV'):
                fromstring =' frá Reykjavík (' + from_code + ')'
                break
            if case('AEY'):
                fromstring = ' frá Akureyri (' + from_code  + ')'
                break
            if case('KEF'):
                fromstring = ' frá Keflavík (' + from_code  + ')'
                break
            if case('EGS'):
                fromstring = ' frá Egilsstöðum (' + from_code  + ')'
                break
            if case('IFJ'):
                fromstring = ' frá Ísafirði (' + from_code  + ')'
                break
            if case('VEY'):
                fromstring = ' frá Vestmannaeyjum (' + from_code  + ')'
                break
            if case('HFN'):
                fromstring = ' frá Hornafirði (' + from_code  + ')'
                break
            if case('GRY'):
                fromstring = ' frá Grímsey (' + from_code  + ')'
                break
            if case('BIU'):
                fromstring = ' frá Bíldudal (' + from_code  + ')'
                break
            if case('VPN'):
                fromstring = ' frá Vopnafirði (' + from_code  + ')'
                break
            if case('THO'):
                fromstring = ' frá Þórshöfn (' + from_code  + ')'
                break
            if case('TEY'):
                fromstring = ' frá Þingeyri (' + from_code  + ')'
                break
            if case('GJR'):
                fromstring = ' frá Gjögri (' + from_code  + ')'
                break
            if case(): # default, could also just omit condition or 'if True'
                fromstring = fromstring

    #to string buildin
    for case in switch(to):
        if case('RKV'):
            to=' í Reykjavík (' + to + ')'
            break
        if case('AEY'):
            to = ' á Akureyri (' + to  + ')'
            break
        if case('KEF'):
            to = ' í Keflavík (' + to  + ')'
            break
        if case('EGS'):
            to = ' á Egilsstöðum (' + to  + ')'
            break
        if case('IFJ'):
            to = ' á Ísafirði (' + to  + ')'
            break
        if case('VEY'):
            to = ' í Vestmannaeyjum (' + to  + ')'
            break
        if case('HFN'):
            to = ' á Hornafirði (' + to  + ')'
            break
        if case('GRY'):
            to = ' í Grímsey (' + to  + ')'
            break
        if case('BIU'):
            to = ' á Bíldudal (' + to  + ')'
            break
        if case('VPN'):
            to = ' á Vopnafirði (' + to  + ')'
            break
        if case('THO'):
            to = ' á Þórshöfn (' + to  + ')'
            break
        if case('TEY'):
            to = ' á Þingeyri (' + to  + ')'
            break
        if case('GJR'):
            to = ' á Gjögri (' + to  + ')'
            break
        if case(): # default, could also just omit condition or 'if True'
            to = to
    

    record['to'] = to
    #print x.text_content().encode('iso-8859-1') + ' --- ' + str(x.attrib)
    #record['from'] = x[0].text.encode('iso-8859-1')
    record['from'] = fromstring
    record['flightcode'] = x[0][0].text.encode('iso-8859-1')
    record['time'] = x[1].text.encode('iso-8859-1')
    record['date'] = x[1][0].text.encode('iso-8859-1')
    try:
        record['comment'] = x[2].text#.encode('utf-8')
    except AttributeError:
        pass 
    try:
        if 'Lent' in record['comment']:
            lent = to_regex.findall(record['comment'])
            tweet = 'Klukkan ' + lent[0] + ' lenti vél ('+record['flightcode']+') frá ' + record['from'] + record['to'] + ' - http://info.flightmapper.net/flight/'+record['flightcode'][:2]+'_'+record['flightcode'][2:]
            try:
                auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)  
                auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
                api = tweepy.API(auth)
                api.update_status(tweet)
            except Exception, e:
                print 'Failed to send tweet: %s' % tweet, e
    except TypeError:
        pass
    #print record

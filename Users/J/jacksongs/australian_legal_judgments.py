import scraperwiki
import urllib2
import string

u = 2012
v = 1


def scrapethat(u,v):
    def onerep(start,end):
        ft = html.find('for the',start)
        if ft == -1:
            return
        if ft > end:
            return
        breaker = html.rfind('>',0,ft)
        nbreaker = html.find(' ',ft+8)
        rep1 = html[breaker+2:ft]
        if 'General' in html[breaker+2:ft]:
            ft2 = html.find('for the',ft+1)
            rep1 = html[breaker+2:ft2]
        forthe = html[ft+8:nbreaker]
        if html[ft+8:nbreaker] == 'first' or 'second' or 'third' or 'fourth' or 'fifth' or 'sixth' or 'seventh' or 'eighth' or 'ninth':
            nsbreaker = html.find(' ',ft+14)
            forthe = html[ft+8:nsbreaker]
        if html[ft+8:nbreaker] == 'State':
            nnbreaker = html.find('(',ft+8)
            forthe = html[ft+8:nnbreaker]
        withhim = None
        if ' with ' in html[breaker+2:ft]:
            print 'OOOOW!'
            wither = html.find(' with ',ft+8)
            forthe = html[ft+8:wither]
            withhim = html[wither+5:nbreaker]
            print withhim
        print 'Barrister:',rep1
        print 'Representing... ',forthe
        print 'With:',withhim
        ib = html.find('instructed by',start)
        space = html.find(')',ib)
        firm = html[ib+13:space]
        if '(' in firm:
            brack2 = html.find(')',space)
            firm = html[ib+13:brack2]
        print 'Firm:',firm
        onerep(space,end)
    try:
        baseurl = 'http://www.austlii.edu.au/au/cases/cth/HCA/%(year)d/%(number)d.html' % {"year":u,"number":v}
        html = scraperwiki.scrape(baseurl)
        print baseurl
        low = html.lower()
        x = low.find('order')        
        cw = low.find('catchwords')
        r = low.find('representation')
        onerep(r,cw)
        return True
    except:
        return False

def allcases(u,v):
    while True:
        if scrapethat(u,v) == False:
            return False
        v = v + 1

while True:
    if allcases(u,v) == False:
        u = u - 1
        v = 1    

print 'done!'



import scraperwiki

import urllib2

elections = ["A"]
referendum = "F"

dates_finder = ".lista_date a"
level_finder = '.right-panel .sezione ul li a'
BASE = "http://elezionistorico.interno.it"


base_url = BASE+"/index.php?tpel="

from pyquery import PyQuery as pq

def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')

def to_dict(aind,aval):
    ret = {}
    for i in range(len(aind)):
        ret[aind[i]] = aval[i]
    return ret

for election in elections:
    print election
    # print base_url+election
    u = urllib2.urlopen(base_url+election).read()
    s = pq(u)

    for date_url in s(dates_finder):
            ud = pq(date_url)
            date = ud.attr('title')
            lev1 = ""
            lev2 = ""
            lev3 = ""
            hr = ud.attr('href')
            print date
            i = urllib2.urlopen(BASE+hr).read()
            d = pq(i)
            for l1 in d(level_finder):
                l1 = pq(l1)
                lev1 = l1.attr('title')
                print lev1
                l2u = l1.attr('href')
                print BASE+l2u
                l2c = urllib2.urlopen(BASE+l2u).read()
                f = pq(l2c)
                for l2 in f(level_finder):    
                    l2 = pq(l2)
                    lev2 = l2.attr('title')
                    print ">", lev2
                    l3u = l2.attr('href')
                    print BASE+l3u
                    l3c = urllib2.urlopen(BASE+l3u).read()
                    g = pq(l3c)
                    for l3 in g(level_finder):    
                        l3 = pq(l3)
                        lev3 = l3.attr('title')
                        print ">>", lev3
                        l4u = l3.attr('href')
                        l4c = urllib2.urlopen(BASE+l4u).read()
                        h = pq(l4c)
                        for l4 in h(level_finder):    
                            l4 = pq(l4)
                            lev4 = l4.attr('title')
                            print ">>>", lev4
                            rdu = l4.attr('href')
                            rdc = urllib2.urlopen(BASE+rdu).read()
                            j = pq(rdc)
                            print j('.dati_riepilogo td' )[0]
                            elettori = pq(j('.dati_riepilogo td')[0]).text()
                            votanti = pq(j('.dati_riepilogo td')[2]).text()
                            bianche = pq(j('.dati_riepilogo td')[5]).text()
                            nulle = pq(j('.dati_riepilogo td')[7]).text()
                            keys= ["date","l1","l2","l3","l4", "elettori", "votanti", "partito", "voti" ]
                            scraperwiki.sqlite.save(unique_keys = keys, data= to_dict(keys, [date,safe_str(lev1),safe_str(lev2),safe_str(lev3),safe_str(lev4), elettori, votanti, "BLANK", bianche]))
                            scraperwiki.sqlite.save(unique_keys = keys, data= to_dict(keys, [date,safe_str(lev1),safe_str(lev2),safe_str(lev3),safe_str(lev4), elettori, votanti, "NULL", nulle]))

                            for party in j('.dati tr').not_('.totalecomplessivovoti'):
                                k = pq(party)
                                if len(k('th'))==1:
                                    img = pq(k.children()[0])
                                    panme = pq(k.children()[1]).text()
                                    votes = pq(k.children()[2]).text()
                                    
                                    data = {}
                                    scraperwiki.sqlite.save(unique_keys = keys, data= to_dict(keys, [date,safe_str(lev1),safe_str(lev2),safe_str(lev3), safe_str(lev4), elettori, votanti, safe_str(panme), votes ]))
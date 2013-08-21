import scraperwiki
import mechanize
import lxml.html           
from pyquery import PyQuery as pq
import re

br = mechanize.Browser()
br.set_handle_robots(False)   
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

minint_url = "http://elezionistorico.interno.it/index.php?tpel=S"
response = br.open(minint_url)

def is_table(tag):
    return tag.has_key('class') and not tag.has_key('id')

def get_fontpiccolo(data):
    print data
    fp = re.compile(r"fontpiccolo\'\>(\w*\s\w*)")
    s = fp.findall(data)    
    print s
    return s

date_links = br.links(url_regex='tpel=S&dtel=13/05/2001')
elections_links = {}
for date_link in date_links:
    date_title = date_link.attrs[1][1]
    (day, month, year) = date_title.split('/')
    date_key = "%s-%s-%s" % (year, month, day)
    elections_links[date_key] = date_link.url



sorted_dates = reversed(sorted(elections_links.iterkeys()))
for el_date in sorted_dates:
    print "Data: %s" % el_date
    br.open(elections_links[el_date])

    # simulate click on Italia link in the right sidebar 
    br.open(br.click_link(url_regex='tpel=S&dtel=.*&tpa=I', nr=0))

    area_links = {}
    for l in br.links(url_regex='tpel=S&dtel=.*&tpa=I&tpe=A'):
        area_links[l.text] = l.url

    sorted_area = reversed(sorted(area_links.iterkeys()))
    for area in sorted_area:
        print " Area: %s" % area
        br.open(area_links[area])

        reg_links = {}
        for l in br.links(url_regex='tpel=S&dtel=.*&tpa=I&tpe=R'):
            reg_links[l.text] = l.url
            
        sorted_reg = reversed(sorted(reg_links.iterkeys()))
        for reg in sorted_reg:
            if reg == 'EMILIA ROMAGNA':
                print "  Regione: %s" % reg
                br.open(reg_links[reg])

            
                coll_links = {}
                for l in br.links(url_regex='tpel=S&dtel=.*&tpa=I&tpe=L'):
                    coll_links[l.text] = l.url

                sorted_coll = reversed(sorted(coll_links.iterkeys()))
                for coll in sorted_coll:
                    print "  Collegio: %s" % coll
                    br.open(coll_links[coll])    

                    com_links = {}
                    for l in br.links(url_regex='tpel=S&dtel=.*&tpa=I&tpe=C'):
                        com_links[l.text] = l.url

                    sorted_com = reversed(sorted(com_links.iterkeys()))
                    for com in sorted_com:
                        print "  Comune: %s" % com
                        br.open(com_links[com]) 
            
                        data = br.response().read()
                        cands = get_fontpiccolo(data )
                        print data
                        root = pq(data)
                        print root          
                        rows = root("table.dati tr")[1:]
                        print rows
                        j = 0
                        for row in rows:
                            rr = pq(row)
                            ths= rr('th')
                            ths1= rr('th span')
                            tds= rr('td')
                            
                            print ths
                            print ths1
                            print tds

                            data = {
                                   'date': el_date,
                                   'area': area,
                                   'reg' : reg,
                                   'collegio' : coll,
                                   'com' : com,
                                   'candidate' : cands[j] ,
                                   'party' : ths[0].text_content(),   
                                   'votes' : tds[1].text_content(), 
                                   'perc' : tds[1].text_content(),                      
                                        }
                            scraperwiki.sqlite.save(unique_keys=['date', 'area', 'reg', 'collegio', 'com', 'candidate', 'party', 'votes', 'perc'], data=data)
                            j+=1

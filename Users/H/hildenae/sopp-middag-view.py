import scraperwiki # retriving html
import lxml.html # parsing html
import re # parsing arkivsaksnr
import urlparse
import time
import datetime
import sys
from datetime import datetime
utils=scraperwiki.swimport('hildenae_utils') # for caching + pretty-print
sm=scraperwiki.swimport('sopp-middag_1')

middag="http://sopp.no/index.php?option=com_content&view=article&id=56&Itemid=67"

y_w_wd = datetime.date(datetime.now()).isocalendar()
middag_key = middag + "#" + str(y_w_wd[0])+ "-" + str(y_w_wd[1])

scraperwiki.utils.httpresponseheader("Content-Type", 'text/plain; charset="utf-8"')

#food = utils.findInCache(middag_key, tableName="__parsed")
#if food is not None:
#    print food;
#    sys.exit();

html = utils.findInCache(middag_key)
if html is None:
    html = scraperwiki.scrape(middag)
    utils.putInCache(middag_key, html)

root = lxml.html.fromstring(html)

table = sm.extractTable(root)
ctable = sm.cleanup(table)
d = sm.tableToDict(ctable);
sm.printWeek(d);


#import os
#urlquery = os.getenv('URLQUERY')

#today=False
#if urlquery and "today" in urlquery:
#    today = True

#result = ""
#for el in root.cssselect("div.content table.contentpaneopen table"):
#    tableSource = lxml.html.tostring(el)
#    if "Ukedag" in tableSource:
#        for tr in el.cssselect("tr"):
#            trs = lxml.html.tostring(tr)
#            if "Ukedag" in trs and "Matrix" in trs and "Mathilde" in trs:
#                continue
#            stuff = []
#            for td in tr.cssselect("td"):
#                tds = lxml.html.tostring(td);
#                matchObj = re.match(r'.*((Man|Tirs|Ons|Tors|Fre)dag).*$', tds, re.DOTALL)
#                if matchObj:
#                    dag=matchObj.group(1)
#                    stuff.append(matchObj.group(1))
#                    continue
#
#                #print "tds: ", tds
#
#                if tds.count("</p>") > 0:
#                    tds = tds.replace(" eller ", "/");
#                    num_dish = tds.count("<br>");
#                    tds = tds.replace("<br>", ", ", num_dish-1);
#                    tds = tds.replace("<br>", ", eller ");
#                    td = lxml.html.fromstring(tds)
#                    dishes = []
#                    for p in td.cssselect("p"):
#                        #print "p:", p.text_content().strip()
#                        dishes.append(p.text_content().strip())
#                    if len(dishes) <= 2:
#                        text = ", eller ".join(dishes)
#                    else:
#                        tmptext = ", ".join(dishes[0:-1])
#                        text = ", eller ".join([tmptext, dishes[len(dishes)-1]])
#                        
#                else:
#                    num_dish = tds.count("<br>");
#                    #print num_dish_p, num_dish
#                    tds = tds.replace("<br>", ", ", num_dish-1);
#                    tds = tds.replace("<br>", " eller ");
#
#                    td = lxml.html.fromstring(tds)
#                    text = td.text_content().strip()
#
#                if (text.endswith(" eller")):
#                    text = text[:-6]
#                    li = text.rsplit(",", 1)
#                    text = ', eller'.join(li)
#                stuff.append(text.strip().replace('m/', "med "))
#                #print stuff
#                stuff = [item.capitalize() for item in stuff]
#                #print stuff
#            if today:
#                daynum = int(time.strftime("%w"))
#                if daynum < 1 or daynum > 5:
#                    print "ERROR: Kantina er ikke åpen i dag"
#                    exit(0)
#                days = ["", "Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag"]
#                if days[daynum] == dag:
#                    result = result + ";".join(stuff)
#            else:
#                result = result + ";".join(stuff) +"\n"
#utils.putInCache(middag_key, result.strip().encode('utf-8-sig'), tableName="__parsed")
#print result.strip();
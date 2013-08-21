import scraperwiki
import lxml.html
import datetime

"""Scrapes Yahoo Finance Stock Page and builds data set for daily \
    stock information. Modify HTML as needed for different stock pages."""
#Website definition
html = scraperwiki.scrape("http://finance.yahoo.com/q?s=NYX")
root = lxml.html.fromstring(html)

def storeData(websiteData):
    lastNum = 0

    try:
        scraperwiki.sqlite.execute("""\
            create table storage (id INTEGER PRIMARY KEY AUTOINCREMENT)""")
    except:
        print "Table already exists."

    scraperwiki.sqlite.save(unique_keys=[], \
        data = websiteData,\
        table_name='storage')

def parenthesisCutter(string):
    while string[0] == ' ':
        stringlen = len(string)
        string = string[1:stringlen]

    firstplace = string.find('(')
    secondplace = string.find(')')
    part1 = string[0:firstplace]
    part2 = string[firstplace+1:secondplace]
    return (part1 , part2)

def remX(string):
    while string[0] == ' ':
        stringlen = len(string)
        string = string[1:stringlen]
    
    firstplace = string.find('x')
    hold = firstplace+2
    part1 = string[0:firstplace]
    part2 = string[hold:len(string)]
    return (part1, part2)

def remsign(string):
    while string[0] == ' ':
        stringlen = len(string)
        string = string[1:stringlen]
    
    firstplace = string.find('-')
    hold = firstplace+2
    part1 = string[0:firstplace]
    part2 = string[hold:len(string)]
    return (part1, part2)

#Data

info = {}
info['exchange'] = 'NYSE'
info['ticker'] = 'NYX'
info['accessTime'] = datetime.datetime.now()
info['close'] = float(root.cssselect("span.time_rtq_ticker")[0].text_content())
hold_change = parenthesisCutter(str(root.cssselect("span.up_g")[0].text_content()))
info['change'] = float(hold_change[0])
info['percentChange'] = hold_change[1]
info['prevClose'] = float(root.cssselect("td.yfnc_tabledata1")[0].text_content())
info['open'] = float(root.cssselect("td.yfnc_tabledata1")[1].text_content())
hold_bid = remX(str(root.cssselect("td.yfnc_tabledata1")[2].text_content()))
hold_ask = remX(str(root.cssselect("td.yfnc_tabledata1")[3].text_content()))
info['bid'] = float(hold_bid[0])
info['bid_quant'] = int(hold_bid[1])
info['ask'] = float(hold_ask[0])
info['ask_quant'] = int(hold_ask[1])
info['1yrTarEst'] = float(str(root.cssselect("td.yfnc_tabledata1")[4].text_content()))
info['beta'] = float(str(root.cssselect("td.yfnc_tabledata1")[4].text_content()))
hold_spread = remsign(str(root.cssselect("td.yfnc_tabledata1")[7].text_content()))
info['spreadMax'] = float(hold_spread[0])
info['spreadMin'] = float(hold_spread[1])
hold_52wk = remsign(str(root.cssselect("td.yfnc_tabledata1")[8].text_content()))
info['spreadMax'] = float(hold_52wk[0])
info['spreadMin'] = float(hold_52wk[1])
info['volume'] = int(root.cssselect("td.yfnc_tabledata1")[9].text_content().replace(",", ""))
info['avVolume'] = int(root.cssselect("td.yfnc_tabledata1")[10].text_content().replace(",", ""))
info['markcap'] = str(root.cssselect("td.yfnc_tabledata1")[11].text_content())
info['pe'] = float(root.cssselect("td.yfnc_tabledata1")[12].text_content())
info['eps'] = float(root.cssselect("td.yfnc_tabledata1")[13].text_content())
hold_divyld = parenthesisCutter(str(root.cssselect("td.yfnc_tabledata1")[14].text_content()))
info['div'] = float(hold_divyld[0])
info['yield'] = hold_divyld[1]
print info
storeData(info)

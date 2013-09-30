import scraperwiki

sources = \
    [
    'dividendexdividenddate',
    'dividendyahoo',
    'dividendadvfn',
    'dividendstockopedia',
    'dividenddividendinvestor',
    'dividendshemscott',
    'dividendnorthcote',
    'dividendiii',
    'dividendsproactive'
    ]

def copy_data (source):
    print source
    scraperwiki.sqlite.attach(source, source)
    try:
        alldata = scraperwiki.sqlite.select("* from %s.swdata" % source)
        scraperwiki.sqlite.save (unique_keys=["Source", "Ticker", "ExDivDate", "Type"], data=alldata)
    except:
        print "Failed ", source
        

for s in sources:
    copy_data (s)
import scraperwiki

sources = \
    [
    'dividendexdividenddate',
    'dividendyahoo',
    'dividendadvfn',
    'dividendstockopedia',
    'dividenddividendinvestor',
    'dividendshemscott',
    'dividendnorthcote',
    'dividendiii',
    'dividendsproactive'
    ]

def copy_data (source):
    print source
    scraperwiki.sqlite.attach(source, source)
    try:
        alldata = scraperwiki.sqlite.select("* from %s.swdata" % source)
        scraperwiki.sqlite.save (unique_keys=["Source", "Ticker", "ExDivDate", "Type"], data=alldata)
    except:
        print "Failed ", source
        

for s in sources:
    copy_data (s)

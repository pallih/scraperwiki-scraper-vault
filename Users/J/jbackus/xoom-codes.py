import scraperwiki
import lxml.html

countryUrls = [
    '/argentina',
    '/australia',
    '/bolivia',
    '/brazil',
    '/canada',
    '/chile',
    '/colombia',
    '/costa-rica',
    '/dominican-republic',
    '/ecuador',
    '/el-salvador',
    '/france',
    '/germany',
    '/guatemala',
    '/honduras',
    '/india',
    '/ireland',
    '/italy',
    '/jamaica',
    '/mexico',
    '/netherlands',
    '/nicaragua',
    '/panama',
    '/peru',
    '/philippines',
    '/poland',
    '/south-africa',
    '/spain',
    '/united-kingdom',
    '/uruguay'
]


for url in countryUrls:
    html = scraperwiki.scrape("https://www.xoom.com"+url+"/fees")
    root = lxml.html.fromstring(html)
    code_meta = root.cssselect("meta[name='receiveCountryCode']")
    code_meta = code_meta[0]
    data = {
        'uri'  : url,
        'code' : code_meta.attrib['content']
    }
    scraperwiki.sqlite.save(unique_keys=['code'], data=data)
        
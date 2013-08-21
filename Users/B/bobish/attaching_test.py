import scraperwiki
import urlparse
import lxml.html

# Blank Python
def clean(text):
    text = text.replace("u\'","")
    text = text.replace("\'","")
    text = text.replace("\\xa0","")
    text = text.strip('[]')
    return text
    
cnt = 0
scraperwiki.sqlite.attach("url_data", "src") 

#scraperwiki.sqlite.attach("url_data")
results = scraperwiki.sqlite.select("url from src.swdata limit 10")


for company in results:
    companyurl = company['url']
    url = "{0}".format(companyurl)
    html = scraperwiki.scrape(url)
    
    tree = lxml.html.parse(url)
    cnt =cnt + 1
    data = {}
    data['id'] = cnt
    data['name'] = tree.xpath("//table[@id='company']/tr[1]/td/text()")
    data['name'] = clean(str(data['name']))
    data['address'] = tree.xpath("//table[@id='company']/tr[2]/td/text()")
    data['address'] = clean(str(data['address']))
    data['zip'] = tree.xpath("//table[@id='company']/tr[3]/td/text()")
    data['zip'] = clean(str(data['zip']))
    data['city'] = tree.xpath("//table[@id='company']/tr[4]/td/text()")
    data['city'] = clean(str(data['city']))
    data['region'] = tree.xpath("//table[@id='company']/tr[5]/td/text()")
    data['region'] = clean(str(data['region']))
    data['country'] = tree.xpath("//table[@id='company']/tr[6]/td/text()")
    data['country'] = clean(str(data['country']))
    data['phone'] = tree.xpath("//table[@id='company']/tr[7]/td/text()")
    data['phone'] = clean(str(data['phone']))
    data['fax'] = tree.xpath("//table[@id='company']/tr[8]/td/text()")
    data['fax'] = clean(str(data['fax']))
    data['email'] = tree.xpath("//table[@id='company']/tr[9]/td/a/text()")
    data['email'] = clean(str(data['email']))
    data['web'] = tree.xpath("//table[@id='company']/tr[10]/td/a/text()")
    data['web'] = clean(str(data['web']))
    data['services'] = tree.xpath("//table[@id='company']/tr[11]/td/text()")
    data['services'] = clean(str(data['services']))
    data['certi'] = tree.xpath("//table[@id='company']/tr[12]/td/text()")
    data['certi'] = clean(str(data['certi']))
    data['compcer'] = tree.xpath("//table[@id='company']/tr[13]/td/text()")
    data['compcer'] = clean(str(data['compcer']))
    data['linktocert'] = tree.xpath("//table[@id='company']/tr[14]/td/text()")
    data['linktocert'] = clean(str(data['linktocert']))
    data['label'] = tree.xpath("//table[@id='company']/tr[15]/td/text()")
    data['label'] = clean(str(data['label']))
    data['surface'] = tree.xpath("//table[@id='company']/tr[16]/td/text()")
    data['surface'] = clean(str(data['surface']))
    data['founded'] = tree.xpath("//table[@id='company']/tr[17]/td/text()")
    data['founded'] = clean(str(data['founded']))
    data['contact'] = tree.xpath("//table[@id='company']/tr[18]/td/text()")
    data['contact'] = clean(str(data['contact']))
    data['product_sell'] = tree.xpath("//table[@id='company']/tr[19]/td/text()")
    data['product_sell'] = clean(str(data['product_sell']))
    data['product_buy'] = tree.xpath("//table[@id='company']/tr[20]/td/text()")
    data['product_buy'] = clean(str(data['product_buy']))
    data['service_pro'] = tree.xpath("//table[@id='company']/tr[21]/td/text()")
    data['service_pro'] = clean(str(data['service_pro']))
    data['comp_prof'] = tree.xpath("//table[@id='company']/tr[22]/td/text()")
    data['comp_prof'] = clean(str(data['comp_prof']))
    scraperwiki.sqlite.save(['id'], data)


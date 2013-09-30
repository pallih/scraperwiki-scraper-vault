# Based on https://gist.github.com/1893036

import scraperwiki
import cgi, os
import lxml.html
import datetime
import dateutil.parser
import json

import suds # suds from https://fedorahosted.org/suds/
import sys

class JSONDateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)

def get_dell_warr(svctag):
    # Should this be xserv.dell.com instead?
    url = "http://xserv.ins.dell.com/services/AssetService.asmx?WSDL"
    client = suds.client.Client(url)
    #print client
    res=client.service.GetAssetInformation('12345678-1234-1234-1234-123456789012', 'dellwarrantycheck', svctag)

    #print client.dict(res)

    hdrdata=res['Asset'][0]['AssetHeaderData']
    ent=res['Asset'][0]['Entitlements'][0]

    shipped=hdrdata['SystemShipDate']
    warrs=[]
    for i in ent:
        if i==None:
            continue
        warrs.append(i['EndDate'])

    warrs.sort()
    endwarranty=warrs[-1]

    return (url, shipped.strftime("%Y-%m-%d"), endwarranty.strftime("%Y-%m-%d"))

def get_dell_warr_html(servicetag):
    url = "http://support.euro.dell.com/support/topics/topic.aspx/emea/shared/support/my_systems_info/no/details?c=no&cs=nodhs1&l=no&s=dhs&ServiceTag=%s" % servicetag;

    return (url, "unknown", "unknown")

def get_hp_warr(servicetag, productnumber):
    if -1 != productnumber.find("#"):
        productnumber = (productnumber.split("#"))[0]
    url = 'http://h20000.www2.hp.com/bizsupport/TechSupport/WarrantyResults.jsp?lang=en&cc=us&sn=%s&pn=%s&country=NO&find=Display+Warranty+Information' % (servicetag, productnumber);

    #print url

    shipped = "unknown"
    endw = "unknown"

    # /html/body/table[4]/tbody/tr/td[2]/table/tbody/tr[7]/td
    # <td align="left" colspan="2" valign="top" height="8">

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    tables = root.cssselect("td[height='8'] table")

    t = tables[1]
    entries = []
    shipped = None
    endw = None
    d = {}
    trs = t.cssselect("tr")
    for tr in trs:
        tds = tr.cssselect("td")
        if False:
            print "TR:"
            for td in tds:
                print "TD:" + td.text_content().strip()
                print td.attrib
        if 'Warranty type' != tds[0].text_content().strip() and \
            (('rowspan' in tds[0].attrib and '2' == tds[0].attrib['rowspan']) or \
            (2 == len(trs))):
            wtype = tds[0].text_content().strip()
            d['warrantytype'] = wtype
            d['servicetype'] = tds[1].text_content().strip()
            d['startdate'] = dateutil.parser.parse(tds[2].text_content().strip()).date()
            if not shipped or shipped > d['startdate']:
                shipped = d['startdate']
            d['enddate'] = dateutil.parser.parse(tds[3].text_content().strip()).date()
            if not endw or endw < d['enddate']:
                endw = d['enddate']
            d['status'] = tds[4].text_content().strip()
            d['servicelevel'] = tds[5].text_content().strip()
            d['deliverables'] = tds[6].text_content().strip()
            #print d
        else:
            if 2 < len(tds):
                if 'warrantytype' in d:
                    entries.append(d)
                # FIXME Should handle these rows too (include new service type with same warranty type
                d = {}
            else:
                d['servicetypedesc'] = tds[0].text_content().strip()
            if 'warrantytype' in d:
                entries.append(d)
                d = {}
    #print "E: " + str(entries)
    return (url, shipped, endw)

def get_ibm_warr(servicetag, productnumber):
    # Examples: servicetag=KKPAH1X productid=8670-M1X
    url = "http://www-947.ibm.com/systems/support/supportsite.wss/warranty?action=warranty&brandind=5000008&Submit=Submit&type=%s&serial=%s" % (productnumber, servicetag)
    print url
    shipped = "unknown"
    endw = "unknown"
    return (url, shipped, endw)

def html_form():
    return """
<p>Sites with many computers need to keep track of the support status for each computer, and this is best done automatically. Several computer vendors provide web services to look up the support status of a given machine, using service tag, serial number, product type etc. The problem with these vendor sites is that they return the information on different formats.</p>

<p>This scraper/service is trying to do something about this, by providing a service to look up and standardise the information provided by vendors, and keep a copy of the scraped information to make sure the status can be queried again even if the vendor change the web service or the vendor site is unavailable.</p>

<p>The Dell and HP lookup work, the IBM one do not work yet.</p>

<p><form>
Format: <select name='format'><option value="html">HTML</option><option value="json">JSON</option><option value="xml">XML</option></select>    
<br>Vendor: <select name='vendor'><option value="Dell">Dell</option><option value="HP">HP</option><option value="IBM">IBM</option></select>    
<br>Servicetag/Serial number: <form><input name='servicetag'>
<br>Product number: <form><input name='productid'> (Used on HP and IBM)
<br><input type="submit" value="Submit" />
</form></p>

<p>See <a href="https://scraperwiki.com/views/computer-hardware-support-status/">scraperwiki</a> for the source.</p>
"""

def scrape(paramdict):
    servicetag = paramdict['servicetag']
    vendor = paramdict['vendor']
    data = {
        'vendor' : vendor,
        'servicetag' : '',
        'productid' : '',
    }
    unique_keys = ["servicetag", 'productid']
    if 'Dell' == vendor:
        servicetag = paramdict['servicetag'].lower()
        data['servicetag'] = servicetag
        (url, shipped, endw) = get_dell_warr(servicetag)
    elif 'HP' == vendor:
        servicetag = paramdict['servicetag'].lower()
        productid = paramdict['productid'].lower()
        data['productid'] = productid
        data['servicetag'] = servicetag
        (url, shipped, endw) = get_hp_warr(servicetag, productid)
    elif 'IBM' == vendor:
        servicetag = paramdict['servicetag']
        productid = paramdict['productid']
        data['productid'] = productid
        data['servicetag'] = servicetag
        (url, shipped, endw) = get_ibm_warr(servicetag, productid)
    else:
        raise ValueError("Unknown vendor " + vendor)
    data['shipped'] = shipped
    data['warrantyend'] = endw
    data['scrapedurl'] = url
    data['scrapestamputc'] = datetime.datetime.now()
    #print data
    scraperwiki.sqlite.save(unique_keys=unique_keys, data=data)
    return data

def test():
    scrape(paramdict = {'vendor' : 'Dell', 'servicetag' : '8DSGD2J'})
    scrape(paramdict = {'vendor' : 'Dell', 'servicetag' : 'BPCG0P1'})

    scrape(paramdict = {'vendor' : 'IBM', 'servicetag' : 'KKPAH1X', 'productid' : '8670-M1X'})
    scrape(paramdict = {'vendor' : 'IBM', 'servicetag' : 'KBLR940', 'productid' : '8670-52G'})
    scrape(paramdict = {'vendor' : 'IBM', 'servicetag' : 'L3CD933', 'productid' : '2526WKF'})

    scrape(paramdict = {'vendor' : 'HP', 'servicetag' : 'cnd8521bw9', 'productid' : 'NA039EA'})
    scrape(paramdict = {'vendor' : 'HP', 'servicetag' : 'GB8730N8SX', 'productid' : '414109-B21'})
    exit(0)

def scraper():
    paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
    if 'test' in paramdict:
        test()
    if 'servicetag' not in paramdict:
        print html_form()
        return 0
    data = scrape(paramdict)
    if 'format' in paramdict and paramdict['format'] == 'json':
        scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
        print 'supportstatus('+json.dumps(data, cls=JSONDateTimeEncoder)+')'
    elif 'format' in paramdict and paramdict['format'] == 'xml':
        scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")
        print "<supportstatus>"
        for key in data.keys():
            print "<%s>%s</%s>" % (key, data[key], key)
        print "</supportstatus>"
    else:
        for key in data.keys():
            print "<p>%s: %s</p>" % (key, data[key])
    return 0

if __name__ == "scraper":
    exit(scraper())# Based on https://gist.github.com/1893036

import scraperwiki
import cgi, os
import lxml.html
import datetime
import dateutil.parser
import json

import suds # suds from https://fedorahosted.org/suds/
import sys

class JSONDateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)

def get_dell_warr(svctag):
    # Should this be xserv.dell.com instead?
    url = "http://xserv.ins.dell.com/services/AssetService.asmx?WSDL"
    client = suds.client.Client(url)
    #print client
    res=client.service.GetAssetInformation('12345678-1234-1234-1234-123456789012', 'dellwarrantycheck', svctag)

    #print client.dict(res)

    hdrdata=res['Asset'][0]['AssetHeaderData']
    ent=res['Asset'][0]['Entitlements'][0]

    shipped=hdrdata['SystemShipDate']
    warrs=[]
    for i in ent:
        if i==None:
            continue
        warrs.append(i['EndDate'])

    warrs.sort()
    endwarranty=warrs[-1]

    return (url, shipped.strftime("%Y-%m-%d"), endwarranty.strftime("%Y-%m-%d"))

def get_dell_warr_html(servicetag):
    url = "http://support.euro.dell.com/support/topics/topic.aspx/emea/shared/support/my_systems_info/no/details?c=no&cs=nodhs1&l=no&s=dhs&ServiceTag=%s" % servicetag;

    return (url, "unknown", "unknown")

def get_hp_warr(servicetag, productnumber):
    if -1 != productnumber.find("#"):
        productnumber = (productnumber.split("#"))[0]
    url = 'http://h20000.www2.hp.com/bizsupport/TechSupport/WarrantyResults.jsp?lang=en&cc=us&sn=%s&pn=%s&country=NO&find=Display+Warranty+Information' % (servicetag, productnumber);

    #print url

    shipped = "unknown"
    endw = "unknown"

    # /html/body/table[4]/tbody/tr/td[2]/table/tbody/tr[7]/td
    # <td align="left" colspan="2" valign="top" height="8">

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    tables = root.cssselect("td[height='8'] table")

    t = tables[1]
    entries = []
    shipped = None
    endw = None
    d = {}
    trs = t.cssselect("tr")
    for tr in trs:
        tds = tr.cssselect("td")
        if False:
            print "TR:"
            for td in tds:
                print "TD:" + td.text_content().strip()
                print td.attrib
        if 'Warranty type' != tds[0].text_content().strip() and \
            (('rowspan' in tds[0].attrib and '2' == tds[0].attrib['rowspan']) or \
            (2 == len(trs))):
            wtype = tds[0].text_content().strip()
            d['warrantytype'] = wtype
            d['servicetype'] = tds[1].text_content().strip()
            d['startdate'] = dateutil.parser.parse(tds[2].text_content().strip()).date()
            if not shipped or shipped > d['startdate']:
                shipped = d['startdate']
            d['enddate'] = dateutil.parser.parse(tds[3].text_content().strip()).date()
            if not endw or endw < d['enddate']:
                endw = d['enddate']
            d['status'] = tds[4].text_content().strip()
            d['servicelevel'] = tds[5].text_content().strip()
            d['deliverables'] = tds[6].text_content().strip()
            #print d
        else:
            if 2 < len(tds):
                if 'warrantytype' in d:
                    entries.append(d)
                # FIXME Should handle these rows too (include new service type with same warranty type
                d = {}
            else:
                d['servicetypedesc'] = tds[0].text_content().strip()
            if 'warrantytype' in d:
                entries.append(d)
                d = {}
    #print "E: " + str(entries)
    return (url, shipped, endw)

def get_ibm_warr(servicetag, productnumber):
    # Examples: servicetag=KKPAH1X productid=8670-M1X
    url = "http://www-947.ibm.com/systems/support/supportsite.wss/warranty?action=warranty&brandind=5000008&Submit=Submit&type=%s&serial=%s" % (productnumber, servicetag)
    print url
    shipped = "unknown"
    endw = "unknown"
    return (url, shipped, endw)

def html_form():
    return """
<p>Sites with many computers need to keep track of the support status for each computer, and this is best done automatically. Several computer vendors provide web services to look up the support status of a given machine, using service tag, serial number, product type etc. The problem with these vendor sites is that they return the information on different formats.</p>

<p>This scraper/service is trying to do something about this, by providing a service to look up and standardise the information provided by vendors, and keep a copy of the scraped information to make sure the status can be queried again even if the vendor change the web service or the vendor site is unavailable.</p>

<p>The Dell and HP lookup work, the IBM one do not work yet.</p>

<p><form>
Format: <select name='format'><option value="html">HTML</option><option value="json">JSON</option><option value="xml">XML</option></select>    
<br>Vendor: <select name='vendor'><option value="Dell">Dell</option><option value="HP">HP</option><option value="IBM">IBM</option></select>    
<br>Servicetag/Serial number: <form><input name='servicetag'>
<br>Product number: <form><input name='productid'> (Used on HP and IBM)
<br><input type="submit" value="Submit" />
</form></p>

<p>See <a href="https://scraperwiki.com/views/computer-hardware-support-status/">scraperwiki</a> for the source.</p>
"""

def scrape(paramdict):
    servicetag = paramdict['servicetag']
    vendor = paramdict['vendor']
    data = {
        'vendor' : vendor,
        'servicetag' : '',
        'productid' : '',
    }
    unique_keys = ["servicetag", 'productid']
    if 'Dell' == vendor:
        servicetag = paramdict['servicetag'].lower()
        data['servicetag'] = servicetag
        (url, shipped, endw) = get_dell_warr(servicetag)
    elif 'HP' == vendor:
        servicetag = paramdict['servicetag'].lower()
        productid = paramdict['productid'].lower()
        data['productid'] = productid
        data['servicetag'] = servicetag
        (url, shipped, endw) = get_hp_warr(servicetag, productid)
    elif 'IBM' == vendor:
        servicetag = paramdict['servicetag']
        productid = paramdict['productid']
        data['productid'] = productid
        data['servicetag'] = servicetag
        (url, shipped, endw) = get_ibm_warr(servicetag, productid)
    else:
        raise ValueError("Unknown vendor " + vendor)
    data['shipped'] = shipped
    data['warrantyend'] = endw
    data['scrapedurl'] = url
    data['scrapestamputc'] = datetime.datetime.now()
    #print data
    scraperwiki.sqlite.save(unique_keys=unique_keys, data=data)
    return data

def test():
    scrape(paramdict = {'vendor' : 'Dell', 'servicetag' : '8DSGD2J'})
    scrape(paramdict = {'vendor' : 'Dell', 'servicetag' : 'BPCG0P1'})

    scrape(paramdict = {'vendor' : 'IBM', 'servicetag' : 'KKPAH1X', 'productid' : '8670-M1X'})
    scrape(paramdict = {'vendor' : 'IBM', 'servicetag' : 'KBLR940', 'productid' : '8670-52G'})
    scrape(paramdict = {'vendor' : 'IBM', 'servicetag' : 'L3CD933', 'productid' : '2526WKF'})

    scrape(paramdict = {'vendor' : 'HP', 'servicetag' : 'cnd8521bw9', 'productid' : 'NA039EA'})
    scrape(paramdict = {'vendor' : 'HP', 'servicetag' : 'GB8730N8SX', 'productid' : '414109-B21'})
    exit(0)

def scraper():
    paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
    if 'test' in paramdict:
        test()
    if 'servicetag' not in paramdict:
        print html_form()
        return 0
    data = scrape(paramdict)
    if 'format' in paramdict and paramdict['format'] == 'json':
        scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
        print 'supportstatus('+json.dumps(data, cls=JSONDateTimeEncoder)+')'
    elif 'format' in paramdict and paramdict['format'] == 'xml':
        scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")
        print "<supportstatus>"
        for key in data.keys():
            print "<%s>%s</%s>" % (key, data[key], key)
        print "</supportstatus>"
    else:
        for key in data.keys():
            print "<p>%s: %s</p>" % (key, data[key])
    return 0

if __name__ == "scraper":
    exit(scraper())
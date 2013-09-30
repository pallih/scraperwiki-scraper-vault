import scraperwiki
import urllib2
import urllib
import BeautifulSoup as bs
import lxml.html

url ='http://202.166.205.141/bbvrs/view_ward.php'
scraperwiki.sqlite.attach("regions", "reg")

def getpage(url, query_args):
    data = urllib.urlencode(query_args)
    request = urllib2.Request(url, data)
    response = urllib2.urlopen(request)
    page = response.read()
    
    return page

startval=10000
errorno = 0
try:
    offsetrow = scraperwiki.sqlite.select("max(count_id) from swdata")
    offset = offsetrow[0]['max(count_id)']
except:
    pass
if offset>37000:
    offset = startval
print offset
endval = startval + 5000
for i in range(offset, endval):
    rows = scraperwiki.sqlite.select("* from reg.swdata where count_id="+str(i+errorno))
    for row in rows:
        post_data = { 'district' : row['district_id'], 'vdc_mun' : row['vdc_id'], 'ward' : row['wards'], 'hidVdcType' : row['vdc_type'], 'reg_centre' : row['region_id'] } 
        try:
            page = getpage(url, post_data)

            root = lxml.html.fromstring(page)
            voters = root.cssselect("div.div_bbvrs_data table.bbvrs_data tr")
            voters.pop(0)
            for voter in voters:
                try:
                    voter_id = voter[1].text_content()
                    voter_name = voter[2].text_content()
                    voter_sex = voter[3].text_content()
                    voter_father = voter[4].text_content()
                    voter_mother = voter[5].text_content()
                    data = {'count_id':i, 'voter_id' : voter_id, 'voter_name' : voter_name, 'voter_sex':voter_sex,'voter_father':voter_father,'voter_mother':voter_mother}
                    scraperwiki.sqlite.save(unique_keys=['voter_id'], data=data)
                except:
                    pass
        except:
            errorno -= 1
import scraperwiki
import urllib2
import urllib
import BeautifulSoup as bs
import lxml.html

url ='http://202.166.205.141/bbvrs/view_ward.php'
scraperwiki.sqlite.attach("regions", "reg")

def getpage(url, query_args):
    data = urllib.urlencode(query_args)
    request = urllib2.Request(url, data)
    response = urllib2.urlopen(request)
    page = response.read()
    
    return page

startval=10000
errorno = 0
try:
    offsetrow = scraperwiki.sqlite.select("max(count_id) from swdata")
    offset = offsetrow[0]['max(count_id)']
except:
    pass
if offset>37000:
    offset = startval
print offset
endval = startval + 5000
for i in range(offset, endval):
    rows = scraperwiki.sqlite.select("* from reg.swdata where count_id="+str(i+errorno))
    for row in rows:
        post_data = { 'district' : row['district_id'], 'vdc_mun' : row['vdc_id'], 'ward' : row['wards'], 'hidVdcType' : row['vdc_type'], 'reg_centre' : row['region_id'] } 
        try:
            page = getpage(url, post_data)

            root = lxml.html.fromstring(page)
            voters = root.cssselect("div.div_bbvrs_data table.bbvrs_data tr")
            voters.pop(0)
            for voter in voters:
                try:
                    voter_id = voter[1].text_content()
                    voter_name = voter[2].text_content()
                    voter_sex = voter[3].text_content()
                    voter_father = voter[4].text_content()
                    voter_mother = voter[5].text_content()
                    data = {'count_id':i, 'voter_id' : voter_id, 'voter_name' : voter_name, 'voter_sex':voter_sex,'voter_father':voter_father,'voter_mother':voter_mother}
                    scraperwiki.sqlite.save(unique_keys=['voter_id'], data=data)
                except:
                    pass
        except:
            errorno -= 1

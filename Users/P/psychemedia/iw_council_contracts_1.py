import scraperwiki
import mechanize
import lxml.html

def flatten(el):           
    result = [ (el.text or "") ]
    for sel in el:
        result.append(flatten(sel))
        result.append(sel.tail or "")
    return "".join(result)

url='http://www.iwight.com/contracts/'


def parseContractPage(page,typ):
    print page
    root = lxml.html.fromstring(page)
    table=root.xpath('//table[@id="dgSearchResults"]')[0]
    for row in table.xpath('tr')[1:]:
        print 'contracts',flatten(row)
        print row.xpath('td/a/@onclick')[0],row.xpath('td/a')[0].text,row.xpath('td')[1].text,row.xpath('td')[2].text
        data={}
        data['id']=row.xpath('td/a/@onclick')[0].replace("window.open('",'').replace("')",'').strip(';')
        data['name']=row.xpath('td/a')[0].text
        data['amount']=row.xpath('td')[1].text
        data['date']=row.xpath('td')[2].text
        data['typ']=typ

        scraperwiki.sqlite.save(unique_keys=['id'], table_name='contractList', data=data)

scrape=0
if scrape==1:
    br = mechanize.Browser()
    
    response = br.open(url)
    print response.read()
    
    #for form in br.forms():
        #print "Form name:", form.name
        #print form
    
    br.form = list(br.forms())[0]
    
    for control in br.form.controls:
        #print control.name
        if control.type == "select" and control.name=='ddlCat':  # means it's class ClientForm.SelectControl
            for item in control.items[1:]:
                print " name=%s values=%s" % (item.name, str([label.text  for label in item.get_labels()]))
                label=[label.text  for label in item.get_labels()][0]
                br['ddlCat'] = [ item.name ]
                response2 = br.submit()
                #print response.read()
                parseContractPage(response2.read(),label)
                br.back()
                br.form = list(br.forms())[0]

#Get contract
q = '* FROM `contractList`'
data = scraperwiki.sqlite.select(q)

headings=['Contract Title', 'Selection Method','Framework','Type of Contract','Category of Spend','Contract Start','Contract End', 'End date of extension', 'Annual value', 'Total Contract Value','Currency','Title','Name']

#scraperwiki.sqlite.execute('drop table "contractDetails"')

#----ish via http://stackoverflow.com/a/379966/454773
def num (s):
    s=s.replace(',','')
    try:
        return int(s)
    except:
        return float(s)
#----

for item in data:
    curl=url+item['id']
    data={'id':item['id']}
    html = scraperwiki.scrape(curl)
    print html
    root = lxml.html.fromstring(html)
    rows=root.xpath('//tr')
    for row in rows:
        cells=row.xpath('td')
        #print cells
        if len(cells) >1 and cells[1].text!=None:
            if cells[1].text.strip() in headings:
                if cells[2]!=None:
                    #print cells[1].text.strip(),':-:', flatten(cells[2])
                    data[cells[1].text.strip()] = flatten(cells[2])
                else:
                    #print cells[1].text.strip()
                    data[cells[1].text.strip()]=''
            elif cells[1].text.strip()=='Option to extend':
                #print 'Option to extend',cells[2].xpath('table/tr/td/input[@checked="checked"]/../label')[0].text
                data['Option to extend']=cells[2].xpath('table/tr/td/input[@checked="checked"]/../label')[0].text
    numtidy=['Annual value', 'Total Contract Value']
    for tidy in numtidy:
        data[tidy]=num(data[tidy]) 
    #Also consider properly date-ifying dates?
    scraperwiki.sqlite.save(unique_keys=['id'], table_name='contractDetails', data=data)
import scraperwiki
import mechanize
import lxml.html

def flatten(el):           
    result = [ (el.text or "") ]
    for sel in el:
        result.append(flatten(sel))
        result.append(sel.tail or "")
    return "".join(result)

url='http://www.iwight.com/contracts/'


def parseContractPage(page,typ):
    print page
    root = lxml.html.fromstring(page)
    table=root.xpath('//table[@id="dgSearchResults"]')[0]
    for row in table.xpath('tr')[1:]:
        print 'contracts',flatten(row)
        print row.xpath('td/a/@onclick')[0],row.xpath('td/a')[0].text,row.xpath('td')[1].text,row.xpath('td')[2].text
        data={}
        data['id']=row.xpath('td/a/@onclick')[0].replace("window.open('",'').replace("')",'').strip(';')
        data['name']=row.xpath('td/a')[0].text
        data['amount']=row.xpath('td')[1].text
        data['date']=row.xpath('td')[2].text
        data['typ']=typ

        scraperwiki.sqlite.save(unique_keys=['id'], table_name='contractList', data=data)

scrape=0
if scrape==1:
    br = mechanize.Browser()
    
    response = br.open(url)
    print response.read()
    
    #for form in br.forms():
        #print "Form name:", form.name
        #print form
    
    br.form = list(br.forms())[0]
    
    for control in br.form.controls:
        #print control.name
        if control.type == "select" and control.name=='ddlCat':  # means it's class ClientForm.SelectControl
            for item in control.items[1:]:
                print " name=%s values=%s" % (item.name, str([label.text  for label in item.get_labels()]))
                label=[label.text  for label in item.get_labels()][0]
                br['ddlCat'] = [ item.name ]
                response2 = br.submit()
                #print response.read()
                parseContractPage(response2.read(),label)
                br.back()
                br.form = list(br.forms())[0]

#Get contract
q = '* FROM `contractList`'
data = scraperwiki.sqlite.select(q)

headings=['Contract Title', 'Selection Method','Framework','Type of Contract','Category of Spend','Contract Start','Contract End', 'End date of extension', 'Annual value', 'Total Contract Value','Currency','Title','Name']

#scraperwiki.sqlite.execute('drop table "contractDetails"')

#----ish via http://stackoverflow.com/a/379966/454773
def num (s):
    s=s.replace(',','')
    try:
        return int(s)
    except:
        return float(s)
#----

for item in data:
    curl=url+item['id']
    data={'id':item['id']}
    html = scraperwiki.scrape(curl)
    print html
    root = lxml.html.fromstring(html)
    rows=root.xpath('//tr')
    for row in rows:
        cells=row.xpath('td')
        #print cells
        if len(cells) >1 and cells[1].text!=None:
            if cells[1].text.strip() in headings:
                if cells[2]!=None:
                    #print cells[1].text.strip(),':-:', flatten(cells[2])
                    data[cells[1].text.strip()] = flatten(cells[2])
                else:
                    #print cells[1].text.strip()
                    data[cells[1].text.strip()]=''
            elif cells[1].text.strip()=='Option to extend':
                #print 'Option to extend',cells[2].xpath('table/tr/td/input[@checked="checked"]/../label')[0].text
                data['Option to extend']=cells[2].xpath('table/tr/td/input[@checked="checked"]/../label')[0].text
    numtidy=['Annual value', 'Total Contract Value']
    for tidy in numtidy:
        data[tidy]=num(data[tidy]) 
    #Also consider properly date-ifying dates?
    scraperwiki.sqlite.save(unique_keys=['id'], table_name='contractDetails', data=data)

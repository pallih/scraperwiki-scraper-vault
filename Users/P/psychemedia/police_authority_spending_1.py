import scraperwiki,csv,urllib,re,simplejson

#Full list of police authorities here: http://www.apa.police.uk/your-police-authority/contact-information
#Please feel freee to use this scraper to scrape data from other authorities into additional tables:-)

def hampshire():
    #some of the files are a mss... this is just a quick first pass
    files=['march-2012-csv.csv','february-2012.csv','january-2012.csv','december-2011.csv','november-2011.csv','october-2011.csv', 'september-2011.csv','august-2011.csv','july-2011.csv','january-2011-csv.csv']
    companies={}
    for f in files:
        url='http://www.hants.gov.uk/'+f
        nReader = csv.reader(urllib.urlopen(url))
        keys=[]
        for nrow in nReader:
            for i in nrow:
                keys.append(i.strip())
            if 'Category' in keys: break
            else: keys=[]
        keys=['Body Name', 'Supplier Name', 'Category', 'Transaction Reference', 'Date Paid', 'Gross Amount', 'Period', 'Accounting Year','Gross Amount Parsed']
        for nrow in nReader:
            datarow={}
            try:
                start= nrow.index('Hampshire Constabulary')
            except: continue
            ix=0
            for item in nrow[start:9]:
                item=item.strip()
                '''
                if ix==1:
                    cname=''
                    cid=''
                    if item not in companies:
                        rurl='http://opencorporates.com/reconcile/gb?query='+urllib.quote(item)
                        json=simplejson.load(urllib.urlopen(rurl))
                        if len(json['result'])>0:
                            companies[item]=(json['result'][0]['id'],json['result'][0]['name'])
                            cname=json['result'][0]['name']
                            cid=json['result'][0]['id']
                        else: companies[item]=''
                    else:
                        if companies[item]!='': cid,cname=companies[item]
                    datarow['ocName Guess']=cname
                    datarow['ocID Guess']=cid
                '''
                if ix==5:
                    r=re.match(r"\((.*)\)$",item)
                    if r!=None: datarow['Gross Amount Parsed']='-'+r.group(1).strip()
                    else: datarow['Gross Amount Parsed']=item
                    datarow['Gross Amount Parsed']=datarow['Gross Amount Parsed'].replace(',','')
                datarow[keys[ix]]=item
                ix=ix+1
            scraperwiki.sqlite.save(unique_keys=[], table_name='hampshire_police', data=datarow)

scraperwiki.sqlite.execute('drop table "hampshire_police"')
hampshire()import scraperwiki,csv,urllib,re,simplejson

#Full list of police authorities here: http://www.apa.police.uk/your-police-authority/contact-information
#Please feel freee to use this scraper to scrape data from other authorities into additional tables:-)

def hampshire():
    #some of the files are a mss... this is just a quick first pass
    files=['march-2012-csv.csv','february-2012.csv','january-2012.csv','december-2011.csv','november-2011.csv','october-2011.csv', 'september-2011.csv','august-2011.csv','july-2011.csv','january-2011-csv.csv']
    companies={}
    for f in files:
        url='http://www.hants.gov.uk/'+f
        nReader = csv.reader(urllib.urlopen(url))
        keys=[]
        for nrow in nReader:
            for i in nrow:
                keys.append(i.strip())
            if 'Category' in keys: break
            else: keys=[]
        keys=['Body Name', 'Supplier Name', 'Category', 'Transaction Reference', 'Date Paid', 'Gross Amount', 'Period', 'Accounting Year','Gross Amount Parsed']
        for nrow in nReader:
            datarow={}
            try:
                start= nrow.index('Hampshire Constabulary')
            except: continue
            ix=0
            for item in nrow[start:9]:
                item=item.strip()
                '''
                if ix==1:
                    cname=''
                    cid=''
                    if item not in companies:
                        rurl='http://opencorporates.com/reconcile/gb?query='+urllib.quote(item)
                        json=simplejson.load(urllib.urlopen(rurl))
                        if len(json['result'])>0:
                            companies[item]=(json['result'][0]['id'],json['result'][0]['name'])
                            cname=json['result'][0]['name']
                            cid=json['result'][0]['id']
                        else: companies[item]=''
                    else:
                        if companies[item]!='': cid,cname=companies[item]
                    datarow['ocName Guess']=cname
                    datarow['ocID Guess']=cid
                '''
                if ix==5:
                    r=re.match(r"\((.*)\)$",item)
                    if r!=None: datarow['Gross Amount Parsed']='-'+r.group(1).strip()
                    else: datarow['Gross Amount Parsed']=item
                    datarow['Gross Amount Parsed']=datarow['Gross Amount Parsed'].replace(',','')
                datarow[keys[ix]]=item
                ix=ix+1
            scraperwiki.sqlite.save(unique_keys=[], table_name='hampshire_police', data=datarow)

scraperwiki.sqlite.execute('drop table "hampshire_police"')
hampshire()
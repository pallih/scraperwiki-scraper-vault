import scraperwiki
import lxml.html
import re

scraperwiki.sqlite.attach("londongazette_html")


scraperwiki.sqlite.execute("DROP TABLE IF EXISTS notices4")
scraperwiki.sqlite.execute("CREATE TABLE `notices4` (`id` integer,`sourceurl` text, `notice_code` text,`publication_date` text,   `app_type` text,   `applicant` text,  `description` text, `related_licence` text, `full_text` text)")
scraperwiki.sqlite.commit()

linklist=[]
record={}
linklist = scraperwiki.sqlite.select("* from londongazette_html.swdata")


for l in linklist:
    record['id']=l['id']
    record['sourceurl']=l['sourceurl']


#collect date
    data=l['data']
    if  'datatype="xsd:date" content="' in data: publication_date=data.partition('datatype="xsd:date" content="')[2].partition('">')[0]
    record['publication_date'] = publication_date

#collect notice type (for filtering out non-abstraction - anything other than 1901 is suspicious)
    data=l['data']
    if  'property="g:hasNoticeCode" datatype="xsd:string">' in data: notice_code=data.partition('property="g:hasNoticeCode" datatype="xsd:string">')[2].partition('</')[0]
    record['notice_code'] = notice_code

#save full text
    data=l['data']
    data=data.replace('\n',' ').replace('\r',' ').replace('&#160;',' ').replace('  ',' ').replace('   ',' ').replace('  ',' ').replace('  ',' ').replace('&amp;','&')
    #text=data.replace('\n',' ').replace('\r',' ').replace('  ',' ').replace('   ',' ').replace('  ',' ').replace('  ',' ').replace('&amp;','&')
    record['full_text'] =lxml.html.fromstring(data).text_content()
   
#filter out EA updates
    if 'Environment Agency in pursuance of section ' in  l['data'] or 'Environment Agency, in pursuance of section ' in  l['data']:
         data1= '-- EA change --'   
#remove beginning text
    elif  'Take notice that' in data: data1=data.partition('Take notice that')[2]
    elif  'Take note that' in data: data1=data.partition('Take note that')[2]
    elif  'Notice is hereby given that' in data: data1=data.partition('Notice is hereby given that')[2]
    elif  'an application is being made to the Environment Agency' in data: data1=data.partition('an application is being made to the Environment Agency')[2]
    else:
        RE = re.compile("(NOTICE OF APPLICATION|Application for Licence to abstract water|NOTIFICATION OF APPLICATION TO VARY A LICENCE TO ABSTRACT WATER|Notice that)", re.I | re.DOTALL)
        r= RE.search(data)
        if (r!= None): data1=data[r.end():]
        else: data1=data

#remove ending text
    RE = re.compile('(<p>\(<span property="g:hasNoticeNumber|<br><span|<br>on behalf of)', re.I)
    r=RE.search(data1)
    if (r != None): data2=data1[:r.start()]
    else: 
        data2=data1
        print data1
        #if '</div>' in data1:
        #    data2=data1.partition('</div>')[0]
        #else: data2=data1 #print '--- Could not trim end ---' + data
# ---------------------------------------------------------------------------------    UNcomment following line, to keep breaking down description...
    #record['data']=data2
#find name
    RE = re.compile("(are|is)[ \n\r]*(applying)", re.I)
    r=RE.search(data2)
    if (r != None): applicant=data2[:r.start()]
    else:
        if ' by ' in data2 and ' to ' in data2:
            applicant=data2.partition(' by ')[2].partition('to')[0]
            applicant=lxml.html.fromstring(applicant).text_content()
        else: applicant=None
    record['applicant']=applicant

#find application description (volumes, locations etc)
    #find the begining
    RE = re.compile("(vary [a |the |abstraction ]*licence[s]*)", re.I)
    r=RE.search(data2)
    if (r != None):
        data3=data2[r.end():]
        record['app_type']='variation'
        #get licence number.

        #find string after 'serial number'
        RE = re.compile("((serial)* (number|No)[s]*)", re.I)
        r=RE.search(data3)
        if (r != None):
            next=data3[r.end():].strip().strip('.').strip()
            #find the first word, with no numbers, which ends with a space
            RE = re.compile("([a-z]{2,100})\s", re.I)
            r1=RE.search(next)
            if r1 != None:
                record['related_licence']= next[:r1.start()].strip(', (').strip()
        else: record['related_licence']=None

    elif 'abstract water from' in data2:
        data3=data2.partition('abstract water from')[2]
        record['app_type']='abstraction'
        record['related_licence']=None
    else:
        RE = re.compile("(licence[s]* to abst[r]*act)|(which authorises [the ]*abstraction)", re.I)
        r=RE.search(data2)
        if (r != None):
            data3=data2[r.end():]
            record['app_type']=None
        else : print 'ERROR cannot match beggining of abstraction description'
        record['related_licence']=None
    
    #find the end
    if data3 !=None:
        RE = re.compile("(((A copy|Copies) of [theais]* appl[ic]*a[t]*ion)|(A copy of this notice))", re.I)
        r=RE.search(data3)
        if (r != None):
            data3=data3[:r.start()]
            data3=lxml.html.fromstring(data3).text_content()
        else : 
            print 'ERROR cannot match end of abstraction description'
            data3=None
    record['description']=data3


    if data3 != None:
# ------   get grid references  ------
        gridRE1 = re.compile("\s((?:[nsth]{1})(?:[a-z]{1})\s*(?:[0-9\s\./-]{4,20}))", re.I | re.DOTALL)
        iterator = gridRE1.finditer(data3)
        grid=''
        if (iterator != None):
            for m in iterator:
                if 'No' in m.group() or 'no' in m.group() : pass
                elif 'to' in m.group() : pass
                #in future version remember to check if the iterator isnt already in the list (if m.group() in grid: pass)
                elif m.group() in grid: pass
                else: grid=grid+ m.group()+', '
            #print grid
            record['n_gridref']=grid
        else: record['n_gridref']=None


# ------   get postcodes  ------

        postRE1 = re.compile("((?:GIR &0AA)|(?:(?:(?:[A-PR-UWYZ][A-HK-Y]?[0-9][0-9]?)|(?:(?:[A-PR-UWYZ][0-9][A-HJKSTUW])|(?:[A-PR-UWYZ][A-HK-Y][0-9][ABEHMNPRV-Y]))) *[0-9][ABD-HJLNP-UW-Z]{2}))", re.I)
        match = postRE1.findall(data3)
        if (match != None):
             record['n_postcode']=', '.join(match)
        else: record['n_postcode']=None

    else: 
        record['n_gridref']=None
        record['n_postcode']=None


    scraperwiki.sqlite.save(['id'], record, 'notices4')


scraperwiki.sqlite.execute("UPDATE `notices4` set app_type=NULL where app_type=''")
scraperwiki.sqlite.execute("UPDATE `notices4` set related_licence=NULL where related_licence=''")
scraperwiki.sqlite.execute("UPDATE `notices4` set description=NULL where description=''")
scraperwiki.sqlite.execute("UPDATE `notices4` set n_gridref=NULL where n_gridref=''")
scraperwiki.sqlite.execute("UPDATE `notices4` set n_postcode=NULL where n_postcode=''")
scraperwiki.sqlite.commit()

import scraperwiki
import lxml.html
import re

scraperwiki.sqlite.attach("londongazette_html")


scraperwiki.sqlite.execute("DROP TABLE IF EXISTS notices4")
scraperwiki.sqlite.execute("CREATE TABLE `notices4` (`id` integer,`sourceurl` text, `notice_code` text,`publication_date` text,   `app_type` text,   `applicant` text,  `description` text, `related_licence` text, `full_text` text)")
scraperwiki.sqlite.commit()

linklist=[]
record={}
linklist = scraperwiki.sqlite.select("* from londongazette_html.swdata")


for l in linklist:
    record['id']=l['id']
    record['sourceurl']=l['sourceurl']


#collect date
    data=l['data']
    if  'datatype="xsd:date" content="' in data: publication_date=data.partition('datatype="xsd:date" content="')[2].partition('">')[0]
    record['publication_date'] = publication_date

#collect notice type (for filtering out non-abstraction - anything other than 1901 is suspicious)
    data=l['data']
    if  'property="g:hasNoticeCode" datatype="xsd:string">' in data: notice_code=data.partition('property="g:hasNoticeCode" datatype="xsd:string">')[2].partition('</')[0]
    record['notice_code'] = notice_code

#save full text
    data=l['data']
    data=data.replace('\n',' ').replace('\r',' ').replace('&#160;',' ').replace('  ',' ').replace('   ',' ').replace('  ',' ').replace('  ',' ').replace('&amp;','&')
    #text=data.replace('\n',' ').replace('\r',' ').replace('  ',' ').replace('   ',' ').replace('  ',' ').replace('  ',' ').replace('&amp;','&')
    record['full_text'] =lxml.html.fromstring(data).text_content()
   
#filter out EA updates
    if 'Environment Agency in pursuance of section ' in  l['data'] or 'Environment Agency, in pursuance of section ' in  l['data']:
         data1= '-- EA change --'   
#remove beginning text
    elif  'Take notice that' in data: data1=data.partition('Take notice that')[2]
    elif  'Take note that' in data: data1=data.partition('Take note that')[2]
    elif  'Notice is hereby given that' in data: data1=data.partition('Notice is hereby given that')[2]
    elif  'an application is being made to the Environment Agency' in data: data1=data.partition('an application is being made to the Environment Agency')[2]
    else:
        RE = re.compile("(NOTICE OF APPLICATION|Application for Licence to abstract water|NOTIFICATION OF APPLICATION TO VARY A LICENCE TO ABSTRACT WATER|Notice that)", re.I | re.DOTALL)
        r= RE.search(data)
        if (r!= None): data1=data[r.end():]
        else: data1=data

#remove ending text
    RE = re.compile('(<p>\(<span property="g:hasNoticeNumber|<br><span|<br>on behalf of)', re.I)
    r=RE.search(data1)
    if (r != None): data2=data1[:r.start()]
    else: 
        data2=data1
        print data1
        #if '</div>' in data1:
        #    data2=data1.partition('</div>')[0]
        #else: data2=data1 #print '--- Could not trim end ---' + data
# ---------------------------------------------------------------------------------    UNcomment following line, to keep breaking down description...
    #record['data']=data2
#find name
    RE = re.compile("(are|is)[ \n\r]*(applying)", re.I)
    r=RE.search(data2)
    if (r != None): applicant=data2[:r.start()]
    else:
        if ' by ' in data2 and ' to ' in data2:
            applicant=data2.partition(' by ')[2].partition('to')[0]
            applicant=lxml.html.fromstring(applicant).text_content()
        else: applicant=None
    record['applicant']=applicant

#find application description (volumes, locations etc)
    #find the begining
    RE = re.compile("(vary [a |the |abstraction ]*licence[s]*)", re.I)
    r=RE.search(data2)
    if (r != None):
        data3=data2[r.end():]
        record['app_type']='variation'
        #get licence number.

        #find string after 'serial number'
        RE = re.compile("((serial)* (number|No)[s]*)", re.I)
        r=RE.search(data3)
        if (r != None):
            next=data3[r.end():].strip().strip('.').strip()
            #find the first word, with no numbers, which ends with a space
            RE = re.compile("([a-z]{2,100})\s", re.I)
            r1=RE.search(next)
            if r1 != None:
                record['related_licence']= next[:r1.start()].strip(', (').strip()
        else: record['related_licence']=None

    elif 'abstract water from' in data2:
        data3=data2.partition('abstract water from')[2]
        record['app_type']='abstraction'
        record['related_licence']=None
    else:
        RE = re.compile("(licence[s]* to abst[r]*act)|(which authorises [the ]*abstraction)", re.I)
        r=RE.search(data2)
        if (r != None):
            data3=data2[r.end():]
            record['app_type']=None
        else : print 'ERROR cannot match beggining of abstraction description'
        record['related_licence']=None
    
    #find the end
    if data3 !=None:
        RE = re.compile("(((A copy|Copies) of [theais]* appl[ic]*a[t]*ion)|(A copy of this notice))", re.I)
        r=RE.search(data3)
        if (r != None):
            data3=data3[:r.start()]
            data3=lxml.html.fromstring(data3).text_content()
        else : 
            print 'ERROR cannot match end of abstraction description'
            data3=None
    record['description']=data3


    if data3 != None:
# ------   get grid references  ------
        gridRE1 = re.compile("\s((?:[nsth]{1})(?:[a-z]{1})\s*(?:[0-9\s\./-]{4,20}))", re.I | re.DOTALL)
        iterator = gridRE1.finditer(data3)
        grid=''
        if (iterator != None):
            for m in iterator:
                if 'No' in m.group() or 'no' in m.group() : pass
                elif 'to' in m.group() : pass
                #in future version remember to check if the iterator isnt already in the list (if m.group() in grid: pass)
                elif m.group() in grid: pass
                else: grid=grid+ m.group()+', '
            #print grid
            record['n_gridref']=grid
        else: record['n_gridref']=None


# ------   get postcodes  ------

        postRE1 = re.compile("((?:GIR &0AA)|(?:(?:(?:[A-PR-UWYZ][A-HK-Y]?[0-9][0-9]?)|(?:(?:[A-PR-UWYZ][0-9][A-HJKSTUW])|(?:[A-PR-UWYZ][A-HK-Y][0-9][ABEHMNPRV-Y]))) *[0-9][ABD-HJLNP-UW-Z]{2}))", re.I)
        match = postRE1.findall(data3)
        if (match != None):
             record['n_postcode']=', '.join(match)
        else: record['n_postcode']=None

    else: 
        record['n_gridref']=None
        record['n_postcode']=None


    scraperwiki.sqlite.save(['id'], record, 'notices4')


scraperwiki.sqlite.execute("UPDATE `notices4` set app_type=NULL where app_type=''")
scraperwiki.sqlite.execute("UPDATE `notices4` set related_licence=NULL where related_licence=''")
scraperwiki.sqlite.execute("UPDATE `notices4` set description=NULL where description=''")
scraperwiki.sqlite.execute("UPDATE `notices4` set n_gridref=NULL where n_gridref=''")
scraperwiki.sqlite.execute("UPDATE `notices4` set n_postcode=NULL where n_postcode=''")
scraperwiki.sqlite.commit()


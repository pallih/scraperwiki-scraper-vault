
# -*- coding: utf8 -*-

import scraperwiki
import lxml.html
import re
import dateutil.parser
import datetime
import decimal



# Scrape EA Impoundment License Applications
#
    # Notices of Licence Applications to Abstract or Impound water (index)
    # http://www.environment-agency.gov.uk/research/library/consultations/65549.aspx
#
# Applications for full licences to abstract or impound water *
# http://www.environment-agency.gov.uk/research/library/consultations/65560.aspx
#
# Applications to vary or revoke existing licences to abstract or impound water
# http://www.environment-agency.gov.uk/research/library/consultations/65558.aspx
#
    # Licensing Decision Statements
    # http://www.environment-agency.gov.uk/research/library/consultations/65551.aspx


#scraperwiki.sqlite.execute("DROP TABLE IF EXISTS licence_applications")
#scraperwiki.sqlite.execute("DROP TABLE IF EXISTS swvariables")
#scraperwiki.sqlite.execute("DROP TABLE IF EXISTS log")
#scraperwiki.sqlite.commit()

#scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS licence_applications (app_ID INT, url text, scrape_date text, notice_type text, notice_desc text, full_text text, applicant_name text, closing_date text, app_desc text, site_location text, site_location_NGR text, quantity_long text,quantity_hour text, abs_max_daily_qty text,  abs_max_annual_qty text, abs_ave_daily_qty text, quantity_seasonal text, use_long text, new_yn INT, hydroelectric text)")
#scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `log` ( `scrape_id` real, `scrape_date` text, `task` text, `url` text, `result` text,`warnings` text)")
#scraperwiki.sqlite.commit()

now = str(datetime.datetime.now())[:19]
warning=''
if scraperwiki.sqlite.get_var('last_page')==None:
    scraperwiki.sqlite.save_var('last_page', 1)
else : scraperwiki.sqlite.save_var('last_page',scraperwiki.sqlite.get_var('last_page')+1)

scrape_id=scraperwiki.sqlite.get_var('last_page')

def parseNewApplications(url):
    html = scraperwiki.scrape(url)
    html = html.decode("utf8")
    apps = lxml.html.fromstring(html)
    new_cnt=0
    total_cnt=0
    global warning
    global scrape_id
    warning=''
    for app in apps.cssselect("ul[id='highlights'] li"):
        try:
            appAnchor = safeXPath(app.cssselect("a"), 0)
            appHref = safeXPath(appAnchor.xpath("@href"), 0)
            app_ID = appHref.partition('consultations/')[2].partition('.aspx')[0]
            #appTitle = safeXPath(appAnchor.xpath("@title"), 0)
            #appPara = safeXPath(app.cssselect("p"), 0)
            #appDescr = safeXPath(appPara.xpath("text()"), 0)            

            if scraperwiki.sqlite.select("* from licence_applications WHERE app_ID="+str(app_ID)) == []:
                new_yn=1
                new_cnt=new_cnt+1
            else: new_yn=0

            parseAppDetail(app_ID, baseURL+appHref, new_yn)
            total_cnt=total_cnt+1
        except IndexError as ex:
            print "parseNewApplications: ex={1}: url={0} app={2}".format(url, str(ex), app)
            warning='Could not parse page'
#save log
    scrape_id=scraperwiki.sqlite.get_var('last_page')
    log_entry= {"scrape_id":scrape_id , "scrape_date":now, "task":'parse list', "url":url, "result":str(new_cnt) + ' New records / ' + str(total_cnt) + ' Total records', "warnings":warning}
    scraperwiki.sqlite.save(['scrape_id'],log_entry,'log')

def safeXPath(xpath, index):
    global warning
    try :
        return xpath[index];
    except IndexError as ex:
        print "safeXpath: ex={2}: xpath={0} index={1}".format(xpath, index, str(ex))
        warning='Could not parse page'
    return ""

appSiteLocation=''

def parseAppDetail(app_ID, appUrl, new_yn):
    global warning
    global t
    t=''
    global scrape_id
    warning=''
    global appSiteLocation
    appClosingDate = None;
    appPlaceName = None
    appAddress = None;
    scrape_id=scrape_id+0.01

    if new_yn==1:
    
        #appIdRE = re.compile(".*/(\d+)\.aspx$", re.I)
        #match = appIdRE.match(appUrl)
        #if (match == None):
        #    print "NO MATCH for ID in",appUrl
        #    return
        #app_ID = match.group(1)
    
        #today = datetime.date.today()
        record= {"app_ID":app_ID, "scrape_date":now, "url":appUrl, "new_yn":new_yn}
    
        html = scraperwiki.scrape(appUrl)
        html1 = html.decode("utf8")
        #clean up the html, to get rid of lists
        #print html
        html = re.sub("<ul>","",html)
        html = re.sub("<\ul>","",html)
        html = re.sub("<li>","<p>",html)
        html = re.sub("</li>","</p>",html)
        #print html
        parsed = lxml.html.fromstring(html)
    
    #get name of applicant
        applicant = parsed.cssselect("h1")[0].text
        record["applicant_name"] = applicant
    
        content = parsed.cssselect("div[id='content']")
        contentText = content[0].text_content()
    
    
    #check if hydroelectric
        if (re.search("(hydropower|hydro.*electric)", contentText, re.I) != None):
            record["hydroelectric"] = True
    
    
        intro = content[0].cssselect("p[class='intro']")
        introText = intro[0].text_content()
        introRE = re.compile("Closin. date.*:\s*(\d{1,2}\s+\w+\s+\d{2,4})\.+\s+(.*)", re.I)
    
                #Closin. date.*:\s*(\d{1,2}\s+\w+\s+\d{2,4})\.+\s+(.*)\s+(at|between)
                #start with closing date then anything, untill a ':'. then any non whitespace character (\s) for as many times as it wants (*)
                    # then start the first group '(' any decimal digit (1 or 2) then some chracters and then digits again (2-4). finish first group ')'
                    # then a full stop and ONE non whitespace character \.+\s+
                    #then collect the scond group up untill a (at|between) appears = group 3
                    #then collect the reminder of string as group 4
        match = introRE.match(introText)

        if (match == None):
            print "NO MATCH! line=",introText
            warning=warning+' ; '+'Could not break down Intro text : '+introText
        else:
            if (match.group(1) != None):
                appClosingDate = dateutil.parser.parse( match.group(1) )
                record["closing_date"] = appClosingDate.date()
        
            if (match.group(2) != None):
                a=match.group(2)
                if ' at ' in a:
                    appDesc = a.partition(' at ')[0]
                    appSiteLocation = a.partition(' at ')[2]
                elif ' between ' in a :
                    appDesc = a.partition(' between ')[0]
                    appSiteLocation = a.partition(' between ')[2]
                else :
                    appDesc = a
                    appSiteLocation=''
                record["app_desc"] = appDesc
                record["site_location"] = appSiteLocation
    #
    
    #get full text description
     #extract notice type    
        plain_text_ps = content[0].cssselect("div.plain_text p")
        notice_desc= plain_text_ps[0].text_content().replace('\r',' ').replace('\n',' ').upper().partition('NOTICE')[1]+plain_text_ps[0].text_content().replace('\r',' ').replace('\n',' ').upper().partition('NOTICE')[2].partition('</')[0]
        notice_desc=notice_desc.strip(' .')
        notice_type=''
        if notice_desc=='NOTICE OF APPLICATION FOR A FULL LICENCE TO ABSTRACT WATER' : notice_type='Abstract'
        elif notice_desc=='NOTICE OF APPLICATION FOR A FULL LICENCE TO ABSTRACT WATER AND FOR A LICENCE TO OBSTRUCT OR IMPEDE THE FLOW OF AN INLAND WATER BY MEANS OF IMPOUNDING WORKS' : notice_type='Abstract & Impede'
        elif notice_desc=='NOTICE OF APPLICATION FOR A LICENCE TO OBSTRUCT OR IMPEDE THE FLOW OF AN INLAND WATER BY MEANS OF IMPOUNDING WORKS' : notice_type='Impede'
        elif notice_desc=='NOTICE OF APPLICATION TO VARY A FULL LICENCE TO ABSTRACT WATER' : notice_type='Change'
        elif 'NOTICE OF APPLICATION FOR A TRANSFER LICENCE' in notice_desc : notice_type='Transfer'
        else :
            print record["app_ID"] + ' ---- NON_STANDARD notice type ---- ' + notice_desc
            warning=warning+' ; '+ 'NON_STANDARD notice type : '+ notice_desc
        
        record["notice_desc"] = notice_desc
        record["notice_type"] = notice_type

#extract all text below applicant name
        text=''
        atext=''
        trigger=0
        for p in plain_text_ps:
            if 'A copy of the applicatio' in p.text_content():
                text=text + ' ' + p.text_content().replace('\r',' ').replace('\n',' ').partition('A copy of the applicatio')[0]
                break
            if trigger==1:
                text=text + ' ' + p.text_content().replace('\r',' ').replace('\n',' ')
            if 'an application has been made to the Environment Agency' in p.text_content():
                trigger=1
            atext=atext + ' ' + p.text_content().replace('\r',' ').replace('\n',' ')
        #in case the full text ends up empty
        if text==' ': text=atext
        record["full_text"] = text

    #remove weird characters
        text=text.replace(u'…', '')
        text=text.replace(u'•', '')
        text=text.replace(u'\xa0', ' ')
            
     #get quantities & use
        if 'following rates and periods' in text:
            if 'The water' in text.partition('following rates and periods')[2]:
                t=text.partition('following rates and periods')[2].partition('The water')[0]
                t=t.strip(' :.').strip()
                record["quantity_long"] =t
                record["use_long"] =text.partition('following rates and periods')[2].partition('The water')[1]+text.partition('following rates and periods')[2].partition('The water')[2]
            else:
                t=text.partition('following rates and periods')[2]
                t=t.strip(' :.').strip()
                record["quantity_long"] =t
        elif 'Quantities to be abstracted' in text:
                t=text.partition('Quantities to be abstracted')[2]
                t=t.strip(' :.').strip()
                record["quantity_long"] =t
    
    
    #break down volumes
        if t != None:
            t=t.replace('\r\n',' ')
            volumeRE = re.compile("([0-9.,\s]+)cubic metres an hour[,;\s\n]*([0-9., ]+)\s*cubic metres a day[;]* and[\s\n]*([0-9., ]+)\s*cubic metres a year(.*)", re.I | re.DOTALL)
            match = volumeRE.match(t)
            if (match == None):
                print record["app_ID"] + " --- Could not break down volume! --- line=",t
                warning=warning+' ; '+'Could not break down volume : '+t
    
            else:
                if (match.group(1) != None):
                    record["quantity_hour"] = decimal.Decimal(match.group(1).strip().replace(',','').replace(' ','').strip('.'))
        
                if (match.group(2) != None):
                    record["abs_max_daily_qty"] = decimal.Decimal(match.group(2).strip().replace(',','').replace(' ','').strip('.'))
        
                if (match.group(3) != None):
                    record["abs_max_annual_qty"] =decimal.Decimal(match.group(3).strip().replace(',','').replace(' ','').strip('.'))
                    record["abs_ave_daily_qty"]=round(decimal.Decimal(match.group(3).strip().replace(',','').replace(' ','').strip('.'))/365,2)
        
                if (match.group(4) != None):
                    record["quantity_seasonal"] = match.group(4)
    
    #try to get out a licence serial number
        if 'serial number' in text:
            RE = re.compile("serial number ([0-9/\*a-zA-Z]*)", re.I)
            f=RE.findall(text)
            if (f== None):
                print "serial number : NO MATCH! line=",text
                warning=warning+' ; '+ "Could not extract licence serial number. : line="+text
            else:        
                a=' ; '.join(f)
                record["related_licence"] = a
    #get national grid ref
    
        if 'National Grid Reference' in appSiteLocation or 'NGR' in appSiteLocation:
            if 'NGR' in appSiteLocation:
                n=appSiteLocation.partition('NGR')[2]
            elif 'National Grid Reference' in appSiteLocation:
                n=appSiteLocation.partition('National Grid Reference')[2]
            else:n=''
            n=n.replace('(','').replace(')','').strip().strip(' :,.').strip()
            record["site_location_NGR"] = n
        else: record["site_location_NGR"] = ''
#save or update
    if new_yn==1:
        scraperwiki.sqlite.save(unique_keys = ["app_ID"],
                                data = record,
                                table_name = "licence_applications",
                                verbose = 2)
        log_entry= {"scrape_id":scrape_id , "scrape_date":now, "task":'parse page', "url":appUrl, "result":'new record. ID: '+str(app_ID), "warnings":warning}
        scraperwiki.sqlite.save(['scrape_id'], log_entry,'log')

    elif new_yn==0:
        log_entry= {"scrape_id":scrape_id , "scrape_date":now, "task":'parse page', "url":appUrl, "result":'existing record. ID: '+str(app_ID), "warnings":warning}
        scraperwiki.sqlite.save(['scrape_id'], log_entry,'log')
    else:
        log_entry= {"scrape_id":scrape_id , "scrape_date":now, "task":'parse page', "url":appUrl, "result":'-- ERROR -- Neither New nor updated (?)'}
        scraperwiki.sqlite.save(['scrape_id'], log_entry,'log')
    


baseURL = "http://www.environment-agency.gov.uk"
parseNewApplications(baseURL+"/research/library/consultations/65560.aspx")

# Twitter observatory - anniversary module
# Author: @jackottaviani for RadioRadicale.it and FaiNotizia.it (Italy)

import scraperwiki
import xlrd 
from time import gmtime, strftime
import random
import datetime

hashtag = 'via @Fai_Notizia #DetenutoIgnoto'

now = datetime.datetime.now()

scraperwiki.sqlite.attach("ristretti", "ristretti")

# take current time compatible to RSS2 pubDate format
current_date = strftime("%a, %d %m %Y %H:%M:%S +0000", gmtime())


#Generatore di anniversari, momentaneamente disattivo
def gen_anniversary():

    # if exists anniversary...
    if len(str(now.day)) == 1:
        today = '0'+str(now.day)
    else: 
        today = str(now.day)

    if len(str(now.month)) == 1:
        month = '0'+str(now.month)
    else: 
        month = str(now.month)
    
    q = "titolo_xml, data_decesso FROM ristretti.decessi_per_istituto WHERE substr(data_decesso,1,2) IS '%s' AND substr(data_decesso,4,2) IS '%s' AND substr(data_decesso,length(data_decesso),7) IS NOT '%s'" % (today, month, str(now.year))

    anniversaries = scraperwiki.sqlite.select(q)

    if (len(anniversaries) > 0): 
        anniversary = random.choice(anniversaries)

        diff_years = int (now.year) - int (anniversary["data_decesso"][-4:])

        return str(diff_years) +' anni fa, '+ anniversary["titolo_xml"].replace("muore","moriva")
    else: return '-1'
        
    


stat = {}
stats_entry = gen_anniversary()
if (stats_entry != -1):
    stat["titolo_xml"] = stats_entry
    stat["current_date"] = current_date
    scraperwiki.sqlite.save(["titolo_xml", "current_date"], stat, table_name="ann_table", verbose=2)
    
# Twitter observatory - anniversary module
# Author: @jackottaviani for RadioRadicale.it and FaiNotizia.it (Italy)

import scraperwiki
import xlrd 
from time import gmtime, strftime
import random
import datetime

hashtag = 'via @Fai_Notizia #DetenutoIgnoto'

now = datetime.datetime.now()

scraperwiki.sqlite.attach("ristretti", "ristretti")

# take current time compatible to RSS2 pubDate format
current_date = strftime("%a, %d %m %Y %H:%M:%S +0000", gmtime())


#Generatore di anniversari, momentaneamente disattivo
def gen_anniversary():

    # if exists anniversary...
    if len(str(now.day)) == 1:
        today = '0'+str(now.day)
    else: 
        today = str(now.day)

    if len(str(now.month)) == 1:
        month = '0'+str(now.month)
    else: 
        month = str(now.month)
    
    q = "titolo_xml, data_decesso FROM ristretti.decessi_per_istituto WHERE substr(data_decesso,1,2) IS '%s' AND substr(data_decesso,4,2) IS '%s' AND substr(data_decesso,length(data_decesso),7) IS NOT '%s'" % (today, month, str(now.year))

    anniversaries = scraperwiki.sqlite.select(q)

    if (len(anniversaries) > 0): 
        anniversary = random.choice(anniversaries)

        diff_years = int (now.year) - int (anniversary["data_decesso"][-4:])

        return str(diff_years) +' anni fa, '+ anniversary["titolo_xml"].replace("muore","moriva")
    else: return '-1'
        
    


stat = {}
stats_entry = gen_anniversary()
if (stats_entry != -1):
    stat["titolo_xml"] = stats_entry
    stat["current_date"] = current_date
    scraperwiki.sqlite.save(["titolo_xml", "current_date"], stat, table_name="ann_table", verbose=2)
    
# Twitter observatory - anniversary module
# Author: @jackottaviani for RadioRadicale.it and FaiNotizia.it (Italy)

import scraperwiki
import xlrd 
from time import gmtime, strftime
import random
import datetime

hashtag = 'via @Fai_Notizia #DetenutoIgnoto'

now = datetime.datetime.now()

scraperwiki.sqlite.attach("ristretti", "ristretti")

# take current time compatible to RSS2 pubDate format
current_date = strftime("%a, %d %m %Y %H:%M:%S +0000", gmtime())


#Generatore di anniversari, momentaneamente disattivo
def gen_anniversary():

    # if exists anniversary...
    if len(str(now.day)) == 1:
        today = '0'+str(now.day)
    else: 
        today = str(now.day)

    if len(str(now.month)) == 1:
        month = '0'+str(now.month)
    else: 
        month = str(now.month)
    
    q = "titolo_xml, data_decesso FROM ristretti.decessi_per_istituto WHERE substr(data_decesso,1,2) IS '%s' AND substr(data_decesso,4,2) IS '%s' AND substr(data_decesso,length(data_decesso),7) IS NOT '%s'" % (today, month, str(now.year))

    anniversaries = scraperwiki.sqlite.select(q)

    if (len(anniversaries) > 0): 
        anniversary = random.choice(anniversaries)

        diff_years = int (now.year) - int (anniversary["data_decesso"][-4:])

        return str(diff_years) +' anni fa, '+ anniversary["titolo_xml"].replace("muore","moriva")
    else: return '-1'
        
    


stat = {}
stats_entry = gen_anniversary()
if (stats_entry != -1):
    stat["titolo_xml"] = stats_entry
    stat["current_date"] = current_date
    scraperwiki.sqlite.save(["titolo_xml", "current_date"], stat, table_name="ann_table", verbose=2)
    
# Twitter observatory - anniversary module
# Author: @jackottaviani for RadioRadicale.it and FaiNotizia.it (Italy)

import scraperwiki
import xlrd 
from time import gmtime, strftime
import random
import datetime

hashtag = 'via @Fai_Notizia #DetenutoIgnoto'

now = datetime.datetime.now()

scraperwiki.sqlite.attach("ristretti", "ristretti")

# take current time compatible to RSS2 pubDate format
current_date = strftime("%a, %d %m %Y %H:%M:%S +0000", gmtime())


#Generatore di anniversari, momentaneamente disattivo
def gen_anniversary():

    # if exists anniversary...
    if len(str(now.day)) == 1:
        today = '0'+str(now.day)
    else: 
        today = str(now.day)

    if len(str(now.month)) == 1:
        month = '0'+str(now.month)
    else: 
        month = str(now.month)
    
    q = "titolo_xml, data_decesso FROM ristretti.decessi_per_istituto WHERE substr(data_decesso,1,2) IS '%s' AND substr(data_decesso,4,2) IS '%s' AND substr(data_decesso,length(data_decesso),7) IS NOT '%s'" % (today, month, str(now.year))

    anniversaries = scraperwiki.sqlite.select(q)

    if (len(anniversaries) > 0): 
        anniversary = random.choice(anniversaries)

        diff_years = int (now.year) - int (anniversary["data_decesso"][-4:])

        return str(diff_years) +' anni fa, '+ anniversary["titolo_xml"].replace("muore","moriva")
    else: return '-1'
        
    


stat = {}
stats_entry = gen_anniversary()
if (stats_entry != -1):
    stat["titolo_xml"] = stats_entry
    stat["current_date"] = current_date
    scraperwiki.sqlite.save(["titolo_xml", "current_date"], stat, table_name="ann_table", verbose=2)
    

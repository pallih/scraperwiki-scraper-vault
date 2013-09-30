# Twitter observatory - statistics module
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


def gen_cause_stats():

    # dati disponibili dal 2002    
    year = random.randint(2011, now.year)

    # scegli tra Suicidio e tutte le cause (le altre cause sono minoritarie)
    cause_list = ["Suicidio", "Tutte"]
    cause_to_aggregate = random.choice(cause_list)
    
    # Nel %s %s detenuti sono morti per cause non naturali. (Fonte: Ristretti.it) 
    if cause_to_aggregate == "Tutte":
        q = "COUNT(*) from ristretti.decessi_per_istituto WHERE substr(data_decesso,length(data_decesso)-3) is '%s'" % year
        tot = scraperwiki.sqlite.select(q)[0]["COUNT(*)"]

        s = 'Nel %s, per esempio, %s detenuti sono morti per cause non naturali. (Fonte: Ristretti.it) %s' % (year, tot, hashtag)
        

    # Nel %s, %s detenuti sono morti di. (Fonte: Ristretti.it) 
    else:

        q = "COUNT(*) from ristretti.decessi_per_istituto WHERE substr(data_decesso,length(data_decesso)-3) is '%s' AND ragione_decesso IS '%s'" % (year,cause_to_aggregate)
        tot = scraperwiki.sqlite.select(q)[0]["COUNT(*)"]
        s = 'Nel %s, %s detenuti si sono tolti la vita. (Fonte: Ristretti.it) %s' % (year, tot, hashtag)
    
    return s



def gen_tot():

    #cause_list=["Malattia"]
    cause_list = ["Suicidio", "Omicidio", "Da accertare", "Overdose", "Malattia", "Tutte"]
    cause_to_aggregate = random.choice(cause_list)


    # Dal 2002 a oggi si contano nelle carceri italiane %s morti
    if cause_to_aggregate == "Tutte":
        q = "COUNT(*) from ristretti.decessi_per_istituto"
        tot = scraperwiki.sqlite.select(q)[0]["COUNT(*)"]

        s = 'Dal 2002 nelle carceri italiane sono morti %s detenuti per suicidio, malattia, droga, omicidio o altro. %s' % (tot,hashtag)
        

    # Dal 2002 a oggi si contano nelle carceri italiane %s morti per %s
    else:
        q = "COUNT(*) from ristretti.decessi_per_istituto WHERE ragione_decesso IS '%s'" % (cause_to_aggregate)
        tot = scraperwiki.sqlite.select(q)[0]["COUNT(*)"]
        if cause_to_aggregate == "Da accertare":
            cause_to_aggregate = "cause da accertare"
        s = 'Dal 2002 nelle carceri italiane sono morti %s detenuti per %s. (Fonte: Ristretti.it) %s' % (tot,cause_to_aggregate.lower(),hashtag)
    
    return s




my_list = [gen_cause_stats, gen_tot]

for k in range(2):

    # call random method to generate one statistics
    stats_msg = random.choice(my_list)()
    
    # save entry
    stat = {}
    stat["titolo_xml"] = stats_msg
    stat["current_date"] = current_date

    #print stats_msg
    scraperwiki.sqlite.save(["titolo_xml", "current_date"], stat, table_name="stats_table", verbose=2)
#exit()


# Twitter observatory - statistics module
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


def gen_cause_stats():

    # dati disponibili dal 2002    
    year = random.randint(2011, now.year)

    # scegli tra Suicidio e tutte le cause (le altre cause sono minoritarie)
    cause_list = ["Suicidio", "Tutte"]
    cause_to_aggregate = random.choice(cause_list)
    
    # Nel %s %s detenuti sono morti per cause non naturali. (Fonte: Ristretti.it) 
    if cause_to_aggregate == "Tutte":
        q = "COUNT(*) from ristretti.decessi_per_istituto WHERE substr(data_decesso,length(data_decesso)-3) is '%s'" % year
        tot = scraperwiki.sqlite.select(q)[0]["COUNT(*)"]

        s = 'Nel %s, per esempio, %s detenuti sono morti per cause non naturali. (Fonte: Ristretti.it) %s' % (year, tot, hashtag)
        

    # Nel %s, %s detenuti sono morti di. (Fonte: Ristretti.it) 
    else:

        q = "COUNT(*) from ristretti.decessi_per_istituto WHERE substr(data_decesso,length(data_decesso)-3) is '%s' AND ragione_decesso IS '%s'" % (year,cause_to_aggregate)
        tot = scraperwiki.sqlite.select(q)[0]["COUNT(*)"]
        s = 'Nel %s, %s detenuti si sono tolti la vita. (Fonte: Ristretti.it) %s' % (year, tot, hashtag)
    
    return s



def gen_tot():

    #cause_list=["Malattia"]
    cause_list = ["Suicidio", "Omicidio", "Da accertare", "Overdose", "Malattia", "Tutte"]
    cause_to_aggregate = random.choice(cause_list)


    # Dal 2002 a oggi si contano nelle carceri italiane %s morti
    if cause_to_aggregate == "Tutte":
        q = "COUNT(*) from ristretti.decessi_per_istituto"
        tot = scraperwiki.sqlite.select(q)[0]["COUNT(*)"]

        s = 'Dal 2002 nelle carceri italiane sono morti %s detenuti per suicidio, malattia, droga, omicidio o altro. %s' % (tot,hashtag)
        

    # Dal 2002 a oggi si contano nelle carceri italiane %s morti per %s
    else:
        q = "COUNT(*) from ristretti.decessi_per_istituto WHERE ragione_decesso IS '%s'" % (cause_to_aggregate)
        tot = scraperwiki.sqlite.select(q)[0]["COUNT(*)"]
        if cause_to_aggregate == "Da accertare":
            cause_to_aggregate = "cause da accertare"
        s = 'Dal 2002 nelle carceri italiane sono morti %s detenuti per %s. (Fonte: Ristretti.it) %s' % (tot,cause_to_aggregate.lower(),hashtag)
    
    return s




my_list = [gen_cause_stats, gen_tot]

for k in range(2):

    # call random method to generate one statistics
    stats_msg = random.choice(my_list)()
    
    # save entry
    stat = {}
    stat["titolo_xml"] = stats_msg
    stat["current_date"] = current_date

    #print stats_msg
    scraperwiki.sqlite.save(["titolo_xml", "current_date"], stat, table_name="stats_table", verbose=2)
#exit()


# Twitter observatory - statistics module
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


def gen_cause_stats():

    # dati disponibili dal 2002    
    year = random.randint(2011, now.year)

    # scegli tra Suicidio e tutte le cause (le altre cause sono minoritarie)
    cause_list = ["Suicidio", "Tutte"]
    cause_to_aggregate = random.choice(cause_list)
    
    # Nel %s %s detenuti sono morti per cause non naturali. (Fonte: Ristretti.it) 
    if cause_to_aggregate == "Tutte":
        q = "COUNT(*) from ristretti.decessi_per_istituto WHERE substr(data_decesso,length(data_decesso)-3) is '%s'" % year
        tot = scraperwiki.sqlite.select(q)[0]["COUNT(*)"]

        s = 'Nel %s, per esempio, %s detenuti sono morti per cause non naturali. (Fonte: Ristretti.it) %s' % (year, tot, hashtag)
        

    # Nel %s, %s detenuti sono morti di. (Fonte: Ristretti.it) 
    else:

        q = "COUNT(*) from ristretti.decessi_per_istituto WHERE substr(data_decesso,length(data_decesso)-3) is '%s' AND ragione_decesso IS '%s'" % (year,cause_to_aggregate)
        tot = scraperwiki.sqlite.select(q)[0]["COUNT(*)"]
        s = 'Nel %s, %s detenuti si sono tolti la vita. (Fonte: Ristretti.it) %s' % (year, tot, hashtag)
    
    return s



def gen_tot():

    #cause_list=["Malattia"]
    cause_list = ["Suicidio", "Omicidio", "Da accertare", "Overdose", "Malattia", "Tutte"]
    cause_to_aggregate = random.choice(cause_list)


    # Dal 2002 a oggi si contano nelle carceri italiane %s morti
    if cause_to_aggregate == "Tutte":
        q = "COUNT(*) from ristretti.decessi_per_istituto"
        tot = scraperwiki.sqlite.select(q)[0]["COUNT(*)"]

        s = 'Dal 2002 nelle carceri italiane sono morti %s detenuti per suicidio, malattia, droga, omicidio o altro. %s' % (tot,hashtag)
        

    # Dal 2002 a oggi si contano nelle carceri italiane %s morti per %s
    else:
        q = "COUNT(*) from ristretti.decessi_per_istituto WHERE ragione_decesso IS '%s'" % (cause_to_aggregate)
        tot = scraperwiki.sqlite.select(q)[0]["COUNT(*)"]
        if cause_to_aggregate == "Da accertare":
            cause_to_aggregate = "cause da accertare"
        s = 'Dal 2002 nelle carceri italiane sono morti %s detenuti per %s. (Fonte: Ristretti.it) %s' % (tot,cause_to_aggregate.lower(),hashtag)
    
    return s




my_list = [gen_cause_stats, gen_tot]

for k in range(2):

    # call random method to generate one statistics
    stats_msg = random.choice(my_list)()
    
    # save entry
    stat = {}
    stat["titolo_xml"] = stats_msg
    stat["current_date"] = current_date

    #print stats_msg
    scraperwiki.sqlite.save(["titolo_xml", "current_date"], stat, table_name="stats_table", verbose=2)
#exit()


# Twitter observatory - statistics module
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


def gen_cause_stats():

    # dati disponibili dal 2002    
    year = random.randint(2011, now.year)

    # scegli tra Suicidio e tutte le cause (le altre cause sono minoritarie)
    cause_list = ["Suicidio", "Tutte"]
    cause_to_aggregate = random.choice(cause_list)
    
    # Nel %s %s detenuti sono morti per cause non naturali. (Fonte: Ristretti.it) 
    if cause_to_aggregate == "Tutte":
        q = "COUNT(*) from ristretti.decessi_per_istituto WHERE substr(data_decesso,length(data_decesso)-3) is '%s'" % year
        tot = scraperwiki.sqlite.select(q)[0]["COUNT(*)"]

        s = 'Nel %s, per esempio, %s detenuti sono morti per cause non naturali. (Fonte: Ristretti.it) %s' % (year, tot, hashtag)
        

    # Nel %s, %s detenuti sono morti di. (Fonte: Ristretti.it) 
    else:

        q = "COUNT(*) from ristretti.decessi_per_istituto WHERE substr(data_decesso,length(data_decesso)-3) is '%s' AND ragione_decesso IS '%s'" % (year,cause_to_aggregate)
        tot = scraperwiki.sqlite.select(q)[0]["COUNT(*)"]
        s = 'Nel %s, %s detenuti si sono tolti la vita. (Fonte: Ristretti.it) %s' % (year, tot, hashtag)
    
    return s



def gen_tot():

    #cause_list=["Malattia"]
    cause_list = ["Suicidio", "Omicidio", "Da accertare", "Overdose", "Malattia", "Tutte"]
    cause_to_aggregate = random.choice(cause_list)


    # Dal 2002 a oggi si contano nelle carceri italiane %s morti
    if cause_to_aggregate == "Tutte":
        q = "COUNT(*) from ristretti.decessi_per_istituto"
        tot = scraperwiki.sqlite.select(q)[0]["COUNT(*)"]

        s = 'Dal 2002 nelle carceri italiane sono morti %s detenuti per suicidio, malattia, droga, omicidio o altro. %s' % (tot,hashtag)
        

    # Dal 2002 a oggi si contano nelle carceri italiane %s morti per %s
    else:
        q = "COUNT(*) from ristretti.decessi_per_istituto WHERE ragione_decesso IS '%s'" % (cause_to_aggregate)
        tot = scraperwiki.sqlite.select(q)[0]["COUNT(*)"]
        if cause_to_aggregate == "Da accertare":
            cause_to_aggregate = "cause da accertare"
        s = 'Dal 2002 nelle carceri italiane sono morti %s detenuti per %s. (Fonte: Ristretti.it) %s' % (tot,cause_to_aggregate.lower(),hashtag)
    
    return s




my_list = [gen_cause_stats, gen_tot]

for k in range(2):

    # call random method to generate one statistics
    stats_msg = random.choice(my_list)()
    
    # save entry
    stat = {}
    stat["titolo_xml"] = stats_msg
    stat["current_date"] = current_date

    #print stats_msg
    scraperwiki.sqlite.save(["titolo_xml", "current_date"], stat, table_name="stats_table", verbose=2)
#exit()



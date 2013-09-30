import scraperwiki  
import lxml.html
import re
import dateutil.parser 
from datetime import date
import datetime

# coding: utf-8

debug = 0;

def DBG(text):
    if debug:
        print text


###########################################################
#                      Main routine                       #
###########################################################

scraperwiki.sqlite.execute("drop table if exists portcall")
scraperwiki.sqlite.execute("drop table if exists port")
scraperwiki.sqlite.execute("drop table if exists berth")

scraperwiki.sqlite.execute("CREATE TABLE `portcall` (`id` integer PRIMARY KEY AUTOINCREMENT, `portin` datetime, `portout` datetime, `ship_name` text, `prev_port` text, `next_port` text, `berth_name` text, `tour_name` text)")
scraperwiki.sqlite.execute("CREATE TABLE `port` (`port_name` text PRIMARY KEY, `longitude` float, `latitude` float)")

portcall_id = 0;

html = scraperwiki.scrape("http://www.city.kobe.lg.jp/culture/leisure/harbor/passenger/schedule/index.html")

sjis_char  = "\x87\x55"
print "Roman numeral 2 appears " + str(html.count(sjis_char)) + " time(s)."

root = lxml.html.fromstring(html.replace(sjis_char, "II"))


for elmTRow in root.cssselect("table tbody tr"):

    elmTData = elmTRow.cssselect("td")

    DBG("====> elmTRow: " + lxml.html.tostring(elmTRow)) 

    # 結合された列をスキップ
    if len(elmTData) <= 1:
        print len(elmTData) 
        DBG("elmTRow : " + lxml.html.tostring(elmTRow)) 
        DBG(elmTData[0].text_content().strip())
        continue

    #######################################################
    ## Database に突っ込む用の変数を初期化
    #######################################################

    datetime_portin = None
    datetime_portout = None
    ship_name = prev_port = next_port = berth_name = tour_name = ""

    ## 
    ## 入港（表記例：「 | 1月6日(金) | 15:00 | 」）
    ## 
    dayIn= hourIn = minIn = "0";
    flgDateInUp = 0

    txtDateIn = elmTData[3].text_content().strip()
    DBG("txtDateIn  : " + txtDateIn)
    # 「1月6日(金)」をパース
    if re.match(r"([0-9]+)\D+([0-9]+)\D+", txtDateIn, re.UNICODE):
        mDateIn = re.match(r"([0-9]+)\D+([0-9]+)\D+", txtDateIn, re.UNICODE)
        monIn = mDateIn.group(1)
        dayIn = mDateIn.group(2)
        DBG(monIn + "/" + dayIn)
    else:
        print " *** not match : txtDateIn  *** "
        print txtDateIn 
        continue

    txtTimeIn = elmTData[4].text_content().strip()
    DBG("txtTimeIn : " + txtTimeIn ) 
    # 「15:00」をパース
    if re.match(r"([0-9]+)\D+([0-9]+)", txtTimeIn , re.UNICODE):
        mTimeIn = re.match(r"([0-9]+)\D+([0-9]+)", txtTimeIn , re.UNICODE)
        hourIn = mTimeIn.group(1)
        minIn = mTimeIn.group(2)
        DBG(hourIn + ":" + minIn)
    else:
        print " *** not match : txtTimeIn *** "
        print txtTimeIn 
        continue

    time_portin = "2012-" + monIn + "-" + dayIn + " " + hourIn + ":" + minIn + ":00"
    datetime_portin = dateutil.parser.parse(time_portin ) + datetime.timedelta(days=flgDateInUp )# 2010-06-21
    DBG("datetime_portin : " +  str(datetime_portin)) 

    ## 
    ## 出港（表記例：「 | 1月6日(金) | 21:00 | 」）
    ## 
    dayOut= hourOut = minOut = "0";
    flgDateOutUp = 0

    txtDateOut = elmTData[5].text_content().strip()
    DBG("txtDateOut  : " + txtDateOut)
    # 「1月6日(金)」をパース
    if re.match(r"([0-9]+)\D+([0-9]+)\D+", txtDateOut, re.UNICODE):
        mDateOut = re.match(r"([0-9]+)\D+([0-9]+)\D+", txtDateOut, re.UNICODE)
        monOut = mDateOut.group(1)
        dayOut = mDateOut.group(2)
        DBG(monOut + "/" + dayOut)
    else:
        print " *** not match : txtDateOut  *** "
        print txtDateOut 
        continue

    txtTimeOut = elmTData[6].text_content().strip()
    DBG("txtTimeOut : " + txtTimeOut ) 
    # 「21:00」をパース
    if re.match(r"([0-9]+)\D+([0-9]+)", txtTimeOut, re.UNICODE):
        mTimeOut = re.match(r"([0-9]+)\D+([0-9]+)", txtTimeOut , re.UNICODE)
        hourOut = mTimeOut.group(1)
        minOut = mTimeOut.group(2)
        DBG(hourOut + ":" + minOut)
    else:
        print " *** not match : txtTimeOut *** "
        print txtTimeOut
        continue

    time_portout = "2012-" + monOut + "-" + dayOut + " " + hourOut + ":" + minOut + ":00"
    datetime_portout = dateutil.parser.parse(time_portout ) + datetime.timedelta(days=flgDateOutUp )# 2010-06-21
    DBG("datetime_portout : " +  str(datetime_portout)) 

    ## 
    ## 客船名（表記例：「飛鳥II」）
    ## 
    ship_name = elmTData[0].text_content().strip()

    ## 
    ## 前港（表記例：「ホンコン」）
    ## 
    prev_port = elmTData[7].text_content().strip()

    ## 
    ## 次港（表記例：「横浜」）
    ## 
    next_port = elmTData[8].text_content().strip()

    ## 
    ## バース（表記例：「NAKA-BC」）
    ## 
    berth_name = elmTData[2].text_content().strip()

    ## 
    ## クルーズ内容など（表記例：「ニューイヤー香港クルーズ帰港」）
    ## 
    tour_name = elmTData[9].text_content().strip()


    #######################################################
    ## Datastore (DB : "portcall")
    #######################################################
    entry = {}
    entry["id"] = portcall_id; portcall_id += 1;
    entry["portin"] = datetime_portin
    entry["portout"] = datetime_portout
    entry["ship_name"] = ship_name
    entry["prev_port"] = prev_port
    entry["next_port"] = next_port
    entry["berth_name"] = berth_name;
    entry["tour_name"] = tour_name

    scraperwiki.sqlite.save(["id"], entry, "portcall")   
    print datetime_portin.__str__() + " ~ " + datetime_portout.__str__() + " : " + ship_name + " (" + prev_port+ " -> " + berth_name + " -> " + next_port + ") ; " + tour_name 
    
    #######################################################
    ## Datastore (DB : "port")
    #######################################################
    entry = {}
    entry["port_name"] = prev_port
    scraperwiki.sqlite.save(["port_name"], entry, "port")

    entry = {}
    entry["port_name"] = next_port
    scraperwiki.sqlite.save(["port_name"], entry, "port")import scraperwiki  
import lxml.html
import re
import dateutil.parser 
from datetime import date
import datetime

# coding: utf-8

debug = 0;

def DBG(text):
    if debug:
        print text


###########################################################
#                      Main routine                       #
###########################################################

scraperwiki.sqlite.execute("drop table if exists portcall")
scraperwiki.sqlite.execute("drop table if exists port")
scraperwiki.sqlite.execute("drop table if exists berth")

scraperwiki.sqlite.execute("CREATE TABLE `portcall` (`id` integer PRIMARY KEY AUTOINCREMENT, `portin` datetime, `portout` datetime, `ship_name` text, `prev_port` text, `next_port` text, `berth_name` text, `tour_name` text)")
scraperwiki.sqlite.execute("CREATE TABLE `port` (`port_name` text PRIMARY KEY, `longitude` float, `latitude` float)")

portcall_id = 0;

html = scraperwiki.scrape("http://www.city.kobe.lg.jp/culture/leisure/harbor/passenger/schedule/index.html")

sjis_char  = "\x87\x55"
print "Roman numeral 2 appears " + str(html.count(sjis_char)) + " time(s)."

root = lxml.html.fromstring(html.replace(sjis_char, "II"))


for elmTRow in root.cssselect("table tbody tr"):

    elmTData = elmTRow.cssselect("td")

    DBG("====> elmTRow: " + lxml.html.tostring(elmTRow)) 

    # 結合された列をスキップ
    if len(elmTData) <= 1:
        print len(elmTData) 
        DBG("elmTRow : " + lxml.html.tostring(elmTRow)) 
        DBG(elmTData[0].text_content().strip())
        continue

    #######################################################
    ## Database に突っ込む用の変数を初期化
    #######################################################

    datetime_portin = None
    datetime_portout = None
    ship_name = prev_port = next_port = berth_name = tour_name = ""

    ## 
    ## 入港（表記例：「 | 1月6日(金) | 15:00 | 」）
    ## 
    dayIn= hourIn = minIn = "0";
    flgDateInUp = 0

    txtDateIn = elmTData[3].text_content().strip()
    DBG("txtDateIn  : " + txtDateIn)
    # 「1月6日(金)」をパース
    if re.match(r"([0-9]+)\D+([0-9]+)\D+", txtDateIn, re.UNICODE):
        mDateIn = re.match(r"([0-9]+)\D+([0-9]+)\D+", txtDateIn, re.UNICODE)
        monIn = mDateIn.group(1)
        dayIn = mDateIn.group(2)
        DBG(monIn + "/" + dayIn)
    else:
        print " *** not match : txtDateIn  *** "
        print txtDateIn 
        continue

    txtTimeIn = elmTData[4].text_content().strip()
    DBG("txtTimeIn : " + txtTimeIn ) 
    # 「15:00」をパース
    if re.match(r"([0-9]+)\D+([0-9]+)", txtTimeIn , re.UNICODE):
        mTimeIn = re.match(r"([0-9]+)\D+([0-9]+)", txtTimeIn , re.UNICODE)
        hourIn = mTimeIn.group(1)
        minIn = mTimeIn.group(2)
        DBG(hourIn + ":" + minIn)
    else:
        print " *** not match : txtTimeIn *** "
        print txtTimeIn 
        continue

    time_portin = "2012-" + monIn + "-" + dayIn + " " + hourIn + ":" + minIn + ":00"
    datetime_portin = dateutil.parser.parse(time_portin ) + datetime.timedelta(days=flgDateInUp )# 2010-06-21
    DBG("datetime_portin : " +  str(datetime_portin)) 

    ## 
    ## 出港（表記例：「 | 1月6日(金) | 21:00 | 」）
    ## 
    dayOut= hourOut = minOut = "0";
    flgDateOutUp = 0

    txtDateOut = elmTData[5].text_content().strip()
    DBG("txtDateOut  : " + txtDateOut)
    # 「1月6日(金)」をパース
    if re.match(r"([0-9]+)\D+([0-9]+)\D+", txtDateOut, re.UNICODE):
        mDateOut = re.match(r"([0-9]+)\D+([0-9]+)\D+", txtDateOut, re.UNICODE)
        monOut = mDateOut.group(1)
        dayOut = mDateOut.group(2)
        DBG(monOut + "/" + dayOut)
    else:
        print " *** not match : txtDateOut  *** "
        print txtDateOut 
        continue

    txtTimeOut = elmTData[6].text_content().strip()
    DBG("txtTimeOut : " + txtTimeOut ) 
    # 「21:00」をパース
    if re.match(r"([0-9]+)\D+([0-9]+)", txtTimeOut, re.UNICODE):
        mTimeOut = re.match(r"([0-9]+)\D+([0-9]+)", txtTimeOut , re.UNICODE)
        hourOut = mTimeOut.group(1)
        minOut = mTimeOut.group(2)
        DBG(hourOut + ":" + minOut)
    else:
        print " *** not match : txtTimeOut *** "
        print txtTimeOut
        continue

    time_portout = "2012-" + monOut + "-" + dayOut + " " + hourOut + ":" + minOut + ":00"
    datetime_portout = dateutil.parser.parse(time_portout ) + datetime.timedelta(days=flgDateOutUp )# 2010-06-21
    DBG("datetime_portout : " +  str(datetime_portout)) 

    ## 
    ## 客船名（表記例：「飛鳥II」）
    ## 
    ship_name = elmTData[0].text_content().strip()

    ## 
    ## 前港（表記例：「ホンコン」）
    ## 
    prev_port = elmTData[7].text_content().strip()

    ## 
    ## 次港（表記例：「横浜」）
    ## 
    next_port = elmTData[8].text_content().strip()

    ## 
    ## バース（表記例：「NAKA-BC」）
    ## 
    berth_name = elmTData[2].text_content().strip()

    ## 
    ## クルーズ内容など（表記例：「ニューイヤー香港クルーズ帰港」）
    ## 
    tour_name = elmTData[9].text_content().strip()


    #######################################################
    ## Datastore (DB : "portcall")
    #######################################################
    entry = {}
    entry["id"] = portcall_id; portcall_id += 1;
    entry["portin"] = datetime_portin
    entry["portout"] = datetime_portout
    entry["ship_name"] = ship_name
    entry["prev_port"] = prev_port
    entry["next_port"] = next_port
    entry["berth_name"] = berth_name;
    entry["tour_name"] = tour_name

    scraperwiki.sqlite.save(["id"], entry, "portcall")   
    print datetime_portin.__str__() + " ~ " + datetime_portout.__str__() + " : " + ship_name + " (" + prev_port+ " -> " + berth_name + " -> " + next_port + ") ; " + tour_name 
    
    #######################################################
    ## Datastore (DB : "port")
    #######################################################
    entry = {}
    entry["port_name"] = prev_port
    scraperwiki.sqlite.save(["port_name"], entry, "port")

    entry = {}
    entry["port_name"] = next_port
    scraperwiki.sqlite.save(["port_name"], entry, "port")
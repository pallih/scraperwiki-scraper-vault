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

scraperwiki.sqlite.execute("CREATE TABLE `portcall` (`id` integer PRIMARY KEY AUTOINCREMENT, `portin` datetime, `portout` datetime, `ship_name` text, `prev_port` text, `next_port` text, `tour_name` text)")
scraperwiki.sqlite.execute("CREATE TABLE `port` (`port_name` text PRIMARY KEY, `longitude` float, `latitude` float)")

portcall_id = 0;

html = scraperwiki.scrape("http://www.city.yokohama.lg.jp/kowan/cruise/schedule/20111102200949.html")
root = lxml.html.fromstring(html)

for elmTable in root.cssselect("table"):
    # caption タグを含まないテーブルはカレンダー情報じゃないのでスキップ
    if len(elmTable.cssselect("caption")) == 0:
        print "break"
        continue
    else:
        year_month = elmTable.cssselect("caption").pop(0).text
        print year_month
        mYrMon = re.match(r"([0-9]+)\D+([0-9]+)", year_month, re.UNICODE)

    for elmTRow in elmTable.cssselect("tbody tr"):
        elmTData = elmTRow.cssselect("td")
        if elmTData[0].attrib.has_key("bgcolor"):
            print "table header"
            continue
        # 伊豆諸島の最後の列をスキップ
        elif len(elmTData) < 1:
            print "jointed td"
            continue
        
        ## 
        ## 入港（着岸）予定（表記例：「4(水) 8:30」）
        ## 
        dayIn= hourIn = minIn = "0";
        flgDateInUp = 0

        txtDateIn = elmTData[0].text_content().strip()
        DBG("IN: " + txtDateIn) 
        if re.match(r"([0-9]+)\D+([0-9]+)\D+([0-9]+)", txtDateIn, re.UNICODE):
            mDateIn = re.match(r"([0-9]+)\D+([0-9]+)\D+([0-9]+)", txtDateIn, re.UNICODE)
            dayIn = mDateIn.group(1)
            if mDateIn.group(2) == "24":
                DBG("24:00 appears -> handle as the next day")
                flgDateInUp = 1
                hourIn = "0"
            else:
                hourIn = mDateIn.group(2)
            minIn = mDateIn.group(3)
        elif re.match(r"([0-9]+)\D+PM", txtDateIn, re.UNICODE):
            DBG("パターン「4日 PM」")
            mDateIn = re.match(r"([0-9]+)\D+PM", txtDateIn, re.UNICODE)
            dayIn = mDateIn.group(1)
            hourIn = "12"
            minIn = "01"
        elif re.match(r"([0-9]+)\D+", txtDateIn, re.UNICODE):
            DBG("パターン「4日」")
            mDateIn = re.match(r"([0-9]+)\D+", txtDateIn, re.UNICODE)
            dayIn = mDateIn.group(1)
            hourIn = "00"
            minIn = "01"
        else:
            print " *** not match : port-in  *** "
            print txtDateIn 
            continue

        time_portin = mYrMon.group(1) + "-" + mYrMon.group(2) + "-" + dayIn + " " + hourIn + ":" + minIn + ":00"
        datetime_portin = dateutil.parser.parse(time_portin ) + datetime.timedelta(days=flgDateInUp )# 2010-06-21

        ## 
        ## 出港（離岸）予定（表記例：「4(水) 17:00」）
        ## 
        dayOut = hourOut = minOut = "0";
        flgDateOutUp = 0
        flgMonthNext = 0

        txtDateOut= elmTData[1].text_content().strip()
        DBG("OUT : " + txtDateOut) 
        if re.match(r"([0-9]+)\D+([0-9]+)\D+([0-9]+)", txtDateOut, re.UNICODE):
            mDateOut = re.match(r"([0-9]+)\D+([0-9]+)\D+([0-9]+)", txtDateOut, re.UNICODE)
            dayOut = mDateOut.group(1)
            if mDateOut .group(2) == "24":
                DBG("24:00 appears -> handle as the next day")
                flgDateOutUp = 1
                hourOut = "0"
            else:
                hourOut = mDateOut.group(2)
            minOut = mDateOut.group(3)
        elif re.match(r"([0-9]+)\D+PM", txtDateOut, re.UNICODE):
            DBG("パターン「4日 PM」")
            mDateOut = re.match(r"([0-9]+)\D+PM", txtDateOut, re.UNICODE)
            dayOut = mDateOut.group(1)
            hourOut = "12"
            minOut = "01"
        elif re.match(r"([0-9]+)\D+", txtDateOut, re.UNICODE):
            DBG("パターン「4日」")
            mDateOut = re.match(r"([0-9]+)\D+", txtDateOut, re.UNICODE)
            dayOut = mDateOut.group(1)
            hourOut = "00"
            minOut = "01"
        else:
            print " *** not match : port-out *** "
            print txtDateOut 
            continue
        
        if dayOut < dayIn:
            flgMonthNext = 1

        time_portout = mYrMon.group(1) + "-" + mYrMon.group(2) + "-" + dayOut + " " + hourOut + ":" + minOut + ":00"
        datetime_portout = dateutil.parser.parse(time_portout ) + datetime.timedelta(days=flgDateOutUp ) + dateutil.relativedelta.relativedelta(months=flgMonthNext)

        ## 
        ## 客船名（表記例：「飛鳥II」）
        ## 
        ship_name = elmTData[2].text_content().strip()

        ## 
        ## 前港（表記例：「ホンコン」）
        ## 
        prev_port = elmTData[3].text_content().strip()

        ## 
        ## 次港（表記例：「横浜」）
        ## 
        next_port = elmTData[4].text_content().strip()

        ## 
        ## クルーズ内容など（表記例：「ニューイヤー香港クルーズ帰港」）
        ## 
        tour_name = elmTData[5].text_content().strip()

        ##
        ## Datastore (DB : "portcall")
        ##
        entry = {}
        entry["id"] = portcall_id; portcall_id += 1;
        entry["portin"] = datetime_portin
        entry["portout"] = datetime_portout
        entry["ship_name"] = ship_name
        entry["prev_port"] = prev_port
        entry["next_port"] = next_port
        entry["tour_name"] = tour_name

        scraperwiki.sqlite.save(["id"], entry, "portcall")   
        print datetime_portin.__str__() + " ~ " + datetime_portout.__str__() + " : " + ship_name + " (" + prev_port+ " -> , -> " + next_port + ") ; " + tour_name 
        
        ##
        ## Datastore (DB : "port")
        ##
        entry = {}
        entry["port_name"] = prev_port
        scraperwiki.sqlite.save(["port_name"], entry, "port")

        entry = {}
        entry["port_name"] = next_port
        scraperwiki.sqlite.save(["port_name"], entry, "port")
# coding: utf-8

import scraperwiki           
import lxml.html
import re
import htmlentitydefs

##
## Quoted from http://www.programming-magic.com/20080820002254/
##

# 実体参照 & 文字参照を通常の文字に戻す
def htmlentity2unicode(text):
    # 正規表現のコンパイル
    reference_regex = re.compile(u'&(#x?[0-9a-f]+|[a-z]+);', re.IGNORECASE)
    num16_regex = re.compile(u'#x\d+', re.IGNORECASE)
    num10_regex = re.compile(u'#\d+', re.IGNORECASE)
    
    result = u''
    i = 0
    while True:
        # 実体参照 or 文字参照を見つける
        match = reference_regex.search(text, i)
        if match is None:
            result += text[i:]
            break
        
        result += text[i:match.start()]
        i = match.end()
        name = match.group(1)
        
        # 実体参照
        if name in htmlentitydefs.name2codepoint.keys():
            result += unichr(htmlentitydefs.name2codepoint[name])
        # 文字参照
        elif num16_regex.match(name):
            # 16進数
            result += unichr(int(u'0'+name[1:], 16))
        elif num10_regex.match(name):
            # 10進数
            result += unichr(int(name[1:]))

    return result

def parse_device_page(url):
    html_dev = scraperwiki.scrape(url)
    root_dev = lxml.html.fromstring(html_dev)
    
    cat0_name = root_dev.cssselect("div.archive h2 img").pop(0).attrib['alt']
    cat1_name = root_dev.cssselect("div.archive h3").pop(0).text
    if len(root_dev.cssselect("div.archive h4")) > 0:
        cat2_name = root_dev.cssselect("div.archive h4").pop(0).text
    else:
        cat2_name = "-"
    dateChecked = root_dev.cssselect("p.lastDateBox").pop(0).text
    print cat0_name, cat1_name, url
    
    for el in root_dev.cssselect("div.entryBox"):
        device_name = el.cssselect("dt").pop(0).text
        device_entry = parse_support_devices(el.cssselect("dd p").pop(0))
        device_entry["id"] = url.split("?category_name=").pop(1) + "_" + device_name.replace(" ", "-")
        device_entry["cat0"] = cat0_name
        device_entry["cat1"] = cat1_name
        device_entry["cat2"] = cat2_name
        device_entry["device"] = device_name
        device_entry["url"] = url
        device_entry["lastDateChecked"] = dateChecked
        scraperwiki.sqlite.save(["id"], device_entry, "compatibility")   


def parse_support_devices(element):
    text = lxml.html.tostring(element)
    if text[3:6] == "KBC":
        precondition_text = ""
    else:
        precondition_text = htmlentity2unicode(re.findall("<p>.*<", text).pop(0)[3:-1])
        text = text[len((re.findall("<p>.*<", text).pop(0))):]
        print text
    ret_support_list = {}
    for charger in re.findall("KBC-.*", text):
        ret_support_list[charger.split(" ",1).pop(0)] = htmlentity2unicode(charger.split(" ",1).pop(1).split("<").pop(0))
    ret_support_list["precondition_text "] = precondition_text
    return ret_support_list


###########################################################
#                      Main routine                       #
###########################################################

scraperwiki.sqlite.execute("drop table if exists swdata")
scraperwiki.sqlite.execute("drop table if exists boosted")
#scraperwiki.sqlite.execute("drop table if exists compatibility")

#scraperwiki.sqlite.execute("CREATE TABLE `compatibility` (`id` text1, `cat0` text, `cat1` text, `cat2` text, `device` text, `precondition` text, `KBC-L54D` text, `KBC-L27D` text, `KBC-L2BS` text, `KBC-D1AS` text, `KBC-L2AS` text, `KBC-L3AS` text,`KBC-E1AS` text, `KBC-D1BS` text, `KBC-DS2AS` text, `KBC-DS3AS` text, `lastDateChecked` text, `url` text)")

#parse_device_page("http://jp.sanyo.com/eneloop/m/?category_name=mb1_docomo_fujitsu")

html = scraperwiki.scrape("http://jp.sanyo.com/eneloop/m/")
root = lxml.html.fromstring(html)

for el in root.cssselect("p.lastDateBox"):
    print el.text

for el in root.cssselect("li.cat-item a"):           
    print el.attrib['href']
    
    ## mb3_ のページのみを試す用
    #if re.search("mb3_", el.attrib['href']) == None:
    #    continue

    html_cat = scraperwiki.scrape(el.attrib['href']);
    root_cat = lxml.html.fromstring(html_cat)

    ## メーカー別ページがはさまれる場合
    if len(root_cat.cssselect("div.pagebody-inner div.sectionBox")) > 0:
    
        for el in root_cat.cssselect("ul.indexList li.cat-item a"):
            parse_device_page(el.attrib['href'])
    
    ## 直接機器一覧ページに飛ぶ場合
    elif len(root_cat.cssselect("div.pagebody-inner div.entryBoxArea")) > 0:

        parse_device_page(el.attrib['href'])
# coding: utf-8

import scraperwiki           
import lxml.html
import re
import htmlentitydefs

##
## Quoted from http://www.programming-magic.com/20080820002254/
##

# 実体参照 & 文字参照を通常の文字に戻す
def htmlentity2unicode(text):
    # 正規表現のコンパイル
    reference_regex = re.compile(u'&(#x?[0-9a-f]+|[a-z]+);', re.IGNORECASE)
    num16_regex = re.compile(u'#x\d+', re.IGNORECASE)
    num10_regex = re.compile(u'#\d+', re.IGNORECASE)
    
    result = u''
    i = 0
    while True:
        # 実体参照 or 文字参照を見つける
        match = reference_regex.search(text, i)
        if match is None:
            result += text[i:]
            break
        
        result += text[i:match.start()]
        i = match.end()
        name = match.group(1)
        
        # 実体参照
        if name in htmlentitydefs.name2codepoint.keys():
            result += unichr(htmlentitydefs.name2codepoint[name])
        # 文字参照
        elif num16_regex.match(name):
            # 16進数
            result += unichr(int(u'0'+name[1:], 16))
        elif num10_regex.match(name):
            # 10進数
            result += unichr(int(name[1:]))

    return result

def parse_device_page(url):
    html_dev = scraperwiki.scrape(url)
    root_dev = lxml.html.fromstring(html_dev)
    
    cat0_name = root_dev.cssselect("div.archive h2 img").pop(0).attrib['alt']
    cat1_name = root_dev.cssselect("div.archive h3").pop(0).text
    if len(root_dev.cssselect("div.archive h4")) > 0:
        cat2_name = root_dev.cssselect("div.archive h4").pop(0).text
    else:
        cat2_name = "-"
    dateChecked = root_dev.cssselect("p.lastDateBox").pop(0).text
    print cat0_name, cat1_name, url
    
    for el in root_dev.cssselect("div.entryBox"):
        device_name = el.cssselect("dt").pop(0).text
        device_entry = parse_support_devices(el.cssselect("dd p").pop(0))
        device_entry["id"] = url.split("?category_name=").pop(1) + "_" + device_name.replace(" ", "-")
        device_entry["cat0"] = cat0_name
        device_entry["cat1"] = cat1_name
        device_entry["cat2"] = cat2_name
        device_entry["device"] = device_name
        device_entry["url"] = url
        device_entry["lastDateChecked"] = dateChecked
        scraperwiki.sqlite.save(["id"], device_entry, "compatibility")   


def parse_support_devices(element):
    text = lxml.html.tostring(element)
    if text[3:6] == "KBC":
        precondition_text = ""
    else:
        precondition_text = htmlentity2unicode(re.findall("<p>.*<", text).pop(0)[3:-1])
        text = text[len((re.findall("<p>.*<", text).pop(0))):]
        print text
    ret_support_list = {}
    for charger in re.findall("KBC-.*", text):
        ret_support_list[charger.split(" ",1).pop(0)] = htmlentity2unicode(charger.split(" ",1).pop(1).split("<").pop(0))
    ret_support_list["precondition_text "] = precondition_text
    return ret_support_list


###########################################################
#                      Main routine                       #
###########################################################

scraperwiki.sqlite.execute("drop table if exists swdata")
scraperwiki.sqlite.execute("drop table if exists boosted")
#scraperwiki.sqlite.execute("drop table if exists compatibility")

#scraperwiki.sqlite.execute("CREATE TABLE `compatibility` (`id` text1, `cat0` text, `cat1` text, `cat2` text, `device` text, `precondition` text, `KBC-L54D` text, `KBC-L27D` text, `KBC-L2BS` text, `KBC-D1AS` text, `KBC-L2AS` text, `KBC-L3AS` text,`KBC-E1AS` text, `KBC-D1BS` text, `KBC-DS2AS` text, `KBC-DS3AS` text, `lastDateChecked` text, `url` text)")

#parse_device_page("http://jp.sanyo.com/eneloop/m/?category_name=mb1_docomo_fujitsu")

html = scraperwiki.scrape("http://jp.sanyo.com/eneloop/m/")
root = lxml.html.fromstring(html)

for el in root.cssselect("p.lastDateBox"):
    print el.text

for el in root.cssselect("li.cat-item a"):           
    print el.attrib['href']
    
    ## mb3_ のページのみを試す用
    #if re.search("mb3_", el.attrib['href']) == None:
    #    continue

    html_cat = scraperwiki.scrape(el.attrib['href']);
    root_cat = lxml.html.fromstring(html_cat)

    ## メーカー別ページがはさまれる場合
    if len(root_cat.cssselect("div.pagebody-inner div.sectionBox")) > 0:
    
        for el in root_cat.cssselect("ul.indexList li.cat-item a"):
            parse_device_page(el.attrib['href'])
    
    ## 直接機器一覧ページに飛ぶ場合
    elif len(root_cat.cssselect("div.pagebody-inner div.entryBoxArea")) > 0:

        parse_device_page(el.attrib['href'])

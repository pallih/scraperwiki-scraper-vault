import scraperwiki
import lxml.html
import re
import math

def GetSize1(exp,prof):

    result = 0

    # 指定された条件で検索
    m = re.search(exp,prof)

    if not m is None:
        size = m.group()
        result = int(size[2:len(size)])
    else:
        result = -1

    return result

def GetTheoryValue(T,B,W,H):

    # 理論値
    Theory_B = T*0.54
    Theory_W = T*0.38
    Theory_H = Theory_B

    # 有効率
    Rate = (B-W)*100/float(T)

    # 縦横比
    Direction = (B+W+H)*10/float(T)

    # style
    style = ""
    styleN = 0

    if Rate > 14.5:
        if Direction > 14.5:
            style = "gram"
            styleN  = 3
        else:
            style = "nice"
            styleN = 4
    else:
        if Direction > 14.3:
            style = "寸胴"
            styleN  = 2
        else:
            style = "すとん"
            styleN = 1

    # 分類
    val =  ((B**2) - W) / float(T)
    ti = ""
    if val < 30:
        ti = "無"
    elif 30 <= val and val < 38:
        ti = "貧"
    elif 38 <= val and val < 45:
        ti = "普"
    elif 45 <= val and val < 55:
        ti = "巨"
    elif 55 <= val and val < 65:
        ti = "爆"
    elif 65 <= val:
        ti = "超"

    return Theory_B,Theory_W,Theory_H,Rate,Direction,style,styleN,val,ti



# Blank Python

URL = "http://www.h-sister.com" 
URI = URL + "/cast.html"

html = lxml.html.parse(URI)
persons = html.xpath('//div[@id="wrap"]')

for p in persons:

    name = ""
    status = ""
    img = ""
    href =""

    for i in p.findall('div'):

        if i.attrib.has_key("class") and i.attrib["class"] == "castall" and i.attrib.has_key("id") :

            if i.attrib["id"] == "aname":
                name = i.text

            if i.attrib["id"] == "status":
                status = i.text

            if i.attrib["id"] == "aphoto":

                for e in i.getiterator():
                    
                    if e.tag == "a":
                        href = e.get("href")
                        #print e.get("href")
                    if e.tag =="img":
                        img = e.get("src")


    print name,status,href,img

    age = re.search('\d{2,2}',name)
    if not age is None:
        age = int(age.group())
    else:
        age =-1

    T = re.search('T:[0-9][0-9][0-9]',status)
    if not T is None:
        T = int(T.group()[2:5])
    else:
        T = -1
            
    B = GetSize1('B:\d{2,3}',status)
    W = GetSize1('W:\d{2,3}',status)
    H = GetSize1('H:\d{2,3}',status)

    #print T,B,W,H

    if name != "" and age != "" and T > 0 and B > 0 and W > 0 and H > 0:

        result = GetTheoryValue(T,B,W,H)

        scraperwiki.sqlite.save(unique_keys=["name"],data = {
                "name":name,
                "T":T,
                "B":B,
                "W":W,
                "H":H,
                "C":"",
                "Theory_B":result[0],
                "Theory_W":result[1],
                "Theory_H":result[2],
                "Rate":result[3],
                "Direction":result[4],
                "Style":result[5],
                "StyleN":result[6],
                "Level":result[8],
                "LevelN":result[7],
                "info":"",
                "age":age,
                "shop":"funabashi H",
                "image":URL + img,
                "detail":URL + href[1:len(href)]
            } )               


import scraperwiki
import lxml.html
import re
import math

def GetSize1(exp,prof):

    result = 0

    # 指定された条件で検索
    m = re.search(exp,prof)

    if not m is None:
        size = m.group()
        result = int(size[2:len(size)])
    else:
        result = -1

    return result

def GetTheoryValue(T,B,W,H):

    # 理論値
    Theory_B = T*0.54
    Theory_W = T*0.38
    Theory_H = Theory_B

    # 有効率
    Rate = (B-W)*100/float(T)

    # 縦横比
    Direction = (B+W+H)*10/float(T)

    # style
    style = ""
    styleN = 0

    if Rate > 14.5:
        if Direction > 14.5:
            style = "gram"
            styleN  = 3
        else:
            style = "nice"
            styleN = 4
    else:
        if Direction > 14.3:
            style = "寸胴"
            styleN  = 2
        else:
            style = "すとん"
            styleN = 1

    # 分類
    val =  ((B**2) - W) / float(T)
    ti = ""
    if val < 30:
        ti = "無"
    elif 30 <= val and val < 38:
        ti = "貧"
    elif 38 <= val and val < 45:
        ti = "普"
    elif 45 <= val and val < 55:
        ti = "巨"
    elif 55 <= val and val < 65:
        ti = "爆"
    elif 65 <= val:
        ti = "超"

    return Theory_B,Theory_W,Theory_H,Rate,Direction,style,styleN,val,ti



# Blank Python

URL = "http://www.h-sister.com" 
URI = URL + "/cast.html"

html = lxml.html.parse(URI)
persons = html.xpath('//div[@id="wrap"]')

for p in persons:

    name = ""
    status = ""
    img = ""
    href =""

    for i in p.findall('div'):

        if i.attrib.has_key("class") and i.attrib["class"] == "castall" and i.attrib.has_key("id") :

            if i.attrib["id"] == "aname":
                name = i.text

            if i.attrib["id"] == "status":
                status = i.text

            if i.attrib["id"] == "aphoto":

                for e in i.getiterator():
                    
                    if e.tag == "a":
                        href = e.get("href")
                        #print e.get("href")
                    if e.tag =="img":
                        img = e.get("src")


    print name,status,href,img

    age = re.search('\d{2,2}',name)
    if not age is None:
        age = int(age.group())
    else:
        age =-1

    T = re.search('T:[0-9][0-9][0-9]',status)
    if not T is None:
        T = int(T.group()[2:5])
    else:
        T = -1
            
    B = GetSize1('B:\d{2,3}',status)
    W = GetSize1('W:\d{2,3}',status)
    H = GetSize1('H:\d{2,3}',status)

    #print T,B,W,H

    if name != "" and age != "" and T > 0 and B > 0 and W > 0 and H > 0:

        result = GetTheoryValue(T,B,W,H)

        scraperwiki.sqlite.save(unique_keys=["name"],data = {
                "name":name,
                "T":T,
                "B":B,
                "W":W,
                "H":H,
                "C":"",
                "Theory_B":result[0],
                "Theory_W":result[1],
                "Theory_H":result[2],
                "Rate":result[3],
                "Direction":result[4],
                "Style":result[5],
                "StyleN":result[6],
                "Level":result[8],
                "LevelN":result[7],
                "info":"",
                "age":age,
                "shop":"funabashi H",
                "image":URL + img,
                "detail":URL + href[1:len(href)]
            } )               



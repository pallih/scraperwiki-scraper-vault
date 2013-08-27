# -*- coding: utf-8 -*-

import scraperwiki
import requests
import urllib2
import re
import urlparse
import lxml.html
import StringIO
from lxml import etree
import datetime
import locale

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
    styleName = ''
    styleValue = 0

    if Rate > 14.5:
        if Direction > 14.5:
            styleName = "gram"
            styleValue  = 3
        else:
            styleName = "nice"
            styleValue = 4
    else:
        if Direction > 14.3:
            styleName = u"寸胴"
            styleValue  = 2
        else:
            styleName = u"すとん"
            styleValue = 1

    # 分類
    nyuValue =  ((B**2) - W) / float(T)
    nyuName = ""
    if nyuValue < 30:
        nyuName = u"無"
    elif 30 <= nyuValue and nyuValue < 38:
        nyuName = u"貧"
    elif 38 <= nyuValue and nyuValue < 45:
        nyuName = u"普"
    elif 45 <= nyuValue and nyuValue < 55:
        nyuName = u"巨"
    elif 55 <= nyuValue and nyuValue < 65:
        nyuName = u"爆"
    elif 65 <= nyuValue:
        nyuName = u"超"

    #                                                スタイル値 スタイル名 nyu値   nyu名
    return Theory_B,Theory_W,Theory_H,Rate,Direction,styleValue,styleName,nyuValue,nyuName
    
def GetDetail(baseURL,shopName):

    html = requests.get(baseURL + 'lady.php')
    
    #lists = re.findall('<div class="cast clear">.*?<p class="prof">.*?</p>',html.content.decode('shift_jis'),re.DOTALL)
    lists = re.findall(u'1人分ここから.*?ここまで',html.content.decode('shift_jis'),re.DOTALL)
    
    for l in lists:
        
        #print l
        if re.search('today.gif',l) is None:
            today = 0
        else:
            today = 1
        

        deTag = re.compile('<.*?>')
        
        # name and years
        wk = re.search('<strong>.*?</strong>',l)
        name = deTag.sub('',wk.group())
    
        T = int(re.search('T[0-9][0-9][0-9]',l).group()[1:4])
        
        wk = re.search('B\d{2,3}',l).group()
        B = int(wk[1:len(wk)])
        
        wk = re.search('W\d{2,3}',l).group()
        W = int(wk[1:len(wk)])
        
        wk = re.search('H\d{2,3}',l).group()
        H = int(wk[1:len(wk)])
        
        # 理論値計算
        result = GetTheoryValue(T,B,W,H)
        
        # personal pages
        detail = baseURL + re.search('detail.php\?id=\d{1,4}',l).group()
        
        # picture
        # [a-z0-9]{32}
        if re.search('cgi3/pict/[a-z0-9]{32}',l) is None:
            pict = ''
        else:
            pict = baseURL + re.search('cgi3/pict/[a-z0-9]{32}',l).group()
        
        #print name,T,B,W,H,detail,pict
    
        # unique_keys = [ 'id' ]
        # data = { 'id':12, 'name':'violet', 'age':7 }
        # scraperwiki.sql.save(unique_keys, data)
    
        #                                                 スタイル値 スタイル名 nyu値   nyu名
    #return Theory_B,Theory_W,Theory_H,Rate,Direction,styleValue,styleName,nyuValue,nyuName

        dataRow = {
            'name' : name,
            'T' : T,
            'B' : B,
            'W' : W,
            'H' : H,
            'detail' : detail,
            'pict' : pict ,
            'tB' : result[0],
            'tW' : result[1],
            'tH' : result[2],
            'rate' : result[3],        # 有効率
            'direction' : result[4],    # 縦横比
            'styleValue' : result[5],   # 値
            'styleName' : result[6],    # 名前
            'nyuValue' : result[7],     # 値
            'nyuName' : result[8],      # 名前
            'shopName' : shopName,
            'today' : today
        }
        
        scraperwiki.sqlite.save(unique_keys=['detail'],data=dataRow)   
    
    
############################################
# MAIN
############################################

# 銀座
GetDetail('http://www.ginza-kagayaki.com/','ginza')

# 新宿
GetDetail('http://www.d-kagayaki.com/','shinjuku')

# 渋谷
GetDetail('http://www.shibuya-kagayaki.com/','shibuya')


    # -*- coding: utf-8 -*-

import scraperwiki
import requests
import urllib2
import re
import urlparse
import lxml.html
import StringIO
from lxml import etree
import datetime
import locale

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
    styleName = ''
    styleValue = 0

    if Rate > 14.5:
        if Direction > 14.5:
            styleName = "gram"
            styleValue  = 3
        else:
            styleName = "nice"
            styleValue = 4
    else:
        if Direction > 14.3:
            styleName = u"寸胴"
            styleValue  = 2
        else:
            styleName = u"すとん"
            styleValue = 1

    # 分類
    nyuValue =  ((B**2) - W) / float(T)
    nyuName = ""
    if nyuValue < 30:
        nyuName = u"無"
    elif 30 <= nyuValue and nyuValue < 38:
        nyuName = u"貧"
    elif 38 <= nyuValue and nyuValue < 45:
        nyuName = u"普"
    elif 45 <= nyuValue and nyuValue < 55:
        nyuName = u"巨"
    elif 55 <= nyuValue and nyuValue < 65:
        nyuName = u"爆"
    elif 65 <= nyuValue:
        nyuName = u"超"

    #                                                スタイル値 スタイル名 nyu値   nyu名
    return Theory_B,Theory_W,Theory_H,Rate,Direction,styleValue,styleName,nyuValue,nyuName
    
def GetDetail(baseURL,shopName):

    html = requests.get(baseURL + 'lady.php')
    
    #lists = re.findall('<div class="cast clear">.*?<p class="prof">.*?</p>',html.content.decode('shift_jis'),re.DOTALL)
    lists = re.findall(u'1人分ここから.*?ここまで',html.content.decode('shift_jis'),re.DOTALL)
    
    for l in lists:
        
        #print l
        if re.search('today.gif',l) is None:
            today = 0
        else:
            today = 1
        

        deTag = re.compile('<.*?>')
        
        # name and years
        wk = re.search('<strong>.*?</strong>',l)
        name = deTag.sub('',wk.group())
    
        T = int(re.search('T[0-9][0-9][0-9]',l).group()[1:4])
        
        wk = re.search('B\d{2,3}',l).group()
        B = int(wk[1:len(wk)])
        
        wk = re.search('W\d{2,3}',l).group()
        W = int(wk[1:len(wk)])
        
        wk = re.search('H\d{2,3}',l).group()
        H = int(wk[1:len(wk)])
        
        # 理論値計算
        result = GetTheoryValue(T,B,W,H)
        
        # personal pages
        detail = baseURL + re.search('detail.php\?id=\d{1,4}',l).group()
        
        # picture
        # [a-z0-9]{32}
        if re.search('cgi3/pict/[a-z0-9]{32}',l) is None:
            pict = ''
        else:
            pict = baseURL + re.search('cgi3/pict/[a-z0-9]{32}',l).group()
        
        #print name,T,B,W,H,detail,pict
    
        # unique_keys = [ 'id' ]
        # data = { 'id':12, 'name':'violet', 'age':7 }
        # scraperwiki.sql.save(unique_keys, data)
    
        #                                                 スタイル値 スタイル名 nyu値   nyu名
    #return Theory_B,Theory_W,Theory_H,Rate,Direction,styleValue,styleName,nyuValue,nyuName

        dataRow = {
            'name' : name,
            'T' : T,
            'B' : B,
            'W' : W,
            'H' : H,
            'detail' : detail,
            'pict' : pict ,
            'tB' : result[0],
            'tW' : result[1],
            'tH' : result[2],
            'rate' : result[3],        # 有効率
            'direction' : result[4],    # 縦横比
            'styleValue' : result[5],   # 値
            'styleName' : result[6],    # 名前
            'nyuValue' : result[7],     # 値
            'nyuName' : result[8],      # 名前
            'shopName' : shopName,
            'today' : today
        }
        
        scraperwiki.sqlite.save(unique_keys=['detail'],data=dataRow)   
    
    
############################################
# MAIN
############################################

# 銀座
GetDetail('http://www.ginza-kagayaki.com/','ginza')

# 新宿
GetDetail('http://www.d-kagayaki.com/','shinjuku')

# 渋谷
GetDetail('http://www.shibuya-kagayaki.com/','shibuya')


    # -*- coding: utf-8 -*-

import scraperwiki
import requests
import urllib2
import re
import urlparse
import lxml.html
import StringIO
from lxml import etree
import datetime
import locale

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
    styleName = ''
    styleValue = 0

    if Rate > 14.5:
        if Direction > 14.5:
            styleName = "gram"
            styleValue  = 3
        else:
            styleName = "nice"
            styleValue = 4
    else:
        if Direction > 14.3:
            styleName = u"寸胴"
            styleValue  = 2
        else:
            styleName = u"すとん"
            styleValue = 1

    # 分類
    nyuValue =  ((B**2) - W) / float(T)
    nyuName = ""
    if nyuValue < 30:
        nyuName = u"無"
    elif 30 <= nyuValue and nyuValue < 38:
        nyuName = u"貧"
    elif 38 <= nyuValue and nyuValue < 45:
        nyuName = u"普"
    elif 45 <= nyuValue and nyuValue < 55:
        nyuName = u"巨"
    elif 55 <= nyuValue and nyuValue < 65:
        nyuName = u"爆"
    elif 65 <= nyuValue:
        nyuName = u"超"

    #                                                スタイル値 スタイル名 nyu値   nyu名
    return Theory_B,Theory_W,Theory_H,Rate,Direction,styleValue,styleName,nyuValue,nyuName
    
def GetDetail(baseURL,shopName):

    html = requests.get(baseURL + 'lady.php')
    
    #lists = re.findall('<div class="cast clear">.*?<p class="prof">.*?</p>',html.content.decode('shift_jis'),re.DOTALL)
    lists = re.findall(u'1人分ここから.*?ここまで',html.content.decode('shift_jis'),re.DOTALL)
    
    for l in lists:
        
        #print l
        if re.search('today.gif',l) is None:
            today = 0
        else:
            today = 1
        

        deTag = re.compile('<.*?>')
        
        # name and years
        wk = re.search('<strong>.*?</strong>',l)
        name = deTag.sub('',wk.group())
    
        T = int(re.search('T[0-9][0-9][0-9]',l).group()[1:4])
        
        wk = re.search('B\d{2,3}',l).group()
        B = int(wk[1:len(wk)])
        
        wk = re.search('W\d{2,3}',l).group()
        W = int(wk[1:len(wk)])
        
        wk = re.search('H\d{2,3}',l).group()
        H = int(wk[1:len(wk)])
        
        # 理論値計算
        result = GetTheoryValue(T,B,W,H)
        
        # personal pages
        detail = baseURL + re.search('detail.php\?id=\d{1,4}',l).group()
        
        # picture
        # [a-z0-9]{32}
        if re.search('cgi3/pict/[a-z0-9]{32}',l) is None:
            pict = ''
        else:
            pict = baseURL + re.search('cgi3/pict/[a-z0-9]{32}',l).group()
        
        #print name,T,B,W,H,detail,pict
    
        # unique_keys = [ 'id' ]
        # data = { 'id':12, 'name':'violet', 'age':7 }
        # scraperwiki.sql.save(unique_keys, data)
    
        #                                                 スタイル値 スタイル名 nyu値   nyu名
    #return Theory_B,Theory_W,Theory_H,Rate,Direction,styleValue,styleName,nyuValue,nyuName

        dataRow = {
            'name' : name,
            'T' : T,
            'B' : B,
            'W' : W,
            'H' : H,
            'detail' : detail,
            'pict' : pict ,
            'tB' : result[0],
            'tW' : result[1],
            'tH' : result[2],
            'rate' : result[3],        # 有効率
            'direction' : result[4],    # 縦横比
            'styleValue' : result[5],   # 値
            'styleName' : result[6],    # 名前
            'nyuValue' : result[7],     # 値
            'nyuName' : result[8],      # 名前
            'shopName' : shopName,
            'today' : today
        }
        
        scraperwiki.sqlite.save(unique_keys=['detail'],data=dataRow)   
    
    
############################################
# MAIN
############################################

# 銀座
GetDetail('http://www.ginza-kagayaki.com/','ginza')

# 新宿
GetDetail('http://www.d-kagayaki.com/','shinjuku')

# 渋谷
GetDetail('http://www.shibuya-kagayaki.com/','shibuya')


    
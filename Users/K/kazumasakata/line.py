import scraperwiki

#!/usr/bin/python
# -*- coding: utf-8 -*-


import re
import glob
import datetime
import locale
import sqlite3
import sys
import traceback
import urllib
import cgi

print "Content-Type: text/plain\n\n"

def fOpen(filename):
    buff = []
    f = open(filename,"r")

    for line in f:
            buff.append(line)
    f.close()
    return ''.join(buff)

################################################################################
# Main
################################################################################

deTag = re.compile('<.*?>')

# 一時格納用のレコード配列
dataRows = []

# ファイル名

html =scraperwiki.scrape('http://line-friends.com/category/woman/page/')

# 必要部分を取得
posts = re.findall('<div class="postmetadata">.*?<p class="admin_del">', html, re.DOTALL)


for post in posts:
    # 空白を除外
    buff = re.sub('\t| ','',post)
    
    # レコード格納用
    dr= {}
    
    # deTag.sub('置換文字列',検索対象文字列変数)
    # deTag部分が正規表現
    
    # 投稿年月日を抽出
    dr["y"] = str(deTag.sub('',re.search('<spanclass="date-year">.*?</span>',buff).group()))
    dr["m"] = str(deTag.sub('',re.search('<spanclass="date-month">.*?</span>',buff).group())).replace('月','')
    dr["d"] = str(deTag.sub('',re.search('<spanclass="date-day">.*?</span>',buff).group()))
    dr["t"] = str(deTag.sub('',re.search('<pclass="posted_time">.*?</p>',buff).group()))
    
    # 投稿内容を抽出
    dr["name"] = deTag.sub('',re.search('<pclass="poster_name">.*?</p>',buff).group())
    dr["age"]  = deTag.sub('',re.search('<pclass="poster_age">.*?</p>',buff).group())
    dr["area"] = deTag.sub('',re.search('<pclass="poster_area">.*?</p>',buff).group())
    
    work = re.search('<pclass="poster_line">.*?readonly/></p>',buff).group()
    work = re.sub('.*"type="text"value="','',work)
    dr["ID"] = re.sub('"readonly/></p>','',work)
    
    dr["txt"]  = deTag.sub('',re.search('<pclass="poster_txt"><p>.*?</p>',buff,re.DOTALL).group())
    
    # 写真
    result = re.search('<imgsrc="http://line-friends.com/uploads/.*?/>',buff)
    if not result is None:
        dr["img"] = re.sub('<imgsrc="|"/>','',result.group())
    else:
        dr["img"] = ""
    
    dataRows.append(dr)
    print dr["ID"]
    


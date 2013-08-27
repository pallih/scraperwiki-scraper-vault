import scraperwiki
import urllib2
import re
import urlparse
import lxml.html
import StringIO
from lxml import etree
import datetime
import locale

# function block
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

def GetAttendance():

    html1 = scraperwiki.scrape("http://www.tora-h-shibuya.jp/schedule.php")

    shops = re.findall('<div class="today">.*?^\t\t\t<div class="clear"></div>', html1 , re.DOTALL)

    for shop in shops:

        print shop

    return 0

def GetDetail(url,regexp,html,shop):

    # 対象URLを指定された正規表現で抽出
    #everyheadline = re.findall(regexp, scraperwiki.scrape(url+"girls.html/"), re.DOTALL)

    everyheadline = re.findall(regexp, html, re.DOTALL)

    deTag = re.compile('<.*?>')
    
    dataRows = []

    for headline in everyheadline:

        s= datetime.datetime.today()
        #print '%s:%s:%s.%d [%s]' % (s.hour, s.minute, s.second, s.microsecond/1000 ,headline)               

        # 名前
        work = re.search('<p class="todaytle">.*?</p>',headline, re.DOTALL)
        name = deTag.sub('',work.group())


        #出勤有無
        if not re.search('<p class="todaytle">' + name + '</p>',attendance , re.DOTALL) is None:
            syukkin = "today"
        else:
            syukkin = ""

    
        # 属性
        work = re.search('<p class="todaytxt">.*?</p>',headline, re.DOTALL)
        attr = deTag.sub('',work.group())#.decode('euc-jp')


        #attr_tiger= re.search(u"[ダイヤモンド|プラチナ|ゴールド]タイガー",attr).group()
        attr_tiger = " "

        attr_T = int(re.search('T[0-9][0-9][0-9]',attr).group()[1:4])
        
        work = re.search('B\d{2,3}',attr).group()
        attr_B = int(work[1:len(work)])

        if not re.search('W\d{2,3}',attr) is None :
            work = re.search('W\d{2,3}',attr).group()
            attr_W = int(work[1:len(work)])
        else :
            attr_W = 999

        if not re.search('H\d{2,3}',attr) is None:
            work = re.search('H\d{2,3}',attr).group()
            attr_H = int(work[1:len(work)])
        else :
            attr_H = 999

        attr_C = re.search('\(.?\)',attr).group()
        de = re.compile('\(|\)')

        attr_C = de.sub('',attr_C)

        # 画像
        #img = url + re.search('girls_img.*jpg',headline).group()
        img = url + re.search('sys_img/tora/cast/.*jpg|images/common/s1.jpg',headline).group()

        # 個人ページ
        #detail = url + re.search('detail.html\?uid=\d{3}',headline).group()
        detail = url + re.search('detail.php\?id=\d{1,3}',headline).group()

        # 理論値計算
        result = GetTheoryValue(attr_T,attr_B,attr_W,attr_H)
    
        # 配列へ移送
        dataRow = {}
        dataRow["name"] = name
        dataRow["T"] = attr_T
        dataRow["B"] = attr_B
        dataRow["W"] = attr_W
        dataRow["H"] = attr_H
        dataRow["C"] = attr_C
        dataRow["Theory_B"] = result[0]
        dataRow["Theory_W"] = result[1]
        dataRow["Theory_H"] = result[2]
        dataRow["Rate"] = result[3]
        dataRow["Direction"] = result[4]
        dataRow["Style"] = result[5]
        dataRow["StyleN"] = result[6]
        dataRow["Level"] = result[8]
        dataRow["LevelN"] = result[7]
        dataRow["info"] = syukkin + " " + attr_tiger
        dataRow["age"] = ""
        dataRow["shop"] = shop
        dataRow["image"] = img
        dataRow["detail"] = detail

        dataRows.append(dataRow)

    # DBに保存
    scraperwiki.sqlite.save(unique_keys=["name","T","B","W","H"],data=dataRows)

#        scraperwiki.sqlite.save(unique_keys=["detail"],data = {
#                "name":name,
#                "T":attr_T,
#                "B":attr_B,
#                "W":attr_W,
#                "H":attr_H,
#                "C":attr_C,
#                "Theory_B":result[0],
#                "Theory_W":result[1],
#                "Theory_H":result[2],
#                "Rate":result[3],
#                "Direction":result[4],
#                "Style":result[5],
#                "StyleN":result[6],
#                "Level":result[8],
#                "LevelN":result[7],
#                "info":attr_tiger,
#                "age":"",
#                "shop":shop,
#                "image":img,
#                "detail":detail
#                } )

#        scraperwiki.sqlite.execute(sql ,[name,
#                                            attr_T,
#                                            attr_B,
#                                            attr_W,
#                                            attr_H,
#                                            attr_C,
#                                            result[0],
#                                            result[1],
#                                            result[2],
#                                            result[3],
#                                            result[4],
#                                            result[5],
#                                            result[6],
#                                            result[8],
#                                            result[7],
#                                            attr_tiger,
#                                            "",
#                                            shop,
#                                            img,
#                                            detail
#                                            ])
        #sql = "insert or replace into swdata values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

    return len(dataRows)


#############################################################################
# Main
#############################################################################

# 出勤情報を保持
attendance = scraperwiki.scrape("http://www.tora-h-shibuya.jp/schedule.php")

urlAoyama = "http://www.tora-ana.jp/"
urlShinjyuku = "http://www.tora-shinjyuku.jp/"
urlIkebukuro = "http://www.tora-ikebukuro.jp/"
urlShibuya = "http://www.tora-h-shibuya.jp/"

# DBクリア
#scraperwiki.sqlite.execute("delete from swdata")

count = 0

# 青山
html = scraperwiki.scrape(urlAoyama +"girls.php/")
count += GetDetail(urlAoyama ,'<div class="box03_new">.*?</div>',html ,"虎(青山)")
count += GetDetail(urlAoyama ,'<div class="box03">.*?</div>',html ,"虎(青山)")

# 新宿
html = scraperwiki.scrape(urlShinjyuku +"girls.php/")
count += GetDetail(urlShinjyuku ,'<div class="box03_new">.*?</div>',html ,"虎(新宿)")
count += GetDetail(urlShinjyuku ,'<div class="box03">.*?</div>',html ,"虎(新宿)")

# 池袋
html = scraperwiki.scrape(urlIkebukuro +"girls.php/")
count += GetDetail(urlIkebukuro ,'<div class="box05_new">.*?</div>',html ,"虎(池袋)")
count += GetDetail(urlIkebukuro ,'<div class="box05">.*?</div>',html ,"虎(池袋)")

# 渋谷
html = scraperwiki.scrape(urlShibuya +"girls.php/")
count += GetDetail(urlShibuya ,'<div class="box06_new">.*?</div>',html ,"虎(渋谷)")
count += GetDetail(urlShibuya ,'<div class="box06">.*?</div>',html ,"虎(渋谷)")

print "HTML取り込み件数=%d DB格納件数=%s" % (count,scraperwiki.sqlite.select("count(*) from swdata"))

#scraperwiki.sqlite.commit()



import scraperwiki
import urllib2
import re
import urlparse
import lxml.html
import StringIO
from lxml import etree
import datetime
import locale

# function block
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

def GetAttendance():

    html1 = scraperwiki.scrape("http://www.tora-h-shibuya.jp/schedule.php")

    shops = re.findall('<div class="today">.*?^\t\t\t<div class="clear"></div>', html1 , re.DOTALL)

    for shop in shops:

        print shop

    return 0

def GetDetail(url,regexp,html,shop):

    # 対象URLを指定された正規表現で抽出
    #everyheadline = re.findall(regexp, scraperwiki.scrape(url+"girls.html/"), re.DOTALL)

    everyheadline = re.findall(regexp, html, re.DOTALL)

    deTag = re.compile('<.*?>')
    
    dataRows = []

    for headline in everyheadline:

        s= datetime.datetime.today()
        #print '%s:%s:%s.%d [%s]' % (s.hour, s.minute, s.second, s.microsecond/1000 ,headline)               

        # 名前
        work = re.search('<p class="todaytle">.*?</p>',headline, re.DOTALL)
        name = deTag.sub('',work.group())


        #出勤有無
        if not re.search('<p class="todaytle">' + name + '</p>',attendance , re.DOTALL) is None:
            syukkin = "today"
        else:
            syukkin = ""

    
        # 属性
        work = re.search('<p class="todaytxt">.*?</p>',headline, re.DOTALL)
        attr = deTag.sub('',work.group())#.decode('euc-jp')


        #attr_tiger= re.search(u"[ダイヤモンド|プラチナ|ゴールド]タイガー",attr).group()
        attr_tiger = " "

        attr_T = int(re.search('T[0-9][0-9][0-9]',attr).group()[1:4])
        
        work = re.search('B\d{2,3}',attr).group()
        attr_B = int(work[1:len(work)])

        if not re.search('W\d{2,3}',attr) is None :
            work = re.search('W\d{2,3}',attr).group()
            attr_W = int(work[1:len(work)])
        else :
            attr_W = 999

        if not re.search('H\d{2,3}',attr) is None:
            work = re.search('H\d{2,3}',attr).group()
            attr_H = int(work[1:len(work)])
        else :
            attr_H = 999

        attr_C = re.search('\(.?\)',attr).group()
        de = re.compile('\(|\)')

        attr_C = de.sub('',attr_C)

        # 画像
        #img = url + re.search('girls_img.*jpg',headline).group()
        img = url + re.search('sys_img/tora/cast/.*jpg|images/common/s1.jpg',headline).group()

        # 個人ページ
        #detail = url + re.search('detail.html\?uid=\d{3}',headline).group()
        detail = url + re.search('detail.php\?id=\d{1,3}',headline).group()

        # 理論値計算
        result = GetTheoryValue(attr_T,attr_B,attr_W,attr_H)
    
        # 配列へ移送
        dataRow = {}
        dataRow["name"] = name
        dataRow["T"] = attr_T
        dataRow["B"] = attr_B
        dataRow["W"] = attr_W
        dataRow["H"] = attr_H
        dataRow["C"] = attr_C
        dataRow["Theory_B"] = result[0]
        dataRow["Theory_W"] = result[1]
        dataRow["Theory_H"] = result[2]
        dataRow["Rate"] = result[3]
        dataRow["Direction"] = result[4]
        dataRow["Style"] = result[5]
        dataRow["StyleN"] = result[6]
        dataRow["Level"] = result[8]
        dataRow["LevelN"] = result[7]
        dataRow["info"] = syukkin + " " + attr_tiger
        dataRow["age"] = ""
        dataRow["shop"] = shop
        dataRow["image"] = img
        dataRow["detail"] = detail

        dataRows.append(dataRow)

    # DBに保存
    scraperwiki.sqlite.save(unique_keys=["name","T","B","W","H"],data=dataRows)

#        scraperwiki.sqlite.save(unique_keys=["detail"],data = {
#                "name":name,
#                "T":attr_T,
#                "B":attr_B,
#                "W":attr_W,
#                "H":attr_H,
#                "C":attr_C,
#                "Theory_B":result[0],
#                "Theory_W":result[1],
#                "Theory_H":result[2],
#                "Rate":result[3],
#                "Direction":result[4],
#                "Style":result[5],
#                "StyleN":result[6],
#                "Level":result[8],
#                "LevelN":result[7],
#                "info":attr_tiger,
#                "age":"",
#                "shop":shop,
#                "image":img,
#                "detail":detail
#                } )

#        scraperwiki.sqlite.execute(sql ,[name,
#                                            attr_T,
#                                            attr_B,
#                                            attr_W,
#                                            attr_H,
#                                            attr_C,
#                                            result[0],
#                                            result[1],
#                                            result[2],
#                                            result[3],
#                                            result[4],
#                                            result[5],
#                                            result[6],
#                                            result[8],
#                                            result[7],
#                                            attr_tiger,
#                                            "",
#                                            shop,
#                                            img,
#                                            detail
#                                            ])
        #sql = "insert or replace into swdata values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

    return len(dataRows)


#############################################################################
# Main
#############################################################################

# 出勤情報を保持
attendance = scraperwiki.scrape("http://www.tora-h-shibuya.jp/schedule.php")

urlAoyama = "http://www.tora-ana.jp/"
urlShinjyuku = "http://www.tora-shinjyuku.jp/"
urlIkebukuro = "http://www.tora-ikebukuro.jp/"
urlShibuya = "http://www.tora-h-shibuya.jp/"

# DBクリア
#scraperwiki.sqlite.execute("delete from swdata")

count = 0

# 青山
html = scraperwiki.scrape(urlAoyama +"girls.php/")
count += GetDetail(urlAoyama ,'<div class="box03_new">.*?</div>',html ,"虎(青山)")
count += GetDetail(urlAoyama ,'<div class="box03">.*?</div>',html ,"虎(青山)")

# 新宿
html = scraperwiki.scrape(urlShinjyuku +"girls.php/")
count += GetDetail(urlShinjyuku ,'<div class="box03_new">.*?</div>',html ,"虎(新宿)")
count += GetDetail(urlShinjyuku ,'<div class="box03">.*?</div>',html ,"虎(新宿)")

# 池袋
html = scraperwiki.scrape(urlIkebukuro +"girls.php/")
count += GetDetail(urlIkebukuro ,'<div class="box05_new">.*?</div>',html ,"虎(池袋)")
count += GetDetail(urlIkebukuro ,'<div class="box05">.*?</div>',html ,"虎(池袋)")

# 渋谷
html = scraperwiki.scrape(urlShibuya +"girls.php/")
count += GetDetail(urlShibuya ,'<div class="box06_new">.*?</div>',html ,"虎(渋谷)")
count += GetDetail(urlShibuya ,'<div class="box06">.*?</div>',html ,"虎(渋谷)")

print "HTML取り込み件数=%d DB格納件数=%s" % (count,scraperwiki.sqlite.select("count(*) from swdata"))

#scraperwiki.sqlite.commit()



import scraperwiki
import urllib2
import re
import urlparse
import lxml.html
import StringIO
from lxml import etree
import datetime
import locale

# function block
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

def GetAttendance():

    html1 = scraperwiki.scrape("http://www.tora-h-shibuya.jp/schedule.php")

    shops = re.findall('<div class="today">.*?^\t\t\t<div class="clear"></div>', html1 , re.DOTALL)

    for shop in shops:

        print shop

    return 0

def GetDetail(url,regexp,html,shop):

    # 対象URLを指定された正規表現で抽出
    #everyheadline = re.findall(regexp, scraperwiki.scrape(url+"girls.html/"), re.DOTALL)

    everyheadline = re.findall(regexp, html, re.DOTALL)

    deTag = re.compile('<.*?>')
    
    dataRows = []

    for headline in everyheadline:

        s= datetime.datetime.today()
        #print '%s:%s:%s.%d [%s]' % (s.hour, s.minute, s.second, s.microsecond/1000 ,headline)               

        # 名前
        work = re.search('<p class="todaytle">.*?</p>',headline, re.DOTALL)
        name = deTag.sub('',work.group())


        #出勤有無
        if not re.search('<p class="todaytle">' + name + '</p>',attendance , re.DOTALL) is None:
            syukkin = "today"
        else:
            syukkin = ""

    
        # 属性
        work = re.search('<p class="todaytxt">.*?</p>',headline, re.DOTALL)
        attr = deTag.sub('',work.group())#.decode('euc-jp')


        #attr_tiger= re.search(u"[ダイヤモンド|プラチナ|ゴールド]タイガー",attr).group()
        attr_tiger = " "

        attr_T = int(re.search('T[0-9][0-9][0-9]',attr).group()[1:4])
        
        work = re.search('B\d{2,3}',attr).group()
        attr_B = int(work[1:len(work)])

        if not re.search('W\d{2,3}',attr) is None :
            work = re.search('W\d{2,3}',attr).group()
            attr_W = int(work[1:len(work)])
        else :
            attr_W = 999

        if not re.search('H\d{2,3}',attr) is None:
            work = re.search('H\d{2,3}',attr).group()
            attr_H = int(work[1:len(work)])
        else :
            attr_H = 999

        attr_C = re.search('\(.?\)',attr).group()
        de = re.compile('\(|\)')

        attr_C = de.sub('',attr_C)

        # 画像
        #img = url + re.search('girls_img.*jpg',headline).group()
        img = url + re.search('sys_img/tora/cast/.*jpg|images/common/s1.jpg',headline).group()

        # 個人ページ
        #detail = url + re.search('detail.html\?uid=\d{3}',headline).group()
        detail = url + re.search('detail.php\?id=\d{1,3}',headline).group()

        # 理論値計算
        result = GetTheoryValue(attr_T,attr_B,attr_W,attr_H)
    
        # 配列へ移送
        dataRow = {}
        dataRow["name"] = name
        dataRow["T"] = attr_T
        dataRow["B"] = attr_B
        dataRow["W"] = attr_W
        dataRow["H"] = attr_H
        dataRow["C"] = attr_C
        dataRow["Theory_B"] = result[0]
        dataRow["Theory_W"] = result[1]
        dataRow["Theory_H"] = result[2]
        dataRow["Rate"] = result[3]
        dataRow["Direction"] = result[4]
        dataRow["Style"] = result[5]
        dataRow["StyleN"] = result[6]
        dataRow["Level"] = result[8]
        dataRow["LevelN"] = result[7]
        dataRow["info"] = syukkin + " " + attr_tiger
        dataRow["age"] = ""
        dataRow["shop"] = shop
        dataRow["image"] = img
        dataRow["detail"] = detail

        dataRows.append(dataRow)

    # DBに保存
    scraperwiki.sqlite.save(unique_keys=["name","T","B","W","H"],data=dataRows)

#        scraperwiki.sqlite.save(unique_keys=["detail"],data = {
#                "name":name,
#                "T":attr_T,
#                "B":attr_B,
#                "W":attr_W,
#                "H":attr_H,
#                "C":attr_C,
#                "Theory_B":result[0],
#                "Theory_W":result[1],
#                "Theory_H":result[2],
#                "Rate":result[3],
#                "Direction":result[4],
#                "Style":result[5],
#                "StyleN":result[6],
#                "Level":result[8],
#                "LevelN":result[7],
#                "info":attr_tiger,
#                "age":"",
#                "shop":shop,
#                "image":img,
#                "detail":detail
#                } )

#        scraperwiki.sqlite.execute(sql ,[name,
#                                            attr_T,
#                                            attr_B,
#                                            attr_W,
#                                            attr_H,
#                                            attr_C,
#                                            result[0],
#                                            result[1],
#                                            result[2],
#                                            result[3],
#                                            result[4],
#                                            result[5],
#                                            result[6],
#                                            result[8],
#                                            result[7],
#                                            attr_tiger,
#                                            "",
#                                            shop,
#                                            img,
#                                            detail
#                                            ])
        #sql = "insert or replace into swdata values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

    return len(dataRows)


#############################################################################
# Main
#############################################################################

# 出勤情報を保持
attendance = scraperwiki.scrape("http://www.tora-h-shibuya.jp/schedule.php")

urlAoyama = "http://www.tora-ana.jp/"
urlShinjyuku = "http://www.tora-shinjyuku.jp/"
urlIkebukuro = "http://www.tora-ikebukuro.jp/"
urlShibuya = "http://www.tora-h-shibuya.jp/"

# DBクリア
#scraperwiki.sqlite.execute("delete from swdata")

count = 0

# 青山
html = scraperwiki.scrape(urlAoyama +"girls.php/")
count += GetDetail(urlAoyama ,'<div class="box03_new">.*?</div>',html ,"虎(青山)")
count += GetDetail(urlAoyama ,'<div class="box03">.*?</div>',html ,"虎(青山)")

# 新宿
html = scraperwiki.scrape(urlShinjyuku +"girls.php/")
count += GetDetail(urlShinjyuku ,'<div class="box03_new">.*?</div>',html ,"虎(新宿)")
count += GetDetail(urlShinjyuku ,'<div class="box03">.*?</div>',html ,"虎(新宿)")

# 池袋
html = scraperwiki.scrape(urlIkebukuro +"girls.php/")
count += GetDetail(urlIkebukuro ,'<div class="box05_new">.*?</div>',html ,"虎(池袋)")
count += GetDetail(urlIkebukuro ,'<div class="box05">.*?</div>',html ,"虎(池袋)")

# 渋谷
html = scraperwiki.scrape(urlShibuya +"girls.php/")
count += GetDetail(urlShibuya ,'<div class="box06_new">.*?</div>',html ,"虎(渋谷)")
count += GetDetail(urlShibuya ,'<div class="box06">.*?</div>',html ,"虎(渋谷)")

print "HTML取り込み件数=%d DB格納件数=%s" % (count,scraperwiki.sqlite.select("count(*) from swdata"))

#scraperwiki.sqlite.commit()




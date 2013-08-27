import scraperwiki

ShowImage = "true"

def GetOverValue(val1,val2):

    result = ""

    # val1 = 実測値
    # val2 = 理論値
    # val1 - val2 > 0 の場合に青字、それ以外は赤字

    if val1 - val2 > 0:
        result = "<td><font color=""blue"">%d(%+.0F)</font></td>" % (val1,val1-val2)
    else:
        result = "<td><font color=""red"">%d(%+.0F)</font></td>" % (val1,val1-val2)


    return str(result)

def GetUnderValue(val1,val2):

    # val1 = 実測値
    # val2 = 理論値
    # val1 - val2 > 0 の場合に赤字、それ以外は青字

    if val1 - val2 < 0:
        result = "<td><font color=""blue"">%d(%+.0F)</font></td>" % (val1,val1-val2)
    else:
        result = "<td><font color=""red"">%d(%+.0F)</font></td>" % (val1,val1-val2)


    return str(result)

scraperwiki.sqlite.attach("kin")
scraperwiki.sqlite.attach("toranoana_1")
scraperwiki.sqlite.attach("h")

#select = "name,T,B,W,H,C,Theory_B,Theory_W,Theory_H,Rate,Direction,Style,Level,LevelN,shop,info,image,detail from \
#(select name,T,B,W,H,C,Theory_B,Theory_W,Theory_H,Rate,Direction,Style,StyleN,Level,LevelN,shop,info,image,detail from kin.swdata \
# union \
# select name,T,B,W,H,C,Theory_B,Theory_W,Theory_H,Rate,Direction,Style,StyleN,Level,LevelN,shop,info,image,detail from toranoana_1.swdata \
# union \
# select name,T,B,W,H,C,Theory_B,Theory_W,Theory_H,Rate,Direction,Style,StyleN,Level,LevelN,shop,info,image,detail from h.swdata ) "

select = "name,T,B,W,H,C,Theory_B,Theory_W,Theory_H,Rate,Direction,Style,Level,LevelN,shop,info,image,detail from \
(select name,T,B,W,H,C,Theory_B,Theory_W,Theory_H,Rate,Direction,Style,StyleN,Level,LevelN,shop,info,image,detail from toranoana_1.swdata \
 where name in ('りか','るい','れんな','リオナ','リエ','りく','りこ','リナ','リノ','りのあ','りょう','るあん','るる','れいこ','れな','レミ')) "

where = ""


order = "order by StyleN desc,LevelN desc,Rate desc,T desc"
#order = "order by LevelN desc,StyleN desc,T desc"
sql = select + order

print "<html>"
print "<head>"
print "<STYLE TYPE=""text/css"">"
print "<!--table{font-size:8pt;}-->"
print "</STYLE>"
print "</head>"
print "<body>"
print '<div><table border="1" cellpadding="0">'
print "<tr>"
print "<th>","NO","</th>"
print "<th>","name","</th>"
print "<th>","image","</th>"
print "<th>","T","</th>"
print "<th>","B","</th>"
print "<th>","W","</th>"
print "<th>","H","</th>"
#print "<th>","理論値(B)","</th>"
#print "<th>","理論値(W)","</th>"
#print "<th>","理論値(H)","</th>"
print "<th>","スタイル","</th>"
print "<th>","分類","</th>"
print "<th>","nyu","</th>"
print "<th>","有効率","</th>"
print "<th>","縦横比","</th>"
print "<th>","店","</th>"
print "<th>","","</th>"
print "</tr>"

cnt = 1



for row in scraperwiki.sqlite.select(sql):
    
    buff = []
    
    buff.append("<tr>")

    buff.append("<td>")
    buff.append(str(cnt))
    buff.append("</td>")
    
    buff.append("<td>")
    buff.append(row["name"])
    buff.append("</td>")

    # 画像表示切替
    if ShowImage == "true":
        buff.append('<td><a href="' + row["detail"] + '"><img src="' + row["image"] + '" width="50%" height="50%"></a></td>')
    else:
        buff.append("<td></td>")

    buff.append("<td>" + str(row["T"]) + "</td>")
    buff.append(GetOverValue(row["B"],row["Theory_B"]))
    buff.append(GetUnderValue(row["W"],row["Theory_W"]))
    buff.append(GetOverValue(row["H"],row["Theory_H"]))

#    print("<td>%d(%.2F)</td>" % (row["B"],row["B"]-row["Theory_B"]))
#    print("<td>%d(%.2F)</td>" % (row["W"],row["W"]-row["Theory_W"]))
#    print("<td>%d(%.2F)</td>" % (row["H"],row["H"]-row["Theory_H"]))

#    print "<td>",row["B"],"</td>"
#    print "<td>",row["W"],"</td>"
#    print "<td>",row["H"],"</td>"
#    print "<td>",row["Theory_B"],"</td>"
#    print "<td>",row["Theory_W"],"</td>"
#    print "<td>",row["Theory_H"],"</td>"

    buff.append("<td>"+row["Style"]+"</td>")
    buff.append("<td>"+row["Level"]+"</td>")
    buff.append(("<td>%.2F</td>" % row["LevelN"]))
    buff.append(("<td>%.2F</td>" % row["Rate"]))
    buff.append(("<td>%.2F</td>" % row["Direction"]))
    buff.append("<td>"+row["shop"]+"</td>")
    buff.append("<td>"+row["info"]+"</td>")
    
    buff.append("</tr>")

    s = ''.join(buff)

    print s

    cnt=cnt+1

print "</table></div>"
print "</body>"
print "</html>"


import scraperwiki

ShowImage = "true"

def GetOverValue(val1,val2):

    result = ""

    # val1 = 実測値
    # val2 = 理論値
    # val1 - val2 > 0 の場合に青字、それ以外は赤字

    if val1 - val2 > 0:
        result = "<td><font color=""blue"">%d(%+.0F)</font></td>" % (val1,val1-val2)
    else:
        result = "<td><font color=""red"">%d(%+.0F)</font></td>" % (val1,val1-val2)


    return str(result)

def GetUnderValue(val1,val2):

    # val1 = 実測値
    # val2 = 理論値
    # val1 - val2 > 0 の場合に赤字、それ以外は青字

    if val1 - val2 < 0:
        result = "<td><font color=""blue"">%d(%+.0F)</font></td>" % (val1,val1-val2)
    else:
        result = "<td><font color=""red"">%d(%+.0F)</font></td>" % (val1,val1-val2)


    return str(result)

scraperwiki.sqlite.attach("kin")
scraperwiki.sqlite.attach("toranoana_1")
scraperwiki.sqlite.attach("h")

#select = "name,T,B,W,H,C,Theory_B,Theory_W,Theory_H,Rate,Direction,Style,Level,LevelN,shop,info,image,detail from \
#(select name,T,B,W,H,C,Theory_B,Theory_W,Theory_H,Rate,Direction,Style,StyleN,Level,LevelN,shop,info,image,detail from kin.swdata \
# union \
# select name,T,B,W,H,C,Theory_B,Theory_W,Theory_H,Rate,Direction,Style,StyleN,Level,LevelN,shop,info,image,detail from toranoana_1.swdata \
# union \
# select name,T,B,W,H,C,Theory_B,Theory_W,Theory_H,Rate,Direction,Style,StyleN,Level,LevelN,shop,info,image,detail from h.swdata ) "

select = "name,T,B,W,H,C,Theory_B,Theory_W,Theory_H,Rate,Direction,Style,Level,LevelN,shop,info,image,detail from \
(select name,T,B,W,H,C,Theory_B,Theory_W,Theory_H,Rate,Direction,Style,StyleN,Level,LevelN,shop,info,image,detail from toranoana_1.swdata \
 where name in ('りか','るい','れんな','リオナ','リエ','りく','りこ','リナ','リノ','りのあ','りょう','るあん','るる','れいこ','れな','レミ')) "

where = ""


order = "order by StyleN desc,LevelN desc,Rate desc,T desc"
#order = "order by LevelN desc,StyleN desc,T desc"
sql = select + order

print "<html>"
print "<head>"
print "<STYLE TYPE=""text/css"">"
print "<!--table{font-size:8pt;}-->"
print "</STYLE>"
print "</head>"
print "<body>"
print '<div><table border="1" cellpadding="0">'
print "<tr>"
print "<th>","NO","</th>"
print "<th>","name","</th>"
print "<th>","image","</th>"
print "<th>","T","</th>"
print "<th>","B","</th>"
print "<th>","W","</th>"
print "<th>","H","</th>"
#print "<th>","理論値(B)","</th>"
#print "<th>","理論値(W)","</th>"
#print "<th>","理論値(H)","</th>"
print "<th>","スタイル","</th>"
print "<th>","分類","</th>"
print "<th>","nyu","</th>"
print "<th>","有効率","</th>"
print "<th>","縦横比","</th>"
print "<th>","店","</th>"
print "<th>","","</th>"
print "</tr>"

cnt = 1



for row in scraperwiki.sqlite.select(sql):
    
    buff = []
    
    buff.append("<tr>")

    buff.append("<td>")
    buff.append(str(cnt))
    buff.append("</td>")
    
    buff.append("<td>")
    buff.append(row["name"])
    buff.append("</td>")

    # 画像表示切替
    if ShowImage == "true":
        buff.append('<td><a href="' + row["detail"] + '"><img src="' + row["image"] + '" width="50%" height="50%"></a></td>')
    else:
        buff.append("<td></td>")

    buff.append("<td>" + str(row["T"]) + "</td>")
    buff.append(GetOverValue(row["B"],row["Theory_B"]))
    buff.append(GetUnderValue(row["W"],row["Theory_W"]))
    buff.append(GetOverValue(row["H"],row["Theory_H"]))

#    print("<td>%d(%.2F)</td>" % (row["B"],row["B"]-row["Theory_B"]))
#    print("<td>%d(%.2F)</td>" % (row["W"],row["W"]-row["Theory_W"]))
#    print("<td>%d(%.2F)</td>" % (row["H"],row["H"]-row["Theory_H"]))

#    print "<td>",row["B"],"</td>"
#    print "<td>",row["W"],"</td>"
#    print "<td>",row["H"],"</td>"
#    print "<td>",row["Theory_B"],"</td>"
#    print "<td>",row["Theory_W"],"</td>"
#    print "<td>",row["Theory_H"],"</td>"

    buff.append("<td>"+row["Style"]+"</td>")
    buff.append("<td>"+row["Level"]+"</td>")
    buff.append(("<td>%.2F</td>" % row["LevelN"]))
    buff.append(("<td>%.2F</td>" % row["Rate"]))
    buff.append(("<td>%.2F</td>" % row["Direction"]))
    buff.append("<td>"+row["shop"]+"</td>")
    buff.append("<td>"+row["info"]+"</td>")
    
    buff.append("</tr>")

    s = ''.join(buff)

    print s

    cnt=cnt+1

print "</table></div>"
print "</body>"
print "</html>"


import scraperwiki

ShowImage = "true"

def GetOverValue(val1,val2):

    result = ""

    # val1 = 実測値
    # val2 = 理論値
    # val1 - val2 > 0 の場合に青字、それ以外は赤字

    if val1 - val2 > 0:
        result = "<td><font color=""blue"">%d(%+.0F)</font></td>" % (val1,val1-val2)
    else:
        result = "<td><font color=""red"">%d(%+.0F)</font></td>" % (val1,val1-val2)


    return str(result)

def GetUnderValue(val1,val2):

    # val1 = 実測値
    # val2 = 理論値
    # val1 - val2 > 0 の場合に赤字、それ以外は青字

    if val1 - val2 < 0:
        result = "<td><font color=""blue"">%d(%+.0F)</font></td>" % (val1,val1-val2)
    else:
        result = "<td><font color=""red"">%d(%+.0F)</font></td>" % (val1,val1-val2)


    return str(result)

scraperwiki.sqlite.attach("kin")
scraperwiki.sqlite.attach("toranoana_1")
scraperwiki.sqlite.attach("h")

#select = "name,T,B,W,H,C,Theory_B,Theory_W,Theory_H,Rate,Direction,Style,Level,LevelN,shop,info,image,detail from \
#(select name,T,B,W,H,C,Theory_B,Theory_W,Theory_H,Rate,Direction,Style,StyleN,Level,LevelN,shop,info,image,detail from kin.swdata \
# union \
# select name,T,B,W,H,C,Theory_B,Theory_W,Theory_H,Rate,Direction,Style,StyleN,Level,LevelN,shop,info,image,detail from toranoana_1.swdata \
# union \
# select name,T,B,W,H,C,Theory_B,Theory_W,Theory_H,Rate,Direction,Style,StyleN,Level,LevelN,shop,info,image,detail from h.swdata ) "

select = "name,T,B,W,H,C,Theory_B,Theory_W,Theory_H,Rate,Direction,Style,Level,LevelN,shop,info,image,detail from \
(select name,T,B,W,H,C,Theory_B,Theory_W,Theory_H,Rate,Direction,Style,StyleN,Level,LevelN,shop,info,image,detail from toranoana_1.swdata \
 where name in ('りか','るい','れんな','リオナ','リエ','りく','りこ','リナ','リノ','りのあ','りょう','るあん','るる','れいこ','れな','レミ')) "

where = ""


order = "order by StyleN desc,LevelN desc,Rate desc,T desc"
#order = "order by LevelN desc,StyleN desc,T desc"
sql = select + order

print "<html>"
print "<head>"
print "<STYLE TYPE=""text/css"">"
print "<!--table{font-size:8pt;}-->"
print "</STYLE>"
print "</head>"
print "<body>"
print '<div><table border="1" cellpadding="0">'
print "<tr>"
print "<th>","NO","</th>"
print "<th>","name","</th>"
print "<th>","image","</th>"
print "<th>","T","</th>"
print "<th>","B","</th>"
print "<th>","W","</th>"
print "<th>","H","</th>"
#print "<th>","理論値(B)","</th>"
#print "<th>","理論値(W)","</th>"
#print "<th>","理論値(H)","</th>"
print "<th>","スタイル","</th>"
print "<th>","分類","</th>"
print "<th>","nyu","</th>"
print "<th>","有効率","</th>"
print "<th>","縦横比","</th>"
print "<th>","店","</th>"
print "<th>","","</th>"
print "</tr>"

cnt = 1



for row in scraperwiki.sqlite.select(sql):
    
    buff = []
    
    buff.append("<tr>")

    buff.append("<td>")
    buff.append(str(cnt))
    buff.append("</td>")
    
    buff.append("<td>")
    buff.append(row["name"])
    buff.append("</td>")

    # 画像表示切替
    if ShowImage == "true":
        buff.append('<td><a href="' + row["detail"] + '"><img src="' + row["image"] + '" width="50%" height="50%"></a></td>')
    else:
        buff.append("<td></td>")

    buff.append("<td>" + str(row["T"]) + "</td>")
    buff.append(GetOverValue(row["B"],row["Theory_B"]))
    buff.append(GetUnderValue(row["W"],row["Theory_W"]))
    buff.append(GetOverValue(row["H"],row["Theory_H"]))

#    print("<td>%d(%.2F)</td>" % (row["B"],row["B"]-row["Theory_B"]))
#    print("<td>%d(%.2F)</td>" % (row["W"],row["W"]-row["Theory_W"]))
#    print("<td>%d(%.2F)</td>" % (row["H"],row["H"]-row["Theory_H"]))

#    print "<td>",row["B"],"</td>"
#    print "<td>",row["W"],"</td>"
#    print "<td>",row["H"],"</td>"
#    print "<td>",row["Theory_B"],"</td>"
#    print "<td>",row["Theory_W"],"</td>"
#    print "<td>",row["Theory_H"],"</td>"

    buff.append("<td>"+row["Style"]+"</td>")
    buff.append("<td>"+row["Level"]+"</td>")
    buff.append(("<td>%.2F</td>" % row["LevelN"]))
    buff.append(("<td>%.2F</td>" % row["Rate"]))
    buff.append(("<td>%.2F</td>" % row["Direction"]))
    buff.append("<td>"+row["shop"]+"</td>")
    buff.append("<td>"+row["info"]+"</td>")
    
    buff.append("</tr>")

    s = ''.join(buff)

    print s

    cnt=cnt+1

print "</table></div>"
print "</body>"
print "</html>"



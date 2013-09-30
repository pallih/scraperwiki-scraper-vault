import scraperwiki
import re
import urllib
import cgi


ShowImage = "true"
ShowOnlyAttendance = "false"


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

################################################################################
# Main
################################################################################

# POST処理
form = cgi.FieldStorage()
if form.has_key("q1") and form.has_key("q2"):
    # 両方あるときのみパラメータを変更

    # 画像表示
    if form["q1"].value == "yes":
        ShowImage = "true"
    else:
        ShowImage = "false"

    # 出勤のみ
    if form["q2"].value == "yes":
        ShowOnlyAttendance = "true"
    else:
        ShowOnlyAttendance = "false"
else:
    # 上記以外は初期値と見なす。
    ShowImage = "true"
    ShowOnlyAttendance = "false"



scraperwiki.sqlite.attach("kagayaki")

sql = "name, T, B || '(' || round(B-tB,2) || ')' as B, W || '(' || round(W-tW,2) || ')' as W, H || '(' || round(H-tH,2) || ')' as H, detail, pict, styleName, nyuName, styleValue, nyuValue, rate, direction, today,shopName from kagayaki.swdata where today = 1 order by styleValue desc,nyuValue desc,T desc"

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
    

#    if row["today"] == 1:
#        buff.append('<tr bgcolor="#6495ed">')
#    else:
#        #buff.append("<tr>")
#        continue

    buff.append("<td>")
    buff.append(str(cnt))
    buff.append("</td>")
    
    buff.append("<td>")
    buff.append(row["name"])
    buff.append("</td>")

    # 画像表示切替
    buff.append('<td><a href="' + row["detail"] + '" target="_blank"><img src="' + row["pict"] + '" width="60" height="96"></a></td>')


    buff.append("<td>" + str(row["T"]) + "</td>")
    buff.append("<td>" + str(row["B"]) + "</td>")
    buff.append("<td>" + str(row["W"]) + "</td>")
    buff.append("<td>" + str(row["H"]) + "</td>")

    buff.append("<td>"+row["styleName"]+"</td>")
    buff.append("<td>"+row["nyuName"]+"</td>")
    buff.append(("<td>%.2F</td>" % row["nyuValue"]))
    buff.append(("<td>%.2F</td>" % row["rate"]))
    buff.append(("<td>%.2F</td>" % row["direction"]))
    buff.append("<td>"+row["shopName"]+"</td>")
    buff.append("<td>"+"</td>")
    
    buff.append("</tr>")

    s = ''.join(buff)

    print s

    cnt=cnt+1

print "</table></div>"
print "</body>"
print "</html>"



import scraperwiki
import re
import urllib
import cgi


ShowImage = "true"
ShowOnlyAttendance = "false"


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

################################################################################
# Main
################################################################################

# POST処理
form = cgi.FieldStorage()
if form.has_key("q1") and form.has_key("q2"):
    # 両方あるときのみパラメータを変更

    # 画像表示
    if form["q1"].value == "yes":
        ShowImage = "true"
    else:
        ShowImage = "false"

    # 出勤のみ
    if form["q2"].value == "yes":
        ShowOnlyAttendance = "true"
    else:
        ShowOnlyAttendance = "false"
else:
    # 上記以外は初期値と見なす。
    ShowImage = "true"
    ShowOnlyAttendance = "false"



scraperwiki.sqlite.attach("kagayaki")

sql = "name, T, B || '(' || round(B-tB,2) || ')' as B, W || '(' || round(W-tW,2) || ')' as W, H || '(' || round(H-tH,2) || ')' as H, detail, pict, styleName, nyuName, styleValue, nyuValue, rate, direction, today,shopName from kagayaki.swdata where today = 1 order by styleValue desc,nyuValue desc,T desc"

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
    

#    if row["today"] == 1:
#        buff.append('<tr bgcolor="#6495ed">')
#    else:
#        #buff.append("<tr>")
#        continue

    buff.append("<td>")
    buff.append(str(cnt))
    buff.append("</td>")
    
    buff.append("<td>")
    buff.append(row["name"])
    buff.append("</td>")

    # 画像表示切替
    buff.append('<td><a href="' + row["detail"] + '" target="_blank"><img src="' + row["pict"] + '" width="60" height="96"></a></td>')


    buff.append("<td>" + str(row["T"]) + "</td>")
    buff.append("<td>" + str(row["B"]) + "</td>")
    buff.append("<td>" + str(row["W"]) + "</td>")
    buff.append("<td>" + str(row["H"]) + "</td>")

    buff.append("<td>"+row["styleName"]+"</td>")
    buff.append("<td>"+row["nyuName"]+"</td>")
    buff.append(("<td>%.2F</td>" % row["nyuValue"]))
    buff.append(("<td>%.2F</td>" % row["rate"]))
    buff.append(("<td>%.2F</td>" % row["direction"]))
    buff.append("<td>"+row["shopName"]+"</td>")
    buff.append("<td>"+"</td>")
    
    buff.append("</tr>")

    s = ''.join(buff)

    print s

    cnt=cnt+1

print "</table></div>"
print "</body>"
print "</html>"



import scraperwiki
import re
import urllib
import cgi


ShowImage = "true"
ShowOnlyAttendance = "false"


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

################################################################################
# Main
################################################################################

# POST処理
form = cgi.FieldStorage()
if form.has_key("q1") and form.has_key("q2"):
    # 両方あるときのみパラメータを変更

    # 画像表示
    if form["q1"].value == "yes":
        ShowImage = "true"
    else:
        ShowImage = "false"

    # 出勤のみ
    if form["q2"].value == "yes":
        ShowOnlyAttendance = "true"
    else:
        ShowOnlyAttendance = "false"
else:
    # 上記以外は初期値と見なす。
    ShowImage = "true"
    ShowOnlyAttendance = "false"



scraperwiki.sqlite.attach("kagayaki")

sql = "name, T, B || '(' || round(B-tB,2) || ')' as B, W || '(' || round(W-tW,2) || ')' as W, H || '(' || round(H-tH,2) || ')' as H, detail, pict, styleName, nyuName, styleValue, nyuValue, rate, direction, today,shopName from kagayaki.swdata where today = 1 order by styleValue desc,nyuValue desc,T desc"

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
    

#    if row["today"] == 1:
#        buff.append('<tr bgcolor="#6495ed">')
#    else:
#        #buff.append("<tr>")
#        continue

    buff.append("<td>")
    buff.append(str(cnt))
    buff.append("</td>")
    
    buff.append("<td>")
    buff.append(row["name"])
    buff.append("</td>")

    # 画像表示切替
    buff.append('<td><a href="' + row["detail"] + '" target="_blank"><img src="' + row["pict"] + '" width="60" height="96"></a></td>')


    buff.append("<td>" + str(row["T"]) + "</td>")
    buff.append("<td>" + str(row["B"]) + "</td>")
    buff.append("<td>" + str(row["W"]) + "</td>")
    buff.append("<td>" + str(row["H"]) + "</td>")

    buff.append("<td>"+row["styleName"]+"</td>")
    buff.append("<td>"+row["nyuName"]+"</td>")
    buff.append(("<td>%.2F</td>" % row["nyuValue"]))
    buff.append(("<td>%.2F</td>" % row["rate"]))
    buff.append(("<td>%.2F</td>" % row["direction"]))
    buff.append("<td>"+row["shopName"]+"</td>")
    buff.append("<td>"+"</td>")
    
    buff.append("</tr>")

    s = ''.join(buff)

    print s

    cnt=cnt+1

print "</table></div>"
print "</body>"
print "</html>"



import scraperwiki
import re
import urllib
import cgi


ShowImage = "true"
ShowOnlyAttendance = "false"


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

################################################################################
# Main
################################################################################

# POST処理
form = cgi.FieldStorage()
if form.has_key("q1") and form.has_key("q2"):
    # 両方あるときのみパラメータを変更

    # 画像表示
    if form["q1"].value == "yes":
        ShowImage = "true"
    else:
        ShowImage = "false"

    # 出勤のみ
    if form["q2"].value == "yes":
        ShowOnlyAttendance = "true"
    else:
        ShowOnlyAttendance = "false"
else:
    # 上記以外は初期値と見なす。
    ShowImage = "true"
    ShowOnlyAttendance = "false"



scraperwiki.sqlite.attach("kagayaki")

sql = "name, T, B || '(' || round(B-tB,2) || ')' as B, W || '(' || round(W-tW,2) || ')' as W, H || '(' || round(H-tH,2) || ')' as H, detail, pict, styleName, nyuName, styleValue, nyuValue, rate, direction, today,shopName from kagayaki.swdata where today = 1 order by styleValue desc,nyuValue desc,T desc"

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
    

#    if row["today"] == 1:
#        buff.append('<tr bgcolor="#6495ed">')
#    else:
#        #buff.append("<tr>")
#        continue

    buff.append("<td>")
    buff.append(str(cnt))
    buff.append("</td>")
    
    buff.append("<td>")
    buff.append(row["name"])
    buff.append("</td>")

    # 画像表示切替
    buff.append('<td><a href="' + row["detail"] + '" target="_blank"><img src="' + row["pict"] + '" width="60" height="96"></a></td>')


    buff.append("<td>" + str(row["T"]) + "</td>")
    buff.append("<td>" + str(row["B"]) + "</td>")
    buff.append("<td>" + str(row["W"]) + "</td>")
    buff.append("<td>" + str(row["H"]) + "</td>")

    buff.append("<td>"+row["styleName"]+"</td>")
    buff.append("<td>"+row["nyuName"]+"</td>")
    buff.append(("<td>%.2F</td>" % row["nyuValue"]))
    buff.append(("<td>%.2F</td>" % row["rate"]))
    buff.append(("<td>%.2F</td>" % row["direction"]))
    buff.append("<td>"+row["shopName"]+"</td>")
    buff.append("<td>"+"</td>")
    
    buff.append("</tr>")

    s = ''.join(buff)

    print s

    cnt=cnt+1

print "</table></div>"
print "</body>"
print "</html>"




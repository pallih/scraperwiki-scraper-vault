import scraperwiki           
scraperwiki.sqlite.attach("mobilebooster_list")

data = scraperwiki.sqlite.select(           
    '''* from mobilebooster_list.compatibility'''
)

print """
<html>
<head>
  <style type="text/css">
/* ------------------
 styling for the tables 
   ------------------   */


body
{
    line-height: 1.6em;
}

#hor-minimalist-a
{
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;
    background: #f0f0f0;
    margin: 15px;
    border-collapse: collapse;
    text-align: left;
}
#hor-minimalist-a th
{
    font-size: 14px;
    font-weight: normal;
    color: #039;
    padding: 10px 8px;
    border-bottom: 2px solid #6678b1;
}
#hor-minimalist-a td
{
    color: #669;
    padding: 9px 8px 0px 8px;
}
#hor-minimalist-a tbody tr:hover td
{
    color: #009;
}


#hor-minimalist-b
{
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;
    background: #fff;
    margin: 45px;
    width: 480px;
    border-collapse: collapse;
    text-align: left;
}
#hor-minimalist-b th
{
    font-size: 14px;
    font-weight: normal;
    color: #039;
    padding: 10px 8px;
    border-bottom: 2px solid #6678b1;
}
#hor-minimalist-b td
{
    border-bottom: 1px solid #ccc;
    color: #669;
    padding: 6px 8px;
}
#hor-minimalist-b tbody tr:hover td
{
    color: #009;
}


#ver-minimalist
{
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;
    margin: 45px;
    width: 480px;
    text-align: left;
    border-collapse: collapse;
}
#ver-minimalist th
{
    padding: 8px 2px;
    font-weight: normal;
    font-size: 14px;
    border-bottom: 2px solid #6678b1;
    border-right: 30px solid #fff;
    border-left: 30px solid #fff;
    color: #039;
}
#ver-minimalist td
{
    padding: 12px 2px 0px 2px;
    border-right: 30px solid #fff;
    border-left: 30px solid #fff;
    color: #669;
}


#box-table-a
{
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;
    margin: 45px;
    width: 480px;
    text-align: left;
    border-collapse: collapse;
}
#box-table-a th
{
    font-size: 13px;
    font-weight: normal;
    padding: 8px;
    background: #b9c9fe;
    border-top: 4px solid #aabcfe;
    border-bottom: 1px solid #fff;
    color: #039;
}
#box-table-a td
{
    padding: 8px;
    background: #e8edff; 
    border-bottom: 1px solid #fff;
    color: #669;
    border-top: 1px solid transparent;
}
#box-table-a tr:hover td
{
    background: #d0dafd;
    color: #339;
}


#box-table-b
{
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;
    margin: 45px;
    width: 480px;
    text-align: center;
    border-collapse: collapse;
    border-top: 7px solid #9baff1;
    border-bottom: 7px solid #9baff1;
}
#box-table-b th
{
    font-size: 13px;
    font-weight: normal;
    padding: 8px;
    background: #e8edff;
    border-right: 1px solid #9baff1;
    border-left: 1px solid #9baff1;
    color: #039;
}
#box-table-b td
{
    padding: 8px;
    background: #e8edff; 
    border-right: 1px solid #aabcfe;
    border-left: 1px solid #aabcfe;
    color: #669;
}


#hor-zebra
{
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;
    margin: 45px;
    width: 480px;
    text-align: left;
    border-collapse: collapse;
}
#hor-zebra th
{
    font-size: 14px;
    font-weight: normal;
    padding: 10px 8px;
    color: #039;
}
#hor-zebra td
{
    padding: 8px;
    color: #669;
}
#hor-zebra .odd
{
    background: #e8edff; 
}


#ver-zebra
{
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;
    margin: 45px;
    width: 480px;
    text-align: left;
    border-collapse: collapse;
}
#ver-zebra th
{
    font-size: 14px;
    font-weight: normal;
    padding: 12px 15px;
    border-right: 1px solid #fff;
    border-left: 1px solid #fff;
    color: #039;
}
#ver-zebra td
{
    padding: 8px 15px;
    border-right: 1px solid #fff;
    border-left: 1px solid #fff;
    color: #669;
}
.vzebra-odd
{
    background: #eff2ff;
}
.vzebra-even
{
    background: #e8edff;
}
#ver-zebra #vzebra-adventure, #ver-zebra #vzebra-children
{
    background: #d0dafd;
    border-bottom: 1px solid #c8d4fd;
}
#ver-zebra #vzebra-comedy, #ver-zebra #vzebra-action
{
    background: #dce4ff;
    border-bottom: 1px solid #d6dfff;
}


#one-column-emphasis
{
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;
    margin: 45px;
    width: 480px;
    text-align: left;
    border-collapse: collapse;
}
#one-column-emphasis th
{
    font-size: 14px;
    font-weight: normal;
    padding: 12px 15px;
    color: #039;
}
#one-column-emphasis td
{
    padding: 10px 15px;
    color: #669;
    border-top: 1px solid #e8edff;
}
.oce-first
{
    background: #d0dafd;
    border-right: 10px solid transparent;
    border-left: 10px solid transparent;
}
#one-column-emphasis tr:hover td
{
    color: #339;
    background: #eff2ff;
}


#newspaper-a
{
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;
    margin: 45px;
    width: 480px;
    text-align: left;
    border-collapse: collapse;
    border: 1px solid #69c;
}
#newspaper-a th
{
    padding: 12px 17px 12px 17px;
    font-weight: normal;
    font-size: 14px;
    color: #039;
    border-bottom: 1px dashed #69c;
}
#newspaper-a td
{
    padding: 7px 17px 7px 17px;
    color: #669;
}
#newspaper-a tbody tr:hover td
{
    color: #339;
    background: #d0dafd;
}


#newspaper-b
{
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;
    margin: 45px;
    width: 480px;
    text-align: left;
    border-collapse: collapse;
    border: 1px solid #69c;
}
#newspaper-b th
{
    padding: 15px 10px 10px 10px;
    font-weight: normal;
    font-size: 14px;
    color: #039;
}
#newspaper-b tbody
{
    background: #e8edff;
}
#newspaper-b td
{
    padding: 10px;
    color: #669;
    border-top: 1px dashed #fff;
}
#newspaper-b tbody tr:hover td
{
    color: #339;
    background: #d0dafd;
}


#newspaper-c
{
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;
    margin: 45px;
    width: 480px;
    text-align: left;
    border-collapse: collapse;
    border: 1px solid #6cf;
}
#newspaper-c th
{
    padding: 20px;
    font-weight: normal;
    font-size: 13px;
    color: #039;
    text-transform: uppercase;
    border-right: 1px solid #0865c2;
    border-top: 1px solid #0865c2;
    border-left: 1px solid #0865c2;
    border-bottom: 1px solid #fff;
}
#newspaper-c td
{
    padding: 10px 20px;
    color: #669;
    border-right: 1px dashed #6cf;
}


#rounded-corner
{
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;
    margin: 45px;
    width: 480px;
    text-align: left;
    border-collapse: collapse;
}
#rounded-corner thead th.rounded-company
{
    background: #b9c9fe url('table-images/left.png') left -1px no-repeat;
}
#rounded-corner thead th.rounded-q4
{
    background: #b9c9fe url('table-images/right.png') right -1px no-repeat;
}
#rounded-corner th
{
    padding: 8px;
    font-weight: normal;
    font-size: 13px;
    color: #039;
    background: #b9c9fe;
}
#rounded-corner td
{
    padding: 8px;
    background: #e8edff;
    border-top: 1px solid #fff;
    color: #669;
}
#rounded-corner tfoot td.rounded-foot-left
{
    background: #e8edff url('table-images/botleft.png') left bottom no-repeat;
}
#rounded-corner tfoot td.rounded-foot-right
{
    background: #e8edff url('table-images/botright.png') right bottom no-repeat;
}
#rounded-corner tbody tr:hover td
{
    background: #d0dafd;
}


#background-image
{
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;
    margin: 45px;
    width: 480px;
    text-align: left;
    border-collapse: collapse;
    background: url('table-images/blurry.jpg') 330px 59px no-repeat;
}
#background-image th
{
    padding: 12px;
    font-weight: normal;
    font-size: 14px;
    color: #339;
}
#background-image td
{
    padding: 9px 12px;
    color: #669;
    border-top: 1px solid #fff;
}
#background-image tfoot td
{
    font-size: 11px;
}
#background-image tbody td
{
    background: url('table-images/back.png');
}
* html #background-image tbody td
{
    /* 
       ----------------------------
        PUT THIS ON IE6 ONLY STYLE 
        AS THE RULE INVALIDATES
        YOUR STYLESHEET
       ----------------------------
    */
    filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(src='table-images/back.png',sizingMethod='crop');
    background: none;
}    
#background-image tbody tr:hover td
{
    color: #339;
    background: none;
}


#gradient-style
{
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;
    margin: 45px;
    width: 480px;
    text-align: left;
    border-collapse: collapse;
}
#gradient-style th
{
    font-size: 13px;
    font-weight: normal;
    padding: 8px;
    background: #b9c9fe url('table-images/gradhead.png') repeat-x;
    border-top: 2px solid #d3ddff;
    border-bottom: 1px solid #fff;
    color: #039;
}
#gradient-style td
{
    padding: 8px; 
    border-bottom: 1px solid #fff;
    color: #669;
    border-top: 1px solid #fff;
    background: #e8edff url('table-images/gradback.png') repeat-x;
}
#gradient-style tfoot tr td
{
    background: #e8edff;
    font-size: 12px;
    color: #99c;
}
#gradient-style tbody tr:hover td
{
    background: #d0dafd url('table-images/gradhover.png') repeat-x;
    color: #339;
}


#pattern-style-a
{
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;
    margin: 45px;
    width: 480px;
    text-align: left;
    border-collapse: collapse;
    background: url('table-images/pattern.png');
}
#pattern-style-a thead tr
{
    background: url('table-images/pattern-head.png');
}
#pattern-style-a th
{
    font-size: 13px;
    font-weight: normal;
    padding: 8px;
    border-bottom: 1px solid #fff;
    color: #039;
}
#pattern-style-a td
{
    padding: 8px; 
    border-bottom: 1px solid #fff;
    color: #669;
    border-top: 1px solid transparent;
}
#pattern-style-a tbody tr:hover td
{
    color: #339;
    background: #fff;
}


#pattern-style-b
{
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;
    margin: 45px;
    width: 480px;
    text-align: left;
    border-collapse: collapse;
    background: url('table-images/patternb.png');
}
#pattern-style-b thead tr
{
    background: url('table-images/patternb-head.png');
}
#pattern-style-b th
{
    font-size: 13px;
    font-weight: normal;
    padding: 8px;
    border-bottom: 1px solid #fff;
    color: #039;
}
#pattern-style-b td
{
    padding: 8px; 
    border-bottom: 1px solid #fff;
    color: #669;
    border-top: 1px solid transparent;
}
#pattern-style-b tbody tr:hover td
{
    color: #339;
    background: #cdcdee;
}
  </style>
</head>
"""

print """
<body>
"""

count = 0

print "<table id='hor-minimalist-a'>"           
print "<tr>"
print "<th>大カテゴリ</th><th>中カテゴリ</th><th>小カテゴリ</th><th>デバイス名</th><th>前提</th>"
print "<th>KBC-L54D</th><th>KBC-L27D</th><th>KBC-L2BS</th><th>KBC-D1AS</th><th>KBC-L2AS</th><th>KBC-L3AS</th><th>KBC-E1AS</th><th>KBC-D1BS</th><th>KBC-DS2AS</th><th>KBC-DS3AS</th>"
print "<th>最終更新日</th><th>URL</th>"
for d in data:
    print "<tr>"
    print "<td font-size='xx-small'>", d["cat0"][:4], "</td>"
    print "<td>", d["cat1"], "</td>"
    print "<td>", d["cat2"], "</td>"
    print "<td>", d["device"], "</td>"
    print "<td>", d["precondition_text "], "</td>"
    print "<td>", d["KBC-L54D"], "</td>"
    print "<td>", d["KBC-L27D"], "</td>"
    print "<td>", d["KBC-L2BS"], "</td>"
    print "<td>", d["KBC-D1AS"], "</td>"
    print "<td>", d["KBC-L2AS"], "</td>"
    print "<td>", d["KBC-L3AS"], "</td>"
    print "<td>", d["KBC-E1AS"], "</td>"
    print "<td>", d["KBC-D1BS"], "</td>"
    print "<td>", d["KBC-DS2AS"], "</td>"
    print "<td>", d["KBC-DS3AS"], "</td>"
    print "<td>", d["lastDateChecked"][:11], "</td>"
    print "<td><a href='", d["url"], "'>link</a></td>"
    print "</tr>"

    count += 1
    #if count > 10:
    #    break
print "</table>"

print """
</body>
</html>
"""
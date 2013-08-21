#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite

sourcescraper = 'bay_tv_liverpool'
limit = 32
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata limit ? offset ?", (limit, offset))
keys = sdata.get("keys")
rows = sdata.get("data")

print '<style type="text/css">'
print 'div #scraperwikipane { display:none; background:none; border:none; }'
print 'a #scraperwikipane { display:none; background:none; border:none; }'
print '</style>'

print '<table class="joblist" style="border-collapse:collapse">'


# rows
rownum = 1
column = 1
repeated = 1

for row in rows:
    if repeated == 1:
        if column == 1:
            print "<tr>",
        if rownum == 1:
            rownum = 2;
        else:
            rownum = 1;
    if rownum == 2:
        if repeated == 1:
            if column == 1:
                linkfull = "target='_blank' href='http://baytvliverpool.com/vod/index.php" + row.pop(0) + "' title='View video'"
                imgfull = '<img border="0" src="http://baytvliverpool.com/vod/thumbs/' + row.pop(0) + "/>"

                imgfull2 = imgfull[:(imgfull.find('width="') + 7)]
                imgfull2end = imgfull[(imgfull.find('width="') + 11):]
                imgfull3 = imgfull2 + '190"' + imgfull2end   

                imgfull4 = imgfull3[:(imgfull3.find('height="') + 8)]
                imgfull4end = imgfull3[(imgfull3.find('height="') + 12):]
                imgfull5 = imgfull4 + '104"' + imgfull4end             

                imgfull5.lstrip()
                linkfull.lstrip()
                print "<td style='text-align:center; background-color:#F6F6F6; padding:5px 5px 5px 5px; '><a", linkfull, '>', imgfull5, "</a></td>"
            if column == 2:
                linkfull = "target='_blank' href='http://baytvliverpool.com/vod/index.php" + row.pop(0) + "' title='View video'"
                imgfull = '<img border="0" src="http://baytvliverpool.com/vod/thumbs/' + row.pop(0) + "/>"

                imgfull2 = imgfull[:(imgfull.find('width="') + 7)]
                imgfull2end = imgfull[(imgfull.find('width="') + 11):]
                imgfull3 = imgfull2 + '190"' + imgfull2end   

                imgfull4 = imgfull3[:(imgfull3.find('height="') + 8)]
                imgfull4end = imgfull3[(imgfull3.find('height="') + 12):]
                imgfull5 = imgfull4 + '104"' + imgfull4end             

                imgfull5.lstrip()
                linkfull.lstrip()
                print "<td style='text-align:center; background-color:#E8E8E8; padding:5px 5px 5px 5px; '><a", linkfull, '>', imgfull5, "</a></td>"
            if column == 3:
                linkfull = "target='_blank' href='http://baytvliverpool.com/vod/index.php" + row.pop(0) + "' title='View video'"
                imgfull = '<img border="0" src="http://baytvliverpool.com/vod/thumbs/' + row.pop(0) + "/>"

                imgfull2 = imgfull[:(imgfull.find('width="') + 7)]
                imgfull2end = imgfull[(imgfull.find('width="') + 11):]
                imgfull3 = imgfull2 + '190"' + imgfull2end   

                imgfull4 = imgfull3[:(imgfull3.find('height="') + 8)]
                imgfull4end = imgfull3[(imgfull3.find('height="') + 12):]
                imgfull5 = imgfull4 + '104"' + imgfull4end             

                imgfull5.lstrip()
                linkfull.lstrip()
                print "<td style='text-align:center; background-color:#F6F6F6; padding:5px 5px 5px 5px; '><a", linkfull, '>', imgfull5, "</a></td>"
        

    else:
        if repeated == 1:
            if column == 1:
                linkfull = "target='_blank' href='http://baytvliverpool.com/vod/index.php" + row.pop(0) + "' title='View video'"
                imgfull = '<img border="0" src="http://baytvliverpool.com/vod/thumbs/' + row.pop(0) + "/>"

                imgfull2 = imgfull[:(imgfull.find('width="') + 7)]
                imgfull2end = imgfull[(imgfull.find('width="') + 11):]
                imgfull3 = imgfull2 + '190"' + imgfull2end   

                imgfull4 = imgfull3[:(imgfull3.find('height="') + 8)]
                imgfull4end = imgfull3[(imgfull3.find('height="') + 12):]
                imgfull5 = imgfull4 + '104"' + imgfull4end             

                imgfull5.lstrip()
                linkfull.lstrip()
                print "<td style='text-align:center; background-color:#FEFEFE; padding:5px 5px 5px 5px; '><a", linkfull, '>', imgfull5, "</a></td>"
            if column == 2:
                linkfull = "target='_blank' href='http://baytvliverpool.com/vod/index.php" + row.pop(0) + "' title='View video'"
                imgfull = '<img border="0" src="http://baytvliverpool.com/vod/thumbs/' + row.pop(0) + "/>"

                imgfull2 = imgfull[:(imgfull.find('width="') + 7)]
                imgfull2end = imgfull[(imgfull.find('width="') + 11):]
                imgfull3 = imgfull2 + '190"' + imgfull2end   

                imgfull4 = imgfull3[:(imgfull3.find('height="') + 8)]
                imgfull4end = imgfull3[(imgfull3.find('height="') + 12):]
                imgfull5 = imgfull4 + '104"' + imgfull4end             

                imgfull5.lstrip()
                linkfull.lstrip()
                print "<td style='text-align:center; background-color:#F0F0F0; padding:5px 5px 5px 5px; '><a", linkfull, '>', imgfull5, "</a></td>"
            if column == 3:
                linkfull = "target='_blank' href='http://baytvliverpool.com/vod/index.php" + row.pop(0) + "' title='View video'"
                imgfull = '<img border="0" src="http://baytvliverpool.com/vod/thumbs/' + row.pop(0) + "/>"

                imgfull2 = imgfull[:(imgfull.find('width="') + 7)]
                imgfull2end = imgfull[(imgfull.find('width="') + 11):]
                imgfull3 = imgfull2 + '190"' + imgfull2end   

                imgfull4 = imgfull3[:(imgfull3.find('height="') + 8)]
                imgfull4end = imgfull3[(imgfull3.find('height="') + 12):]
                imgfull5 = imgfull4 + '104"' + imgfull4end             

                imgfull5.lstrip()
                linkfull.lstrip()
                print "<td style='text-align:center; background-color:#FEFEFE; padding:5px 5px 5px 5px; '><a", linkfull, '>', imgfull5, "</a></td>"
    if repeated == 1:
        if column == 3:
            print "</tr>"
            column = 0
        column = int(float(column)) + 1
        repeated = 2;
    elif repeated == 2:
        repeated = 1;
if column <> 1:
    print "</tr>"
print "</table>"
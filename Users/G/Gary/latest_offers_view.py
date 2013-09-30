#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite

sourcescraper = "latest_offers"
limit = 51
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata limit ? offset ?", (limit, offset))
keys = sdata.get("keys")
rows = sdata.get("data")

print '<style type="text/css">'
print 'div #scraperwikipane { display:none; background:none; border:none; }'
print 'a #scraperwikipane { display:none; }'
print '</style>'


print '<table class="joblist" style="border-collapse:collapse">'

# column headings
print '<tr>',

print '''<th style="color:white; padding: 10px 30px 10px 30px; text-align:center; font-weight:bold; font-size:1.6em; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">Company</td>'''
print '''<th style="color:white; padding: 10px 30px 10px 30px; text-align:center; font-weight:bold; font-size:1.6em; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">Logo</td>'''
print '''<th style="color:white; padding: 10px 30px 10px 30px; text-align:center; font-weight:bold; font-size:1.6em; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">Donation</td>'''

print "</tr>"

# rows
rownum = 1
rowprogress = 1
for row in rows:
    print "<tr>",
    if rownum == 1:
        rownum = 2;
    else:
        rownum = 1;
    if rownum == 2:
            
            logo = row.pop(0)
            company = row.pop(0)
            link = row.pop(0)
            donation = row.pop(0)

            print "<td style='text-align:center; font-weight:bold; background-color:#B99292; padding:5px 5px 5px 5px; '><a href='" + link + "' title='" + company + "' target='_blank' style='color:white;'>", company, "</a></td>"
            print "<td style='text-align:center; background-color:#F6F6F6; padding:5px 5px 5px 5px; '><a href='" + link + "' title='" + company + "' target='_blank'>", logo, "</a></td>"
            print "<td style='text-align:center; background-color:#E8E8E8; padding:5px 5px 5px 5px;'>", donation, "</td>"
            
    else:

            logo = row.pop(0)
            company = row.pop(0)
            link = row.pop(0)
            donation = row.pop(0)

            print "<td style='text-align:center; font-weight:bold; background-color:#D99E9E; padding:5px 5px 5px 5px; '><a href='" + link + "' title='" + company + "' target='_blank' style='color:white;'>", company, "</a></td>"
            print "<td style='text-align:center; background-color:#FEFEFE; padding:5px 5px 5px 5px; '><a href='" + link + "' title='" + company + "' target='_blank'>", logo, "</a></td>"
            print "<td style='text-align:center; background-color:#F0F0F0; padding:5px 5px 5px 5px;'>", donation, "</td>"
            
    print "</tr>"
    rowprogress = int(float(rowprogress)) + 1
print "</table>"#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite

sourcescraper = "latest_offers"
limit = 51
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata limit ? offset ?", (limit, offset))
keys = sdata.get("keys")
rows = sdata.get("data")

print '<style type="text/css">'
print 'div #scraperwikipane { display:none; background:none; border:none; }'
print 'a #scraperwikipane { display:none; }'
print '</style>'


print '<table class="joblist" style="border-collapse:collapse">'

# column headings
print '<tr>',

print '''<th style="color:white; padding: 10px 30px 10px 30px; text-align:center; font-weight:bold; font-size:1.6em; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">Company</td>'''
print '''<th style="color:white; padding: 10px 30px 10px 30px; text-align:center; font-weight:bold; font-size:1.6em; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">Logo</td>'''
print '''<th style="color:white; padding: 10px 30px 10px 30px; text-align:center; font-weight:bold; font-size:1.6em; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">Donation</td>'''

print "</tr>"

# rows
rownum = 1
rowprogress = 1
for row in rows:
    print "<tr>",
    if rownum == 1:
        rownum = 2;
    else:
        rownum = 1;
    if rownum == 2:
            
            logo = row.pop(0)
            company = row.pop(0)
            link = row.pop(0)
            donation = row.pop(0)

            print "<td style='text-align:center; font-weight:bold; background-color:#B99292; padding:5px 5px 5px 5px; '><a href='" + link + "' title='" + company + "' target='_blank' style='color:white;'>", company, "</a></td>"
            print "<td style='text-align:center; background-color:#F6F6F6; padding:5px 5px 5px 5px; '><a href='" + link + "' title='" + company + "' target='_blank'>", logo, "</a></td>"
            print "<td style='text-align:center; background-color:#E8E8E8; padding:5px 5px 5px 5px;'>", donation, "</td>"
            
    else:

            logo = row.pop(0)
            company = row.pop(0)
            link = row.pop(0)
            donation = row.pop(0)

            print "<td style='text-align:center; font-weight:bold; background-color:#D99E9E; padding:5px 5px 5px 5px; '><a href='" + link + "' title='" + company + "' target='_blank' style='color:white;'>", company, "</a></td>"
            print "<td style='text-align:center; background-color:#FEFEFE; padding:5px 5px 5px 5px; '><a href='" + link + "' title='" + company + "' target='_blank'>", logo, "</a></td>"
            print "<td style='text-align:center; background-color:#F0F0F0; padding:5px 5px 5px 5px;'>", donation, "</td>"
            
    print "</tr>"
    rowprogress = int(float(rowprogress)) + 1
print "</table>"
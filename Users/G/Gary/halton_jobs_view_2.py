#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite

sourcescraper = "halton_jobs_2"
limit = 31
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata limit ? offset ?", (limit, offset))
keys = sdata.get("keys")
rows = sdata.get("data")

print '<table class="joblist" style="border-collapse:collapse">'

# column headings
print '<tr>',

print '''<th style="color:white; padding: 10px 30px 10px 30px; text-align:center; font-weight:bold; font-size:1.6em; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">Job Title</td>'''
print '''<th style="color:white; padding: 10px 30px 10px 30px; text-align:center; font-weight:bold; font-size:1.6em; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">Salary</td>'''
print '''<th style="color:white; padding: 10px 30px 10px 30px; text-align:center; font-weight:bold; font-size:1.6em; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">Location</td>'''
print '''<th style="color:white; padding: 10px 30px 10px 30px; text-align:center; font-weight:bold; font-size:1.6em; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">Type</td>'''
print '''<th style="color:white; padding: 10px 30px 10px 30px; text-align:center; font-weight:bold; font-size:1.6em; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">Company</td>'''

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
            if rowprogress > 20:
                title = row.pop(1) + "</a>"
                titlestart = title[:(title.find('ref="') + 5)]
                titleend = title[(title.find('ref="') + 5):]
                titleedit2 = titlestart + 'http://www.reed.co.uk' + titleend
                titlestart2 = titleedit2[:(titleedit2.find('href='))]
                titleend2 = titleedit2[(titleedit2.find('href=')):]
                titlefull2 = titlestart2 + 'target="_blank" title="View this job" style="color:white; text-decoration:underline;" ' + titleend2
                titlefull2.lstrip()
            
                print '<td style="text-align:center; font-weight:bold; color:white; background-color:#B99292; padding:5px 5px 5px 5px; ">', titlefull2, '</td>'

            else:
                title = row.pop(1) + "</a>"
                titlestart = title[:(title.find('ref="') + 5)]
                titleend = title[(title.find('ref="') + 5):]
                titleedit2 = titlestart + 'http://www.totaljobs.com' + titleend
                titlestart2 = titleedit2[:(titleedit2.find('href='))]
                titleend2 = titleedit2[(titleedit2.find('href=')):]
                titlefull2 = titlestart2 + 'target="_blank" title="View this job" style="color:white; text-decoration:underline;" ' + titleend2
                titlefull2.lstrip()
            
                print '<td style="text-align:center; font-weight:bold; color:white; background-color:#B99292; padding:5px 5px 5px 5px; ">', titlefull2, '</td>'

            print "<td style='text-align:center; background-color:#F6F6F6; padding:5px 5px 5px 5px; '>", row.pop(0), "</td>"
            print "<td style='text-align:center; background-color:#E8E8E8; padding:5px 5px 5px 5px;'>", row.pop(2), "</td>"
            print "<td style='text-align:center; background-color:#F6F6F6; padding:5px 5px 5px 5px;'>", row.pop(0), "</td>"

            if rowprogress > 20:
                companyname = row.pop(0)
                companyname2 = companyname
                companyname2.replace (" ", "+")
                linkname = "href='http://www.reed.co.uk/job/searchresults.aspx?k=" + companyname2 + "&jto=false&s=&l=Halton%2C+Cheshire&lp=5&ms=From&mxs=To&st=5&ns=true&da=8630'"
                linkname.lstrip()
                print "<td style='text-align:center; background-color:#E8E8E8; padding:5px 5px 5px 5px;'><a style='text-decoration:none;' title='View jobs from this company'", linkname, ">", companyname, "</a></td>"

            else:
                company = row.pop(0)
                companyedit = company[4:]
                companystart = companyedit[:(companyedit.find('ref="') + 5)]
                companyend = companyedit[(companyedit.find('ref="') + 5):]
                companyedit2 = companystart + 'http://www.totaljobs.com' + companyend
                companystart2 = companyedit2[:(companyedit.find('title='))]
                companyend2 = companyedit2[(companyedit.find('title=')):]
                companyfull2 = companystart2 + 'target="_blank" title="View jobs from this company" style="text-decoration:none; ' + companyend2   
                companyfull2.lstrip()
                companyfull = companyfull2[:-5]

                print "<td style='text-align:center; background-color:#E8E8E8; padding:5px 5px 5px 5px;'>", companyfull, "</td>"

    else:
            if rowprogress > 20:
                title = row.pop(1) + "</a>"
                titlestart = title[:(title.find('ref="') + 5)]
                titleend = title[(title.find('ref="') + 5):]
                titleedit2 = titlestart + 'http://www.reed.co.uk' + titleend
                titlestart2 = titleedit2[:(titleedit2.find('href='))]
                titleend2 = titleedit2[(titleedit2.find('href=')):]
                titlefull2 = titlestart2 + 'target="_blank" title="View this job" style="color:white; text-decoration:underline;" ' + titleend2
                titlefull2.lstrip()
            
                print '<td style="text-align:center; font-weight:bold; color:white; background-color:#D99E9E; padding:5px 5px 5px 5px; ">', titlefull2, '</td>'

            else:
                title = row.pop(1) + "</a>"
                titlestart = title[:(title.find('ref="') + 5)]
                titleend = title[(title.find('ref="') + 5):]
                titleedit2 = titlestart + 'http://www.totaljobs.com' + titleend
                titlestart2 = titleedit2[:(titleedit2.find('href='))]
                titleend2 = titleedit2[(titleedit2.find('href=')):]
                titlefull2 = titlestart2 + 'target="_blank" title="View this job" style="color:white; text-decoration:underline;" ' + titleend2
                titlefull2.lstrip()

                print "<td style='text-align:center; font-weight:bold; color:white; background-color:#D99E9E; padding:5px 5px 5px 5px;'>", titlefull2, "</td>"
            print "<td style='text-align:center; background-color:#FEFEFE; padding:5px 5px 5px 5px;'>", row.pop(0), "</td>"
            print "<td style='text-align:center; background-color:#F0F0F0; padding:5px 5px 5px 5px;'>", row.pop(2), "</td>"
            print "<td style='text-align:center; background-color:#FEFEFE; padding:5px 5px 5px 5px;'>", row.pop(0), "</td>"

            if rowprogress > 20:
                companyname = row.pop(0)
                companyname2 = companyname
                companyname2.replace (" ", "+")
                linkname = "href='http://www.reed.co.uk/job/searchresults.aspx?k=" + companyname2 + "&jto=false&s=&l=Halton%2C+Cheshire&lp=5&ms=From&mxs=To&st=5&ns=true&da=8630'"
                linkname.lstrip()
                print "<td style='text-align:center; background-color:#F0F0F0; padding:5px 5px 5px 5px;'><a style='text-decoration:none;' title='View jobs from this company'", linkname, ">", companyname, "</a></td>"

            else:
                company = row.pop(0)
                companyedit = company[4:]
                companystart = companyedit[:(companyedit.find('ref="') + 5)]
                companyend = companyedit[(companyedit.find('ref="') + 5):]
                companyedit2 = companystart + 'http://www.totaljobs.com' + companyend
                companystart2 = companyedit2[:(companyedit.find('title='))]
                companyend2 = companyedit2[(companyedit.find('title=')):]
                companyfull2 = companystart2 + 'target="_blank" title="View jobs from this company" style="text-decoration:none; ' + companyend2   
                companyfull2.lstrip()
                companyfull = companyfull2[:-5]

                print "<td style='text-align:center; background-color:#F0F0F0; padding:5px 5px 5px 5px;'>", companyfull, "</td>"

    print "</tr>"
    rowprogress = int(float(rowprogress)) + 1
print "</table>"
print '''<div style="padding:10px 10px 10px 10px; margin-top:-2px; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">'''
print "</div>"#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite

sourcescraper = "halton_jobs_2"
limit = 31
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata limit ? offset ?", (limit, offset))
keys = sdata.get("keys")
rows = sdata.get("data")

print '<table class="joblist" style="border-collapse:collapse">'

# column headings
print '<tr>',

print '''<th style="color:white; padding: 10px 30px 10px 30px; text-align:center; font-weight:bold; font-size:1.6em; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">Job Title</td>'''
print '''<th style="color:white; padding: 10px 30px 10px 30px; text-align:center; font-weight:bold; font-size:1.6em; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">Salary</td>'''
print '''<th style="color:white; padding: 10px 30px 10px 30px; text-align:center; font-weight:bold; font-size:1.6em; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">Location</td>'''
print '''<th style="color:white; padding: 10px 30px 10px 30px; text-align:center; font-weight:bold; font-size:1.6em; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">Type</td>'''
print '''<th style="color:white; padding: 10px 30px 10px 30px; text-align:center; font-weight:bold; font-size:1.6em; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">Company</td>'''

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
            if rowprogress > 20:
                title = row.pop(1) + "</a>"
                titlestart = title[:(title.find('ref="') + 5)]
                titleend = title[(title.find('ref="') + 5):]
                titleedit2 = titlestart + 'http://www.reed.co.uk' + titleend
                titlestart2 = titleedit2[:(titleedit2.find('href='))]
                titleend2 = titleedit2[(titleedit2.find('href=')):]
                titlefull2 = titlestart2 + 'target="_blank" title="View this job" style="color:white; text-decoration:underline;" ' + titleend2
                titlefull2.lstrip()
            
                print '<td style="text-align:center; font-weight:bold; color:white; background-color:#B99292; padding:5px 5px 5px 5px; ">', titlefull2, '</td>'

            else:
                title = row.pop(1) + "</a>"
                titlestart = title[:(title.find('ref="') + 5)]
                titleend = title[(title.find('ref="') + 5):]
                titleedit2 = titlestart + 'http://www.totaljobs.com' + titleend
                titlestart2 = titleedit2[:(titleedit2.find('href='))]
                titleend2 = titleedit2[(titleedit2.find('href=')):]
                titlefull2 = titlestart2 + 'target="_blank" title="View this job" style="color:white; text-decoration:underline;" ' + titleend2
                titlefull2.lstrip()
            
                print '<td style="text-align:center; font-weight:bold; color:white; background-color:#B99292; padding:5px 5px 5px 5px; ">', titlefull2, '</td>'

            print "<td style='text-align:center; background-color:#F6F6F6; padding:5px 5px 5px 5px; '>", row.pop(0), "</td>"
            print "<td style='text-align:center; background-color:#E8E8E8; padding:5px 5px 5px 5px;'>", row.pop(2), "</td>"
            print "<td style='text-align:center; background-color:#F6F6F6; padding:5px 5px 5px 5px;'>", row.pop(0), "</td>"

            if rowprogress > 20:
                companyname = row.pop(0)
                companyname2 = companyname
                companyname2.replace (" ", "+")
                linkname = "href='http://www.reed.co.uk/job/searchresults.aspx?k=" + companyname2 + "&jto=false&s=&l=Halton%2C+Cheshire&lp=5&ms=From&mxs=To&st=5&ns=true&da=8630'"
                linkname.lstrip()
                print "<td style='text-align:center; background-color:#E8E8E8; padding:5px 5px 5px 5px;'><a style='text-decoration:none;' title='View jobs from this company'", linkname, ">", companyname, "</a></td>"

            else:
                company = row.pop(0)
                companyedit = company[4:]
                companystart = companyedit[:(companyedit.find('ref="') + 5)]
                companyend = companyedit[(companyedit.find('ref="') + 5):]
                companyedit2 = companystart + 'http://www.totaljobs.com' + companyend
                companystart2 = companyedit2[:(companyedit.find('title='))]
                companyend2 = companyedit2[(companyedit.find('title=')):]
                companyfull2 = companystart2 + 'target="_blank" title="View jobs from this company" style="text-decoration:none; ' + companyend2   
                companyfull2.lstrip()
                companyfull = companyfull2[:-5]

                print "<td style='text-align:center; background-color:#E8E8E8; padding:5px 5px 5px 5px;'>", companyfull, "</td>"

    else:
            if rowprogress > 20:
                title = row.pop(1) + "</a>"
                titlestart = title[:(title.find('ref="') + 5)]
                titleend = title[(title.find('ref="') + 5):]
                titleedit2 = titlestart + 'http://www.reed.co.uk' + titleend
                titlestart2 = titleedit2[:(titleedit2.find('href='))]
                titleend2 = titleedit2[(titleedit2.find('href=')):]
                titlefull2 = titlestart2 + 'target="_blank" title="View this job" style="color:white; text-decoration:underline;" ' + titleend2
                titlefull2.lstrip()
            
                print '<td style="text-align:center; font-weight:bold; color:white; background-color:#D99E9E; padding:5px 5px 5px 5px; ">', titlefull2, '</td>'

            else:
                title = row.pop(1) + "</a>"
                titlestart = title[:(title.find('ref="') + 5)]
                titleend = title[(title.find('ref="') + 5):]
                titleedit2 = titlestart + 'http://www.totaljobs.com' + titleend
                titlestart2 = titleedit2[:(titleedit2.find('href='))]
                titleend2 = titleedit2[(titleedit2.find('href=')):]
                titlefull2 = titlestart2 + 'target="_blank" title="View this job" style="color:white; text-decoration:underline;" ' + titleend2
                titlefull2.lstrip()

                print "<td style='text-align:center; font-weight:bold; color:white; background-color:#D99E9E; padding:5px 5px 5px 5px;'>", titlefull2, "</td>"
            print "<td style='text-align:center; background-color:#FEFEFE; padding:5px 5px 5px 5px;'>", row.pop(0), "</td>"
            print "<td style='text-align:center; background-color:#F0F0F0; padding:5px 5px 5px 5px;'>", row.pop(2), "</td>"
            print "<td style='text-align:center; background-color:#FEFEFE; padding:5px 5px 5px 5px;'>", row.pop(0), "</td>"

            if rowprogress > 20:
                companyname = row.pop(0)
                companyname2 = companyname
                companyname2.replace (" ", "+")
                linkname = "href='http://www.reed.co.uk/job/searchresults.aspx?k=" + companyname2 + "&jto=false&s=&l=Halton%2C+Cheshire&lp=5&ms=From&mxs=To&st=5&ns=true&da=8630'"
                linkname.lstrip()
                print "<td style='text-align:center; background-color:#F0F0F0; padding:5px 5px 5px 5px;'><a style='text-decoration:none;' title='View jobs from this company'", linkname, ">", companyname, "</a></td>"

            else:
                company = row.pop(0)
                companyedit = company[4:]
                companystart = companyedit[:(companyedit.find('ref="') + 5)]
                companyend = companyedit[(companyedit.find('ref="') + 5):]
                companyedit2 = companystart + 'http://www.totaljobs.com' + companyend
                companystart2 = companyedit2[:(companyedit.find('title='))]
                companyend2 = companyedit2[(companyedit.find('title=')):]
                companyfull2 = companystart2 + 'target="_blank" title="View jobs from this company" style="text-decoration:none; ' + companyend2   
                companyfull2.lstrip()
                companyfull = companyfull2[:-5]

                print "<td style='text-align:center; background-color:#F0F0F0; padding:5px 5px 5px 5px;'>", companyfull, "</td>"

    print "</tr>"
    rowprogress = int(float(rowprogress)) + 1
print "</table>"
print '''<div style="padding:10px 10px 10px 10px; margin-top:-2px; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">'''
print "</div>"
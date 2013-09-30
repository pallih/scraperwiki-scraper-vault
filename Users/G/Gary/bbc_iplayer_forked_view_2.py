import scraperwiki

scraperwiki.sqlite.attach('bbc_iplayer_forked') 

films = scraperwiki.sqlite.select('* from `bbc_iplayer_forked`.swdata')

print "<table class='bbc-iplayer-films'>"
print "<tr>"
print '''<th style="-webkit-border-radius: 99px;-moz-border-radius: 99px;border-radius: 99px;color:white; padding: 10px 30px 10px 30px; text-align:center; font-weight:bold; font-size:1.6em; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">Current BBC iPlayer Films</td>'''
print "</tr>"

oddrow = 1
for film in films:
    if oddrow == 1:
        print "<tr><td style='-webkit-border-radius: 99px;-moz-border-radius: 99px;border-radius: 99px;text-align:center; font-weight:bold; padding:5px 5px 5px 5px; background-color:#B99292; color:white;' class='bbc-iplayer-film'><a style='color:white;' href='" + film['href'] + "' title='" + film['title'] + "'>" + film['title'] + "</a></td></tr>"
        oddrow = 2
    else:
        print "<tr><td style='-webkit-border-radius: 99px;-moz-border-radius: 99px;border-radius: 99px;text-align:center; font-weight:bold; padding:5px 5px 5px 5px; background-color:#D99E9E; color:white;' class='bbc-iplayer-film'><a style='color:white;' href='" + film['href'] + "' title='" + film['title'] + "'>" + film['title'] + "</a></td></tr>"
        oddrow = 1
print "</table>"

import scraperwiki

scraperwiki.sqlite.attach('bbc_iplayer_forked') 

films = scraperwiki.sqlite.select('* from `bbc_iplayer_forked`.swdata')

print "<table class='bbc-iplayer-films'>"
print "<tr>"
print '''<th style="-webkit-border-radius: 99px;-moz-border-radius: 99px;border-radius: 99px;color:white; padding: 10px 30px 10px 30px; text-align:center; font-weight:bold; font-size:1.6em; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDEyOSw1OCw1OCwxKTsiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjpyZ2JhKDE4OSwxNTIsMTUyLDEpOyIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCBmaWxsPSJ1cmwoI2dyYWRpZW50KSIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgLz48L3N2Zz4=);
background: -o-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -moz-linear-gradient(top, rgba(129,58,58,1), rgba(189,152,152,1)); background: -webkit-gradient(linear, left top, left bottom, color-stop(0, rgba(129,58,58,1)), color-stop(1, rgba(189,152,152,1)));
filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898);
-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#FF813A3A,EndColorStr=#FFBD9898)";">Current BBC iPlayer Films</td>'''
print "</tr>"

oddrow = 1
for film in films:
    if oddrow == 1:
        print "<tr><td style='-webkit-border-radius: 99px;-moz-border-radius: 99px;border-radius: 99px;text-align:center; font-weight:bold; padding:5px 5px 5px 5px; background-color:#B99292; color:white;' class='bbc-iplayer-film'><a style='color:white;' href='" + film['href'] + "' title='" + film['title'] + "'>" + film['title'] + "</a></td></tr>"
        oddrow = 2
    else:
        print "<tr><td style='-webkit-border-radius: 99px;-moz-border-radius: 99px;border-radius: 99px;text-align:center; font-weight:bold; padding:5px 5px 5px 5px; background-color:#D99E9E; color:white;' class='bbc-iplayer-film'><a style='color:white;' href='" + film['href'] + "' title='" + film['title'] + "'>" + film['title'] + "</a></td></tr>"
        oddrow = 1
print "</table>"


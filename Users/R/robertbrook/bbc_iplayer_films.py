import scraperwiki

scraperwiki.sqlite.attach('bbc-iplayer-films') 

films = scraperwiki.sqlite.select('* from `bbc-iplayer-films`.swdata')

print "<ol class='bbc-iplayer-films'>"

for film in films:
    print "<li class='bbc-iplayer-film'><a href='" + film['href'] + "' title='" + film['href'] + "'>" + film['title'] + "</a></li>"

print "</ol>"

import scraperwiki

scraperwiki.sqlite.attach('bbc-iplayer-films') 

films = scraperwiki.sqlite.select('* from `bbc-iplayer-films`.swdata')

print "<ol class='bbc-iplayer-films'>"

for film in films:
    print "<li class='bbc-iplayer-film'><a href='" + film['href'] + "' title='" + film['href'] + "'>" + film['title'] + "</a></li>"

print "</ol>"


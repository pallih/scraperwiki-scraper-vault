##########################################################
# Dynamically builds SQL to create simple table of Top 20#
#  values by frequency for basic sense-checking of data  #
#  only change required is to set sourcescraper variable #
##########################################################

#CHANGE THIS TO INTERNAL SCRAPER NAME
sourcescraper = 'classic_fm_playlist_scraper'


import scraperwiki


#POINT AT CORRECT SCRAPER
scraperwiki.sqlite.attach( sourcescraper)

popqry=  scraperwiki.sqlite.execute("SELECT * FROM swdata LIMIT 1")

#LOOP THROUGH TABLE COLUMNS TO BUILD SQL


for col in popqry['keys']:
    sel  =  'select [' + col + '] as "' + col + '" ,count(*) from swdata group by 1 order by 2 desc limit 20'
    data =  scraperwiki.sqlite.execute(sel)

    #print poptots


    print "<table border='1'>"           
    print "<tr><th>", col ,"</th><th>Count</th>"

    for key, value in data['data']:

        print "<tr>"
        print "<td>", key, "</td>"
        print "<td>",value, "</td>"
        print "</tr>"
    print "</table>"

##########################################################
# Dynamically builds SQL to create simple table of Top 20#
#  values by frequency for basic sense-checking of data  #
#  only change required is to set sourcescraper variable #
##########################################################

#CHANGE THIS TO INTERNAL SCRAPER NAME
sourcescraper = 'classic_fm_playlist_scraper'


import scraperwiki


#POINT AT CORRECT SCRAPER
scraperwiki.sqlite.attach( sourcescraper)

popqry=  scraperwiki.sqlite.execute("SELECT * FROM swdata LIMIT 1")

#LOOP THROUGH TABLE COLUMNS TO BUILD SQL


for col in popqry['keys']:
    sel  =  'select [' + col + '] as "' + col + '" ,count(*) from swdata group by 1 order by 2 desc limit 20'
    data =  scraperwiki.sqlite.execute(sel)

    #print poptots


    print "<table border='1'>"           
    print "<tr><th>", col ,"</th><th>Count</th>"

    for key, value in data['data']:

        print "<tr>"
        print "<td>", key, "</td>"
        print "<td>",value, "</td>"
        print "</tr>"
    print "</table>"


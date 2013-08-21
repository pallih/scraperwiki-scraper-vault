##########################################################
# Dynamically builds SQL to create simple table of field #
#  population rates for basic sense-checking of data     #
#  only change required is to set sourcescraper variable #
##########################################################

#CHANGE THIS TO INTERNAL SCRAPER NAME
sourcescraper = 'classic_fm_playlist_scraper'


import scraperwiki


#POINT AT CORRECT SCRAPER
scraperwiki.sqlite.attach( sourcescraper)

popqry=  scraperwiki.sqlite.execute("SELECT * FROM swdata LIMIT 1")

#LOOP THROUGH TABLE COLUMNS TO BUILD SQL
#NULLIF-TRIM COMBO MAKES SURE THAT NON-NULL EMPTY AND SPACES ARE TREATED AS NULL 
sel = 'SELECT count(*) as allrows'

for col in popqry['keys']:
        sel  +=  ',COUNT(nullif(trim([' + col + ']),"")) as "' + col + '"'

sel += ' FROM swdata'

poptots=  scraperwiki.sqlite.execute(sel)


poptotdict = dict(zip(poptots['keys'], poptots['data'][0]))

totrecs = poptotdict['allrows']


print "<table border='1'>"           
print "<tr><th>Column</th><th>Pct Population</th>"

for key, value in poptotdict.iteritems():
    if key != 'allrows':
        print "<tr>"
        print "<td>", key, "</td>"
        print "<td>", round((float(value)/float(totrecs)) * 100,2), "%</td>"
        print "</tr>"
print "</table>"

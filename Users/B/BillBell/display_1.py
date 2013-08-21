import scraperwiki           
scraperwiki.sqlite.attach("canadian-nocs")
data = scraperwiki.sqlite.select(           
    '''NOC, title from swdata order by NOC'''
)

for item in data :
    title = item [ 'title' ]
    NOC = item [ 'NOC' ]
    print '<div style="font: Arial; "><span style="width: 5em; font-weight: bold; ">%s</span><span>%s</span></div>\n' % ( NOC, title, )


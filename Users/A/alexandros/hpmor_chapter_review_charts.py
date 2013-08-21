import scraperwiki
from pygooglechart import GroupedVerticalBarChart

def get_chart_url(data):
    chart = GroupedVerticalBarChart(800, 200, y_range=(0, max(data)))
    chart.set_bar_width(3) #should be calculated
    chart.set_bar_spacing(0)
    chart.set_colours(['4D89F9'])
    chart.add_data(data)
    return chart.get_url()

scraperwiki.sqlite.attach('hpmor_chapter_reviews') 
data =  scraperwiki.sqlite.select('* from `hpmor_chapter_reviews`.swdata')

graphs = {
    'reviews':[], 
    'words_per_review':[], 
    'review_words':[], 
    'stumbleupon':[], 
    'twitter':[], 
    'delicious':[], 
    'buzz':[],
    'fb shar cnt':[],
    'fb comm cnt':[],
    'fb like cnt':[]
}

#print len(data)

for item in data:
    for key in graphs:
        graphs[key].append(item[key])

#print reviews

#axis x labels 1..71

print """<html>
    <head>
        <title>HP:MoR Chapter Metrics</title>
    </head>
    <body>"""

for key in graphs:
    print "        <img src='%s'/>" % (get_chart_url(graphs[key]) )

print """    </body>
</html>"""

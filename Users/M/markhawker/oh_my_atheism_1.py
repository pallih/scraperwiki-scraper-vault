sourcescraper = 'oh_my_atheism'

import scraperwiki           
scraperwiki.sqlite.attach('oh_my_atheism')

print '<!DOCTYPE html>'
print '<html>'
print ' <head>'
print '  <title>Oh My Atheism!</title>'
print '  <style type="text/css">'
print '  body { padding: 5px 30px; }'
print '  h1, p, button { font-size: 150%; }'
print '  </style>'
print '  <script type="text/javascript" src="https://www.google.com/jsapi"></script>'
print '  <script type="text/javascript">'
print '  google.load("visualization", "1", {packages:["treemap"]});'
print '  google.setOnLoadCallback(drawChart);'
print '  var tree;'
print '  function drawChart() {'
print '   var data = google.visualization.arrayToDataTable(['
print '    ["Month/Year", "Year", "Articles"]'
print '    ,["Articles", null, 0]'

data = scraperwiki.sqlite.select('year, count(*) as articles from oh_my_atheism.swdata group by year')

for d in data:
  print '    ,["' + str(d["year"]) + '", "Articles", 0]'

data = scraperwiki.sqlite.select('year, month, count(*) as articles from oh_my_atheism.swdata group by year, month')

for d in data:
  print '    ,["' + str(d["month"]) + "/" + str(d['year']) + '", "' + str(d["year"]) + '", ' + str(d["articles"]) + ']'

print '   ]);'
print '   tree = new google.visualization.TreeMap(document.getElementById("chart_div"));'
print '   tree.draw(data, {'
print '    minColor: "#f00",'
print '    midColor: "#ddd",'
print '    maxColor: "#0d0",'
print '    headerHeight: 24,'
print '    fontColor: "black",'
print '    fontSize: 20,'
print '    showScale: false});'
print '  }'
print '  </script>'
print ' </head>'
print ' <body>'
print '  <h1>Oh My Atheism!</h1>'
print "  <p>A <a href='https://developers.google.com/chart/interactive/docs/gallery/treemap'>Treemap</a> depicting articles on Atheism scraped from <a href='http://www.guardian.co.uk/commentisfree/commentisfree+world/atheism'>The Guardian's 'Comment Is Free'</a>. Created by me, <a href='http://twitter.com/markhawker'>Mark Hawker</a>, because I was curious to see whether the articles centred around 'key' Christian months e.g. April and December.</p>"
print '  <div id="chart_div" style="width: 900px; height: 500px;"></div>'
print '  <p><button type="button" onclick="tree.goUpAndDraw()">Reset Treemap</button></p>'
print ' </body>'
print '</html>'
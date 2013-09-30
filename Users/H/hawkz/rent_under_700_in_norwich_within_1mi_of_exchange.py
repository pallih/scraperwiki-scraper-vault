# Blank Python
sourcescraper = 'rightmove_scraper_for_particular_estate_agent'
import scraperwiki
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select(
    '''* from rightmove_scraper_for_particular_estate_agent.swdata 
    order by price asc'''
)

print """
<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset="utf-8" />
<title>Possible homes</title>
<style type="text/css">
body {
        font-family: Arial;
}
#homes .item { width: 280px; float: left; margin: 10px; background:#f0f0f0; padding: 10px; list-style:none; height: 600px; }
#homes img { width: 100%; }
</style>
</head>

<body>
<h1>Places to live?</h1>
<div id="homes">
"""


for d in data:
    print '<div class="item"><h2><a href="' , d['link'] , '">' , d['title'] , '</a></h2>';
    print '<img src="' , d['image_url'] , '"/>';
    print '<p>' , d['address'] ,'<br />' , d['saleType'] , '</p><p><b>&pound;' , d['price'] , '</b></p></div>';

print """
</div>
</body>
</html>
"""# Blank Python
sourcescraper = 'rightmove_scraper_for_particular_estate_agent'
import scraperwiki
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select(
    '''* from rightmove_scraper_for_particular_estate_agent.swdata 
    order by price asc'''
)

print """
<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset="utf-8" />
<title>Possible homes</title>
<style type="text/css">
body {
        font-family: Arial;
}
#homes .item { width: 280px; float: left; margin: 10px; background:#f0f0f0; padding: 10px; list-style:none; height: 600px; }
#homes img { width: 100%; }
</style>
</head>

<body>
<h1>Places to live?</h1>
<div id="homes">
"""


for d in data:
    print '<div class="item"><h2><a href="' , d['link'] , '">' , d['title'] , '</a></h2>';
    print '<img src="' , d['image_url'] , '"/>';
    print '<p>' , d['address'] ,'<br />' , d['saleType'] , '</p><p><b>&pound;' , d['price'] , '</b></p></div>';

print """
</div>
</body>
</html>
"""
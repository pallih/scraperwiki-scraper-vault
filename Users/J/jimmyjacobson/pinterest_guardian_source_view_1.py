# Blank Python
sourcescraper = 'pinterest_for_source_1'
import scraperwiki           
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select(           
    '''* from swdata join swvariables on swdata.url = swvariables.name 
    order by value_blob'''
)

print """
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Zappos Sources on Pinterest</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Le styles -->
    <link href="http://twitter.github.com/bootstrap/1.3.0/bootstrap.min.css" rel="stylesheet">

    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
  </head>
<body>
<h1>Zappos Pins on Pinterest</h1>
<div class="container">
<table class="zebra-striped">
"""
for pin in data:
    print "<tr>"
    print "<td><img src='%(img)s'/><br/><a href='%(url)s'>%(description)s</a>" % pin 
    print "</tr>"
print """
</table>
</div>
</body>
"""

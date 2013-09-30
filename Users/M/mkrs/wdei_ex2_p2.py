import scraperwiki           
scraperwiki.sqlite.attach("wdei_ex2_d_p1")

data = scraperwiki.sqlite.select("* from wdei_ex2_d_p1.swdata")

print """
<html>
<head>
<style type="text/css">
table { border-spacing:0; }
table, th, td { border:thin solid black; }
</style>
<title>WDEI Exercise 2, Part D, Point 2</title>
</head>
<body>
<table>
    <tr>
        <th>Auction Title</th>
        <th>Current Price (EUR)</th>
        <th>Auctioner</th>
        <th>Article Location</th>
        <th>Shipping To</th>
        <th>Detail</th>
    </tr>
"""

for d in data:
    print """
    <tr>
        <td>%(title)s</td>
        <td>%(price)s</td>
        <td>%(user)s</td>
        <td>%(location)s</td>
        <td>%(sendTo)s</td>
        <td><a href='%(link)s'>Detail Page</a></td>
    </tr>""" % d

print """
</table>
</body>
</html>
"""import scraperwiki           
scraperwiki.sqlite.attach("wdei_ex2_d_p1")

data = scraperwiki.sqlite.select("* from wdei_ex2_d_p1.swdata")

print """
<html>
<head>
<style type="text/css">
table { border-spacing:0; }
table, th, td { border:thin solid black; }
</style>
<title>WDEI Exercise 2, Part D, Point 2</title>
</head>
<body>
<table>
    <tr>
        <th>Auction Title</th>
        <th>Current Price (EUR)</th>
        <th>Auctioner</th>
        <th>Article Location</th>
        <th>Shipping To</th>
        <th>Detail</th>
    </tr>
"""

for d in data:
    print """
    <tr>
        <td>%(title)s</td>
        <td>%(price)s</td>
        <td>%(user)s</td>
        <td>%(location)s</td>
        <td>%(sendTo)s</td>
        <td><a href='%(link)s'>Detail Page</a></td>
    </tr>""" % d

print """
</table>
</body>
</html>
"""
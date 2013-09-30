import scraperwiki

# Get data from scraper
scraperwiki.sqlite.attach('researcherpositions')

# Get directors, order descending to put Executive Director on top
directors = scraperwiki.sqlite.select("* FROM swdata WHERE pos LIKE '%Director' ORDER BY pos DESC")
# Get rest (desc to put Research Assistants after Researchers, but order is still not optimal)
researchers = scraperwiki.sqlite.select("* FROM swdata WHERE pos NOT LIKE '%Director' ORDER BY pos DESC")
data = directors + researchers

print """<html> 
            <head>
                <title>TEST</title> 
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            </head>

            <body>
                <h1>Researchers</h1> 
                <br/>
                <table>
                    <tr> <th>Name</th> <th>Position</th> </tr>"""

# Print all names and Positions
for row in data:
    print u'<tr> <td>{}</td> <td>{}</td> </tr>'.format(row['name'], row['pos'])


print """       </table>
            </body>
        </html>"""
import scraperwiki

# Get data from scraper
scraperwiki.sqlite.attach('researcherpositions')

# Get directors, order descending to put Executive Director on top
directors = scraperwiki.sqlite.select("* FROM swdata WHERE pos LIKE '%Director' ORDER BY pos DESC")
# Get rest (desc to put Research Assistants after Researchers, but order is still not optimal)
researchers = scraperwiki.sqlite.select("* FROM swdata WHERE pos NOT LIKE '%Director' ORDER BY pos DESC")
data = directors + researchers

print """<html> 
            <head>
                <title>TEST</title> 
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            </head>

            <body>
                <h1>Researchers</h1> 
                <br/>
                <table>
                    <tr> <th>Name</th> <th>Position</th> </tr>"""

# Print all names and Positions
for row in data:
    print u'<tr> <td>{}</td> <td>{}</td> </tr>'.format(row['name'], row['pos'])


print """       </table>
            </body>
        </html>"""

import scraperwiki

sourcescraper = 'iplayer_comedy'

scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select(           
    '''* from iplayer_comedy.swdata 
    order by title asc'''
)
print '''
<!doctype html>
<html>
    <head>

    </head>
    <body>
        <h1>iPlayer Comedy</h1>
        <ul>
'''

for item in data:
    print '''
    <li>
        <a href="{href}">{title}</a>
    </li>
'''.format(
    href=item['href'].encode('utf-8'),
    title=item['title'].encode('utf-8'),
)

print '''
        </ul>
    </body>
</html>
'''
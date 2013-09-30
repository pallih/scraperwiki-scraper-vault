import scraperwiki

scraper = 'new_zealand_earthquakes'
scraperwiki.sqlite.attach(scraper, 'eqnz')

data = scraperwiki.sqlite.execute("SELECT lat,long, depth, magnitude FROM quakes LIMIT 10").get('data')
print data

        
import scraperwiki

scraper = 'new_zealand_earthquakes'
scraperwiki.sqlite.attach(scraper, 'eqnz')

data = scraperwiki.sqlite.execute("SELECT lat,long, depth, magnitude FROM quakes LIMIT 10").get('data')
print data

        

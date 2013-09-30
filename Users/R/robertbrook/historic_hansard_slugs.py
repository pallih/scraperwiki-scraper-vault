import scraperwiki
import lxml.html
import simplejson
import urllib

# What's it supposed to do?

# A scraper to generate a list of URL slugs for Historic Hansard content

# http://hansard.millbanksystems.com/


# How's it supposed to do it?

# Generate a list of all available sitting decades - such as http://hansard.millbanksystems.com/sittings/1800s

# sitting_centuries_fragments = ['21']

sitting_centuries_fragments = ['19', '20', '21']

sitting_decades_fragments = []

for sitting_centuries_fragment in sitting_centuries_fragments:
    html = scraperwiki.scrape('http://hansard.millbanksystems.com/sittings/C' + sitting_centuries_fragment)
    root = lxml.html.fromstring(html)
    
    for timeline_date in root.cssselect("td.timeline_date a"):
        sitting_decades_fragments.append(timeline_date.attrib['href'])

# Loop over each decade to generate a list of all available sitting years - such as http://hansard.millbanksystems.com/sittings/1803

sitting_years_fragments = []

for sitting_decades_fragment in sitting_decades_fragments:
    html = scraperwiki.scrape('http://hansard.millbanksystems.com' + sitting_decades_fragment)
    root = lxml.html.fromstring(html)

    for timeline_date in root.cssselect("td.timeline_date a"):
        sitting_years_fragments.append(timeline_date.attrib['href'])


# Loop over each year to generate a list of all available sitting months - such as http://hansard.millbanksystems.com/sittings/1803/nov

sitting_months_fragments = []

for sitting_years_fragment in sitting_years_fragments:
    html = scraperwiki.scrape('http://hansard.millbanksystems.com' + sitting_years_fragment)
    root = lxml.html.fromstring(html)

    for timeline_date in root.cssselect("td.timeline_date a"):
        sitting_months_fragments.append(timeline_date.attrib['href'])

# Loop over each month to generate a list of all available sitting days with .js URLs - such as http://hansard.millbanksystems.com/sittings/1803/nov/22.js

sitting_days_paths = []

for sitting_months_fragment in sitting_months_fragments:
    html = scraperwiki.scrape('http://hansard.millbanksystems.com' + sitting_months_fragment)
    root = lxml.html.fromstring(html)

    for timeline_date in root.cssselect("td.timeline_date a"):
        sitting_days_paths.append('http://hansard.millbanksystems.com' + timeline_date.attrib['href'] + '.js')
        
for sitting_days_path in sitting_days_paths:
    sitting_days_json = simplejson.load(urllib.urlopen(sitting_days_path))
    data = {
            'url' : sitting_days_path,
            'json' : sitting_days_json
        }
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)


# Generate records for each "section" element in the .js files


# Am I missing something? It feels like I am.

# also forgotten how to write python

# json pretty printer: http://jsonformatter.curiousconcept.com/






import scraperwiki
import lxml.html
import simplejson
import urllib

# What's it supposed to do?

# A scraper to generate a list of URL slugs for Historic Hansard content

# http://hansard.millbanksystems.com/


# How's it supposed to do it?

# Generate a list of all available sitting decades - such as http://hansard.millbanksystems.com/sittings/1800s

# sitting_centuries_fragments = ['21']

sitting_centuries_fragments = ['19', '20', '21']

sitting_decades_fragments = []

for sitting_centuries_fragment in sitting_centuries_fragments:
    html = scraperwiki.scrape('http://hansard.millbanksystems.com/sittings/C' + sitting_centuries_fragment)
    root = lxml.html.fromstring(html)
    
    for timeline_date in root.cssselect("td.timeline_date a"):
        sitting_decades_fragments.append(timeline_date.attrib['href'])

# Loop over each decade to generate a list of all available sitting years - such as http://hansard.millbanksystems.com/sittings/1803

sitting_years_fragments = []

for sitting_decades_fragment in sitting_decades_fragments:
    html = scraperwiki.scrape('http://hansard.millbanksystems.com' + sitting_decades_fragment)
    root = lxml.html.fromstring(html)

    for timeline_date in root.cssselect("td.timeline_date a"):
        sitting_years_fragments.append(timeline_date.attrib['href'])


# Loop over each year to generate a list of all available sitting months - such as http://hansard.millbanksystems.com/sittings/1803/nov

sitting_months_fragments = []

for sitting_years_fragment in sitting_years_fragments:
    html = scraperwiki.scrape('http://hansard.millbanksystems.com' + sitting_years_fragment)
    root = lxml.html.fromstring(html)

    for timeline_date in root.cssselect("td.timeline_date a"):
        sitting_months_fragments.append(timeline_date.attrib['href'])

# Loop over each month to generate a list of all available sitting days with .js URLs - such as http://hansard.millbanksystems.com/sittings/1803/nov/22.js

sitting_days_paths = []

for sitting_months_fragment in sitting_months_fragments:
    html = scraperwiki.scrape('http://hansard.millbanksystems.com' + sitting_months_fragment)
    root = lxml.html.fromstring(html)

    for timeline_date in root.cssselect("td.timeline_date a"):
        sitting_days_paths.append('http://hansard.millbanksystems.com' + timeline_date.attrib['href'] + '.js')
        
for sitting_days_path in sitting_days_paths:
    sitting_days_json = simplejson.load(urllib.urlopen(sitting_days_path))
    data = {
            'url' : sitting_days_path,
            'json' : sitting_days_json
        }
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)


# Generate records for each "section" element in the .js files


# Am I missing something? It feels like I am.

# also forgotten how to write python

# json pretty printer: http://jsonformatter.curiousconcept.com/







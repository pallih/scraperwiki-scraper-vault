import scraperwiki

scraperwiki.sqlite.attach("cyberwords")

print '''<h1>CyberWords</h1>
counting words in cyber space...<br/>

'''


data = scraperwiki.sqlite.select('''count(*) from cyberwords.swdata''')
print '''<p>Number of distinct words: ''', data, '''</p>'''


# Blank Python
sourcescraper = ''
import scraperwiki

scraperwiki.sqlite.attach("cyberwords")

print '''<h1>CyberWords</h1>
counting words in cyber space...<br/>

'''


data = scraperwiki.sqlite.select('''count(*) from cyberwords.swdata''')
print '''<p>Number of distinct words: ''', data, '''</p>'''


# Blank Python
sourcescraper = ''

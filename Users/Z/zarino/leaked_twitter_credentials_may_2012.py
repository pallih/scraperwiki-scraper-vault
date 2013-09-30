import scraperwiki
import urllib2
import re

bins = [
    'http://pastebin.com/raw.php?i=Kc9ng18h',
    'http://pastebin.com/raw.php?i=vCMndK2L',
    'http://pastebin.com/raw.php?i=JdQkuYwG',
    'http://pastebin.com/raw.php?i=fw43srjY',
    'http://pastebin.com/raw.php?i=jv4LBjPX'
]

for bin in bins:
    print '-- scraping ' + bin
    rows = []
    for line in urllib2.urlopen(bin):
        try:
            temp = {
                'username': line.split(':')[0],
                'password': line.split(':')[1],
                'source': bin
            }
            rows.append(temp)
        except ValueError:
            print '-- could not split: ' + line
        except:
            print '-- unexpected line: ' + line
    print '-- saving'
    scraperwiki.sqlite.save(['username','password'], rows, 'credentials', 0)import scraperwiki
import urllib2
import re

bins = [
    'http://pastebin.com/raw.php?i=Kc9ng18h',
    'http://pastebin.com/raw.php?i=vCMndK2L',
    'http://pastebin.com/raw.php?i=JdQkuYwG',
    'http://pastebin.com/raw.php?i=fw43srjY',
    'http://pastebin.com/raw.php?i=jv4LBjPX'
]

for bin in bins:
    print '-- scraping ' + bin
    rows = []
    for line in urllib2.urlopen(bin):
        try:
            temp = {
                'username': line.split(':')[0],
                'password': line.split(':')[1],
                'source': bin
            }
            rows.append(temp)
        except ValueError:
            print '-- could not split: ' + line
        except:
            print '-- unexpected line: ' + line
    print '-- saving'
    scraperwiki.sqlite.save(['username','password'], rows, 'credentials', 0)
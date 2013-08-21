from scraperwiki.sqlite import execute, save
import feedparser
import datetime
import json
import time
from lxml.html import fromstring

sample_table = fromstring('''<table border="0" width="224"><tr><td width='112'>Romney</td><td width='112' align='right'>50</td></tr><tr><td width='112'>Obama</td><td width='112' align='right'>43</td></tr><tr><td><strong>Spread</strong></td><td align='right'><strong><span class="rep">Romney +7</span></strong></td></tr></table>''')

def get_poll_data_from_table(table):
    return table.xpath('//td/text()')

def main():
    entries = feedparser.parse('http://www.realclearpolitics.com/epolls/2012/president/az/arizona_romney_vs_obama-1757.xml')['entries']

    for entry in entries:
    
        # Remove text datetime
        del(entry['updated'])
    
        for k, v in entry.items():
    
            # Convert to datetime
            if k == 'updated_parsed':
                entry['updated_parsed'] = datetime.datetime.fromtimestamp(time.mktime(v))
    
            # JSON dump nested things
            elif type(v) not in [bool, unicode]:
                entry[k] = json.dumps(v)
    
            table = fromstring(entry['summary'])
            get_poll_data_from_table(table)
    
    # Unique index on id
    save(['id'], entries, 'entries')

print get_poll_data_from_table(sample_table)
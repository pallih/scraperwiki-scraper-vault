import scraperwiki
import lxml.etree
import lxml.html
from xml.sax import saxutils

# Global data
rss_url = 'http://csoalerts.blogspot.com/feeds/posts/default'
data_verbose = True

def scrape():
    data_items = []
    rss_xml = lxml.html.fromstring(scraperwiki.scrape(rss_url))
    for entry_el in rss_xml.findall('entry'):
        alert_id = entry_el.findtext('id').partition('.post-')[2]
        location_name = entry_el.findtext('title').replace('Rower Notification - ', '')
        html = lxml.html.fromstring(saxutils.unescape(entry_el.findtext('content')).replace('<BR>', '\n').replace('<br />', '\n').partition('___')[0].partition('Regards')[0])
        note_text = html.text_content().strip()
        (subject, sep, detail) = note_text.partition('\n')
        location_desc = subject.replace('Rower notification from Thames Water:', '').strip() # Remove prefix
        date_time = entry_el.findtext('published').partition('.')[0].replace('T', ' ')
        alert_detail = detail.strip()
        data_items.append({ 'alert_id': alert_id, 'loc_name': location_name, 'loc_desc': location_desc, 'published': date_time, 'detail': alert_detail })

    # Save the data
    scraperwiki.sqlite.save(unique_keys=['alert_id'], data=data_items, table_name='alerts', verbose=data_verbose)

scrape()import scraperwiki
import lxml.etree
import lxml.html
from xml.sax import saxutils

# Global data
rss_url = 'http://csoalerts.blogspot.com/feeds/posts/default'
data_verbose = True

def scrape():
    data_items = []
    rss_xml = lxml.html.fromstring(scraperwiki.scrape(rss_url))
    for entry_el in rss_xml.findall('entry'):
        alert_id = entry_el.findtext('id').partition('.post-')[2]
        location_name = entry_el.findtext('title').replace('Rower Notification - ', '')
        html = lxml.html.fromstring(saxutils.unescape(entry_el.findtext('content')).replace('<BR>', '\n').replace('<br />', '\n').partition('___')[0].partition('Regards')[0])
        note_text = html.text_content().strip()
        (subject, sep, detail) = note_text.partition('\n')
        location_desc = subject.replace('Rower notification from Thames Water:', '').strip() # Remove prefix
        date_time = entry_el.findtext('published').partition('.')[0].replace('T', ' ')
        alert_detail = detail.strip()
        data_items.append({ 'alert_id': alert_id, 'loc_name': location_name, 'loc_desc': location_desc, 'published': date_time, 'detail': alert_detail })

    # Save the data
    scraperwiki.sqlite.save(unique_keys=['alert_id'], data=data_items, table_name='alerts', verbose=data_verbose)

scrape()
from datetime import datetime
import re
import scraperwiki
import lxml.html

base_url = 'http://183.82.99.66/payroll/flw1.php'
num_columns = 9


mapping = { 'origin bus station' : 'source',
            'origin bus staion'  : 'source',
            'from'               : 'source',
            'to'                 : 'destination',
            'dep. time'          : 'departure_time_from_this_stop',
            'reach time'         : 'arrival_time',
            'service no'         : 'service_number',
            'adult fare'         : 'fare_in_rupees_from_this_stop',
            'kms'                : 'distance_in_km_from_this_stop',
          }

unique_keys = [ 'service_number',
                'source',
                'destination',
                'stop_name',
                'departure_time_from_this_stop']


def empty(rec):
    for k,v in rec.items():
        if v:
            return False
        if k in unique_keys and not v:
            # Null data for primary key
            return True
    else:
        return True


def clean(items):
    cleaned = []
    for item in items:
        # Remove non-ascii characters
        item = unicode(item).encode("ascii", "ignore")

        # Convert to lowercase
        item = item.lower()

        # Remove escaped html characters like &nbsp;
        item = re.sub(r'&\S+;', '', item)

        # Remove extra whitespace
        item = ' '.join(item.split())

        # Change NULL to empty string
        item = item or ''

        # map
        item = mapping.get(item) or item

        # Convert to int if numeric
        try:
            item = int(item)
        except Exception:
            pass

        cleaned.append(item)

    return cleaned


def get_table(root, text):
    # APSRTC website has multiple tables on a page and there is no markup to uniquely identify the data. Using the presence of text to identify our table.
    for table in root.cssselect('table'):
        if text in table.text_content():
            return table


def get_stop_name(root):
    for td in root.cssselect('td'):
        text = td.text_content()
        if 'FROM BUS STATION' in text:
            stop_name = text.split(':')[-1]
            return clean([stop_name])[0]


def get_headers(rows):
    # There is no guarantee that headings are on the top of the table. Who wrote this HTML?
    for row in rows:
        if 'Frequency' in row.text_content():
            rows.remove(row)
        if 'Service' in row.text_content():
            rows.remove(row)
            headers = [td.text_content() for td in row.cssselect('td')]
            return clean(headers)


def process(station):
    print "Processing", station
    html = scraperwiki.scrape(station)
    assert 'Service' in html
    root = lxml.html.fromstring(html)

    stop_name = get_stop_name(root)
    table = get_table(root, 'Service')
    # There are some rows with dummy data or empty. Ignore them.
    rows = [tr for tr in table.cssselect('tr') if len(tr) == num_columns]

    headers = get_headers(rows)
    data = []
    for tr in rows:
        values = [td.text_content() for td in tr]
        values = clean(values)
        rec = dict(zip(headers, values))
        if empty(rec):
            continue

        # Times in ISO format
        dep = rec['departure_time_from_this_stop']
        if dep:
            rec['departure_time_from_this_stop'] = str(dep).replace('.', ':')
        arr = rec['arrival_time']
        if arr:
            rec['arrival_time'] = str(arr).replace('.', ':')
        rec['crawled_on'] = datetime.now()
        rec['stop_name'] = stop_name
        data.append(rec)

    scraperwiki.sqlite.save(data=data, unique_keys=unique_keys)


def process_main_page():
    html = scraperwiki.scrape(base_url + 'TimeTable.htm')
    assert 'TIME TABLE' in html
    assert 'Hyderabad' in html
    root = lxml.html.fromstring(html)

    table = get_table(root, 'Hyderabad')
    station_urls = [base_url + a.get('href') for a in table.cssselect('a')]
    station_urls = sorted(set(station_urls)) # Remove duplicates

    for station in station_urls:
        process(station)


process_main_page()

import scraperwiki
import lxml.html
import lxml.etree
import re
import urllib2

from datetime import date

data = { 'races': [], 'results': [], 'club_points': [] }
batch_size = 100

#scraperwiki.sqlite.execute("create table club_points ('hasler_year' int, 'race_url' string, 'race_name' string, 'club_name' string, 'position' int, 'points' int)")
#print scraperwiki.sqlite.execute("delete from races where race_date LIKE '%2011'")
#scraperwiki.sqlite.commit()

base_url = 'http://www.marathon-canoeing.org.uk/marathon/results/'
years = [ date.today().year ]

keys = {
    'results': [ 'boat_number', 'name_1', 'club_1', 'class_1', 'p_d_1', 'bcu_number_1', 'name_2', 'club_2', 'class_2', 'p_d_2', 'bcu_number_2', 'race_name', 'race_division', 'position', 'retired', 'time' ],
    'races': [ 'race_name', 'race_title', 'race_date', 'results_url' ],
    'club_points': [ 'hasler_year', 'race_url', 'race_name', 'club_name', 'position', 'points' ]
}
unique_keys = {
    'results': ['race_name', 'race_division', 'boat_number'],
    'races': [ 'race_name', 'race_date' ],
    'club_points': [ 'hasler_year', 'race_url', 'club_name' ]
}
table_names = { 'results': 'results', 'races': 'races', 'club_points': 'club_points' }

data_verbose=0
skip_races=0

result_url_overrides = { '2008/Richmond2008.htm': 'http://www.richmondcanoeclub.com/documents/2008/hrmTemplate2richmond2008_scroll.htm',
#    '2008/Chester2_2008.htm': 'http://chestercanoeclub.org.uk/chester_2_2008.htm'
#     '2012/Maidstone2012.htm': 'http://www.maidstonecanoeclub.net/joomla/index.php/racing/maidstone-marathon/results/71-maidstone-marathon-results-2012-provisional',
#     '2012/Hastings2012.htm': 'http://www.hastingscanoeclub.org.uk/recent-events-results/192-1066-marathon-results-2012'
#    '2012/Royal2012.htm': 'http://www.royalcanoeclub.com/wp-content/uploads/2012/06/Hasler2012-results.htm',
#    '2012/Richmond2012.htm': 'http://richmondcanoeclub.com/wp-content/uploads/2012/07/Richmond-Hasler-2012-Results.htm'
}

extra_results = [
#    ('2012/Richmond2012.htm', 'Richmond', '08/07/2012')
]

club_points = {}
club_names = {} # Cache of recently looked-up club names

def delete_race_data(url):
    scraperwiki.sqlite.execute("DELETE FROM club_points WHERE race_url = '" + url + "'")
    scraperwiki.sqlite.execute("DELETE FROM results WHERE race_name = '" + url + "'")
    scraperwiki.sqlite.execute("DELETE FROM races WHERE results_url = '" + url + "'")
    scraperwiki.sqlite.commit()

scraperwiki.sqlite.attach('hasler_marathon_club_list')

def main():
    #delete_race_data('2012/Richmond2012.htm')
    for year in years:
        try:
            races_url = '%sResults%s.html' % (base_url, year)
            races = get_races(races_url)
            races.extend(extra_results)
            scrape_races_html(races)
        except urllib2.HTTPError, e:
            if e.code == 404:
                print "Missing year %s" % (year)
            else:
                raise e
    #scrape_results_html('http://www.hastingscanoeclub.org.uk/recent-events-results/192-1066-marathon-results-2012', 'Hastings 1066', '20/05/2012')
    #scrape_results_html('http://www.maidstonecanoeclub.net/joomla/index.php/racing/maidstone-marathon/results/71-maidstone-marathon-results-2012-provisional', 'Maidstone', '17/06/2012')
    #delete_race_data('http://www.maidstonecanoeclub.net/joomla/index.php/racing/maidstone-marathon/results/71-maidstone-marathon-results-2012-provisional')
    #delete_race_data('http://www.hastingscanoeclub.org.uk/recent-events-results/192-1066-marathon-results-2012')
    #scrape_results_html('2012/Windsor2012.htm', 'Windsor', '14/10/2012')
    print "Finished"

def get_races(races_url):
    races = []
    race_html = lxml.html.fromstring(scraperwiki.scrape(races_url))
    race_rows = race_html.cssselect('table tr')[skip_races:]
    #print "Found %s rows" % (len(race_rows))
    for n in range(len(race_rows)):
        td_els = race_rows[n].findall('td')
        if len(td_els) == 2:
            #print "%s. %s" % (n, td_els[1].text_content().strip())
            race_date = td_els[0].text_content().strip()
            link = td_els[1].find('a')
            if link is not None:
                race_name = link.text_content().strip()
                race_path = link.get('href')
                if race_path is not None and race_path.endswith(('.htm', '.html')):
                    races.append((race_path, race_name, race_date))
                else:
                    print 'WARNING: Missing race link' if race_path is None else 'WARNING: Skipping bad (non-HTML) race link %s' % (race_path)
    return races

def scrape_races_html(races):
    for r in races:
        scrape_results_html(r[0], r[1], r[2])

def scrape_results_html(race_path, race_name='', race_date=''):
    global club_points
    # Allow race URL to be overridden (e.g. results only posted on club website, not marathon site)
    race_url = ('%s%s' % (base_url, race_path) if race_path not in result_url_overrides else result_url_overrides[race_path]) if not race_path.startswith('http') else race_path
    try:
        # Must remove </body>\n</html>\n<html>\n<body> lines in middle of the document
        results_html = lxml.html.fromstring(re.sub(r'\s</body>\s</html>\s<html>\s<body>', '', scraperwiki.scrape(race_url).replace('UTF-8', 'iso-8859-1')))
        h1_el = results_html.find('*/h1')
        if h1_el is None:
            h1_el = results_html.find('*/H1')
        # Older template uses h2
        if h1_el is None:
            h1_el = results_html.find('*/h2')
        if h1_el is None:
            h1_el = results_html.find('*/H2')
        race_title = re.sub('Results\:? ', '', h1_el.text_content().strip()) if h1_el is not None else ''
        date_arr = race_date.split('/');
        # save race
        #scraperwiki.sqlite.save(unique_keys=races_unique_keys, data=dict(zip(races_keys, [race_name, race_title, race_date, race_path])), table_name=races_table_name, verbose=data_verbose)
        # Save race data
        save_data({'races': dict(zip(keys['races'], [race_name, race_title, '%s-%s-%s' % (date_arr[2], date_arr[1], date_arr[0]), race_path]))})
        club_points = {}
        club_points_saved = False
        
        for table_el in results_html.cssselect('table'):
            caption_el = table_el.find('caption') if table_el.find('caption') is not None else table_el.find('CAPTION')
            if caption_el is not None:
                div_name = caption_el.text_content().strip()
                boat_num = 0
                hdr_names = []
                r_th_els = table_el.cssselect('tr th')
                for r_tr_el in table_el.cssselect('tr'):
                    hdr_names = [ get_result_value(thel).lower() for thel in r_th_els ]
                    r_td_els = r_tr_el.cssselect('td')
                    if div_name == 'Club points':
                        #print 'Saving club points'
                        if len(r_td_els) == 3:
                            data_row = dict(zip(hdr_names[0:len(r_td_els)], get_row_values(r_td_els)))
                            date_arr = race_date.split('/')
                            save_data({'club_points': {
                                'hasler_year': get_hasler_end_year(date(int(date_arr[2]), int(date_arr[1]), int(date_arr[0]))),
                                'race_url': race_path,
                                'race_name': race_name,
                                'club_name': data_row['club'],
                                'points': data_row['points'],
                                'position': data_row['overall']
                            }})
                            club_points_saved = True
                    else:
                        if len(r_td_els) >= 5:
                            boat_num += 1
                            data_row = dict(zip(hdr_names[0:len(r_td_els)], get_row_values(r_td_els)))
                            position = data_row['position'] if 'position' in data_row else None
                            names = data_row['name'] if 'name' in data_row else None
                            clubs = data_row['club'] if 'club' in data_row else None
                            classes = data_row['class'] if 'class' in data_row else None
                            divs = data_row['div'] if 'div' in data_row else None
                            pd = data_row['p/d'] if 'p/d' in data_row else None
                            time = data_row['time'] if 'time' in data_row else None
                            points = data_row['points'] if 'points' in data_row else None
                            rtd = False
                            if time == 'rtd':
                                rtd = True
                                time = ''
    
                            if names is None or position is None or clubs is None or classes is None:
                                raise Exception("Mandatory result data was not found")

                            if div_name.startswith('Div') and points is not None:
                                if (isinstance(clubs, list)):
                                    for i in [0,1]:
                                        if len(points) > i and points[i] is not None and points[i] != "":
                                            add_club_points(clubs[i], int(points[i]))
                                else:
                                    if points is not None and points != "":
                                        add_club_points(clubs, int(points))
    
                            # Save result data
                            save_data({'results': {
                                'boat_number': boat_num, 
                                'name_1': (names[0] if (isinstance(names, list)) else names), 
                                'club_1': (clubs[0] if (isinstance(clubs, list)) else clubs), 
                                'class_1': (classes[0] if (isinstance(classes, list)) else classes), 
                                'div_1': (divs[0] if (divs is not None and isinstance(divs, list)) else divs), 
                                'p_d_1': (pd[0] if (pd is not None and isinstance(pd, list)) else pd), 
                                'bcu_number_1': None, 
                                'name_2': (names[1] if (isinstance(names, list) and len(names) > 1) else None), 
                                'club_2': (clubs[1] if (isinstance(clubs, list) and len(clubs) > 1) else None), 
                                'class_2': (classes[1] if (isinstance(classes, list) and len(classes) > 1) else None), 
                                'div_2': (divs[1] if (divs is not None and isinstance(divs, list) and len(divs) > 1) else None), 
                                'p_d_2': (pd[1] if (pd is not None and isinstance(pd, list) and len(pd) > 1) else None), 
                                'bcu_number_2': None, 
                                'race_name': race_path, 
                                'race_division': div_name, 
                                'position': position, 
                                'retired': rtd, 
                                'time': time
                            }})

        # Save club points if they have not been saved yet
        if not club_points_saved:
            if len(club_points) > 0:
                date_arr = race_date.split('/')
                hasler_year = get_hasler_end_year(date(int(date_arr[2]), int(date_arr[1]), int(date_arr[0])))
                positions = get_club_positions()
                for cp in positions:
                    save_data({'club_points': {
                        'hasler_year': hasler_year,
                        'race_url': race_path,
                        'race_name': race_name,
                        'club_name': cp['name'] or cp['code'],
                        'points': cp['points'],
                        'position': cp['position']
                    }})
            else:
                print 'Warning: Could not find club points listed for race %s' % (race_name)

        # Flush all results in this division and the race itself to the datastore
        print "Saving %s results for %s" % (len(data['results']), race_name)
        save_data(items={'races': None, 'results': None, 'club_points': None}, force=True)
                
    except urllib2.HTTPError, e:
        if e.code == 404:
            print 'WARNING: Missing data for %s' % (race_name)
        else:
            raise e

def get_row_values(tdels):
    return [ (get_result_values(el) if '<br' in lxml.etree.tostring(el).lower() else get_result_value(el)) for el in tdels ]

def get_result_values(tdel):
    return re.sub('\s*<[bB][rR] */?>\s*', '|', re.sub('\s*</?[tT][dD][^>]*>\s*', '', re.sub('&#160;?', ' ', re.sub('&nbsp;?', ' ', (lxml.etree.tostring(tdel) or ''))))).replace('&#13;', '').strip().split('|')

def get_result_value(tdel):
    return tdel.text_content().replace('&#13;', '').strip()

# The Hasler season runs from 1st September to 31st August each year. This gives the year in which the Hasler season for the given date finishes, i.e. when the finals are held.
def get_hasler_end_year(date):
    return int(date.year) if date.month < 9 else int(date.year + 1)

def add_club_points(club_code, points):
    if club_code not in club_points:
        club_points[club_code] = []
    club_points[club_code].append(points)

def get_club_positions():
    def compare(a, b):
        return cmp(b[1], a[1]) # compare points
    positions = []
    lastpoints = 9999
    lastpos = 11
    nextpos = 10
    items = get_club_total_points().items()
    items.sort(compare)
    for p in items:
        pos = lastpos if p[1] == lastpoints else nextpos
        nextpos = nextpos - 1
        positions.append({'code': p[0], 'name': get_club_name(p[0]), 'points': p[1], 'position': pos if pos > 0 else 1}) # all clubs taking part seem to get 1 point
        lastpos = pos
        lastpoints = p[1]
    return positions

def get_club_total_points():
    return dict(zip(club_points.keys(), [club_points[k].sort(reverse=True) or sum(club_points[k][0:12]) for k in club_points.keys()]))

def get_club_name(code):
    global club_names
    if code not in club_names:
        row = scraperwiki.sqlite.select("name from hasler_marathon_club_list.swdata where code='%s'" % (code))
        club_names[code] = row[0]['name'] if len(row) == 1 else None
    return club_names[code]

def save_data(items={}, force=False):
    global data
    for k in items.keys():
        if items[k] is not None:
            data[k].append(items[k])
        if len(data[k]) >= batch_size or force == True:
            scraperwiki.sqlite.save(unique_keys=unique_keys[k], data=data[k], table_name=table_names[k], verbose=data_verbose)
            data[k] = []

main()


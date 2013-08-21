import scraperwiki
import lxml.html
import lxml.etree
import re
import urllib2

from datetime import date

data = { 'races': [], 'results': [] }
batch_size = 100

# TODO Use http://www.reading-canoe.org.uk/thameside_results.htm

result_url_overrides = []
#scraperwiki.sqlite.execute("delete from results where race_name='results/20120304_Thameisde2.htm'") 
base_url = 'http://www.reading-canoe.org.uk/'
results_pages = [
    {'name': 'Thameside 1 2011', 'date': '2011-03-06', 'path': 'results/20110306_rdg_Thameside1.htm'},
    {'name': 'Thameside 2 2011', 'date': '2011-03-11', 'path': 'T2_110320-1259.htm'},
    {'name': 'Thameside 1 2012', 'date': '2012-02-19', 'path': 'results/20120219_Thameisde1.htm'},
    {'name': 'Thameside 2 2012', 'date': '2012-03-04', 'path': 'results/20120304_Thameisde2.htm'},
    {'name': 'Thameside 1 2012', 'date': '2012-02-10', 'path': 'results/thamesides/2013_T1.htm'}
]

results_keys = [ 'boat_number', 'name_1', 'club_1', 'class_1', 'p_d_1', 'bcu_number_1', 'name_2', 'club_2', 'class_2', 'p_d_2', 'bcu_number_2', 'race_name', 'race_division', 'position', 'retired', 'time' ]
results_unique_keys = [ 'boat_number', 'race_name', 'race_division' ]

races_keys = [ 'race_name', 'race_title', 'race_date', 'results_url' ]
races_unique_keys = [ 'race_name', 'race_date' ]

races_table_name = 'races'
results_table_name = 'results'

data_verbose=0
skip_races=0

def main():
    for p in results_pages:
        scrape_results_html(p['path'], p['name'], p['date'])

def scrape_results_html(race_path, race_name='', race_date=''):
    # Allow race URL to be overridden (e.g. results only posted on club website, not marathon site)
    race_url = '%s%s' % (base_url, race_path) if race_path not in result_url_overrides else result_url_overrides[race_path]
    try:
        results_html = lxml.html.fromstring(scraperwiki.scrape(race_url).replace('UTF-8', 'iso-8859-1'))
        h1_el = results_html.find('*/h1')
        if h1_el is None:
            h1_el = results_html.find('*/H1')
        # Older template uses h2
        if h1_el is None:
            h1_el = results_html.find('*/h2')
        if h1_el is None:
            h1_el = results_html.find('*/H2')
        race_title = re.sub('Results\:? ', '', h1_el.text_content().strip()) if h1_el is not None else ''
        # save race
        scraperwiki.sqlite.save(unique_keys=races_unique_keys, data=dict(zip(races_keys, [race_name, race_title, race_date, race_path])), table_name=races_table_name, verbose=data_verbose)
        # Save race data
        save_data(race=dict(zip(races_keys, [race_name, race_title, race_date, race_path])))
        
        for table_el in results_html.cssselect('table'):
            caption_el = table_el.find('caption') if table_el.find('caption') is not None else table_el.find('CAPTION')
            if caption_el is not None:
                div_name = caption_el.text_content().strip()
                boat_num = 0
                hdr_names = []
                for r_tr_el in table_el.cssselect('tr'):
                    r_th_els = r_tr_el.cssselect('th')
                    if len(r_th_els) >= 5:
                        hdr_names = [ get_result_value(thel).lower() for thel in r_th_els ]
                    r_td_els = r_tr_el.cssselect('td')
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
                        rtd = False
                        if time == 'rtd':
                            rtd = True
                            time = ''

                        if names is None or position is None or clubs is None or classes is None:
                            print("Mandatory result data was not found, skipping row")
                            continue

                        # Save result data
                        save_data(result={
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
                        })

        # Flush all results in this division and the race itself to the datastore
        print "Saving %s results for %s" % (len(data['results']), race_name)
        save_data(force=True)
                
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

# Save the data in batches
def save_data(race=None, result=None, force=False):
    global data
    if race is not None:
        data['races'].append(race)
    if result is not None:
        data['results'].append(result)
    if len(data['races']) >= batch_size or force == True:
        scraperwiki.sqlite.save(unique_keys=races_unique_keys, data=data['races'], table_name=races_table_name, verbose=data_verbose)
        data['races'] = []
    if len(data['results']) >= batch_size or force == True:
        scraperwiki.sqlite.save(unique_keys=results_unique_keys, data=data['results'], table_name=results_table_name, verbose=data_verbose)
        #scraperwiki.sqlite.save(unique_keys=results_unique_keys, data=dict(zip(results_keys, result_data)), table_name=results_table_name, verbose=data_verbose)
        #scraperwiki.sqlite.execute("insert or replace into %s values (%s)" % (results_table_name, ', '.join([':%s' % (k) for k in results_keys])), dict(zip(results_keys, result_data)))
        data['results'] = []
main()


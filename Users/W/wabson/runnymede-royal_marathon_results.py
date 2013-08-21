import scraperwiki
import lxml.html
import lxml.etree
import re
import urllib2

from datetime import date

data = { 'races': [], 'results': [] }
batch_size = 100

base_url = 'http://www.royalcanoeclub.com/'
results_pages = [
    {'name': 'Runnymede-Royal 2012', 'date': '2012-03-20', 'path': 'index.php/2012/03/18/runnymede-royal-marathon-results/'}
]

results_keys = [ 'position', 'boat_number', 'name_1', 'club_1', 'name_2', 'club_2', 'time', 'div_1', 'class_1', 'bcu_number_1', 'div_2', 'class_2', 'bcu_number_2', 'race_name', 'race_division', 'retired' ]
results_unique_keys = [ 'race_name', 'race_division', 'boat_number' ]

races_keys = [ 'race_name', 'race_title', 'race_date', 'results_url' ]
races_unique_keys = [ 'race_name', 'race_date' ]

races_table_name = 'races'
results_table_name = 'results'

data_verbose=0
skip_races=0

result_url_overrides = { }

def main():
    for p in results_pages:
        scrape_results_blogpost(p['path'], p['name'], p['date'])

def scrape_results_blogpost(race_path, race_name='', race_date=''):
    # Allow race URL to be overridden (e.g. results only posted on club website, not marathon site)
    race_url = '%s%s' % (base_url, race_path) if race_path not in result_url_overrides else result_url_overrides[race_path]
    try:
        results_html = lxml.html.fromstring(scraperwiki.scrape(race_url).replace('UTF-8', 'iso-8859-1'))
        h1_el = results_html.find('body/div/div/div/div/div/h2')
        race_title = re.sub('Results\:? ', '', h1_el.text_content().strip()) if h1_el is not None else ''
        # save race
        scraperwiki.sqlite.save(unique_keys=races_unique_keys, data=dict(zip(races_keys, [race_name, race_title, race_date, race_path])), table_name=races_table_name, verbose=data_verbose)
        # Save race data
        save_data(race=dict(zip(races_keys, [race_name, race_title, race_date, race_path])))
        
        div_name = None
        for table_el in results_html.cssselect('table'):
            for r_tr_el in table_el.cssselect('tr')[1:]:
                r_td_els = r_tr_el.cssselect('td')
                if len(r_td_els) == 7:
                    div_name = r_td_els[1].text_content().strip()
                elif len(r_td_els) == 8:
                    position = r_td_els[0].text_content().strip()
                    boat_num = r_td_els[1].text_content().strip()
                    names = [r_td_els[2].text_content().strip(), r_td_els[4].text_content().strip()]
                    clubs = [r_td_els[3].text_content().strip(), r_td_els[5].text_content().strip()]
                    classes = [None, None]
                    divs = [None, None]
                    time = r_td_els[6].text_content().strip()
                    rtd = False
                    if time == 'rtd':
                        rtd = True
                        time = ''

                    if names[0] is None or names[1] is None or position is None or clubs is None or classes is None:
                        print("Mandatory result data was not found, skipping row")
                        continue

                    # Save result data
                    save_data(result={
                        'boat_number': boat_num, 
                        'name_1': names[0], 
                        'club_1': clubs[0], 
                        'class_1': classes[0], 
                        'div_1': divs[0], 
                        'bcu_number_1': None, 
                        'name_2': names[1], 
                        'club_2': clubs[1], 
                        'class_2': classes[1], 
                        'div_2': divs[1], 
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
        data['results'] = []
main()


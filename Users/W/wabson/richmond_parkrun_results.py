import scraperwiki
import lxml.html
import lxml.etree
import re
import urllib2

data = { 'results': [] }
keys = { 'results': [ 'race_id', 'race_num', 'pos', 'athlete_name', 'athlete_id', 'time', 'age_cat', 'age_grade', 'gender', 'gender_pos', 'club_name', 'club_id', 'note', 'tot_runs' ] }
unique_keys = { 'results': [ 'race_id', 'race_num', 'pos' ] }
batch_size = { 'results': 100 }
data_verbose = 0

def main():
    scrape_results_html('richmond')

def scrape_results_html(race_id):
    race_url = 'http://www.parkrun.org.uk/%s/results/latestresults' % (race_id)
    results_html = lxml.html.fromstring(scraperwiki.scrape(race_url))
    div_el = results_html.get_element_by_id('dnn_ContentPane');
    h1_el = div_el.find('div/div/span/h2')
    race_num = re.search(r"#\s*(\d+)", h1_el.text_content().strip(), flags=re.MULTILINE).group(1)

    table_el = results_html.get_element_by_id('results');
    
    hdr_names = []
    for r_tr_el in table_el.cssselect('tr'):
        r_th_els = r_tr_el.cssselect('th')
        if len(r_th_els) >= 5:
            hdr_names = [ thel.text_content().lower().replace(' ', '_') for thel in r_th_els ]
        r_td_els = r_tr_el.cssselect('td')
        if len(r_td_els) >= 5:
            #if names is None or position is None or clubs is None or classes is None:
            #    print("Mandatory result data was not found, skipping row")
            #    continue
            # TODO Check header names are as expected
            athlete_link = r_td_els[1].find('a').get('href') if r_td_els[1].find('a') is not None else None
            athlete_id = athlete_link[(athlete_link.find('=') + 1):] if athlete_link is not None else None

            club_link = r_td_els[7].find('a').get('href')if r_td_els[7].find('a') is not None else None
            club_id = club_link[(club_link.find('=') + 1):] if club_link is not None else None

            # Save result data
            save_data({'results': [{
                'race_id': race_id,
                'race_num': race_num,
                'pos': r_td_els[0].text_content(),
                'athlete_name': r_td_els[1].text_content(),
                'athlete_id': athlete_id,
                'time': r_td_els[2].text_content(),
                'age_cat': r_td_els[3].text_content(),
                'age_grade': r_td_els[4].text_content().replace(' %', ''),
                'gender': r_td_els[5].text_content(),
                'gender_pos': r_td_els[6].text_content(),
                'club_name': r_td_els[7].text_content(),
                'club_id': club_id,
                'note': r_td_els[8].text_content(),
                'tot_runs': r_td_els[9].text_content()
            }]})

    # Flush all results in this race and the race itself to the datastore
    print "Saving %s results for %s" % (len(data['results']), race_id)
    save_data({}, force=True)

    scraperwiki.sqlite.save_var('race_num', race_num)

# Save the data in batches
def save_data(items, force=False):
    global data
    for table in ['results']:
        if table in items:
            data[table].extend(items[table])
            if len(data[table]) >= batch_size[table] or force == True:
                scraperwiki.sqlite.save(unique_keys=unique_keys[table], data=data[table], table_name=table, verbose=data_verbose)
                data[table] = []

main();
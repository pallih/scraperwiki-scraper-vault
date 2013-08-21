import scraperwiki
import lxml.html
import time

# Global data
race_data = []

year = None
timestamp = int(time.time())

entries_unique_keys = ['year', 'surname_1', 'forename_1', 'club_1', 'surname_2', 'forename_2', 'club_2' ]
entries_table_name = 'entries'

data_verbose=0
batch_size=1000

# Blank Python
def scrape_entries_html(races_url):
    global year
    race_html = lxml.html.fromstring(scraperwiki.scrape(races_url))
    # Parse page title for year
    year = int(race_html.cssselect('span.pagetitle')[0].text_content().replace('Thamesides ', ''))
    rows = race_html.cssselect('table table tr') 
    race_class = None
    entry_paddlers = []
    for n,row in enumerate(rows):
        trclass = row.get('class')
        tdels = row.findall('td')
        if len(tdels) == 1:
            tdclass = tdels[0].get('class')
            if tdclass is not None and tdclass == 'sub-title': # Sub-heading
                race_class = str(cell_text_content(tdels[0]))
        elif len(tdels) == 9:
            tdclass = tdels[0].get('class')
            if trclass is None: # Data row
                if tdclass == 'xl24':
                    add_global(entry_paddlers)
                    entry_paddlers = []
                paddler = { 'race_class': race_class, 'surname': cell_text_content(tdels[0]), 'forename': cell_text_content(tdels[1]), 'club': cell_text_content(tdels[2]), 'class': cell_text_content(tdels[3]), 'bcu': str(cell_text_content(tdels[4])), 't1': cell_has_tick(tdels[5]), 't2': cell_has_tick(tdels[6]), 'cost': cell_text_content(tdels[7]), 'remove': cell_text_content(tdels[8]) }
                entry_paddlers.append(paddler)
            elif trclass == 'header_row':
                # TODO check row headings are as expected
                pass
            else:
                # TODO warn about bad class name
                pass
        else:
            print 'WARNING: WARNING: Skipping bad row #%s (bad number of table cells)' % (race_path)

def cell_text_content(cell):
    return cell.text_content().replace(u'\xa3', '').strip()

def cell_has_tick(cell):
    imgel = cell.find('img')
    return 1 if (imgel is not None and imgel.get('alt') is not None and imgel.get('alt') == 'Tick') else 0

def add_global(paddlers):
    if len(paddlers) == 1:
        save_data({'year': year, 'race_class': paddlers[0]['race_class'], 'surname_1': paddlers[0]['surname'], 'forename_1': paddlers[0]['forename'], 'club_1': paddlers[0]['club'], 'class_1': paddlers[0]['class'], 'bcu_number_1': paddlers[0]['bcu'], 'cost_1': paddlers[0]['cost'], 'remove_1': paddlers[0]['remove'], 'surname_2': '', 'forename_2': '', 'club_2': '', 'class_2': '', 'bcu_number_2': '', 'cost_2': '', 'remove_2': '', 'race_t1': paddlers[0]['t1'], 'race_t2': paddlers[0]['t2'], 'updated': timestamp})
    elif len(paddlers) == 2:
        if paddlers[0]['t1'] == paddlers[1]['t1'] and paddlers[0]['t2'] == paddlers[1]['t2'] and paddlers[0]['race_class'] == paddlers[1]['race_class']:
            save_data({'year': year, 'race_class': paddlers[0]['race_class'], 'surname_1': paddlers[0]['surname'], 'forename_1': paddlers[0]['forename'], 'club_1': paddlers[0]['club'], 'class_1': paddlers[0]['class'], 'bcu_number_1': paddlers[0]['bcu'], 'cost_1': paddlers[0]['cost'], 'remove_1': paddlers[0]['remove'], 'surname_2': paddlers[1]['surname'], 'forename_2': paddlers[1]['forename'], 'club_2': paddlers[1]['club'], 'class_2': paddlers[1]['class'], 'bcu_number_2': paddlers[1]['bcu'], 'cost_2': paddlers[1]['cost'], 'remove_2': paddlers[1]['remove'], 'race_t1': paddlers[0]['t1'], 'race_t2': paddlers[0]['t2'], 'updated': timestamp})
        else:
            raise Exception('Paddlers race classes and entry statuses must match!')
    elif len(paddlers) == 0:
        pass
    else:
        raise Exception('Bad number of paddlers found!')

# Save the data in batches
def save_data(entry=None, force=False):
    global race_data
    if entry is not None:
        race_data.append(entry)
    if len(race_data) >= batch_size or force == True:
        scraperwiki.sqlite.save(unique_keys=entries_unique_keys, data=race_data, table_name=entries_table_name, verbose=data_verbose)
        #print race_data
        race_data = []

def main():
    scrape_entries_html('http://bacon-fat.co.uk/thamesides/entries.asp')
    save_data(force=True)

main()
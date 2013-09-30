import scraperwiki
import lxml.html
import time

# Global data
dl_data = []
can = 2 # 1=all, 2=current, 3=featured, 4=deprecated
cols = ['Project', 'Filename', 'Summary', 'Uploaded', 'ReleaseDate', 'Size', 'Addon', 'UploadedBy']
query = ''
groupby = ''

timestamp = int(time.time())
pname = 'share-extras' # Google Code project name

entries_unique_keys = ['Project', 'Filename']
entries_table_name = 'downloads'

data_verbose=0
batch_size=1000

# Blank Python
def scrape_entries_html(races_url):
    global year
    race_html = lxml.html.fromstring(scraperwiki.scrape(races_url))
    rows = race_html.cssselect('table#resultstable tr')
    for n in range(len(rows)):
        trclass = rows[n].get('class')
        tdels = rows[n].findall('td')
        if len(tdels) == len(cols) + 2:
            dl = {}
            for m in range(len(cols)):
                dl[cols[m]] = cell_text_content(tdels[m + 1]) # We ignore the first row cell, which contains no data
            save_data(dl)

def cell_text_content(cell):
    link = cell.find('a')
    el = link if (link is not None) else cell
    return el.text_content().strip().replace('----', '')

# Save the data in batches
def save_data(entry=None, force=False):
    global dl_data
    if entry is not None:
        dl_data.append(entry)
    if len(dl_data) >= batch_size or force == True:
        scraperwiki.sqlite.save(unique_keys=entries_unique_keys, data=dl_data, table_name=entries_table_name, verbose=data_verbose)
        dl_data = []

def main():
    colspec = '+'.join(cols)
    scrape_entries_html('http://code.google.com/p/%s/downloads/list?can=%s&q=%s&groupby=%s&colspec=%s' % (pname, can, query, groupby, colspec))
    save_data(force=True)

main()import scraperwiki
import lxml.html
import time

# Global data
dl_data = []
can = 2 # 1=all, 2=current, 3=featured, 4=deprecated
cols = ['Project', 'Filename', 'Summary', 'Uploaded', 'ReleaseDate', 'Size', 'Addon', 'UploadedBy']
query = ''
groupby = ''

timestamp = int(time.time())
pname = 'share-extras' # Google Code project name

entries_unique_keys = ['Project', 'Filename']
entries_table_name = 'downloads'

data_verbose=0
batch_size=1000

# Blank Python
def scrape_entries_html(races_url):
    global year
    race_html = lxml.html.fromstring(scraperwiki.scrape(races_url))
    rows = race_html.cssselect('table#resultstable tr')
    for n in range(len(rows)):
        trclass = rows[n].get('class')
        tdels = rows[n].findall('td')
        if len(tdels) == len(cols) + 2:
            dl = {}
            for m in range(len(cols)):
                dl[cols[m]] = cell_text_content(tdels[m + 1]) # We ignore the first row cell, which contains no data
            save_data(dl)

def cell_text_content(cell):
    link = cell.find('a')
    el = link if (link is not None) else cell
    return el.text_content().strip().replace('----', '')

# Save the data in batches
def save_data(entry=None, force=False):
    global dl_data
    if entry is not None:
        dl_data.append(entry)
    if len(dl_data) >= batch_size or force == True:
        scraperwiki.sqlite.save(unique_keys=entries_unique_keys, data=dl_data, table_name=entries_table_name, verbose=data_verbose)
        dl_data = []

def main():
    colspec = '+'.join(cols)
    scrape_entries_html('http://code.google.com/p/%s/downloads/list?can=%s&q=%s&groupby=%s&colspec=%s' % (pname, can, query, groupby, colspec))
    save_data(force=True)

main()
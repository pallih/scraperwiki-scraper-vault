#missing persons from findthemissing.org
import scraperwiki
import mechanize
import simplejson

url2 = 'https://www.findthemissing.org/ajax/search_results?page=1&rows=10000&sidx=DateLKA&sord=desc' #Get 10000 - currently around 5800 are listed
url = 'https://www.findthemissing.org/'


br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
response = br.open(url)
br.select_form(nr=2)
br.form.set_all_readonly(False)
br.form['search[CaseInformation.FirstName]'] = "%" # we want it all
response = br.submit().read()
response2 = br.open(url2)
missing = simplejson.loads(response2.read())
for m in missing['rows']:
    record = {}
    id = m['cell'][0]
    record['id'] = id
    record['detail_url'] = 'https://www.findthemissing.org/cases/' + str(id) + '/0/'
    record['name'] = m['cell'][1]
    record['date'] = m['cell'][2]
    record['location'] = m['cell'][3]
    record['sex'] = m['cell'][4]
    record['race'] = m['cell'][5]
    record['age'] = m['cell'][6]
    scraperwiki.sqlite.save(['id'], data=record, table_name='missing_persons_usa')
#missing persons from findthemissing.org
import scraperwiki
import mechanize
import simplejson

url2 = 'https://www.findthemissing.org/ajax/search_results?page=1&rows=10000&sidx=DateLKA&sord=desc' #Get 10000 - currently around 5800 are listed
url = 'https://www.findthemissing.org/'


br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
response = br.open(url)
br.select_form(nr=2)
br.form.set_all_readonly(False)
br.form['search[CaseInformation.FirstName]'] = "%" # we want it all
response = br.submit().read()
response2 = br.open(url2)
missing = simplejson.loads(response2.read())
for m in missing['rows']:
    record = {}
    id = m['cell'][0]
    record['id'] = id
    record['detail_url'] = 'https://www.findthemissing.org/cases/' + str(id) + '/0/'
    record['name'] = m['cell'][1]
    record['date'] = m['cell'][2]
    record['location'] = m['cell'][3]
    record['sex'] = m['cell'][4]
    record['race'] = m['cell'][5]
    record['age'] = m['cell'][6]
    scraperwiki.sqlite.save(['id'], data=record, table_name='missing_persons_usa')

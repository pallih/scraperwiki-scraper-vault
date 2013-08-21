import scraperwiki
import requests
from pprint import pprint
from lxml import html
from urllib import urlencode

QUERY_URL = 'http://www3.rki.de/SurvStat/QueryForm.aspx'
RESULT_URL = 'http://www3.rki.de/SurvStat/ResultList.aspx'

headers = {
    'User-Agent': 'Mozilla/6.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0',
    'Referer': QUERY_URL
    }

session = requests.Session()
session.headers.update(headers)


def get_form_data(res, var=None, value=None):
    doc = html.fromstring(res.content)
    replaced = []
    for (field_k, field_v) in doc.forms[0].form_values():
        if field_k == 'webTab':
            field_v = '%3Cx%20SelectedTab%3D%220%22%3E%3C/x%3E'
        if var is not None and field_k == '__EVENTTARGET' and var is not 'btnSend':
            replaced.append((field_k, var))
        elif var is not None and field_k == '__EVENTARGUMENT':
            replaced.append((field_k, value))
        elif field_k != var:
            replaced.append((field_k, field_v))
        else:
            replaced.append((var, value))
    return replaced
    

res = session.get(QUERY_URL)
data = get_form_data(res, 'webTab$_ctl0$ctrlDisease$Migrated_lbMeldekategorie', 'INV')
data = dict(data)
pprint(data)
res = session.post(QUERY_URL, data=urlencode(data))
print res.content
data = get_form_data(res, 'btnSend', 'Abfrage starten')
data = dict(data)
pprint(data)
res = session.post(QUERY_URL, data=data)
print res.content
#res = session.get(RESULT_URL)
#print res.content


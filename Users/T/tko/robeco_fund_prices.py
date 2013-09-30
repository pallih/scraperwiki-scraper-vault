import datetime
import itertools
import re

from BeautifulSoup import BeautifulSoup
import requests
import scraperwiki

# "log" in - get usable session cookie along with page listing known funds and codes
rsession = requests.session()
r = rsession.get('https://www.robeco.com/extranet/f4i/quotescenter.do',
                 params=dict(pdstchn='profcom', plang='enu'),
                 verify=False)


soup = BeautifulSoup(r.content, convertEntities='html')
select = soup.find('select', attrs=dict(name='selectable'))
known_fund_codes = [option['value'] for option in select.findAll('option')]


endDate = datetime.date.today()
startDate = endDate - datetime.timedelta(days=30)

data = dict(
    #countryId='172',  # 172=Netherlands
    priceType='OPN',  # OPN=Opening price, NAV=Net Asset Value
    quotesCenterType='2',  # 1=Stock prices report, 2=Historical prices
    startDateString=format(startDate, '%d-%m-%Y'),
    endDateString=format(endDate, '%d-%m-%Y'),
    resultViewType='WEB',  # WEB/XLS
    submitText='funds',
)

"""
known_fund_codes = [
    "10", "1051", "1052", "11", "12", "1202", "1203", "1211", "1215", "1218",
    "1220", "1221", "13", "1302", "15", "1505", "1506", "1543", "1562", "1581",
    "1583", "1587", "1623", "1625", "1627", "163", "1641", "1787", "1788",
    "1789", "1808", "1841", "1843", "1884", "1886", "1903", "1990", "2042",
    "2044", "2045", "2046", "2049", "2050", "2051", "2082", "2102", "2103",
    "2281", "2303", "2322", "2424", "2425", "2426", "2427", "2435", "2442",
    "2443", "2444", "2445", "2521", "2581", "2643", "29", "2961", "2962",
    "2983", "30", "3002", "3003", "3041", "3061", "3062", "3063", "3082",
    "3101", "3121", "3122", "3123", "3190", "32", "3232", "3250", "3251", "33",
    "3330", "3331", "3370", "3390", "34", "3490", "3491", "3550", "3590",
    "3591", "3610", "3650", "3741", "3742", "3747", "3750", "3770", "3797",
    "3798", "3799", "3802", "3803", "3811", "3830", "3929", "3931", "3970",
    "4090", "4130", "4131", "4170", "4171", "4190", "4250", "4251", "4270",
    "4291", "4353", "4470", "4510", "4511", "4690", "4691", "4770", "4810",
    "4811", "4812", "4850", "4870", "4890", "4912", "4933", "5010", "5011",
    "5030", "5031", "5090", "5091", "5092", "5110", "5150", "5190", "5230",
    "5231", "5250", "5270", "5290", "5310", "5311", "5312", "5330", "5333",
    "5334", "5350", "5351", "5352", "5390", "5410", "5450", "5470", "5471",
    "5472", "5490", "5530", "5531", "5571", "5573", "5574", "5575", "5590",
    "5630", "5631", "5632", "5633", "5634", "5637", "5638", "5650", "5651",
    "5670", "5671", "5672", "5673", "5674", "5690", "5691", "5692", "5731",
    "5732", "5751", "5752", "5754", "5755", "5756", "5790", "5791", "5792",
    "5810", "5830", "5833", "5870", "5890", "5891", "5910", "5911", "5912",
    "5913", "5931", "6010", "6030", "6070", "6090", "6091", "6092", "6093",
    "6094", "6095", "6096", "6097", "6098", "6099", "6110", "6150", "6151",
    "814", "825", "858", "864", "893", "899", "900", "910", "938", "939",
]
"""

data['selected'] = known_fund_codes

r = rsession.post('https://www.robeco.com/extranet/f4i/quotescenter.do',
                  data=data,
                  verify=False)
assert r.status_code == requests.codes.ok


soup = BeautifulSoup(r.content, convertEntities='html')

for price in soup.findAll(text=re.compile('^\d+\.\d+$')):
    tables = price.findParents('table')
    assert len(tables) == 1
    table = tables[0]
    break
else:
    assert False

data = []
for tr in table.findAll('tr', recursive=False):
    row = []
    for td in tr.findAll('td', recursive=False):
        row.append(td.text)
    data.append(row)

""" data looks like
"Fund name", date, date...  # (date ~ 1 Jan 2012)
name, price, price...
name, price, price...
...
"""

""" convert to SQL-ish format:
name,date,price
name,date,price
...
"""

dates = data.pop(0)
dates.pop(0)

datetimes = [datetime.datetime.strptime(dt, '%d %b %Y') for dt in dates]
dates = [dt.date().isoformat() for dt in datetimes]

db = []
for row in data:
    name = row.pop(0)
    names = itertools.cycle([name])
    
    db.extend([dict(zip(['name', 'date', 'price'], val)) for val in zip(names, dates, row)])

scraperwiki.sqlite.save(unique_keys=['name', 'date'], data=db)import datetime
import itertools
import re

from BeautifulSoup import BeautifulSoup
import requests
import scraperwiki

# "log" in - get usable session cookie along with page listing known funds and codes
rsession = requests.session()
r = rsession.get('https://www.robeco.com/extranet/f4i/quotescenter.do',
                 params=dict(pdstchn='profcom', plang='enu'),
                 verify=False)


soup = BeautifulSoup(r.content, convertEntities='html')
select = soup.find('select', attrs=dict(name='selectable'))
known_fund_codes = [option['value'] for option in select.findAll('option')]


endDate = datetime.date.today()
startDate = endDate - datetime.timedelta(days=30)

data = dict(
    #countryId='172',  # 172=Netherlands
    priceType='OPN',  # OPN=Opening price, NAV=Net Asset Value
    quotesCenterType='2',  # 1=Stock prices report, 2=Historical prices
    startDateString=format(startDate, '%d-%m-%Y'),
    endDateString=format(endDate, '%d-%m-%Y'),
    resultViewType='WEB',  # WEB/XLS
    submitText='funds',
)

"""
known_fund_codes = [
    "10", "1051", "1052", "11", "12", "1202", "1203", "1211", "1215", "1218",
    "1220", "1221", "13", "1302", "15", "1505", "1506", "1543", "1562", "1581",
    "1583", "1587", "1623", "1625", "1627", "163", "1641", "1787", "1788",
    "1789", "1808", "1841", "1843", "1884", "1886", "1903", "1990", "2042",
    "2044", "2045", "2046", "2049", "2050", "2051", "2082", "2102", "2103",
    "2281", "2303", "2322", "2424", "2425", "2426", "2427", "2435", "2442",
    "2443", "2444", "2445", "2521", "2581", "2643", "29", "2961", "2962",
    "2983", "30", "3002", "3003", "3041", "3061", "3062", "3063", "3082",
    "3101", "3121", "3122", "3123", "3190", "32", "3232", "3250", "3251", "33",
    "3330", "3331", "3370", "3390", "34", "3490", "3491", "3550", "3590",
    "3591", "3610", "3650", "3741", "3742", "3747", "3750", "3770", "3797",
    "3798", "3799", "3802", "3803", "3811", "3830", "3929", "3931", "3970",
    "4090", "4130", "4131", "4170", "4171", "4190", "4250", "4251", "4270",
    "4291", "4353", "4470", "4510", "4511", "4690", "4691", "4770", "4810",
    "4811", "4812", "4850", "4870", "4890", "4912", "4933", "5010", "5011",
    "5030", "5031", "5090", "5091", "5092", "5110", "5150", "5190", "5230",
    "5231", "5250", "5270", "5290", "5310", "5311", "5312", "5330", "5333",
    "5334", "5350", "5351", "5352", "5390", "5410", "5450", "5470", "5471",
    "5472", "5490", "5530", "5531", "5571", "5573", "5574", "5575", "5590",
    "5630", "5631", "5632", "5633", "5634", "5637", "5638", "5650", "5651",
    "5670", "5671", "5672", "5673", "5674", "5690", "5691", "5692", "5731",
    "5732", "5751", "5752", "5754", "5755", "5756", "5790", "5791", "5792",
    "5810", "5830", "5833", "5870", "5890", "5891", "5910", "5911", "5912",
    "5913", "5931", "6010", "6030", "6070", "6090", "6091", "6092", "6093",
    "6094", "6095", "6096", "6097", "6098", "6099", "6110", "6150", "6151",
    "814", "825", "858", "864", "893", "899", "900", "910", "938", "939",
]
"""

data['selected'] = known_fund_codes

r = rsession.post('https://www.robeco.com/extranet/f4i/quotescenter.do',
                  data=data,
                  verify=False)
assert r.status_code == requests.codes.ok


soup = BeautifulSoup(r.content, convertEntities='html')

for price in soup.findAll(text=re.compile('^\d+\.\d+$')):
    tables = price.findParents('table')
    assert len(tables) == 1
    table = tables[0]
    break
else:
    assert False

data = []
for tr in table.findAll('tr', recursive=False):
    row = []
    for td in tr.findAll('td', recursive=False):
        row.append(td.text)
    data.append(row)

""" data looks like
"Fund name", date, date...  # (date ~ 1 Jan 2012)
name, price, price...
name, price, price...
...
"""

""" convert to SQL-ish format:
name,date,price
name,date,price
...
"""

dates = data.pop(0)
dates.pop(0)

datetimes = [datetime.datetime.strptime(dt, '%d %b %Y') for dt in dates]
dates = [dt.date().isoformat() for dt in datetimes]

db = []
for row in data:
    name = row.pop(0)
    names = itertools.cycle([name])
    
    db.extend([dict(zip(['name', 'date', 'price'], val)) for val in zip(names, dates, row)])

scraperwiki.sqlite.save(unique_keys=['name', 'date'], data=db)
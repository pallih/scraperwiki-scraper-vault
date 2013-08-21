import scraperwiki
import simplejson



url = "http://www.quandl.com/api/v1/datasets/DISASTERCENTER/LEVELS.json?&auth_token=Lb7rNa7MpBNyMyT55ap9&utf8=â&trim_start=1960-12-31&trim_end=07/12/31&sort_order=desc"
data = scraperwiki.scrape(url)
data = simplejson.loads(data)
keys = data.keys()
columns = data.get('column_names')
datas = data.get('data')
print columns
print datas
for datum in datas:
    holder = {}
    for i in range(11):
        holder[columns[i]] = datum[i]
    scraperwiki.sqlite.save(unique_keys = ['Date'], data = holder)import scraperwiki
import simplejson



url = "http://www.quandl.com/api/v1/datasets/DISASTERCENTER/LEVELS.json?&auth_token=Lb7rNa7MpBNyMyT55ap9&utf8=â&trim_start=1960-12-31&trim_end=07/12/31&sort_order=desc"
data = scraperwiki.scrape(url)
data = simplejson.loads(data)
keys = data.keys()
columns = data.get('column_names')
datas = data.get('data')
print columns
print datas
for datum in datas:
    holder = {}
    for i in range(11):
        holder[columns[i]] = datum[i]
    scraperwiki.sqlite.save(unique_keys = ['Date'], data = holder)
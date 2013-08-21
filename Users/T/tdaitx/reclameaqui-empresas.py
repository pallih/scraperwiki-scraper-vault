import scraperwiki
import lxml.html

#table = ("six_months", "table#tabelaDados6");
table = ("geral", "table#tabelaDados");

statsKeys = ['consumer_rating', 'response_delay', 'number_ratings', 'ignored', 'answered', 'total', 'answered_percentage', 'solved', 'again']

def getURL(id, code):
    return "http://www.reclameaqui.com.br/indices/" + id + "/" + code
    
def getStats(data):
    html = scraperwiki.scrape(data['url'], user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.45 Safari/537.36")
    root = lxml.html.fromstring(html)
    tableData = root.cssselect(table[1])[0]
    elems = dict(zip(statsKeys, tableData.cssselect("td big")))
    return {k: v.text_content().strip() for k,v in elems.iteritems()}

def fetchAll(exceptIds=[]):
    result = scraperwiki.scrape("http://www.reclameaqui.com.br/xml/busca_empresas.php?q=transporte", user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.45 Safari/537.36")
    for line in result.split("\n"):
        if len(line.strip()) == 0: continue
        data = {}
        print line
        (data['name'], data['id'], data['code']) = line.split('|')
        if (int(data['id']) in exceptIds): continue

        data['url'] = getURL(data['id'], data['code'])
        
        data.update(getStats(data))
        data.update({k: int(v) for k,v in data.items() if v.isdigit()})

        scraperwiki.sqlite.save(['id'], data, table[0])


#getStats({'url':'http://www.reclameaqui.com.br/indices/16963/via-brasil-mudancas-e-transportes-ltda-me/'})
try:
    existing_ids = [row['id'] for row in scraperwiki.sqlite.select("id from " + table[0])]
except scraperwiki.sqlite.SqliteError, e:
    existing_ids = []
    print "Ignored: " + str(e)

print existing_ids
fetchAll(existing_ids)

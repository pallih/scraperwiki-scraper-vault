import scraperwiki
from itertools import count
from lxml import html

URL = "http://www.e-ships.net/new/?View=ShipSearchResult"
URL += "&ship_name=&fdwt=&tdwt=&last_ex_name=&fgt=&tgt=&imo=&fnrt=&tnrt=&ship_type=-1&fteu=&tteu=&"
URL += "flag=-1&floa=&tloa=&ship_class=-1&fbeam=&tbeam=&call_sign=&fdraft=&tdraft=&owner_id="
URL += "&fbuilt=&tbuilt=&manager_id=&fengine_kw_total=&tengine_kw_total=&builder_id=&fengine_hp_total="
URL += "&tengine_hp_total=&sortby=ship_name&p=%s"

while True:
    p = scraperwiki.sqlite.get_var("p", 0)
    doc = html.parse(URL % p)
    rows = list(doc.findall('//tr'))
    if len(rows) == 1:
        break
    ldata = [ ]
    for row in rows:
        link = row.find('td/a')
        if link is None or not 'ShipDetails' in link.get('href'):
            continue
        number, name, stype, dwt, built, flag, _ = map(lambda c: c.text, row)
        imo = link.get('href').rsplit("=")[-1]
        ldata.append({'number': number, 'name': name, 'type': stype, 'dwt': dwt, 'built': built, 'flag': flag, 'imo': imo})
    scraperwiki.sqlite.save(['number'], ldata)
    scraperwiki.sqlite.save_var("p", p + 1)


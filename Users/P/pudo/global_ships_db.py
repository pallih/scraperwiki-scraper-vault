from scraperwiki.sqlite import save,get_var,save_var
from lxml import html

URL = "http://www.e-ships.net/new/?View=ShipSearchResult"
URL += "&ship_name=&fdwt=&tdwt=&last_ex_name=&fgt=&tgt=&imo=&fnrt=&tnrt=&ship_type=-1&fteu=&tteu=&"
URL += "flag=-1&floa=&tloa=&ship_class=-1&fbeam=&tbeam=&call_sign=&fdraft=&tdraft=&owner_id="
URL += "&fbuilt=&tbuilt=&manager_id=&fengine_kw_total=&tengine_kw_total=&builder_id=&fengine_hp_total="
URL += "&tengine_hp_total=&sortby=ship_name&p=%s"

i=get_var('page')
if i==None:
  i=0
while i<=1174:
    doc = html.parse(URL % i).getroot()
    rows = doc.xpath('//tr')
    if len(rows) == 1:
        break

    d=[]
    for row in rows:
      link = row.find('td/a')
      if link is None or not 'ShipDetails' in link.get('href'):
          continue
      number, name, type, dwt, built, flag, _ = map(lambda c: c.text, row)
      
      d.append({
        'number': number,
        'name': name, 
        'type': type,
        'dwt': dwt,
        'built': built,
        'flag': flag
      })
    save(['number'], d)
    i+=1
    save_var('page',i)
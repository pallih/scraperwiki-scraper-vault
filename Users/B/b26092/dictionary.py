import scraperwiki
import random
import lxml.html

NUMFETCH = 1000
MAXID = 57777

for i in range(NUMFETCH):
    id = random.randint(0,MAXID)
    html = scraperwiki.scrape("http://www.cantonese.sheik.co.uk/dictionary/words/"+str(id)+"/")
    if "couldn't find a word with an ID" in html: continue
    table = None
    try: table = lxml.html.fromstring(html).cssselect("table.cardborder")[0]
    except: pass
    if table is None: continue

    data = {
        'id' : id,
        'jyutping' : table.cssselect("span.cardjyutping")[0].text_content(),
        'defn' : table.cssselect("td.wordmeaning > div")[0].text_content(),
        'level' : int(table.cssselect("td.wordmeaning > div.wordlevel")[0].text_content().split(": ")[1][0])
    }

    data['trad'] = data['simp'] = table.cssselect("span.script")[0].text_content()
    try: data['simp'] = table.cssselect("td.chinesebig")[0].text_content().split("/")[1].strip()
    except: pass

    try: data['pinyin'] = table.cssselect("span.cardpinyin")[0].text_content()
    except: pass

    typedesc = table.cssselect("span.typedesc")[0].text_content()
    if "not sure if this term was Chinese, Cantonese" in typedesc: data['type'] = '?'
    elif "both" in typedesc: data['type'] = 'MC'
    elif "is used in Cantonese, not Mandarin" in typedesc: data['type'] = 'C'
    else: data['type'] = 'M'

    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
import scraperwiki
import random
import lxml.html

NUMFETCH = 1000
MAXID = 57777

for i in range(NUMFETCH):
    id = random.randint(0,MAXID)
    html = scraperwiki.scrape("http://www.cantonese.sheik.co.uk/dictionary/words/"+str(id)+"/")
    if "couldn't find a word with an ID" in html: continue
    table = None
    try: table = lxml.html.fromstring(html).cssselect("table.cardborder")[0]
    except: pass
    if table is None: continue

    data = {
        'id' : id,
        'jyutping' : table.cssselect("span.cardjyutping")[0].text_content(),
        'defn' : table.cssselect("td.wordmeaning > div")[0].text_content(),
        'level' : int(table.cssselect("td.wordmeaning > div.wordlevel")[0].text_content().split(": ")[1][0])
    }

    data['trad'] = data['simp'] = table.cssselect("span.script")[0].text_content()
    try: data['simp'] = table.cssselect("td.chinesebig")[0].text_content().split("/")[1].strip()
    except: pass

    try: data['pinyin'] = table.cssselect("span.cardpinyin")[0].text_content()
    except: pass

    typedesc = table.cssselect("span.typedesc")[0].text_content()
    if "not sure if this term was Chinese, Cantonese" in typedesc: data['type'] = '?'
    elif "both" in typedesc: data['type'] = 'MC'
    elif "is used in Cantonese, not Mandarin" in typedesc: data['type'] = 'C'
    else: data['type'] = 'M'

    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

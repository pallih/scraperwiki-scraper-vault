import scraperwiki
scraperwiki.sqlite.attach("washington_dc_vacantexemptblighted_properties")
from json import loads

table = scraperwiki.sqlite.select('* from dc_vacant_props')
for row in table:
    try:
        json = row['coords'].replace("u'", "'").replace('\'', '"')
        row['latitude'], row['longitude'] = map(float, [l[0] for l in loads(json)])
    except:
        pass


scraperwiki.sqlite.save(['addr_key'], table)import scraperwiki
scraperwiki.sqlite.attach("washington_dc_vacantexemptblighted_properties")
from json import loads

table = scraperwiki.sqlite.select('* from dc_vacant_props')
for row in table:
    try:
        json = row['coords'].replace("u'", "'").replace('\'', '"')
        row['latitude'], row['longitude'] = map(float, [l[0] for l in loads(json)])
    except:
        pass


scraperwiki.sqlite.save(['addr_key'], table)
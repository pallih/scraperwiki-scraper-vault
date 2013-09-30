import scraperwiki
import re
scraperwiki.sqlite.attach("welsh_school_data_save")
r = scraperwiki.sqlite.select("urn,data from welsh_school_data_save.swdata where urn = '6639115'")

print r[0]['urn']
m = re.search("Percentage of pupils entitled to free school meals.*text([^\d])+(\d+)",r[0]['data'])
me = re.search("text([^\d])+(\d+)",m.group(0))
fsm = me.group(2);
print r[0]["urn"]+' = '+fsm
#print results[0]["data"]import scraperwiki
import re
scraperwiki.sqlite.attach("welsh_school_data_save")
r = scraperwiki.sqlite.select("urn,data from welsh_school_data_save.swdata where urn = '6639115'")

print r[0]['urn']
m = re.search("Percentage of pupils entitled to free school meals.*text([^\d])+(\d+)",r[0]['data'])
me = re.search("text([^\d])+(\d+)",m.group(0))
fsm = me.group(2);
print r[0]["urn"]+' = '+fsm
#print results[0]["data"]
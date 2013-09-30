import scraperwiki
import simplejson
import urllib

scraperwiki.sqlite.attach("administrative_persecution_in_belarus_viasna_datab", "viasna")
scraperwiki.sqlite.attach("complete_court_table", "courts")


data = scraperwiki.sqlite.select(           
    "viasna.swdata.Number, viasna.swdata.Name, viasna.swdata.'Arrest', viasna.swdata.'Date' as 'Date of Arrest', viasna.swdata.'Date of Trial' as 'Date of Trial', viasna.swdata.'Article of Law', viasna.swdata.Judge, courts.swdata.Court, courts.swdata.Lng, courts.swdata.Lat, courts.swdata.Address, courts.swdata.Telephone, viasna.swdata.Arrest as Arrest, date(viasna.swdata.'Date of Trial', ('+' || replace(Arrest,'сут.','') || 'days')) as 'Release', viasna.swdata.Fine, viasna.swdata.Remarks from viasna.swdata left join courts.swdata on viasna.swdata.Court = courts.swdata.CourtViasna"
)

for d in data:
    fine = d['Fine'].split(u'\u0431.\u0432.')
    if len(fine) > 1:
        d['Fine Units'] = fine[0].strip()
        d['Fine Rubles'] = fine[1].replace(u'\u0440\u0443\u0431.','').strip()
    d['Arrest'] = d['Arrest'].replace(u'\u0441\u0443\u0442.','').strip()
    scraperwiki.sqlite.save(unique_keys=['Number'], data=d)


import scraperwiki
import simplejson
import urllib

scraperwiki.sqlite.attach("administrative_persecution_in_belarus_viasna_datab", "viasna")
scraperwiki.sqlite.attach("complete_court_table", "courts")


data = scraperwiki.sqlite.select(           
    "viasna.swdata.Number, viasna.swdata.Name, viasna.swdata.'Arrest', viasna.swdata.'Date' as 'Date of Arrest', viasna.swdata.'Date of Trial' as 'Date of Trial', viasna.swdata.'Article of Law', viasna.swdata.Judge, courts.swdata.Court, courts.swdata.Lng, courts.swdata.Lat, courts.swdata.Address, courts.swdata.Telephone, viasna.swdata.Arrest as Arrest, date(viasna.swdata.'Date of Trial', ('+' || replace(Arrest,'сут.','') || 'days')) as 'Release', viasna.swdata.Fine, viasna.swdata.Remarks from viasna.swdata left join courts.swdata on viasna.swdata.Court = courts.swdata.CourtViasna"
)

for d in data:
    fine = d['Fine'].split(u'\u0431.\u0432.')
    if len(fine) > 1:
        d['Fine Units'] = fine[0].strip()
        d['Fine Rubles'] = fine[1].replace(u'\u0440\u0443\u0431.','').strip()
    d['Arrest'] = d['Arrest'].replace(u'\u0441\u0443\u0442.','').strip()
    scraperwiki.sqlite.save(unique_keys=['Number'], data=d)



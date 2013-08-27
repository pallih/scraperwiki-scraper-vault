import scraperwiki

# these are the ones that can be match exactly between the two datasets
# later we can handle less good matches by having a look at the misspellings
natflow = { }
for arc in scraperwiki.datastore.getData('national-river-flow-archive-stations'):
    natflow[(arc['River'], arc['Location'])] = arc
            
for ea in scraperwiki.datastore.getData('environment-agency-river-levels'):
    arc = natflow.get((ea['River'], ea['station']))
            
    if arc:
        if 'url' in arc:
            arc['eaurl'] = arc.pop('url')
        arc.update(ea)
        scraperwiki.datastore.save(unique_keys=['River', 'Location'], data=arc, latlng=arc.get('latlng'))

import scraperwiki

# these are the ones that can be match exactly between the two datasets
# later we can handle less good matches by having a look at the misspellings
natflow = { }
for arc in scraperwiki.datastore.getData('national-river-flow-archive-stations'):
    natflow[(arc['River'], arc['Location'])] = arc
            
for ea in scraperwiki.datastore.getData('environment-agency-river-levels'):
    arc = natflow.get((ea['River'], ea['station']))
            
    if arc:
        if 'url' in arc:
            arc['eaurl'] = arc.pop('url')
        arc.update(ea)
        scraperwiki.datastore.save(unique_keys=['River', 'Location'], data=arc, latlng=arc.get('latlng'))

import scraperwiki

# these are the ones that can be match exactly between the two datasets
# later we can handle less good matches by having a look at the misspellings
natflow = { }
for arc in scraperwiki.datastore.getData('national-river-flow-archive-stations'):
    natflow[(arc['River'], arc['Location'])] = arc
            
for ea in scraperwiki.datastore.getData('environment-agency-river-levels'):
    arc = natflow.get((ea['River'], ea['station']))
            
    if arc:
        if 'url' in arc:
            arc['eaurl'] = arc.pop('url')
        arc.update(ea)
        scraperwiki.datastore.save(unique_keys=['River', 'Location'], data=arc, latlng=arc.get('latlng'))

import scraperwiki

# these are the ones that can be match exactly between the two datasets
# later we can handle less good matches by having a look at the misspellings
natflow = { }
for arc in scraperwiki.datastore.getData('national-river-flow-archive-stations'):
    natflow[(arc['River'], arc['Location'])] = arc
            
for ea in scraperwiki.datastore.getData('environment-agency-river-levels'):
    arc = natflow.get((ea['River'], ea['station']))
            
    if arc:
        if 'url' in arc:
            arc['eaurl'] = arc.pop('url')
        arc.update(ea)
        scraperwiki.datastore.save(unique_keys=['River', 'Location'], data=arc, latlng=arc.get('latlng'))

import scraperwiki

# these are the ones that can be match exactly between the two datasets
# later we can handle less good matches by having a look at the misspellings
natflow = { }
for arc in scraperwiki.datastore.getData('national-river-flow-archive-stations'):
    natflow[(arc['River'], arc['Location'])] = arc
            
for ea in scraperwiki.datastore.getData('environment-agency-river-levels'):
    arc = natflow.get((ea['River'], ea['station']))
            
    if arc:
        if 'url' in arc:
            arc['eaurl'] = arc.pop('url')
        arc.update(ea)
        scraperwiki.datastore.save(unique_keys=['River', 'Location'], data=arc, latlng=arc.get('latlng'))

import scraperwiki

# these are the ones that can be match exactly between the two datasets
# later we can handle less good matches by having a look at the misspellings
natflow = { }
for arc in scraperwiki.datastore.getData('national-river-flow-archive-stations'):
    natflow[(arc['River'], arc['Location'])] = arc
            
for ea in scraperwiki.datastore.getData('environment-agency-river-levels'):
    arc = natflow.get((ea['River'], ea['station']))
            
    if arc:
        if 'url' in arc:
            arc['eaurl'] = arc.pop('url')
        arc.update(ea)
        scraperwiki.datastore.save(unique_keys=['River', 'Location'], data=arc, latlng=arc.get('latlng'))

import scraperwiki

# these are the ones that can be match exactly between the two datasets
# later we can handle less good matches by having a look at the misspellings
natflow = { }
for arc in scraperwiki.datastore.getData('national-river-flow-archive-stations'):
    natflow[(arc['River'], arc['Location'])] = arc
            
for ea in scraperwiki.datastore.getData('environment-agency-river-levels'):
    arc = natflow.get((ea['River'], ea['station']))
            
    if arc:
        if 'url' in arc:
            arc['eaurl'] = arc.pop('url')
        arc.update(ea)
        scraperwiki.datastore.save(unique_keys=['River', 'Location'], data=arc, latlng=arc.get('latlng'))

import scraperwiki

# these are the ones that can be match exactly between the two datasets
# later we can handle less good matches by having a look at the misspellings
natflow = { }
for arc in scraperwiki.datastore.getData('national-river-flow-archive-stations'):
    natflow[(arc['River'], arc['Location'])] = arc
            
for ea in scraperwiki.datastore.getData('environment-agency-river-levels'):
    arc = natflow.get((ea['River'], ea['station']))
            
    if arc:
        if 'url' in arc:
            arc['eaurl'] = arc.pop('url')
        arc.update(ea)
        scraperwiki.datastore.save(unique_keys=['River', 'Location'], data=arc, latlng=arc.get('latlng'))


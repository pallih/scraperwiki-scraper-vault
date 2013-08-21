# postcode -> lsoa
# Returns an LSOA code and name for the given postcode

def postcode_to_lsoa(postcode):
    import requests, json, urllib
    url = 'http://mapit.mysociety.org/postcode/' + urllib.quote(postcode)
    j = json.loads(requests.get(url).text)
    for k,v in j['areas'].iteritems():
        if v['type_name'] == 'Lower Layer Super Output Area (Generalised)':
            return {
                'name': v['name'],
                'code': v['codes']['ons']
            }

print postcode_to_lsoa('L3 1EN')
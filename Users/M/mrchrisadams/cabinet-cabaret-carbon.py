import scraperwiki
import sys
import os
import urllib2
import simplejson as json
import datetime

def run():
    final = {}
    output = {}
    base_url = 'http://data.carbonculture.net/'
    try:
        fp = urllib2.urlopen(base_url)
        data = json.loads(fp.read())
        fp.close()
    except:
        pass
    else:
        for organisation in data['organisations']:
            org_url = base_url + '%s/'%organisation
            try:
                fp = urllib2.urlopen(org_url)
                data = json.loads(fp.read())
                fp.close()
            except:
                pass
            else:
                total_kwh = 0
                total_people = 0
                print data
                for p in data['place']:
                    premises_url = org_url+'%s/'%p
                    try:
                        fp = urllib2.urlopen(premises_url)
                        data = json.loads(fp.read())
                        fp.close()
                    except:
                        pass
                    else:
                        total_people += data['building_stats']['no_occupants']
                        for ns_channel in data['channels']:
                            channel = ns_channel.split('.')[-1]
                            #channel_url = premises_url+'%s/?end_time=%s'%(channel, datetime.datetime.now().strftime('%y-%m-%d'))
                            channel_url = premises_url+'%s/'%(channel, )
                            try:
                                fp = urllib2.urlopen(channel_url)
                                data = json.loads(fp.read())
                                fp.close()
                            except:
                                pass
                            else:
                                if data["channel-info"]["unit"] == "kWh":
                                    for item in data['results']:
                                        total_kwh += item[0]
                score = float(total_kwh)/total_people
                final[organisation] = dict(people=total_people, energy=total_kwh, score=score)
                output[organisation] = score
    max = 0
    min = 10000000
    for k, v in output.items():
        if v > max:
            max = v
        if v < min:
            min = v
    scale = 100.0/max
    heights = {}
    for k, v in output.items():
        heights[k] = (100 - (v*scale)) + (min*scale)
    result = {'heights': heights, 'figures': output}
    scraperwiki.datastore.save(unique_keys=['cabinetcabaret-carbon'], data={'cabinetcabaret-carbon':result})

run()


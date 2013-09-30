import scraperwiki
import json
import time

# Blank Python


NAMEs = ['Bob Filner', 'Darrell Issa', 'Brian Bilbray', 'Duncan Hunter', 'Susan Davis']

output = {}

index = 0

for rep, url in enumerate(URLs):
    
    try:
        page = scraperwiki.scrape(url)
    except:
        time.sleep(4)
        page = scraperwiki.scrape(url)
    
    myjson = json.loads(page)

    for item in myjson['results']:
        output['title'] = item['title']
        output['date'] = item['date']
        output['chamber'] = item['chamber']
        output['speaker_state'] = item['speaker_state']
        output['speaker_party'] = item['speaker_party']
        
        if item['speaker_first']:
            output['speaker_name'] = "Rep. " + str(item['speaker_first']) + " " + str(item['speaker_last'])
        else:
            output['speaker_name'] = "No speaker listed."
        
        output['congress'] = item['congress']
        output['number'] = item['number']
        output['order'] = item['order']
        output['volume'] = item['volume']
        output['session'] = item['session']
        output['capitolwords_url'] = item['capitolwords_url']
        output['origin_url'] = item['origin_url']
        output['key'] = index
        scraperwiki.sqlite.save(unique_keys=['key'], data=output)
        index += 1













        
    


import scraperwiki
import json
import time

# Blank Python


NAMEs = ['Bob Filner', 'Darrell Issa', 'Brian Bilbray', 'Duncan Hunter', 'Susan Davis']

output = {}

index = 0

for rep, url in enumerate(URLs):
    
    try:
        page = scraperwiki.scrape(url)
    except:
        time.sleep(4)
        page = scraperwiki.scrape(url)
    
    myjson = json.loads(page)

    for item in myjson['results']:
        output['title'] = item['title']
        output['date'] = item['date']
        output['chamber'] = item['chamber']
        output['speaker_state'] = item['speaker_state']
        output['speaker_party'] = item['speaker_party']
        
        if item['speaker_first']:
            output['speaker_name'] = "Rep. " + str(item['speaker_first']) + " " + str(item['speaker_last'])
        else:
            output['speaker_name'] = "No speaker listed."
        
        output['congress'] = item['congress']
        output['number'] = item['number']
        output['order'] = item['order']
        output['volume'] = item['volume']
        output['session'] = item['session']
        output['capitolwords_url'] = item['capitolwords_url']
        output['origin_url'] = item['origin_url']
        output['key'] = index
        scraperwiki.sqlite.save(unique_keys=['key'], data=output)
        index += 1













        
    



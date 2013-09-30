import json
import urllib2
import scraperwiki
import datetime
import time



for x in range(1, 2):


    twitter_search ="https://search.twitter.com/search.json?q=boston+bit&result_type=popular+since%3A2013-04-15+until%3A2013-04-16&rpp=100&include_entities=true";
    data0 = urllib2.urlopen(twitter_search).read()
    datum0 = json.loads(data0)
    for result0 in datum0['results']:
        #print(result0['entities'])
        #print(result0['entities']['urls'])
        if 'urls' in result0['entities']:
            if len(result0['entities']['urls'])>0:
                #print(result0['entities']['urls'][0]['display_url'])
                refined_name = (result0['entities']['urls'][0]['display_url'].decode('unicode_escape').encode('ascii','ignore'))
                url0 = 'https://api-ssl.bitly.com/v3/link/clicks?access_token=56b48892f54baafc285151479ff06dc35ca82108&link=http://' + refined_name
                data0a = urllib2.urlopen(url0).read()
                datum0a = json.loads(data0a)
                #print(datum0a)
                if (datum0a['status_txt'] == 'OK'):
                    #print(datum0a['data']['link_clicks'])
                    alldata = {"Link": refined_name, "Title": result0['text'], "Url": refined_name, "DateTime": str(datetime.datetime.now()), "Count": datum0a['data']['link_clicks']}
                    scraperwiki.sqlite.save(['Link','DateTime'], alldata)

import json
import urllib2
import scraperwiki
import datetime
import time



for x in range(1, 2):


    twitter_search ="https://search.twitter.com/search.json?q=boston+bit&result_type=popular+since%3A2013-04-15+until%3A2013-04-16&rpp=100&include_entities=true";
    data0 = urllib2.urlopen(twitter_search).read()
    datum0 = json.loads(data0)
    for result0 in datum0['results']:
        #print(result0['entities'])
        #print(result0['entities']['urls'])
        if 'urls' in result0['entities']:
            if len(result0['entities']['urls'])>0:
                #print(result0['entities']['urls'][0]['display_url'])
                refined_name = (result0['entities']['urls'][0]['display_url'].decode('unicode_escape').encode('ascii','ignore'))
                url0 = 'https://api-ssl.bitly.com/v3/link/clicks?access_token=56b48892f54baafc285151479ff06dc35ca82108&link=http://' + refined_name
                data0a = urllib2.urlopen(url0).read()
                datum0a = json.loads(data0a)
                #print(datum0a)
                if (datum0a['status_txt'] == 'OK'):
                    #print(datum0a['data']['link_clicks'])
                    alldata = {"Link": refined_name, "Title": result0['text'], "Url": refined_name, "DateTime": str(datetime.datetime.now()), "Count": datum0a['data']['link_clicks']}
                    scraperwiki.sqlite.save(['Link','DateTime'], alldata)


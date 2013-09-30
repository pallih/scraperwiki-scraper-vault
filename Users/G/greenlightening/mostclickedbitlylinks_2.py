import json
import urllib2
import scraperwiki
import datetime
import time



for x in range(1, 2):


    url = 'https://api-ssl.bitly.com/v3/user/popular_links?access_token=d67f353a6d46af2c6b9c0b1090d2f6569c6cd5eb'
        
    print(url)
    data = urllib2.urlopen(url).read()
    print(data)
    print(x)
    datum = json.loads(data)
    total_items = datum['data']['results']
    #print(total_items)
    
    for result in total_items:
        titolo = ''
        #print(result['aggregate_link'])
        url2 = 'https://api-ssl.bitly.com/v3/link/clicks?access_token=56b48892f54baafc285151479ff06dc35ca82108&link=' + result['aggregate_link']
        data2 = urllib2.urlopen(url2).read()
        datum2 = json.loads(data2)
        #print(datum2)
        print(datum2['data']['link_clicks'])
        if 'title' in result:
            titolo = result['title']
        alldata = {"Link": result['aggregate_link'], "Title": titolo, "Url": result['url'], "DateTime": str(datetime.datetime.now()), "Count": datum2['data']['link_clicks']}
        scraperwiki.sqlite.save(['Link','DateTime'], alldata)
import json
import urllib2
import scraperwiki
import datetime
import time



for x in range(1, 2):


    url = 'https://api-ssl.bitly.com/v3/user/popular_links?access_token=d67f353a6d46af2c6b9c0b1090d2f6569c6cd5eb'
        
    print(url)
    data = urllib2.urlopen(url).read()
    print(data)
    print(x)
    datum = json.loads(data)
    total_items = datum['data']['results']
    #print(total_items)
    
    for result in total_items:
        titolo = ''
        #print(result['aggregate_link'])
        url2 = 'https://api-ssl.bitly.com/v3/link/clicks?access_token=56b48892f54baafc285151479ff06dc35ca82108&link=' + result['aggregate_link']
        data2 = urllib2.urlopen(url2).read()
        datum2 = json.loads(data2)
        #print(datum2)
        print(datum2['data']['link_clicks'])
        if 'title' in result:
            titolo = result['title']
        alldata = {"Link": result['aggregate_link'], "Title": titolo, "Url": result['url'], "DateTime": str(datetime.datetime.now()), "Count": datum2['data']['link_clicks']}
        scraperwiki.sqlite.save(['Link','DateTime'], alldata)

import scraperwiki
import simplejson

source_url = "http://graph.facebook.com/search?q=ski&type=post&limit=1000"
page = 1
 
while 1:       
    try:        
        results_json = simplejson.loads(scraperwiki.scrape(source_url))                       
        profile = results_json['data']
        next = results_json['paging']        
        npage = ''
        source_url = ''
        npage = next['next']
        source_url = npage                                      
        for index in range(len(profile)):                
            profile2 = {}
            profile2['id'] = profile[index]['from']['id'] 
            profile2['name'] = profile[index]['from']['name'] 
            profile2['message'] = profile[index]['message'] 
            profile2['created'] = profile[index]['created_time']
            scraperwiki.datastore.save(["id"], profile2)              
        page = page + 1            
    except:                                
        print str(page) + ' pages scraped'
        break

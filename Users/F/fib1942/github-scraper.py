import mechanize
import json
import cookielib
import scraperwiki

url="https://api.github.com/legacy/repos/search/:python?start_page=XXX"
br = mechanize.Browser()
start_page=scraperwiki.sqlite.get_var('last_page')

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

#get the API results
def get_results(url):
    return json.loads(br.open(url).get_data())

#Save data into scraperwiki data store
def save(values):
    scraperwiki.sqlite.save(
    unique_keys=["username"], data={'username':values[0],'fork':values[1],
    'watchers':values[2], 'description':values[3], 'language':values[4], 'created':values[5], 'created_at':values[6], 
    'private':values[7], 'name':values[8], 'pushed_at':values[9], 'pushed':values[10], 'followers':values[11], 
    'owner':values[12], 'forks':values[13], 'type':values[14], 'size':values[15]}) 

#Convert Json data and save into database
def scrape(resp):
    start=scraperwiki.sqlite.get_var('last_page')
    if start==1:
        sno=1
    else:
        sno=start*100

    for each in range(0,99):
        values=[]
        try:
            new_repo=resp['repositories'][each]
        except IndexError as e:
            print e,"Error at page:",start

        for each_key in new_repo.keys():
            values.append(new_repo[each_key])
        save(values)
        
#Let the 1868 page scraping begin            
while start_page<240000:
    print "starting with page:,",start_page
    scraperwiki.sqlite.save_var('last_page', start_page)
    actual_url=url.replace('XXX',str(start_page))
    resp=get_results(actual_url)
    
    if resp['repositories']==[]:
        print "skipping this one"
        start_page+=1
        continue
    scrape(resp)
    start_page+=1
    
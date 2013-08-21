import scraperwiki
from scrapemark import scrape
import urllib
import urllib2
import simplejson

state_urls = ["http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Alabama"
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Alaska"
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Arizona"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Arkansas"
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=California"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Colorado"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Connecticut"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Delaware"
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Florida"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Georgia"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Hawaii"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Idaho"
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Illinois"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Indiana"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Iowa"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Kansas"
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Kentucky"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Louisiana"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Maine"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Maryland"
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Massachusetts"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Michigan"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Minnesota"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Mississippi"
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Missouri"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Montana"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Nebraska"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Nevada"
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=New+Hampshire"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=New+Jersey"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=New+Mexico"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=New+York"
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=North+Carolina"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=North+Dakota"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Ohio"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Oklahoma"
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Oregon"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Pennsylvania"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Rhode+Island"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=South+Carolina"
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=South+Dakota"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Tennessee"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Texas"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Utah"
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Vermont"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Virginia"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Washington"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=West+Virginia"
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Wisconsin"    
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=Wyoming"
    ,"http://www.nonprofitlist.org/cgi-bin/id/city.cgi?city=&state=District+of+Columbia"]
#state_pack = [state_urls[0]]
#state_pack = [state_urls[1],state_urls[2],state_urls[3]]
state_pack = [state_urls[4]]
#state_pack = [state_urls[5],state_urls[6],state_urls[7],state_urls[8],state_urls[9]]
#state_pack = [state_urls[10],state_urls[11],state_urls[12],state_urls[13],state_urls[14]]
#state_pack = [state_urls[15],state_urls[16],state_urls[17],state_urls[18],state_urls[19]]
#state_pack = [state_urls[20],state_urls[21],state_urls[22],state_urls[23],state_urls[24]]]
#state_pack = [state_urls[25],state_urls[26],state_urls[27],state_urls[28],state_urls[29]]
#state_pack = [state_urls[30],state_urls[31],state_urls[32],state_urls[33],state_urls[34]]
#state_pack = [state_urls[35],state_urls[36],state_urls[37],state_urls[38],state_urls[39]]
#state_pack = [state_urls[40],state_urls[41],state_urls[42],state_urls[43],state_urls[44]]
#state_pack = [state_urls[45],state_urls[46],state_urls[47],state_urls[48],state_urls[49]]
#state_pack = [state_urls[50]]
#print homepage

for item in state_pack:
    page = scraperwiki.scrape(item)
    #print item
    list_scrape = scrape("""
        <script type="text/javascript"></script>
            {*
            <tr><td width="90%"><a href="{{[list].url}}"><strong></strong></a>
            *}
        """,
        page)['list']
    for np_url in list_scrape:
        np_page = scraperwiki.scrape(np_url['url'])
        np_scrape = scrape("""
                <TD width="50%" valign="top" align="left">  
                {* <B> {{[np].name}}</B>
                <br>
                <B><br>{{[np].address}}
                <br>{{[np].city_state}}<br> Phone Number: {{[np].phone}} </B> *}
                {* <br />Visit Website: <a>{{[np].url}}</a>*}
                <a border="0" rel="nofollow"> </a>
                {* <script></script><script></script>
                <br />{{[np].description}}<br /><br /><br />NonProfitList.org <div></div>*}
        """,
        np_page)['np']

        full_address = np_scrape[0]['address'] + " " + np_scrape[0]['city_state']
        #print full_address
        
        geocode_url = 'http://tasks.arcgisonline.com/ArcGIS/rest/services/Locators/TA_Streets_US_10/GeocodeServer/findAddressCandidates?Single+Line+Input='+urllib.quote_plus(full_address)+'&outFields=&outSR=&f=json'
        #print geocode_url
        georeq = urllib2.Request(geocode_url)
        geo_response = urllib2.urlopen(georeq)
        geocode = simplejson.loads(geo_response.read())
        #print geocode
        if len(geocode['candidates']):
            data_lat = geocode['candidates'][0]['location']['y']
            data_lng = geocode['candidates'][0]['location']['x']
        
        np_scrape[0]['lat'] = data_lat
        np_scrape[0]['lng'] = data_lng
        #print data_lat 
        #print data_lng

        scraperwiki.sqlite.save(unique_keys=['name'], data=np_scrape[0])

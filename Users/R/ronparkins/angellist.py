import scraperwiki
import json       
import lxml.html 
import sys
import csv        

for j in range(0,7):
    for i in range(0,10):
        if ((j*10)+i) >0:
            if ((j*10)+i) <2:
                test = scraperwiki.scrape("https://api.angel.co/1/tags/1654/startups?page=" + str((j*10)+i))
                test2 = json.loads(test) 
                print(test2["startups"])
                print(dict(test2))
                test_string = json.dumps(test2["startups"], sort_keys=True, indent=2)
                print(test_string)

                data2="""[
                    {"longitude":"-73.689070","latitude":"40.718000"},
                    {"longitude":"-73.688400","latitude":"40.715990"},
                    {"longitude":"-73.688340","latitude":"40.715790"},
                    {"longitude":"-73.688370","latitude":"40.715500"},
                    {"longitude":"-73.688490","latitude":"40.715030"},
                    {"longitude":"-73.688810","latitude":"40.714370"},
                    {"longitude":"-73.688980","latitude":"40.714080"},
                    {"longitude":"-73.689350","latitude":"40.713390"},
                    {"longitude":"-73.689530","latitude":"40.712800"},
                    {"longitude":"-73.689740","latitude":"40.712050"},
                    {"longitude":"-73.689820","latitude":"40.711810"},
                    {"longitude":"-73.689930","latitude":"40.711380"},
                    {"longitude":"-73.690110","latitude":"40.710710"}
                ]"""

                data2 = json.loads(data2)
            

                #f = csv.writer(open('file.csv', 'wb+'))
                # use encode to convert non-ASCII characters
                for item in data2:
                    #values = [ x.encode('utf8') for x in item['fields'].values() ]
                                        
                    #print([item['longitude'], item['latitude']])
                    scraperwiki.sqlite.save(unique_keys=["longitude"], data=([item['longitude'], item['latitude']]))

                #scraperwiki.scrape("https://api.angel.co/1/tags/1654/startups?page=" + str((j*10)+i)))
                #html = scraperwiki.scrape("https://api.angel.co/1/tags/1654/startups?page=" + str((j*10)+i))
                #root = lxml.html.fromstring(html)
                #if ((j*10)+i) <2:
                    #data = {
                    #   'id',
                     #  'hidden'
                    #   'community_profile' : tds[2].text_content(),
                    #   'name' : tds[3].text_content(),
                    #   'angellist_url' : tds[4].text_content(),
                    #   'logo_url' : tds[5].text_content(), 
                    #   'thumb_url' : tds[6].text_content(),
                    #   'quality' : tds[7].text_content(),
                    #   'product_desc' : tds[8].text_content(),
                    #   'high_concept' : tds[9].text_content(), 
                    #   'follower_count' : tds[10].text_content(),
                    #   'company_url' : tds[11].text_content(),
                    #   'created_at' : tds[12].text_content(),
                    #   'updated_at' : tds[13].text_content(),



                   #}
                    #scraperwiki.sqlite.save(unique_keys=['id'], data=data)
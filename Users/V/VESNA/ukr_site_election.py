import scraperwiki
html = scraperwiki.scrape("http://www.cvk.gov.ua/vnd2012/wp300pt001f01=900.html")
print "Click on the ...more link to see the whole page"
print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object


# tds = root.cssselect('td') # get all the <td> tags
# for td in tds:
#     print lxml.html.tostring(td) # the full HTML tag
#     print td.text                # just the text inside the HTML tag

i = 0
match_details = "" 

ranking = "" 
party = ""
percent = ""
number_votes = "" 

for match in root.cssselect("table class=t2 cellspacing=1"):
    match_details  = lxml.html.tostring(match)

    #Retrieve match status (FT or not)
#    start = match_details.find("wmcResBoxCaption",0);
#    start = start + len("wmcResBoxCaption>") + 1
#    end = match_details.find("</div>",start);
#    match_status = match_details[start:end]
#    print match_status 

    
 # Retrieve ranking
        start = match_details.find("td class=td10",0);
        start = start + len("td class=td10") + 1
        end = match_details.find("</font>",start);
        ranking = match_details[start:end]
        print ranking

i = i + 1

        data = {
                'ranking' : ranking,
                'party'  : party,
                'percent'  : percent,
                'number_votes'      : number_votes
            }
    
        #print data
        scraperwiki.sqlite.save(unique_keys=['ranking'], data=data)





# for td in tds:
#      record = { "td" : td.text } # column name and value
#     scraperwiki.sqlite.save(["td"], record) # save the records one by one

#for tr in root.cssselect("div[align='center'] tr"):
#    tds = tr.cssselect("td")
#    if len(tds)==5:
#        data = {
#            'number' : tds[0].text_content(),
#            'party' : int(tds[1].text_content()),
#            'percent' : int(tds[3].text_content()),            
#            'number_votes' : int(tds[4].text_content()) 
#        }
           

#        scraperwiki.sqlite.save(unique_keys=['country'], data=data)




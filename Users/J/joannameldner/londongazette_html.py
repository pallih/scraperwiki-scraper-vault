import scraperwiki
import lxml.html
         
#scraperwiki.sqlite.attach("londongazette")
#scraperwiki.sqlite.execute("create table websites  as select * from londongazette.websites order by id") 

#scraperwiki.sqlite.save_var('last_page', 0)

a=scraperwiki.sqlite.get_var('last_page')

linklist=[]
linklist = scraperwiki.sqlite.select("* from websites where id>="+str(a))

record = {}

for i in linklist:
    scraperwiki.sqlite.save_var('last_page', i['id'])
    #print i['link']
    html=scraperwiki.scrape(i['link'])
    #scrape_urls(html)    
    record['id']=i['id']
    record['sourceurl']=i['link']
    root = lxml.html.fromstring(html)
    dx = root.cssselect('div.Data div')
    if dx==[]: 
        #print 'empty'
        record['data']='ERROR'
        scraperwiki.sqlite.save(['sourceurl'], record, 'errors') 
    else : 
        d = root.cssselect('div.Data div')[0]
        #print lxml.html.tostring(d)
        record['data']=lxml.html.tostring(dx[0])
        scraperwiki.sqlite.save(['sourceurl'], record) import scraperwiki
import lxml.html
         
#scraperwiki.sqlite.attach("londongazette")
#scraperwiki.sqlite.execute("create table websites  as select * from londongazette.websites order by id") 

#scraperwiki.sqlite.save_var('last_page', 0)

a=scraperwiki.sqlite.get_var('last_page')

linklist=[]
linklist = scraperwiki.sqlite.select("* from websites where id>="+str(a))

record = {}

for i in linklist:
    scraperwiki.sqlite.save_var('last_page', i['id'])
    #print i['link']
    html=scraperwiki.scrape(i['link'])
    #scrape_urls(html)    
    record['id']=i['id']
    record['sourceurl']=i['link']
    root = lxml.html.fromstring(html)
    dx = root.cssselect('div.Data div')
    if dx==[]: 
        #print 'empty'
        record['data']='ERROR'
        scraperwiki.sqlite.save(['sourceurl'], record, 'errors') 
    else : 
        d = root.cssselect('div.Data div')[0]
        #print lxml.html.tostring(d)
        record['data']=lxml.html.tostring(dx[0])
        scraperwiki.sqlite.save(['sourceurl'], record) 
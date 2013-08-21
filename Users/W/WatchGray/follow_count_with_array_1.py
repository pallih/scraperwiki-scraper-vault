import scraperwiki
import lxml.html
import datetime

try:
    scraperwiki.sqlite.execute("""
        create table followers
        ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT
                
        )
    """)
except:
    print "Table probably already exists."


candidates = (["mittromney", "BarackObama", "RickSantorum", "newtgingrich", "RONPAUL"]);
date = datetime.date.today()

count = 1

for i in candidates:
    url = ("http://twitter.com/" + i)

    html = scraperwiki.scrape(url)
    raw = lxml.html.fromstring(html)

    for row in raw.cssselect("span#follower_count"):
        print row.text
        data = {
            'row_id':count,
            'date':date,
            'handle':i,
            'followers':row.text
        }
        print count
        count += 1
#        scraperwiki.sqlite.save(unique_keys=['row_id'], data=data)
        scraperwiki.sqlite.save(unique_keys=[], data=data, table_name='followers')

#scraperwiki.sqlite.save_var('next_id', count)
#print scraperwiki.sqlite.get_var('next_id')




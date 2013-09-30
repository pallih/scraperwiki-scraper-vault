import scraperwiki
import datetime
import time


count = int(scraperwiki.scrape("http://thecostofknowledge.com/namecount.php"))
now = datetime.datetime.now()
scraperwiki.sqlite.save(unique_keys=['date'], data= {'date': now, 'count': count})
import scraperwiki
import datetime
import time


count = int(scraperwiki.scrape("http://thecostofknowledge.com/namecount.php"))
now = datetime.datetime.now()
scraperwiki.sqlite.save(unique_keys=['date'], data= {'date': now, 'count': count})

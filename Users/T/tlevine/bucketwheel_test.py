from scraperwiki import swimport
bucketwheel = swimport('bucketwheel')
from scraperwiki.sqlite import execute, commit

execute('drop table if exists stack')
commit()
bucketwheel.seed([bucketwheel.GetLinks('http://thomaslevine.com')])from scraperwiki import swimport
bucketwheel = swimport('bucketwheel')
from scraperwiki.sqlite import execute, commit

execute('drop table if exists stack')
commit()
bucketwheel.seed([bucketwheel.GetLinks('http://thomaslevine.com')])
from scraperwiki import swimport
from scraperwiki.sqlite import save, select
search = swimport('twitter_search').search
from time import sleep

# Broad search
search(['@nacue'])



# Summary statistics
d = select('from_user, count(*) as "tweet count" from `swdata` group by from_user')
save(['from_user'], d, 'counts-by-user')from scraperwiki import swimport
from scraperwiki.sqlite import save, select
search = swimport('twitter_search').search
from time import sleep

# Broad search
search(['@nacue'])



# Summary statistics
d = select('from_user, count(*) as "tweet count" from `swdata` group by from_user')
save(['from_user'], d, 'counts-by-user')
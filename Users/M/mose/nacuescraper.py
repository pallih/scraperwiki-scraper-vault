import scraperwiki

# Import Libraries

from scraperwiki import swimport
from scraperwiki.sqlite import save, select
search = swimport('twitter_search').search

# Broad search
search(['#englandsgreatest'])



# Summary statistics
hombre = select('from_user, count(*) as "tweet count" from `swdata` group by from_user')
save(['from_user'], hombre, 'counts-by-user')import scraperwiki

# Import Libraries

from scraperwiki import swimport
from scraperwiki.sqlite import save, select
search = swimport('twitter_search').search

# Broad search
search(['#englandsgreatest'])



# Summary statistics
hombre = select('from_user, count(*) as "tweet count" from `swdata` group by from_user')
save(['from_user'], hombre, 'counts-by-user')
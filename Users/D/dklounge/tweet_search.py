from scraperwiki import swimport
from scraperwiki.sqlite import save, select
search = swimport('twitter_search').search
from time import sleep

# Broad search
search(['picnic #tcamp12', 'from:TCampDC', '@TCampDC', '#tcamp12', '#viphack'])

# Search by user to get some more
users = [row['from_user'] + ' tcamp12' for row in \
    select('distinct from_user from swdata where from_user where user > "%s"' \
    % get_var('previous_from_user', ''))]

for user in users:
    search([user], num_pages = 2)
    save_var('previous_from_user', user)
    sleep(2)

# Summary statistics
d = select('from_user, count(*) as "tweet count" from `swdata` group by from_user')
save(['from_user'], d, 'counts-by-user')
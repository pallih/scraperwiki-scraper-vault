from scraperwiki import swimport
from scraperwiki.sqlite import save, select
search = swimport('twitter_search').search
from time import sleep

search(['#webcampkl','webcampkl'])

users = [row['from_user'] + ' webcampkl' for row in \
    select('distinct from_user from swdata where from_user where user > "%s"' \
    % get_var('previous_from_user', ''))]

for user in users:
    search([user], num_pages = 2)
    save_var('previous_from_user', user)
    sleep(2)

d = select('from_user, count(*) as "tweet count" from `swdata` group by from_user')
save(['from_user'], d, 'counts-by-user')
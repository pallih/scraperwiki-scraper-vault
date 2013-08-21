import scraperwiki
import datetime
try:
    scraperwiki.sqlite.execute("delete from wp_posts")
    scraperwiki.sqlite.commit()
except scraperwiki.sqlite.SqliteError:
    pass 

post_id = 123
parent_id = 99
title = 'A test'
content = '<b>Boo</b>'
slug='aboutus'
date_posted = datetime.datetime.now()
date_modified = date_posted

data = {
    'id': post_id,
    'post_type' : 'page',
    'post_parent' : parent_id,
    'post_title' : title,
    'content' : content,
    'post_name' : slug,
    'post_status' : 'publish',
    'post_author' : 1,
    'post_date' : date_posted,
    'post_date_gmt' : date_posted,
    'post_modified' : date_modified,
    'post_modified_gmt' : date_modified,
    'comment_status' : 'closed',
    'ping_status' : 'closed',
    'menu_order' : 1,
    'comment_count' : 0
}

scraperwiki.sqlite.save(unique_keys=['id'],
                        data=data, table_name='wp_posts')

result = scraperwiki.sqlite.select("max(id) as maxid from wp_posts")
print result[0]['maxid'] + 1


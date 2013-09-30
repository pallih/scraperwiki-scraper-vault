"""
Notes on the Canada Temperature Data scraper

4 millions rows: queries can be very slow.
An id index:
create index obs_id on obs(id);
speeds up:
select id,n from (select id,count(*) as n from obs group by id) where n >= 240;
from about 30 seconds to about 3 seconds.
This is still slow (ish):
select count(*) from (select id,count(*) as n from obs where element='tmeanM' group by id) where n >= 240;
at 17 seconds, and create an element index only speeds it up minimally (15 seconds);
but... creating an element,id index: create index obs_element_id on obs(element,id);
speeds that query up hugely: 1.4 seconds.

The time required to create an index exceeds scraperwiki's timeout on sqlite queries.
Indexes have to be created by hand by ross.
"""
"""
Notes on the Canada Temperature Data scraper

4 millions rows: queries can be very slow.
An id index:
create index obs_id on obs(id);
speeds up:
select id,n from (select id,count(*) as n from obs group by id) where n >= 240;
from about 30 seconds to about 3 seconds.
This is still slow (ish):
select count(*) from (select id,count(*) as n from obs where element='tmeanM' group by id) where n >= 240;
at 17 seconds, and create an element index only speeds it up minimally (15 seconds);
but... creating an element,id index: create index obs_element_id on obs(element,id);
speeds that query up hugely: 1.4 seconds.

The time required to create an index exceeds scraperwiki's timeout on sqlite queries.
Indexes have to be created by hand by ross.
"""

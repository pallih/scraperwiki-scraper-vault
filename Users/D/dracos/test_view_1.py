from icalendar import Calendar, Event
import scraperwiki

#CREATE TABLE `swdata` (`id` text, `time` text, `feature` text, `day`  text, `title` text, `desc_long` text, `contributors` text, `url` text,  `performances` text, `desc_short` text, `categories` text)

scraperwiki.sqlite.attach("bbc_proms_2011")
s = scraperwiki.sqlite.select('* FROM swdata ORDER BY day,time')
for row in s:
    print row['title']
    print row['desc_short']


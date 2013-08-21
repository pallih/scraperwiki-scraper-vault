from scraperwiki import swimport
from scraperwiki.sqlite import save, select, execute, commit
eventbrite = swimport('eventbrite')

def union(year, eventbrite_name, table_name):
    eventbrite.scrape('http://%s.eventbrite.com' % eventbrite_name, table_name)
    d = select('* from `%s`' % table_name)
    for row in d:
        row['year'] = year
    save([], d, 'tcamp')

def download():
    execute('CREATE TABLE IF NOT EXISTS `tcamp`'
        '(`year` integer, `first_scraped` real, `Twitter handle` text, `Intro for your fellow campers` text)')
    execute('DELETE FROM tcamp')
    union(2013, 'tcamp13', '2013')
    union(2012, 'tcamp12', '2012')
    union(2011, 'tcamp11', '2011')

def aggregate():
    execute('create table if not exists twitter (handle text, times integer)')
    execute('create unique index if not exists twitter_handle on twitter(handle)')
    execute('delete from twitter where 1 = 1')
    execute('insert into twitter '
        'select replace(`twitter handle`, "@", ""), count(*) from `tcamp` '
        'where `twitter handle` is not null group by [twitter handle]'
    )
    commit()

download()
aggregate()
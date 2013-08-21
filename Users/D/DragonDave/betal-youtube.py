import scraperwiki
import urlparse
import lxml.html
import cgi

#scraperwiki.sqlite.execute('drop table youtube')
#scraperwiki.sqlite.commit()
position=scraperwiki.sqlite.get_var('position')
print position
#if position==None: position=0
#position=0
scraperwiki.sqlite.attach('betal-populate','pop')

while True:
    print position
    pull=scraperwiki.sqlite.select('* from pop.raw limit 1000 offset ?', position)
    for row in pull:
        #print row['html']
        root=lxml.html.fromstring(row['html'])
        for x in root.xpath('//*/@*'):
            try:
                u=urlparse.urlparse(x)
            except Exception, e:
                print e
            query=None
            if 'youtube' in u.netloc and 'watch' in u.path:
                query= dict(cgi.parse_qsl(u.query)).get('v')
            if 'youtube' in u.netloc and '/v/' in u.path:
                query= u.path.split('/')[-1].partition('&')[0]
            if 'youtube' in u.netloc and '/embed/' in u.path:
                query= u.path.split('/')[-1].partition('&')[0]
            if query:
                tag=x._parent.tag
                print query, tag, row['link']
                scraperwiki.sqlite.save(table_name='youtube', data=[{'link':row['link'], 'query': query, 'tag':tag}], unique_keys=['query', 'link', 'tag'])
            
    position=position+len(pull)
    scraperwiki.sqlite.save_var('position',position)
    assert len(pull)>0


import scraperwiki

# Blank Python

#scraperwiki.sqlite.execute ("CREATE VIRTUAL TABLE texts USING fts3(wibble TEXT)")
scraperwiki.sqlite.save(table_name='texts', data={'wibble':

   """We were singin' ...
My my this here Anakin guy
May be Vader someday later - now he's just a small fry
And he left his home and kissed his mommy goodbye
Sayin' "Soon I'm gonna be a Jedi"""}, unique_keys=[])

print scraperwiki.sqlite.select('* from texts where wibble match "Jedi"')

#scraperwiki.sqlite.commit()

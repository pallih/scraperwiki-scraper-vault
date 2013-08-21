import scraperwiki

# Blank Python
sourcescraper = 'termcymru_english_welsh_translations'

scraperwiki.sqlite.attach('termcymru_english_welsh_translations', 'cy')
scraperwiki.sqlite.attach('whatdotheyknow_bodies', 'wdtk')

rows = scraperwiki.sqlite.select('a.en_term as en_term, a.cy_term as cy_term, b.`url name` as id from cy.swdata a inner join wdtk.swdata b on a.en_term = b.name')

#for row in rows:
#    print(dict((k, v.encode('utf-8')) for k, v in row.iteritems()))

#print runbook
for k in rows:
    print k


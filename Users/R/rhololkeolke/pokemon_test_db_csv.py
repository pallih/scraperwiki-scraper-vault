import scraperwiki

scraperwiki.sqlite.attach("pokemon_test_db")

data = scraperwiki.sqlite.select(           
    '''* from pokemon_test_db.swdata 
    order by pokeNum''')


for row in data:
    rowText = row['pokeNum'] + '\t' + row['bio'] + '\t' + row['type1'] + '\t'
    if(row['type2'] is not None):
        rowText = rowText + row['type2']
    else:
        rowText = rowText + ''
    rowText = rowText + '<br />'
    print rowText


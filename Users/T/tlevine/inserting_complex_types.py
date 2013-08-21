import scraperwiki
shopping_list = []
scraperwiki.sqlite.save([], {'shopping_list': shopping_list})
scraperwiki.sqlite.save([], {'sHopping_list': shopping_list})
data = scraperwiki.sqlite.select('SHOPPING_LIST from swdata')
print(data)

print([row['SHOPPING_LIST'] for row in data])

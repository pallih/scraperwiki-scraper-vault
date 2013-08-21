import scraperwiki

# Here is a simple Python dictionary containing one thing - a shop name
data = { 'shop_name' : 'Happy Shop'}

# We save the data using the datastore API - it can then be used by a view
# (in this case http://scraperwiki.com/views/example_shops_view )
scraperwiki.datastore.save(unique_keys=['shop_name'], data=data)




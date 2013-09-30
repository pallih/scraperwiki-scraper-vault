from scraperwiki import datastore
datastore.save(unique_keys=['key'], data={ 'key' : 'key_1', 'message' : 'HELLO_1' })
datastore.save(unique_keys=['key'], data={ 'key' : 'key_2', 'message' : 'HELLO_2' })
print "OK"

from scraperwiki import datastore
datastore.save(unique_keys=['key'], data={ 'key' : 'key_1', 'message' : 'HELLO_1' })
datastore.save(unique_keys=['key'], data={ 'key' : 'key_2', 'message' : 'HELLO_2' })
print "OK"


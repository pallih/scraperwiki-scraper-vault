# Unicode datastore test

# 20110811 - Modified Klaus

import scraperwiki

# This is a pound sign stored in a byte-string as UTF-8
s = '£'
# Its representation is '\xc2\xa3'
print repr(s)

# Save it to the datastore - 1st Record in the Database(in a Byte String as UTF-8

scraperwiki.sqlite.save(['test'], { 'test': 1, 'value': s} )

# Now decode it from a UTF-8 byte-string into a Python unicode character
s_decoded = s.decode('utf-8')

# That has a representation of a unicode string u'\xa3'

print 'PoundSignDecoded: ' ,repr(s_decoded)

print 'Pound Sterling Sign: ', ( u'\xa3'.encode("UTF-8"))

# Save it to the datastore -  2nd Record in the Database (in a Unicode String)

scraperwiki.sqlite.save(['test'], { 'test': 2, 'value': s_decoded} )

print s_decoded# Unicode datastore test

# 20110811 - Modified Klaus

import scraperwiki

# This is a pound sign stored in a byte-string as UTF-8
s = '£'
# Its representation is '\xc2\xa3'
print repr(s)

# Save it to the datastore - 1st Record in the Database(in a Byte String as UTF-8

scraperwiki.sqlite.save(['test'], { 'test': 1, 'value': s} )

# Now decode it from a UTF-8 byte-string into a Python unicode character
s_decoded = s.decode('utf-8')

# That has a representation of a unicode string u'\xa3'

print 'PoundSignDecoded: ' ,repr(s_decoded)

print 'Pound Sterling Sign: ', ( u'\xa3'.encode("UTF-8"))

# Save it to the datastore -  2nd Record in the Database (in a Unicode String)

scraperwiki.sqlite.save(['test'], { 'test': 2, 'value': s_decoded} )

print s_decoded
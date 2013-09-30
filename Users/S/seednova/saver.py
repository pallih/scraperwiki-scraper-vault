import scraperwiki


# save four records into the database
# data3 will over-write data1 because 
#    data3["first"], data3["last"] == data1["first"], data3["last"]

data1 = { "first":3, "last":"Smith", "age":23, "language":"python" }
#
scraperwiki.sqlite.save(unique_keys=["first"],table_name="words", data=data1)


# see the contents of the whole database ("swdata" is the default table name)
l =  scraperwiki.sqlite.select("* from words")
d = l[0]
print d['first']import scraperwiki


# save four records into the database
# data3 will over-write data1 because 
#    data3["first"], data3["last"] == data1["first"], data3["last"]

data1 = { "first":3, "last":"Smith", "age":23, "language":"python" }
#
scraperwiki.sqlite.save(unique_keys=["first"],table_name="words", data=data1)


# see the contents of the whole database ("swdata" is the default table name)
l =  scraperwiki.sqlite.select("* from words")
d = l[0]
print d['first']
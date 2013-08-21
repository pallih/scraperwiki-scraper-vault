import scraperwiki

# Blank Python

record = {}
testlist1 = ["rod","jane","freddy"]
for name in testlist1:
    record['name'] = name
    scraperwiki.sqlite.save(["name"], record, 'testdataset1')
    print record

secondrecord = {}
testlist2 = ["paul","george","ringo","john"]
for thing in testlist2:
    secondrecord['name2'] = thing
    scraperwiki.sqlite.save(["name2"], secondrecord, 'testdataset2')
    print secondrecord

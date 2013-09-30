import scraperwiki
superdictionary = {}
superlist       = []
superdictionary['1'] = {"a":1, "b":"Foo"}
superdictionary['1'].update({"c":"Bar"})
superdictionary['2'] = {"a":2, "b":"Grue", "c":"Gnu"}

for subdictionary in superdictionary:
    superlist.append(superdictionary[subdictionary])
scraperwiki.sqlite.save(["a"], superlist)
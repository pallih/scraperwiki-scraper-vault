import scraperwiki

# Blank Python

scraperwiki.sqlite.attach("fulllist", "src")


list = scraperwiki.sqlite.select("link from src.swdata limit 10")


for link in list:
    stringlink = str(link)
    print stringlink

    stringlink = stringlink.replace(' ', '')[:-2]
    print stringlink

    stringlink = stringlink[11:]
    print stringlink


"""

print test[0]
boom = str(test[0])
print "this is a string and then... " + boom
boom2 = boom.replace(' ', '')[:-2]

print boom2[11:]


for item in L:
        print item
"""import scraperwiki

# Blank Python

scraperwiki.sqlite.attach("fulllist", "src")


list = scraperwiki.sqlite.select("link from src.swdata limit 10")


for link in list:
    stringlink = str(link)
    print stringlink

    stringlink = stringlink.replace(' ', '')[:-2]
    print stringlink

    stringlink = stringlink[11:]
    print stringlink


"""

print test[0]
boom = str(test[0])
print "this is a string and then... " + boom
boom2 = boom.replace(' ', '')[:-2]

print boom2[11:]


for item in L:
        print item
"""
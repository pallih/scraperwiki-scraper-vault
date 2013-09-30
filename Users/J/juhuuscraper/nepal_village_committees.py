import scraperwiki
import lxml.html

wikipedia_utils = scraperwiki.swimport("wikipedia_utils")

# this page contains all the links from http://en.wikipedia.org/wiki/Village_development_committee
html = scraperwiki.scrape("http://juhahuuskonen.fi/2013/nepal-test/index.html")    
root = lxml.html.fromstring(html)

ldata = [ ]

for el in root.cssselect("a"):
#    print el.attrib['title']
    title = el.attrib['title']
    val = wikipedia_utils.GetWikipediaPage(title)
    res = wikipedia_utils.ParseTemplates(val["text"])
#    print res               # prints everything we have found in the text
#    print dict(res["templates"]).keys()
    data = dict(res["templates"])

    data_to_save = {'title': title}
    for k in data.keys():
        data2 = dict(data[k])
        for j in ["latd", "longd", "latm", "longm", "subdivision_name1"]:
            if j in data2:
                value_cleaned = data2[j].lstrip('[').rstrip(']')
                data_to_save[j] = value_cleaned

    if "latm" in data_to_save.keys():
        data_to_save["latd"] = data_to_save["latd"] + '.' + data_to_save["latm"]
        del data_to_save["latm"]
 
    if "longm" in data_to_save.keys():
        data_to_save["longd"] = data_to_save["longd"] + '.' + data_to_save["longm"]
        del data_to_save["longm"]

    for k in dict(res["templates"]).keys():
        if k.count("District") == 1:
            data_to_save["District"] = k

    print data_to_save
    ldata.append(data_to_save)

scraperwiki.sqlite.save(["title"], ldata, "Nepal village development committees")



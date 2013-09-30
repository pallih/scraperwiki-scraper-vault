import scraperwiki
import csv
import lxml.html
import time
import re
data = scraperwiki.scrape("http://other.lukehmu.com/REGIONAL.csv")
reader = csv.DictReader(data.splitlines())
london = ["4943", 7, "london"]
southeast = ["5381", 8, "southeast"]
southwest = ["5444", 6, "southwest"]
east = ["5496", 6, "east"]
eastmidlands = ["5526", 6, "eastmidlands"]
westmidlands = ["5556", 6, "westmidlands"]
wales = ["5604", 6, "wales"]
yorkshire = ["5634", 6, "yorkshire"]
northwest = ["5664", 6, "northwest"]
northeast = ["5694", 6, "northeast"]
ni = ["6081", 5, "ni"]
scotland = ["5736",6, "scotland"]
def regionswitch(currentregion):
    return {
        "london": london[0],
        "southeast": southeast[0],
        "southwest": southwest[0],
        "east": east[0],
        "eastmidlands": eastmidlands[0],
        "westmidlands": westmidlands[0],
        "wales": wales[0],
        "yorkshire": yorkshire[0],
        "northwest": northwest[0],
        "northeast": northeast[0],
        "ni": ni[0],
        "scotland": scotland[0]
        }[currentregion]
        
i = 0
for row in reader:
    if row['title'] and row['link']:
        #scraperwiki.sqlite.save(unique_keys=['link'], data=row, table_name="csv_table")
        html = scraperwiki.scrape(row['link'])
        root = lxml.html.fromstring(html)
        region = row['region']
        myimg = ""
        for elImg in root.cssselect("img.thumbnail"):
            if 'src' in elImg.attrib:
                myimg = elImg.attrib['src']
        if myimg:
            myimg = "http://www.cvqo.org" + myimg
            scraperwiki.sqlite.save(unique_keys=[], data={"id":i, "img_link":myimg}, table_name="img_table")
        else:
            scraperwiki.sqlite.save(unique_keys=[], data={"id":i, "img_link":"blank"}, table_name="img_table")
        for author in root.cssselect("a#dnn_ctr" + regionswitch(region) + "_ArticleList_ctl00_hypUser"):
            author = author.text_content()
        for date in root.cssselect("span#dnn_ctr" + regionswitch(region) + "_ArticleList_ctl00_lblDatePosted"):
            date = date.text_content()
        scraperwiki.sqlite.save(unique_keys=[], data={"id":i, "author":author, "date":date}, table_name="author_date")
    i += 1
import scraperwiki
import csv
import lxml.html
import time
import re
data = scraperwiki.scrape("http://other.lukehmu.com/REGIONAL.csv")
reader = csv.DictReader(data.splitlines())
london = ["4943", 7, "london"]
southeast = ["5381", 8, "southeast"]
southwest = ["5444", 6, "southwest"]
east = ["5496", 6, "east"]
eastmidlands = ["5526", 6, "eastmidlands"]
westmidlands = ["5556", 6, "westmidlands"]
wales = ["5604", 6, "wales"]
yorkshire = ["5634", 6, "yorkshire"]
northwest = ["5664", 6, "northwest"]
northeast = ["5694", 6, "northeast"]
ni = ["6081", 5, "ni"]
scotland = ["5736",6, "scotland"]
def regionswitch(currentregion):
    return {
        "london": london[0],
        "southeast": southeast[0],
        "southwest": southwest[0],
        "east": east[0],
        "eastmidlands": eastmidlands[0],
        "westmidlands": westmidlands[0],
        "wales": wales[0],
        "yorkshire": yorkshire[0],
        "northwest": northwest[0],
        "northeast": northeast[0],
        "ni": ni[0],
        "scotland": scotland[0]
        }[currentregion]
        
i = 0
for row in reader:
    if row['title'] and row['link']:
        #scraperwiki.sqlite.save(unique_keys=['link'], data=row, table_name="csv_table")
        html = scraperwiki.scrape(row['link'])
        root = lxml.html.fromstring(html)
        region = row['region']
        myimg = ""
        for elImg in root.cssselect("img.thumbnail"):
            if 'src' in elImg.attrib:
                myimg = elImg.attrib['src']
        if myimg:
            myimg = "http://www.cvqo.org" + myimg
            scraperwiki.sqlite.save(unique_keys=[], data={"id":i, "img_link":myimg}, table_name="img_table")
        else:
            scraperwiki.sqlite.save(unique_keys=[], data={"id":i, "img_link":"blank"}, table_name="img_table")
        for author in root.cssselect("a#dnn_ctr" + regionswitch(region) + "_ArticleList_ctl00_hypUser"):
            author = author.text_content()
        for date in root.cssselect("span#dnn_ctr" + regionswitch(region) + "_ArticleList_ctl00_lblDatePosted"):
            date = date.text_content()
        scraperwiki.sqlite.save(unique_keys=[], data={"id":i, "author":author, "date":date}, table_name="author_date")
    i += 1

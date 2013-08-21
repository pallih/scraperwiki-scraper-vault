import scraperwiki
import lxml.html
import itertools 


# Want to make it easy to grab new versions from index... some other time perhaps.

#html = scraperwiki.scrape("http://www.cdc.gov/mmwr/mmwr_su/mmwr_nd")
#root = lxml.html.fromstring(html) 
#
#runindex = 0#
#
#link = root.cssselect("h3")[runindex + 1].cssselect("a")[0].attrib["href"]
#print(root.cssselect("h3")[0].cssselect("a")[0].text)
#print(link)

# 2010
# html = scraperwiki.scrape('http://www.cdc.gov/mmwr/preview/mmwrhtml/mm5953a1.htm')

# 2009
html = scraperwiki.scrape('http://www.cdc.gov/mmwr/preview/mmwrhtml/mm5853a1.htm')

root = lxml.html.fromstring(html) 

levels = [None]*10

title = root.cssselect("div#content-main h1")[0].text
print title 


year = int(title[len(title) - 4:len(title)])
print year 

tables = [root.cssselect("table.Data-Table"), root.cssselect("table.data-table")]
allTables = list(itertools.chain(*tables))

for dataTable in allTables:
    if dataTable.cssselect("th.header-row p b")[0].text.find("TABLE 1.") > -1:
        for row in dataTable.cssselect("tbody tr"):
            data = row.cssselect("td")
            textElem = data[0].cssselect("p")[0]
            titleText = textElem.text
            clsIdx = textElem.attrib["class"]

            if clsIdx.find( "x7pt-footnote-supports-indent") > -1:
                continue

            if len(clsIdx) < 22:
                titleLvl = 1
            else:
                titleLvl = int(clsIdx[22])
            # 
            # print titleLvl
            levels[titleLvl - 1] = titleText
            levels[titleLvl:len(levels)] = [None]*(len(levels)-titleLvl)
            
            if len(data) > 12:
                disease = "|".join(str(level) for level in levels if level != None)
                print disease 

                for mon in range(1, 13):
                    paras = data[mon].cssselect("p") 
                    if len(paras) == 0:
                        # some rows have 13 cells, with no paras in data cells. These are not a data rows.
                        break
                    
                    incidenceTxt = paras[0].text
                    if incidenceTxt == None:
                        # Some rows have 13 cells, with empty paras. These are not a data rows.
                        break
                    print incidenceTxt 
                    try:
                        incidence = int(incidenceTxt)
                    except ValueError: 
                        incidence = 0

                    if mon == 13:
                       saveMon = None
                    else:
                       saveMon = mon
                    scraperwiki.sqlite.save(unique_keys=["disease", "year", "month"], data={"disease":disease, "year":year, "month": saveMon, "incidence":incidence}) 
            #for monIdx in [1:12]
            
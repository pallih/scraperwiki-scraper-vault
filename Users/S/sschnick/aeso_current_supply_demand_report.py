import scraperwiki
import lxml.html as lh

# parse the page - note that this html is broken (img tags not terminated), so it need to use the "parse" method
tree = lh.parse("http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet")
plant = dict()

# find all the row elements in the page
# note: the name of the facility is a "tail" of the img tag because of the broken html
rows = tree.findall("//tr")
for id, cells in enumerate(rows):
#    print len(cells), cells[0].text

    if len(cells) == 1:
        genType = cells[0].text
        plant["type"] = genType
        continue

    # only extract data from tables with four columns
    if len(cells) == 4:

        # only store Wind
        if genType <> "WIND": continue

        # has an image?
        imgs = cells[0].findall(".//img")
        if len(imgs) > 0:
            name = imgs[0].tail.strip()
        else:
            name = cells[0].text.strip()

        # the header row has no data, so skip it
        if not name: continue

        plant["name"] = name
        plant["mc"] = float(cells[1].text.strip())
        plant["tng"] = float(cells[2].text.strip())
        plant["dcr"] = float(cells[3].text.strip())

#        print plant

        scraperwiki.sqlite.save(unique_keys = ["name"], data = plant)


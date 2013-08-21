import scraperwiki
from lxml import etree

xml = scraperwiki.scrape("http://data.parliament.uk/EDMi/EDMi.svc/Member/List")

picklist = etree.XML(xml)

picklist_items_list = picklist.find("PickListItems")

picklist_items = picklist_items_list.findall("PickListItem")

for picklist_item in picklist_items:
    data = {
      'name' : picklist_item.text,
      'id' : picklist_item.attrib["id"]
    }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
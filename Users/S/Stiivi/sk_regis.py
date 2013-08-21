# encoding: UTF-8

# Blank Python
import scraperwiki
import re

BASE_URL="http://www.statistics.sk/pls/wregis/detail?wxidorg="
START_ID=1
STOP_ID=1146000
# STOP_ID = 5

def download(url):
    doc = scraperwiki.scrape(url)
    return unicode(doc, "iso-8859-2")

def parse(document, url, document_id):
    string = re.sub(r'[\n\r]/', '', document)
    string = re.sub(r"<((TR)|(tr))", "\n<TR", string)
    string = re.sub(r"<\/((TD)|(td))[^>]*>", "", string)
    string = re.sub(r"<[^>]+>", "", string)
    string = re.sub(r"&nbsp;", " ", string)
    string = re.sub(r"\n\s*\n", "\n", string)
    lines = string.splitlines()

    # line = 0
    # while line < len(lines):
    #     print "%d: %s" % (line, lines[line])
    #     line += 1

    record = {}
    record["document_id"] = document_id
    record["url"] = url

    line = 0
    while line < len(lines) and not lines[line].startswith(u"IČO"):
        line += 1

    if line >= len(lines):
        return record

    line += 1
    # print "%d: %s" % (line, lines[line])
    # print "%d: %s" % (line, lines[line+1])

    record["ico"] = lines[line].strip()
    record["name"] = lines[line+2].strip()
    record["legal_form"] = lines[line+4].strip()

    record["date_start"]  = lines[line+6].strip()
    record["date_end"]  = lines[line+8].strip()
    record["address"] = lines[line+10].strip()
    record["region"] = lines[line+12].strip()

    line += 12
    while line < len(lines) and not lines[line].startswith(u"Názov"):
        line += 1

    line += 4
    record["form_code"] = lines[line].strip()
    record["form"] = lines[line+1].strip()

    record["activity1_code"] = lines[line+3].strip()
    record["activity1"] = lines[line+4].strip()

    record["activity2_code"] = lines[line+6].strip()
    record["activity2"] = lines[line+7].strip()

    record["account_sector_code"] = lines[line+9].strip()
    record["account_sector"] = lines[line+10].strip()

    record["ownership_code"] = lines[line+12].strip()
    record["ownership"] = lines[line+13].strip()

    try:
        record["size_code"] = lines[line+15].strip()
        record["size"] = lines[line+16].strip()
    except:
        pass
    # self.output.append(record)
    return record

scraperwiki.sqlite.save_var( "data_columns", 
                [
                 'document_id', 'ico', 'name', 'legal_form',
            "date_start", "date_end", "address", "region", 
            "form_code", "form",
            "activity1_code", "activity1", "activity2_code", "activity2", 
            "account_sector_code", "account_sector", "ownership_code","ownership",
            "size_code", "size", "url"
                ]
        )

miss_count = 0
max_miss_count = 0
last_miss_start = 0

for i in range(START_ID, STOP_ID):
    url = "%s%d" % (BASE_URL, i)
    try:
        doc = download(url)
        record = parse(doc, url, i)
        scraperwiki.sqlite.save(["document_id"], record)
        last_miss_start = i
        miss_count = 0
    except:
        miss_count += 1
        max_miss_count = max([miss_count, max_miss_count])

        
scraperwiki.sqlite.save_var("last_id", STOP_ID)
scraperwiki.sqlite.save_var("max_miss_count", max_miss_count)
scraperwiki.sqlite.save_var("last_miss_start", last_miss_start)


    


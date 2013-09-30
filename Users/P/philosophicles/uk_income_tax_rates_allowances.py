import scraperwiki
import lxml.html
import re

def clean_up_text(s,chars_to_remove): return " ".join(re.sub(chars_to_remove,"",s).strip().split())


def parse_hmrc_webpage(html_root):
    """Returns a list of dicts representing the data in the HTML tables on this page"""

    page_data = []
    chars_to_strip = "[\n\r]"

    # Get each html table on the page, in turn
    for grid in html_root.cssselect("table"):
        table_name = grid.cssselect("caption")[0].text_content()

        # The table's top row has the years on.  
        # enumerate() helps to tie up with values later.
        years = {}
        for colNo,year in enumerate(grid.cssselect("thead th.colHeader p")):
            years[colNo] = year.text_content()

        # Now iterate through the rest of the table, 
        # building a dict for every cell then appending to data
        for row in grid.cssselect("tbody tr"):
            for colNo,cellContent in enumerate(row.cssselect("td")):
                D = {}
                D["table"] = clean_up_text(table_name,chars_to_strip)
                D["year"] = clean_up_text(years[colNo+1],chars_to_strip)
                D["fact"] = clean_up_text(row.cssselect("th.colHeader")[0].text_content(),chars_to_strip)
                D["value"] = cellContent.text_content()
                page_data.append(D)

    return page_data


if "swdata" not in scraperwiki.sqlite.show_tables():
    scraperwiki.sqlite.execute("create table swdata (`table` string, year string, fact string, value string)") 
    scraperwiki.sqlite.commit()

pages_to_scrape = ["http://www.hmrc.gov.uk/rates/it.htm","http://www.hmrc.gov.uk/rates/nic.htm"]

for page in pages_to_scrape:
    html_page = scraperwiki.scrape(page)
    root = lxml.html.fromstring(html_page)
    data = parse_hmrc_webpage(root)
    scraperwiki.sqlite.save(["table","year","fact"], data)import scraperwiki
import lxml.html
import re

def clean_up_text(s,chars_to_remove): return " ".join(re.sub(chars_to_remove,"",s).strip().split())


def parse_hmrc_webpage(html_root):
    """Returns a list of dicts representing the data in the HTML tables on this page"""

    page_data = []
    chars_to_strip = "[\n\r]"

    # Get each html table on the page, in turn
    for grid in html_root.cssselect("table"):
        table_name = grid.cssselect("caption")[0].text_content()

        # The table's top row has the years on.  
        # enumerate() helps to tie up with values later.
        years = {}
        for colNo,year in enumerate(grid.cssselect("thead th.colHeader p")):
            years[colNo] = year.text_content()

        # Now iterate through the rest of the table, 
        # building a dict for every cell then appending to data
        for row in grid.cssselect("tbody tr"):
            for colNo,cellContent in enumerate(row.cssselect("td")):
                D = {}
                D["table"] = clean_up_text(table_name,chars_to_strip)
                D["year"] = clean_up_text(years[colNo+1],chars_to_strip)
                D["fact"] = clean_up_text(row.cssselect("th.colHeader")[0].text_content(),chars_to_strip)
                D["value"] = cellContent.text_content()
                page_data.append(D)

    return page_data


if "swdata" not in scraperwiki.sqlite.show_tables():
    scraperwiki.sqlite.execute("create table swdata (`table` string, year string, fact string, value string)") 
    scraperwiki.sqlite.commit()

pages_to_scrape = ["http://www.hmrc.gov.uk/rates/it.htm","http://www.hmrc.gov.uk/rates/nic.htm"]

for page in pages_to_scrape:
    html_page = scraperwiki.scrape(page)
    root = lxml.html.fromstring(html_page)
    data = parse_hmrc_webpage(root)
    scraperwiki.sqlite.save(["table","year","fact"], data)
import scraperwiki
import urlparse
import lxml.html

def scrape_table(root):
    rows = root.cssselect("table tr")
    for row in rows:
        record = {}
        table_cells = row.cssselect("td")
        if table_cells: 
            record['Place'] = table_cells[0].text_content()
            table_cellsurl = table_cells[0].cssselect("a")
            record['URL'] = table_cellsurl[0].attrib.get('href')
            record['Address'] = table_cells[1].text_content()
            #record['Postcode'] = table_cells[1].text_content()
            #(GIR 0AA)|((([A-Z-[QVX]][0-9][0-9]?)|(([A-Z-[QVX]][A-Z-[IJZ]][0-9][0-9]?)|(([A-Z-[QVX‌]][0-9][A-HJKSTUW])|([A-Z-[QVX]][A-Z-[IJZ]][0-9][ABEHMNPRVWXY]))))\s?[0-9][A-Z-[C‌IKMOV]]{2})
            print record, '******'
            scraperwiki.sqlite.save(["Place"], record)

def scrape_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)

base_url = 'http://www.ukjockey.com/maps.html'
scrape_link(base_url)

#,'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
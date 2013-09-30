import scraperwiki

def main():
    scraperwiki.sqlite.attach("beermad_brewery_urls", "src")
    print scraperwiki.sqlite.table_info("src.swdata")

main()
import scraperwiki

def main():
    scraperwiki.sqlite.attach("beermad_brewery_urls", "src")
    print scraperwiki.sqlite.table_info("src.swdata")

main()

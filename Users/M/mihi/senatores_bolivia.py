import scraperwiki
import lxml.html

base="http://www.senado.bo/lista_de_senadores/pagina%s" #the base URL for all our scraping. Note how it's always pagina+number

pages=[base%n for n in range(1,9)] #create the list of pages

def extract_text(s):
    try:
        return s[0].text_content()
    except AttributeError:
        return str(s[0])

def parse_page(page):
    """ The function to parse pages and extract Senator information"""
    h=scraperwiki.scrape(page)
    r=lxml.html.fromstring(h)
    senators=r.xpath("//div/div/div[2]/div/div/div")
    mapping={"name":"./p[1]",
            "type":"./p[2]",
            "party":"./p[3]",
            "district":"./p[4]",
            "email":"./p[5]",
            "image_url":"./img/@src"}
    for s in senators:
        data=dict([(k,extract_text(s.xpath(x))) for (k,x) in mapping.items()])
        scraperwiki.sqlite.save(unique_keys=["email"],data=data)

for p in pages:
    parse_page(p)
        

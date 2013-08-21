import scraperwiki

# http://www.tse.jus.br/bu/2008/o/1/pr/75353/XXXX/pro175353XXXXYYYY.html
# XXXX zona
# YYYY secao

url = "http://www.tse.jus.br/bu/2008/o/1/pr/75353/%04s/pro175353%04s%04d.html"



zonas = [
    { "codigo": "0001", "start": 51, "end": 596 },
    { "codigo": "0002", "start": 56, "end": 534 },
    { "codigo": "0003", "start": 50, "end": 634 },
    { "codigo": "0004", "start": 179, "end": 564 },
    { "codigo": "0145", "start": 288, "end": 744 },
    { "codigo": "0174", "start": 1, "end": 340 },
    { "codigo": "0175", "start": 1, "end": 314 },
    { "codigo": "0176", "start": 1, "end": 268 },
    { "codigo": "0177", "start": 1, "end": 364 },
    { "codigo": "0178", "start": 1, "end": 320 }

]


for zona in zonas:
    #print(zona["codigo"])
    for secao in range(zona["start"], zona["end"]):
        print("%04s: %04d" % (zona["codigo"], secao))
        url_scrap = url % (zona["codigo"], zona["codigo"], secao)
        html = scraperwiki.scrape(url_scrap)
        print(url_scrap)
        print(html)
        
        







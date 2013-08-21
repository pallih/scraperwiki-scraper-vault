import scraperwiki
import lxml.html 
p = 0
base_url = "http://www.catinabib.it/"
catalog_url = "?q=digitalib/res_in_coll/247&page="
info_url = "/?q=node/"
img_url = "http://www.catinabib.it/files/"
dublincore_url = "http://www.catinabib.it/?q=digitalib/generate_dc/"
mag_url = "http://www.catinabib.it/?q=digitalib/generate_mag/"
html = scraperwiki.scrape(base_url + catalog_url + str(p))
root = lxml.html.fromstring(html) 
last_page= root.cssselect("li.pager-last a")[0].attrib['href'].split("page=")[1]
tables = root.cssselect("div.node")
for table in tables:
    internal_id = table.cssselect("h2 a")[0].attrib['href'].replace(info_url,"")
    infohtml = lxml.html.fromstring(scraperwiki.scrape(base_url + info_url + str(internal_id)))
    fields = infohtml.cssselect("fieldset")
    raccolta = fields[0].cssselect("div")[0].text_content().replace("Raccolta: ","")
    foto = fields[1].cssselect("img")[0].attrib['src'].replace('/?q=digitalib/reduced/','')
    for f in fields[2]:
        v = lxml.html.tostring(f)
        if ((v[0:3] != '<br') and (v[0:3] != '<di')):
            campo = v.split(": ")[0].replace("<b>","").replace("</b>","")
            valore = v.split(": ")[1]
        dublincore = dublincore_url + internal_id
        mag = mag_url + id


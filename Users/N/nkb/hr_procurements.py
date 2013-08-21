import scraperwiki
from lxml import etree
import lxml.html
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

def findElement(element, root):
    try:
        return root.cssselect("span#uiDokumentPodaci_ui" + element)[0].text.encode("iso-8859-1")
    except:
        return ""

# Find how many records are in the DB already
num_rows = scraperwiki.sqlite.execute('SELECT COALESCE(MAX(id)+1, 0) FROM swdata')

#extracts the number of records in the DB
start = num_rows['data'][0][0]
end = start + 10000

for doc_id in range(start, end):

    url = "https://eojn.nn.hr/SPIN/application/ipn/DocumentManagement/DokumentPodaciFrm.aspx?id=" + str(doc_id)
    
    try:
        html = scraperwiki.scrape(url)
        
        root = lxml.html.fromstring(html)
        
        Narucitelj = findElement("Narucitelj", root)
        Broj = findElement("BrojObjave", root)
        Naziv = findElement("Naslov", root)
        Vrsta_dokumenta = findElement("VrstaObjave", root)
        Vrsta_ugovora = findElement("VrstaUgovora", root)
        CPV = findElement("Cpv", root)
        Vrsta_postupka = findElement("VrstaPostupka", root)
        Proc_vrijed = findElement("ProcijenjenaVrijednost", root)
        Datum_slanja = root.cssselect("span[title='Datum slanja']")[1].text
        Datum_objave = root.cssselect("span[title='Datum objave']")[1].text
    
        data = {
            'id': str(doc_id),
            'Narucitelj': Narucitelj,
            'Broj': Broj,
            'Naziv': Naziv,
            'Vrsta_dokumenta': Vrsta_dokumenta,
            'Vrsta_ugovora': Vrsta_ugovora,
            'CPV': CPV,
            'Vrsta_postupka': Vrsta_postupka,
            'Proc_vrijed': Proc_vrijed,
            'Datum_slanja': Datum_slanja,
            'Datum_objave': Datum_objave
        }
    
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

    except:
        data = {
            'id': str(doc_id),
            'Error': 'true'
        }
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)
        
        pass

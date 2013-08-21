import scraperwiki           
import lxml.html
from scrapely import Scraper
from rdflib import RDF
from rdflib.graph import Graph
from rdflib import Literal, BNode, Namespace

catalogUrlFormat ='http://www.omnibusrevue.de/buskatalog-578829.html?skip=%d'
busUrlFormat = 'http://www.omnibusrevue.de/bus-%s.html'
busUrlFormatWithName = 'http://www.omnibusrevue.de/{0}-{1}.html'

exampleData = {'maker': 'Volvo Busse Deutschland GmbH', 
    'model': '8900R', 
    'type': 'Überlandbus', 
    'length': '12.097', 
    'width': '2.550', 
    'height': '3.300', 
    'floorHeight': '860', 
    'luggageSpace': '8,00', 
    'axlesCount': '2', 
    'wheelbase': '6.000', 
    'grossWeight': '19,00', 
    'netWeight': '11,50', 
    'seats': '47', 
    'engine': 'D7E290', 
    'engineNorm': 'Euro 5, EEV', 
    'emissionControl': 'SCR', 
    'displacement': '7,14', 
    'cylinders': '6', 
    'power': '213 (290)', 
    'maxTorque': 'k.A', 
    'gearbox': 'Voith / ZF', 
    'suspension': 'Luft / Luft', 
    'steering': 'ZF Servocom'}

BUS = Namespace("http://purl.org/wikibus/omnibusrevue/")
OR = Namespace("http://purl.org/wikibus/omnibusrevue/bus/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")

def CreateGraph(busId, busData):
    graph = Graph()
    busRes = OR[busId]
    graph.add((busRes, RDF.type, BUS["Bus"]))
    graph.add((busRes, FOAF["page"], Literal(busUrlFormatWithName.format(busData[0]['model'][0].encode('utf-8'), busId))))
    for key in busData[0]:        
        obj = busData[0][key][0].encode('utf-8')
        if obj <> "k.A":
            graph.add((busRes, BUS[key], Literal(obj)))
    return graph.serialize(format='turtle')

busScraper = Scraper()
busScraper.train(busUrlFormat % '1120301', exampleData)

offset = 0
while True:
    html = scraperwiki.scrape(catalogUrlFormat % offset)
    root = lxml.html.fromstring(html)
    busIds = root.cssselect('input[type=checkbox]')
    if len(busIds) > 0:
        for busCheckbox in busIds:
            busUrl = busUrlFormat % busCheckbox.attrib['value']
            busGraph = CreateGraph(busCheckbox.attrib['value'], busScraper.scrape(busUrl))
            dataStored = {'url': busUrl, 'graph': busGraph}
            scraperwiki.sqlite.save(unique_keys=['url'], data=dataStored)
        offset += 20
    else:
        break
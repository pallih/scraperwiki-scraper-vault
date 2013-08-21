import scraperwiki
import json

sourcescraper = 'argentina_compra_-_proveedores'

params = scraperwiki.utils.GET()

scraperwiki.sqlite.attach(sourcescraper)

encoder = json.JSONEncoder()
answer = scraperwiki.sqlite.select('* from swdata where Cuit like "%%%s%%"' % params['cuit'])
print encoder.encode(answer)

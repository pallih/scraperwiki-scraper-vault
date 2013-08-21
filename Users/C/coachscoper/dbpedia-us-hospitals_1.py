import csv
from lxml import etree
import re
import scraperwiki
from StringIO import StringIO
from urllib import urlencode

NSMAP = {
    'dbpedia-owl': 'http://dbpedia.org/ontology/',
    'dbpprop': 'http://dbpedia.org/property/',
    'dcterms': 'http://purl.org/dc/terms/',
    'foaf': 'http://xmlns.com/foaf/0.1/',
    'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
    'georss': 'http://www.georss.org/georss/',
    'n0pred': 'http://dbpedia.org/property/org/',
    'owl': 'http://www.w3.org/2002/07/owl#',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
}
SPARQL = '''\
PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
PREFIX dbpedia2: <http://dbpedia.org/property/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?hospital
WHERE {
?s foaf:page ?hospital .
?s rdf:type <http://dbpedia.org/ontology/Hospital> .
?s dbpedia-owl:country ?country;
   dbpedia2:country ?propcountry .
FILTER (?propcountry = "United States" || ?propcountry = "US")
}'''
US_URL = 'http://dbpedia.org/resource/Category:Hospitals_in_the_United_States_by_state'
XMLNS_RE = re.compile(r'xmlns:([-\w]+)="(.+?)"')


def csv_url(sparql):
    params = {
        'default-graph-uri': 'http://dbpedia.org',
        'query': sparql,
        'format': 'text/csv',
    }
    return 'http://dbpedia.org/sparql?%s' % urlencode(params)


def describe_csv_url(base_url):
    return csv_url('DESCRIBE <%s>' % base_url)


def parse_csv(url, parse_row_func):
    data = StringIO()
    data.write(scraperwiki.scrape(url))
    data.seek(0)

    data_csv = csv.DictReader(data)

    for row in data_csv:
        parse_row_func(row)


def parse_us_data(row):
    if row['predicate'] == 'http://www.w3.org/2004/02/skos/core#broader':
        parse_csv(describe_csv_url(row['subject']), parse_state_data)


def parse_state_data(row):
    if row['predicate'] == 'http://purl.org/dc/terms/subject':
        parse_hospital_data(row['subject'])


class DBpediaRDF(object):

    def __init__(self, resource):
        self._resource = resource
        self._url = '%s.rdf' % resource.replace('/resource/', '/data/')
        self._xml_data = scraperwiki.scrape(self._url)
        #self._nsmap = dict(set(XMLNS_RE.findall(self._xml_data)))
        self._xml = etree.fromstring(self._xml_data)

    @property
    def base_xpath_expr(self):
        return '/rdf:RDF/rdf:Description[@rdf:about="%s"]' % self._resource

    def xpath_text(self, expr):
        if '/' not in expr and '[' not in expr:
            # HACK - assume it's just a FQ tag name
            if expr not in self._xml_data:
                return None
        return self.xpath('%s/text()' % expr)

    def xpath(self, expr):
        result = self._xml.xpath('%s/%s' % (self.base_xpath_expr, expr),
#                                 namespaces=self._nsmap)
                                 namespaces=NSMAP)
        if len(result) > 0:
            return result[0]
        else:
            return None


def parse_sparql_result(row):
    print row


def parse_hospital_data(resource_url):
    hospital = DBpediaRDF(resource_url)
    data = {
        'resource': resource_url,
        'name': hospital.xpath_text('foaf:name'),
        'organization': hospital.xpath_text('dbpprop:affiliation'),
        'latitude': hospital.xpath_text('geo:lat'),
        'longitude': hospital.xpath_text('geo:long'),
        'website': hospital.xpath_text('dbpprop:website'),
        'description': hospital.xpath_text('dbpedia-owl:abstract'),
        'category': hospital.xpath_text('dbpprop:healthcare'),
    }
    if data['name'] and data['latitude'] and data['longitude']:
        scraperwiki.sqlite.save(unique_keys=['resource'], data=data)

parse_csv(describe_csv_url(US_URL), parse_us_data)
#parse_csv(csv_url(SPARQL), parse_sparql_result)

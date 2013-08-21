import scraperwiki
import lxml.html         

class InfojobsScraper ( object ):
    
    def __init__ ( self ):
        self.items = { \
            'oferta'     : 'h1.heading-a', \
            'fecha'      : '#prefijoFecha', \
            'empresa'    : '#prefijoEmpresa', \
            'poblacion'  : '#prefijoPoblacion', \
            'descripcion': '#prefijoDescripcion1', \
            'requisitos' : '#prefijoReqMinimos', \
            'salario'    : '#prefijoSalario' } 
        self.urls = self.load_urls()    
    
    def load_urls ( self ):
        urls = []
    
        #debug 
        print scraperwiki.sqlite.show_tables()
    
        table = scraperwiki.sqlite.table_info("vacants")
        
        if table:
            print table
            q = scraperwiki.sqlite.execute( 'select url from vacants' )
            for row in q['data']:
                urls.append(row[0])
        else:
            print 'empty'
            
            create = 'create table vacants ('
            for field in self.items:
                create += field + ' string, '
            create += ' url string )'
            
            scraperwiki.sqlite.execute( create )
    
        return urls
    
    def save_job ( self, url, keywords ):
        print url
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
    
        row = { 'url': url, 'keywords': keywords }
        
        for key in self.items:
            item = root.cssselect(self.items[key])
            value = ''
            if item:
                value = item[0].text_content()
            row[key] = value
    
        print row
    
        scraperwiki.sqlite.save( unique_keys = ['url'], data = row, table_name = 'vacants' )
    
    def fetch_jobs ( self, keywords, inicio ):
        
        params = { \
            'of_area'           : 0, \
            'of_provincia'      : 9, \
            'origen_accion'     : 0, \
            'palabra'           : keywords, \
            'origen_busqueda'   : 0, \
            'canal'             : 0, \
            'inicio'            : inicio
        }
        
        html    = scraperwiki.scrape( 'https://www.infojobs.net/jobsearch/search-results/list.xhtml', params )
        root    = lxml.html.fromstring(html)
        vacants = root.cssselect('h2.title a')
    
        for vac in vacants:
            url = 'http:' + vac.get('href')
            print 'get url ' + url
            if not (url in self.urls ):
                self.save_job( url, keywords )
            else:
                print 'url exists: ' + url


# scraper

scraper = InfojobsScraper()

for i in range( 4 ):
    for k in ['php', 'ios', 'iphone', 'linux', 'delphi']:
        scraper.fetch_jobs( k, 1 + i )
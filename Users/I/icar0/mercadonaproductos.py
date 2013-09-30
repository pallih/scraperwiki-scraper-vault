import urllib2
from lxml.html import fromstring
from lxml.html.clean import clean_html
import re
import scraperwiki
from scraperwiki.sqlite import save,execute

#This info must be changed
cookie_info = "mercadona_username=ICARHGM; mercadona_idioma=1; TELECOMPRA_MERCADONA=4c8b7de514cb58c2105f0e0a74cc7cd4; mercadona_username=ICARHGM"

START_URL = "https://www.mercadona.es/sfprincipal.php?pag_origen=entrada.php&CP=&Pais=34&Provincia=&Localidad=&TiendaVisita=1&EntradaUsername=1&AyudaPassword="
URL_FIND = "sfprincipal.php?page=buscador&id_seccion="
URL_PRODUCT = "https://www.mercadona.es/sfprincipal.php?page=sflista&id_seccion="
headers = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.3) Gecko/20091020 Ubuntu/9.10 (karmic) Firefox/3.6.0' 

def get_content(url):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie',cookie_info))
    opener.addheaders.append(('User-Agent',headers))
    req = opener.open(url)
    clean_text = clean_html(req.read())
    root = fromstring(clean_text)
    main_node = root.getroottree()
    return main_node

def get_item_tree(root_node):
    caters = root_node.xpath('//a[@class="level1"]/@href')
    caters_name = root_node.xpath('//a[@class="level1"]/text()')
    for (cat,name) in zip(caters,caters_name):
        val = int(re.findall('id_seccion=([0-9]*)',cat)[0])
        save(['id'],{'id':val,'name':name.encode('latin-1'),'parent':0,'leaf':0},table_name='categorias')
        get_children_from_cat(root_node,val)
    
def get_children_from_cat(root_node,val):
    sub = root_node.xpath('//a[@href="' + URL_FIND + str(val) + '"]/following-sibling::ul/li/a/text()')
    sub_href = root_node.xpath('//a[@href="' + URL_FIND + str(val) + '"]/following-sibling::ul/li/a/@href')
    if(len(sub) > 0):
        for ref,name in zip(sub_href,sub):
            val_n  = int(re.findall('id_seccion=([0-9]*)',ref)[0])
            save(['id'],{'id':val_n,'name':name.encode('latin-1'),'parent':val,'leaf':0},table_name='categorias')
            get_children_from_cat(root_node,val_n)
    else:
        scraperwiki.sqlite.execute("UPDATE categorias SET 'leaf'=1 WHERE 'id'=?", [val])

def get_products_from_url(url,result):
    node = get_content(url)
    #La url tiene que llevar la variable #page = sflista
    #assert(re.search("sflista",url) != None)
    descripcion = node.xpath('//table[@class="tablaproductos"][1]/tbody/tr/td[@headers="header1"]/span/text()')
    precio = node.xpath('//table[@class="tablaproductos"][1]/tbody/tr/td[@headers="header2"]/span[starts-with(@id,"txtPrecio")]/text()')
    keyid = 0;
    for (i,j) in zip(descripcion,precio):
        result.insert(-1,{'desc':i,'precio':j})
    #Las tablas incluyen 3 datos Articulo Precio Precio/Kilo
    #assert((descripcion.__len__() + 1 ) % 3 == 0)
    #for i in range(0,descripcion.__len__(),3):
        #save(['id'],{'id':keyid,'Articulo':descripcion[i],'Precio':descripcion[i+1],'PrecioKilo':descripcion[i+2]})
    #    keyid = keyid + 1

def get_products():
    resultado = []
    id = 0
    lista = select("id from categorias WHERE leaf=1")
    for element in lista:
        get_products_from_url(URL_PRODUCT + str(element),resultado)
    for elem in resultado:
        save(['id'],{'id':int(id),'descripcion':elem['desc'],'precio':elem['precio']},table_name='articulos')
        id = id+1
node = get_content(START_URL)
get_item_tree(node)
import urllib2
from lxml.html import fromstring
from lxml.html.clean import clean_html
import re
import scraperwiki
from scraperwiki.sqlite import save,execute

#This info must be changed
cookie_info = "mercadona_username=ICARHGM; mercadona_idioma=1; TELECOMPRA_MERCADONA=4c8b7de514cb58c2105f0e0a74cc7cd4; mercadona_username=ICARHGM"

START_URL = "https://www.mercadona.es/sfprincipal.php?pag_origen=entrada.php&CP=&Pais=34&Provincia=&Localidad=&TiendaVisita=1&EntradaUsername=1&AyudaPassword="
URL_FIND = "sfprincipal.php?page=buscador&id_seccion="
URL_PRODUCT = "https://www.mercadona.es/sfprincipal.php?page=sflista&id_seccion="
headers = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.3) Gecko/20091020 Ubuntu/9.10 (karmic) Firefox/3.6.0' 

def get_content(url):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie',cookie_info))
    opener.addheaders.append(('User-Agent',headers))
    req = opener.open(url)
    clean_text = clean_html(req.read())
    root = fromstring(clean_text)
    main_node = root.getroottree()
    return main_node

def get_item_tree(root_node):
    caters = root_node.xpath('//a[@class="level1"]/@href')
    caters_name = root_node.xpath('//a[@class="level1"]/text()')
    for (cat,name) in zip(caters,caters_name):
        val = int(re.findall('id_seccion=([0-9]*)',cat)[0])
        save(['id'],{'id':val,'name':name.encode('latin-1'),'parent':0,'leaf':0},table_name='categorias')
        get_children_from_cat(root_node,val)
    
def get_children_from_cat(root_node,val):
    sub = root_node.xpath('//a[@href="' + URL_FIND + str(val) + '"]/following-sibling::ul/li/a/text()')
    sub_href = root_node.xpath('//a[@href="' + URL_FIND + str(val) + '"]/following-sibling::ul/li/a/@href')
    if(len(sub) > 0):
        for ref,name in zip(sub_href,sub):
            val_n  = int(re.findall('id_seccion=([0-9]*)',ref)[0])
            save(['id'],{'id':val_n,'name':name.encode('latin-1'),'parent':val,'leaf':0},table_name='categorias')
            get_children_from_cat(root_node,val_n)
    else:
        scraperwiki.sqlite.execute("UPDATE categorias SET 'leaf'=1 WHERE 'id'=?", [val])

def get_products_from_url(url,result):
    node = get_content(url)
    #La url tiene que llevar la variable #page = sflista
    #assert(re.search("sflista",url) != None)
    descripcion = node.xpath('//table[@class="tablaproductos"][1]/tbody/tr/td[@headers="header1"]/span/text()')
    precio = node.xpath('//table[@class="tablaproductos"][1]/tbody/tr/td[@headers="header2"]/span[starts-with(@id,"txtPrecio")]/text()')
    keyid = 0;
    for (i,j) in zip(descripcion,precio):
        result.insert(-1,{'desc':i,'precio':j})
    #Las tablas incluyen 3 datos Articulo Precio Precio/Kilo
    #assert((descripcion.__len__() + 1 ) % 3 == 0)
    #for i in range(0,descripcion.__len__(),3):
        #save(['id'],{'id':keyid,'Articulo':descripcion[i],'Precio':descripcion[i+1],'PrecioKilo':descripcion[i+2]})
    #    keyid = keyid + 1

def get_products():
    resultado = []
    id = 0
    lista = select("id from categorias WHERE leaf=1")
    for element in lista:
        get_products_from_url(URL_PRODUCT + str(element),resultado)
    for elem in resultado:
        save(['id'],{'id':int(id),'descripcion':elem['desc'],'precio':elem['precio']},table_name='articulos')
        id = id+1
node = get_content(START_URL)
get_item_tree(node)

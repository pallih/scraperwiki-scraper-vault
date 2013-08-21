import scraperwiki
import lxml.html
import re
import inspect

SITE_ROOT = 'http://www.dati.piemonte.it'
CATALOG_PAGINATION = SITE_ROOT + '/dato/index.php?option=com_rd&view=cerca&pagina='
FIRST_CATALOG_PAGE = CATALOG_PAGINATION + str(1)

def callername():
    return inspect.stack()[2][3]
    
_date_pattern = re.compile('(\d{,2})/(\d{,2})/(\d{4}) ?((\d{,2}):(\d{2}):(\d{2}))?')
def _normalize_date(date_str):
    (dd, mm, yyyy, datetime, hh, mi, ss) = _date_pattern.search(date_str).groups()
    return '%d-%d-%d' % (int(yyyy), int(mm), int(dd)) + ( datetime if datetime else '' )

def _func_name_attr_value(attr_value_dom):
    value = attr_value_dom.text_content().strip()
    cname = callername()
    if cname.endswith('_date'): value = _normalize_date(value)
    return { cname.replace('_process_', '') : value }

def _process_license(attr_value_dom):
    img_lic = attr_value_dom.cssselect('img')[0].get('src')
    if 'lic_b_cc0.gif' in img_lic: 
        return {'license' : 'cc0'}
    elif 'lic_b_cc-by.gif' in img_lic:
        return {'license' : 'cc-by'}
    else:
        raise Exception('Unknown license: ' + img_lic)

def _process_filetype(attr_value_dom):
    return _func_name_attr_value(attr_value_dom)

_download_re = re.compile("scarica[C0]*\(\'([^\']+)\'\)")
def _process_download(attr_value_dom):
    onclick = attr_value_dom.cssselect('img')[0].get('onclick')
    return {'download' : SITE_ROOT + '/' + _download_re.findall(onclick)[0] }

def _process_description(attr_value_dom):
    return _func_name_attr_value(attr_value_dom)   

def _process_tags(attr_value_dom):
    return _func_name_attr_value(attr_value_dom)   

def _process_subjects(attr_value_dom):
    return _func_name_attr_value(attr_value_dom)   

def _process_curator(attr_value_dom):
    return _func_name_attr_value(attr_value_dom)   

def _process_datatype(attr_value_dom):
    return _func_name_attr_value(attr_value_dom)   

def _process_source(attr_value_dom):
    return _func_name_attr_value(attr_value_dom)   

def _process_update_frequency(attr_value_dom):
    return _func_name_attr_value(attr_value_dom)   

def _process_creation_date(attr_value_dom):
    return _func_name_attr_value(attr_value_dom)   

def _process_modification_date(attr_value_dom):
    return _func_name_attr_value(attr_value_dom)   

def _process_meta_modification_date(attr_value_dom):
    return _func_name_attr_value(attr_value_dom)   

def _process_expiration_date(attr_value_dom):
    return _func_name_attr_value(attr_value_dom)   

def _process_scale(attr_value_dom):
    return _func_name_attr_value(attr_value_dom)   

def _process_srs(attr_value_dom):
    return _func_name_attr_value(attr_value_dom)

attribute_actions = {\
    'licenza'                             : _process_license,
    'tipo di file'                        : _process_filetype,
    'download'                            : _process_download,
    'descrizione'                         : _process_description,
    'parole chiave'                       : _process_tags,
    'argomenti'                           : _process_subjects,
    'enti'                                : _process_curator,
    'tipo di dato'                        : _process_datatype,
    'fonte del dato'                      : _process_source,
    'frequenza di aggiornamento'          : _process_update_frequency,
    'data creazione'                      : _process_creation_date,
    'data di ultima modifica al dato'     : _process_modification_date,
    'data di ultima modifica al metadato' : _process_meta_modification_date,
    'data di scadenza del dato'           : _process_expiration_date,
    'scala'                               : _process_scale,
    'sistema di riferimento'              : _process_srs
}

def process_dataset_page(dataset_path):
    print 'Processing Dataset Page:', dataset_path
    dataset_page_url  = SITE_ROOT + dataset_path
    dataset_page_html = scraperwiki.scrape(dataset_page_url)
    dataset_page_dom  = lxml.html.fromstring(dataset_page_html)
    dataset_name      = dataset_page_dom.cssselect('.dato_titolo')[0].text_content().strip()

    dataset_metadata = {}
    for attribute_row in dataset_page_dom.cssselect('tr'):
        attr_name = attribute_row.cssselect('.tab_dato_titolo')
        if len(attr_name) == 1:
            attr_name = attr_name[0].text_content()
            try:
                result = attribute_actions[attr_name.lower()](attribute_row.cssselect('.tab_dato_testo' )[0])
                dataset_metadata.update(result)
            except Exception as e:
                raise Exception('Error while processing attribute ' + attr_name, repr(e) )
    dataset_metadata.update({'url'  : dataset_page_url})
    dataset_metadata.update({'name' : dataset_name})
    print 'Metadata', dataset_metadata
    scraperwiki.sqlite.save(table_name='meta', unique_keys=['url'], data=dataset_metadata)

def process_catalog_page(page_index):
    catalog_page_html = scraperwiki.scrape(CATALOG_PAGINATION + str(page_index)) 
    catalog_page_dom  = lxml.html.fromstring(catalog_page_html)
    for dataset_link in catalog_page_dom.cssselect('.cerca_td_nome a'):
        process_dataset_page( dataset_link.get('href') )
        

def process_catalog(catalog_size):
    print 'Catalog pages:', catalog_size
    for i in range(1,catalog_size):
        process_catalog_page(i)        

def process_search_page(search_page):
    search_page_html = scraperwiki.scrape(search_page)
    search_page_dom  = lxml.html.fromstring(search_page_html)
    try:
        last_page_link  = search_page_dom.cssselect('a[title="ultima pagina"]')[0]
        last_page_js = last_page_link.get('href')
        last_page_re = re.compile('cambiaPagina\((.+)\)')
        process_catalog( int(last_page_re.findall(last_page_js)[0]) )
    except Exception as e:
        raise Exception('Error while retrieving catalog size', e)

process_search_page(FIRST_CATALOG_PAGE)



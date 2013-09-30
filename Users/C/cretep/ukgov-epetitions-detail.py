import scraperwiki, lxml.html

uid  = int(265)

uri  = 'http://epetitions.direct.gov.uk/petitions/' + str(uid)
html = scraperwiki.scrape(uri)

root = lxml.html.fromstring(html)
data = {
    'URI'               : uri,
    'eGMS'              : root.cssselect('meta[name="eGMS.identifier.systemID"]')[0].get('content'),
    'title'             : root.cssselect('meta[name="DC.title"]')[0].get('content')[:-len(' - e-petitions')],
    'department'        : root.cssselect('.content .department')[0].text_content()[len('Responsible department: '):],
    'description'       : root.cssselect('.content .description')[0].text_content(),
    'signature_count'   : root.cssselect('.data dd.signature_count')[0].text_content(),
    'created_by'        : root.cssselect('.data dd.created_by')[0].text_content(),
    'closing_date'      : root.cssselect('.data dd.closing_date')[0].text_content()
}

scraperwiki.sqlite.save(unique_keys=['eGMS'], data=data)



#this is code modified, not page content updated
#'modified'          : root.cssselect('meta[name="DCTERMS.modified"]')[0].get('content'),

import scraperwiki, lxml.html

uid  = int(265)

uri  = 'http://epetitions.direct.gov.uk/petitions/' + str(uid)
html = scraperwiki.scrape(uri)

root = lxml.html.fromstring(html)
data = {
    'URI'               : uri,
    'eGMS'              : root.cssselect('meta[name="eGMS.identifier.systemID"]')[0].get('content'),
    'title'             : root.cssselect('meta[name="DC.title"]')[0].get('content')[:-len(' - e-petitions')],
    'department'        : root.cssselect('.content .department')[0].text_content()[len('Responsible department: '):],
    'description'       : root.cssselect('.content .description')[0].text_content(),
    'signature_count'   : root.cssselect('.data dd.signature_count')[0].text_content(),
    'created_by'        : root.cssselect('.data dd.created_by')[0].text_content(),
    'closing_date'      : root.cssselect('.data dd.closing_date')[0].text_content()
}

scraperwiki.sqlite.save(unique_keys=['eGMS'], data=data)



#this is code modified, not page content updated
#'modified'          : root.cssselect('meta[name="DCTERMS.modified"]')[0].get('content'),


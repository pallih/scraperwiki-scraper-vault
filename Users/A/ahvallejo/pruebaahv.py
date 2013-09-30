###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here:
# http://wwwsearch.sourceforge.net/mechanize/
# Base de datos de certificaciones en PMP
###############################################################################
import mechanize
import scraperwiki
import lxml.html as lh 


for letra in range(ord("z"),ord("z")+1):
    pmiurl = "https://certification.pmi.org/registry.aspx"
    br = mechanize.Browser()
    response = br.open(pmiurl)
    print "All forms:", [ form.name  for form in br.forms() ]
    br.select_form(name="_Form")
    print br.form
    print response.read()
    br["dph_RegistryContent$tbSearch"] = chr(letra)
    br["dph_RegistryContent$wcountry"] = ["COL"]
    response = br.submit()
    doc=lh.fromstring(response.read())
    i=1;
    j=1
    for tr in doc.cssselect('tr'):
        if i==1:
             i=i+1
             continue
        cell=tr.cssselect('td')
        index="{:s}{:d}".format(chr(letra),j)
        j=j+1
        data = {
           'Indice' : index,
           'Nombre' : cell[0].text_content().strip('\n\t\r '),
          'Ciudad' : cell[1].text_content().strip('\n\t\r '),
          'Pais' : cell[2].text_content().strip('\n\t\r '),    
         'Certificacion' : cell[3].text_content().strip('\n\t\r '),
         'Fecha' : cell[4].text_content().strip('\n\t\r '),
            }
        scraperwiki.sqlite.save(unique_keys=['Indice'], data=data)

###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here:
# http://wwwsearch.sourceforge.net/mechanize/
# Base de datos de certificaciones en PMP
###############################################################################
import mechanize
import scraperwiki
import lxml.html as lh 


for letra in range(ord("z"),ord("z")+1):
    pmiurl = "https://certification.pmi.org/registry.aspx"
    br = mechanize.Browser()
    response = br.open(pmiurl)
    print "All forms:", [ form.name  for form in br.forms() ]
    br.select_form(name="_Form")
    print br.form
    print response.read()
    br["dph_RegistryContent$tbSearch"] = chr(letra)
    br["dph_RegistryContent$wcountry"] = ["COL"]
    response = br.submit()
    doc=lh.fromstring(response.read())
    i=1;
    j=1
    for tr in doc.cssselect('tr'):
        if i==1:
             i=i+1
             continue
        cell=tr.cssselect('td')
        index="{:s}{:d}".format(chr(letra),j)
        j=j+1
        data = {
           'Indice' : index,
           'Nombre' : cell[0].text_content().strip('\n\t\r '),
          'Ciudad' : cell[1].text_content().strip('\n\t\r '),
          'Pais' : cell[2].text_content().strip('\n\t\r '),    
         'Certificacion' : cell[3].text_content().strip('\n\t\r '),
         'Fecha' : cell[4].text_content().strip('\n\t\r '),
            }
        scraperwiki.sqlite.save(unique_keys=['Indice'], data=data)


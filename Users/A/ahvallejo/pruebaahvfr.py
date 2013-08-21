###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here:
# http://wwwsearch.sourceforge.net/mechanize/
# Base de datos de certificaciones en PMP
###############################################################################
import mechanize
import scraperwiki
import lxml.html as lh 
#    pmiurl = "http://www.fincaraiz.com.co/viviendas/venta/colombia/ofertas.aspx?opi=2&crp=3&pgg=true"

#/viviendas/venta/colombia/ofertas.aspx?opi=2&crp=3&pgg=true
for letra in range(ord("a"),ord("a")+1):
    pmiurl = "http://www.fincaraiz.com.co/viviendas/venta/colombia/ofertas.aspx"
    br = mechanize.Browser()
    response = br.open(pmiurl)
    print "All forms:", [ form.name  for form in br.forms() ]
    br.select_form(name="frmMain")
    print br.form
    doc=lh.fromstring(response.read())
    print doc
#  br["dph_RegistryContent$tbSearch"] = chr(letra)
#  br["dph_RegistryContent$wcountry"] = ["COL"]
#  response = br.submit()
    i=1;
    j=1
    for tr in doc.cssselect('table'):
        if i==1:
             i=i+1
             continue
        cell=tr.cssselect('td')
        index="{:s}{:d}".format(chr(letra),j)
        j=j+1
        data = {
           'Indice' : index,
           'campo1' : cell[0].text_content().strip('\n\t\r '),
          'campo2' : cell[1].text_content().strip('\n\t\r '),
          'campo3' : cell[2].text_content().strip('\n\t\r '),    
         'campo3' : cell[3].text_content().strip('\n\t\r '),
         'campo4' : cell[4].text_content().strip('\n\t\r '),
            }
        scraperwiki.sqlite.save(unique_keys=['Indice'], data=data)


import scraperwiki
import lxml.html 
base_url = "http://www.consiglio.provincia.tn.it/"
url_consiglieri = "consiglio/composizione_attuale_consiglio.it.asp"
url = base_url + url_consiglieri
url_scheda_consigliere = "/consiglio/consiglieri_provinciali/consiglieri_rice.it.asp?pagetype=rice&ZID=2568018"
url_foto = '/images/foto_consiglieri/'
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html) 
list_consiglieri = root.cssselect("ul.sez-cons-menu-figli-testo")[0].cssselect("li")
for i in range(2,len(list_consiglieri)):
    consigliere = list_consiglieri[i].text_content()
    scheda = list_consiglieri[i].cssselect('a')[0].attrib['href']
    id_consigliere = scheda.split("&")[1].replace("id=","")
    cognome_consigliere = consigliere.split(" ")[0]
    nome_consigliere = consigliere.split(" ")[1]
    url_consigliere = base_url + url_scheda_consigliere + "&id=" + id_consigliere
    html_scheda_consigliere = lxml.html.fromstring(scraperwiki.scrape(url_consigliere))
    main_html = html_scheda_consigliere.cssselect('div#sez-cons-menu-content')[0]
    info = main_html.cssselect('div.sez-cons-recapiti-consigliere div.sez-cons-incarichi strong')[0]
    gruppo_appartenenza = info.text_content()
    foto = base_url + url_foto + id_consigliere + ".jpg"
    data = { 
        'id' : id_consigliere, 
        'nome' : nome_consigliere,
        'cognome' : cognome_consigliere,
        'cognome_nome' : consigliere,
        'url_consigliere' : url_consigliere,
        'gruppo_appartenenza' : gruppo_appartenenza,
        'foto' : gruppo_appartenenza
    }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
import scraperwiki
import lxml.html 
base_url = "http://www.consiglio.provincia.tn.it/"
url_consiglieri = "consiglio/composizione_attuale_consiglio.it.asp"
url = base_url + url_consiglieri
url_scheda_consigliere = "/consiglio/consiglieri_provinciali/consiglieri_rice.it.asp?pagetype=rice&ZID=2568018"
url_foto = '/images/foto_consiglieri/'
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html) 
list_consiglieri = root.cssselect("ul.sez-cons-menu-figli-testo")[0].cssselect("li")
for i in range(2,len(list_consiglieri)):
    consigliere = list_consiglieri[i].text_content()
    scheda = list_consiglieri[i].cssselect('a')[0].attrib['href']
    id_consigliere = scheda.split("&")[1].replace("id=","")
    cognome_consigliere = consigliere.split(" ")[0]
    nome_consigliere = consigliere.split(" ")[1]
    url_consigliere = base_url + url_scheda_consigliere + "&id=" + id_consigliere
    html_scheda_consigliere = lxml.html.fromstring(scraperwiki.scrape(url_consigliere))
    main_html = html_scheda_consigliere.cssselect('div#sez-cons-menu-content')[0]
    info = main_html.cssselect('div.sez-cons-recapiti-consigliere div.sez-cons-incarichi strong')[0]
    gruppo_appartenenza = info.text_content()
    foto = base_url + url_foto + id_consigliere + ".jpg"
    data = { 
        'id' : id_consigliere, 
        'nome' : nome_consigliere,
        'cognome' : cognome_consigliere,
        'cognome_nome' : consigliere,
        'url_consigliere' : url_consigliere,
        'gruppo_appartenenza' : gruppo_appartenenza,
        'foto' : gruppo_appartenenza
    }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

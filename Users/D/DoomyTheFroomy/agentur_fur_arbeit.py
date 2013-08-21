import scraperwiki
import simplejson
import urllib2
import lxml.html

not_given = "keine Angabe"
base_url = 'http://www.arbeitsagentur.de/nn_29892/SiteGlobals/Forms/Suche/Partner/partnersuche__large__form,templateId=processForm.html?plz='
url = ''
th = 10000
plz = ''

def getNr(string):
    try: 
        tel = ''
        for index in range(len(string)):
            if (string[index].isdigit() | string[index].isspace()):
                tel = tel + string[index]
        return tel.strip( ' ' );
    except:
        'Oh no Number?' + tel
## 99998
for n in reversed(range(1067,33609)):
    if (n < th) :
        url = base_url + str(0) + str(n) + '&x=-474&y=-230#'
        plz = str(0) + str(n)
    else :
        url = base_url + str(n) + '&x=-474&y=-230#'
        plz = str(n)
    try:
        result_html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(result_html)
        adrBoxArr = root.cssselect("div.addressbox")
        for adrBox in adrBoxArr: 
            data = {}
            name = adrBox.cssselect('span')[0].text
            data['id'] = plz + " " + name
            data['name'] = name
            data['postal-code'] = plz
            for el in adrBox: 
                if (el.tag == 'address'):
                    adrArr = el.cssselect('p.anschrift')
                    if (len(adrArr) > 0):
                        for adr in adrArr:
                            kind_of = adr.cssselect('strong')[0].text
                            data[kind_of+"_str"] = adr.cssselect('br')[0].tail
                            data[kind_of + "_ort"] = adr.cssselect('br')[1].tail
                    else:
                        adrCompl = lxml.html.tostring(el).replace('<address>','').replace('</address>','').replace('&#13;','')
                        adrArr = adrCompl.split('<br>')
                        data["str"] = adrArr[0]
                        data["ort"] = adrArr[1]
                            
                elif (el.text_content().find('@') > -1 ):
                        data['email'] = el.text_content()
                elif (el.tag == 'p') :
                    comp = lxml.html.tostring(el).replace('<p>','').replace('</p>','')
                    compArr = comp.split('<br>')
                    for comm in compArr:
                        nr = getNr(comm)
                        if (comm.find('Tel:') > -1 & comm.find('Arbeitnehmer') > -1 ):
                            data['tel_arbeitnehmer'] = nr
                        elif (comm.find('Tel:') > -1 & comm.find('Arbeitgeber') > -1 ):
                            data['tel_arbeitgeber'] = nr
                        elif (comm.find('Tel:') > -1):
                            data['tel_arbeitgeber'] = nr
                            data['tel_arbeitnehmer'] = nr
                        elif (comm.find('Fax:') > -1 & comm.find('Arbeitnehmer') > -1 ):
                            data['fax_arbeitnehmer'] = nr
                        elif (comm.find('Fax:') > -1 & comm.find('Arbeitgeber') > -1 ):
                            data['fax_arbeitgeber'] = nr
                        elif (comm.find('Fax:') > -1):
                            data['fax_arbeitgeber'] = nr
                            data['fax_arbeitnehmer'] = nr
                        ##else:
                          ##  print comm
                elif (el.tag == 'a') :
                     homepage = el.attrib['href']
                     data['url'] = 'http://www.arbeitsagentur.de/' + homepage.replace('../','')
                ##else: 
                    ##print el.text_content()
            scraperwiki.sqlite.save(["id"], data)   
    except:
        print 'Oh dear, failed to scrape %s' % url
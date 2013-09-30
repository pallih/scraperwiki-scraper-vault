import scraperwiki
from lxml import html

from urllib2 import urlopen, Request, URLError
import re
import string

URL = "http://www.afd.fr/base-projets/listerProjets.action?page=%s"

def cleanURL(data):
    expression=re.compile("(\S*);jsessionid=(\S*)\?(\S*)")
    d = expression.match(data)
    return d.group(1)+"?"+d.group(3)

def cleandata(data):
    if data:
        newdata = string.strip(data)
    else:
        newdata=''
    return newdata

def cleanamount(data):
    eurosign = u"\u20AC"
    commas = ','
    spaces = '\r\n\t\t\t\t\t'

    fixed = re.sub(eurosign, '', data)
    fixed = re.sub(commas, '', fixed)
    fixed = re.sub(spaces, '', fixed)    

    return fixed

def removeImage(data):
    print "Trying to remove image from", data
    fixed = re.sub('<img alt="" src="img/pdf.gif">', '', data)
    fixed = re.sub("\r", '', data)
    fixed = re.sub("\n", '', data)
    fixed = re.sub("\t", '', data)
    print "Final data after removing image is", data
    return fixed

# utf8 : database_field_name
translations = {
    u'Libell\xe9 du projet': 'name',
    u'Num\xe9ro de projet': 'id',
    u'Pays de r\xe9alisation': 'country',
    u'B\xe9n\xe9ficiaire': 'beneficiary',
    "Secteur d'intervention": 'aim',
    'Agence de gestion': 'agency',
    'Classement environnemental': 'environmental_impact',
    'Classement social': 'social_impact',
    u"Commentaire sur l'\xe9x\xe9cution du projet": 'comment',
    'Execution': 'in progress',
    'Etat du projet': 'status',
    'Montant global du projet': 'funding_total_euros',
    "Financement de l'AFD": 'funding_from_afd_euros',
    'Forme de concours': 'funding_type',
    'Cofinancement': 'is_co_financed',
    u"Date d'identification valid\xe9e": 'date_validated',
    "Date d'octroi du financement": 'date_funded',
    'Chef de projet': 'project_manager',
    'Responsable agence': 'responsible_agency',
    'Structure responsable': 'responsible_structure',
    
    'non': 'no',
    'oui': 'yes',
    }

def translate(french_str, warn_if_no_translation=False):
    if not french_str:
        return ''
    if french_str in translations:
        return translations[french_str].decode('utf8')
    else:
        if warn_if_no_translation:
            print 'Could not translate: %s = %r' % (french_str, french_str)
        return french_str

def scrape_project_page(data, project_url):
    req = Request(project_url)
    data['project_details'] = project_url
    doc = html.parse(urlopen(req))
    for tr in doc.findall('//table//tr'):
        field = []
        for cell_type in ('th', 'td'):
            cells = tr.findall(cell_type)
            if not cells:
                # ignore row <th>Commentaire...</th> with no <td>
                # TODO get the pdf links at this point
                continue
            warn_if_no_translation = cell_type == 'th'
            if cells and cells[0].get('colspan') == '2':
                # ignore section titles (they span both columns)
                break
            cells = [translate(cleanamount(cleandata(cell.text)),
                               warn_if_no_translation) \
                     for cell in cells]
            field.append(' | '.join(cells))
        if len(field) == 2:
            if not field[0]:
                # don't save a blank key
                assert not field[1], 'Throwing away data without key: %r' % field[1]
                continue
            data[field[0]] = field[1]
            #print 'SAVE %s : %s' % tuple(field)
    document_field = doc.find('//tr//td//div/a')

    if document_field is not None:
        data["document_url"] = cleanURL("http://www.afd.fr"+document_field.get("href"))
        data["document_name"] = document_field.text_content()
        print "document name is", cleandata(document_field.text_content())
        print "document url is", cleanURL("http://www.afd.fr"+document_field.get("href"))

    scraperwiki.sqlite.save(unique_keys=["country", "description"],
                            data=data)

# loop over the pages of the "liste des projets"
page_number = 0
while True:
    page_number += 1
    req = Request(URL % (page_number))

    try:
        response = urlopen(req)
    except URLError, e:
#        import pdb; pdb.set_trace()
        if response.status == 404:
            break
    
    doc = html.parse(response)
    if not(doc.findall('//tbody//tr')):
        break
    # loop over each project summary
    for tr in doc.findall('//tbody//tr'):
        cells = list(tr.findall('td'))
        if not len(cells):
            continue
        amount = re.sub(',', '', cells[2].text)
        project_url = 'http://www.afd.fr' + cells[1].find('a').get('href')
        data = {
            'country' : cleandata(cells[0].text),
            'description' : cleandata(cells[1].find('a').text),
            'project_url' : cleanURL(project_url),
            'funding_total_euros' : cleanamount(cleandata(amount)),
            'status' : cleandata(cells[3].text),
            'date_updated' : cells[4].text
        }


        # drill down into the project page
        try:
            scrape_project_page(data, project_url)
        except:
            # if that fails, save what we have!
            scraperwiki.sqlite.save(unique_keys=["country", "description"],
            data=data)

import scraperwiki
from lxml import html

from urllib2 import urlopen, Request, URLError
import re
import string

URL = "http://www.afd.fr/base-projets/listerProjets.action?page=%s"

def cleanURL(data):
    expression=re.compile("(\S*);jsessionid=(\S*)\?(\S*)")
    d = expression.match(data)
    return d.group(1)+"?"+d.group(3)

def cleandata(data):
    if data:
        newdata = string.strip(data)
    else:
        newdata=''
    return newdata

def cleanamount(data):
    eurosign = u"\u20AC"
    commas = ','
    spaces = '\r\n\t\t\t\t\t'

    fixed = re.sub(eurosign, '', data)
    fixed = re.sub(commas, '', fixed)
    fixed = re.sub(spaces, '', fixed)    

    return fixed

def removeImage(data):
    print "Trying to remove image from", data
    fixed = re.sub('<img alt="" src="img/pdf.gif">', '', data)
    fixed = re.sub("\r", '', data)
    fixed = re.sub("\n", '', data)
    fixed = re.sub("\t", '', data)
    print "Final data after removing image is", data
    return fixed

# utf8 : database_field_name
translations = {
    u'Libell\xe9 du projet': 'name',
    u'Num\xe9ro de projet': 'id',
    u'Pays de r\xe9alisation': 'country',
    u'B\xe9n\xe9ficiaire': 'beneficiary',
    "Secteur d'intervention": 'aim',
    'Agence de gestion': 'agency',
    'Classement environnemental': 'environmental_impact',
    'Classement social': 'social_impact',
    u"Commentaire sur l'\xe9x\xe9cution du projet": 'comment',
    'Execution': 'in progress',
    'Etat du projet': 'status',
    'Montant global du projet': 'funding_total_euros',
    "Financement de l'AFD": 'funding_from_afd_euros',
    'Forme de concours': 'funding_type',
    'Cofinancement': 'is_co_financed',
    u"Date d'identification valid\xe9e": 'date_validated',
    "Date d'octroi du financement": 'date_funded',
    'Chef de projet': 'project_manager',
    'Responsable agence': 'responsible_agency',
    'Structure responsable': 'responsible_structure',
    
    'non': 'no',
    'oui': 'yes',
    }

def translate(french_str, warn_if_no_translation=False):
    if not french_str:
        return ''
    if french_str in translations:
        return translations[french_str].decode('utf8')
    else:
        if warn_if_no_translation:
            print 'Could not translate: %s = %r' % (french_str, french_str)
        return french_str

def scrape_project_page(data, project_url):
    req = Request(project_url)
    data['project_details'] = project_url
    doc = html.parse(urlopen(req))
    for tr in doc.findall('//table//tr'):
        field = []
        for cell_type in ('th', 'td'):
            cells = tr.findall(cell_type)
            if not cells:
                # ignore row <th>Commentaire...</th> with no <td>
                # TODO get the pdf links at this point
                continue
            warn_if_no_translation = cell_type == 'th'
            if cells and cells[0].get('colspan') == '2':
                # ignore section titles (they span both columns)
                break
            cells = [translate(cleanamount(cleandata(cell.text)),
                               warn_if_no_translation) \
                     for cell in cells]
            field.append(' | '.join(cells))
        if len(field) == 2:
            if not field[0]:
                # don't save a blank key
                assert not field[1], 'Throwing away data without key: %r' % field[1]
                continue
            data[field[0]] = field[1]
            #print 'SAVE %s : %s' % tuple(field)
    document_field = doc.find('//tr//td//div/a')

    if document_field is not None:
        data["document_url"] = cleanURL("http://www.afd.fr"+document_field.get("href"))
        data["document_name"] = document_field.text_content()
        print "document name is", cleandata(document_field.text_content())
        print "document url is", cleanURL("http://www.afd.fr"+document_field.get("href"))

    scraperwiki.sqlite.save(unique_keys=["id"],
                            data=data)

# loop over the pages of the "liste des projets"
page_number = 0
while True:
    page_number += 1
    req = Request(URL % (page_number))

    try:
        response = urlopen(req)
    except URLError, e:
#        import pdb; pdb.set_trace()
        if response.status == 404:
            break
    
    doc = html.parse(response)
    if not(doc.findall('//tbody//tr')):
        break
    # loop over each project summary
    for tr in doc.findall('//tbody//tr'):
        cells = list(tr.findall('td'))
        if not len(cells):
            continue
        amount = re.sub(',', '', cells[2].text)
        project_url = 'http://www.afd.fr' + cells[1].find('a').get('href')
        data = {
            'country' : cleandata(cells[0].text),
            'description' : cleandata(cells[1].find('a').text),
            'project_url' : cleanURL(project_url),
            'funding_total_euros' : cleanamount(cleandata(amount)),
            'status' : cleandata(cells[3].text),
            'date_updated' : cells[4].text
        }


        # drill down into the project page
        try:
            scrape_project_page(data, project_url)
        except:
            # if that fails, save what we have!
            scraperwiki.sqlite.save(unique_keys=["id"],
            data=data)


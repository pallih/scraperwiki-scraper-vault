import scraperwiki
import urllib
import re
import BeautifulSoup

word_list = ["aborto", "aleitamento", "amamentação", "amamentar", "bebê", "berçário", "brincadeira", "brincar", "brinquedo", "cognitivo", "comunitário", "creche", "criança", "cuidador", "doulas", "educador", "família", "filha", "filho", "gestante", "gravidez ", "infância", "infantil", "infantis", "infanto", "lactante", "leite", "leitura", "lúdico", "mãe", "maternal", "maternidade", "materno", "materno-infantil", "morbimortalidade", "mortalidade", "neonatal", "obstetra", "olhinho", "orelhinha", "pai", "parto", "parturiente", "pedagógica", "pedagógico", "pediatra", "pediatria", "pedofilia", "pedófilo", "pezinho", "poliomielite", "pré-natal", "primíparas", "puericultura", "puérpera", "puerpério", "ultrasson", "vacina", "vacinação", "visita domiciliar", "visitas domiciliares", "adoção", "abuso", "aluno", "bolsa", "colégio", "educação", "escola", "ensino", "professor"]

def getUrls(start_year, last_count):  
    for ano in range(start_year,2012):
        url = 'http://sidornet.planejamento.gov.br/docs/cadacao/cadacao' + str(ano) + '/downloads.htm'
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup.BeautifulSoup(html)
        links = soup.findAll('div', 'volume_a')
        count = 0
        for link in links:
            if 0 == 1:
                count += 1
            else:                             
                data = {}
                data['id'] = str(ano) + '-' + re.search('([0-9]*) -',link.a.text).group(1)
                data['name'] = link.a.renderContents()
                data['year'] = ano
                data['url'] = 'http://sidornet.planejamento.gov.br/docs/cadacao/' + link.a['href']
                data['words'] = checkPdf(['http://sidornet.planejamento.gov.br/docs/cadacao/' + link.a['href']])
                print data
                scraperwiki.datastore.save(['id'], data)
                last_count += 1
                scraperwiki.sqlite.save_var('last_count', count)
        scraperwiki.sqlite.save_var('last_year',ano)
        scraperwiki.sqlite.save_var('last_count', 0)
        last_count = 0         

def getPdf(pdfurl):
    pdfdata = urllib.urlopen(pdfurl).read()
    pdfxml = scraperwiki.pdftoxml(pdfdata)
    #soup = BeautifulSoup.BeautifulStoneSoup(pdfxml)
    return pdfxml.lower()


def checkPdf(pdfurls):
    words = []
    for url in pdfurls:
        pdf = getPdf(url)
        for word in word_list:
            if re.search(standword(word), pdf):
                words += [word.decode('utf-8')]
    return words

def standword(word): 
    """ return a regular expression that can find 'peter' 
    only if it's written alone (next to space, start of  
    string, end of string, comma, etc) but not if inside  
    another word like peterbe """ 
    return re.compile(r'\b%s\b' % word, re.I)

#reset
#scraperwiki.sqlite.save_var('last_year', 2008)
#scraperwiki.sqlite.save_var('last_count', 0)

last_count = scraperwiki.sqlite.get_var('last_count', 0)
last_year = scraperwiki.sqlite.get_var('last_year', 2008)
getUrls(last_year + 1, last_count)import scraperwiki
import urllib
import re
import BeautifulSoup

word_list = ["aborto", "aleitamento", "amamentação", "amamentar", "bebê", "berçário", "brincadeira", "brincar", "brinquedo", "cognitivo", "comunitário", "creche", "criança", "cuidador", "doulas", "educador", "família", "filha", "filho", "gestante", "gravidez ", "infância", "infantil", "infantis", "infanto", "lactante", "leite", "leitura", "lúdico", "mãe", "maternal", "maternidade", "materno", "materno-infantil", "morbimortalidade", "mortalidade", "neonatal", "obstetra", "olhinho", "orelhinha", "pai", "parto", "parturiente", "pedagógica", "pedagógico", "pediatra", "pediatria", "pedofilia", "pedófilo", "pezinho", "poliomielite", "pré-natal", "primíparas", "puericultura", "puérpera", "puerpério", "ultrasson", "vacina", "vacinação", "visita domiciliar", "visitas domiciliares", "adoção", "abuso", "aluno", "bolsa", "colégio", "educação", "escola", "ensino", "professor"]

def getUrls(start_year, last_count):  
    for ano in range(start_year,2012):
        url = 'http://sidornet.planejamento.gov.br/docs/cadacao/cadacao' + str(ano) + '/downloads.htm'
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup.BeautifulSoup(html)
        links = soup.findAll('div', 'volume_a')
        count = 0
        for link in links:
            if 0 == 1:
                count += 1
            else:                             
                data = {}
                data['id'] = str(ano) + '-' + re.search('([0-9]*) -',link.a.text).group(1)
                data['name'] = link.a.renderContents()
                data['year'] = ano
                data['url'] = 'http://sidornet.planejamento.gov.br/docs/cadacao/' + link.a['href']
                data['words'] = checkPdf(['http://sidornet.planejamento.gov.br/docs/cadacao/' + link.a['href']])
                print data
                scraperwiki.datastore.save(['id'], data)
                last_count += 1
                scraperwiki.sqlite.save_var('last_count', count)
        scraperwiki.sqlite.save_var('last_year',ano)
        scraperwiki.sqlite.save_var('last_count', 0)
        last_count = 0         

def getPdf(pdfurl):
    pdfdata = urllib.urlopen(pdfurl).read()
    pdfxml = scraperwiki.pdftoxml(pdfdata)
    #soup = BeautifulSoup.BeautifulStoneSoup(pdfxml)
    return pdfxml.lower()


def checkPdf(pdfurls):
    words = []
    for url in pdfurls:
        pdf = getPdf(url)
        for word in word_list:
            if re.search(standword(word), pdf):
                words += [word.decode('utf-8')]
    return words

def standword(word): 
    """ return a regular expression that can find 'peter' 
    only if it's written alone (next to space, start of  
    string, end of string, comma, etc) but not if inside  
    another word like peterbe """ 
    return re.compile(r'\b%s\b' % word, re.I)

#reset
#scraperwiki.sqlite.save_var('last_year', 2008)
#scraperwiki.sqlite.save_var('last_count', 0)

last_count = scraperwiki.sqlite.get_var('last_count', 0)
last_year = scraperwiki.sqlite.get_var('last_year', 2008)
getUrls(last_year + 1, last_count)
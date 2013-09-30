import scraperwiki
import urllib
import BeautifulSoup
import re

errors = ['https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG025.DT012011.pdf']
pdfurls = ['https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG010.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG012.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG013.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG016.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG017.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG018.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG020.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG023.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG025.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG026.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG028.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG029.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG035.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG037.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG038.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG039.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG040.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG041.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG043.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG044.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG046.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG047.DT012011.pdf']

pdfurls_big = ['https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG009.DT012011.pdf',
'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG008.DT012011.pdf']

#retorna item de array se a url existe



def scrapePdf(pdfdata, id=0):
    pdfxml = scraperwiki.pdftoxml(pdfdata)
    soup = BeautifulSoup.BeautifulStoneSoup(pdfxml)
    soup = soup.findAll('text')
    left = {}
    left['nome'] = soup[0]['left']
    left['cargo'] = soup[1]['left']
    left['vinculo'] = soup[2]['left']
    left['cargo_comissao'] = soup[3]['left']
    left['jornada'] = soup[4]['left']
    left['sit_funcional'] = soup[5]['left']
    left['secretaria'] = soup[6]['left']
    left['un_orcamentaria'] = soup[7]['left']
    left['un_gestora'] = soup[8]['left']
    left['un_administrativa'] = soup[9]['left']
    left['municipio'] = soup[10]['left']
    for r in range(0,11):
        print soup[r]
    for x in soup:
        if x['left'] == left['nome']:
            data = {}
            data['id'] = id
            data['nome'] = x.text
            data['cargo'] = ''
            data['vinculo'] = ''
            data['cargo_comissao'] = ''
            data['jornada'] = ''
            data['sit_funcional'] = ''
            data['secretaria'] = ''
            data['un_orcamentaria'] = ''
            data['un_gestora'] = ''
            data['un_administrativa'] = ''
        elif x['left'] == left['cargo'] and x.text: data['cargo'] = x.text
        elif x['left'] == left['vinculo'] and x.text: data['vinculo'] = x.text
        elif x['left'] == left['cargo_comissao'] and x.text: data['cargo_comissao'] = x.text
        elif x['left'] == left['jornada'] and x.text: data['jornada'] = x.text
        elif x['left'] == left['sit_funcional'] and x.text: data['sit_funcional'] = x.text
        #algumas colunas truncam no pdf de teste e ficam nesse mesmo <text>
        elif x['left'] == left['secretaria'] and x.text:
            s = x.text.split('             ')
            len_s = len(s)
            if len_s == 3:
                data['secretaria'] = s[0]
                data['un_orcamentaria'] = s[1]
                data['un_gestora'] = s[2]
            elif len_s == 2:
                data['secretaria'] = s[0]
                data['un_orcamentaria'] = s[1]
            else: data['secretaria'] = x.text        
        elif x['left'] == left['un_orcamentaria'] and x.text: data['un_orcamentaria'] = x.text
        elif x['left'] == left['un_gestora'] and x.text: data['un_gestora'] = x.text
        elif x['left'] == left['un_administrativa'] and x.text: data['un_administrativa'] = x.text
        elif x['left'] == left['municipio'] and x.text:
            data['municipio'] = x.text
            scraperwiki.datastore.save(["id"], data)
            id = id + 1
        else:
            if x.text: print x['left'] + ' - Erro: ' + x.text
    scraperwiki.sqlite.save_var('last_id', int(id))

def rockndroll(pdfurls):
    for pdfurl in pdfurls:
#        try:
        lastid = scraperwiki.sqlite.get_var('last_id', 0)
        print 'Baixando ' + pdfurl
        pdfdata = urllib.urlopen(pdfurl).read()
        scrapePdf(pdfdata, lastid)
        print 'Ultimo id ' + str(lastid)
    #    except:
           #failed_urls = scraperwiki.sqlite.get_var('failed_urls', [])
            #failed_urls = failed_urls + [str(pdfurl)]
            #scraperwiki.sqlite.save_var('failed_urls', failed_urls)
#            pass

rockndroll(errors)import scraperwiki
import urllib
import BeautifulSoup
import re

errors = ['https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG025.DT012011.pdf']
pdfurls = ['https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG010.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG012.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG013.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG016.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG017.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG018.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG020.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG023.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG025.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG026.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG028.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG029.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG035.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG037.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG038.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG039.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG040.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG041.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG043.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG044.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG046.DT012011.pdf', 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG047.DT012011.pdf']

pdfurls_big = ['https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG009.DT012011.pdf',
'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG008.DT012011.pdf']

#retorna item de array se a url existe



def scrapePdf(pdfdata, id=0):
    pdfxml = scraperwiki.pdftoxml(pdfdata)
    soup = BeautifulSoup.BeautifulStoneSoup(pdfxml)
    soup = soup.findAll('text')
    left = {}
    left['nome'] = soup[0]['left']
    left['cargo'] = soup[1]['left']
    left['vinculo'] = soup[2]['left']
    left['cargo_comissao'] = soup[3]['left']
    left['jornada'] = soup[4]['left']
    left['sit_funcional'] = soup[5]['left']
    left['secretaria'] = soup[6]['left']
    left['un_orcamentaria'] = soup[7]['left']
    left['un_gestora'] = soup[8]['left']
    left['un_administrativa'] = soup[9]['left']
    left['municipio'] = soup[10]['left']
    for r in range(0,11):
        print soup[r]
    for x in soup:
        if x['left'] == left['nome']:
            data = {}
            data['id'] = id
            data['nome'] = x.text
            data['cargo'] = ''
            data['vinculo'] = ''
            data['cargo_comissao'] = ''
            data['jornada'] = ''
            data['sit_funcional'] = ''
            data['secretaria'] = ''
            data['un_orcamentaria'] = ''
            data['un_gestora'] = ''
            data['un_administrativa'] = ''
        elif x['left'] == left['cargo'] and x.text: data['cargo'] = x.text
        elif x['left'] == left['vinculo'] and x.text: data['vinculo'] = x.text
        elif x['left'] == left['cargo_comissao'] and x.text: data['cargo_comissao'] = x.text
        elif x['left'] == left['jornada'] and x.text: data['jornada'] = x.text
        elif x['left'] == left['sit_funcional'] and x.text: data['sit_funcional'] = x.text
        #algumas colunas truncam no pdf de teste e ficam nesse mesmo <text>
        elif x['left'] == left['secretaria'] and x.text:
            s = x.text.split('             ')
            len_s = len(s)
            if len_s == 3:
                data['secretaria'] = s[0]
                data['un_orcamentaria'] = s[1]
                data['un_gestora'] = s[2]
            elif len_s == 2:
                data['secretaria'] = s[0]
                data['un_orcamentaria'] = s[1]
            else: data['secretaria'] = x.text        
        elif x['left'] == left['un_orcamentaria'] and x.text: data['un_orcamentaria'] = x.text
        elif x['left'] == left['un_gestora'] and x.text: data['un_gestora'] = x.text
        elif x['left'] == left['un_administrativa'] and x.text: data['un_administrativa'] = x.text
        elif x['left'] == left['municipio'] and x.text:
            data['municipio'] = x.text
            scraperwiki.datastore.save(["id"], data)
            id = id + 1
        else:
            if x.text: print x['left'] + ' - Erro: ' + x.text
    scraperwiki.sqlite.save_var('last_id', int(id))

def rockndroll(pdfurls):
    for pdfurl in pdfurls:
#        try:
        lastid = scraperwiki.sqlite.get_var('last_id', 0)
        print 'Baixando ' + pdfurl
        pdfdata = urllib.urlopen(pdfurl).read()
        scrapePdf(pdfdata, lastid)
        print 'Ultimo id ' + str(lastid)
    #    except:
           #failed_urls = scraperwiki.sqlite.get_var('failed_urls', [])
            #failed_urls = failed_urls + [str(pdfurl)]
            #scraperwiki.sqlite.save_var('failed_urls', failed_urls)
#            pass

rockndroll(errors)
import scraperwiki
import urllib2
import lxml.etree


pdfurls = [
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG010.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG012.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG013.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG016.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG017.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG018.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG020.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG023.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG025.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG026.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG028.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG029.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG035.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG037.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG038.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG039.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG040.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG041.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG043.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG044.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG046.DT012011.pdf', 
    'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/PAGD471.ORG047.DT012011.pdf']


colunas = [
    'nome', 'cargo', 'tipo_vinculo', 'comissao_designado', 'jornada', 'situacao_funcional', 'secretaria', 'unidade_orcamentaria', 'unidade_gestora', 'unidade_administrativa', 'municipio'
]

def carregaPagina(url):
    print url
    pdfdata = urllib2.urlopen(url).read()
    #print "The pdf file has %d bytes" % len(pdfdata)
    
    xmldata = scraperwiki.pdftoxml(pdfdata)
    #print "After converting to xml it has %d bytes" % len(xmldata)
    print "The first 5000 characters are: ", xmldata[:5000]
    
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)
    print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

    arquivo = url.replace("https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/Arquivos/", "")
    cabecalho = True

    for page in pages: #[:1]
        data = {}
        conta = 0
        coluna = 0
        for el in list(page)[:110]: #[:100]
            if el.tag == "text":
                data[colunas[coluna]] = el.text.strip()
                coluna = coluna + 1
                if coluna >= len(colunas):
                    if not cabecalho:
                        data['arquivo'] = arquivo
                        #print el.attrib['left'], el.text
                        if conta < 10: print data
                        scraperwiki.datastore.save(["arquivo", "nome", "cargo", "municipio"], data)
                        conta = conta + 1
                        data = {}

                    cabecalho = False
                    coluna = 0

        print "Pagina %s: %s registro(s)" % (page.attrib.get("number"), conta)



# starter
for url in pdfurls:
    carregaPagina(url)



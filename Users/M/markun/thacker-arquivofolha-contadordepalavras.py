import urllib
import BeautifulSoup
import re
import scraperwiki

ano_inicio = 1921
ano_fim = 2011
site = 'fsp'

def pegaPalavra(palavra, site, ano_inicio, ano_fim):
    for ano in range(ano_inicio,ano_fim+1):
    
        url = "http://acervo.folha.com.br/resultados/" + str(ano) + "?periodo=acervo&q=" + palavra + "&x=0&y=14&site=" + site
        js = urllib.urlopen(url).read()
        
        js = js.lstrip("""$("#div3 ul").html('""")
        js = js.rstrip("""')
        $("#loading").hide();""")
        
        doc = BeautifulSoup.BeautifulSoup(js)
        hits = doc.findAll('div')
        if hits:
            for m in hits:
                g = re.search('^(.*) <span>([0-9]*) p', m.renderContents())
                data = {}
                data['palavra'] = palavra
                data['ano'] = ano
                data['mes'] = g.group(1)
                data['paginas'] = g.group(2)
                data['id'] = data['palavra'] + str(data['ano']) + data['mes']
                scraperwiki.sqlite.save(['id'], data, palavra)

palavras = ['hackers']
for palavra in palavras:
    pegaPalavra(palavra, site, ano_inicio, ano_fim)
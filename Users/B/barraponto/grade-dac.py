import scraperwiki
from lxml.html import parse

pagina = parse('http://www.dac.unicamp.br/sistemas/horarios/grad/G1S0/IA.htm').getroot()

for linha in pagina.cssselect('a'):
    disciplina = {
        'nome': linha.text_content(),
        'link': 'http://www.dac.unicamp.br/sistemas/horarios/grad/G1S0/' + linha.get('href')
    }

    print 'pegando a pagina da disciplina ' + disciplina['nome']

    paginadadisciplina = parse(disciplina['link']).getroot()
    disciplina['creditos'] = paginadadisciplina.cssselect('p')[0].text_content().strip()

    scraperwiki.sqlite.save(['link'], disciplina)


import scraperwiki
from lxml import etree
from lxml.cssselect import CSSSelector

# Start our list
votings = []
# Get the XML data
root = etree.parse('http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterVotacaoProposicao?tipo=PL&numero=1876&ano=1999')

for voting in CSSSelector('Votacao')(root):
    thisvoting = {
        'description': voting.get('ObjVotacao'),
        'date': voting.get('Data'),
        'supporting': [],
        'opposing': []
    }
    for deputado in CSSSelector('Deputado')(voting):
        if deputado.get('Voto') == 'Sim':
            thisvoting['supporting'].append({
                'name': deputado.get('Nome'),
                'party': deputado.get('Partido'),
                'state': deputado.get('UF')
            })
        else:
            thisvoting['opposing'].append({
                'name': deputado.get('Nome'),
                'party': deputado.get('Partido'),
                'state': deputado.get('UF')
            })

    votings.append(thisvoting)
import scraperwiki
from lxml import etree
from lxml.cssselect import CSSSelector

# Start our list
votings = []
# Get the XML data
root = etree.parse('http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterVotacaoProposicao?tipo=PL&numero=1876&ano=1999')

for voting in CSSSelector('Votacao')(root):
    thisvoting = {
        'description': voting.get('ObjVotacao'),
        'date': voting.get('Data'),
        'supporting': [],
        'opposing': []
    }
    for deputado in CSSSelector('Deputado')(voting):
        if deputado.get('Voto') == 'Sim':
            thisvoting['supporting'].append({
                'name': deputado.get('Nome'),
                'party': deputado.get('Partido'),
                'state': deputado.get('UF')
            })
        else:
            thisvoting['opposing'].append({
                'name': deputado.get('Nome'),
                'party': deputado.get('Partido'),
                'state': deputado.get('UF')
            })

    votings.append(thisvoting)

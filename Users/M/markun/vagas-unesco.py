from datetime import datetime
import scraperwiki
from lxml.html import parse

url = "http://www1.brasilia.unesco.org/vagasubo/index.php?option=com_phocadownload&view=category&id=1&Itemid=5"
html = parse(url).getroot()

vagas = html.cssselect("td[colspan=5]")
for vaga in vagas:
    try:
        data = {}
        data['projeto'] = vaga.cssselect("span[lang='EN'] strong")[0].text
        data['vaga'] = vaga.cssselect("p span strong")[1].tail
        data['responsavel'] = vaga.cssselect("p span strong")[2].tail
        data['data_limite'] = vaga.cssselect("p span strong")[3].tail
        data['date_scraped'] = datetime.now()

        download_url = vaga.getparent().getnext().cssselect("a")
        data['url'] = "http://www1.brasilia.unesco.org" + download_url[0].get("href")
    
        scraperwiki.sqlite.save(["projeto"], data)
    except:
        pass
    
#<td colspan="5"><p><span lang="EN"><span lang="EN"><span lang="EN"><strong>PROJETO&nbsp;914BRZ1122&nbsp;&nbsp;- Edital 01/2012</strong></span></span> </span></p>
#<p><span><strong>Vagas Disponíveis:</strong> nível superior em saúde pública e/ou avaliação de processos ou áreas correlatas</span></p>
#<p><span><strong>Responsável Técnico pela Seleção: </strong>UNESCO<br></span></p>
#<p><span><strong>Data limite para entrega do currículo:</strong> Fevereiro 05, 2011</span></p></td>


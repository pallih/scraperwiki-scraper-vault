from lxml.html import parse
import scraperwiki

page = parse('http://www.vnews.com.br/editoria.php?id=1').getroot()

for event in page.cssselect('.atualizado_editoria'):

    data = {}

    data['qdo'] = event.cssselect('div')[0].text_content()   
       

    scraperwiki.sqlite.save(['qdo'], data)



page = parse('http://www.vnews.com.br/editoria.php?id=1').getroot()

for event in page.cssselect('.EditoriaTitulo'):

    data = {}

    data['title'] = event.cssselect('a')[0].text_content()          

    scraperwiki.sqlite.save(['title'], data)


page = parse('http://www.vnews.com.br/editoria.php?id=1').getroot()

for event in page.cssselect('.EditoriaNoticia'):

    data = {}

    data['noti'] = event.cssselect('a')[0].text_content()          

    scraperwiki.sqlite.save(['noti'], data)from lxml.html import parse
import scraperwiki

page = parse('http://www.vnews.com.br/editoria.php?id=1').getroot()

for event in page.cssselect('.atualizado_editoria'):

    data = {}

    data['qdo'] = event.cssselect('div')[0].text_content()   
       

    scraperwiki.sqlite.save(['qdo'], data)



page = parse('http://www.vnews.com.br/editoria.php?id=1').getroot()

for event in page.cssselect('.EditoriaTitulo'):

    data = {}

    data['title'] = event.cssselect('a')[0].text_content()          

    scraperwiki.sqlite.save(['title'], data)


page = parse('http://www.vnews.com.br/editoria.php?id=1').getroot()

for event in page.cssselect('.EditoriaNoticia'):

    data = {}

    data['noti'] = event.cssselect('a')[0].text_content()          

    scraperwiki.sqlite.save(['noti'], data)
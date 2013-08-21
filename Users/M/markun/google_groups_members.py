import mechanize 
import BeautifulSoup
import scraperwiki

def scrapear(url):
    response2 = br.open(url)
    soup = BeautifulSoup.BeautifulSoup(response2)
    soup = soup.findAll("div", "maincontbox")

    lista = soup[0].findAll("tr")

    for x, i in enumerate(lista):
        if i.td.get('class') == 'padt5':
            data = {}
            data['user'] = i.td.nextSibling.a.text
            data['date'] = i.td.nextSibling.span.text
            y = x + 1
            data['name'] = ''
            data['local'] = ''
            data['bio'] = ''
            while y < len(lista)-1 and lista[y].td.get('class') != 'padt5':
                if lista[y].td.text == 'Name:':
                    data['name'] = lista[y].td.nextSibling.text
                if lista[y].td.text == 'Location:':
                    data['local'] = lista[y].td.nextSibling.text
                if lista[y].td.text == 'Bio:':
                    data['bio'] = lista[y].td.nextSibling.text
                y = y + 1
            scraperwiki.sqlite.save(['user'], data)
            print data
    links = soup[0].findAll('a', 'uitl')
    if links[len(links)-1].text == "Next &raquo;":
        next_link = "http://groups.google.com" + links[len(links)-1].get('href')
        print 'scrapeando outra pagina'
        scrapear(next_link)
    else:
        print 'trabajo completo!'

url = "http://www.gmail.com"

br = mechanize.Browser()
br.set_handle_robots(False)

br.open(url)

loginForm = br.forms().next()
loginForm["Email"] = 'testedummy007@gmail.com'
loginForm["Passwd"] = 'testedummy'
response = br.open(loginForm.click())
scrapear("http://groups.google.com/group/thackday/members")
import scraperwiki
import requests
import lxml.html

def main():
    html = requests.get('http://hdrstats.undp.org/en/indicators/72206.html').text
    dom = lxml.html.fromstring(html)
    data = []
    for row in dom.cssselect('tbody tr'):
        tds = row.cssselect('td')
        if tds[0].text != '..':
            data.append({
                'country': tds[1].text_content(),
                'lei': tds[-1].text.strip()
            })
    scraperwiki.sqlite.save(['country'], data)

main()


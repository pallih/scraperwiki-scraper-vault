import scraperwiki
import lxml.html

def scrape_directory_text():
    html = scraperwiki.scrape("http://ritter.tea.state.tx.us/perfreport/account/2011/statelist.html")
    root = lxml.html.fromstring(html)
    text = root.cssselect("table table pre a")[0].text
    return text

def parse_directory_text(text):
    print text

text = scrape_directory_text()
parse_directory_text(text)
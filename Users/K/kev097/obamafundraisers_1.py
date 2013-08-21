import scraperwiki
import scraperwiki.sqlite
import lxml.html

code = scraperwiki.scrape("https://donate.barackobama.com/page/contribute/o2012-march30burlingtonreception?custom1=303852")

root = lxml.html.fromstring(code)

container = root.find_class('bsd-contribForm-aboveContent')

data = {'fundraiser': container[0].text_content()}

scraperwiki.sqlite.save(unique_keys=['fundraiser'], data=data)

print container[0].text_content()

# container.make_links_absolute('http://donate.barackobama.com/')
# links = container.iterlinks()


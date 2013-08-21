from scraperwiki import swimport
bucketwheel = swimport('bucketwheel_get')

class GetLinks(bucketwheel.Get):
    def parse(self, text):
        html = fromstring(text)
        links = html.xpath('//a/@href')
        for link in links:
            if link[0] == '/':
                link = 'http://thomaslevine.com' + link
        return map(GetLinks, links)

if __name__ == "scraper":
    #execute('drop table if exists stack')
    #commit()
    bucketwheel.seed([GetLinks('http://thomaslevine.com')])
import scraperwiki
import lxml.html


plans = {
    2012: 'http://www.verwaltungsvorschriften-im-internet.de/bsvwvbund_16052001_IIFPl.htm',
    2013: 'http://www.verwaltungsvorschriften-im-internet.de/bsvwvbund_07082012_IIA3H11041210001FPL.htm'
}


def ctext(el):
    result = []
    if el.text:
        result.append(el.text)
    for sel in el:
        if sel.tag in ["dd", "br", "div", "p"]:
            result.append(ctext(sel))
            result.append('\n')
        else:
            result.append(ctext(sel))
        if sel.tail:
            result.append(sel.tail)
    return "".join(result)


class Scraper(object):
    def scrape_2012(self, root):
        for dl in root.cssselect("dl.ez0"):
            for dt, dd in zip(dl.cssselect("dt.w9"), dl.cssselect("dd.ez9")):
                nums = dt.text_content().strip()
                for num in nums.split('/'):
                    num = num.replace('.', '').ljust(3, '0')
                    assert len(num) == 3
                    text = ctext(dd).strip().splitlines()
                    name = text[0].strip()
                    text = '\n'.join(text[1:]).strip()
                    scraperwiki.sqlite.save(unique_keys=['year', 'id'], data={
                        'year': 2012,
                        'id': num,
                        'name': name,
                        'text': text
                    })
        # Fix mistake manually
        scraperwiki.sqlite.save(unique_keys=['year', 'id'], data={
            'year': 2012,
            'id': '270',
            'name': u'Einrichtungen der Jugendhilfe',
            'text': ''
        })    

    def scrape_2013(self, root):
        last = []
        delete = False
        for tr in root.cssselect('table tr'):
            tds = tr.cssselect('td')
            nums = tds[0].text_content().strip()
            if nums:
                if last:
                    last = []
                for num in nums.split('/'):
                    num = num.ljust(3, '0')
                    assert len(num) == 3
                    name = tds[1].text_content().strip()
                    last.append({
                        'year': 2013,
                        'id': num,
                        'name': name,
                        'text': ''
                    })
            else:
                text = ctext(tds[1]).strip()
                for l in last:
                    l['text'] += text
                delete = True
            for l in last:
                scraperwiki.sqlite.save(unique_keys=['year', 'id'], data=l)
            if delete:
                last = []
                delete = False

def main():
    s = Scraper()
    for year in plans:
        html = scraperwiki.scrape(plans[year])
        getattr(s, 'scrape_%d' % year)(lxml.html.fromstring(html))
        

main()
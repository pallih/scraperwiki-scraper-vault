import scraperwiki
import lxml.html

plans = {
    2013: "http://www.verwaltungsvorschriften-im-internet.de/bsvwvbund_16052001_IIGPl.htm",
    2014: "http://www.verwaltungsvorschriften-im-internet.de/bsvwvbund_07082012_IIA3H11041210001GPL.htm"
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


def get_range(nums):
    if ' bis ' in nums:
        low, high = nums.split(' bis ', 1)
    elif '/' in nums:
        low, high = nums.split('/', 1)
    else:
        low, high = nums, nums
    low, high = low.replace('.','').strip(), high.replace('.', '').strip()
    
    low, high = int(low), int(high)
    nums = [str(x) for x in range(low, high + 1)]    
    nums = [n.ljust(3, '0') for n in nums]
    for n in nums:
        assert len(n) == 3
    return nums

    

class Scraper(object):
    def scrape_2013(self, root):
        for tr in root.cssselect('table tr'):
            tds = tr.cssselect('td')
            nums = tds[0].text_content().strip()
            if not nums:
                continue
            nums = get_range(nums)
            for num in nums:
                name = tds[1].text_content().strip()
                if not name:
                    continue
                scraperwiki.sqlite.save(unique_keys=['year', 'id'], data={
                    'year': 2013,
                    'id': num,
                    'name': name,
                    'text': ''
                })

        for dl in root.cssselect("dl.ez0"):
            for dt, dd in zip(dl.cssselect("dt.w11"), dl.cssselect("dd.ez11")):
                nums = dt.text_content().strip()
                if not nums:
                    continue
                for num in get_range(nums):
                    text = ctext(dd).strip().splitlines()
                    name = text[0].strip()
                    text = '\n'.join(text[1:]).strip()
                    scraperwiki.sqlite.save(unique_keys=['year', 'id'], data={
                        'year': 2013,
                        'id': num,
                        'name': name,
                        'text': text
                    })

    def scrape_2014(self, root):
        last = []
        last_text = []
        delete = False
        for tr in root.cssselect('table tr'):
            tds = tr.cssselect('td')
            nums = tds[0].text_content().strip()
            if nums:
                if last:
                    last = []
                    last_text = []
                nums = get_range(nums)
                for num in nums:
                    name = tds[1].text_content().strip()
                    if not name:
                        continue
                    last.append({
                        'year': 2014,
                        'id': num,
                        'name': name,
                        'text': ''
                    })
            else:
                text = ctext(tds[1]).strip()
                last_text.append(text)
                for l in last:
                    l['text'] = '\n'.join(last_text)
            for l in last:
                scraperwiki.sqlite.save(unique_keys=['year', 'id'], data=l)

def main():
    s = Scraper()
    for year in plans:
        html = scraperwiki.scrape(plans[year])
        getattr(s, 'scrape_%d' % year)(lxml.html.fromstring(html))
        

main()
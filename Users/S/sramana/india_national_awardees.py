"""List of various Indian National Award Winners
"""
import scraperwiki
import lxml.html

utils = scraperwiki.utils.swimport("utils")
utils.save.unique_keys = ['award_code', 'year', 'awardee_name']

base_url = 'http://india.gov.in/myindia/'
awards = dict()


def get_awards_list():
    url = base_url + 'advsearch_awards.php'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    options = root.cssselect('form[name=frm2] select[name=award] option')
    for option in options:
        id = option.get('value')
        if not id:
            continue
        name = option.text_content()
        awards[id] = name


@utils.cache
def get_awardees(award):
    for i in range(100000):
        url = base_url + 'awards.php?type=%s&start=%s' % (award, i*10)
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        items = root.cssselect('div.awardsblock1 ul li')
        if not items:
            break

        for item in items:
            rec = dict()
            meta = item.cssselect('span')[0]
            meta_data = meta.text_content().split(' : ')
            item.remove(meta)

            rec['awardee_name'] = item.text_content()
            rec['award_code'] = award
            rec['award_name'] = awards[award]
            rec['state'] = meta_data[-1]
            rec['year'] = meta_data[-2]
            if len(meta_data) == 3:
                rec['area'] = meta_data[-3]

            utils.save(rec)


@utils.clear_cache
def main():
    get_awards_list()
    for award in awards:
        get_awardees(award)


main()
"""List of various Indian National Award Winners
"""
import scraperwiki
import lxml.html

utils = scraperwiki.utils.swimport("utils")
utils.save.unique_keys = ['award_code', 'year', 'awardee_name']

base_url = 'http://india.gov.in/myindia/'
awards = dict()


def get_awards_list():
    url = base_url + 'advsearch_awards.php'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    options = root.cssselect('form[name=frm2] select[name=award] option')
    for option in options:
        id = option.get('value')
        if not id:
            continue
        name = option.text_content()
        awards[id] = name


@utils.cache
def get_awardees(award):
    for i in range(100000):
        url = base_url + 'awards.php?type=%s&start=%s' % (award, i*10)
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        items = root.cssselect('div.awardsblock1 ul li')
        if not items:
            break

        for item in items:
            rec = dict()
            meta = item.cssselect('span')[0]
            meta_data = meta.text_content().split(' : ')
            item.remove(meta)

            rec['awardee_name'] = item.text_content()
            rec['award_code'] = award
            rec['award_name'] = awards[award]
            rec['state'] = meta_data[-1]
            rec['year'] = meta_data[-2]
            if len(meta_data) == 3:
                rec['area'] = meta_data[-3]

            utils.save(rec)


@utils.clear_cache
def main():
    get_awards_list()
    for award in awards:
        get_awardees(award)


main()

import scraperwiki
from bs4 import BeautifulSoup

search_part1 = "http://www.findagrave.com/cgi-bin/fg.cgi?page=gsr&GSsr="
search_part2 = "&GScid=107758&CScn=rose+hill&CScntry=4&CSst=16&CScnty=782&"

import re

for n in range (1, 26):
    n40 = str((n-1)*40 + 2000)
    page = search_part1 + n40 + search_part2
    html = scraperwiki.scrape(page)
    soup = BeautifulSoup(html)

    all_on_page = soup.find_all(href=re.compile("page=gr&"))

    from lxml import html
    from urllib import urlopen

    for each in all_on_page:
        link = "http://www.findagrave.com" + each["href"]
        # data = {"URL": link }
        # print data

        # scraperwiki.sqlite.save(["URL"], data)

        # from lxml import html
        # from urllib import urlopen
        fh = urlopen(link)
        document = html.parse(fh).getroot()

        # title = document.cssselect('title')[0].text.strip()
        # title = title[:-24]
        title = document.cssselect('td.gr font b')[0].text
        birth = document.cssselect('td.gr td + td')[0].text.strip()
        death = document.cssselect('td.gr td + td')[1].text.strip()
        info = document.cssselect('td.gr * td[colspan]')[0]
        infotext = info.text_content()

        # birth = document.cssselect('birth')[0].text.strip()
        # death = document.cssselect('death')[0].text.strip()
        # data = {"Name": title, "URL": link}
        data = {"Name": title, "Birth": birth, "Death": death, "Info": infotext}

        # for el in document.cssselect('td.gr * td[colspan][0]'):           
        #     print el.text_content()

        # print data


        scraperwiki.sqlite.save(["Name"], data)
        
        """
        if document.cssselect('span.fn'):
            title = document.cssselect('span.fn')[0].text.strip()
            list_check_1 = ["lord", "baroness"]
            if any(word in title.lower() for word in list_check_1):
                data = { "Name": title, "URL": link }
                rest = document.cssselect('li.li-c span, li.li-e span')           
                if (len(rest) > 0):
                    for j in range(0, len(rest)):
                        data['%d' % (j+2)] = rest[j].text.strip()
                scraperwiki.sqlite.save(["Name"], data)
        """
import scraperwiki
from bs4 import BeautifulSoup

search_part1 = "http://www.findagrave.com/cgi-bin/fg.cgi?page=gsr&GSsr="
search_part2 = "&GScid=107758&CScn=rose+hill&CScntry=4&CSst=16&CScnty=782&"

import re

for n in range (1, 26):
    n40 = str((n-1)*40 + 2000)
    page = search_part1 + n40 + search_part2
    html = scraperwiki.scrape(page)
    soup = BeautifulSoup(html)

    all_on_page = soup.find_all(href=re.compile("page=gr&"))

    from lxml import html
    from urllib import urlopen

    for each in all_on_page:
        link = "http://www.findagrave.com" + each["href"]
        # data = {"URL": link }
        # print data

        # scraperwiki.sqlite.save(["URL"], data)

        # from lxml import html
        # from urllib import urlopen
        fh = urlopen(link)
        document = html.parse(fh).getroot()

        # title = document.cssselect('title')[0].text.strip()
        # title = title[:-24]
        title = document.cssselect('td.gr font b')[0].text
        birth = document.cssselect('td.gr td + td')[0].text.strip()
        death = document.cssselect('td.gr td + td')[1].text.strip()
        info = document.cssselect('td.gr * td[colspan]')[0]
        infotext = info.text_content()

        # birth = document.cssselect('birth')[0].text.strip()
        # death = document.cssselect('death')[0].text.strip()
        # data = {"Name": title, "URL": link}
        data = {"Name": title, "Birth": birth, "Death": death, "Info": infotext}

        # for el in document.cssselect('td.gr * td[colspan][0]'):           
        #     print el.text_content()

        # print data


        scraperwiki.sqlite.save(["Name"], data)
        
        """
        if document.cssselect('span.fn'):
            title = document.cssselect('span.fn')[0].text.strip()
            list_check_1 = ["lord", "baroness"]
            if any(word in title.lower() for word in list_check_1):
                data = { "Name": title, "URL": link }
                rest = document.cssselect('li.li-c span, li.li-e span')           
                if (len(rest) > 0):
                    for j in range(0, len(rest)):
                        data['%d' % (j+2)] = rest[j].text.strip()
                scraperwiki.sqlite.save(["Name"], data)
        """

import scraperwiki
from bs4 import BeautifulSoup

search_page = "http://data.gov.uk/data/search?q=procurement+card"

html = scraperwiki.scrape(search_page)

soup = BeautifulSoup(html)

num_results = int(soup.find("h2", "result-count").get_text())

#print num_results

if num_results % 10 == 0:
    num_pages = num_results//10
else:
    num_pages = (num_results//10) + 1

#print num_pages

for n in range (1, num_pages + 1):
    page = search_page + "&page=" + str(n)
    html = scraperwiki.scrape(page)
    soup = BeautifulSoup(html)

    all_on_page = soup.find("ul", "common-dataset-list")
    each_on_page = all_on_page.find_all("li")
    #print each_on_page

    for each in each_on_page:
        link = "http://data.gov.uk" + each.find("a", "dataset-header")["href"]
        title = each.find("h3").get_text().encode("utf8")
        list_check_1 = ["government", "procurement", "card"] 
        list_check_2 = ["gpc"]

        if all(word in title.lower() for word in list_check_1) or all(word in title.lower() for word in list_check_2):
            print title
            publisher = each.find("div", "property").get_text().replace("Publisher:", "").strip()
            description = each.find("div", "dataset-description").get_text().strip().encode("utf8")
            latest = each.find("span", "property pull-right").get_text().strip()

            data = { "URL": link, "Description": description, "Publisher": publisher, "Title": title, "Latest": latest }
            scraperwiki.sqlite.save(["URL"], data)
import scraperwiki
from bs4 import BeautifulSoup

search_page = "http://data.gov.uk/data/search?q=procurement+card"

html = scraperwiki.scrape(search_page)

soup = BeautifulSoup(html)

num_results = int(soup.find("h2", "result-count").get_text())

#print num_results

if num_results % 10 == 0:
    num_pages = num_results//10
else:
    num_pages = (num_results//10) + 1

#print num_pages

for n in range (1, num_pages + 1):
    page = search_page + "&page=" + str(n)
    html = scraperwiki.scrape(page)
    soup = BeautifulSoup(html)

    all_on_page = soup.find("ul", "common-dataset-list")
    each_on_page = all_on_page.find_all("li")
    #print each_on_page

    for each in each_on_page:
        link = "http://data.gov.uk" + each.find("a", "dataset-header")["href"]
        title = each.find("h3").get_text().encode("utf8")
        list_check_1 = ["government", "procurement", "card"] 
        list_check_2 = ["gpc"]

        if all(word in title.lower() for word in list_check_1) or all(word in title.lower() for word in list_check_2):
            print title
            publisher = each.find("div", "property").get_text().replace("Publisher:", "").strip()
            description = each.find("div", "dataset-description").get_text().strip().encode("utf8")
            latest = each.find("span", "property pull-right").get_text().strip()

            data = { "URL": link, "Description": description, "Publisher": publisher, "Title": title, "Latest": latest }
            scraperwiki.sqlite.save(["URL"], data)

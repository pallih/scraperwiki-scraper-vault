import scraperwiki
from bs4 import BeautifulSoup


def extract_meetings(url, category, subcategory):
    raw_page = scraperwiki.scrape(url)
    page_soup = BeautifulSoup(raw_page)

    main_table = page_soup.find_all("table")[4]
    all_rows = main_table.find_all("tr")

    flag = 0
    all_entries = []

    for row in all_rows:
        if flag==0:
            if "Meetings with SEC Officials" in row.get_text():
                flag = 1
            continue

        new_entry = {}
        cols = row.find_all("td")
        new_entry['category'] = category
        new_entry['subcategory'] = subcategory

        new_entry['date'] = cols[0].get_text()
        new_entry['text'] = cols[1].get_text()
        new_entry['link'] = "http://sec.gov" + cols[1].find('a').get('href')
        all_entries.append(new_entry)
    if len(all_entries) > 0:
        scraperwiki.sqlite.save(['category','subcategory','text'], all_entries, table_name="SECMeetings")

#BEGIN MAIN
#==========

url = "http://sec.gov/spotlight/regreformcomments.shtml"

raw_page = scraperwiki.scrape(url)
page_soup = BeautifulSoup(raw_page)

main_list = page_soup.find("ul")
title_list = main_list.find_all("li", recursive=False)

for title in title_list:
    category = title.find("b").get_text()
    sublist = title.find("ul")
    sublist_items = sublist.find_all("li")
    for subcategory in sublist_items:
        full_text = subcategory.get_text()
        subcat = full_text.replace("Submit Comments: Web Comment Form | Email", "").replace("Comments received are available.", "").strip()
        link = "http://sec.gov" + subcategory.find('a', text="are available").get('href')
        extract_meetings(link, category, subcat)




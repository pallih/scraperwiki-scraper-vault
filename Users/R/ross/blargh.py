#!/usr/bin/env python

import scraperwiki
import requests
import re
from bs4 import BeautifulSoup

# Hack for classic
scraperwiki.sql = scraperwiki.sqlite

# scraperwiki.sql.execute('drop table swdata')
# scraperwiki.sql.commit()

# It's faster to create the regex once. \d+ means digits
re_subpage = re.compile(".*p=(\d+):(\d+):(\d+)::.*")

def get_sub_page(url):
    # The bit we want from the URL is p=307:40:8065299045513::NO:40
    m = re_subpage.match(url)
    print m.groups()
    data = {
        "p_request":"APXWGT",
        "p_instance": m.groups()[2],
        "p_flow_id":m.groups()[0],
        "p_flow_step_id": m.groups()[1],
        "p_widget_num_return":"100",
        "p_widget_name":"worksheet",
        "p_widget_mod":"ACTION",
        "p_widget_action":"PAGE",
        "p_widget_action_mod":"pgR_min_row=1max_rows=100rows_fetched=100",
        "x01":"43365114008526011",
        "x02":"43366830004558829"}

    headers = {
        "Cookie":"WWV_CUSTOM-F_2510803204390849_307=84B868E97E666166EB907778A523C936",
    }
    
    html = requests.post("http://cgrw01.cgr.go.cr/apex/wwv_flow.show?", data=data, headers=headers)
    if html.status_code == 404:  
        # There is only a single page of results so we don't need to call the search,
        # Call the original URL instead.                 
        html = requests.get(url, headers=headers)
    return html.content

def get_root_page():
    data = {
    "p_request":"APXWGT",
    "p_instance":"8283535962848",
    "p_flow_id":"307",
    "p_flow_step_id":"36",
    "p_widget_num_return":"250", # Gets 250 records max
    "p_widget_name":"worksheet",
    "p_widget_mod":"ACTION",
    "p_widget_action":"PAGE",
    "p_widget_action_mod":"pgR_min_row=0max_rows=250rows_fetched=0",  # Just to be safe tell them we want 250
    "x01":"43340102598786160",
    "x02":"43342327187829426",
    }
    headers = {
        "Cookie":"WWV_CUSTOM-F_2510803204390849_307=977E6A1EC305155F28EE4559205AFABF;  ORACLE_SMP_CHRONOS_GL=24:1373611929:611517",
    }
    html = requests.post("http://cgrw01.cgr.go.cr/apex/wwv_flow.show", data=data, headers=headers)
    return html.content


root_page = get_root_page() # Gets ALL the content!!!
soup = BeautifulSoup(root_page)
table = soup.find("table", "apexir_WORKSHEET_DATA")
trs = table.find_all("tr")
rows = []
for tr in trs[2:10]:
    if not tr.find("br"):
        tds = tr.find_all("td")
        institucion = tds[0].get_text()
        link = "http://cgrw01.cgr.go.cr/apex/" + tds[0].find("a")["href"]

        # The is ALL the search results after following the link.
        # Or rather it should be, they've all got very similar links and it breaks.

        # There's something weird going on with cookies, because even in Chrome I can 
        # wait a while and then the next button doesn't work (sends me to a 404) so it
        # looks like it is remembering your last request. This sucks.
        # Might be worth trying with mechanize
        #print institucion, link
        #print get_sub_page(link)

        procedimientos_iniciados = int(tds[1].get_text())
        procedimientos_adjudicados = int(tds[2].get_text())
        monto = int(str(tds[3].get_text()).replace(".",""))
        porcentaje = float(str(tds[4].get_text()).replace(",", "."))
        data = { "Procedimientos iniciados": procedimientos_iniciados, "Institucion": institucion, "url": link, "Procedimientos adjudicados": procedimientos_adjudicados, "Monto": monto, "Porcentaje": porcentaje}
        rows.append(data)        

scraperwiki.sql.save(["url"], rows)
#!/usr/bin/env python

import scraperwiki
import requests
import re
from bs4 import BeautifulSoup

# Hack for classic
scraperwiki.sql = scraperwiki.sqlite

# scraperwiki.sql.execute('drop table swdata')
# scraperwiki.sql.commit()

# It's faster to create the regex once. \d+ means digits
re_subpage = re.compile(".*p=(\d+):(\d+):(\d+)::.*")

def get_sub_page(url):
    # The bit we want from the URL is p=307:40:8065299045513::NO:40
    m = re_subpage.match(url)
    print m.groups()
    data = {
        "p_request":"APXWGT",
        "p_instance": m.groups()[2],
        "p_flow_id":m.groups()[0],
        "p_flow_step_id": m.groups()[1],
        "p_widget_num_return":"100",
        "p_widget_name":"worksheet",
        "p_widget_mod":"ACTION",
        "p_widget_action":"PAGE",
        "p_widget_action_mod":"pgR_min_row=1max_rows=100rows_fetched=100",
        "x01":"43365114008526011",
        "x02":"43366830004558829"}

    headers = {
        "Cookie":"WWV_CUSTOM-F_2510803204390849_307=84B868E97E666166EB907778A523C936",
    }
    
    html = requests.post("http://cgrw01.cgr.go.cr/apex/wwv_flow.show?", data=data, headers=headers)
    if html.status_code == 404:  
        # There is only a single page of results so we don't need to call the search,
        # Call the original URL instead.                 
        html = requests.get(url, headers=headers)
    return html.content

def get_root_page():
    data = {
    "p_request":"APXWGT",
    "p_instance":"8283535962848",
    "p_flow_id":"307",
    "p_flow_step_id":"36",
    "p_widget_num_return":"250", # Gets 250 records max
    "p_widget_name":"worksheet",
    "p_widget_mod":"ACTION",
    "p_widget_action":"PAGE",
    "p_widget_action_mod":"pgR_min_row=0max_rows=250rows_fetched=0",  # Just to be safe tell them we want 250
    "x01":"43340102598786160",
    "x02":"43342327187829426",
    }
    headers = {
        "Cookie":"WWV_CUSTOM-F_2510803204390849_307=977E6A1EC305155F28EE4559205AFABF;  ORACLE_SMP_CHRONOS_GL=24:1373611929:611517",
    }
    html = requests.post("http://cgrw01.cgr.go.cr/apex/wwv_flow.show", data=data, headers=headers)
    return html.content


root_page = get_root_page() # Gets ALL the content!!!
soup = BeautifulSoup(root_page)
table = soup.find("table", "apexir_WORKSHEET_DATA")
trs = table.find_all("tr")
rows = []
for tr in trs[2:10]:
    if not tr.find("br"):
        tds = tr.find_all("td")
        institucion = tds[0].get_text()
        link = "http://cgrw01.cgr.go.cr/apex/" + tds[0].find("a")["href"]

        # The is ALL the search results after following the link.
        # Or rather it should be, they've all got very similar links and it breaks.

        # There's something weird going on with cookies, because even in Chrome I can 
        # wait a while and then the next button doesn't work (sends me to a 404) so it
        # looks like it is remembering your last request. This sucks.
        # Might be worth trying with mechanize
        #print institucion, link
        #print get_sub_page(link)

        procedimientos_iniciados = int(tds[1].get_text())
        procedimientos_adjudicados = int(tds[2].get_text())
        monto = int(str(tds[3].get_text()).replace(".",""))
        porcentaje = float(str(tds[4].get_text()).replace(",", "."))
        data = { "Procedimientos iniciados": procedimientos_iniciados, "Institucion": institucion, "url": link, "Procedimientos adjudicados": procedimientos_adjudicados, "Monto": monto, "Porcentaje": porcentaje}
        rows.append(data)        

scraperwiki.sql.save(["url"], rows)
#!/usr/bin/env python

import scraperwiki
import requests
import re
from bs4 import BeautifulSoup

# Hack for classic
scraperwiki.sql = scraperwiki.sqlite

# scraperwiki.sql.execute('drop table swdata')
# scraperwiki.sql.commit()

# It's faster to create the regex once. \d+ means digits
re_subpage = re.compile(".*p=(\d+):(\d+):(\d+)::.*")

def get_sub_page(url):
    # The bit we want from the URL is p=307:40:8065299045513::NO:40
    m = re_subpage.match(url)
    print m.groups()
    data = {
        "p_request":"APXWGT",
        "p_instance": m.groups()[2],
        "p_flow_id":m.groups()[0],
        "p_flow_step_id": m.groups()[1],
        "p_widget_num_return":"100",
        "p_widget_name":"worksheet",
        "p_widget_mod":"ACTION",
        "p_widget_action":"PAGE",
        "p_widget_action_mod":"pgR_min_row=1max_rows=100rows_fetched=100",
        "x01":"43365114008526011",
        "x02":"43366830004558829"}

    headers = {
        "Cookie":"WWV_CUSTOM-F_2510803204390849_307=84B868E97E666166EB907778A523C936",
    }
    
    html = requests.post("http://cgrw01.cgr.go.cr/apex/wwv_flow.show?", data=data, headers=headers)
    if html.status_code == 404:  
        # There is only a single page of results so we don't need to call the search,
        # Call the original URL instead.                 
        html = requests.get(url, headers=headers)
    return html.content

def get_root_page():
    data = {
    "p_request":"APXWGT",
    "p_instance":"8283535962848",
    "p_flow_id":"307",
    "p_flow_step_id":"36",
    "p_widget_num_return":"250", # Gets 250 records max
    "p_widget_name":"worksheet",
    "p_widget_mod":"ACTION",
    "p_widget_action":"PAGE",
    "p_widget_action_mod":"pgR_min_row=0max_rows=250rows_fetched=0",  # Just to be safe tell them we want 250
    "x01":"43340102598786160",
    "x02":"43342327187829426",
    }
    headers = {
        "Cookie":"WWV_CUSTOM-F_2510803204390849_307=977E6A1EC305155F28EE4559205AFABF;  ORACLE_SMP_CHRONOS_GL=24:1373611929:611517",
    }
    html = requests.post("http://cgrw01.cgr.go.cr/apex/wwv_flow.show", data=data, headers=headers)
    return html.content


root_page = get_root_page() # Gets ALL the content!!!
soup = BeautifulSoup(root_page)
table = soup.find("table", "apexir_WORKSHEET_DATA")
trs = table.find_all("tr")
rows = []
for tr in trs[2:10]:
    if not tr.find("br"):
        tds = tr.find_all("td")
        institucion = tds[0].get_text()
        link = "http://cgrw01.cgr.go.cr/apex/" + tds[0].find("a")["href"]

        # The is ALL the search results after following the link.
        # Or rather it should be, they've all got very similar links and it breaks.

        # There's something weird going on with cookies, because even in Chrome I can 
        # wait a while and then the next button doesn't work (sends me to a 404) so it
        # looks like it is remembering your last request. This sucks.
        # Might be worth trying with mechanize
        #print institucion, link
        #print get_sub_page(link)

        procedimientos_iniciados = int(tds[1].get_text())
        procedimientos_adjudicados = int(tds[2].get_text())
        monto = int(str(tds[3].get_text()).replace(".",""))
        porcentaje = float(str(tds[4].get_text()).replace(",", "."))
        data = { "Procedimientos iniciados": procedimientos_iniciados, "Institucion": institucion, "url": link, "Procedimientos adjudicados": procedimientos_adjudicados, "Monto": monto, "Porcentaje": porcentaje}
        rows.append(data)        

scraperwiki.sql.save(["url"], rows)

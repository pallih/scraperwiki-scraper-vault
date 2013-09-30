#!/usr/bin/env python
 
import scraperwiki
import requests
from bs4 import BeautifulSoup
 
# scraperwiki.sql.execute('drop table swdata')
# scraperwiki.sql.commit()
 
def get_next_page(offset):
    data = {
    "p_request":"APXWGT",
    "p_instance":"8283535962848",
    "p_flow_id":"307",
    "p_flow_step_id":"36",
    "p_widget_num_return":"15",
    "p_widget_name":"worksheet",
    "p_widget_mod":"ACTION",
    "p_widget_action":"PAGE",
    "p_widget_action_mod":"pgR_min_row={0}max_rows=15rows_fetched=15".format(offset),
    "x01":"43340102598786160",
    "x02":"43342327187829426",
    }
    headers = {
        "Cookie":"WWV_CUSTOM-F_2510803204390849_307=977E6A1EC305155F28EE4559205AFABF",
    }
    html = requests.post("http://cgrw01.cgr.go.cr/apex/wwv_flow.show", data=data, headers=headers)
    return html.content
 
pages = [1, 16, 31, 46, 61]
 
for page in pages:
 
    soup = BeautifulSoup(get_next_page(page))
    table = soup.find("table", "apexir_WORKSHEET_DATA")
    trs = table.find_all("tr")
 
    for tr in trs[2:]:
        if not tr.find("br"):
            tds = tr.find_all("td")
            institucion = tds[0].get_text()
            link = "http://cgrw01.cgr.go.cr/apex/" + tds[0].find("a")["href"]
            procedimientos_iniciados = int(tds[1].get_text())
            procedimientos_adjudicados = int(tds[2].get_text())
            monto = int(str(tds[3].get_text()).replace(".",""))
            porcentaje = float(str(tds[4].get_text()).replace(",", "."))
            data = { "Procedimientos iniciados": procedimientos_iniciados, "Institucion": institucion, "url": link, "Procedimientos adjudicados": procedimientos_adjudicados, "Monto": monto, "Porcentaje": porcentaje}
            scraperwiki.sql.save(["url"], data)
#!/usr/bin/env python
 
import scraperwiki
import requests
from bs4 import BeautifulSoup
 
# scraperwiki.sql.execute('drop table swdata')
# scraperwiki.sql.commit()
 
def get_next_page(offset):
    data = {
    "p_request":"APXWGT",
    "p_instance":"8283535962848",
    "p_flow_id":"307",
    "p_flow_step_id":"36",
    "p_widget_num_return":"15",
    "p_widget_name":"worksheet",
    "p_widget_mod":"ACTION",
    "p_widget_action":"PAGE",
    "p_widget_action_mod":"pgR_min_row={0}max_rows=15rows_fetched=15".format(offset),
    "x01":"43340102598786160",
    "x02":"43342327187829426",
    }
    headers = {
        "Cookie":"WWV_CUSTOM-F_2510803204390849_307=977E6A1EC305155F28EE4559205AFABF",
    }
    html = requests.post("http://cgrw01.cgr.go.cr/apex/wwv_flow.show", data=data, headers=headers)
    return html.content
 
pages = [1, 16, 31, 46, 61]
 
for page in pages:
 
    soup = BeautifulSoup(get_next_page(page))
    table = soup.find("table", "apexir_WORKSHEET_DATA")
    trs = table.find_all("tr")
 
    for tr in trs[2:]:
        if not tr.find("br"):
            tds = tr.find_all("td")
            institucion = tds[0].get_text()
            link = "http://cgrw01.cgr.go.cr/apex/" + tds[0].find("a")["href"]
            procedimientos_iniciados = int(tds[1].get_text())
            procedimientos_adjudicados = int(tds[2].get_text())
            monto = int(str(tds[3].get_text()).replace(".",""))
            porcentaje = float(str(tds[4].get_text()).replace(",", "."))
            data = { "Procedimientos iniciados": procedimientos_iniciados, "Institucion": institucion, "url": link, "Procedimientos adjudicados": procedimientos_adjudicados, "Monto": monto, "Porcentaje": porcentaje}
            scraperwiki.sql.save(["url"], data)

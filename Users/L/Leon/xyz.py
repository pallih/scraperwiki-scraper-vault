#! /usr/bin/eny python

from __future__ import print_function
import datetime
import scraperwiki
import mechanize
import HTMLParser
import lxml.html

THIS_YEAR = datetime.date.today().year

class parser(HTMLParser.HTMLParser):
    """
    Parsing data from specified tags or classes.
    """
    form_a = ""
    def handle_starttag(self, tag, attrs):
        if tag == "table":
            print(tag, attrs)

    def handle_data(self, data):
        print(data)

def scrape(url, form_name):
    browser = mechanize.Browser()
    browser.open(url)
    browser.select_form(name=form_name)
    return browser.submit().read()

def scrape_lxml():
    pass


def requested_annuals():
    '''
    從資料庫開既有的週轉率html，如果都沒有的話就填入init_annuals。
    '''
    scraperwiki.sqlite.attach("test_htmlparser") #
    existed_annuals = []
    requested_annuals = []
    annuals_in_table = scraperwiki.sqlite.select("annual FROM test_htmlparser.turnover_rates_html") #
    #annuals_in_table = []
    for annual in annuals_in_table:
        existed_annuals += [annual["annual"]]
    #existed_annuals = ['2001', '2011'] #
    for init_annual in init_annuals:
        if not init_annual in existed_annuals:
            requested_annuals += [init_annual]
    requested_annuals.sort()
    return requested_annuals


def test0721_scrape_and_clear():
    def clear_html(source_html):        
        html = lxml.html.fromstring(source_html)
        table0 = html.get_element_by_id("GlobalTable")
        table1 = html.cssselect("#GlobalTable tbody tr td table")[1]
        table2 = table1.cssselect("table")[0]
        return lxml.html.tostring(table2, encoding="unicode", pretty_print=True)

    requested_annuals = [2001, 2002]
    browser = mechanize.Browser()
    browser.open("http://www.sitca.org.tw/ROC/Industry/IN2211.aspx")
    html = []
    for annual in requested_annuals:
        browser.select_form(name="aspnetForm")
        browser["ctl00$ContentPlaceHolder1$ddlQ_Y"] = [str(annual)] # 年
        browser["ctl00$ContentPlaceHolder1$ddlQ_M"] = ["Year"] # 月／季／年
        browser["ctl00$ContentPlaceHolder1$ddlQ_Comid"] = [""] # 公司，無作用，原因不明。
        #annual_html = {"annual": int(annual), "html": clear_html(browser.submit().read().decode("utf-8"))}
        html += [clear_html(browser.submit().read().decode("utf-8"))]
    return html

def test0721_parse(source_html):
    dom = lxml.html.fromstring(source_html[0])
    table = dom.cssselect("table")[0]
    rows = table.cssselect("tr") # List
    for row in rows[3:5]: # 一次處理表格的一列
        row_data = [] # 暫存用，每跑完一列清除。
        cells = row.cssselect("td")
        for cell in cells: # 抓每一格的內容存到row_data -> dicts
            if cell.find_class("DTHeader"): # 辨別表格標題並篩選掉
                pass
            else:
                cell_value = cell.text_content()
                row_data.append(cell_value)
        print(row_data[2])


url = "http://www.sitca.org.tw/ROC/Industry/IN2105.aspx"
form_name = "aspnetForm"
#html = scrape(url, form_name)
#parser = parser()
#parser.feed("<table aa='1'><p>abcd</p></table><table bb='2'>xxx<table bbb='1'>ddd</table></table>")
#parser.close()

init_annuals = tuple([str(year) for year in list(range(2001, THIS_YEAR))]) # 年度自動計算從2001年到去年
#init_annuals = ["2001"]
#requested_annuals = requested_annuals()
#print(requested_annuals)

html = test0721_scrape_and_clear()
test0721_parse(html)
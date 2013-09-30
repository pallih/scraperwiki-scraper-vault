#! /usr/bin/eny python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import datetime
import math
import mechanize
import lxml.html
import scraperwiki

reload(sys)
sys.setdefaultencoding('utf-8')

THIS_YEAR = datetime.date.today().year
LAST_YEAR = THIS_YEAR - 1

class Fund:
    def __init__(self, fund_type, id, isin, name, inception_date):
        self.type = fund_type
        self.id = id
        self.isin = isin # 從201206起有ISIN Code
        self.name = name
        self.inception_date = inception_date
        self.turnover_rates = {}
        self.rate_of_return = {}

    def add_turnover_rate(self, annual, turnover_rate):
        '''
        用Dict才能用年份存取，例：Fund.turnover_rates[2003]
        '''
        self.turnover_rates[annual] = turnover_rate

    def average_turnover_rate(self):
        '''
        算術平均數
        '''
        denominator = len(self.turnover_rates) - 1 # 分母減去成立那年
        numerator = 0
        for key in self.turnover_rates:
            if key != self.inception_date.year:
                numerator += self.turnover_rates[key]
        return numerator / denominator
        
    def add_rate_of_return(self, annual, rate_of_return):
        self.rate_of_return[annual] = rate_of_return

    def average_rate_of_return(self):
        '''
        幾何平均數
        '''
        denominator = len(rate_of_return) - 1 # 分母減去成立那年
        numerator = 0
        for key in self.rate_of_return:
            if key != self.inception_date.year:
                numerator += self.rate_of_return[key]
        self.average_rate_of_return = numerator / denominator
        return self.average_rate_of_return

def scrape(target):
    def profile():
        '''
        抓最新的基金資料
        '''
        browser = mechanize.Browser()
        #browser.set_handle_robots(False) # 这个是设置对方网站的robots.txt是否起作用。設成False還是會載入robots.txt…。
        browser.open("http://www.sitca.org.tw/ROC/Industry/IN2105.aspx")
        browser.select_form(name="aspnetForm")
        browser["ctl00$ContentPlaceHolder1$ddlQ_YYYYMM"] = [] # 年月，格式："201206"，表示2012年6月。
        browser["ctl00$ContentPlaceHolder1$ddlQ_Comid"] = [] # 測試只要小量資料時設為A0003
        return browser.submit().read().decode("utf-8") # Decoding form utf-8 to unicode.

    def turnover_rate():
        '''
        輸出格式：{2001: "<html>", 2003: "<html>", ...}
        '''
        def scrape_requested():
            def requested_annuals():
                '''
                從資料庫開既有的週轉率html，如果都沒有的話就填入init_annuals。
                '''
                existed_annuals = []
                requested_annuals = []
                try:
                    annuals_in_table = scraperwiki.sqlite.select("annual FROM turnover_rates_html") # 沒有表格的話勒？就給它try囉～
                except:
                    pass
                else:
                    for annual in annuals_in_table:
                        existed_annuals += [annual["annual"]]
                finally:
                    for init_annual in init_annuals:
                        if not init_annual in existed_annuals:
                            requested_annuals += [init_annual]
                    requested_annuals.sort()
                    return requested_annuals

            def clear_html(source_html):        
                html = lxml.html.fromstring(source_html)
                table0 = html.get_element_by_id("GlobalTable")
                table1 = html.cssselect("#GlobalTable tbody tr td table")[1]
                table2 = table1.cssselect("table")[0]
                return lxml.html.tostring(table2, encoding="unicode", pretty_print=True)

            init_annuals = tuple([year for year in list(range(2001, THIS_YEAR))]) # 年度自動計算從2001年到去年
            requested_annuals = requested_annuals() # List
            if requested_annuals: # 如果有要抓的年份再去抓，沒有就連mechanize都不用開惹。
                browser = mechanize.Browser()
                browser.open("http://www.sitca.org.tw/ROC/Industry/IN2211.aspx")
                for annual in requested_annuals:
                    browser.select_form(name="aspnetForm")
                    browser["ctl00$ContentPlaceHolder1$ddlQ_Y"] = [str(annual)] # 年
                    browser["ctl00$ContentPlaceHolder1$ddlQ_M"] = ["Year"] # 月／季／年
                    browser["ctl00$ContentPlaceHolder1$ddlQ_Comid"] = [""] # 公司，無作用，原因不明。
                    annual_html = {"annual": int(annual), "html": clear_html(browser.submit().read().decode("utf-8"))}
                    scraperwiki.sqlite.save(unique_keys=["annual"],  data=annual_html, table_name="turnover_rates_html")

        turnover_rates = {}
        scrape_requested()
        turnover_rates_in_table = scraperwiki.sqlite.select("* FROM turnover_rates_html")
        for turnover_rate in turnover_rates_in_table:
            turnover_rates[turnover_rate["annual"]] = turnover_rate["html"]
        return turnover_rates

    def rate_of_return():
        browser = mechanize.Browser()
        browser.open("http://www.sitca.org.tw/ROC/Industry/IN2430.aspx")
        browser.select_form(name="aspnetForm")
        return browser.submit().read().decode("utf-8")

    if target == "profile":
        return profile()
    elif target == "turnover_rate":
        return turnover_rate()
    elif target == "rate_of_return":
        return rate_of_return()

def parse(source):
    def profile():
        '''
        Parsing html source to save fund profiles to a List of Dicts.
        格式：[{"fund_typa": "AA1", "id": "00965469B", "name": "第一金復國基金", "inception_data": 20010101}, {...}, ...]以此類推
        '''
        data_list_of_dicts = []
        dom = lxml.html.fromstring(source)
        table = dom.get_element_by_id("ctl00_ContentPlaceHolder1_Table1")
        rows = table.cssselect("tr") # List
        for row in rows[2:]: # 閃掉表格標題列
            cells = row.cssselect("td")
            if datetime.datetime.strptime(cells[8].text_content(), "%Y%m%d").year < LAST_YEAR:
                data_list_of_dicts += [{"fund_type": cells[0].text_content(), 
                                         "id": cells[1].text_content(), 
                                         "isin": cells[2].text_content(),
                                         "name": cells[3].text_content(), 
                                         "inception_date": datetime.datetime.strptime(cells[8].text_content(), "%Y%m%d")}]
        return data_list_of_dicts

    def turnover_rate():
        '''
        輸出格式：[{"id": "00965469A", "turnover_rate_2011": "4.40%", "turnover_rate_2010:" "4.00%", ......}]以此類推
        '''
        def get_column(annual):
            '''
            2001 - 2004為舊格式、2005起為新格式
            決定週轉率所在欄位
            '''
            if annual >= 2005: column = 16
            elif annual <= 2004: column = 14
            return column

        def data():
            '''
            取得含已清算基金的原始資料
            輸出格式 {"00965469": {"id": "00965469", "turnover_rate_2011": "4.40%", "turnover_rate_2010:" "4.00%", ......}, ...{...}, ...}以此類推
            '''
            dicts = {}
            for annual in source: # 一次處理一年份的網頁
                column = get_column(annual)
                print("Parsing turnover rate of " + str(annual) + ". The turnover rates are at column " + str(column) + ".")
                dom = lxml.html.fromstring(source[annual])
                table = dom.cssselect("table")[0]
                rows = table.cssselect("tr") # List
                print("Still parsing...")
                for row in rows[3:]: # 一次處理表格的一列，並過濾掉表格前三行標題列。
                    row_data = [] # 暫存用，每跑完一列清除。
                    cells = row.cssselect("td")
                    for cell in cells: # 抓每一格的內容存到row_data -> dicts
                        cell_value = cell.text_content()
                        row_data.append(cell_value)
                    if cells[1].text_content() in dicts: # 檢查id是否已經有資料，有update，沒有就新增。資料列從row_data取出id和每年度turnover_rate存到dicts。
                        dicts[cells[1].text_content()].update({"id": cells[1].text_content(), 
                                                               "turnover_rate_" + str(annual): float(row_data[column][0:-1]) / 100})
                    else:
                        dicts[cells[1].text_content()] = {"id": cells[1].text_content(), 
                                                          "turnover_rate_" + str(annual): float(row_data[column][0:-1]) / 100}
            return dicts

        def filte(raw_data):
            '''
            拿現有profile_data的id比對原始資料，比對不到的刪除之。
            並作格式轉換
            '''
            filtered_data = []
            profile_id_list = []
            for row in profile_data: # 從profile_data建立要保留的profile_id_list
                profile_id_list += [row["id"]]            
            for row_key in raw_data: # 以profile_id_list為準比對row_key，合者存至filtered_data。
                for profile_id in profile_id_list: # profile_id有的有是97977870A或97977870B，而row_key結尾有些有去掉A、B，故要用in來逐條比對不用==比對。
                    if row_key in profile_id:
                        filtered_data += [raw_data[row_key]]
            return filtered_data

        raw_data = data()
        filtered_data = filte(raw_data)
        return filtered_data

    def rate_of_return(source):
        def convert_to_float(string):
            try:
                return float(string) / 100
            except ValueError:
                return

        rate_of_return_dict = {}
        dom = lxml.html.fromstring(source)
        table = dom.get_element_by_id("ctl00_ContentPlaceHolder1_GridView1")
        rows = table.cssselect("tr")
        for row in rows[2:]: # 過濾掉表格標題列
            cells = row.cssselect("td")
            rate_of_return_dict[cells[4].text_content()] = {"id": cells[4].text_content(),
                                                            2002: convert_to_float(cells[6].text_content()),
                                                            2003: convert_to_float(cells[7].text_content()),
                                                            2004: convert_to_float(cells[8].text_content()),
                                                            2005: convert_to_float(cells[9].text_content()),
                                                            2006: convert_to_float(cells[10].text_content()),
                                                            2007: convert_to_float(cells[11].text_content()),
                                                            2008: convert_to_float(cells[12].text_content()),
                                                            2009: convert_to_float(cells[13].text_content()),
                                                            2010: convert_to_float(cells[14].text_content()),
                                                            2011: convert_to_float(cells[15].text_content())}
        for fund_id in rate_of_return_dict:
            print(rate_of_return_dict[fund_id])
            for key in rate_of_return_dict[fund_id].keys():
                if rate_of_return_dict[fund_id][key] == None:
                    del rate_of_return_dict[fund_id][key]

        print(rate_of_return_dict)
        return rate_of_return_dict

    print("Parsing ", end="")
    if source == profile_html:
        print("profile.")
        return profile()
    elif source == turnover_rate_html:
        print("turnover rate...")
        return turnover_rate()
    elif source == rate_of_return_html:
        print("rate of return...")
        return rate_of_return(source)

def save_data(profile_data, turnover_rate_data):
    '''
    把profile_data和turnover_rate_data合併，並刪除不要的欄位，最後存到DB內。
    '''
    def couple():
        coupled_data = profile_data[:]
        for turnover_rate_item in turnover_rate_data:
            for coupled_item in coupled_data:
                if turnover_rate_item["id"] in coupled_item["id"]:
                    turnover_rate_item_without_id = turnover_rate_item.copy()
                    del turnover_rate_item_without_id["id"]
                    coupled_item.update(turnover_rate_item_without_id)
        return coupled_data

    def del_inception_year_data(list_of_dicts):
        '''
        刪掉每筆基金成立年的週轉率資料，注意週轉率資料最早只到2001年，有些基金早於2001年成立。
        用str型態再用in去比較比較好處理
        '''
        for dict_item in list_of_dicts:
            inception_year = str(dict_item["inception_date"].year)
            for key in dict_item.keys():
                if inception_year in key:
                    del dict_item[key]
        return list_of_dicts

    def add_turnover_rate_average(list_of_dicts):
        for dict_item in list_of_dicts:
            denominator = 0
            numerator = 0
            for key in dict_item:
                if "turnover_rate_" in key:
                    denominator += 1
                    numerator += dict_item[key]
            dict_item["turnover_rate_average"] = numerator / denominator
        return list_of_dicts

    coupled_data = couple()
    coupled_data = del_inception_year_data(coupled_data)
    coupled_data = add_turnover_rate_average(coupled_data)
    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS swdata") # 先把既有的swdata表格刪除，避免舊資料遺留。沒刪除的話已合併或消滅的遺體可能會存在。
    scraperwiki.sqlite.save(unique_keys=["id"], data=coupled_data)
    return print("Data saved.")

fund_dict = {}

profile_html = scrape("profile")
profile_data = parse(profile_html)
for fund_item in profile_data:
    fund = Fund(fund_item["fund_type"], fund_item["id"], fund_item["isin"], fund_item["name"], fund_item["inception_date"])
    fund_dict[fund_item["id"]] = fund

turnover_rate_html = scrape("turnover_rate")
turnover_rate_data = parse(turnover_rate_html)
for fund_item in turnover_rate_data:
    for key in fund_item:
        if "turnover_rate_" in key:
            annual = int(key[14:])
            try:
                fund_dict[fund_item["id"]].add_turnover_rate(annual, fund_item[key])
            except KeyError:
                fund_dict[fund_item["id"]+"A"].add_turnover_rate(annual, fund_item[key])
                fund_dict[fund_item["id"]+"B"].add_turnover_rate(annual, fund_item[key])
                
print(fund_dict["48862809"].turnover_rates, fund_dict["48862809"].average_turnover_rate(), fund_dict['48862809'].inception_date)

rate_of_return_html = scrape("rate_of_return")
rate_of_return_data = parse(rate_of_return_html)

#save_data(profile_data, turnover_rate_data)#! /usr/bin/eny python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import datetime
import math
import mechanize
import lxml.html
import scraperwiki

reload(sys)
sys.setdefaultencoding('utf-8')

THIS_YEAR = datetime.date.today().year
LAST_YEAR = THIS_YEAR - 1

class Fund:
    def __init__(self, fund_type, id, isin, name, inception_date):
        self.type = fund_type
        self.id = id
        self.isin = isin # 從201206起有ISIN Code
        self.name = name
        self.inception_date = inception_date
        self.turnover_rates = {}
        self.rate_of_return = {}

    def add_turnover_rate(self, annual, turnover_rate):
        '''
        用Dict才能用年份存取，例：Fund.turnover_rates[2003]
        '''
        self.turnover_rates[annual] = turnover_rate

    def average_turnover_rate(self):
        '''
        算術平均數
        '''
        denominator = len(self.turnover_rates) - 1 # 分母減去成立那年
        numerator = 0
        for key in self.turnover_rates:
            if key != self.inception_date.year:
                numerator += self.turnover_rates[key]
        return numerator / denominator
        
    def add_rate_of_return(self, annual, rate_of_return):
        self.rate_of_return[annual] = rate_of_return

    def average_rate_of_return(self):
        '''
        幾何平均數
        '''
        denominator = len(rate_of_return) - 1 # 分母減去成立那年
        numerator = 0
        for key in self.rate_of_return:
            if key != self.inception_date.year:
                numerator += self.rate_of_return[key]
        self.average_rate_of_return = numerator / denominator
        return self.average_rate_of_return

def scrape(target):
    def profile():
        '''
        抓最新的基金資料
        '''
        browser = mechanize.Browser()
        #browser.set_handle_robots(False) # 这个是设置对方网站的robots.txt是否起作用。設成False還是會載入robots.txt…。
        browser.open("http://www.sitca.org.tw/ROC/Industry/IN2105.aspx")
        browser.select_form(name="aspnetForm")
        browser["ctl00$ContentPlaceHolder1$ddlQ_YYYYMM"] = [] # 年月，格式："201206"，表示2012年6月。
        browser["ctl00$ContentPlaceHolder1$ddlQ_Comid"] = [] # 測試只要小量資料時設為A0003
        return browser.submit().read().decode("utf-8") # Decoding form utf-8 to unicode.

    def turnover_rate():
        '''
        輸出格式：{2001: "<html>", 2003: "<html>", ...}
        '''
        def scrape_requested():
            def requested_annuals():
                '''
                從資料庫開既有的週轉率html，如果都沒有的話就填入init_annuals。
                '''
                existed_annuals = []
                requested_annuals = []
                try:
                    annuals_in_table = scraperwiki.sqlite.select("annual FROM turnover_rates_html") # 沒有表格的話勒？就給它try囉～
                except:
                    pass
                else:
                    for annual in annuals_in_table:
                        existed_annuals += [annual["annual"]]
                finally:
                    for init_annual in init_annuals:
                        if not init_annual in existed_annuals:
                            requested_annuals += [init_annual]
                    requested_annuals.sort()
                    return requested_annuals

            def clear_html(source_html):        
                html = lxml.html.fromstring(source_html)
                table0 = html.get_element_by_id("GlobalTable")
                table1 = html.cssselect("#GlobalTable tbody tr td table")[1]
                table2 = table1.cssselect("table")[0]
                return lxml.html.tostring(table2, encoding="unicode", pretty_print=True)

            init_annuals = tuple([year for year in list(range(2001, THIS_YEAR))]) # 年度自動計算從2001年到去年
            requested_annuals = requested_annuals() # List
            if requested_annuals: # 如果有要抓的年份再去抓，沒有就連mechanize都不用開惹。
                browser = mechanize.Browser()
                browser.open("http://www.sitca.org.tw/ROC/Industry/IN2211.aspx")
                for annual in requested_annuals:
                    browser.select_form(name="aspnetForm")
                    browser["ctl00$ContentPlaceHolder1$ddlQ_Y"] = [str(annual)] # 年
                    browser["ctl00$ContentPlaceHolder1$ddlQ_M"] = ["Year"] # 月／季／年
                    browser["ctl00$ContentPlaceHolder1$ddlQ_Comid"] = [""] # 公司，無作用，原因不明。
                    annual_html = {"annual": int(annual), "html": clear_html(browser.submit().read().decode("utf-8"))}
                    scraperwiki.sqlite.save(unique_keys=["annual"],  data=annual_html, table_name="turnover_rates_html")

        turnover_rates = {}
        scrape_requested()
        turnover_rates_in_table = scraperwiki.sqlite.select("* FROM turnover_rates_html")
        for turnover_rate in turnover_rates_in_table:
            turnover_rates[turnover_rate["annual"]] = turnover_rate["html"]
        return turnover_rates

    def rate_of_return():
        browser = mechanize.Browser()
        browser.open("http://www.sitca.org.tw/ROC/Industry/IN2430.aspx")
        browser.select_form(name="aspnetForm")
        return browser.submit().read().decode("utf-8")

    if target == "profile":
        return profile()
    elif target == "turnover_rate":
        return turnover_rate()
    elif target == "rate_of_return":
        return rate_of_return()

def parse(source):
    def profile():
        '''
        Parsing html source to save fund profiles to a List of Dicts.
        格式：[{"fund_typa": "AA1", "id": "00965469B", "name": "第一金復國基金", "inception_data": 20010101}, {...}, ...]以此類推
        '''
        data_list_of_dicts = []
        dom = lxml.html.fromstring(source)
        table = dom.get_element_by_id("ctl00_ContentPlaceHolder1_Table1")
        rows = table.cssselect("tr") # List
        for row in rows[2:]: # 閃掉表格標題列
            cells = row.cssselect("td")
            if datetime.datetime.strptime(cells[8].text_content(), "%Y%m%d").year < LAST_YEAR:
                data_list_of_dicts += [{"fund_type": cells[0].text_content(), 
                                         "id": cells[1].text_content(), 
                                         "isin": cells[2].text_content(),
                                         "name": cells[3].text_content(), 
                                         "inception_date": datetime.datetime.strptime(cells[8].text_content(), "%Y%m%d")}]
        return data_list_of_dicts

    def turnover_rate():
        '''
        輸出格式：[{"id": "00965469A", "turnover_rate_2011": "4.40%", "turnover_rate_2010:" "4.00%", ......}]以此類推
        '''
        def get_column(annual):
            '''
            2001 - 2004為舊格式、2005起為新格式
            決定週轉率所在欄位
            '''
            if annual >= 2005: column = 16
            elif annual <= 2004: column = 14
            return column

        def data():
            '''
            取得含已清算基金的原始資料
            輸出格式 {"00965469": {"id": "00965469", "turnover_rate_2011": "4.40%", "turnover_rate_2010:" "4.00%", ......}, ...{...}, ...}以此類推
            '''
            dicts = {}
            for annual in source: # 一次處理一年份的網頁
                column = get_column(annual)
                print("Parsing turnover rate of " + str(annual) + ". The turnover rates are at column " + str(column) + ".")
                dom = lxml.html.fromstring(source[annual])
                table = dom.cssselect("table")[0]
                rows = table.cssselect("tr") # List
                print("Still parsing...")
                for row in rows[3:]: # 一次處理表格的一列，並過濾掉表格前三行標題列。
                    row_data = [] # 暫存用，每跑完一列清除。
                    cells = row.cssselect("td")
                    for cell in cells: # 抓每一格的內容存到row_data -> dicts
                        cell_value = cell.text_content()
                        row_data.append(cell_value)
                    if cells[1].text_content() in dicts: # 檢查id是否已經有資料，有update，沒有就新增。資料列從row_data取出id和每年度turnover_rate存到dicts。
                        dicts[cells[1].text_content()].update({"id": cells[1].text_content(), 
                                                               "turnover_rate_" + str(annual): float(row_data[column][0:-1]) / 100})
                    else:
                        dicts[cells[1].text_content()] = {"id": cells[1].text_content(), 
                                                          "turnover_rate_" + str(annual): float(row_data[column][0:-1]) / 100}
            return dicts

        def filte(raw_data):
            '''
            拿現有profile_data的id比對原始資料，比對不到的刪除之。
            並作格式轉換
            '''
            filtered_data = []
            profile_id_list = []
            for row in profile_data: # 從profile_data建立要保留的profile_id_list
                profile_id_list += [row["id"]]            
            for row_key in raw_data: # 以profile_id_list為準比對row_key，合者存至filtered_data。
                for profile_id in profile_id_list: # profile_id有的有是97977870A或97977870B，而row_key結尾有些有去掉A、B，故要用in來逐條比對不用==比對。
                    if row_key in profile_id:
                        filtered_data += [raw_data[row_key]]
            return filtered_data

        raw_data = data()
        filtered_data = filte(raw_data)
        return filtered_data

    def rate_of_return(source):
        def convert_to_float(string):
            try:
                return float(string) / 100
            except ValueError:
                return

        rate_of_return_dict = {}
        dom = lxml.html.fromstring(source)
        table = dom.get_element_by_id("ctl00_ContentPlaceHolder1_GridView1")
        rows = table.cssselect("tr")
        for row in rows[2:]: # 過濾掉表格標題列
            cells = row.cssselect("td")
            rate_of_return_dict[cells[4].text_content()] = {"id": cells[4].text_content(),
                                                            2002: convert_to_float(cells[6].text_content()),
                                                            2003: convert_to_float(cells[7].text_content()),
                                                            2004: convert_to_float(cells[8].text_content()),
                                                            2005: convert_to_float(cells[9].text_content()),
                                                            2006: convert_to_float(cells[10].text_content()),
                                                            2007: convert_to_float(cells[11].text_content()),
                                                            2008: convert_to_float(cells[12].text_content()),
                                                            2009: convert_to_float(cells[13].text_content()),
                                                            2010: convert_to_float(cells[14].text_content()),
                                                            2011: convert_to_float(cells[15].text_content())}
        for fund_id in rate_of_return_dict:
            print(rate_of_return_dict[fund_id])
            for key in rate_of_return_dict[fund_id].keys():
                if rate_of_return_dict[fund_id][key] == None:
                    del rate_of_return_dict[fund_id][key]

        print(rate_of_return_dict)
        return rate_of_return_dict

    print("Parsing ", end="")
    if source == profile_html:
        print("profile.")
        return profile()
    elif source == turnover_rate_html:
        print("turnover rate...")
        return turnover_rate()
    elif source == rate_of_return_html:
        print("rate of return...")
        return rate_of_return(source)

def save_data(profile_data, turnover_rate_data):
    '''
    把profile_data和turnover_rate_data合併，並刪除不要的欄位，最後存到DB內。
    '''
    def couple():
        coupled_data = profile_data[:]
        for turnover_rate_item in turnover_rate_data:
            for coupled_item in coupled_data:
                if turnover_rate_item["id"] in coupled_item["id"]:
                    turnover_rate_item_without_id = turnover_rate_item.copy()
                    del turnover_rate_item_without_id["id"]
                    coupled_item.update(turnover_rate_item_without_id)
        return coupled_data

    def del_inception_year_data(list_of_dicts):
        '''
        刪掉每筆基金成立年的週轉率資料，注意週轉率資料最早只到2001年，有些基金早於2001年成立。
        用str型態再用in去比較比較好處理
        '''
        for dict_item in list_of_dicts:
            inception_year = str(dict_item["inception_date"].year)
            for key in dict_item.keys():
                if inception_year in key:
                    del dict_item[key]
        return list_of_dicts

    def add_turnover_rate_average(list_of_dicts):
        for dict_item in list_of_dicts:
            denominator = 0
            numerator = 0
            for key in dict_item:
                if "turnover_rate_" in key:
                    denominator += 1
                    numerator += dict_item[key]
            dict_item["turnover_rate_average"] = numerator / denominator
        return list_of_dicts

    coupled_data = couple()
    coupled_data = del_inception_year_data(coupled_data)
    coupled_data = add_turnover_rate_average(coupled_data)
    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS swdata") # 先把既有的swdata表格刪除，避免舊資料遺留。沒刪除的話已合併或消滅的遺體可能會存在。
    scraperwiki.sqlite.save(unique_keys=["id"], data=coupled_data)
    return print("Data saved.")

fund_dict = {}

profile_html = scrape("profile")
profile_data = parse(profile_html)
for fund_item in profile_data:
    fund = Fund(fund_item["fund_type"], fund_item["id"], fund_item["isin"], fund_item["name"], fund_item["inception_date"])
    fund_dict[fund_item["id"]] = fund

turnover_rate_html = scrape("turnover_rate")
turnover_rate_data = parse(turnover_rate_html)
for fund_item in turnover_rate_data:
    for key in fund_item:
        if "turnover_rate_" in key:
            annual = int(key[14:])
            try:
                fund_dict[fund_item["id"]].add_turnover_rate(annual, fund_item[key])
            except KeyError:
                fund_dict[fund_item["id"]+"A"].add_turnover_rate(annual, fund_item[key])
                fund_dict[fund_item["id"]+"B"].add_turnover_rate(annual, fund_item[key])
                
print(fund_dict["48862809"].turnover_rates, fund_dict["48862809"].average_turnover_rate(), fund_dict['48862809'].inception_date)

rate_of_return_html = scrape("rate_of_return")
rate_of_return_data = parse(rate_of_return_html)

#save_data(profile_data, turnover_rate_data)
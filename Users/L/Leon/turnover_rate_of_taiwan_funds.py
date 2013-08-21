#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from __future__ import print_function
import sys
import scraperwiki
import gviz_api # http://developers.google.com/chart/interactive/docs/dev/gviz_api_lib

reload(sys)
sys.setdefaultencoding('utf-8')

page_template = """
<html>
  <title>台灣境內基金平均費用比率</title>
  <script src="https://www.google.com/jsapi" type="text/javascript"></script>
  <script>
    google.load('visualization', '1', {packages:['table']});
    google.setOnLoadCallback(drawTable);
    function drawTable() {
      var json_table = new google.visualization.Table(document.getElementById('table_div_json'));
      var json_data = new google.visualization.DataTable(%(json)s, 0.6);
      var formatter = new google.visualization.NumberFormat({suffix: '%%', fractionDigits: 3});
      formatter.format(json_data, 3);
      json_table.draw(json_data, {showRowNumber: true, allowHtml: true});
    }
  </script>
  <body>
    <H1>台灣境內基金平均費用比率</H1>
    <p>不含該筆基金成立年與今年，因此兩年度資料皆不足整年。</p>
    <p><a href='http://www.sitca.org.tw/OPF/D0000/D2100/D2110/類型代號說明.xls'>類型代號說明</a></p>
    <p>資料來源：<a href='http://www.sitca.org.tw/'>中華民國證券投資信託暨商業同業公會</a></p>
    <div id="table_div_json"></div>
  </body>
</html>
"""
sourcescraper = 'test_htmlparser'
scraperwiki.sqlite.attach(sourcescraper, "src") # Connecting to the source database giving it the name src
sdata = scraperwiki.sqlite.select("* FROM src.swdata") # 這是一個List
schema = [("類型代號"), ("基金統編"), ("基金名稱"), ("平均費用比率", "number")] # 加基金統編方便查詢
data = [[fund.get("fund_type"), fund.get("id"), fund.get("name"), fund.get("turnover_rate_average")*100] for fund in sdata]
data_table = gviz_api.DataTable(schema, data)
json = data_table.ToJSon(columns_order=("類型代號", "基金統編", "基金名稱", "平均費用比率"), order_by="平均費用比率")
print page_template % vars()

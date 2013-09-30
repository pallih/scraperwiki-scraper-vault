import sys, os
import string

import mechanize

import scraperwiki


# Do all pages
try:
    record_start_id_list = scraperwiki.sqlite.select("max(record_id) from lobbyists")

    if (record_start_id_list):
        record_start_id = int(record_start_id_list[0]["max(record_id)"]) + 1
except:
    record_start_id = 1

record_counter = record_start_id

lobbyist_type_list = ["BNK"]

#lobbyist_type_list = ["BNK","COM","EDU","ENV","HMH","INS","LBR","LAW","MNF","MRK","UTL","PUB","RAC","EST","GOV","TRD","TRN","TRV"]
column_name_list = ["LR_ID","LR_Year","YEAR","LOBBYISTNAME","CLIENTNAME","BUSINESS_NATURE","LOBBYING_TYPE","3P_NAME","CLIENT_CITY","LOBBYIST_CITY","3P_CITY","CLIENT_STATE","LOBBYIST_STATE","3P_STATE","TOTAL_EXP","TOTAL_COMP","LR_QueueCode","Lobbying_LOGov","LOBBYIST_ZIP"]

submiturl = "https://apps.jcope.ny.gov/lrr/Administration/LB_QReports.aspx?x=EAOuuh%2b5RxH4ZfC9He6E1kkIf340gkvKCYQW5GCh4jbkh9mx2t26szoPCniItxKv6e1i7bJN0dMg0%2fQ2wHxMPHF85Pja%2fzPXI%2bylmxwrDAI0mHb1d%2fj04q%2ffKHdIXsfk6NDG2bf76yiWEWd6HTOpnYtUFzTrmNruTF9Nosi0GfyF"

params_dict = {}

# Fetch the page
for each_type in lobbyist_type_list:
    br = mechanize.Browser()
    br.add_header = [("User-agent", "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1")]
    br.select_form(nr=0)
    br.form["ddlQBNature"] = each_type

    response = br.submit()
    html = response.read()

    page = br.open( self.loginurl )

    html = "".join([line.strip() for line in html.split("\n")])

    # Find the data grid data in the string
    data_index_start = string.find(html, "DisplayGrid.Data = [[") + 1
    data_index_end = string.find(html, "]];")
    record_text = html[data_index_start:data_index_end]

    record_list = record_text.split("],[")

#  [ [23954,2011,'2011-2012','ACE GROUP - NORTH AMERICA','ACE GROUP- NORTH AMERICA','INS','B','','PHILADELPHIA','PHILADELPHIA','','PA','PA','PA',0,2933,'APR','S','19106',],[25338,2011,'2011-2012','ADOLF, JAY','PHYSICIANS RECIPROCAL INSURERS','INS','N','','ROSLYN','NEW YORK ','','NY','NY','NY',0,10000,'APR','S','10007',],[6625,2005,'2005-2006','AFFINITY HEALTH PLAN','AFFINITY HEALTH PLAN','INS','N','','BRONX','BRONX','','NY','NY','NY',13202,5781,'APR','S','10461',]

    for each_record in record_list:
        print each_record
#            lobbyist_dict = {}
#            column_value_list = each_record.split(",")

#            for each_column in column_name_list:
#                lobbyist_dict[each_column] = column_value.string
# 
#            scraperwiki.sqlite.save(unique_keys=[u"record_id"], table_name="lobbyists", data=lobbyist_dict)
#
#            record_counter += 1

import sys, os
import string

import mechanize

import scraperwiki


# Do all pages
try:
    record_start_id_list = scraperwiki.sqlite.select("max(record_id) from lobbyists")

    if (record_start_id_list):
        record_start_id = int(record_start_id_list[0]["max(record_id)"]) + 1
except:
    record_start_id = 1

record_counter = record_start_id

lobbyist_type_list = ["BNK"]

#lobbyist_type_list = ["BNK","COM","EDU","ENV","HMH","INS","LBR","LAW","MNF","MRK","UTL","PUB","RAC","EST","GOV","TRD","TRN","TRV"]
column_name_list = ["LR_ID","LR_Year","YEAR","LOBBYISTNAME","CLIENTNAME","BUSINESS_NATURE","LOBBYING_TYPE","3P_NAME","CLIENT_CITY","LOBBYIST_CITY","3P_CITY","CLIENT_STATE","LOBBYIST_STATE","3P_STATE","TOTAL_EXP","TOTAL_COMP","LR_QueueCode","Lobbying_LOGov","LOBBYIST_ZIP"]

submiturl = "https://apps.jcope.ny.gov/lrr/Administration/LB_QReports.aspx?x=EAOuuh%2b5RxH4ZfC9He6E1kkIf340gkvKCYQW5GCh4jbkh9mx2t26szoPCniItxKv6e1i7bJN0dMg0%2fQ2wHxMPHF85Pja%2fzPXI%2bylmxwrDAI0mHb1d%2fj04q%2ffKHdIXsfk6NDG2bf76yiWEWd6HTOpnYtUFzTrmNruTF9Nosi0GfyF"

params_dict = {}

# Fetch the page
for each_type in lobbyist_type_list:
    br = mechanize.Browser()
    br.add_header = [("User-agent", "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1")]
    br.select_form(nr=0)
    br.form["ddlQBNature"] = each_type

    response = br.submit()
    html = response.read()

    page = br.open( self.loginurl )

    html = "".join([line.strip() for line in html.split("\n")])

    # Find the data grid data in the string
    data_index_start = string.find(html, "DisplayGrid.Data = [[") + 1
    data_index_end = string.find(html, "]];")
    record_text = html[data_index_start:data_index_end]

    record_list = record_text.split("],[")

#  [ [23954,2011,'2011-2012','ACE GROUP - NORTH AMERICA','ACE GROUP- NORTH AMERICA','INS','B','','PHILADELPHIA','PHILADELPHIA','','PA','PA','PA',0,2933,'APR','S','19106',],[25338,2011,'2011-2012','ADOLF, JAY','PHYSICIANS RECIPROCAL INSURERS','INS','N','','ROSLYN','NEW YORK ','','NY','NY','NY',0,10000,'APR','S','10007',],[6625,2005,'2005-2006','AFFINITY HEALTH PLAN','AFFINITY HEALTH PLAN','INS','N','','BRONX','BRONX','','NY','NY','NY',13202,5781,'APR','S','10461',]

    for each_record in record_list:
        print each_record
#            lobbyist_dict = {}
#            column_value_list = each_record.split(",")

#            for each_column in column_name_list:
#                lobbyist_dict[each_column] = column_value.string
# 
#            scraperwiki.sqlite.save(unique_keys=[u"record_id"], table_name="lobbyists", data=lobbyist_dict)
#
#            record_counter += 1


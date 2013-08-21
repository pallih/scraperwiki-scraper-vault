from scraperwiki import scrape
from scraperwiki.sqlite import save,get_var
from urllib2 import urlopen
from lxml.html import fromstring
from datetime import *

part1 = 'http://wwe1.osc.state.ny.us/transparency/contracts/contractresults.cfm?PageNum_rsContract='
part2 = '&sb=a&searchBy=&a=Z0000&au=0&ac=&v=%28Enter+Vendor+Name%29&vo=B&cn=&c=-1&m1=0&y1=0&m2=0&y2=0&am=0&b=Search&entitytype=Agency&order=PAYEE_NAME&sort=ASC'

start_page=get_var('start_page')
if start_page==None:
    start_page=1

urlstrings = [ part1 + str(i) +part2 for i in range(start_page,992)]
headers = [
  'Vendor','Agency','Contract_Number','Current_Contract_Amount',
  'Spending_to_Date','Contract_Start_Date','Contract_End_Date',
  'Contract_Description','Contract_Type', 'Contract_Approval_Date'
]

for urlstring in urlstrings:
    page_data=scrape(urlstring)
    page_data=fromstring(page_data).cssselect('#tableData tr')
    dict_rows=[]
    for row in page_data:
        dict_row=dict(zip(headers, [cell.text_content().strip()  for cell in row.cssselect('td') if cell.text_content().strip() != None]))
        dict_row['url']=urlstring
        if dict_row:
            try:
                dict_row['Current_Contract_Amount']=float(dict_row.get('Current_Contract_Amount','').replace('$', '').replace(',', '').replace('(', '-').replace(')', ''))
                dict_row['Spending_to_Date']=float(dict_row.get('Spending_to_Date','').replace('$', '').replace(',', '').replace('(', '-').replace(')', ''))
                dict_row['Contract_Start_Date']=datetime.strptime( dict_row.get('Contract_Start_Date'), '%m/%d/%Y' )
                dict_row['Contract_End_Date']=datetime.strptime( dict_row.get('Contract_End_Date'), '%m/%d/%Y' )
                dict_row['Contract_Approval_Date']=datetime.strptime( dict_row.get('Contract_Approval_Date'), '%m/%d/%Y' )
            except Exception as e:
                print dict_row, e
            else:
                dict_rows.append(dict_row)
    save([], dict_rows)

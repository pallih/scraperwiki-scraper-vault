import sys
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
import urllib2
import lxml.html as HTML
import re
import chardet
import time
import sqlite3

sqldb = "taiwan_stock.sqlite"

last_month = date.today()+relativedelta(months = -1)
dt_str = str(last_month.year)+'-'+'%02d' % last_month.month+'-01' ## YYYY-MM-01
    

def get_stk_list(market_type):
    """
    fetch stock list from 2 month ago revenue report
    market_type = ('sii','otc')
    """
    two_month_ago = date.today()+relativedelta(months = -2)
    yr = two_month_ago.year-1911
    mon = two_month_ago.month

    url = 'http://mops.twse.com.tw/t21/'+market_type+'/t21sc03_'+str(yr)+'_'+str(mon)+'.html'
    print u'建立股票清單 ... '+ url
    req = urllib2.Request(url)
    the_page = urllib2.urlopen(req).read()
    doc = the_page.decode('big5', 'ignore')
    root = HTML.document_fromstring(doc)
    stocks_list = list(set(root.xpath('//body/center/table[@width="100%"]/tr[2]/td/table/tr[not(./th)]/td[1]/text()')))
    return stocks_list

def revenue_todo_lst(stklist):
    '''
    check sqldb if any revenue record already update
    the return the stock list that need to update.
    '''
    conn1 = sqlite3.connect(sqldb)
    c1 = conn1.cursor()
    c1.execute('SELECT stkid FROM revenue where yyyymm=? AND revenue_idv <> "" ORDER BY stkid', (dt_str,))
    stkdone = c1.fetchall()
    c1.close()
    conn1.close()
    return list(set(stklist)-set(list(x[0] for x in stkdone)))

sii_stocks = get_stk_list('sii')
otc_stocks = get_stk_list('otc')
sii_stocks.sort()
otc_stocks.sort()
undolist = revenue_todo_lst(sii_stocks+otc_stocks)
print u'上市櫃共計 '+str(len(sii_stocks+otc_stocks))+u' 擋, 母公司營收需更新的有 '+str(len(undolist))+u' 擋'
print undolist


from urllib2 import Request, urlopen, URLError, HTTPError
rows = []
for stk in undolist:
    #revenue_url = u'http://dj.mybank.com.tw/z/zc/zch/zchb_'+stk+'.djhtm' ## 合併營收
    revenue_url = u'http://dj.mybank.com.tw/z/zc/zch/zch_'+stk+'.djhtm' ## 母公司營收
    try:
        response = urlopen(revenue_url)
    except HTTPError, e:
        print 'The server couldn\'t fulfill the request.'
        print stk,'-- Error code: ', e.code
    except URLError, e:
        print 'We failed to reach a server.'
        print stk,'-- Reason: ', e.reason
    else:
        print revenue_url
        the_page = response.read()
        doc = the_page.decode('big5', 'ignore')
        root = HTML.document_fromstring(doc)
        table = root.xpath('//table[@id="oMainTable"]')[0]
        for row in table.xpath('.//tr[position()=5]'):
            colList = []
            cells = row.xpath('.//th') + row.xpath('.//td')
            for cell in cells:
                # The individual cell's content
                content = cell.text_content().encode("utf8")
                if content == "":
                    content = 'NA'
                colList.append(content)
            dt = datetime.strptime(str(int(re.sub(r'/','',colList[0]))+191100),'%Y%m').strftime("%Y-%m-%d")
            revenue_merged = re.sub(r',','',colList[1])
            rows.append((dt, stk, revenue_merged))
        time.sleep(1)

newrows=[]
for i in rows:
    if i[0] == dt_str and i[2] != 'NA':
        newrows.append((i[0],i[1],i[2]))

conn2 = sqlite3.connect(sqldb)
c2 = conn2.cursor()
for item in rows:
    c2.execute('update revenue set revenue_mrg=? where yyyymm=? and stkid=?', [item[2], item[0], item[1]])
conn2.commit()
c2.close()
conn2.close()import sys
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
import urllib2
import lxml.html as HTML
import re
import chardet
import time
import sqlite3

sqldb = "taiwan_stock.sqlite"

last_month = date.today()+relativedelta(months = -1)
dt_str = str(last_month.year)+'-'+'%02d' % last_month.month+'-01' ## YYYY-MM-01
    

def get_stk_list(market_type):
    """
    fetch stock list from 2 month ago revenue report
    market_type = ('sii','otc')
    """
    two_month_ago = date.today()+relativedelta(months = -2)
    yr = two_month_ago.year-1911
    mon = two_month_ago.month

    url = 'http://mops.twse.com.tw/t21/'+market_type+'/t21sc03_'+str(yr)+'_'+str(mon)+'.html'
    print u'建立股票清單 ... '+ url
    req = urllib2.Request(url)
    the_page = urllib2.urlopen(req).read()
    doc = the_page.decode('big5', 'ignore')
    root = HTML.document_fromstring(doc)
    stocks_list = list(set(root.xpath('//body/center/table[@width="100%"]/tr[2]/td/table/tr[not(./th)]/td[1]/text()')))
    return stocks_list

def revenue_todo_lst(stklist):
    '''
    check sqldb if any revenue record already update
    the return the stock list that need to update.
    '''
    conn1 = sqlite3.connect(sqldb)
    c1 = conn1.cursor()
    c1.execute('SELECT stkid FROM revenue where yyyymm=? AND revenue_idv <> "" ORDER BY stkid', (dt_str,))
    stkdone = c1.fetchall()
    c1.close()
    conn1.close()
    return list(set(stklist)-set(list(x[0] for x in stkdone)))

sii_stocks = get_stk_list('sii')
otc_stocks = get_stk_list('otc')
sii_stocks.sort()
otc_stocks.sort()
undolist = revenue_todo_lst(sii_stocks+otc_stocks)
print u'上市櫃共計 '+str(len(sii_stocks+otc_stocks))+u' 擋, 母公司營收需更新的有 '+str(len(undolist))+u' 擋'
print undolist


from urllib2 import Request, urlopen, URLError, HTTPError
rows = []
for stk in undolist:
    #revenue_url = u'http://dj.mybank.com.tw/z/zc/zch/zchb_'+stk+'.djhtm' ## 合併營收
    revenue_url = u'http://dj.mybank.com.tw/z/zc/zch/zch_'+stk+'.djhtm' ## 母公司營收
    try:
        response = urlopen(revenue_url)
    except HTTPError, e:
        print 'The server couldn\'t fulfill the request.'
        print stk,'-- Error code: ', e.code
    except URLError, e:
        print 'We failed to reach a server.'
        print stk,'-- Reason: ', e.reason
    else:
        print revenue_url
        the_page = response.read()
        doc = the_page.decode('big5', 'ignore')
        root = HTML.document_fromstring(doc)
        table = root.xpath('//table[@id="oMainTable"]')[0]
        for row in table.xpath('.//tr[position()=5]'):
            colList = []
            cells = row.xpath('.//th') + row.xpath('.//td')
            for cell in cells:
                # The individual cell's content
                content = cell.text_content().encode("utf8")
                if content == "":
                    content = 'NA'
                colList.append(content)
            dt = datetime.strptime(str(int(re.sub(r'/','',colList[0]))+191100),'%Y%m').strftime("%Y-%m-%d")
            revenue_merged = re.sub(r',','',colList[1])
            rows.append((dt, stk, revenue_merged))
        time.sleep(1)

newrows=[]
for i in rows:
    if i[0] == dt_str and i[2] != 'NA':
        newrows.append((i[0],i[1],i[2]))

conn2 = sqlite3.connect(sqldb)
c2 = conn2.cursor()
for item in rows:
    c2.execute('update revenue set revenue_mrg=? where yyyymm=? and stkid=?', [item[2], item[0], item[1]])
conn2.commit()
c2.close()
conn2.close()
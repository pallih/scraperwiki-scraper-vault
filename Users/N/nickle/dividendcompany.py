import scraperwiki
from datetime import date
import calendar
from lxml.html import fromstring
from lxml.etree import tostring
utils = scraperwiki.utils.swimport('dividendutils')

# Blank Python

mappings = \
    {
    'AAL':r'http://www.angloamerican.com/investors/divinfo/history',
    'ABF':r'http://www.abf.co.uk/Dividend%20history.aspx',
    'ADM':r'http://www.admiralgroup.co.uk/investor/dividend_history.php',
    'ADN':None,
    'AGK':r'http://ir.aggreko.com/agk_ir/shser/divinfo/',
    'AMEC':r'http://www.amec.com/investors/shareholderinformation/dividends/dividend-history-table.htm',
    'ANTO':r'http://www.antofagasta.co.uk/interior/investor/dividend.php',
    'ARM':r'http://ir.arm.com/phoenix.zhtml?c=197211&p=irol-dividends',
    'ASHM':None,
    'AV':r'http://www.aviva.com/investor-relations/shareholder-services/ordinary-shareholders/aviva-plc-dividends/',
    'AZN':None,
    'BA':r'http://bae-systems-investor-relations.production.investis.com/shareholder-information/dividend-information.aspx',
    'BARC':r'http://group.barclays.com/Investor-Relations/Shareholder-information/Dividends',
    #'BATS':r"http://www.bat.com/servlet/SPMerge?mainurl=%2Fgroup%2Fsites%2Fuk__3mnfen%2Ensf%2FvwPagesWebLive%2FDO538FK6",
    'BP':r"http://www.bp.com/extendedsectiongenericarticle.do?categoryId=9038614&contentId=7070557",
    'BATS':None,
    'BG':r'http://www.bg-group.com/InvestorRelations/ShareholderServices/Pages/DividendHistory.aspx',
    'BLND':r'http://www.britishland.com/index.asp?pageid=255',
    'BLT':None,
    #'BSY':r"http://corporate.sky.com/documents/pdf/shareholder_info/dividend_history_12_11_10", PDF!
    'BT.A':r'http://www.btplc.com/Sharesandperformance/Dividends/Datesandpayments/Datesandpayments.htm',
    'CCL':r'http://phx.corporate-ir.net/phoenix.zhtml?c=140690&p=irol-dividends',
    'CNA':r'http://www.centrica.com/index.asp?pageid=251',
    'CPG':r"http://www.compass-group.com/806.htm",
    #'CPI':r"http://www.capita.co.uk/investors/pages/dividends.aspx",
    'CRDA':r"http://www.croda.com/home.aspx?s=1&r=233&p=1121",
    #'CRH':r"http://www.crh.com/investors/equity-investors/dividends",
    'CSCG':r"http://www.capital-shopping-centres.co.uk/investors/shareholder_info/dividends/",

    'DGE':r'http://www.diageo.com/en-sc/investor/shareholderservices/ordinaryshares/Pages/Dividend-Information.aspx',
    'EMG':r"http://www.mangroupplc.com/investor-relations/shareholder-information/dividends.jsf",
    'DLAR':r'http://investors.delarue.com/dlr/services/prevdiv/',
    'GKN':r'http://www.gkn.com/investorrelations/shareholderservices/Pages/dividends.aspx',
    'GSK':r'http://www.gsk.com/investors/dividend-calculator.htm',
    'IAP':r'http://www.icap.com/investor-relations/shareholder-information/dividend-information/icap-dividend-history.aspx',
    'IMT':r'http://www.imperial-tobacco.com/index.asp?page=62',
    'ISF':None,
    'LLOY':r'http://www.lloydsbankinggroup.com/investors/shareholder_information/uk_dividend_history_hbos.asp',
    'MKS':r'http://corporate.marksandspencer.com/investors/shareholder/yourdividends/dividends_history',
    'NG':None,
    'PHGP':None,
    'PSON':None,
    'RB':r'http://www.rb.com/Media-investors/Shareholder-information/Dividend-information',
    'RBS':r'http://www.investors.rbs.com/dividends',
    'RDSA':r'http://www.shell.com/home/content/investor/dividend_information/historical_payments/2006/',
    'SBRY':r'http://www.j-sainsbury.co.uk/investor-centre/shareholder-centre/dividends/',
    'SL':r'http://www.standardlife.com/shareholders/dividends.html',
    'SSE':r'http://www.sse.com/Investors/Dividend/History/',
    'SVT':r'http://www.severntrent.com/category/37',
    'TATE':r'http://www.tateandlyle.com/InvestorRelations/shareinformation/dividendinformation/Pages/DividendCalculatorandHistory.aspx',
    'TNI':r'http://www.trinitymirror.com/investors/shareholder-information/dividend-policy-history/',
    'TT':None,
    'UU':r'http://www.unitedutilities.com/Dividends.aspx',
    'VOD':r'http://www.vodafone.com/content/index/investors/share_debt/ordinary_shareholders/dividends.html',
    'WMH':r'http://www.williamhillplc.com/wmh/investors/shareholder_services/dividends/payment_history/'
    }

def read_table (table):
    res = [[],[]]
    #print tostring (table, pretty_print=True)
    for header in table.xpath ("thead"):
        for th in header.xpath("tr/th"):
            txt = tostring (th, method="text", encoding="utf-8")
            txt = txt.strip()
            txt = txt.replace ('\xc2', '')
            txt = txt.replace ('\xa0', '')
            res[0].append (txt)
    for row in table.xpath ("tbody/tr|tr"):
        res[1].append ([])
        for td in row.xpath("td"):
            txt = tostring (td, method="text", encoding="utf-8")
            txt = txt.strip()
            txt = txt.replace ('\xc2', '')
            txt = txt.replace ('\xa0', '')
            res[1][-1].append (txt)
    return res

def read (url):
    try:
        html = scraperwiki.scrape (url)
    except:
        print 'Cannot find url %s' % url
        return []
    html = html.replace(r"<br />", " ")
    root = fromstring (html)
    try:
        tables = root.xpath ('//table')
    except:
        print 'No no tables in html for url %s'  % url
    res = []
    for table in tables:
        res.append (read_table (table))
    return res

def BLND(t):
    res = []
    for i in range (0,3):
        for r in t[i][1]:
            if len (r) == 7:
                res.append ({'Type':r[0], 'Amount':r[6], 'Payment':r[2], 'Record':'', 'Currency':'GBP'})
    return res

def BT_A(t):
    res = []
    for i in range (0,1):
        for r in t[i][1]:
            if r[2] == 'Nil':
                continue
            if len(r) == 5:     
                res.append ({'Type':r[1], 'Record':r[3], 'Payment':r[4], 'Currency':'GBP', 'Amount':r[2]})
            if len(r) == 4:     
                res.append ({'Type':r[1], 'Payment':r[3], 'Currency':'GBP', 'Amount':r[2]})
    return res

def CCL(t):
    res = []
    for r in t[5][1]:
        res.append ({'Type':r[1], 'Amount':r[2], 'Payment':r[3], 'Record':r[4], 'Currency':'GBP'})
    return res

def DLAR(t):
    res = []
    for r in t[0][1]:
        if len (r) == 4:
            res.append ({'Type':r[3], 'Amount':r[2][:-1], 'Payment':r[1], 'Record':'', 'Currency':'GBP'})
        elif len (r) == 3:
            res.append ({'Type':r[2], 'Amount':r[1][:-1], 'Payment':r[0], 'Record':'', 'Currency':'GBP'})
    return res

def IAP (t):
    t = read (url)
    for r in t[0][1]:
        if len(r) != 8:
            continue
        res.append ({'Type':r[4], 'Amount':r[2], 'Payment':r[7], 'Record':r[6], 'ExDiv':r[5], 'Currency':'GBP'})
    return res

def IMT(t):
    res = []
    for r in t[0][1]:
        if r[6] == 'N/A':
            amount = r[4]
        else:
            amount = r[6]
        if amount == 'TBA':
            continue
        res.append ({'Announce':r[0], 'ExDiv':r[1], 'Record':r[2], 'Payment':r[3], 'Currency':'GBP', 'Amount':amount})
    return res

def MKS (t):
    res = []
    for r in t[0][1]:
        res.append ({'Type':'', 'Amount':r[3], 'Payment':r[2], 'Record':r[1], 'ExDiv':r[0], 'Currency':'GBP'})
    return res


#scraperwiki.sqlite.save (unique_keys=["Source", "Ticker", "ExDivDate", "Type"], data=alldata)

def validate (data):
    if 'ExDiv' in data and 'Record' in data:
        if data['ExDiv'] != None and data['Record'] != None:
            if data['ExDiv'] > data['Record']:
                print "ExDiv after Record"
    if 'ExDiv' in data and 'Payment' in data:
        if data['ExDiv'] != None and data['Payment'] != None:
            if data['ExDiv'] > data['Payment']:
                print "ExDiv after Payment"

def dump (ticker):
    nticker = ticker.replace (".", "_")
    url = mappings [ticker]
    t = read (url)
    for row in eval ("%s(t)" % nticker):
        data = {}
        for k, v in row.items():
            #print k,v
            try:
                if k == 'Type':
                    data [k] = utils.convert_type (v)
                if k in ['ExDiv', 'Record', 'Payment', 'Anounce']:
                    data [k] = utils.convert_date (v)
                if k == 'Amount':
                    data [k] = utils.convert_amount (v)
                if k == 'Currency':
                    data [k] = utils.convert_currency (v)
            except:
                print "Bad ", k, "|"+ v + "|"
        print data
        validate (data)


def AAL(t):
    res = []
    for r in t[0][1]:
        if len (r) == 0:
            continue
        currs = r[0].split('\r\n')
        amounts = r[1].split('\r\n')
        res.append ({ 'Record':r[2], 'Payment':r[3], 'Currency':currs[1], 'Amount':amounts[1]})
    return res

def ABF(t):
    res = []
    for r in t[0][1]:
        if len (r) != 4:
            continue
        res.append ({ 'Record':r[1], 'Payment':r[2], 'Currency':'GBP', 'Amount':r[3]})
    return res

def ADM(t):
    res = []
    for r in t[0][1]:
        if r[0] =='Year':
            continue
        res.append ({'Type':r[1], 'ExDiv':r[2], 'Record':r[3], 'Payment':r[4], 'Currency':'GBP', 'Amount':r[5]})
        
    return res

def AGK(t):
    res = []
    for r in t[0][1]:
        if r[2] != '':
            res.append ({'Type':'Interim','ExDiv':r[1],'Currency':'GBP', 'Amount':r[2]})
        if r[4] != '':
            res.append ({'Type':'Final','ExDiv':r[3],'Currency':'GBP', 'Amount':r[4]})
        
    return res

def AMEC(t):
    res = []
    for r in t[0][1]:
        if len(r) != 4:
            continue
        final = r[1][0:10]
        interim = r[1][11:]
        res.append ({'Type':'Final',  'Payment':final,  'Currency':'GBP', 'Amount':r[2].split(" ")[0]})
        res.append ({'Type':'Interim','Payment':interim,'Currency':'GBP', 'Amount':r[2].split(" ")[1]})
    return res

def ANTO(t):
    res = []
    # 5 for future dividends
    for r in t[5][1]:
        if r[0] in ['Next Dividend','']:
            continue
        if r[4] == r'N/A*':
            res.append ({'Type':r[0][:-5],  'Payment':r[1], 'Record':r[2], 'Currency':'USD', 'Amount':r[3]})
        else:
            res.append ({'Type':r[0][:-5],  'Payment':r[1], 'Record':r[2], 'Currency':'GBP', 'Amount':r[4]})
    for r in t[6][1]:
        if r[0] in ['Dividend','']:
            continue
        res.append ({'Type':r[0][:-5],  'Payment':r[1],  'Currency':'GBP', 'Amount':r[3]})
    return res

def ARM(t):
    res = []
    for r in t[1][1]:
        if r[0] == 'Declared':
            continue
        res.append ({'Announce':r[0], 'Record':r[1], 'Payment':r[2], 'Currency':'GBP', 'Amount':r[3], 'Type':r[4]})
    return res

def AV(t):
    res = []
    for r in t[0][1]:
        if len (r) < 5:
            continue
        res.append ({'ExDiv':r[1], 'Record':r[2], 'Payment':r[3], 'Currency':'GBP', 'Amount':r[4][:-1], 'Type':r[0]})
    return res

def BA(t):
    res = []
    for r in t[0][1]:
        res.append ({'Record':r[2], 'Payment':r[1], 'Currency':'GBP', 'Amount':r[4], 'Type':r[3][:-5]})
    return res

def BARC(t):
    res = []
    for r in t[0][1]:
        amount, typ = r[3].split ('p')
        typ = typ.strip()[1:-1]
        res.append ({'ExDiv':r[0], 'Record':r[1], 'Payment':r[2], 'Currency':'GBP', 'Amount':amount, 'Type':typ})
    return res


def BATS(t):
    res = []
    print t
    for i in range (0,10):
        for r in t[i][1]:
            print i, r
    return res

def BP(t):
    res = []
    for r in t[1][1]:
        if len(r) != 13:
            continue
        res.append ({'Anounce':r[3], 'Payment':r[5], 'Currency':'GBP', 'Amount':r[11]})
    return res

def BSY(t):
    print t
    res = []
    for i in range (0,10):
        for r in t[i][1]:
            print i, r
    return res

def CCL(t):
    res = []
    for r in t[6][1]:
        if r[1] == 'Record':
            continue
        res.append ({'Announce':r[2], 'ExDiv':r[0], 'Record':r[1], 'Payment':r[3], 'Currency':'USD', 'Amount':r[4][1:]})
    return res

def CNA(t):
    res = []
    for r in t[1][1]:
        res.append ({'Type':r[0].split(" ")[0], 'Announce':r[1], 'ExDiv':r[2], 'Record':r[3], 'Payment':r[4], 'Currency':'GBP', 'Amount':r[5][:-1]})
    return res

def CPG(t):
    res = []
    for r in t[0][1]:
        if r[0][0:5] != "Final":
            continue
        parts = r[0].split(' ')
        if parts[1] <= '2000':
            continue
        pfinal   = r[1].split("\n")[0]
        pinterim = r[1].split("\n")[1]
        afinal   = r[2].split("\n")[0]
        ainterim = r[2].split("\n")[1]
        res.append ({'Type':'Final',   'Payment':pfinal,   'Currency':'GBP', 'Amount':afinal  })
        res.append ({'Type':'Interim', 'Payment':pinterim, 'Currency':'GBP', 'Amount':ainterim})
    return res

def CPI(t):
    res = []
    for r in t[0][1]:
        print r
    return res

def CRDA(t):
    res = []
    for r in t[2][1]:
        if len(r) != 5:
            continue
        res.append ({'Type':r[0], 'Record':r[3], 'Payment':r[4], 'Currency':'GBP', 'Amount':r[1]})
    return res

def CSCG(t):
    res = []
    for r in t[0][1]:
        if len (r) != 8:
            continue
        if not r[2] in ['final', 'Interim']:
            continue
        #print r
        res.append ({'Type':r[2], 'Record':r[6][0:8], 'Payment':r[7][0:8], 'Currency':'GBP', 'Amount':r[3]})
    return res

def DGE(t):
    res = []
    for r in t[1][1]:
        if len(r) != 4:
            continue
        ipayment = r[3][0:8]
        fpayment = r[3][8:]
        iamount  = r[2].split('p')[0]
        famount  = r[2].split('p')[1]
        res.append ({'Type':'Interim', 'Payment':ipayment, 'Currency':'GBP', 'Amount':iamount})
        res.append ({'Type':'Final',   'Payment':fpayment, 'Currency':'GBP', 'Amount':famount})
    return res

def template(t):
    res = []
    for i in range (0,10):
        for r in t[i][1]:
            print i, r
    return res


def EMG(t):
    res = []
    for r in t[3][1]:
        if len (r) != 8:
            continue
        print  r
        res.append ({'Payment':r[1],   'ExDiv':r[3], 'Currency':'GBP', 'Amount':r[2]})
    return res

    
    return res


dump ('EMG')




import scraperwiki
from datetime import date
import calendar
from lxml.html import fromstring
from lxml.etree import tostring
utils = scraperwiki.utils.swimport('dividendutils')

# Blank Python

mappings = \
    {
    'AAL':r'http://www.angloamerican.com/investors/divinfo/history',
    'ABF':r'http://www.abf.co.uk/Dividend%20history.aspx',
    'ADM':r'http://www.admiralgroup.co.uk/investor/dividend_history.php',
    'ADN':None,
    'AGK':r'http://ir.aggreko.com/agk_ir/shser/divinfo/',
    'AMEC':r'http://www.amec.com/investors/shareholderinformation/dividends/dividend-history-table.htm',
    'ANTO':r'http://www.antofagasta.co.uk/interior/investor/dividend.php',
    'ARM':r'http://ir.arm.com/phoenix.zhtml?c=197211&p=irol-dividends',
    'ASHM':None,
    'AV':r'http://www.aviva.com/investor-relations/shareholder-services/ordinary-shareholders/aviva-plc-dividends/',
    'AZN':None,
    'BA':r'http://bae-systems-investor-relations.production.investis.com/shareholder-information/dividend-information.aspx',
    'BARC':r'http://group.barclays.com/Investor-Relations/Shareholder-information/Dividends',
    #'BATS':r"http://www.bat.com/servlet/SPMerge?mainurl=%2Fgroup%2Fsites%2Fuk__3mnfen%2Ensf%2FvwPagesWebLive%2FDO538FK6",
    'BP':r"http://www.bp.com/extendedsectiongenericarticle.do?categoryId=9038614&contentId=7070557",
    'BATS':None,
    'BG':r'http://www.bg-group.com/InvestorRelations/ShareholderServices/Pages/DividendHistory.aspx',
    'BLND':r'http://www.britishland.com/index.asp?pageid=255',
    'BLT':None,
    #'BSY':r"http://corporate.sky.com/documents/pdf/shareholder_info/dividend_history_12_11_10", PDF!
    'BT.A':r'http://www.btplc.com/Sharesandperformance/Dividends/Datesandpayments/Datesandpayments.htm',
    'CCL':r'http://phx.corporate-ir.net/phoenix.zhtml?c=140690&p=irol-dividends',
    'CNA':r'http://www.centrica.com/index.asp?pageid=251',
    'CPG':r"http://www.compass-group.com/806.htm",
    #'CPI':r"http://www.capita.co.uk/investors/pages/dividends.aspx",
    'CRDA':r"http://www.croda.com/home.aspx?s=1&r=233&p=1121",
    #'CRH':r"http://www.crh.com/investors/equity-investors/dividends",
    'CSCG':r"http://www.capital-shopping-centres.co.uk/investors/shareholder_info/dividends/",

    'DGE':r'http://www.diageo.com/en-sc/investor/shareholderservices/ordinaryshares/Pages/Dividend-Information.aspx',
    'EMG':r"http://www.mangroupplc.com/investor-relations/shareholder-information/dividends.jsf",
    'DLAR':r'http://investors.delarue.com/dlr/services/prevdiv/',
    'GKN':r'http://www.gkn.com/investorrelations/shareholderservices/Pages/dividends.aspx',
    'GSK':r'http://www.gsk.com/investors/dividend-calculator.htm',
    'IAP':r'http://www.icap.com/investor-relations/shareholder-information/dividend-information/icap-dividend-history.aspx',
    'IMT':r'http://www.imperial-tobacco.com/index.asp?page=62',
    'ISF':None,
    'LLOY':r'http://www.lloydsbankinggroup.com/investors/shareholder_information/uk_dividend_history_hbos.asp',
    'MKS':r'http://corporate.marksandspencer.com/investors/shareholder/yourdividends/dividends_history',
    'NG':None,
    'PHGP':None,
    'PSON':None,
    'RB':r'http://www.rb.com/Media-investors/Shareholder-information/Dividend-information',
    'RBS':r'http://www.investors.rbs.com/dividends',
    'RDSA':r'http://www.shell.com/home/content/investor/dividend_information/historical_payments/2006/',
    'SBRY':r'http://www.j-sainsbury.co.uk/investor-centre/shareholder-centre/dividends/',
    'SL':r'http://www.standardlife.com/shareholders/dividends.html',
    'SSE':r'http://www.sse.com/Investors/Dividend/History/',
    'SVT':r'http://www.severntrent.com/category/37',
    'TATE':r'http://www.tateandlyle.com/InvestorRelations/shareinformation/dividendinformation/Pages/DividendCalculatorandHistory.aspx',
    'TNI':r'http://www.trinitymirror.com/investors/shareholder-information/dividend-policy-history/',
    'TT':None,
    'UU':r'http://www.unitedutilities.com/Dividends.aspx',
    'VOD':r'http://www.vodafone.com/content/index/investors/share_debt/ordinary_shareholders/dividends.html',
    'WMH':r'http://www.williamhillplc.com/wmh/investors/shareholder_services/dividends/payment_history/'
    }

def read_table (table):
    res = [[],[]]
    #print tostring (table, pretty_print=True)
    for header in table.xpath ("thead"):
        for th in header.xpath("tr/th"):
            txt = tostring (th, method="text", encoding="utf-8")
            txt = txt.strip()
            txt = txt.replace ('\xc2', '')
            txt = txt.replace ('\xa0', '')
            res[0].append (txt)
    for row in table.xpath ("tbody/tr|tr"):
        res[1].append ([])
        for td in row.xpath("td"):
            txt = tostring (td, method="text", encoding="utf-8")
            txt = txt.strip()
            txt = txt.replace ('\xc2', '')
            txt = txt.replace ('\xa0', '')
            res[1][-1].append (txt)
    return res

def read (url):
    try:
        html = scraperwiki.scrape (url)
    except:
        print 'Cannot find url %s' % url
        return []
    html = html.replace(r"<br />", " ")
    root = fromstring (html)
    try:
        tables = root.xpath ('//table')
    except:
        print 'No no tables in html for url %s'  % url
    res = []
    for table in tables:
        res.append (read_table (table))
    return res

def BLND(t):
    res = []
    for i in range (0,3):
        for r in t[i][1]:
            if len (r) == 7:
                res.append ({'Type':r[0], 'Amount':r[6], 'Payment':r[2], 'Record':'', 'Currency':'GBP'})
    return res

def BT_A(t):
    res = []
    for i in range (0,1):
        for r in t[i][1]:
            if r[2] == 'Nil':
                continue
            if len(r) == 5:     
                res.append ({'Type':r[1], 'Record':r[3], 'Payment':r[4], 'Currency':'GBP', 'Amount':r[2]})
            if len(r) == 4:     
                res.append ({'Type':r[1], 'Payment':r[3], 'Currency':'GBP', 'Amount':r[2]})
    return res

def CCL(t):
    res = []
    for r in t[5][1]:
        res.append ({'Type':r[1], 'Amount':r[2], 'Payment':r[3], 'Record':r[4], 'Currency':'GBP'})
    return res

def DLAR(t):
    res = []
    for r in t[0][1]:
        if len (r) == 4:
            res.append ({'Type':r[3], 'Amount':r[2][:-1], 'Payment':r[1], 'Record':'', 'Currency':'GBP'})
        elif len (r) == 3:
            res.append ({'Type':r[2], 'Amount':r[1][:-1], 'Payment':r[0], 'Record':'', 'Currency':'GBP'})
    return res

def IAP (t):
    t = read (url)
    for r in t[0][1]:
        if len(r) != 8:
            continue
        res.append ({'Type':r[4], 'Amount':r[2], 'Payment':r[7], 'Record':r[6], 'ExDiv':r[5], 'Currency':'GBP'})
    return res

def IMT(t):
    res = []
    for r in t[0][1]:
        if r[6] == 'N/A':
            amount = r[4]
        else:
            amount = r[6]
        if amount == 'TBA':
            continue
        res.append ({'Announce':r[0], 'ExDiv':r[1], 'Record':r[2], 'Payment':r[3], 'Currency':'GBP', 'Amount':amount})
    return res

def MKS (t):
    res = []
    for r in t[0][1]:
        res.append ({'Type':'', 'Amount':r[3], 'Payment':r[2], 'Record':r[1], 'ExDiv':r[0], 'Currency':'GBP'})
    return res


#scraperwiki.sqlite.save (unique_keys=["Source", "Ticker", "ExDivDate", "Type"], data=alldata)

def validate (data):
    if 'ExDiv' in data and 'Record' in data:
        if data['ExDiv'] != None and data['Record'] != None:
            if data['ExDiv'] > data['Record']:
                print "ExDiv after Record"
    if 'ExDiv' in data and 'Payment' in data:
        if data['ExDiv'] != None and data['Payment'] != None:
            if data['ExDiv'] > data['Payment']:
                print "ExDiv after Payment"

def dump (ticker):
    nticker = ticker.replace (".", "_")
    url = mappings [ticker]
    t = read (url)
    for row in eval ("%s(t)" % nticker):
        data = {}
        for k, v in row.items():
            #print k,v
            try:
                if k == 'Type':
                    data [k] = utils.convert_type (v)
                if k in ['ExDiv', 'Record', 'Payment', 'Anounce']:
                    data [k] = utils.convert_date (v)
                if k == 'Amount':
                    data [k] = utils.convert_amount (v)
                if k == 'Currency':
                    data [k] = utils.convert_currency (v)
            except:
                print "Bad ", k, "|"+ v + "|"
        print data
        validate (data)


def AAL(t):
    res = []
    for r in t[0][1]:
        if len (r) == 0:
            continue
        currs = r[0].split('\r\n')
        amounts = r[1].split('\r\n')
        res.append ({ 'Record':r[2], 'Payment':r[3], 'Currency':currs[1], 'Amount':amounts[1]})
    return res

def ABF(t):
    res = []
    for r in t[0][1]:
        if len (r) != 4:
            continue
        res.append ({ 'Record':r[1], 'Payment':r[2], 'Currency':'GBP', 'Amount':r[3]})
    return res

def ADM(t):
    res = []
    for r in t[0][1]:
        if r[0] =='Year':
            continue
        res.append ({'Type':r[1], 'ExDiv':r[2], 'Record':r[3], 'Payment':r[4], 'Currency':'GBP', 'Amount':r[5]})
        
    return res

def AGK(t):
    res = []
    for r in t[0][1]:
        if r[2] != '':
            res.append ({'Type':'Interim','ExDiv':r[1],'Currency':'GBP', 'Amount':r[2]})
        if r[4] != '':
            res.append ({'Type':'Final','ExDiv':r[3],'Currency':'GBP', 'Amount':r[4]})
        
    return res

def AMEC(t):
    res = []
    for r in t[0][1]:
        if len(r) != 4:
            continue
        final = r[1][0:10]
        interim = r[1][11:]
        res.append ({'Type':'Final',  'Payment':final,  'Currency':'GBP', 'Amount':r[2].split(" ")[0]})
        res.append ({'Type':'Interim','Payment':interim,'Currency':'GBP', 'Amount':r[2].split(" ")[1]})
    return res

def ANTO(t):
    res = []
    # 5 for future dividends
    for r in t[5][1]:
        if r[0] in ['Next Dividend','']:
            continue
        if r[4] == r'N/A*':
            res.append ({'Type':r[0][:-5],  'Payment':r[1], 'Record':r[2], 'Currency':'USD', 'Amount':r[3]})
        else:
            res.append ({'Type':r[0][:-5],  'Payment':r[1], 'Record':r[2], 'Currency':'GBP', 'Amount':r[4]})
    for r in t[6][1]:
        if r[0] in ['Dividend','']:
            continue
        res.append ({'Type':r[0][:-5],  'Payment':r[1],  'Currency':'GBP', 'Amount':r[3]})
    return res

def ARM(t):
    res = []
    for r in t[1][1]:
        if r[0] == 'Declared':
            continue
        res.append ({'Announce':r[0], 'Record':r[1], 'Payment':r[2], 'Currency':'GBP', 'Amount':r[3], 'Type':r[4]})
    return res

def AV(t):
    res = []
    for r in t[0][1]:
        if len (r) < 5:
            continue
        res.append ({'ExDiv':r[1], 'Record':r[2], 'Payment':r[3], 'Currency':'GBP', 'Amount':r[4][:-1], 'Type':r[0]})
    return res

def BA(t):
    res = []
    for r in t[0][1]:
        res.append ({'Record':r[2], 'Payment':r[1], 'Currency':'GBP', 'Amount':r[4], 'Type':r[3][:-5]})
    return res

def BARC(t):
    res = []
    for r in t[0][1]:
        amount, typ = r[3].split ('p')
        typ = typ.strip()[1:-1]
        res.append ({'ExDiv':r[0], 'Record':r[1], 'Payment':r[2], 'Currency':'GBP', 'Amount':amount, 'Type':typ})
    return res


def BATS(t):
    res = []
    print t
    for i in range (0,10):
        for r in t[i][1]:
            print i, r
    return res

def BP(t):
    res = []
    for r in t[1][1]:
        if len(r) != 13:
            continue
        res.append ({'Anounce':r[3], 'Payment':r[5], 'Currency':'GBP', 'Amount':r[11]})
    return res

def BSY(t):
    print t
    res = []
    for i in range (0,10):
        for r in t[i][1]:
            print i, r
    return res

def CCL(t):
    res = []
    for r in t[6][1]:
        if r[1] == 'Record':
            continue
        res.append ({'Announce':r[2], 'ExDiv':r[0], 'Record':r[1], 'Payment':r[3], 'Currency':'USD', 'Amount':r[4][1:]})
    return res

def CNA(t):
    res = []
    for r in t[1][1]:
        res.append ({'Type':r[0].split(" ")[0], 'Announce':r[1], 'ExDiv':r[2], 'Record':r[3], 'Payment':r[4], 'Currency':'GBP', 'Amount':r[5][:-1]})
    return res

def CPG(t):
    res = []
    for r in t[0][1]:
        if r[0][0:5] != "Final":
            continue
        parts = r[0].split(' ')
        if parts[1] <= '2000':
            continue
        pfinal   = r[1].split("\n")[0]
        pinterim = r[1].split("\n")[1]
        afinal   = r[2].split("\n")[0]
        ainterim = r[2].split("\n")[1]
        res.append ({'Type':'Final',   'Payment':pfinal,   'Currency':'GBP', 'Amount':afinal  })
        res.append ({'Type':'Interim', 'Payment':pinterim, 'Currency':'GBP', 'Amount':ainterim})
    return res

def CPI(t):
    res = []
    for r in t[0][1]:
        print r
    return res

def CRDA(t):
    res = []
    for r in t[2][1]:
        if len(r) != 5:
            continue
        res.append ({'Type':r[0], 'Record':r[3], 'Payment':r[4], 'Currency':'GBP', 'Amount':r[1]})
    return res

def CSCG(t):
    res = []
    for r in t[0][1]:
        if len (r) != 8:
            continue
        if not r[2] in ['final', 'Interim']:
            continue
        #print r
        res.append ({'Type':r[2], 'Record':r[6][0:8], 'Payment':r[7][0:8], 'Currency':'GBP', 'Amount':r[3]})
    return res

def DGE(t):
    res = []
    for r in t[1][1]:
        if len(r) != 4:
            continue
        ipayment = r[3][0:8]
        fpayment = r[3][8:]
        iamount  = r[2].split('p')[0]
        famount  = r[2].split('p')[1]
        res.append ({'Type':'Interim', 'Payment':ipayment, 'Currency':'GBP', 'Amount':iamount})
        res.append ({'Type':'Final',   'Payment':fpayment, 'Currency':'GBP', 'Amount':famount})
    return res

def template(t):
    res = []
    for i in range (0,10):
        for r in t[i][1]:
            print i, r
    return res


def EMG(t):
    res = []
    for r in t[3][1]:
        if len (r) != 8:
            continue
        print  r
        res.append ({'Payment':r[1],   'ExDiv':r[3], 'Currency':'GBP', 'Amount':r[2]})
    return res

    
    return res


dump ('EMG')





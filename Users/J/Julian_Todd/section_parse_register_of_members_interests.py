import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse



monthdict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 
          'October':10, 'November':11, 'December':12}

regpayfields = ["mpname text", "datepay text", "datedeclared text", "money real", "minutes real"]
scraperwiki.sqlite.execute("drop table if exists regpay")
scraperwiki.sqlite.execute("create table regpay (%s)" % ",".join(regpayfields))


def Cparsereg(data, txt):
    mregistered = re.match("(.*?)\s*\(Registered\s*(\d+)\s*([A-Z][a-z]+)\s*(\d+)\)$", txt)
    if mregistered and mregistered.group(3) in monthdict:
        data["regdate"] = datetime.date(int(mregistered.group(4)), monthdict[mregistered.group(3)], int(mregistered.group(2)))
        txt = mregistered.group(1)

    mpay = re.search("(?i)\s*(?:(?:received )?payment of|fee of|received|of)?\s*\xc2\xa3([\d+,\.]+)(?:\s*received\.?)?", txt)
    if mpay:
        data["pounds"] = float(re.sub(",", "", mpay.group(1).strip(".")))
        txt = txt[:mpay.start(0)]+txt[mpay.end(0):]

    mhrmin = re.search("\s*Hours:\s*(\d+)\s+hr\s+(\d+)\s+mins\.?\s*", txt)
    if mhrmin:
        data["minutes"] = float(mhrmin.group(1)) * 60 + float(mhrmin.group(2))
        txt = txt[:mhrmin.start(0)]+txt[mhrmin.end(0):]

    mhours = re.search("\s*Hours:\s*([\d\.]+)\s*(minutes|mins|hours?|hrs?)\.*", txt)
    if mhours:
        if mhours.group(2)[:3] == "min":
            data["minutes"] = float(mhours.group(1))
        else:
            data["minutes"] = float(mhours.group(1)) * 60
        txt = txt[:mhours.start(0)]+txt[mhours.end(0):]

    monehour = re.search("\s*(?:Hours: )?One hour\.\s*", txt)
    if monehour:
        data["minutes"] = 60
        txt = txt[:monehour.start(0)]+txt[monehour.end(0):]


    mdate = re.search("(?:for\s+|on\s+)?(\d+)?\s*([A-Z]\w+)\s*(\d+)[,\.]?", txt)
    if mdate and mdate.group(2) in monthdict:
        data["date"] = datetime.date(int(mdate.group(3)), monthdict[mdate.group(2)], int(mdate.group(1) or "1"))
        txt = txt[:mdate.start(0)]+txt[mdate.end(0):]
        
    mchar = re.search("\s*\(Fee paid to (charity).\)\s*", txt)
    if mchar:
        data["paidto"] = mchar.group(1)
        txt = txt[:mchar.start(0)]+txt[mchar.end(0):]

    msurv = re.search(u'\s*for (?:completing )?(?:a )?(survey|speech|advising clients|writing an article|seminar with students)[,\.]?\s*', txt)
    if msurv:
        data["workdone"] = msurv.group(1)
        txt = txt[:msurv.start(0)]+txt[msurv.end(0):]

    msal = re.search(u'\s*gross monthly (salary)\s*', txt)
    if msal:
        data["workdone"] = msal.group(1)
        txt = txt[:msal.start(0)]+txt[msal.end(0):]

    return txt



def ParseType2(mpname, contents):
    i = 1
    for ptag, txt in re.findall("(\S+)\s(.*)", contents):
        i += 1
        if ptag == "p.indent2":
            data = { }
            txt2 = Cparsereg(data, txt)
            if txt2:
                print "\n".join([mpname, str([txt2]), str(data), txt])
            data["mpname"] = mpname
            data["i"] = i
            scraperwiki.sqlite.save(unique_keys=["mpname", "i"], data=data)



#            sqlitecommand("execute", "insert into regpay values (?,?,?,?,?)", 
#                          (mpname, paydate.isoformat(), regdate.isoformat(), pounds, minutes))
#        sqlitecommand("commit")



print scraperwiki.sqlite.attach("parse-register-members-interests", "src")
result = scraperwiki.sqlite.execute("select mpname, contents from src.regmemtext where h3num = 2 limit 2000")
for mpdata in result["data"]:
    ParseType2(mpdata[0], mpdata[1])
    import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse



monthdict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 
          'October':10, 'November':11, 'December':12}

regpayfields = ["mpname text", "datepay text", "datedeclared text", "money real", "minutes real"]
scraperwiki.sqlite.execute("drop table if exists regpay")
scraperwiki.sqlite.execute("create table regpay (%s)" % ",".join(regpayfields))


def Cparsereg(data, txt):
    mregistered = re.match("(.*?)\s*\(Registered\s*(\d+)\s*([A-Z][a-z]+)\s*(\d+)\)$", txt)
    if mregistered and mregistered.group(3) in monthdict:
        data["regdate"] = datetime.date(int(mregistered.group(4)), monthdict[mregistered.group(3)], int(mregistered.group(2)))
        txt = mregistered.group(1)

    mpay = re.search("(?i)\s*(?:(?:received )?payment of|fee of|received|of)?\s*\xc2\xa3([\d+,\.]+)(?:\s*received\.?)?", txt)
    if mpay:
        data["pounds"] = float(re.sub(",", "", mpay.group(1).strip(".")))
        txt = txt[:mpay.start(0)]+txt[mpay.end(0):]

    mhrmin = re.search("\s*Hours:\s*(\d+)\s+hr\s+(\d+)\s+mins\.?\s*", txt)
    if mhrmin:
        data["minutes"] = float(mhrmin.group(1)) * 60 + float(mhrmin.group(2))
        txt = txt[:mhrmin.start(0)]+txt[mhrmin.end(0):]

    mhours = re.search("\s*Hours:\s*([\d\.]+)\s*(minutes|mins|hours?|hrs?)\.*", txt)
    if mhours:
        if mhours.group(2)[:3] == "min":
            data["minutes"] = float(mhours.group(1))
        else:
            data["minutes"] = float(mhours.group(1)) * 60
        txt = txt[:mhours.start(0)]+txt[mhours.end(0):]

    monehour = re.search("\s*(?:Hours: )?One hour\.\s*", txt)
    if monehour:
        data["minutes"] = 60
        txt = txt[:monehour.start(0)]+txt[monehour.end(0):]


    mdate = re.search("(?:for\s+|on\s+)?(\d+)?\s*([A-Z]\w+)\s*(\d+)[,\.]?", txt)
    if mdate and mdate.group(2) in monthdict:
        data["date"] = datetime.date(int(mdate.group(3)), monthdict[mdate.group(2)], int(mdate.group(1) or "1"))
        txt = txt[:mdate.start(0)]+txt[mdate.end(0):]
        
    mchar = re.search("\s*\(Fee paid to (charity).\)\s*", txt)
    if mchar:
        data["paidto"] = mchar.group(1)
        txt = txt[:mchar.start(0)]+txt[mchar.end(0):]

    msurv = re.search(u'\s*for (?:completing )?(?:a )?(survey|speech|advising clients|writing an article|seminar with students)[,\.]?\s*', txt)
    if msurv:
        data["workdone"] = msurv.group(1)
        txt = txt[:msurv.start(0)]+txt[msurv.end(0):]

    msal = re.search(u'\s*gross monthly (salary)\s*', txt)
    if msal:
        data["workdone"] = msal.group(1)
        txt = txt[:msal.start(0)]+txt[msal.end(0):]

    return txt



def ParseType2(mpname, contents):
    i = 1
    for ptag, txt in re.findall("(\S+)\s(.*)", contents):
        i += 1
        if ptag == "p.indent2":
            data = { }
            txt2 = Cparsereg(data, txt)
            if txt2:
                print "\n".join([mpname, str([txt2]), str(data), txt])
            data["mpname"] = mpname
            data["i"] = i
            scraperwiki.sqlite.save(unique_keys=["mpname", "i"], data=data)



#            sqlitecommand("execute", "insert into regpay values (?,?,?,?,?)", 
#                          (mpname, paydate.isoformat(), regdate.isoformat(), pounds, minutes))
#        sqlitecommand("commit")



print scraperwiki.sqlite.attach("parse-register-members-interests", "src")
result = scraperwiki.sqlite.execute("select mpname, contents from src.regmemtext where h3num = 2 limit 2000")
for mpdata in result["data"]:
    ParseType2(mpdata[0], mpdata[1])
    import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse



monthdict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 
          'October':10, 'November':11, 'December':12}

regpayfields = ["mpname text", "datepay text", "datedeclared text", "money real", "minutes real"]
scraperwiki.sqlite.execute("drop table if exists regpay")
scraperwiki.sqlite.execute("create table regpay (%s)" % ",".join(regpayfields))


def Cparsereg(data, txt):
    mregistered = re.match("(.*?)\s*\(Registered\s*(\d+)\s*([A-Z][a-z]+)\s*(\d+)\)$", txt)
    if mregistered and mregistered.group(3) in monthdict:
        data["regdate"] = datetime.date(int(mregistered.group(4)), monthdict[mregistered.group(3)], int(mregistered.group(2)))
        txt = mregistered.group(1)

    mpay = re.search("(?i)\s*(?:(?:received )?payment of|fee of|received|of)?\s*\xc2\xa3([\d+,\.]+)(?:\s*received\.?)?", txt)
    if mpay:
        data["pounds"] = float(re.sub(",", "", mpay.group(1).strip(".")))
        txt = txt[:mpay.start(0)]+txt[mpay.end(0):]

    mhrmin = re.search("\s*Hours:\s*(\d+)\s+hr\s+(\d+)\s+mins\.?\s*", txt)
    if mhrmin:
        data["minutes"] = float(mhrmin.group(1)) * 60 + float(mhrmin.group(2))
        txt = txt[:mhrmin.start(0)]+txt[mhrmin.end(0):]

    mhours = re.search("\s*Hours:\s*([\d\.]+)\s*(minutes|mins|hours?|hrs?)\.*", txt)
    if mhours:
        if mhours.group(2)[:3] == "min":
            data["minutes"] = float(mhours.group(1))
        else:
            data["minutes"] = float(mhours.group(1)) * 60
        txt = txt[:mhours.start(0)]+txt[mhours.end(0):]

    monehour = re.search("\s*(?:Hours: )?One hour\.\s*", txt)
    if monehour:
        data["minutes"] = 60
        txt = txt[:monehour.start(0)]+txt[monehour.end(0):]


    mdate = re.search("(?:for\s+|on\s+)?(\d+)?\s*([A-Z]\w+)\s*(\d+)[,\.]?", txt)
    if mdate and mdate.group(2) in monthdict:
        data["date"] = datetime.date(int(mdate.group(3)), monthdict[mdate.group(2)], int(mdate.group(1) or "1"))
        txt = txt[:mdate.start(0)]+txt[mdate.end(0):]
        
    mchar = re.search("\s*\(Fee paid to (charity).\)\s*", txt)
    if mchar:
        data["paidto"] = mchar.group(1)
        txt = txt[:mchar.start(0)]+txt[mchar.end(0):]

    msurv = re.search(u'\s*for (?:completing )?(?:a )?(survey|speech|advising clients|writing an article|seminar with students)[,\.]?\s*', txt)
    if msurv:
        data["workdone"] = msurv.group(1)
        txt = txt[:msurv.start(0)]+txt[msurv.end(0):]

    msal = re.search(u'\s*gross monthly (salary)\s*', txt)
    if msal:
        data["workdone"] = msal.group(1)
        txt = txt[:msal.start(0)]+txt[msal.end(0):]

    return txt



def ParseType2(mpname, contents):
    i = 1
    for ptag, txt in re.findall("(\S+)\s(.*)", contents):
        i += 1
        if ptag == "p.indent2":
            data = { }
            txt2 = Cparsereg(data, txt)
            if txt2:
                print "\n".join([mpname, str([txt2]), str(data), txt])
            data["mpname"] = mpname
            data["i"] = i
            scraperwiki.sqlite.save(unique_keys=["mpname", "i"], data=data)



#            sqlitecommand("execute", "insert into regpay values (?,?,?,?,?)", 
#                          (mpname, paydate.isoformat(), regdate.isoformat(), pounds, minutes))
#        sqlitecommand("commit")



print scraperwiki.sqlite.attach("parse-register-members-interests", "src")
result = scraperwiki.sqlite.execute("select mpname, contents from src.regmemtext where h3num = 2 limit 2000")
for mpdata in result["data"]:
    ParseType2(mpdata[0], mpdata[1])
    import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse



monthdict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 
          'October':10, 'November':11, 'December':12}

regpayfields = ["mpname text", "datepay text", "datedeclared text", "money real", "minutes real"]
scraperwiki.sqlite.execute("drop table if exists regpay")
scraperwiki.sqlite.execute("create table regpay (%s)" % ",".join(regpayfields))


def Cparsereg(data, txt):
    mregistered = re.match("(.*?)\s*\(Registered\s*(\d+)\s*([A-Z][a-z]+)\s*(\d+)\)$", txt)
    if mregistered and mregistered.group(3) in monthdict:
        data["regdate"] = datetime.date(int(mregistered.group(4)), monthdict[mregistered.group(3)], int(mregistered.group(2)))
        txt = mregistered.group(1)

    mpay = re.search("(?i)\s*(?:(?:received )?payment of|fee of|received|of)?\s*\xc2\xa3([\d+,\.]+)(?:\s*received\.?)?", txt)
    if mpay:
        data["pounds"] = float(re.sub(",", "", mpay.group(1).strip(".")))
        txt = txt[:mpay.start(0)]+txt[mpay.end(0):]

    mhrmin = re.search("\s*Hours:\s*(\d+)\s+hr\s+(\d+)\s+mins\.?\s*", txt)
    if mhrmin:
        data["minutes"] = float(mhrmin.group(1)) * 60 + float(mhrmin.group(2))
        txt = txt[:mhrmin.start(0)]+txt[mhrmin.end(0):]

    mhours = re.search("\s*Hours:\s*([\d\.]+)\s*(minutes|mins|hours?|hrs?)\.*", txt)
    if mhours:
        if mhours.group(2)[:3] == "min":
            data["minutes"] = float(mhours.group(1))
        else:
            data["minutes"] = float(mhours.group(1)) * 60
        txt = txt[:mhours.start(0)]+txt[mhours.end(0):]

    monehour = re.search("\s*(?:Hours: )?One hour\.\s*", txt)
    if monehour:
        data["minutes"] = 60
        txt = txt[:monehour.start(0)]+txt[monehour.end(0):]


    mdate = re.search("(?:for\s+|on\s+)?(\d+)?\s*([A-Z]\w+)\s*(\d+)[,\.]?", txt)
    if mdate and mdate.group(2) in monthdict:
        data["date"] = datetime.date(int(mdate.group(3)), monthdict[mdate.group(2)], int(mdate.group(1) or "1"))
        txt = txt[:mdate.start(0)]+txt[mdate.end(0):]
        
    mchar = re.search("\s*\(Fee paid to (charity).\)\s*", txt)
    if mchar:
        data["paidto"] = mchar.group(1)
        txt = txt[:mchar.start(0)]+txt[mchar.end(0):]

    msurv = re.search(u'\s*for (?:completing )?(?:a )?(survey|speech|advising clients|writing an article|seminar with students)[,\.]?\s*', txt)
    if msurv:
        data["workdone"] = msurv.group(1)
        txt = txt[:msurv.start(0)]+txt[msurv.end(0):]

    msal = re.search(u'\s*gross monthly (salary)\s*', txt)
    if msal:
        data["workdone"] = msal.group(1)
        txt = txt[:msal.start(0)]+txt[msal.end(0):]

    return txt



def ParseType2(mpname, contents):
    i = 1
    for ptag, txt in re.findall("(\S+)\s(.*)", contents):
        i += 1
        if ptag == "p.indent2":
            data = { }
            txt2 = Cparsereg(data, txt)
            if txt2:
                print "\n".join([mpname, str([txt2]), str(data), txt])
            data["mpname"] = mpname
            data["i"] = i
            scraperwiki.sqlite.save(unique_keys=["mpname", "i"], data=data)



#            sqlitecommand("execute", "insert into regpay values (?,?,?,?,?)", 
#                          (mpname, paydate.isoformat(), regdate.isoformat(), pounds, minutes))
#        sqlitecommand("commit")



print scraperwiki.sqlite.attach("parse-register-members-interests", "src")
result = scraperwiki.sqlite.execute("select mpname, contents from src.regmemtext where h3num = 2 limit 2000")
for mpdata in result["data"]:
    ParseType2(mpdata[0], mpdata[1])
    
import scraperwiki

import json
import httplib, urllib
import datetime
import dateutil.parser
import time
import re

agency = "Arendal kommune"
urlhost = "www.arendal.kommune.no"

fieldmap = {
    'AntallVedlegg' : '',
    'Arkivdel' : '',
    'AvsenderMottaker' : 'sender', # or recipient
    'Dokumentdato' : 'docdate',
    'Dokumentnummer' : 'casedocseq',
    'Dokumenttype' : 'doctype',
    'EkspedertDato' : '',
    'Hjemmel' : 'exemption',
    'Id' : 'id',
    'Innholdsbeskrivelse' : 'docdesc',
    'Mappetype' : '',
    'Offentlig' : 'ispublic',
    'PostlisteType' : 'doctype',
    'RegistrertDato' : 'recorddate',
    'SaksId' : '',
    'SaksNr' : 'caseid',
    'Sakstittel' : 'casedesc',
    #'SaksNr' : 'SA.SAAR + SA.SEKNR',
    'Saksansvarlig' : 'saksbehandler',
    'SaksansvarligEnhet' : '',
    'SaksansvarligEpost' : '',

#    'scrapestamputc' : '',
#    'scrapedurl' : '',
#    'agency' : '',
}


# Convert "/Date(1317808020000+0200)/" to a datetime object
# FIXME Currently ignore the timezone information
def parse_datestr(str):
    match = re.split("[/()+]", str)
#    print match
    sinceepoch = float(match[2]) / 1000
    if match[3] == '0200':
        sinceepoch = sinceepoch + 2 * 60 * 60
    if match[3] == '0100':
        sinceepoch = sinceepoch + 1 * 60 * 60
#    print sinceepoch
    date = datetime.datetime.fromtimestamp(sinceepoch)
#    print date
    return date

def reformat_caseid(caseid):
    # Input 12/13123, output 2012, 13123, "2012/13123"
    year, seqnr = caseid.split("/")
    year = int(year)
    if year < 100:
        year = year + 2000
    caseid = "%d/%s" % (year, seqnr)
    return year, int(seqnr), caseid

def ws_post(url, urlhost, urlpath, params):
    jsonparams = json.dumps(params)
    headers = {"Content-type": "application/json; charset=utf-8",
               "Accept": "application/json"}
    conn = httplib.HTTPConnection(urlhost)
    #print jsonparams
    conn.request("POST", urlpath, jsonparams, headers)
    response = conn.getresponse()
    #print response.status, response.reason
    jsonres = response.read()
    res = json.loads(jsonres)
    #print res
    return res

def fetch_journal_entry(id):
    params = { "id" : str(id)}
    headers = {"Content-type": "application/json; charset=utf-8",
               "Accept": "application/json"}
    urlpath = "/Templates/eDemokrati/Services/eDemokratiService.svc/GetPostlisteObjekt"
    data = ws_post(None, urlhost, urlpath, params)['d']
    entry = None
    if data:
        del data['__type'] # This is useless, ignore
        print data
        entry = {}
        entry['agency'] = agency
        entry['scrapestamputc'] = datetime.datetime.now()
        entry['scrapedurl'] = "http://" + urlhost + urlpath
#        entry['scrapedurl'] = url
        for dfield in fieldmap.keys():
            if dfield in data and data[dfield]:
                if dfield in fieldmap and fieldmap[dfield] != "":
                    fieldname = fieldmap[dfield]
                else:
                    fieldname = dfield
                if 'sender' == fieldname:
                    if data['Dokumenttype'] == 'U':
                        fieldname = 'recipient'
                if dfield in ['RegistrertDato', 'Dokumentdato', 'EkspedertDato']:
                    entry[fieldname] = parse_datestr(data[dfield]).date()
                else:
                    entry[fieldname] = data[dfield]
            else:
                entry[dfield] = data[dfield]
        entry['caseyear'], entry['caseseqnr'], entry['caseid'] = reformat_caseid(entry['caseid'])
#    data["sourceurl"] = "http://" + server + path
    print entry
    return entry

def epoctime_to_datestr(epoctime):
    return "/Date("+str(int(epoctime * 1000) )+")/"

def get_last_entry_id():
    now = time.time()
    # Get the last week, as the most recent entry should be in this range
    fradato = epoctime_to_datestr(now - 7 * 24 * 60 * 60)
    tildato = epoctime_to_datestr(now)
    #print fradato

    maxid = 0

    urlpath = "/Templates/eDemokrati/Services/eDemokratiService.svc/GetPostlisteArkivdeler"
    params = {
        "dato": fradato,
        "tilDato": tildato,
        "søkestreng":""}
    arkivdeler = ws_post(None, urlhost, urlpath, params)['d']
    # {u'd': [u'_', u'HVA-IFE-A', u'KAR-BR-A', u'KAR-BRUK-A', u'KAR-EIEN-A', u'KAR-ELBH-A', u'KAR-ELS-A', ...

    urlpath = "/Templates/eDemokrati/Services/eDemokratiService.svc/GetPostlisteDokumenttyper"
    for arkivdel in arkivdeler[0]:
        params = {
            "dato":fradato,
            "tilDato":tildato,
            "søkestreng":"",
            "arkivdel":arkivdel,
        }
        doctypes = ws_post(None, urlhost, urlpath, params)['d']
        #{"d":["I","N","S","U","X"]}
        urlpath = "/Templates/eDemokrati/Services/eDemokratiService.svc/GetPostlisteS%C3%B8k"
        for doctype in doctypes:
            params = {
                "fraDato":fradato,
                "tilDato":tildato,
                "søkestreng":"",
                "arkivdel":arkivdel,
                "dokumenttype":doctype,
            }
            entries = ws_post(None, urlhost, urlpath, params)['d']
            for entry in entries:
                #print entry['Id']
                id = int(entry['Id'])
                if id > maxid:
                    maxid = id
#                data = fetch_journal_entry(entry['Id'])
#                if data:
#                    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    return maxid

#{"d":[{"__type":"PostlisteObjekt:#SSP.NoarkServices","AntallVedlegg":1,"Dokumentnummer":2,"Dokumenttype":"I","EkspedertDato":null,"Hjemmel":null,"Id":1507868,"Innholdsbeskrivelse":"Tomtejustering - Lillebæk, eiendom 208\/1611","Offentlig":true,"RegistrertDato":"\/Date(1339538400000+0200)\/","SaksId":296971,"SaksNr":"12\/8658","Arkivdel":"KAR-EIEN-A","AvsenderMottaker":"Randi Wilberg","Dokumentdato":"\/Date(1339624800000+0200)\/","Mappetype":"DS","PostlisteType":"I","Saksansvarlig":null,"SaksansvarligEnhet":null,"SaksansvarligEpost":null,"Sakstittel":null},{"__type":"PostlisteObjekt:#SSP.NoarkServices","AntallVedlegg":4,"Dokumentnummer":1,"Dokumenttype":"I","EkspedertDato":null,"Hjemmel":null,"Id":1507865,"Innholdsbeskrivelse":"Søknkad om utvidelse av balkong - Kalleraveien 14","Offentlig":true,"RegistrertDato":"\/Date(1339538400000+0200)\/","SaksId":298804,"SaksNr":"12\/10480","Arkivdel":"KAR-EIEN-A","AvsenderMottaker":"Ole Henning Løken","Dokumentdato":"\/Date(1338847200000+0200)\/","Mappetype":"BS","PostlisteType":"I","Saksansvarlig":null,"SaksansvarligEnhet":null,"SaksansvarligEpost":null,"Sakstittel":null},...

def get_journal_enries_range(min, max, step):
    for id in range(min, max, step):
        data = fetch_journal_entry(id)
        #print data
        if data:
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)

maxid = get_last_entry_id()
print "max id =", maxid
try:
    start = scraperwiki.sqlite.select("max(id) as max from swdata")[0]['max'] + 1
except:
    start = 137459
print start, maxid
#if maxid > start + 20:
#    maxid = start + 10
get_journal_enries_range(start, maxid, 1)

start = scraperwiki.sqlite.select("min(id) as min from swdata")[0]['min'] - 1
end = start - 1000
print start, end
get_journal_enries_range(start, end, -1)
import scraperwiki

import json
import httplib, urllib
import datetime
import dateutil.parser
import time
import re

agency = "Arendal kommune"
urlhost = "www.arendal.kommune.no"

fieldmap = {
    'AntallVedlegg' : '',
    'Arkivdel' : '',
    'AvsenderMottaker' : 'sender', # or recipient
    'Dokumentdato' : 'docdate',
    'Dokumentnummer' : 'casedocseq',
    'Dokumenttype' : 'doctype',
    'EkspedertDato' : '',
    'Hjemmel' : 'exemption',
    'Id' : 'id',
    'Innholdsbeskrivelse' : 'docdesc',
    'Mappetype' : '',
    'Offentlig' : 'ispublic',
    'PostlisteType' : 'doctype',
    'RegistrertDato' : 'recorddate',
    'SaksId' : '',
    'SaksNr' : 'caseid',
    'Sakstittel' : 'casedesc',
    #'SaksNr' : 'SA.SAAR + SA.SEKNR',
    'Saksansvarlig' : 'saksbehandler',
    'SaksansvarligEnhet' : '',
    'SaksansvarligEpost' : '',

#    'scrapestamputc' : '',
#    'scrapedurl' : '',
#    'agency' : '',
}


# Convert "/Date(1317808020000+0200)/" to a datetime object
# FIXME Currently ignore the timezone information
def parse_datestr(str):
    match = re.split("[/()+]", str)
#    print match
    sinceepoch = float(match[2]) / 1000
    if match[3] == '0200':
        sinceepoch = sinceepoch + 2 * 60 * 60
    if match[3] == '0100':
        sinceepoch = sinceepoch + 1 * 60 * 60
#    print sinceepoch
    date = datetime.datetime.fromtimestamp(sinceepoch)
#    print date
    return date

def reformat_caseid(caseid):
    # Input 12/13123, output 2012, 13123, "2012/13123"
    year, seqnr = caseid.split("/")
    year = int(year)
    if year < 100:
        year = year + 2000
    caseid = "%d/%s" % (year, seqnr)
    return year, int(seqnr), caseid

def ws_post(url, urlhost, urlpath, params):
    jsonparams = json.dumps(params)
    headers = {"Content-type": "application/json; charset=utf-8",
               "Accept": "application/json"}
    conn = httplib.HTTPConnection(urlhost)
    #print jsonparams
    conn.request("POST", urlpath, jsonparams, headers)
    response = conn.getresponse()
    #print response.status, response.reason
    jsonres = response.read()
    res = json.loads(jsonres)
    #print res
    return res

def fetch_journal_entry(id):
    params = { "id" : str(id)}
    headers = {"Content-type": "application/json; charset=utf-8",
               "Accept": "application/json"}
    urlpath = "/Templates/eDemokrati/Services/eDemokratiService.svc/GetPostlisteObjekt"
    data = ws_post(None, urlhost, urlpath, params)['d']
    entry = None
    if data:
        del data['__type'] # This is useless, ignore
        print data
        entry = {}
        entry['agency'] = agency
        entry['scrapestamputc'] = datetime.datetime.now()
        entry['scrapedurl'] = "http://" + urlhost + urlpath
#        entry['scrapedurl'] = url
        for dfield in fieldmap.keys():
            if dfield in data and data[dfield]:
                if dfield in fieldmap and fieldmap[dfield] != "":
                    fieldname = fieldmap[dfield]
                else:
                    fieldname = dfield
                if 'sender' == fieldname:
                    if data['Dokumenttype'] == 'U':
                        fieldname = 'recipient'
                if dfield in ['RegistrertDato', 'Dokumentdato', 'EkspedertDato']:
                    entry[fieldname] = parse_datestr(data[dfield]).date()
                else:
                    entry[fieldname] = data[dfield]
            else:
                entry[dfield] = data[dfield]
        entry['caseyear'], entry['caseseqnr'], entry['caseid'] = reformat_caseid(entry['caseid'])
#    data["sourceurl"] = "http://" + server + path
    print entry
    return entry

def epoctime_to_datestr(epoctime):
    return "/Date("+str(int(epoctime * 1000) )+")/"

def get_last_entry_id():
    now = time.time()
    # Get the last week, as the most recent entry should be in this range
    fradato = epoctime_to_datestr(now - 7 * 24 * 60 * 60)
    tildato = epoctime_to_datestr(now)
    #print fradato

    maxid = 0

    urlpath = "/Templates/eDemokrati/Services/eDemokratiService.svc/GetPostlisteArkivdeler"
    params = {
        "dato": fradato,
        "tilDato": tildato,
        "søkestreng":""}
    arkivdeler = ws_post(None, urlhost, urlpath, params)['d']
    # {u'd': [u'_', u'HVA-IFE-A', u'KAR-BR-A', u'KAR-BRUK-A', u'KAR-EIEN-A', u'KAR-ELBH-A', u'KAR-ELS-A', ...

    urlpath = "/Templates/eDemokrati/Services/eDemokratiService.svc/GetPostlisteDokumenttyper"
    for arkivdel in arkivdeler[0]:
        params = {
            "dato":fradato,
            "tilDato":tildato,
            "søkestreng":"",
            "arkivdel":arkivdel,
        }
        doctypes = ws_post(None, urlhost, urlpath, params)['d']
        #{"d":["I","N","S","U","X"]}
        urlpath = "/Templates/eDemokrati/Services/eDemokratiService.svc/GetPostlisteS%C3%B8k"
        for doctype in doctypes:
            params = {
                "fraDato":fradato,
                "tilDato":tildato,
                "søkestreng":"",
                "arkivdel":arkivdel,
                "dokumenttype":doctype,
            }
            entries = ws_post(None, urlhost, urlpath, params)['d']
            for entry in entries:
                #print entry['Id']
                id = int(entry['Id'])
                if id > maxid:
                    maxid = id
#                data = fetch_journal_entry(entry['Id'])
#                if data:
#                    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    return maxid

#{"d":[{"__type":"PostlisteObjekt:#SSP.NoarkServices","AntallVedlegg":1,"Dokumentnummer":2,"Dokumenttype":"I","EkspedertDato":null,"Hjemmel":null,"Id":1507868,"Innholdsbeskrivelse":"Tomtejustering - Lillebæk, eiendom 208\/1611","Offentlig":true,"RegistrertDato":"\/Date(1339538400000+0200)\/","SaksId":296971,"SaksNr":"12\/8658","Arkivdel":"KAR-EIEN-A","AvsenderMottaker":"Randi Wilberg","Dokumentdato":"\/Date(1339624800000+0200)\/","Mappetype":"DS","PostlisteType":"I","Saksansvarlig":null,"SaksansvarligEnhet":null,"SaksansvarligEpost":null,"Sakstittel":null},{"__type":"PostlisteObjekt:#SSP.NoarkServices","AntallVedlegg":4,"Dokumentnummer":1,"Dokumenttype":"I","EkspedertDato":null,"Hjemmel":null,"Id":1507865,"Innholdsbeskrivelse":"Søknkad om utvidelse av balkong - Kalleraveien 14","Offentlig":true,"RegistrertDato":"\/Date(1339538400000+0200)\/","SaksId":298804,"SaksNr":"12\/10480","Arkivdel":"KAR-EIEN-A","AvsenderMottaker":"Ole Henning Løken","Dokumentdato":"\/Date(1338847200000+0200)\/","Mappetype":"BS","PostlisteType":"I","Saksansvarlig":null,"SaksansvarligEnhet":null,"SaksansvarligEpost":null,"Sakstittel":null},...

def get_journal_enries_range(min, max, step):
    for id in range(min, max, step):
        data = fetch_journal_entry(id)
        #print data
        if data:
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)

maxid = get_last_entry_id()
print "max id =", maxid
try:
    start = scraperwiki.sqlite.select("max(id) as max from swdata")[0]['max'] + 1
except:
    start = 137459
print start, maxid
#if maxid > start + 20:
#    maxid = start + 10
get_journal_enries_range(start, maxid, 1)

start = scraperwiki.sqlite.select("min(id) as min from swdata")[0]['min'] - 1
end = start - 1000
print start, end
get_journal_enries_range(start, end, -1)

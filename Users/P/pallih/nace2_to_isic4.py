import os, cgi
import scraperwiki
import simplejson

qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

def printjson(selection_statement):
    scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
    scraperwiki.sqlite.attach("isic4-nace2")
    nace2_isic4 = scraperwiki.sqlite.select(selection_statement)
    json = simplejson.dumps(nace2_isic4)
    print json
    exit()

if qsenv:
    if 'nace2code' in qsenv:
        nace2code = qsenv['nace2code']
        selection_statement = '* from ISIC4_vs_NACE2 where NACE2code="' + nace2code +'"'
        printjson(selection_statement)
    if 'isic4code' in qsenv:
        isic4code = qsenv["isic4code"]
        selection_statement = '* from ISIC4_vs_NACE2 where ISIC4code="' + isic4code +'"'
        printjson(selection_statement)

print 'Pass in a ISIC4 code or NACE rev2 code, like this:<br><br>'
print 'ISIC4 = https://views.scraperwiki.com/run/nace2_to_isic4/?isic4code=ISIC4_CODE_HERE<br>'
print 'NACE2 = https://views.scraperwiki.com/run/nace2_to_isic4/?nace2code=NACE2_CODE_HERE<br>'
print '<br>'
print 'Response is in JSON'


import os, cgi
import scraperwiki
import simplejson

qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

def printjson(selection_statement):
    scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
    scraperwiki.sqlite.attach("isic4-nace2")
    nace2_isic4 = scraperwiki.sqlite.select(selection_statement)
    json = simplejson.dumps(nace2_isic4)
    print json
    exit()

if qsenv:
    if 'nace2code' in qsenv:
        nace2code = qsenv['nace2code']
        selection_statement = '* from ISIC4_vs_NACE2 where NACE2code="' + nace2code +'"'
        printjson(selection_statement)
    if 'isic4code' in qsenv:
        isic4code = qsenv["isic4code"]
        selection_statement = '* from ISIC4_vs_NACE2 where ISIC4code="' + isic4code +'"'
        printjson(selection_statement)

print 'Pass in a ISIC4 code or NACE rev2 code, like this:<br><br>'
print 'ISIC4 = https://views.scraperwiki.com/run/nace2_to_isic4/?isic4code=ISIC4_CODE_HERE<br>'
print 'NACE2 = https://views.scraperwiki.com/run/nace2_to_isic4/?nace2code=NACE2_CODE_HERE<br>'
print '<br>'
print 'Response is in JSON'



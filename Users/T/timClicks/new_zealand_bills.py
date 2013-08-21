from pprint import pprint

# A look at how bills are progressing through 
# New Zealand's Parliament


## NOT YET FUNCTIONAL

import scraperwiki as sw
from scrapemark import scrape

URL = "http://www.parliament.nz/en-NZ/PB/Legislation/Bills/"


INDIVIDUAL_BILL = """
<head>{{ meta|html }}</head>

<div class="infoTiles right">
{* <a href="{{ [related].link|abs }}">{{ [related].title }}</a> *}
</div>

<div class="copy"><h1>{{ title }}</h1>{{ description }}

<table class="variablelist">
{*
    <tr><th>{{ [details].var }}</th><td>{{ [details].content }}</td></tr>
*}
</table>

</div>

"""

PATTERN = """<div class="numbers">{* <a href="{{ [sources]|abs }}"></a> *}</div>"""

PATTERN2 = """<table class="listing">
<tbody>
{*   <td><a href="{{ [bills]|abs }}"></a></td>  *}
</tbody>
</table>
"""


def do_meta(result):
    """
    Workaround for bug in scrapermark for empty attributes, e.g. NZGLS.subject
    """
    fields = {
        u"DC.Date": 'valid_from',
        u"DC.ChannelGuid": 'dc_channelguid',
        u"DC.CommitteeStatus": 'dc_committeestatus',
        u"DC.Format": 'bill_type',
        u"NZGLS.Identifier": 'nzgls_identifier',
    }
    meta = result['meta'].splitlines()
    for line in meta:
        parts=line.split('"')
        if 'meta' in parts[0] and parts[1] in fields:
            result[fields[parts[1]]] = parts[3]


def normalise_var(variable):
    """
    >>> normalise_var(u'Member in charge:')
    u'member_in_charge'
    """
    return variable[:-1].lower().replace(' ', '_') 

def do_details(result):
    """
    { 'details': [{'var': u'Member in charge:', 'content': u'Hon Bill English'}, {'var': u'Type of bill:', 'content': u'Government'}, {'var': u'Parliament:', 'content': u'49'}, {'var': u'Bill no:', 'content': u'79-1'}, {'var': u'Introduction:', 'content': u'8/9/09'}, {'var': u'First reading:', 'content': u'8/9/09'}, {'var': u'Second reading:', 'content': u'8/9/09'}, {'var': u'', 'content': u''}, {'var': u'Committee of the whole House:', 'content': u'8/9/09'}, {'var': u'Third reading:', 'content': u'8/9/09'}, {'var': u'Royal assent:', 'content': u'12/9/09'}, {'var': u'Act:', 'content': u'Crown Retail Deposit Guarantee Scheme Act 2009 (09/30)'}] }
    """
    for detail in result['details']:
        result[normalise_var(detail['var'])] = detail['content']

def do_related(result):
    """
{'related': [{'link': u'http://www.parliament.nz/en-NZ/PB/Legislation/Bills/BillsDigests/f/d/e/49PLLawBD17071-Crown-Retail-Deposit-Guarantee-Scheme-Bill-2009-Bills.htm', 'title': u'Bills Digest No 1707'}, {'link': u'http://www.parliament.nz/en-NZ/PB/Debates/Debates/f/a/c/49HansD_20090908_00000800-Crown-Retail-Deposit-Guarantee-Scheme-Bill.htm', 'title': u'Parliamentary Debates (Hansard) Crown Retail Deposit Guarantee Scheme Bill \u2014 First Reading, Second Reading, In Committee'}, {'link': u'http://www.parliament.nz/en-NZ/PB/Debates/Debates/9/e/7/49HansD_20090909_00000001-Crown-Retail-Deposit-Guarantee-Scheme-Bill.htm', 'title': u'Parliamentary Debates (Hansard) Crown Retail Deposit Guarantee Scheme Bill \u2014 In Committee, Third Reading'}, {'link': u'http://www.legislation.govt.nz/act/public/2009/0030/15.0/versions.aspx', 'title': u'Text of bill, act and related SOPs on New Zealand Legislation website'}]}
    """
    result['related_pages'] = '|'.join(r['title'] for r in result['related'])

def cleanup(result):
    del result['details']
    del result['related']
    del result['meta']


def main():
    links = scrape(PATTERN, url=URL)
    print links
    #done= set([res['nzgls_identifier'] for res in sw.sqlite.select('nzgls_identifier FROM bills')])
    #print done
    for link in links['sources']:
        bills = scrape(PATTERN2, url=link)['bills']
        print bills
        for bill in bills:
            print bill
            try:
                bill = scrape(INDIVIDUAL_BILL, url=bill)
            except Exception, e:
                print "DEBUG: %s" % e
                continue
            bill['link'] = link
            do_details(bill)
            do_meta(bill)
            do_related(bill)
            for related_doc in bill['related']:
                related_doc['nzgls_identifier']=bill['nzgls_identifier']
                related_doc['bill']=bill['title']
            sw.sqlite.save(['link'], data=bill['related'], table_name='related_docs')
            cleanup(bill)
            sw.sqlite.save(['link', 'valid_from'], data=bill, table_name='bills')
main()

#print scrape(i2, url="http://www.parliament.nz/en-NZ/PB/Legislation/Bills/c/8/e/00DBHOH_BILL9502_1-Crown-Retail-Deposit-Guarantee-Scheme-Bill.htm")
dud = """<h1></h1>{{ [bills].description }}</p>

<table class="variablelist">
{*
    <tr><th>{{ [bills].[details].name }}</th><td>{{ [bills].[details].link }}</td></tr>
*}
</table>

<div class="infoTiles right">
{* 
    <tr><div class="hdr"></div></tr>
    <tr><li><a href="{{ [bills].[related].link|abs }}">{{ [bills].[related].title }}</a></li></tr> 
*}
</div>
"""
# href="/en-NZ/PB/Legislation/Bills/2/4/f/00DBHOH_BILL9637_1-Accident-Compensation-Amendment-Bill.htm"
#                 <h4><a id="ctl00_ctl00_MainContent_ctl01_rptRecords_lnkTitle_0">[bills].title</a></h4>
#{* <td>{{ [] }}</td> *}
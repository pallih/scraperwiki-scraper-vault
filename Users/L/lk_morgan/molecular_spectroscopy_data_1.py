###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree
import lxml.html
import re

htmlurl=scraperwiki.scrape("http://spec.jpl.nasa.gov/ftp/pub/catalog/catdir.html")
html = lxml.html.fromstring(htmlurl)

text_arr=[]
for el in html.cssselect("div[align='left'] a"):
    text=el.text_content()
    text_arr.append(text)

cat_list=[]
for k in text_arr:
    if k != 'pdf' and k !='Tex': cat_list.append(k)

species_list=[]
for l in cat_list:
    start = l.find('c')
    end = l.find('.cat', start)
    species_list.append(l[start+1:end])

for i in species_list:
#Skip the 055002 and 102002 files for now as they don't follow the regular format, need to fix this at some point
    if i !='055002' and i !='102002':
        print i
        sp_url="http://spec.jpl.nasa.gov/ftp/pub/catalog/doc/d"+i+".pdf"
        url = sp_url

    pdfdata = urllib2.urlopen(url).read()
    xmldata = scraperwiki.pdftoxml(pdfdata,'-hidden')
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)

# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
    def gettext_with_bi_tags(el):
        res = [ ]
        if el.text:
            res.append(el.text)
        for lel in el:
            res.append("<%s>" % lel.tag)
            res.append(gettext_with_bi_tags(lel))
            res.append("</%s>" % lel.tag)
            if el.tail:
                res.append(el.tail)
        return "".join(res)

    row=[]
    pagei=0

    for page in list(pages):
        pagei=pagei+1
        eli=0
        for el in list(page):
            eli=eli+1
            row.append(gettext_with_bi_tags(el))

    try:
        Species_Tagn=row.index('Species Tag:')
        Species=row[Species_Tagn+1]
    except:
        Species='No Info'
    try:
        Namen = row.index('Name:')
        if row[Namen+1] == row[Versionn-1]:Name=row[Namen+1]
        else:Name=row[Namen+1]+row[Versionn-1]
    except:
        Name='No Info'
    Versionn=row.index('Version:')
    Daten=row.index('Date:')
    Q300n=row.index('Q(300.0)=')
    Q225n=row.index('Q(225.0)=')
    Q150n=row.index('Q(150.0)=')
    Q75n=row.index('Q(75.00)=')
    Q37n=row.index('Q(37.50)=')
    Q18n=row.index('Q(18.75)=')
    Q9n=row.index('Q(9.375)=')
    try:
        mu_an=row.index('a')
    except:
        mu_an=row.index('0')
    try:
        mu_bn=row.index('b')
    except:
        mu_bn=row.index(u'\xb5 =')
    try:
        mu_cn=row.index('c')
    except:
        mu_cn=row.index('el')
    maxJn=row.index('Max. J:')
    An=row.index('A=')
    Bn=row.index('B=')
    Cn=row.index('C=')

    State=row[Versionn+2:Daten]
    statn=''
    for j in State:
        statn=statn+' '+j
    if row[An+1] == u'\xb5' or row[An+1] == u'\xb5 =':A='no data'
    else: A=row[An+1]
    if row[Bn+1] == u'\xb5':B='no data'
    else: B=row[Bn+1]
    C_test=row[Cn+1]
    if C_test != '0' or '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9':C='no data'
    else:C=row[Cn+1]
    if row[mu_an+2] != '0' or '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9':mua='no data'
    else: mua=row[mu_an+2]
    if row[mu_bn+2] != '0' or '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9':mub='no data'
    else: mub=row[mu_cn+2]
    if row[mu_cn+2] != '0' or '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9':muc='no data'
    else: muc=row[mu_cn+2]

    scraperwiki.sqlite.save(unique_keys=["Species Tag"],data={"Molecule":Name,"State":statn,"Species Tag":Species,"Max J":row[maxJn+1],"mu a":mua,"mu b":mub,"mu c":muc,"A":A,"B":B,"C":C,"Q300":row[Q300n+1],"Q225":row[Q225n+1],"Q150":row[Q150n+1],"Q75":row[Q75n+1],"Q37":row[Q37n+1],"Q18":row[Q18n+1],"Q9":row[Q9n+1]})
###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree
import lxml.html
import re

htmlurl=scraperwiki.scrape("http://spec.jpl.nasa.gov/ftp/pub/catalog/catdir.html")
html = lxml.html.fromstring(htmlurl)

text_arr=[]
for el in html.cssselect("div[align='left'] a"):
    text=el.text_content()
    text_arr.append(text)

cat_list=[]
for k in text_arr:
    if k != 'pdf' and k !='Tex': cat_list.append(k)

species_list=[]
for l in cat_list:
    start = l.find('c')
    end = l.find('.cat', start)
    species_list.append(l[start+1:end])

for i in species_list:
#Skip the 055002 and 102002 files for now as they don't follow the regular format, need to fix this at some point
    if i !='055002' and i !='102002':
        print i
        sp_url="http://spec.jpl.nasa.gov/ftp/pub/catalog/doc/d"+i+".pdf"
        url = sp_url

    pdfdata = urllib2.urlopen(url).read()
    xmldata = scraperwiki.pdftoxml(pdfdata,'-hidden')
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)

# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
    def gettext_with_bi_tags(el):
        res = [ ]
        if el.text:
            res.append(el.text)
        for lel in el:
            res.append("<%s>" % lel.tag)
            res.append(gettext_with_bi_tags(lel))
            res.append("</%s>" % lel.tag)
            if el.tail:
                res.append(el.tail)
        return "".join(res)

    row=[]
    pagei=0

    for page in list(pages):
        pagei=pagei+1
        eli=0
        for el in list(page):
            eli=eli+1
            row.append(gettext_with_bi_tags(el))

    try:
        Species_Tagn=row.index('Species Tag:')
        Species=row[Species_Tagn+1]
    except:
        Species='No Info'
    try:
        Namen = row.index('Name:')
        if row[Namen+1] == row[Versionn-1]:Name=row[Namen+1]
        else:Name=row[Namen+1]+row[Versionn-1]
    except:
        Name='No Info'
    Versionn=row.index('Version:')
    Daten=row.index('Date:')
    Q300n=row.index('Q(300.0)=')
    Q225n=row.index('Q(225.0)=')
    Q150n=row.index('Q(150.0)=')
    Q75n=row.index('Q(75.00)=')
    Q37n=row.index('Q(37.50)=')
    Q18n=row.index('Q(18.75)=')
    Q9n=row.index('Q(9.375)=')
    try:
        mu_an=row.index('a')
    except:
        mu_an=row.index('0')
    try:
        mu_bn=row.index('b')
    except:
        mu_bn=row.index(u'\xb5 =')
    try:
        mu_cn=row.index('c')
    except:
        mu_cn=row.index('el')
    maxJn=row.index('Max. J:')
    An=row.index('A=')
    Bn=row.index('B=')
    Cn=row.index('C=')

    State=row[Versionn+2:Daten]
    statn=''
    for j in State:
        statn=statn+' '+j
    if row[An+1] == u'\xb5' or row[An+1] == u'\xb5 =':A='no data'
    else: A=row[An+1]
    if row[Bn+1] == u'\xb5':B='no data'
    else: B=row[Bn+1]
    C_test=row[Cn+1]
    if C_test != '0' or '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9':C='no data'
    else:C=row[Cn+1]
    if row[mu_an+2] != '0' or '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9':mua='no data'
    else: mua=row[mu_an+2]
    if row[mu_bn+2] != '0' or '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9':mub='no data'
    else: mub=row[mu_cn+2]
    if row[mu_cn+2] != '0' or '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9':muc='no data'
    else: muc=row[mu_cn+2]

    scraperwiki.sqlite.save(unique_keys=["Species Tag"],data={"Molecule":Name,"State":statn,"Species Tag":Species,"Max J":row[maxJn+1],"mu a":mua,"mu b":mub,"mu c":muc,"A":A,"B":B,"C":C,"Q300":row[Q300n+1],"Q225":row[Q225n+1],"Q150":row[Q150n+1],"Q75":row[Q75n+1],"Q37":row[Q37n+1],"Q18":row[Q18n+1],"Q9":row[Q9n+1]})

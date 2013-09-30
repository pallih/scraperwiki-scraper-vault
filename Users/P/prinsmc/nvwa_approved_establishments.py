# scrape the Dutch EU "Approved Establishments" as listed at http://www.vwa.nl/onderwerpen/english/dossier/approved-establishments1/
import scraperwiki
import os
import tempfile
import re

__TABLE_NAME='ApprovedEstablishments'

def pdftotext(pdfdata):
    """converts pdf file to text"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    textin = tempfile.NamedTemporaryFile(mode='r', suffix='.txt')
    tmptext = textin.name
    cmd = '/usr/bin/pdftotext -layout -enc UTF-8 "%s" "%s"' % (pdffout.name, tmptext)
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    text = textin.read()
    textin.close()
    return text

def cleanupHead(linedata):
    """ cleans up the data by removing the head"""
    for i in range(5,-1,-1):
        del linedata[i]
    return linedata

def cleanupTail(linedata):
    """ cleans up the data by removing the tail"""
    for i in range(0,3):
        del linedata[len(linedata)-1]
    return linedata


#TODO comlete list
__PDF_URLS = [
    #Section 0: General activity establishments
    "http://www3.vwa.nl/EULijst%20SECTION%200-General%20activity%20establishments-Cold%20store%20(Independent,%20stand-alone).pdf",
    #Section I: Meat of domestic ungulates
    "http://www3.vwa.nl/EULijst%20SECTION%20I-Meat%20of%20domestic%20ungulates-Cutting%20plant.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20I-Meat%20of%20domestic%20ungulates-Slaughterhouse.pdf",
    #Section II: Meat from poultry and lagomorphs
    "http://www3.vwa.nl/EULijst%20SECTION%20II-Meat%20from%20poultry%20and%20lagomorphs-Cutting%20plant.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20II-Meat%20from%20poultry%20and%20lagomorphs-Slaughterhouse.pdf",
    #Section III: Meat of farmed game
    "http://www3.vwa.nl/EULijst%20SECTION%20III-Meat%20of%20farmed%20game-Slaughterhouse.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20III-Meat%20of%20farmed%20game-Cutting%20plant.pdf",
    #Section IV: Wild game meat 
    "http://www3.vwa.nl/EULijst%20SECTION%20IV-Wild%20game%20meat-Cutting%20plant.pdf", 
    "http://www3.vwa.nl/EULijst%20SECTION%20IV-Wild%20game%20meat-Game-handling%20establishment.pdf",
    #Section V: Minced meat, meat preperations and mechanically seperated meat 
    "http://www3.vwa.nl/EULijst%20SECTION%20V-Minced%20meat,%20meat%20preparations%20and%20mechanically%20separated%20meat-Meat%20preparation%20establishment.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20V-Minced%20meat,%20meat%20preparations%20and%20mechanically%20separated%20meat-Minced%20meat%20establishment.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20V-Minced%20meat,%20meat%20preparations%20and%20mechanically%20separated%20meat-Mechanically%20separated%20meat%20establishment.pdf",
    #Section VI: Meat products
    "http://www3.vwa.nl/EULijst%20SECTION%20VI-Meat%20products-Processing%20plant.pdf",
    #Section VII: Live bivalve molluscs
    "http://www3.vwa.nl/EULijst%20SECTION%20VII-Live%20bivalve%20molluscs-Dispatch%20centre.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20VII-Live%20bivalve%20molluscs-Purification%20centre.pdf",
    #Section VIII: Fishery products
    "http://www3.vwa.nl/EULijst%20SECTION%20VIII-Fishery%20products-Factory%20vessel.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20VIII-Fishery%20products-Freezing%20vessel.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20VIII-Fishery%20products-Processing%20plant.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20VIII-Fishery%20products-Fresh%20fishery%20products%20plant.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20VIII-Fishery%20products-Wholesale%20market.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20VIII-Fishery%20products-Auction%20hall.pdf",
    #Section IX: Raw milk and dairy products
#TODO http://www.vwa.nl/onderwerpen/english/dossier/approved-establishments1/section-ix-raw-milk-and-dairy-products
    #Section X: Eggs and egg products
#TODO http://www.vwa.nl/onderwerpen/english/dossier/approved-establishments1/section-x-eggs-and-egg-products
    #Section XI: Frogs' legs and snails 
    "http://www3.vwa.nl/EULijst%20SECTION%20XI-Frogs'%20legs%20and%20snails-Processing%20plant.pdf",
    #Section XII: Rendered animal fats and greaves
    "http://www3.vwa.nl/EULijst%20SECTION%20XII-Rendered%20animal%20fats%20and%20greaves-Processing%20plant.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20XII-Rendered%20animal%20fats%20and%20greaves-Collection%20centre.pdf",
    #Section XIII: Treated stomachs, bladders and intestines
    "http://www3.vwa.nl/EULijst%20SECTION%20XIII-Treated%20stomachs,%20bladders%20and%20intestines-Processing%20plant.pdf",
    #Section XIV: Gelatine
    "http://www3.vwa.nl/EULijst%20SECTION%20XIV-Gelatine-Processing%20plant.pdf",
    # skip this, see next section "http://www3.vwa.nl/EULijst%20Collection%20centre-Collagen-Gelatine.pdf",
    #Section XV: Collagen
    "http://www3.vwa.nl/EULijst%20SECTION%20XV-Collagen-Processing%20plant.pdf",
    "http://www3.vwa.nl/EULijst%20Collection%20centre-Collagen-Gelatine.pdf"
    #Export registrations??
    #TODO http://www.vwa.nl/onderwerpen/english/dossier/approved-establishments1/export-registrations
          ]

# remove old data / create table
scraperwiki.sqlite.execute("drop table if exists "+__TABLE_NAME)
scraperwiki.sqlite.execute("create table "+__TABLE_NAME+" (ApprovalNumber int PRIMARY KEY DESC, EstablishmentName string, City string)")

for pdfUrl in __PDF_URLS:
    print "Start processing " + pdfUrl
    txt = pdftotext(scraperwiki.scrape(pdfUrl))

    lines = re.split("\n+", txt)
#    print lines
# lines = cleanupHead(lines)
# lines = cleanupTail(lines)
    count = 0;
    for line in lines:
        est = re.split("\s{2,}",line)
        try:
            if(est[1].isdigit()):
                #only insert valid numbers, this will drop any vessels as well because they start with the hometown code
                scraperwiki.sqlite.execute("insert or replace into "+__TABLE_NAME+" values (?,?,?)", (est[1], est[2], est[3]))
                count += 1
        except IndexError:
            # print 'at least 1 index error is expected'
            pass
    scraperwiki.sqlite.commit()
    print 'Processed %i companies from %s.' % (count ,pdfUrl)


# print scraperwiki.sqlite.select("* from `Approved Establishments`") 

# update adress using OpenKVK

# scrape the Dutch EU "Approved Establishments" as listed at http://www.vwa.nl/onderwerpen/english/dossier/approved-establishments1/
import scraperwiki
import os
import tempfile
import re

__TABLE_NAME='ApprovedEstablishments'

def pdftotext(pdfdata):
    """converts pdf file to text"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    textin = tempfile.NamedTemporaryFile(mode='r', suffix='.txt')
    tmptext = textin.name
    cmd = '/usr/bin/pdftotext -layout -enc UTF-8 "%s" "%s"' % (pdffout.name, tmptext)
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    text = textin.read()
    textin.close()
    return text

def cleanupHead(linedata):
    """ cleans up the data by removing the head"""
    for i in range(5,-1,-1):
        del linedata[i]
    return linedata

def cleanupTail(linedata):
    """ cleans up the data by removing the tail"""
    for i in range(0,3):
        del linedata[len(linedata)-1]
    return linedata


#TODO comlete list
__PDF_URLS = [
    #Section 0: General activity establishments
    "http://www3.vwa.nl/EULijst%20SECTION%200-General%20activity%20establishments-Cold%20store%20(Independent,%20stand-alone).pdf",
    #Section I: Meat of domestic ungulates
    "http://www3.vwa.nl/EULijst%20SECTION%20I-Meat%20of%20domestic%20ungulates-Cutting%20plant.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20I-Meat%20of%20domestic%20ungulates-Slaughterhouse.pdf",
    #Section II: Meat from poultry and lagomorphs
    "http://www3.vwa.nl/EULijst%20SECTION%20II-Meat%20from%20poultry%20and%20lagomorphs-Cutting%20plant.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20II-Meat%20from%20poultry%20and%20lagomorphs-Slaughterhouse.pdf",
    #Section III: Meat of farmed game
    "http://www3.vwa.nl/EULijst%20SECTION%20III-Meat%20of%20farmed%20game-Slaughterhouse.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20III-Meat%20of%20farmed%20game-Cutting%20plant.pdf",
    #Section IV: Wild game meat 
    "http://www3.vwa.nl/EULijst%20SECTION%20IV-Wild%20game%20meat-Cutting%20plant.pdf", 
    "http://www3.vwa.nl/EULijst%20SECTION%20IV-Wild%20game%20meat-Game-handling%20establishment.pdf",
    #Section V: Minced meat, meat preperations and mechanically seperated meat 
    "http://www3.vwa.nl/EULijst%20SECTION%20V-Minced%20meat,%20meat%20preparations%20and%20mechanically%20separated%20meat-Meat%20preparation%20establishment.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20V-Minced%20meat,%20meat%20preparations%20and%20mechanically%20separated%20meat-Minced%20meat%20establishment.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20V-Minced%20meat,%20meat%20preparations%20and%20mechanically%20separated%20meat-Mechanically%20separated%20meat%20establishment.pdf",
    #Section VI: Meat products
    "http://www3.vwa.nl/EULijst%20SECTION%20VI-Meat%20products-Processing%20plant.pdf",
    #Section VII: Live bivalve molluscs
    "http://www3.vwa.nl/EULijst%20SECTION%20VII-Live%20bivalve%20molluscs-Dispatch%20centre.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20VII-Live%20bivalve%20molluscs-Purification%20centre.pdf",
    #Section VIII: Fishery products
    "http://www3.vwa.nl/EULijst%20SECTION%20VIII-Fishery%20products-Factory%20vessel.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20VIII-Fishery%20products-Freezing%20vessel.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20VIII-Fishery%20products-Processing%20plant.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20VIII-Fishery%20products-Fresh%20fishery%20products%20plant.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20VIII-Fishery%20products-Wholesale%20market.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20VIII-Fishery%20products-Auction%20hall.pdf",
    #Section IX: Raw milk and dairy products
#TODO http://www.vwa.nl/onderwerpen/english/dossier/approved-establishments1/section-ix-raw-milk-and-dairy-products
    #Section X: Eggs and egg products
#TODO http://www.vwa.nl/onderwerpen/english/dossier/approved-establishments1/section-x-eggs-and-egg-products
    #Section XI: Frogs' legs and snails 
    "http://www3.vwa.nl/EULijst%20SECTION%20XI-Frogs'%20legs%20and%20snails-Processing%20plant.pdf",
    #Section XII: Rendered animal fats and greaves
    "http://www3.vwa.nl/EULijst%20SECTION%20XII-Rendered%20animal%20fats%20and%20greaves-Processing%20plant.pdf",
    "http://www3.vwa.nl/EULijst%20SECTION%20XII-Rendered%20animal%20fats%20and%20greaves-Collection%20centre.pdf",
    #Section XIII: Treated stomachs, bladders and intestines
    "http://www3.vwa.nl/EULijst%20SECTION%20XIII-Treated%20stomachs,%20bladders%20and%20intestines-Processing%20plant.pdf",
    #Section XIV: Gelatine
    "http://www3.vwa.nl/EULijst%20SECTION%20XIV-Gelatine-Processing%20plant.pdf",
    # skip this, see next section "http://www3.vwa.nl/EULijst%20Collection%20centre-Collagen-Gelatine.pdf",
    #Section XV: Collagen
    "http://www3.vwa.nl/EULijst%20SECTION%20XV-Collagen-Processing%20plant.pdf",
    "http://www3.vwa.nl/EULijst%20Collection%20centre-Collagen-Gelatine.pdf"
    #Export registrations??
    #TODO http://www.vwa.nl/onderwerpen/english/dossier/approved-establishments1/export-registrations
          ]

# remove old data / create table
scraperwiki.sqlite.execute("drop table if exists "+__TABLE_NAME)
scraperwiki.sqlite.execute("create table "+__TABLE_NAME+" (ApprovalNumber int PRIMARY KEY DESC, EstablishmentName string, City string)")

for pdfUrl in __PDF_URLS:
    print "Start processing " + pdfUrl
    txt = pdftotext(scraperwiki.scrape(pdfUrl))

    lines = re.split("\n+", txt)
#    print lines
# lines = cleanupHead(lines)
# lines = cleanupTail(lines)
    count = 0;
    for line in lines:
        est = re.split("\s{2,}",line)
        try:
            if(est[1].isdigit()):
                #only insert valid numbers, this will drop any vessels as well because they start with the hometown code
                scraperwiki.sqlite.execute("insert or replace into "+__TABLE_NAME+" values (?,?,?)", (est[1], est[2], est[3]))
                count += 1
        except IndexError:
            # print 'at least 1 index error is expected'
            pass
    scraperwiki.sqlite.commit()
    print 'Processed %i companies from %s.' % (count ,pdfUrl)


# print scraperwiki.sqlite.select("* from `Approved Establishments`") 

# update adress using OpenKVK


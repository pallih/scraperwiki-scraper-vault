##import scraperwiki, simplejson, urllib, re
import scraperwiki, simplejson, urllib
import sys, time

##  PENDING:  clear any old data
##  scraperwiki.sqlite.execute("drop table if exists csp")

##  set private API key
##import os, cgi
##try:
##    q1 = os.getenv('OCKEY')
##    print q1
##    q2 = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
##    print q2
##    ockey=q2["OCKEY"]
##    print ockey
##except:
##    ockey=''
##sys.exit(0)
ockey='tgcvauZDsCvecvk5o9y2'

##rurl='http://api.opencorporates.com/v0.2/companies/search?q=&api_token='+ockey+'&sparse=true&per_page=50&page=9&jurisdiction_code=im&current_status=Live'
##ocentities=simplejson.load(urllib.urlopen(rurl))
##c1=ocentities['results']['total_pages']
##c2=len(ocentities['results']['companies'])
##print 'c1: ',c1
##print 'c2: ',c2
##print ocentities
##entity=ocentities['results']['companies'][42]
##ocjurisdiction=entity['company']['jurisdiction_code']
##ocreference=entity['company']['company_number']
##ocname=entity['company']['name']
##ocurl='http://api.opencorporates.com/v0.2/companies/'+ocjurisdiction+'/'+ocreference+'?api_token='+ockey+'&sparse=true'
##ocdata=simplejson.load(urllib.urlopen(ocurl))
##ocaddress=ocdata['results']['company']['registered_address_in_full']
##print ocreference+': '+ocname+' @ '+ocaddress
##sys.exit(0)

##  http://api.opencorporates.com/documentation/API-Reference
##  The search is deliberately quite loose, requiring the returned companies to
##  have all the searched-for words (in any order), but allowing other words to
##  be present too, so 'Bank Barclays' is the same as 'Barclays Bank'.
##  The search is case-insensitive and returns companies with previous names
##  matching the term as well as current name, and some normalisation of the
##  company names is done, removing non-text characters (e.g. dashes, parentheses,
##  commas), common 'stop words' (e.g. 'the', 'of'), and normalising common company
##  types (e.g. Corp, Inc, Ltd, PLC) to support short and long versions.
##      REVIEW THE PREFIX:  THE OLD COURTHOUSE TO OLD COURTHOUSE
##      REVIEW STREET NUMBERS IN TEXT: ONE THE PARADE, SIXTY CIRCULAR ROAD
##      REVIEW FLOOR REFERENCES IN TEXT/ABBREVIATIONS:  SIXTH FLOOR, 2ND FLR, FLOOR 3
##      REVIEW HOUSE REFERENCE ABBREVIATION: HSE TO HOUSE
##          ANGLO INTERNATIONAL HSE
def Filter1(temp1):
    ##  upper case
    temp2=temp1.upper()
    ##  spaces
    temp2=temp2.replace(" ","")
    ##  commas
    temp2=temp2.replace(",","")
    ##  full stops
    temp2=temp2.replace(".","")
    ## dashes: for example, 12-14
    temp2=temp2.replace("-","")
    ## slashes: for example, 35/37
    temp2=temp2.replace("/","")
    ##  apostrophes and quotes
    temp2=temp2.replace("'","")
    temp2=temp2.replace("`","")
    temp2=temp2.replace('"',"")
    ## ampersands
    temp2=temp2.replace("&","AND")
    ##  floors - FIRST, SECOND, THIRD, TOP
    temp2=temp2.replace("FIRSTFLOOR","1STFLOOR")
    temp2=temp2.replace("SECONDFLOOR","2NDFLOOR")
    temp2=temp2.replace("THIRDFLOOR","3RDFLOOR")
    ##  inconsistent addresses
    temp2=temp2.replace("ISLEOFMAN","")
    temp2=temp2.replace("UNITEDKINGDOM","")
    temp2=temp2.replace("ONECIRCULARROAD","1CIRCULARROAD")
    temp2=temp2.replace("SIXTYCIRCULARROAD","60CIRCULARROAD")
    temp2=temp2.replace("NUMBERFIFTYATHOLSTREET","50ATHOLSTREET")
    temp2=temp2.replace("VICTORIAHSE","VICTORIAHOUSE")
    temp2=temp2.replace("CHESTERFIELDHSE","CHESTERFIELDHOUSE")
    ##  any temporary fixes - minor typos
    temp2=temp2.replace("[","")
    temp2=temp2.replace("#","")
    return temp2

##  PENDING: IOM BUSINESS NAMES IN OC

##  ISLE OF MAN
##  180 corporate licenceholders with 2 in liquidation and 14 personal licenceholders
##  http://www.gov.im/fsc/licenceholders/SearchLicenceHolders.aspx?type=Current&id=1
csp1=[]
csp2=[]
csp1.append(Filter1('Abacus Financial Services Limited'))
  ##  not listed in OC - peviously ABACUS INVESTMENT MANAGEMENT LIMITED
csp2.append(Filter1('2nd Floor, 60 Circular Road, Douglas'))
csp1.append(Filter1('Abacus Trust Company Limited'))
  ##  T/A Abacus Yachts and Abacus Aviation
csp2.append(Filter1('2nd Floor, Sixty Circular Road Douglas IM1 1SA'))
csp1.append(Filter1('Acclaim Limited'))
  ##  also at same address ACCLAIM EGAMING SERVICES LIMTIED
  ##  also at same address ACCLAIM PROPERTIES LIMTIED
csp2.append(Filter1('12 Mount Havelock, Douglas, IM1 2QG'))
csp1.append(Filter1('ACTIVE SERVICES LIMITED'))
  ##  also at same address ACTIVE SERVICES (IOM) LIMITED
csp2.append(Filter1('64a-65 Athol Street, Douglas, IM1 1JE'))
csp1.append(Filter1('AFFINITY MANAGEMENT SERVICES LIMITED'))
  ##  previously Simcocks Yacht and Aircraft Management Limited
csp2.append(Filter1('First Floor, 14 Athol Street, Douglas, IM1 1JA'))
csp1.append(Filter1('ALLIED DUNBAR INTERNATIONAL FUND MANAGERS LIMITED'))
  ##  not listed in OC - previously ALLIED HAMBRO INTERNATIONAL FUND MANAGERS LIMITED
csp2.append(Filter1('43-51 Athol Street, Douglas, IM99 1ET'))
csp1.append(Filter1('AMBER BUSINESS LIMITED'))
csp2.append(Filter1('Royal Trust House, 60 Athol Street , Douglas, IM1 1JD'))
csp1.append(Filter1('ANDCO CORPORATE SERVICES LIMITED'))
csp2.append(Filter1('13 PEEL ROAD, DOUGLAS, IM1 4LR'))
csp1.append(Filter1('ANGLO MANX TRUST COMPANY LIMITED'))
  ##  not listed in OC - previously ANGLO MANX TRUST CORPORATION LIMITED
csp2.append(Filter1('5 Athol Street, Douglas'))
csp1.append(Filter1('AON CORPORATE SERVICES (ISLE OF MAN) LIMITED'))
csp2.append(Filter1('Third Floor, St Georges Court, Upper Church Street, Douglas, IM1 1EE'))
csp1.append(Filter1('APEX FUND SERVICES (IOM) LTD'))
csp2.append(Filter1('EXCHANGE HOUSE, 54-58 ATHOL STREET, DOUGLAS, IM1 1JD'))
csp1.append(Filter1('APPLEBY TRUST (ISLE OF MAN) LIMITED'))
csp2.append(Filter1('33/37 Athol Street, Douglas, IM1 1LB'))
csp1.append(Filter1('ARDENT FUND SOLUTIONS LIMITED'))
csp2.append(Filter1('6 Hope Street, Castletown, IM9 1AS'))
csp1.append(Filter1('ASHGROVES CORPORATE SERVICES LIMITED'))
csp2.append(Filter1('14 ALBERT STREET, DOUGLAS, IM1 2QA'))
csp1.append(Filter1('ASTON INTERNATIONAL LIMITED'))
csp2.append(Filter1('ASTON HOUSE, 19 PEEL ROAD, DOUGLAS, IM1 4LS'))
csp1.append(Filter1('ATLAS CORPORATE SERVICES LIMITED'))
csp2.append(Filter1('Stanley House, Lord Street, Douglas, IM1 2BF'))
csp1.append(Filter1('AXIS COMPANY SERVICES LIMITED'))
csp2.append(Filter1('59 Ballagarey Road, Glen Vine'))
csp1.append(Filter1('BAKER TILLY ISLE OF MAN FIDUCIARIES LIMITED'))
csp2.append(Filter1('P O Box 95, 2A Lord Street, Douglas, IM99 1HP'))
csp1.append(Filter1('BARCLAYS PRIVATE BANK & TRUST (ISLE OF MAN) LIMITED'))
  ##  not listed in OC - previously BARCLAYTRUST INTERNATIONAL (ISLE OF MAN) LIMITED
csp2.append(Filter1('3rd Floor, Barclays House, Victoria Street, Douglas, IM1 2LE'))
csp1.append(Filter1('BARCLAYS WEALTH TRUSTEES (ISLE OF MAN) LIMITED'))
csp2.append(Filter1('PO Box 312 4th Floor, Queen Victoria House, Victoria Street Douglas, IM99 2BJ'))
csp1.append(Filter1('BLUE SEA INTERNATIONAL LIMITED'))
csp2.append(Filter1('31-37 North Quay, Douglas, IM1 4LB'))
csp1.append(Filter1('BOSTON LIMITED'))
  ##  T/A BOSTON TRUST COMPANY
csp2.append(Filter1('Belgravia House, 34-44 Circular Road, Douglas, IM1 1AE'))
  ##  T/A BRIDGEWATERS
csp1.append(Filter1('BRIDGEWATER (IOM) LIMITED'))
csp2.append(Filter1('Victoria House, 26 Victoria Street, Douglas, IM1 2LE'))
csp1.append(Filter1('BW OAKFIELD LIMITED'))
csp2.append(Filter1('MILLENNIUM HOUSE, VICTORIA ROAD, DOUGLAS, IM2 4RW'))
csp1.append(Filter1('CADOGAN TRUST LIMITED'))
csp2.append(Filter1('33-35 Victoria Street, Douglas, IM1 2LF'))
csp1.append(Filter1('CAINS FIDUCIARIES LIMITED'))
csp2.append(Filter1('Fort Anne, Douglas, IM1 5PD'))
csp1.append(Filter1('CALEDONIAN FUND SERVICES (EUROPE) LIMITED'))
csp2.append(Filter1('PO Box 172 4th Floor, One Circular Road, Douglas, IM99 3PA'))
csp1.append(Filter1('CALEDONIAN TRUST (IOM) LIMITED'))
csp2.append(Filter1('PO Box 166, 4th Floor, One Circular Road, Douglas, IM99 3NZ'))
csp1.append(Filter1('CALLOW MATTHEWMAN (CSP) LIMITED'))
csp2.append(Filter1('Atholl House, 29-31 Hope Street, Douglas, IM1 1AR'))
csp1.append(Filter1('CAPITA REGISTRARS (ISLE OF MAN) LIMITED'))
csp2.append(Filter1('3RD FLOOR EXCHANGE HOUSE, 54-62 ATHOL STREET, DOUGLAS, IM1 1JD'))
csp1.append(Filter1('CAPITAL FUND SERVICES LIMITED'))
  ##  not listed in OC - previously ABM CORPORATE SERVICES LIMITED
csp2.append(Filter1('Capital House, Circular Road, Douglas IM1 1AG'))
csp1.append(Filter1('CAPRICORN MANAGEMENT SERVICES LIMITED'))
csp2.append(Filter1('Newcourt Chambers, 39 Bucks Road, Douglas, IM1 3DE'))
csp1.append(Filter1('CAVENDISH TRUST COMPANY LIMITED'))
csp2.append(Filter1('31-37 NORTH QUAY, DOUGLAS, IM1 4LB'))
csp1.append(Filter1('CAYMAN NATIONAL BANK & TRUST COMPANY (ISLE OF MAN) LIMITED'))
  ##  not listed in OC - previously CAYMANX TRUST COMPANY LIMITED
csp2.append(Filter1('Cayman National House, 4-8 Hope Street, Douglas, IM1 1AQ'))
##  -- DUPLICATE ADDRESS --
##  csp1.append(Filter1('CAYMAN NATIONAL FUND SERVICES (ISLE OF MAN) LIMITED'))
##  csp2.append(Filter1('Cayman National House, 4-8 Hope Street, Douglas, IM1 1AQ'))
csp1.append(Filter1('CCW TRUST LIMITED'))
  ##  not listed in OC - previously HCW FIDUCIAIRE LIMITED
csp2.append(Filter1('6TH FLOOR, VICTORY HOUSE, PROSPECT HILL, DOUGLAS, IM1 1EQ'))
csp1.append(Filter1('CELTIC ASSOCIATES LIMITED'))
csp2.append(Filter1('The Red House, One The Parade, Castletown, IM9 1LG'))
csp1.append(Filter1('CENTRAL CORPORATE SERVICES LIMITED'))
csp2.append(Filter1('6 Victoria Street, Douglas'))
csp1.append(Filter1('CHAMBERLAIN FUND SERVICES LIMITED'))
csp2.append(Filter1('Third Floor, Exchange House, 54-62 Athol Street, Douglas, IM1 1JD'))
csp1.append(Filter1('CHAN FIDUCIARY LIMITED'))
  ##  not listed in OC - previously CHAN CORPORATE SERVICES LIMITED
csp2.append(Filter1('Bridge House, Bridge Street, Castletown'))
csp1.append(Filter1('CHANCERY TRUST COMPANY LIMITED'))
  ##  T/A DFK CHANCERY TRUST
csp2.append(Filter1('First Floor, East Wing, Shearwater House, Nunnery Mills , Old Castletown Road'))
csp1.append(Filter1('CHARLEMAGNE CAPITAL (IOM) LIMITED'))
csp2.append(Filter1('St Marys Court, 20 Hill Street, Douglas, IM1 1EU'))
  ##  -- APOSTROPHE --
  ##  St Mary's Court, 20 Hill Street, Douglas, IM1 1EU
csp1.append(Filter1('CHARTERHOUSE LOMBARD LIMITED'))
  ##  not listed in OC - previously CHARTERHOUSE TRUST COMPANY LIMITED
csp2.append(Filter1('1st Floor, Viking House, St Pauls Square, Ramsey, IM8 1GB'))
  ##  -- APOSTROPHE --
  ##  1st Floor, Viking House, St Paul's Square, Ramsey, IM8 1GB
csp1.append(Filter1('CHESTERFIELD FALCON LIMITED'))
  ##  -- Hse abbreviation of House --
csp2.append(Filter1('Chesterfield Suite, Chesterfield Hse, 11-13 Victoria St, Douglas'))
csp1.append(Filter1('CITY TRUST LIMITED'))
csp2.append(Filter1('First Floor, Ragnall House, Peel Road, Douglas, IM1 4LZ'))
  ##  18 PEEL ROAD
##  -- DUPLICATE ADDRESS --
##  csp1.append(Filter1('CLEARWATER FIDUCIARY SERVICES LIMITED'))
##  csp2.append(Filter1('1ST FLOOR, RAGNALL HOUSE, 18 PEEL ROAD, DOUGLAS, IM1 4LZ'))
csp1.append(Filter1('CM MANAGEMENT (IOM) LIMITED'))
  ##  not listed in OC - previously CM SKYEFID LIMITED
csp2.append(Filter1('Commerce House, 1 Bowring Road, Ramsey IM8 2LQ'))
csp1.append(Filter1('CMI FUND MANAGERS (IOM) LIMITED'))
csp2.append(Filter1('Clerical Medical House, Victoria Road, Douglas'))
csp1.append(Filter1('COLAW INTERNATIONAL LIMITED'))
csp2.append(Filter1('Chancery House, 22 Finch Road, Douglas, IM1 2PT'))
csp1.append(Filter1('COMPUTERSHARE INVESTOR SERVICES (IOM) LIMITED'))
csp2.append(Filter1('INTERNATIONAL HOUSE, CASTLE HILL, VICTORIA ROAD, DOUGLAS, IM2 4RB'))
csp1.append(Filter1('CORLETT BOLTON ADMINISTRATION SERVICES LIMITED'))
  ##  not listed in OC - previously AUDEN LIMITED
csp2.append(Filter1('4 FINCH ROAD, DOUGLAS, IM1 2PT'))
csp1.append(Filter1('CORPORATE MANAGEMENT & BUSINESS SERVICES LIMITED'))
csp2.append(Filter1('The Old Courthouse, Athol Street, Douglas,  IM1 1LD'))
csp1.append(Filter1('CORPORATE OPTIONS LIMITED'))
  ##  T/A CORPORATE OPTIONS
csp2.append(Filter1('37 Hope Street, Douglas, IM1 1AR'))
csp1.append(Filter1('CROSSMAN TRUST COMPANY LIMITED'))
csp2.append(Filter1('P O Box 1, Portland House, Station Road, Ballasalla, IM99 6AB'))
csp1.append(Filter1('CROWE MORGAN MANAGEMENT LIMITED'))
  ##  not listed in OC - previously ST. GEORGE'S MANAGEMENT LIMITED
csp2.append(Filter1('8 St Georges Street, Douglas, IM1 1AH'))
  ##  -- APOSTROPHE --
  ##  8 St George's Street, Douglas, IM1 1AH
csp1.append(Filter1('CW CORPORATE SERVICES LIMITED'))
csp2.append(Filter1('50 Athol Street, Douglas, IM1 1JE'))
csp1.append(Filter1('DBAY ADVISORS LIMITED'))
csp2.append(Filter1('4TH FLOOR DERBY HOUSE, 64 ATHOL STREET, DOUGLAS, IM1 1JD'))
csp1.append(Filter1('DELPHI TRUST LIMITED'))
csp2.append(Filter1('16 ST GEORGES STREET, DOUGLAS, IM1 1PL'))
csp1.append(Filter1('DEVONSHIRE CORPORATE SERVICES LIMITED'))
csp2.append(Filter1('15 St Georges Street, Douglas'))
csp1.append(Filter1('DIXCART GLOBAL FUND MANAGERS LIMITED'))
csp2.append(Filter1('69 Athol Street, Douglas, IM1 1JE'))
##  -- DUPLICATE ADDRESS --
##  csp1.append(Filter1('DIXCART MANAGEMENT (IOM) LIMITED'))
##  csp2.append(Filter1('69 Athol Street, Douglas, IM1 1JE'))
csp1.append(Filter1('DOHLE CORPORATE AND TRUST SERVICES LIMITED'))
  ##  T/A CORSIOM
  ##  not listed in OC - previously CORSIOM LIMITED
csp2.append(Filter1('FORT ANNE, SOUTH QUAY, DOUGLAS, IM1 5PD'))
csp1.append(Filter1('DOLMEN FIDUCIARY SERVICES LIMITED'))
csp2.append(Filter1('16 HOPE STREET, DOUGLAS, IM1 1AQ'))
csp1.append(Filter1('DOMINION MARINE CORPORATE SERVICES LIMITED'))
csp2.append(Filter1('Prospect Chambers, Prospect Hill, Douglas'))
csp1.append(Filter1('DOUGLAS AVIATION (ISLE OF MAN) LIMITED'))
csp2.append(Filter1('Penthouse Suite, Analysts House, Douglas, IM1 4LZ'))
##  -- DUPLICATE ADDRESS --
##  csp1.append(Filter1('DOUGLAS TRUSTEES LIMITED'))
##  csp2.append(Filter1('16 St Georges Street, Douglas'))
csp1.append(Filter1('DUNCAN LAWRIE (IOM) LIMITED'))
csp2.append(Filter1('14/15 Mount Havelock, Douglas'))
##  -- DUPLICATE ADDRESS --
##  csp1.append(Filter1('DUNCAN LAWRIE OFFSHORE SERVICES LIMITED'))
##  csp2.append(Filter1('14/15 Mount Havelock, Douglas'))
csp1.append(Filter1('E OPPENHEIMER & SON (IOM) LIMITED'))
  ##  not listed on OC - previously EOS SERVICES LIMITED
csp2.append(Filter1('Tyndall House, 77-79 Bucks Road, Douglas IM1 3EF'))
csp1.append(Filter1('EQUIOM (ISLE OF MAN) LIMITED'))
  ##  not listed in OC - previously EQUIOM TRUST COMPANY LIMITED
csp2.append(Filter1('FIRST FLOOR, JUBILEE BUILDINGS, VICTORIA STREET, DOUGLAS, IM1 2SH'))
csp1.append(Filter1('FEDELTA TRUST LIMITED'))
csp2.append(Filter1('29/31 Athol Street, Douglas, IM1 1LB'))
csp1.append(Filter1('FIDUCS LIMITED'))
csp2.append(Filter1('Theakstons, Regaby, IM7 3HL'))
##  -- DUPLICATE ADDRESS --
##  csp1.append(Filter1('FIRST NAMES (ISLE OF MAN) LIMITED'))
##    not listed in OC - previously IFG INTERNATIONAL LIMITED
##  csp2.append(Filter1('International House, Castle Hill, Victoria Road, Douglas'))
##  -- DUPLICATE ADDRESS --
##  csp1.append(Filter1('FIRST NATIONAL TRUSTEE COMPANY LIMITED'))
##  csp2.append(Filter1('International House, Castle Hill Victoria Road, Douglas'))
csp1.append(Filter1('FISCAL SERVICES LIMITED'))
csp2.append(Filter1('7 Hill Street, Douglas, IM1 1EF'))
csp1.append(Filter1('FORTRESS MANAGEMENT SERVICES LIMITED'))
csp2.append(Filter1('4th Floor, Exchange House, 54-58 Athol Street, Douglas, IM1 1JD'))
csp1.append(Filter1('FRANK SCOTT LIMITED'))
csp2.append(Filter1('Third Floor, Exchange House, 54-58 Athol Street, Douglas, IM1 1JD'))
csp1.append(Filter1('FREELANCE PROFESSIONAL SERVICES LIMITED'))
csp2.append(Filter1('Viking House, St Pauls Square, Ramsey, IM8 1GB'))
  ##  -- APOSTROPHE --
  ##  Viking House, St Paul's Square, Ramsey, IM8 1GB
csp1.append(Filter1('FREEPORT TRUST COMPANY LIMITED'))
csp2.append(Filter1('4 Athol Street, Douglas'))
csp1.append(Filter1('FRIABEL LIMITED'))
csp2.append(Filter1('27 Athol Street, Douglas, IM1 1LB'))
csp1.append(Filter1('FULCRUM LIMITED'))
csp2.append(Filter1('PO Box 1, Portland House, Station Road, Ballasalla, IM99 6AB'))
csp1.append(Filter1('GALILEO FUND SERVICES LIMITED'))
  ##  not listed in OC - previously ANGLO IRISH FUND SERVICES LIMITED
csp2.append(Filter1('Millennium House, 46 Athol Street, Douglas IM1 1JB'))
csp1.append(Filter1('GECKO CORPORATE SERVICES LIMITED'))
csp2.append(Filter1('1 Dale Street, Ramsey, IM8 1BJ'))
csp1.append(Filter1('GEORGE COCHRAN NOBLE'))
  ##  T/A NOBLE & CO
  ##  -- BUSINESS NAMES EXCLUDED --
  ##  not listed in OC - business names excluded
csp2.append(Filter1('ABACUS HOUSE, MONA STREET, DOUGLAS IM1 3AE'))
csp1.append(Filter1('GLAISDALE MANAGEMENT LIMITED'))
  ##  not listed in OC - previously EMBLA MANAGEMENT LIMITED
csp2.append(Filter1('MANNING HOUSE, 21 BUCKS ROAD, DOUGLAS IM1 3DA'))
csp1.append(Filter1('GRANT THORNTON (ISLE OF MAN) LIMITED'))
  ##  not listed in OC - previously READS (ISLE OF MAN) LIMITED
csp2.append(Filter1('Third Floor, Exchange House, 54-58 Athol Street, Douglas, IM1 1JD'))
csp1.append(Filter1('GREYSTONE TRUST COMPANY LIMITED'))
csp2.append(Filter1('18 Athol Street, Douglas, IM1 1JA'))
csp1.append(Filter1('HAMELS (ISLE OF MAN) LIMITED'))
csp2.append(Filter1('9 Circular Road, Douglas, IM1 1AF'))
csp1.append(Filter1('HILL ROBINSON LIMITED'))
csp2.append(Filter1('Prospect Chambers, Prospect Hill, Douglas'))
csp1.append(Filter1('HILLBERRY TRUST COMPANY LIMITED'))
csp2.append(Filter1('GROUND FLOOR, WEST SUITE, EXCHANGE HOUSE, 54-58 ATHOL STREET, DOUGLAS, IM1 1JD'))
csp1.append(Filter1('HL FIDUCIARIES LIMITED'))
csp2.append(Filter1('34 Athol Street, Douglas, IM1 1JB'))
csp1.append(Filter1('IBRC TRUST (IOM) LIMITED'))
  ##  not listed in OC - previously ANGLO IRISH TRUST (IOM) LIMITED
csp2.append(Filter1('Third Floor, Jubilee Buildings, Victoria Street, Douglas IM1 2SH'))
csp1.append(Filter1('ILS FIDUCIARIES (IOM) LIMITED'))
  ##  ALSO T/A M & P CORPORATE SERVICES
  ##  not listed in OC - previously ILS (ISLE OF MAN) LIMITED
csp2.append(Filter1('FIRST FLOOR, MILLENNIUM HOUSE, VICTORIA ROAD, DOUGLAS, IM2 4RW'))
csp1.append(Filter1('INTEGRATED-CAPABILITIES LTD'))
csp2.append(Filter1('Second Floor, Bourne Concourse, Peel Street, Ramsey, IM8 1JJ'))
csp1.append(Filter1('INTER-CONTINENTAL MANAGEMENT LIMITED'))
  ##  T/A ICM WEALTH MANAGEMENT AND ICM AVIATION
csp2.append(Filter1('PROSPECT CHAMBERS, PROSPECT HILL, DOUGLAS, IM1 1ET'))
csp1.append(Filter1('INTRUST (MANX) LIMITED'))
csp2.append(Filter1('1st Floor, 29-33 Bucks Road, Douglas, IM1 3DE'))
csp1.append(Filter1('IOM CORPORATE SOLUTIONS LIMITED'))
csp2.append(Filter1('2nd Floor, Exchange House, 54/58 Athol Street, Douglas, IM1 1JD'))
csp1.append(Filter1('IOMA FUND AND INVESTMENT MANAGEMENT LIMITED'))
  ##  T/A IOMA FUND MANAGEMENT AND IOMA INVESTMENT MANANGEMENT
csp2.append(Filter1('IOMA House, Hope Street, Douglas, IM1 1AP'))
csp1.append(Filter1('IQE LIMITED'))
  ##  previously SIMCOCKS TRUST LIMITED
csp2.append(Filter1('Top Floor, 14 Athol Street, Douglas, IM1 1JA'))
  ##  T/A IOMA FIDUCIARY
csp1.append(Filter1('ISLE OF MAN FINANCIAL TRUST LIMITED'))
csp2.append(Filter1('Hope Street, Douglas, IM1 1AP'))
csp1.append(Filter1('JEFFCOTE DONNISON (OVERSEAS) LIMITED'))
csp2.append(Filter1('Exchange House, First Floor, 54/58 Athol Street, Douglas, IM1 1JD'))
csp1.append(Filter1('JESSUP LIMITED'))
csp2.append(Filter1('44 Athol Street, Douglas, IM1 1JB'))
csp1.append(Filter1('JPS CONSULTANCY SERVICES LIMITED'))
csp2.append(Filter1('Glen Eagles House, Mountain Road, Douglas, IM2 6DG'))
csp1.append(Filter1('JURISTRUST LIMITED'))
csp2.append(Filter1('Ridgeway House, Ridgeway Street, Douglas, IM99 1PY'))
csp1.append(Filter1('KELLADALE LIMITED'))
  ##  not listed in OC - original corporate name
csp2.append(Filter1('Milbourn House, St. Georges Street, Douglas IM1 1AJ'))
  ##  -- APOSTROPHE AND FULL STOP ABBREVIATION --
  ##  Milbourn House, St. George's Street, Douglas IM1 1AJ
csp1.append(Filter1('KERRUISH TRUST LLC'))
  ##  T/A KERRUISH LAW AND TRUST
  ##  not listed in OC - previously GOUGH FIDUCIARY LLC
csp2.append(Filter1('5TH FLOOR, ANGLO INTERNATIONAL HOUSE, BANK HILL, NORTH QUAY, DOUGLAS, IM1 4QE'))
csp1.append(Filter1('KINGSTON MANAGEMENT (ISLE OF MAN) LIMITED'))
csp2.append(Filter1('1st Floor, Ragnall House, 18 Peel Road, Douglas'))
csp1.append(Filter1('KLEINWORT BENSON TRUSTEES (ISLE OF MAN) LIMITED'))
  ##  not listed in OC - previously CLOSE TRUSTEES (ISLE OF MAN) LIMITED
csp2.append(Filter1('St Georges Court, Upper Church Street, Douglas IM1 1EE'))
  ##  -- APOSTROPHE --
  ##  St George's Court, Upper Church Street, Douglas IM1 1EE
csp1.append(Filter1('KNOX DARCY ASSET MANAGEMENT LIMITED'))
  ##  -- APOSTROPHE --
  ##  KNOX D'ARCY ASSET MANAGEMENT LIMITED
csp2.append(Filter1('14 Athol Street, Douglas, IM1 1AJ'))
csp1.append(Filter1('KNOX HOUSE TRUST LIMITED'))
csp2.append(Filter1('Knox House, 16-18 Finch Road, Douglas'))
csp1.append(Filter1('KSI HAWK LIMITED'))
  ##  not listed in OC - previously KSI HAWK MANAGEMENT LIMITED
csp2.append(Filter1('Swan House, 33 Hope Street, Castletown IM9 1AP'))
csp1.append(Filter1('LAXEY PARTNERS LTD'))
csp2.append(Filter1('4th Floor, Derby House, 64 Athol Street, Douglas, IM1 1JD'))
csp1.append(Filter1('LEINSTER MANAGEMENT LIMITED'))
csp2.append(Filter1('Alma House, 7 Circular Road, Douglas, IM1 1AF'))
csp1.append(Filter1('LK (FIDUCIARIES) LIMITED'))
  ##  not listed in OC - previously CHARTSIDE LIMITED
csp2.append(Filter1('47 Victoria Street, Douglas'))
csp1.append(Filter1('MAITLAND SERVICES LIMITED'))
csp2.append(Filter1('Falcon Cliff, Palace Road, Douglas'))
csp1.append(Filter1('MANN MADE CORPORATE SERVICES LIMITED'))
  ##  not listed in OC - previously MANN MADE ENTERPRISES LIMITED
csp2.append(Filter1('19-21 Circular Road, Douglas, IM1 1AF'))
csp1.append(Filter1('MANNBENHAM FIDUCIARIES LIMITED'))
  ##  not listed in OC - previously MANNBENHAM CORPORATE SERVICE PROVIDERS LIMITED
csp2.append(Filter1('49 Victoria Street, Douglas, IM1 2LD'))
csp1.append(Filter1('MANNTAX C.S.P. LIMITED'))
csp2.append(Filter1('8a The Village Walk, Onchan, IM3 4EA'))
csp1.append(Filter1('MARINE SERVICES (I.O.M.) LIMITED'))
csp2.append(Filter1('St. Georges Court, Upper Church Street, Douglas, IM1 1EE'))
  ##  -- APOSTROPHE AND FULL STOP ABBREVIATION --
  ##  St. George's Court, Upper Church Street, Douglas, IM1 1EE
csp1.append(Filter1('MARSH CORPORATE SERVICES ISLE OF MAN LIMITED'))
  ##  not listed in OC - previously SEDGWICK (ISLE OF MAN) LIMITED
csp2.append(Filter1('1st Floor, Rose House, 51-59 Circular Road, Douglas, IM1 1RE'))
csp1.append(Filter1('MERRILL LYNCH BANK & TRUST COMPANY (CAYMAN) LIMITED'))
csp2.append(Filter1('BELGRAVIA HOUSE, 34/44 CIRCULAR ROAD, DOUGLAS IM1 1QW'))
csp1.append(Filter1('MIDDLETON KATZ CHARTERED SECRETARIES LLC'))
csp2.append(Filter1('11 Hope Street, Douglas, IM1 1AQ'))
csp1.append(Filter1('MONA LIMITED'))
csp2.append(Filter1('5 Market Place, Peel, IM5 1AB'))
csp1.append(Filter1('MONTPELIER (TRUST & CORPORATE) SERVICES LIMITED'))
  ##  not listed in OC - previously MTM (ISLE OF MAN) LIMITED
csp2.append(Filter1('FERNLEIGH HOUSE, PALACE ROAD, DOUGLAS, IM2 4LB'))
##  --DUPLICATE ADDRESS--
##  MOORE FUND ADMINISTRATION (IOM) LIMITED
##    not listed in OC - previously IFG FUND ADMINISTRATION (IOM) LIMITED
##  International House, Castle Hill, Victoria Road, Douglas IM2 4RB
csp1.append(Filter1('MOORE STEPHENS TRUST COMPANY LIMITED'))
  ##  not listed in OC - previous name COMPASS TRUST LIMITED
csp2.append(Filter1('26-28 Athol Street, Douglas, IM1 1JB'))
csp1.append(Filter1('NEDGROUP INVESTMENTS (IOM) LIMITED'))
  ##  not listed in OC - PREVIOUS - NIB International Asset Management Limited
  ##  not listed in OC - PREVIOUS - Syfrets International Fund Management Limited
  ##  listed in OC - PREVIOUS - ATC Fund Management Limited
  ##  not listed in OC - PREVIOUS - ATC Fund Management (SG) Limited
csp2.append(Filter1('1st Floor, Samuel Harris House, St George Street, Douglas IM1 1AJ'))
csp1.append(Filter1('NORTHERN WYCHWOOD LIMITED'))
  ##  not listed in OC - previous name NORTHERN LIMITED
csp2.append(Filter1('1st Floor, Exchange House, 54-58 Athol Street, Douglas, IM99 1JD'))
csp1.append(Filter1('OCEANIC ASSET BACKED FINANCE LIMITED'))
  ##  NMV REGISTERED AGENT: MARINE SERVICES (IOM) LIMITED
csp2.append(Filter1('ST GEORGES COURT, UPPER CHURCH STREET, DOUGLAS, IM1 1EE'))
  ##  -- APOSTROPHE --
  ##  ST GEORGE'S COURT, UPPER CHURCH STREET, DOUGLAS, IM1 1EE
csp1.append(Filter1('OCRA (ISLE OF MAN) LIMITED'))
  ##  listed in OC - previous name OVERSEAS COMPANY REGISTRATION AGENTS LIMITED
csp2.append(Filter1('Grosvenor Court, Tower Street, Ramsey, IM8 1JA'))
csp1.append(Filter1('OFFSHORE CORPORATE SERVICES LIMITED'))
csp2.append(Filter1('9 Hope Street, Douglas'))
csp1.append(Filter1('ONYX MANAGEMENT LIMITED'))
csp2.append(Filter1('PO Box 286, 19/21 Circular Road, Douglas, IM99 3JN'))
csp1.append(Filter1('OPTIMUS FIDUCIARIES LIMITED'))
  ##  not listed in OC - previous name TENON (IOM) LIMITED
csp2.append(Filter1('St Marys, The Parade, Castletown, IM9 1LG'))
  ##  -- APOSTROPHE --
  ##  St Mary's, The Parade, Castletown, IM9 1LG
csp1.append(Filter1('OXFORD CORPORATE MANAGEMENT COMPANY LIMITED'))
csp2.append(Filter1('Norton House, Farrants Way, Castletown, IM9 1NR'))
csp1.append(Filter1('P.P.S. LIMITED'))
  ##  T/A CH CONSULTING
csp2.append(Filter1('PO Box 95, 2A Lord Street, Douglas, IM99 1HP'))
csp1.append(Filter1('PAICOLEX TRUST COMPANY (ISLE OF MAN) LIMITED'))
csp2.append(Filter1('PORTLAND HOUSE, STATION ROAD, BALLASALLA, IM99 6AB'))
csp1.append(Filter1('PCS LIMITED'))
csp2.append(Filter1('2nd Floor, Murdoch Chambers, South Quay, Douglas, IM1 5AS'))
##  -- DUPLICATE ADDRESS --
##  csp1.append(Filter1('PCS TRUSTEE LIMITED'))
##  2nd Floor, Murdoch Chambers, South Quay, Douglas, IM1 5AS
csp1.append(Filter1('PEREGRINE CORPORATE SERVICES LIMITED'))
csp2.append(Filter1('Burleigh Manor, Peel Road, Douglas'))
csp1.append(Filter1('PRIVILEGE MANAGEMENT SERVICES LIMITED'))
  ##  not listed in OC - previous name GREENMILE LIMITED
csp2.append(Filter1('2ND FLOOR, KERMODE HOUSE, PARLIAMENT STREET, RAMSEY, IM8 1AG'))
  ##  -- NMV REGISTERED AGENT --
  ##  2ND FLOOR, KERMODE HOUSE, PARLIAMENT STREET, RAMSEY, IM8 1AG
  ##  -- REGISTERED OFFICE --
  ##  EAST LOUGHAN, BRETNEY ROAD, JURBY EAST, IM7 3EZ
##  -- DISSOLVED --
##  csp1.append(Filter1('QUAYSIDE SERVICES LIMITED'))
##  Second Floor, Atlantic House, Circular Road, Douglas
##  -- DUPLICATE ADDRESS --
##  csp1.append(Filter1('R & M MANAGEMENT (I.O.M.) LIMITED'))
##  csp2.append(Filter1('12-14 Finch Road, Douglas, IM1 2SA'))
csp1.append(Filter1('R H CORKILL AND CO LIMITED'))
csp2.append(Filter1('10 Auckland Terrace, Ramsey, IM8 1AF'))
csp1.append(Filter1('ROYAL SKANDIA TRUST COMPANY LIMITED'))
csp2.append(Filter1('Skandia House, King Edward Road, Onchan, IM99 1NU'))
csp1.append(Filter1('SABRE FIDUCIARY LIMITED'))
csp2.append(Filter1('2ND FLOOR, ANGLO INTERNATIONAL HSE, LORD STREET, DOUGLAS, IM1 4LN'))
##  -- DUPLICATE ADDRESS --
##  csp1.append(Filter1('SANNE CORPORATE SERVICES LIMITED'))
##  csp2.append(Filter1('12-14 Finch Road, Douglas, IM1 2SA'))
csp1.append(Filter1('SCARLETT CORPORATE SERVICES LIMITED'))
csp2.append(Filter1('2nd Floor, Viking House, Nelson Street, Douglas, IM1 2AH'))
csp1.append(Filter1('SCOTTISH INTERNATIONAL FUND MANAGERS LIMITED'))
csp2.append(Filter1('Royal London House, Cooil Road, Douglas, IM2 2SP'))
csp1.append(Filter1('SENATE LIMITED'))
csp2.append(Filter1('9 ST RUNIUS WAY, BALLAGAREY ROAD, GLEN VINE, IM4 4FH'))
csp1.append(Filter1('SHANNON CORPORATE SERVICES LIMITED'))
  ##  -- DUPLICATE NAME AND ADDRESS --
  ##  -- 055840C --
  ##  -- 104670C --
csp2.append(Filter1('1st Floor Royal Trust House, 60-62 Athol Street, Douglas, IM1 1JD'))
csp1.append(Filter1('SMP FUND SERVICES LIMITED'))
csp2.append(Filter1('PO BOX 227 CLINCHS HOUSE, LORD STREET, DOUGLAS, IM99 1RZ'))
  ##  -- APOSTROPHE --
  ##  PO BOX 227 CLINCH'S HOUSE, LORD STREET, DOUGLAS, IM99 1RZ
##  -- DUPLICATE ADDRESS --
##  csp1.append(Filter1('SMP PARTNERS LIMITED'))
##    not listed in OC
##  csp2.append(Filter1('PO BOX 227 CLINCHS HOUSE, LORD STREET, DOUGLAS, IM99 1RZ'))
##    -- APOSTROPHE --
##    PO BOX 227, CLINCH'S HOUSE, LORD STREET, DOUGLAS, IM99 1RZ
csp1.append(Filter1('SMP TRUSTEES LIMITED'))
csp2.append(Filter1('CLINCHS HOUSE, LORD STREET, DOUGLAS, IM99 1RZ'))
  ##  -- APOSTROPHE --
  ##  CLINCH'S HOUSE, LORD STREET, DOUGLAS, IM99 1RZ
csp1.append(Filter1('SOVEREIGN TRUST (ISLE OF MAN) LIMITED'))
csp2.append(Filter1('Sovereign House, 14-16 Nelson Street, Douglas, IM1 2AL'))
##  -- DUPLICATE ADDRESS --
##  csp1.append(Filter1('STABITRUST FIDUCIARIES LIMITED'))
##  csp2.append(Filter1('16 ST GEORGES STREET, DOUGLAS, IM1 1PL'))
csp1.append(Filter1('STANDARD BANK TRUST COMPANY (ISLE OF MAN) LIMITED'))
  ##  not listed in OC
  ## PREVIOUS NAME: Brown Shipley Trust Company (I.O.M.) Limited
  ## PREVIOUS NAME: Brown Shipley Corporate Services (Isle of Man) Limited
csp2.append(Filter1('Standard Bank House, One Circular Road, Douglas'))
csp1.append(Filter1('STEED SOLUTIONS LIMITED'))
csp2.append(Filter1('Varley House, 29-31 Duke Street, Douglas, IM1 2AZ'))
csp1.append(Filter1('STEER-FOWLER LIMITED'))
csp2.append(Filter1('1st Floor, Norton House, 41 Arbory Street, Castletown, IM9 1LL'))
csp1.append(Filter1('STERLING TRUST LIMITED'))
  ##  not listed in OC
  ##  PREVIOUS NAME: STERLING INTERNATIONAL TRUST AND CORPORATE SERVICES LIMITED
  ##  PREVIOUS NAME: Sterling Corporate Services Limited
csp2.append(Filter1('12a The Village Walk, Onchan, IM3 4EB'))
csp1.append(Filter1('STOWE TRUSTEES LIMITED'))
csp2.append(Filter1('PO BOX 95, 2A LORD STREET, DOUGLAS, IM99 1HP'))
csp1.append(Filter1('STRONTIUM CONSULTANTS LIMITED'))
csp2.append(Filter1('RIDGEWAY HOUSE, RIDGEWAY STREET, DOUGLAS, IM99 1PY'))
csp1.append(Filter1('THE LAW TRUST LIMITED'))
csp2.append(Filter1('The Old Courthouse, Athol Street, Douglas, IM1 1LD'))
csp1.append(Filter1('THE PREMIER GROUP (ISLE OF MAN) LIMITED'))
  ##  not listed in OC - FSC LIST TYPO: THE PREMIER GROUP (ISLE OF MAN) LIMITED
csp2.append(Filter1('Ground Floor Office, 12-14 Ridgeway Street, Douglas, IM1 1EN'))
csp1.append(Filter1('TRIDENT TRUST COMPANY (I.O.M.) LIMITED'))
csp2.append(Filter1('12-14 FINCH ROAD, DOUGLAS, IM1 2PT'))
csp1.append(Filter1('TURNSTONE (ISLE OF MAN) LIMITED'))
csp2.append(Filter1('DOLBERG HOUSE, 9 ATHOL STREET, DOUGLAS, IM1 1LD'))
##  -- DUPLICATE ADDRESS --
##  csp1.append(Filter1('TYRER WEBSTER LIMITED'))
##  csp2.append(Filter1('9 Circular Road, Douglas, IM1 1AF'))
csp1.append(Filter1('V.COMPANIES LIMITED'))
csp2.append(Filter1('SOVEREIGN HOUSE, STATION ROAD, ST JOHNS, IM4 3AJ'))
csp1.append(Filter1('VANTAGE CORPORATE SERVICES LIMITED'))
  ##  T/A VANTAGE CORPORATE
  ##  not listed in OC
csp2.append(Filter1('Fort Anne, South Quay, Douglas IM1 5PD'))
csp1.append(Filter1('VERIS SECRETARIAL LIMITED'))
csp2.append(Filter1('P.O.Box 237, Peregrine House, Peel Road, Douglas, IM99 1SU'))
csp1.append(Filter1('WACOSER LIMITED'))
  ##  not listed in OC - previous name: EKANS LIMITED
csp2.append(Filter1('Masonic Buildings, Water Street, Ramsey'))
csp1.append(Filter1('WATERMAN TRUST COMPANY LIMITED'))
csp2.append(Filter1('1st Floor, Murdoch House, North Shore Road, Ramsey, IM8 3DY'))
csp1.append(Filter1('WEST CORPORATION LIMITED'))
csp2.append(Filter1('Analyst House, 20-26 Peel Road, Douglas, IM99 1AP'))
##  -- DUPLICATE ADDRESS --
##  csp1.append(Filter1('WESTWINDS OFFSHORE SERVICES LIMITED'))
##  csp2.append(Filter1('1st Floor, Murdoch House, North Shore Road, Ramsey, IM8 3DY'))
csp1.append(Filter1('WHITEBRIDGE CORPORATE SERVICES LIMITED'))
csp2.append(Filter1('2A Lord Street, Douglas'))
csp1.append(Filter1('WILLIS ADMINISTRATION (ISLE OF MAN) LIMITED'))
csp2.append(Filter1('Tower House, Loch Promenade, Douglas'))
csp1.append(Filter1('WILTON (IOM) LIMITED'))
csp2.append(Filter1('22 Athol Street, Douglas, IM1 1JA'))
csp1.append(Filter1('WORLDWIDE CORPORATE SOLUTIONS LIMITED'))
csp2.append(Filter1('Suite 1, Cronkmooar, Shore Road, Castletown, IM9 4PL'))
csp1.append(Filter1('MPH FIDUCIARY LIMITED'))
  ##  -- IN LIQUIDATION --
csp2.append(Filter1('3rd Floor, Atlantic House, Circular Road, Douglas, IM1 1AG'))
csp1.append(Filter1('LOUIS GROUP (IOM) LIMITED'))
  ##  -- IN LIQUIDATION --
csp2.append(Filter1('Louis Building, 29 Bucks Road, Douglas, IM1 3DE'))
csp3=[0] * len(csp2)
##print 'CSP1: '+str(len(csp1))
##print 'CSP2: '+str(len(csp2))
##print csp1
##print csp2
##print csp3
##sys.exit(0)

c3=0
x1=0
##  temp - import pages 101 to 200 with rate limiting (5000 API calls i.e. pages 1 to 100)
x1=100
while 1:
    x1=x1+1
    ##ocurl1='http://api.opencorporates.com/v0.2/companies/search?q=&api_token='+ockey+'&sparse=true'
    ocurl1='http://api.opencorporates.com/v0.2/companies/search?q=&sparse=true'
    ##ocurl2='&per_page=50&page='+str(x1)+'&jurisdiction_code=im&current_status=Live'
    ocurl2='&per_page=50&page='+str(1)+'&jurisdiction_code=im&current_status=Live'
    ocentities=simplejson.load(urllib.urlopen(ocurl1+ocurl2))
    print ocentities
    sys.exit(0)
    if x1==1:
        c1=ocentities['results']['total_pages']    
    c2=len(ocentities['results']['companies'])
    print 'TRACE #2-1: '+str(c2)+'/'+str(x1)+'/'+str(c1)
    print 'TRACE #2-2: ',ocentities
    for x2 in range(0,c2):
        c3=c3+1
        print 'TRACE #3-1: '+str(x2)+'/'+str(x1)+'/'+str(c3)
        entity=ocentities['results']['companies'][x2]
        ocjurisdiction=entity['company']['jurisdiction_code']
        ocreference=entity['company']['company_number']
        ocname=entity['company']['name']
        try:
            ocurl='http://api.opencorporates.com/v0.2/companies/'+ocjurisdiction+'/'+ocreference+'?api_token='+ockey+'&sparse=true'
            ocdata=simplejson.load(urllib.urlopen(ocurl))
            ocaddress=ocdata['results']['company']['registered_address_in_full']
            if ocaddress is None:
                ocaddress='**ERROR**'
        except:
            ocaddress='**ERROR**'
            ##ocaddress=None
        ##time.sleep(1.25)
        if ocaddress is '**ERROR':
            print 'TRACE #4-'+str(x1)+'-'+str(x2)+': ERROR'
        else:
            ocaddress=Filter1(ocaddress)
            ##if ocaddress in csp2:
            ##    print 'TRACE #4-'+str(x1)+'-'+str(x2)+': '+str(ocreference)+'/'+str(ocname)
            ##    db={'ocaddress':ocaddress}
            ##    db['entity']=ocreference
            ##    db['name']=ocname
            ##    scraperwiki.sqlite.save(unique_keys=['ocaddress'], table_name='csp_address', data=db)
            ##    c4=csp2.index(ocaddress)
            ##    csp3[c4]=csp3[c4]+1
            ##else:
            ##    print 'TRACE #4-'+str(x1)+'-'+str(x2)+': OTHER'
            ##    db={'ocaddress':ocaddress}
            ##    db['entity']=ocreference
            ##    db['name']=ocname
            ##    scraperwiki.sqlite.save(unique_keys=['ocaddress'], table_name='csp_address', data=db)
        ##  phase #1:  a unique key on ocaddress can be used to highlight inconsistent address issues
        db={'ocaddress':ocaddress}
        db['name']=ocname
        db['address']=ocaddress
        scraperwiki.sqlite.save(unique_keys=['ocaddress'], table_name='csp_address', data=db)
        ##  phase #2:  a unique key on ocentity would allow a count of all entities with each unique address
        ##  db{'entity'}=ocreference
        ##  db['name']=ocname
        ##  db['address']=ocaddress
        ##  scraperwiki.sqlite.save(unique_keys=['entity'], table_name='csp_address', data=db)
        ##if c3==12:
        ##    sys.exit(0)
    if x1==c1:
        sys.exit(0)
    time.sleep(2.5)

##  PENDING:  switch from csp3[] to count each csp address
##  q = '* FROM "csp_address"'
##  data = scraperwiki.sqlite.select(q)

def searchOCNames(target):
    rurl='http://opencorporates.com/reconcile/im?current_status=Live&query='+urllib.quote(target)
    entities=simplejson.load(urllib.urlopen(rurl))
    print 'TRACE #1: ', entities
    return entities

def searchOCAddresses(target):
    rurl='http://opencorporates.com/reconcile/im?current_status=Live'
    entities=simplejson.load(urllib.urlopen(rurl))
    return entities

def getOCCompanyData(ocid):
##  ocurl='http://api.opencorporates.com'+ocid+'/data'+'?api_token='+ockey
    ocurl='http://api.opencorporates.com'+ocid+'/data'
    ocdata=simplejson.load(urllib.urlopen(ocurl))
    return ocdata

def getOCCompanyDetails(ocid):
    ##ocurl='http://api.opencorporates.com'+ocid+'?api_token='+ockey
    ocurl='http://api.opencorporates.com'+ocid
    ocdata=simplejson.load(urllib.urlopen(ocurl))
    return ocdata

def logCompanyDetails(ocid,ocdata,ttarget):
    if 'error' in ocdata:
        return
    print 'TRACE #Y:',ocdata
    cdata={'ocid':ocid}
    cdata['name']=ocdata['company']['name']
    cdata['address']=ocdata['company']['registered_address_in_full']
    print 'TRACE #Z:',cdata
    scraperwiki.sqlite.save(unique_keys=['ocid'], table_name='companydetails_'+ttarget, data=cdata)
    return

##import time
def processCompany(target):
    ttarget=Filter1(target)
    ocentities=searchOCNames(target)
    ##ccount=len(ocentities['result'])
    ccount=len(ocentities)
    print 'TRACE #2: ', ccount
    cci=1
    for item in ocentities['result']:
        ocid=item['id']
        ocname=item['name']
        print 'processing ',ocid,' ',cci,'/',ccount
        if ocid not in companies:
            ##time.sleep(1.0)
            print ocid,': ',ocname
            ocdata=getOCCompanyDetails(ocid)
            logCompanyDetails(ocid,ocdata,ttarget)
        else:
            print '** already logged **'
        cci=cci+1
    return

def processAddresses():
    ccount=len(companies)
    print 'TRACE #3: ', ccount
    cci=1
    for address in companies:
        ocid=companies['id']
        ocname=companies['name']
        ocaddress=companies['address']
        print ocaddress,' ',cci,'/',ccount
        q = '* FROM "companydetails_'+ocname+'" WHERE registered_address_in_full='+ocaddress
        qdata = scraperwiki.sqlite.select(q)
        print qdata
        cci=cci+1
    return

processCompany('Trident Trust Company (I.O.M.) Limited')
processAddresses()


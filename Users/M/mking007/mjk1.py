import scraperwiki
import urllib
import xlrd
import re
import sys


def ScrapeORR():
    railuseurl = "http://www.rail-reg.gov.uk/upload/xls/station_usage_0910.xls"
    book = xlrd.open_workbook(file_contents=urllib.urlopen(railuseurl).read())
    sheet = list(book.sheets())[1]
    
    headers = [ ]
    for header in sheet.row_values(0):
        lheader = re.sub("&", "and", header)
        lheader = re.sub("\s+", " ", lheader)
        lheader = re.sub("\(|\)", "", lheader)
        headers.append(lheader)
    print headers
    
    
    for row in range(1, sheet.nrows):
        values = sheet.row_values(row)
        if values[0]:
            data = dict(zip(headers, values))
            scraperwiki.sqlite.save(unique_keys=["TLC"], data=data, verbose=0)


print scraperwiki.sqlite.select("TLC from swdata")

from BeautifulSoup import BeautifulSoup


# define the order our columns are displayed in the datastore
# scraperwiki.metadata.save('data_columns', ['id', 'Album', 'Released', 'Sales (m)'])
#scraperwiki.metadata.save('data_columns', ['id', 'station_var', 'station_val'])


record = {}
unique_record_id = 0
tlc_db ={}
tlc_db = [
'SOF','WDH','WDS','WLY','WME','WSR','WOO','WLS','WWA','WWD','WWW','WOF','WCP',
'WOS','WKG','WRK','WOR','WPL','WRT','WRH','WRB','WRY','WRE','WRS','WXC','WRX','WYE','WYM','WYL','WMD','WYT','YAL',
'YRD','YRM','YAE','YAT','YEO','YVJ','YVP','YET','YNW','YOK','YRK','YRT','YSM','YSR']
tlc_db = []

print tlc_db

for tlc in tlc_db:
    print "=============================="
    url_start = 'http://www.nationalrail.co.uk/stations/'
    url_end = '/details.html'
    print tlc
    starting_url = url_start + tlc + url_end
    print starting_url
        
    #    html = scraperwiki.scrape('http://www.nationalrail.co.uk/stations/ABD/details.html')
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object

    print html

    dts = soup.findAll('dt') # get all the <dt> tags that show the variable name
    dds = soup.findAll('dd') # get all the <dd> tags that show the variable value
    i2=0

    for dt in dts:
        print unique_record_id
        print dt
        record ['id']= unique_record_id
        record ['station_code']=tlc
        record ['station_var']= dts [i2].text
        record ['station_val']= dds [i2].text
    #    print database, '------------'
    #    scraperwiki.metadata.save('data_columns', ['id', 'station_var', 'station_val'])
        scraperwiki.datastore.save(['id'],record) # save the records one by one
    
        i2=i2+1
        unique_record_id=unique_record_id+1                    
 



    


   
    ##
    #import scraperwiki
    #from BeautifulSoup import BeautifulSoup
    
    # define the order our columns are displayed in the datastore
    #scraperwiki.metadata.save('data_columns', ['Connection time', 'Cycle storage'])
    #scraperwiki.metadata.save('data_columns', ['Connection time', 'Cycle storage', 'Waiting Rooms', 'Web Kiosk'])
    
    
    # scrape_table function: gets passed an individual page to scrape
    #def scrape_table(soup):
    
    #    data_table = soup.find("acc-c expanded-content", { "class" : "zebra" })
    #    data_table = soup.find("table", { "class" : "data" })
    #    rows = data_table.findAll("dt")
    #     rows = soup.findAll("dt")
    #      print "hello0"
    
    #    for row in rows:
            # Set up our data record - we'll need it later
    #        print "hello1"
    #        print row
    #        print "hello2"
    #        record = {}
    #        table_cells = row.findAll("dd")
    ##        table_cells = row.findAll("td")
    #        if table_cells: 
    #            record['Connection time'] = table_cells[0].text
    #            record['Shops'] = table_cells[1].text
    ##            record['Waiting Rooms'] = table_cells[2].text
    ##            record['Web Kiosk'] = table_cells[4].text
    #            # Print out the data we've gathered
    #            print record, '------------'
    #            # Finally, save the record to the datastore - 'Artist' is our unique key
    #            scraperwiki.datastore.save(["Connection time"], record)
    #        
    # scrape_and_look_for_next_link function: calls the scrape_table
    # function, then hunts for a 'next' link: if one is found, calls itself again
    #def scrape_and_look_for_next_link(url):
    #    html = scraperwiki.scrape(url)
    #
    #    print html
    
    #    soup = BeautifulSoup(html)
    #    scrape_table(soup)
    #    next_link = soup.find("a", { "class" : "next" })
    #    print next_link
    #    if next_link:
    #        next_url = base_url + next_link['href']
    #        print next_url
    #        scrape_and_look_for_next_link(next_url)
    
    # ---------------------------------------------------------------------------
    # START HERE: define your starting URL - then 
    # call a function to scrape the first page in the series.
    # ---------------------------------------------------------------------------
    #url_start = 'http://www.nationalrail.co.uk/stations/'
    #print url_start
    #url_end = '/details.html'
    #print url_end
    #starting_url = url_start + url_end
    #print starting_url
    #scrape_and_look_for_next_link(starting_url)
    
#This is the list of ALL codes. Commented here as a store
#tlc_db = ['ABW','ABE','ACY','ABA','ABD','AUR','AVY','ABH','AGV','AGL','AYW','ACR','AAT','ACN','ACH','ACK','ACL','ACG','ACB','ACC','AML','ADD','ADW','ASN','ADM','ADC','ADL','AWK','AIG','ANS','AIN','AIR','ADR','AYP','ALB','ALD','AMT','AHT','AGT','AAP','AXP','ALX','ALF','ALW',
#'ALO','ASS','ALM','ALR','ASG','ALN','ALP','ABC','AON','ALT','ALV','AMB','AMY','AMR','AMF','ANC','AND','ADV','ANZ','AGR','ANG','ANN','ANL','AFV','APP','APD','APF','APB','APS','ARB',
#'ARD','AUI','ADS','ASB','ADN','ADK','AGS','ARG','ARL','AWT','ARN','ARR','ART','ARU','ACT','AUW','ASH','AHV','ABY','ASC','ASF','AFS','AFK','ASY','AHD','AHN','AHS','ANF','AWM','ASK',
#'ALK','ASP','APG','AST','ATH','ATN','ATT','ATB','ATL','AUK','AUD','AUG','AVM','AVF','AVN','AXM','AYS','AVP','AYL','AYH','AYR','BAC','BAJ','BAG','BLD','BIO','BAB','BDK','BAL','BHC',
#'BSI','BMB','BAM','BNV','BAN','BNG','BAH','BAD','BSS','BLL','BAR','BGI','BGD','BKG','BMG','BRM','BNH','BNS','BNI','BTB','BAA','BNL','BNY','BNP','BTG','BRR','BRL','BAV','BIF','BWS','BRY','BYD','BYI','BYL','BAU','BSO','BSK','BBL','BTH','BHG','BTL','BTT','BAK','BAT','BLB','BAY','BCF','BER','BRN','BSD','BSL','BEU','BEL','BEB','BCC','BEC','BKJ','BDM','BSJ','BDH','BMT','BEH','BDW','BEE','BKS','BLV','BLG','BGM','BLH','BLM','BLP','BEG','BVD','BEM','BEY','BEF','BEN','BTY','BYK','BAS','BFE','BKM','BKW','BYA','BBW','BRS','BRK','BWK','BES','BSC','BTO','BET','BYC','BEV','BEX','BXY','BXH','BCS','BIT','BKL','BID','BIW','BBK','BIC','BIL','BIG','BIN','BIY','BCG','BCH','BWD','BIK','BDL','BKC','BKQ','BKN','BKP','BBS','BHI','BMO','BHM','BSW','BIA','BBG','BIS','BIP','BPT','BTE','BBN','BFR','BKH','BHO','BPN','BPB','BPS','BLK','BAW','BFF','BLA','BAI','BKT','BKD','BLT','BLO','BSB','BLY','BLX','BWN','BLN','BYB','BOD','BOR','BOG','BGS','BON','BTD','BKA','BOC','BNW','BOT','BRG','BRH','BOH','BSN','BOE','BTF','BNE','BMH','BRV','BWB','BOP','BWG','BXW','BCE','BDQ','BDI','BOA','BDN','BTR','BTP','BML','BMY','BLE','BMP','BRP','BCN','BND','BSM','BYS','BDY','BRC','BFD','BRE','BWO','BEA','BRO','BGN','BDG','BWT','BDT','BRF','BGG','BGH','BTN','BMD','BNT','BPW','BRI','BHD','RBS','BNF','BRX','BGE','BDB','BSR','BCU','BHS','BCY','BOM','BMR','BMC','BMN','BMS','BMV','BSY','BSP','BPK','BKO','BME','BMF','BRA','BUH','BYF','BXB','BCV','BDA','BGA','BSU','BRW','BRU','BYN','BUC','BCK','BUK','BGL','BHR','BLW','BUE','BUG','BUY','BUW','BNA','BUD','BNM','BUU','BUB','BNC','BYM','BUI','BTS','BCB','BCJ','BUO','BUJ','BUT','BSE','BUS','BHK','BSH','BUL','BPC','BXD','BUX','BFN','BYE','CAD','CGW','CPH','CWS','CDT','CIR','CSK','CDU','CAM','CBN','CBG','CBH','CBL','CMD','CMO','CNL','CAO','CST','CNN','CBE','CBW','CNY','CPU','CBB','CDD','CDB','CDF','CDQ','CDO','CDR','CRF','CAK','CAR','CTO','CLU','CMN','CML','CNF','CAN','CAY','CPK','CAG','CSH','CSB','CRS','CDY','CBP','CLC','CFD','CAS','CSM','CAT','CTF','CFB','CYS','CCT','CTL','CAU','CYB','CTH','CFH','CFO','CHW','CFR','CEF','CPN','CLN','CWC','CHG','CHX','CHC','CBY','CTN','CRT','CSR','CTE','CTM','CHT','CHU','CHE','CED','CEL','CHM','CLD','CNM','CPW','CYT','CHY','CHN','CSN','CSS','CTR','CRD','CHD','CLS','CSW','CNO','CCH','CIL','CHL','CHI','CLY','CPM','CHP','CRK','CIT','CHK','CHO','CRL','CLW','CHR','CHH','CTW','CHF','CTT','CIM','CTK','CLT','CLA','CPY','CLP','CLJ','CPT','CLR','CKS','CLV','CLG','CLE','CEA','CLI','CFN','CLH','CLK','CUW','CYK','CBC','CBS','COA','CSD','CSL','CGN','COL','CET','CEH','CLM','CLL','CNE','CWL','CWB','CME','COM','CNG','CNS','CON','CEY','CNP','CNW','COB','COO','CBR','COE','COP','CRB','COR','CKH','CKL','CPA','CRR','COY','CSY','COS','CSA','CGM','COT','CDS','COV','CWN','COW','CRA','CGD','CRM','CRV','CRW','CRY','CDI','CES','CSG','CWD','CRE','CKN','CWH','CNR','CCC','CRI','CFF','CFT','CMR','CMF','CKT','CRG','CFL','COI','CKY','CMY','CSO','CRH','COH','CWU','CWE','CRN','CRO','CYP','CUD','CUF','CUM','CUA','CUB','CUP','CUH','CUX','CMH','CWM','CYN','DDK','DSY','DAG','DAL','DAK','DAM','DMR','DLR','DLY','DLS','DLK','DLT','DLW','DNY','DCT','DZY','DAR','DAN','DSM','DFD','DRT','DWN','DAT','DVN','DWL','DWW','DEA','DEN','DNN','DGT','DPD','DGY','DHN','DLM','DBD','DNM','DGC','DMK','DNT','DTN','DEP','DBY','DBR','DKR','DPT','DEW','DID','DIG','DMH','DMG','DNS','DGL','DIN','DND','DTG','DSL','DIS','DOC','DOD','DOL','DLH','DLG','DWD','DON','DCH','DCW','DOR','DKG','DKT','DMS','DDG','DVH','DVP','DVC','DVY','DOW','DRG','DYP','DRM','DRF','DRI','DTW','DRO','DMC','DFR','DRU','DMY','DUD','DDP','DFI','DRN','DST','DUL','DBC','DBE','DUM','DMF','DMP','DUN','DBL','DBG','DCG','DEE','DFL','DFE','DKD','DNL','DNO','DOT','DNG','DHM','DUR','DYC','DYF','EAG','EAL','ERL','EAR','EAD','ELD','EWD','ECR','EDY','EDW','EFL','EGF','EGR','EKL','EML','EMD','ETL','EWR','EBN','EBK','EST','ERA','ESL','EGN','EBB','EBV','ECC','ECS','ECL','EDL','EDN','EBR','EBT','EDG','EDB','EDP','EDR','EFF','EGG','EGH','EGT','EPH','ELG','ELP','ELE','ESD','ESW','ELR','ESM','ELS','ELW','ELO','ELY','EMP','EMS','ENC','ENL','ENF','ENT','EPS','EPD','ERD','ERI','ERH','ESH','EXR','ETC','EUS','EBA','EVE','EWE','EWW','EXC','EXD','EXT','EXG','EXM','EXN','EYN','FLS','FRB','FRF','FRL','FRW','FCN','FKG','FKK','FOC','FMR','FAL','FMT','FAM','FRM','FNB','FNN','FNC','FNH','FNR','FNW','FAR','FLD','FAV','FGT','FAZ','FRN','FEA','FLX','FEL','FST','FNT','FEN','FER','FRY','FYS','FFA','FIL','FIT','FNY','FPK','FIN','FSB','FSG','FGH','FSK','FZW','FWY','FLE','FLM','FLN','FLT','FLI','FLF','FKC','FKW','FOD','FOG','FOH','FBY','FOR','FRS','FTM','FTW','FOK','FOX','FXN','FRT','FTN','FRE','FFD','FML','FRI','FZH','FRD','FRO','FLW','FNV','FZP','GNB','GBL','GCH','GRF','GGV','GAR','GRS','GSD','GSN','GSW','GRH','GMG','GTH','GVE','GST','GTY','GTW','GGJ','GER','GDP','GFN','GIG','GBD','GFF','GIL','GLM','GSC','GIP','GIR','GLS','GCW','GLC','GLQ','GLH','GLZ','GLE','GLF','GLG','GLT','GLO','GCR','GLY','GOB','GOD','GDL','GDN','GOE','GOF','GOL','GOM','GMY','GOO','GTR','GDH','GOR','GBS','GTO','GPO','GRK','GWN','GOX','GPK','GOS','GTN','GRA','GRT','GVH','GRV','GRY','GTA','GRB','GRC','GCT','GMV','GMN','GYM','GNL','GNR','GBK','GRL','GNF','GFD','GNH','GKC','GKW','GNW','GEA','GMD','GMB','GRN','GMT','GRP','GUI','GLD','GSY','GUN','GSL','GNT','GWE','GYP','HAB','HCB','HKC','HAC','HKW','HDM','HAD','HDF','HDW','HGF','HAG','HMY','HAL','HAS','HED','HFX','HLG','HID','HLR','HAI','HWH','HMT','HME','HNC','HNW','HMM','HMD','HDH','HMP','HMC','HMW','HIA','HSD','HAM','HND','HTH','HAN','HPN','HRL','HDN','HRD','HLN','HWM','HWN','HRO','HPD','HRM','HGY','HRY','HRR','HGT','HRW','HOH','HTF','HBY','HPL','HTW','HPQ','HWC','HSL','HSK','HGS','HTE','HAT','HFS','HAP','HSG','HTY','HTN','HAV','HVN','HVF','HWD','HWB','HKH','HDB','HYR','HAY','HYS','HYL','HYM','HHE','HAZ','HCN','HDY','HDL','HDG','HLI','HHL','HLL','HTC','HBD','HEC','HDE','HNF','HEI','HLC','HLU','HLD','HMS','HSB','HML','HEN','HNG','HNL','HOT','HEL','HFD','HNB','HNH','HER','HFE','HFN','HES','HSW','HEV','HEW','HEX','HYD','HHB','HIB','HST','HWY','HGM','HIP','HIG','HHY','HTO','HLB','HLF','HLE','HLW','HIL','HLS','HYW','HNK','HIN','HNA','HIT','HGR','HOC','HBN','HOD','HCH','HLM','HOL','HHD','HLY','HMN','HYB','HON','HOY','HPA','HOK','HOO','HPE','HOP','HPT','HOR','HBP','HRN','HRS','HRH','HSY','HIR','HWI','HSC','HGN','HOU','HOV','HXM','HWW','HOW','HOZ','HYK','HBB','HKN','HUD','HUL','HUP','HCT','HGD','HUB','HUN','HNT','HNX','HUR','HUT','HUY','HYC','HYT','HKM','HYN','HYH','IBM','IFI','IFD','ILK','IMW','INC','INE','INT','INS','IGD','ING','INK','INP','INV','INH','INR','IPS','IRL','IRV','ISL','ISP','IVR','IVY','JEQ','JOH','JHN','JOR','KSL','KSN','KEI','KEH','KEL','KVD','KEM','KMH','KMP','KMS','KML','KEN','KLY','KNE','KNS','KNL','KNR','KPA','KTH','KTN','KTW','KNT','KBK','KET','KWB','KWG','KEY','KYN','KDB','KID','KDG','KWL','KBN','KLD','KIL','KGT','KMK','KLM','KPT','KWN','KBC','KGM','KGH','KGX','KGL','KLN','KNN','KGN','KGP','KGS','KGE','KNG','KND','KIN','KIT','KBX','KKS','KIR','KKB','KSW','KBF','KDY','KRK','KKD','KKM','KKH','KKN','KWD','KTL','KIV','KVP','KNA','KBW','KNI','KCK','KNO','KNU','KNF','KYL','LDY','LAD','LAI','LRG','LKE','LAK','LAM','LNK','LAN','LAC','LAW','LGB','LHO','LNY','LGG','LGM','LGS','LGW','LAG','LAP','LPW','LBT','LAR','LRH','LAU','LWH','LAY','LZB','LEG','LEH','LEA','LHM','LMS','LSW','LHD','LED','LEE','LDS','LEI','LIH','LES','LBZ','LEL','LTS','LEN','LNZ','LEO','LET','LEU','LVM','LWS','LEW','LEY','LEM','LER','LIC','LTV','LID','LHS','LCN','LFD','LGD','LIN','LIP','LSK','LIS','LVT','LTK','LTT','LTL','LIT','LVN','LTP','LVC','LVJ','LIV','LSP','LST','LSN','LVG','LLA','LBR','LLT','LNB','LLN','LDN','LLC','LLL','LLV','LLO','LLD','LLJ','LLI','LLE','LLF','LPG','LLG','LLM','LLH','LGO','LLR','LTH','LLS','LWR','LAS','LWM','LNR','LNW','LLW','LLY','LHA','LHE','LCL','LCS','LCG','LCC','LHW','LOC','LCK','LBG','LOF','LRB','LON','LBK','LGE','LPR','LGK','LOB','LNG','LGF','LND','LPT','LGN','LOO','LTG','LOH','LOT','LOS','LBO','LGJ','LOW','LSY','LWT','LUD','LUT','LTN','LUX','LYD','LYE','LYP','LYT','LYC','LYM','LTM','MAC','MCN','MST','MEW','MAG','MDN','MAI','MDB','MDE','MDW','MAL','MLG','MLT','MVL','MIA','MCO','MAN','MCV','MNE','MNG','MNP','MNR','MRB','MAS','MFT','MSW','MCH','MRN','MAR','MHR','MKR','MNC','MKT','MLW','MPL','MSN','MSK','MGN','MTM','MAO','MTO','MYH','MYL','MYB','MRY','MAT','MTB','MAU','MAX','MAY','MZH','MHS','MEL','MKM','MES','MMO','MEN','MNN','MEO','MEC','MEP','MEY','MHM','MER','MEV','MGM','MCE','MEX','MIC','MIK','MBR','MDL','MDG','MLF','MFH','MLH','MIL','MLB','MBK','MIN','MLM','MIH','MLN','MLR','MKC','MFF','MSR','MIR','MIS','MTC','MIJ','MOB','MON','MRS','MTP','MTS','MRF','MOG','MSD','MRP','MRR','MRD','MDS','MCM','MTN','MRT','MIM','MFA','MLY','MPT','MOR','MTL','MSS','MOS','MSL','MSH','MPK','MSO','MTH','MOT','MTG','MLD','MCB','MFL','MTA','MTV','MOO','MUI','MUB','MYT','NFN','NLS','NRN','NAN','NAR','NBR','NVR','NTH','NMT','NEI','NEL','NES','NET','NRT','NTL','NBA','NBC','NBN','NCE','NWX','NXG','NCK','NEH','NHY','NHL','NHE','NLN','NEM','NMC','NMN','NWM','NPD','NSG','NCT','NNG','NBE','NBY','NRC','NCL','NEW','NVH','NVN','NGT','NMK','NWE','NWP','NQY','NSD','NTN','NTA','NAY','NWN','NTC','NLW','NWR','NOA','NWT','NNP','NIT','NBT','NRB','NSB','NOR','NBW','NCM','NDL','NLR','NQU','NRD','NSH','NWA','NWB','NTR','NMP','NFD','NFL','NLT','NUM','NWI','NRW','NWD','NOT','NUN','NHD','NNT','NUT','NUF','OKN','OKM','OKL','OBN','OCK','OLY','OHL','ORN','OLD','OLF','OLM','OLW','OLT','ORE','OMS','ORP','ORR','OPK','OTF','OUN','OUS','OUT','OVE','OVR','OXN','OXF','OXS','OXT','PAD','PDW','PDG','PGN','PCN','PYG','PYJ','PAL','PAN','PNL','PTF','PAR','PBL','PKT','PKS','PSN','PTK','PRN','PWY','PAT','PTT','PEA','PMR','PEG','PEM','PBY','PMB','PMD','PNA','PEN','PCD','PGM','PNE','PNW','PHG','PNS','PKG','PMW','PNM','PER','PRH','PNR','PYN','PES','PHR','PTB','PNY','PNF','PNZ','PRW','PRY','PSH','PTH','PBO','PTR','PET','PEV','PEB','PEW','PIL','PIN','PIT','PSE','PLS','PLK','PLC','PLM','PMP','PLU','PLY','POK','PLG','PSW','PWE','PWW','PLE','PLW','PMT','POL','PON','PTD','PFR','PFM','POT','PLT','PYC','PYP','PPL','PPD','POO','POP','PTG','PSL','PTA','PTC','POR','PTM','PLN','PLD','PMS','PMA','PMH','PPK','PBR','PFY','PYT','PRS','PSC','PRT','PRB','PRE','PRP','PST','PTW','PRA','PTL','PRR','PRL','PRU','PUL','PFL','PUR','PUO','PUT','PWL','PYL','QYD','QBR','QPK','QPW','QRP','QRB','QUI','RDF','RDT','RAD','RDR','RNF','RNM','RAI','RNH','RAM','RGW','RAN','RAU','RAV','RVB','RVN','RWC','RLG','RAY','RDG','RDW','REC','RDB','RCC','RCE','RDN','RDS','RDC','RDH','RDA','RED','RHM','REE','REI','RTN','RET','RHI','RIA','RHO','RHL','RHY','RHD','RIL','RMD','RIC','RDD','RID','RDM','RCA','RIS','RBR','ROB','RCD','ROC','RTR','RFD','RFY','ROG','ROR','ROL','RMB','RMF','RML','ROM','ROO','RSG','RSH','ROS','RMC','RNR','RLN','ROW','RYB','RYN','RYS','RUA','RUF','RUG','RGT','RGL','RUN','RUE','RKT','RUS','RUT','RYD','RYP','RYR','RRB','RYE','RYH','SFD','SLD','SAF','SAH','SAL','SAE','STS','SLB','SLT','SAM','SLW','SNA','SDB','SNR','SDL','SND','SDG','SAN','SDP','SAD','SDW','SDY','SNK','SQH','SRR','SDF','SDR','SAW','SXY','SAX','SCA','SCT','SCH','SCU','SML','SEF','SFL','SEA','SEM','SSC','SEC','SRG','SBY','SRS','SEL','SEG','SLY','SET','SVK','SVS','SEV','SVB','STJ','SFR','SHN','SHA','SHW','SHL','SSS','SHF','SED','SNF','SEN','SPB','SPH','SPY','SHP','STH','SHE','SIE','SHM','SLS','SDM','SFN','SHD','SHI','SHY','SPP','SIP','SHB','SHH','SRO','SRL','SRY','SHO','SEH','SSE','SRT','SHT','SHS','SHR','SID','SIL','SIC','SLK','SLV','SVR','SIN','SIT','SKG','SKE','SKI','SGR','SWT','SLA','SLR','SLH','SLO','SMA','SAB','SGB','SMR','SMI','SMB','SNI','SDA','SWO','SOR','SOL','SYT','SAT','SBK','SBM','SCY','SES','SGN','SGL','SOH','SOK','SMO','SOM','SRU','STO','SWS','STL','SOA','SOU','SOB','SBU','SEE','SOC','SOE','SOV','SMN','SOP','SWK','SOW','SPA','SBR','SPI','SPO','SPN','SRI','SPR','SPF','SQU','SAA','SAC','SAR','SAS','SAU','SBS','SBF','SBV','SCR','SDN','SER','SGM','SNH','SHJ','SIH','SIV','SJP','SJS','SAJ','SKN','SLQ','SMG','SMT','SMY','STM','SNO','STP','STA','SNS','SLL','SYB','SMD','SMH','SFO','SNT','SSD','SST','SPU','SRD','SBE','SCS','SVL','SCF','SON','SPS','SVG','STV','SWR','STT','STG','SPT','SKS','SSM','STK','SKM','SKW','SOT','SNE','SCG','SBP','SOG','STN','SHU','SNL','SBJ','SBT','SMK','STR','SRA','SFA','SAV','STC','STW','STE','SRC','SRH','SHC','SRN','STF','SOO','STD','STU','SYA','SUY','SUD','SDH','SUG','SUM','SUU','SUN','SUP','SNG','SNY','SUR','SUO','SUT','SUC','SPK','SWL','SAY','SWM','SWA','SNW','SWY','SWG','SWD','SWI','SWE','SNN','SWN','SYD','SYH','SYL','SYS','TAC','TAD','TAF','TAI','TAL','TLB','TLC','TAB','TAM','TAP','TAT','TAU','TAY','TED','TEA','TGM','TFC','TMC','TEN','TEY','THD','THA','THH','THW','TLK','THE','TEO','TTF','THI','TBY','TNN','TNS','THO','THB','TNA','TTH','THT','TPB','TPC','TLS','TBD','TOK','THU','THC','THS','TRS','TIL','THL','TLH','TIP','TIR','TIS','TVP','TOD','TOL','TPN','TON','TDU','TNF','TNP','TOO','TOP','TQY','TRR','TOT','TOM','TTN','TWN','TRA','TRF','TRE','TRH','TRB','TRY','TRM','TRI','TRD','TRN','TRO','TRU','TUL','TUH','TBW','TUR','TUT','TWI','TWY','TYC','TGS','TYG','TYL','TYS','TYW','UCK','UDD','ULC','ULL','ULV','UMB','UNI','UHA','UPL','UPM','UPH','UHL','UTY','UWL','UPT','UPW','URM','UTT','VAL','VXH','VIC','VIR','WDO','WAD','WFL','WKK','WKF','WKD','WLG','WLV','WLT','WAF','WAM','WSL','WDN','WLC','WHC','WMW','WAO','WON','WAL','WAN','WSW','WWR','WNT','WNP','WBL','WAR','WRM','WGV','WMN','WNH','WBQ','WAC','WRW','WRP','WTO','WBC','WTR','WAT','WAE','WLO','WFH','WFJ','WFN','WTG','WAS','WNG','WAV','WEE','WET','WMG','WLI','WEL','WLN','WLP','WGC','WLW','WEM','WMB','WCX','WMS','WND','WNN','WSA','WBP','WBY','WCL','WCY','WDT','WDU','WEA','WEH','WHD','WHP','WHR','WKB','WKI','WMA','WNW','WRU','WRN','WLD','WSU','WWI','WWO','WSB','WCF','WCB','WHA','WTA','WFI','WES','WGA','WHG','WNM','WSM','WRL','WYB','WEY','WBR','WHE','WTS','WFF','WHM','WNL','WHN','WTB','WCH','WTC','WHT','WHL','WNY','WCR','WTH','WTL','WBD','WTE','WHI','WLE','WLF','WTN','WWL','WHY','WHS''WCK','WIC','WCM','WDD','WID','WMR','WGN','WGW','WGT','WMI','WIJ','WLM','WIL','WMC','WML','WNE','WIM','WBO','WSE','WIN','WNF','WIH','WDM','WNC','WNR','WNS','WTI','WSF','WSH','WTM','WTY','WTT','WVF','WIV','WOB','WOK','WKM','WOH','WVH','WOL','WOM','WDE','WST','WDB','WGR','WDL','WDF','WDH','WDS','WLY','WME','WSR','WOO','WLS','WWA','WWD','WWW','WOF','WCP','WOS','WKG','WRK','WOR','WPL','WRT','WRH','WRB','WRY','WRE','WRS','WXC','WRX','WYE','WYM','WYL','WMD','WYT','YAL','YRD','YRM','YAE','YAT','YEO','YVJ','YVP','YET','YNW','YOK','YRK','YRT','YSM','YSR']
#import scraperwiki
import urllib
import xlrd
import re
import sys


def ScrapeORR():
    railuseurl = "http://www.rail-reg.gov.uk/upload/xls/station_usage_0910.xls"
    book = xlrd.open_workbook(file_contents=urllib.urlopen(railuseurl).read())
    sheet = list(book.sheets())[1]
    
    headers = [ ]
    for header in sheet.row_values(0):
        lheader = re.sub("&", "and", header)
        lheader = re.sub("\s+", " ", lheader)
        lheader = re.sub("\(|\)", "", lheader)
        headers.append(lheader)
    print headers
    
    
    for row in range(1, sheet.nrows):
        values = sheet.row_values(row)
        if values[0]:
            data = dict(zip(headers, values))
            scraperwiki.sqlite.save(unique_keys=["TLC"], data=data, verbose=0)


print scraperwiki.sqlite.select("TLC from swdata")

from BeautifulSoup import BeautifulSoup


# define the order our columns are displayed in the datastore
# scraperwiki.metadata.save('data_columns', ['id', 'Album', 'Released', 'Sales (m)'])
#scraperwiki.metadata.save('data_columns', ['id', 'station_var', 'station_val'])


record = {}
unique_record_id = 0
tlc_db ={}
tlc_db = [
'SOF','WDH','WDS','WLY','WME','WSR','WOO','WLS','WWA','WWD','WWW','WOF','WCP',
'WOS','WKG','WRK','WOR','WPL','WRT','WRH','WRB','WRY','WRE','WRS','WXC','WRX','WYE','WYM','WYL','WMD','WYT','YAL',
'YRD','YRM','YAE','YAT','YEO','YVJ','YVP','YET','YNW','YOK','YRK','YRT','YSM','YSR']
tlc_db = []

print tlc_db

for tlc in tlc_db:
    print "=============================="
    url_start = 'http://www.nationalrail.co.uk/stations/'
    url_end = '/details.html'
    print tlc
    starting_url = url_start + tlc + url_end
    print starting_url
        
    #    html = scraperwiki.scrape('http://www.nationalrail.co.uk/stations/ABD/details.html')
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object

    print html

    dts = soup.findAll('dt') # get all the <dt> tags that show the variable name
    dds = soup.findAll('dd') # get all the <dd> tags that show the variable value
    i2=0

    for dt in dts:
        print unique_record_id
        print dt
        record ['id']= unique_record_id
        record ['station_code']=tlc
        record ['station_var']= dts [i2].text
        record ['station_val']= dds [i2].text
    #    print database, '------------'
    #    scraperwiki.metadata.save('data_columns', ['id', 'station_var', 'station_val'])
        scraperwiki.datastore.save(['id'],record) # save the records one by one
    
        i2=i2+1
        unique_record_id=unique_record_id+1                    
 



    


   
    ##
    #import scraperwiki
    #from BeautifulSoup import BeautifulSoup
    
    # define the order our columns are displayed in the datastore
    #scraperwiki.metadata.save('data_columns', ['Connection time', 'Cycle storage'])
    #scraperwiki.metadata.save('data_columns', ['Connection time', 'Cycle storage', 'Waiting Rooms', 'Web Kiosk'])
    
    
    # scrape_table function: gets passed an individual page to scrape
    #def scrape_table(soup):
    
    #    data_table = soup.find("acc-c expanded-content", { "class" : "zebra" })
    #    data_table = soup.find("table", { "class" : "data" })
    #    rows = data_table.findAll("dt")
    #     rows = soup.findAll("dt")
    #      print "hello0"
    
    #    for row in rows:
            # Set up our data record - we'll need it later
    #        print "hello1"
    #        print row
    #        print "hello2"
    #        record = {}
    #        table_cells = row.findAll("dd")
    ##        table_cells = row.findAll("td")
    #        if table_cells: 
    #            record['Connection time'] = table_cells[0].text
    #            record['Shops'] = table_cells[1].text
    ##            record['Waiting Rooms'] = table_cells[2].text
    ##            record['Web Kiosk'] = table_cells[4].text
    #            # Print out the data we've gathered
    #            print record, '------------'
    #            # Finally, save the record to the datastore - 'Artist' is our unique key
    #            scraperwiki.datastore.save(["Connection time"], record)
    #        
    # scrape_and_look_for_next_link function: calls the scrape_table
    # function, then hunts for a 'next' link: if one is found, calls itself again
    #def scrape_and_look_for_next_link(url):
    #    html = scraperwiki.scrape(url)
    #
    #    print html
    
    #    soup = BeautifulSoup(html)
    #    scrape_table(soup)
    #    next_link = soup.find("a", { "class" : "next" })
    #    print next_link
    #    if next_link:
    #        next_url = base_url + next_link['href']
    #        print next_url
    #        scrape_and_look_for_next_link(next_url)
    
    # ---------------------------------------------------------------------------
    # START HERE: define your starting URL - then 
    # call a function to scrape the first page in the series.
    # ---------------------------------------------------------------------------
    #url_start = 'http://www.nationalrail.co.uk/stations/'
    #print url_start
    #url_end = '/details.html'
    #print url_end
    #starting_url = url_start + url_end
    #print starting_url
    #scrape_and_look_for_next_link(starting_url)
    
#This is the list of ALL codes. Commented here as a store
#tlc_db = ['ABW','ABE','ACY','ABA','ABD','AUR','AVY','ABH','AGV','AGL','AYW','ACR','AAT','ACN','ACH','ACK','ACL','ACG','ACB','ACC','AML','ADD','ADW','ASN','ADM','ADC','ADL','AWK','AIG','ANS','AIN','AIR','ADR','AYP','ALB','ALD','AMT','AHT','AGT','AAP','AXP','ALX','ALF','ALW',
#'ALO','ASS','ALM','ALR','ASG','ALN','ALP','ABC','AON','ALT','ALV','AMB','AMY','AMR','AMF','ANC','AND','ADV','ANZ','AGR','ANG','ANN','ANL','AFV','APP','APD','APF','APB','APS','ARB',
#'ARD','AUI','ADS','ASB','ADN','ADK','AGS','ARG','ARL','AWT','ARN','ARR','ART','ARU','ACT','AUW','ASH','AHV','ABY','ASC','ASF','AFS','AFK','ASY','AHD','AHN','AHS','ANF','AWM','ASK',
#'ALK','ASP','APG','AST','ATH','ATN','ATT','ATB','ATL','AUK','AUD','AUG','AVM','AVF','AVN','AXM','AYS','AVP','AYL','AYH','AYR','BAC','BAJ','BAG','BLD','BIO','BAB','BDK','BAL','BHC',
#'BSI','BMB','BAM','BNV','BAN','BNG','BAH','BAD','BSS','BLL','BAR','BGI','BGD','BKG','BMG','BRM','BNH','BNS','BNI','BTB','BAA','BNL','BNY','BNP','BTG','BRR','BRL','BAV','BIF','BWS','BRY','BYD','BYI','BYL','BAU','BSO','BSK','BBL','BTH','BHG','BTL','BTT','BAK','BAT','BLB','BAY','BCF','BER','BRN','BSD','BSL','BEU','BEL','BEB','BCC','BEC','BKJ','BDM','BSJ','BDH','BMT','BEH','BDW','BEE','BKS','BLV','BLG','BGM','BLH','BLM','BLP','BEG','BVD','BEM','BEY','BEF','BEN','BTY','BYK','BAS','BFE','BKM','BKW','BYA','BBW','BRS','BRK','BWK','BES','BSC','BTO','BET','BYC','BEV','BEX','BXY','BXH','BCS','BIT','BKL','BID','BIW','BBK','BIC','BIL','BIG','BIN','BIY','BCG','BCH','BWD','BIK','BDL','BKC','BKQ','BKN','BKP','BBS','BHI','BMO','BHM','BSW','BIA','BBG','BIS','BIP','BPT','BTE','BBN','BFR','BKH','BHO','BPN','BPB','BPS','BLK','BAW','BFF','BLA','BAI','BKT','BKD','BLT','BLO','BSB','BLY','BLX','BWN','BLN','BYB','BOD','BOR','BOG','BGS','BON','BTD','BKA','BOC','BNW','BOT','BRG','BRH','BOH','BSN','BOE','BTF','BNE','BMH','BRV','BWB','BOP','BWG','BXW','BCE','BDQ','BDI','BOA','BDN','BTR','BTP','BML','BMY','BLE','BMP','BRP','BCN','BND','BSM','BYS','BDY','BRC','BFD','BRE','BWO','BEA','BRO','BGN','BDG','BWT','BDT','BRF','BGG','BGH','BTN','BMD','BNT','BPW','BRI','BHD','RBS','BNF','BRX','BGE','BDB','BSR','BCU','BHS','BCY','BOM','BMR','BMC','BMN','BMS','BMV','BSY','BSP','BPK','BKO','BME','BMF','BRA','BUH','BYF','BXB','BCV','BDA','BGA','BSU','BRW','BRU','BYN','BUC','BCK','BUK','BGL','BHR','BLW','BUE','BUG','BUY','BUW','BNA','BUD','BNM','BUU','BUB','BNC','BYM','BUI','BTS','BCB','BCJ','BUO','BUJ','BUT','BSE','BUS','BHK','BSH','BUL','BPC','BXD','BUX','BFN','BYE','CAD','CGW','CPH','CWS','CDT','CIR','CSK','CDU','CAM','CBN','CBG','CBH','CBL','CMD','CMO','CNL','CAO','CST','CNN','CBE','CBW','CNY','CPU','CBB','CDD','CDB','CDF','CDQ','CDO','CDR','CRF','CAK','CAR','CTO','CLU','CMN','CML','CNF','CAN','CAY','CPK','CAG','CSH','CSB','CRS','CDY','CBP','CLC','CFD','CAS','CSM','CAT','CTF','CFB','CYS','CCT','CTL','CAU','CYB','CTH','CFH','CFO','CHW','CFR','CEF','CPN','CLN','CWC','CHG','CHX','CHC','CBY','CTN','CRT','CSR','CTE','CTM','CHT','CHU','CHE','CED','CEL','CHM','CLD','CNM','CPW','CYT','CHY','CHN','CSN','CSS','CTR','CRD','CHD','CLS','CSW','CNO','CCH','CIL','CHL','CHI','CLY','CPM','CHP','CRK','CIT','CHK','CHO','CRL','CLW','CHR','CHH','CTW','CHF','CTT','CIM','CTK','CLT','CLA','CPY','CLP','CLJ','CPT','CLR','CKS','CLV','CLG','CLE','CEA','CLI','CFN','CLH','CLK','CUW','CYK','CBC','CBS','COA','CSD','CSL','CGN','COL','CET','CEH','CLM','CLL','CNE','CWL','CWB','CME','COM','CNG','CNS','CON','CEY','CNP','CNW','COB','COO','CBR','COE','COP','CRB','COR','CKH','CKL','CPA','CRR','COY','CSY','COS','CSA','CGM','COT','CDS','COV','CWN','COW','CRA','CGD','CRM','CRV','CRW','CRY','CDI','CES','CSG','CWD','CRE','CKN','CWH','CNR','CCC','CRI','CFF','CFT','CMR','CMF','CKT','CRG','CFL','COI','CKY','CMY','CSO','CRH','COH','CWU','CWE','CRN','CRO','CYP','CUD','CUF','CUM','CUA','CUB','CUP','CUH','CUX','CMH','CWM','CYN','DDK','DSY','DAG','DAL','DAK','DAM','DMR','DLR','DLY','DLS','DLK','DLT','DLW','DNY','DCT','DZY','DAR','DAN','DSM','DFD','DRT','DWN','DAT','DVN','DWL','DWW','DEA','DEN','DNN','DGT','DPD','DGY','DHN','DLM','DBD','DNM','DGC','DMK','DNT','DTN','DEP','DBY','DBR','DKR','DPT','DEW','DID','DIG','DMH','DMG','DNS','DGL','DIN','DND','DTG','DSL','DIS','DOC','DOD','DOL','DLH','DLG','DWD','DON','DCH','DCW','DOR','DKG','DKT','DMS','DDG','DVH','DVP','DVC','DVY','DOW','DRG','DYP','DRM','DRF','DRI','DTW','DRO','DMC','DFR','DRU','DMY','DUD','DDP','DFI','DRN','DST','DUL','DBC','DBE','DUM','DMF','DMP','DUN','DBL','DBG','DCG','DEE','DFL','DFE','DKD','DNL','DNO','DOT','DNG','DHM','DUR','DYC','DYF','EAG','EAL','ERL','EAR','EAD','ELD','EWD','ECR','EDY','EDW','EFL','EGF','EGR','EKL','EML','EMD','ETL','EWR','EBN','EBK','EST','ERA','ESL','EGN','EBB','EBV','ECC','ECS','ECL','EDL','EDN','EBR','EBT','EDG','EDB','EDP','EDR','EFF','EGG','EGH','EGT','EPH','ELG','ELP','ELE','ESD','ESW','ELR','ESM','ELS','ELW','ELO','ELY','EMP','EMS','ENC','ENL','ENF','ENT','EPS','EPD','ERD','ERI','ERH','ESH','EXR','ETC','EUS','EBA','EVE','EWE','EWW','EXC','EXD','EXT','EXG','EXM','EXN','EYN','FLS','FRB','FRF','FRL','FRW','FCN','FKG','FKK','FOC','FMR','FAL','FMT','FAM','FRM','FNB','FNN','FNC','FNH','FNR','FNW','FAR','FLD','FAV','FGT','FAZ','FRN','FEA','FLX','FEL','FST','FNT','FEN','FER','FRY','FYS','FFA','FIL','FIT','FNY','FPK','FIN','FSB','FSG','FGH','FSK','FZW','FWY','FLE','FLM','FLN','FLT','FLI','FLF','FKC','FKW','FOD','FOG','FOH','FBY','FOR','FRS','FTM','FTW','FOK','FOX','FXN','FRT','FTN','FRE','FFD','FML','FRI','FZH','FRD','FRO','FLW','FNV','FZP','GNB','GBL','GCH','GRF','GGV','GAR','GRS','GSD','GSN','GSW','GRH','GMG','GTH','GVE','GST','GTY','GTW','GGJ','GER','GDP','GFN','GIG','GBD','GFF','GIL','GLM','GSC','GIP','GIR','GLS','GCW','GLC','GLQ','GLH','GLZ','GLE','GLF','GLG','GLT','GLO','GCR','GLY','GOB','GOD','GDL','GDN','GOE','GOF','GOL','GOM','GMY','GOO','GTR','GDH','GOR','GBS','GTO','GPO','GRK','GWN','GOX','GPK','GOS','GTN','GRA','GRT','GVH','GRV','GRY','GTA','GRB','GRC','GCT','GMV','GMN','GYM','GNL','GNR','GBK','GRL','GNF','GFD','GNH','GKC','GKW','GNW','GEA','GMD','GMB','GRN','GMT','GRP','GUI','GLD','GSY','GUN','GSL','GNT','GWE','GYP','HAB','HCB','HKC','HAC','HKW','HDM','HAD','HDF','HDW','HGF','HAG','HMY','HAL','HAS','HED','HFX','HLG','HID','HLR','HAI','HWH','HMT','HME','HNC','HNW','HMM','HMD','HDH','HMP','HMC','HMW','HIA','HSD','HAM','HND','HTH','HAN','HPN','HRL','HDN','HRD','HLN','HWM','HWN','HRO','HPD','HRM','HGY','HRY','HRR','HGT','HRW','HOH','HTF','HBY','HPL','HTW','HPQ','HWC','HSL','HSK','HGS','HTE','HAT','HFS','HAP','HSG','HTY','HTN','HAV','HVN','HVF','HWD','HWB','HKH','HDB','HYR','HAY','HYS','HYL','HYM','HHE','HAZ','HCN','HDY','HDL','HDG','HLI','HHL','HLL','HTC','HBD','HEC','HDE','HNF','HEI','HLC','HLU','HLD','HMS','HSB','HML','HEN','HNG','HNL','HOT','HEL','HFD','HNB','HNH','HER','HFE','HFN','HES','HSW','HEV','HEW','HEX','HYD','HHB','HIB','HST','HWY','HGM','HIP','HIG','HHY','HTO','HLB','HLF','HLE','HLW','HIL','HLS','HYW','HNK','HIN','HNA','HIT','HGR','HOC','HBN','HOD','HCH','HLM','HOL','HHD','HLY','HMN','HYB','HON','HOY','HPA','HOK','HOO','HPE','HOP','HPT','HOR','HBP','HRN','HRS','HRH','HSY','HIR','HWI','HSC','HGN','HOU','HOV','HXM','HWW','HOW','HOZ','HYK','HBB','HKN','HUD','HUL','HUP','HCT','HGD','HUB','HUN','HNT','HNX','HUR','HUT','HUY','HYC','HYT','HKM','HYN','HYH','IBM','IFI','IFD','ILK','IMW','INC','INE','INT','INS','IGD','ING','INK','INP','INV','INH','INR','IPS','IRL','IRV','ISL','ISP','IVR','IVY','JEQ','JOH','JHN','JOR','KSL','KSN','KEI','KEH','KEL','KVD','KEM','KMH','KMP','KMS','KML','KEN','KLY','KNE','KNS','KNL','KNR','KPA','KTH','KTN','KTW','KNT','KBK','KET','KWB','KWG','KEY','KYN','KDB','KID','KDG','KWL','KBN','KLD','KIL','KGT','KMK','KLM','KPT','KWN','KBC','KGM','KGH','KGX','KGL','KLN','KNN','KGN','KGP','KGS','KGE','KNG','KND','KIN','KIT','KBX','KKS','KIR','KKB','KSW','KBF','KDY','KRK','KKD','KKM','KKH','KKN','KWD','KTL','KIV','KVP','KNA','KBW','KNI','KCK','KNO','KNU','KNF','KYL','LDY','LAD','LAI','LRG','LKE','LAK','LAM','LNK','LAN','LAC','LAW','LGB','LHO','LNY','LGG','LGM','LGS','LGW','LAG','LAP','LPW','LBT','LAR','LRH','LAU','LWH','LAY','LZB','LEG','LEH','LEA','LHM','LMS','LSW','LHD','LED','LEE','LDS','LEI','LIH','LES','LBZ','LEL','LTS','LEN','LNZ','LEO','LET','LEU','LVM','LWS','LEW','LEY','LEM','LER','LIC','LTV','LID','LHS','LCN','LFD','LGD','LIN','LIP','LSK','LIS','LVT','LTK','LTT','LTL','LIT','LVN','LTP','LVC','LVJ','LIV','LSP','LST','LSN','LVG','LLA','LBR','LLT','LNB','LLN','LDN','LLC','LLL','LLV','LLO','LLD','LLJ','LLI','LLE','LLF','LPG','LLG','LLM','LLH','LGO','LLR','LTH','LLS','LWR','LAS','LWM','LNR','LNW','LLW','LLY','LHA','LHE','LCL','LCS','LCG','LCC','LHW','LOC','LCK','LBG','LOF','LRB','LON','LBK','LGE','LPR','LGK','LOB','LNG','LGF','LND','LPT','LGN','LOO','LTG','LOH','LOT','LOS','LBO','LGJ','LOW','LSY','LWT','LUD','LUT','LTN','LUX','LYD','LYE','LYP','LYT','LYC','LYM','LTM','MAC','MCN','MST','MEW','MAG','MDN','MAI','MDB','MDE','MDW','MAL','MLG','MLT','MVL','MIA','MCO','MAN','MCV','MNE','MNG','MNP','MNR','MRB','MAS','MFT','MSW','MCH','MRN','MAR','MHR','MKR','MNC','MKT','MLW','MPL','MSN','MSK','MGN','MTM','MAO','MTO','MYH','MYL','MYB','MRY','MAT','MTB','MAU','MAX','MAY','MZH','MHS','MEL','MKM','MES','MMO','MEN','MNN','MEO','MEC','MEP','MEY','MHM','MER','MEV','MGM','MCE','MEX','MIC','MIK','MBR','MDL','MDG','MLF','MFH','MLH','MIL','MLB','MBK','MIN','MLM','MIH','MLN','MLR','MKC','MFF','MSR','MIR','MIS','MTC','MIJ','MOB','MON','MRS','MTP','MTS','MRF','MOG','MSD','MRP','MRR','MRD','MDS','MCM','MTN','MRT','MIM','MFA','MLY','MPT','MOR','MTL','MSS','MOS','MSL','MSH','MPK','MSO','MTH','MOT','MTG','MLD','MCB','MFL','MTA','MTV','MOO','MUI','MUB','MYT','NFN','NLS','NRN','NAN','NAR','NBR','NVR','NTH','NMT','NEI','NEL','NES','NET','NRT','NTL','NBA','NBC','NBN','NCE','NWX','NXG','NCK','NEH','NHY','NHL','NHE','NLN','NEM','NMC','NMN','NWM','NPD','NSG','NCT','NNG','NBE','NBY','NRC','NCL','NEW','NVH','NVN','NGT','NMK','NWE','NWP','NQY','NSD','NTN','NTA','NAY','NWN','NTC','NLW','NWR','NOA','NWT','NNP','NIT','NBT','NRB','NSB','NOR','NBW','NCM','NDL','NLR','NQU','NRD','NSH','NWA','NWB','NTR','NMP','NFD','NFL','NLT','NUM','NWI','NRW','NWD','NOT','NUN','NHD','NNT','NUT','NUF','OKN','OKM','OKL','OBN','OCK','OLY','OHL','ORN','OLD','OLF','OLM','OLW','OLT','ORE','OMS','ORP','ORR','OPK','OTF','OUN','OUS','OUT','OVE','OVR','OXN','OXF','OXS','OXT','PAD','PDW','PDG','PGN','PCN','PYG','PYJ','PAL','PAN','PNL','PTF','PAR','PBL','PKT','PKS','PSN','PTK','PRN','PWY','PAT','PTT','PEA','PMR','PEG','PEM','PBY','PMB','PMD','PNA','PEN','PCD','PGM','PNE','PNW','PHG','PNS','PKG','PMW','PNM','PER','PRH','PNR','PYN','PES','PHR','PTB','PNY','PNF','PNZ','PRW','PRY','PSH','PTH','PBO','PTR','PET','PEV','PEB','PEW','PIL','PIN','PIT','PSE','PLS','PLK','PLC','PLM','PMP','PLU','PLY','POK','PLG','PSW','PWE','PWW','PLE','PLW','PMT','POL','PON','PTD','PFR','PFM','POT','PLT','PYC','PYP','PPL','PPD','POO','POP','PTG','PSL','PTA','PTC','POR','PTM','PLN','PLD','PMS','PMA','PMH','PPK','PBR','PFY','PYT','PRS','PSC','PRT','PRB','PRE','PRP','PST','PTW','PRA','PTL','PRR','PRL','PRU','PUL','PFL','PUR','PUO','PUT','PWL','PYL','QYD','QBR','QPK','QPW','QRP','QRB','QUI','RDF','RDT','RAD','RDR','RNF','RNM','RAI','RNH','RAM','RGW','RAN','RAU','RAV','RVB','RVN','RWC','RLG','RAY','RDG','RDW','REC','RDB','RCC','RCE','RDN','RDS','RDC','RDH','RDA','RED','RHM','REE','REI','RTN','RET','RHI','RIA','RHO','RHL','RHY','RHD','RIL','RMD','RIC','RDD','RID','RDM','RCA','RIS','RBR','ROB','RCD','ROC','RTR','RFD','RFY','ROG','ROR','ROL','RMB','RMF','RML','ROM','ROO','RSG','RSH','ROS','RMC','RNR','RLN','ROW','RYB','RYN','RYS','RUA','RUF','RUG','RGT','RGL','RUN','RUE','RKT','RUS','RUT','RYD','RYP','RYR','RRB','RYE','RYH','SFD','SLD','SAF','SAH','SAL','SAE','STS','SLB','SLT','SAM','SLW','SNA','SDB','SNR','SDL','SND','SDG','SAN','SDP','SAD','SDW','SDY','SNK','SQH','SRR','SDF','SDR','SAW','SXY','SAX','SCA','SCT','SCH','SCU','SML','SEF','SFL','SEA','SEM','SSC','SEC','SRG','SBY','SRS','SEL','SEG','SLY','SET','SVK','SVS','SEV','SVB','STJ','SFR','SHN','SHA','SHW','SHL','SSS','SHF','SED','SNF','SEN','SPB','SPH','SPY','SHP','STH','SHE','SIE','SHM','SLS','SDM','SFN','SHD','SHI','SHY','SPP','SIP','SHB','SHH','SRO','SRL','SRY','SHO','SEH','SSE','SRT','SHT','SHS','SHR','SID','SIL','SIC','SLK','SLV','SVR','SIN','SIT','SKG','SKE','SKI','SGR','SWT','SLA','SLR','SLH','SLO','SMA','SAB','SGB','SMR','SMI','SMB','SNI','SDA','SWO','SOR','SOL','SYT','SAT','SBK','SBM','SCY','SES','SGN','SGL','SOH','SOK','SMO','SOM','SRU','STO','SWS','STL','SOA','SOU','SOB','SBU','SEE','SOC','SOE','SOV','SMN','SOP','SWK','SOW','SPA','SBR','SPI','SPO','SPN','SRI','SPR','SPF','SQU','SAA','SAC','SAR','SAS','SAU','SBS','SBF','SBV','SCR','SDN','SER','SGM','SNH','SHJ','SIH','SIV','SJP','SJS','SAJ','SKN','SLQ','SMG','SMT','SMY','STM','SNO','STP','STA','SNS','SLL','SYB','SMD','SMH','SFO','SNT','SSD','SST','SPU','SRD','SBE','SCS','SVL','SCF','SON','SPS','SVG','STV','SWR','STT','STG','SPT','SKS','SSM','STK','SKM','SKW','SOT','SNE','SCG','SBP','SOG','STN','SHU','SNL','SBJ','SBT','SMK','STR','SRA','SFA','SAV','STC','STW','STE','SRC','SRH','SHC','SRN','STF','SOO','STD','STU','SYA','SUY','SUD','SDH','SUG','SUM','SUU','SUN','SUP','SNG','SNY','SUR','SUO','SUT','SUC','SPK','SWL','SAY','SWM','SWA','SNW','SWY','SWG','SWD','SWI','SWE','SNN','SWN','SYD','SYH','SYL','SYS','TAC','TAD','TAF','TAI','TAL','TLB','TLC','TAB','TAM','TAP','TAT','TAU','TAY','TED','TEA','TGM','TFC','TMC','TEN','TEY','THD','THA','THH','THW','TLK','THE','TEO','TTF','THI','TBY','TNN','TNS','THO','THB','TNA','TTH','THT','TPB','TPC','TLS','TBD','TOK','THU','THC','THS','TRS','TIL','THL','TLH','TIP','TIR','TIS','TVP','TOD','TOL','TPN','TON','TDU','TNF','TNP','TOO','TOP','TQY','TRR','TOT','TOM','TTN','TWN','TRA','TRF','TRE','TRH','TRB','TRY','TRM','TRI','TRD','TRN','TRO','TRU','TUL','TUH','TBW','TUR','TUT','TWI','TWY','TYC','TGS','TYG','TYL','TYS','TYW','UCK','UDD','ULC','ULL','ULV','UMB','UNI','UHA','UPL','UPM','UPH','UHL','UTY','UWL','UPT','UPW','URM','UTT','VAL','VXH','VIC','VIR','WDO','WAD','WFL','WKK','WKF','WKD','WLG','WLV','WLT','WAF','WAM','WSL','WDN','WLC','WHC','WMW','WAO','WON','WAL','WAN','WSW','WWR','WNT','WNP','WBL','WAR','WRM','WGV','WMN','WNH','WBQ','WAC','WRW','WRP','WTO','WBC','WTR','WAT','WAE','WLO','WFH','WFJ','WFN','WTG','WAS','WNG','WAV','WEE','WET','WMG','WLI','WEL','WLN','WLP','WGC','WLW','WEM','WMB','WCX','WMS','WND','WNN','WSA','WBP','WBY','WCL','WCY','WDT','WDU','WEA','WEH','WHD','WHP','WHR','WKB','WKI','WMA','WNW','WRU','WRN','WLD','WSU','WWI','WWO','WSB','WCF','WCB','WHA','WTA','WFI','WES','WGA','WHG','WNM','WSM','WRL','WYB','WEY','WBR','WHE','WTS','WFF','WHM','WNL','WHN','WTB','WCH','WTC','WHT','WHL','WNY','WCR','WTH','WTL','WBD','WTE','WHI','WLE','WLF','WTN','WWL','WHY','WHS''WCK','WIC','WCM','WDD','WID','WMR','WGN','WGW','WGT','WMI','WIJ','WLM','WIL','WMC','WML','WNE','WIM','WBO','WSE','WIN','WNF','WIH','WDM','WNC','WNR','WNS','WTI','WSF','WSH','WTM','WTY','WTT','WVF','WIV','WOB','WOK','WKM','WOH','WVH','WOL','WOM','WDE','WST','WDB','WGR','WDL','WDF','WDH','WDS','WLY','WME','WSR','WOO','WLS','WWA','WWD','WWW','WOF','WCP','WOS','WKG','WRK','WOR','WPL','WRT','WRH','WRB','WRY','WRE','WRS','WXC','WRX','WYE','WYM','WYL','WMD','WYT','YAL','YRD','YRM','YAE','YAT','YEO','YVJ','YVP','YET','YNW','YOK','YRK','YRT','YSM','YSR']
#
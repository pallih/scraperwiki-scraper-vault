import scraperwiki
import re
from bs4 import BeautifulSoup # documentation at http://www.crummy.com/software/BeautifulSoup/bs4/doc/

# Names to check (short list)

companies= ['AAL.L',
'ABF.L',       'ADM.L',       'ADN.L',       'AGK.L',       'AMEC.L',       'ANTO.L',       'ARM.L',       'AV.L',       'AZN.L',       'BA.L',       'BAB.L',       'BARC.L',       'BATS.L',       'BG.L',       'BLND.L',       'BLT.L',       'BNZL.L',       'BP.L',       'BRBY.L',       'BSY.L',       'BT-A.L',       'CCL.L',       'CNA.L',       'CPG.L',       'CPI.L',       'CRDA.L',       'CRH.L',       'CSCG.L',       'DGE.L',       'ENRC.L',       'EVR.L',       'EXPN.L',       'FRES.L',       'GFS.L',       'GKN.L',       'GLEN.L',       'GSK.L',       'HL.L',       'HMSO.L',       'HSBA.L',       'IAG.L',       'IHG.L',       'IMI.L',       'IMT.L',       'ITRK.L',       'ITV.L',       'JMAT.L',       'KAZ.L',       'KGF.L',       'LAND.L',       'LGEN.L',       'LLOY.L',       'MGGT.L',       'MKS.L',       'MRO.L',       'MRW.L',       'NG.L',       'NXT.L',       'OML.L',       'PFC.L',       'PNN.L',       'POLY.L',       'PRU.L',       'PSON.L',       'RB.L',       'RBS.L',       'RDSA.L',       'RDSB.L',       'REL.L',       'REX.L',       'RIO.L',       'RR.L',       'RRS.L',       'RSA.L',       'RSL.L',       'SAB.L',       'SBRY.L',       'SDR.L',       'SGE.L',       'SHP.L',       'SL.L',       'SMIN.L',       'SN.L',       'SRP.L',       'SSE.L',       'STAN.L',       'SVT.L',       'TATE.L',       'TLW.L',       'TSCO.L',       'ULVR.L',       'UU.L',       'VED.L',       'VOD.L',       'WEIR.L',       'WG.L',       'WOS.L',       'WPP.L',       'WTB.L',       'XTA.L',       '3IN.L',       'ABG.L',       'AFR.L',       'AGS.L',       'AHT.L',       'AIE.L',       'AML.L',       'ASHM.L',       'ASL.L',       'ATK.L',       'ATST.L',       'AVV.L',       'AZEM.L',       'BABS.L',       'BAG.L',       'BBA.L',       'BBY.L',       'BDEV.L',       'BET.L',       'BEZ.L',       'BGEO.L',       'BHGG.L',       'BHGU.L',       'BHME.L',       'BHMG.L',       'BHMU.L',       'BKG.L',       'BNKR.L',       'BOK.L',       'BOY.L',       'BPTY.L',       'BRSN.L',       'BRW.L',       'BRWM.L',       'BSET.L',       'BTEM.L',       'BTG.L',       'BUMI.L',       'BVIC.L',       'BVS.L',       'BWNG.L',       'BWY.L',       'BYG.L',       'CAPC.L',       'CBG.L',       'CCC.L',       'CEY.L',       'CGL.L',       'CHG.L',       'CKSN.L',       'CLDN.L',       'CLLN.L',       'CNE.L',       'COB.L',       'COLT.L',       'CPR.L',       'CSR.L',       'CTY.L',       'CWC.L',       'CWK.L',       'DAB.L',       'DCG.L',       'DEB.L',       'DIA.L',       'DJAN.L',       'DLAR.L',       'DLN.L',       'DNLM.L',       'DNO.L',       'DOM.L',       'DPH.L',       'DPLM.L',       'DRX.L',       'DTY.L',       'DVO.L',       'DXNS.L',       'ECM.L',       'EDIN.L',       'EFM.L',       'ELM.L',       'ELTA.L',       'EMG.L',       'ENQ.L',       'ERM.L',       'ESSR.L',       'EZJ.L',       'FCAM.L',       'FCPT.L',       'FCSS.L',       'FDSA.L',       'FENR.L',       'FEV.L',       'FGP.L',       'FLTR.L',       'FRCL.L',       'FXPO.L',       'GFRD.L',       'GNK.L',       'GNS.L',       'GOG.L',       'GPOR.L',       'GRG.L',       'GRI.L',       'GSS.L',       'HAS.L',       'HFD.L',       'HGG.L',       'HICL.L',       'HIK.L',       'HLMA.L',       'HOC.L',       'HOIL.L',       'HOME.L',       'HRI.L',       'HSTN.L',       'HSV.L',       'HSX.L',       'HTG.L',       'HWDN.L',       'IAP.L',       'ICP.L',       'IGG.L',       'III.L',       'IMG.L',       'INCH.L',       'INF.L',       'INPP.L',       'INVP.L',       'IPF.L',       'IPO.L',       'IRV.L',       'ISAT.L',       'ISYS.L',       'ITE.L',       'JAM.L',       'JD.L',       'JDW.L',       'JII.L',       'JLIF.L',       'JLT.L',       'JMG.L',       'JUP.L',       'KCOM.L',       'KENZ.L',       'KIE.L',       'KMR.L',       'LAD.L',       'LMI.L',       'LRD.L',       'LRE.L',       'LSE.L',       'LSP.L',       'LWDB.L',       'MAB.L',       'MARS.L',       'MCRO.L',       'MGCR.L',       'MLC.L',       'MNDI.L',       'MNKS.L',       'MNZS.L',       'MONY.L',       'MPI.L',       'MRC.L',       'MRCH.L',       'MTO.L',       'MUT.L',       'MYI.L',       'NBLS.L',       'NEX.L',       'NMC.L',       'NWR.L',       'OCDO.L',       'OPHR.L',       'OXIG.L',       'PAG.L',       'PAY.L',       'PCT.L',       'PDL.L',       'PER.L',       'PFG.L',       'PFL.L',       'PHNX.L',       'PIC.L',       'PLI.L',       'PMO.L',       'PNL.L',       'POG.L',       'PSN.L',       'PTEC.L',       'PZC.L',       'QQ.L',       'RAT.L',       'RCP.L',       'RDW.L',       'RGU.L',       'RMV.L',       'RNK.L',       'ROR.L',       'RPC.L',       'RPO.L',       'RPS.L',       'RSW.L',       'RTN.L',       'RTO.L',       'RUS.L',       'SCIN.L',       'SDL.L',       'SGC.L',       'SGP.L',       'SGRO.L',       'SHB.L',       'SHI.L',       'SIA.L',       'SKS.L',       'SMDR.L',       'SMDS.L',       'SMP.L',       'SMT.L',       'SMWH.L',       'SNR.L',       'SPD.L',       'SPT.L',       'SPX.L',       'STJ.L',       'STOB.L',       'SVI.L',       'SVS.L',       'SXS.L',       'SYR.L',       'TALK.L',       'TALV.L',       'TCY.L',       'TED.L',       'TEM.L',       'TEP.L',       'TLPR.L',       'TMPL.L',       'TPK.L',       'TRY.L',       'TRYS.L',       'TT.L',       'TW.L',       'UBM.L',       'UEM.L',       'UKCM.L',       'ULE.L',       'UTG.L',       'VCT.L',       'WKP.L',       'WMH.L',       'WTAN.L',       'WWH.L',       'YULC.L']




for company in companies:
    
    link = 'http://uk.finance.yahoo.com/q/pr?s=' + company 
    print link

    link2 = 'http://uk.finance.yahoo.com/q/ks?s=' + company 
    print link2
    span_marketcap_id = 'yfs_j10_' + company.lower()
    html2 = scraperwiki.scrape(link2)
    soup2 = BeautifulSoup(html2)
    s = soup2.find("span", { "id" : span_marketcap_id })
    print s
    exercise="N/A"
    revenue="N/A"
    MostRecentQuarter = "N/A"

    if s is not None:
        exercise = s.get_text().strip()

    s = soup2.find(text = 'Revenue (ttm):' ) 
    if s is not None:
        revenue = s.findNext('td').contents[0]

    s = soup2.find(text = 'Most Recent Quarter (mrq):' )
    if s is not None:
        MostRecentQuarter = s.findNext('td').contents[0]
    
    sector="N/A"
    industry="N/A"
    industry="N/A"
    namerole="N/A"
    salary="N/A"

    
    html = scraperwiki.scrape(link)
    #print html
    soup = BeautifulSoup(html)
    print soup
        
    ps = soup.find_all('td')
    #print ps[0]
    k = 0
    first_time = 0
    for p in ps:
        #print ps[k].get_text().strip()
        if "Sector:" == ps[k].get_text().strip():
            sector =  ps[k+1].get_text().strip()
            print sector 
        if "Industry:" == p.get_text().strip():
            industry =  ps[k+1].get_text().strip()       
            print industry 
        if "Chief" in p.get_text().strip():
            if first_time == 2:
                namerole =  ps[k].get_text().replace('\n','').strip()
                namerole = ' '.join(namerole.split())
                salary =  ps[k+1].get_text().strip()  
                #exercise = ps[k+2].get_text().strip() 
                print namerole 
                print salary
                print exercise
            first_time = first_time+1
        k = k+1

    data = {"Company Code": company, "Sector": sector, "Industry": industry, "NameRole": namerole, "Salary": salary, "Market cap": exercise, "Revenue": revenue, "Most recent quarter for Rev ttm": MostRecentQuarter}
    print data 
    scraperwiki.sqlite.save(['Company Code'], data)



###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree

sumReport = "http://www.cqc.org.uk/_db/_documents/NHS_staff_survey_2010_%s_sum.pdf"
fullReport = "http://www.cqc.org.uk/_db/_documents/NHS_staff_survey_2010_%s_full.pdf"

codes_string ="""RLN RXP 5ND 5J9 RR7 5KF 5D9 5KM 5D7 RX6 Q30 RVW 5D8 TAC RX4 RTF 5QR RTR RE9 5KG 5E1 5KL RX3 RTD RTV REM RBS RY2 5HG TAP 5HP RXL 5HQ 5JX RJX 5NP 5NG RW3 RXA REN RJR RNN 5NE RJN RXR 5NH RXV 5NM 5NQ 5J4 RW5 RXN RY1 RBQ 5NL REP TAE 5NT RW4 RBT RNL 5NF RX7 Q31 5J5 RW6 RT2 RMC RQ6 5F5 RM3 5NJ RVY RBN RWJ 5F7 5LH RMP RBV RET RM4 5NR RM2 RTX RWW 5J2 5NN 5NK RBL RRF RCF RFF 5JE 5NY TAD RAE RWY 5J6 NNF RP5 5N5 5NW RCD RWA 5NX RV9 5N2 RGD 5N1 RR8 RXF TAN 5EF 5NV RJL 5H8 RXE RCC RCU TAH 5N4 RHQ RXG RFR 5N3 RCB RX8 Q32 5ET 5N7 RTG 5N6 RXM RX9 Q33 RNQ 5PC 5PA RT5 RP7 5N9 RNS RP1 5PD 5EM RX1 5N8 RHA RK5 RWD RWE RXT RQ3 RYW 5PG RLU RJF RYG 5MD RYK 5PE RLT 5MX RR1 RLQ 5CN RJD RLY 5PH RL1 RXK TAJ 5PF RXW 5M2 5QW 5M1 RRE 5PK RJC 5PJ 5MK RNA RRJ RL4 RRK RJE RKB RBK 5M3 5PM RYA Q34 5MV RWP RWQ 5PL RDD RC1 5P2 RGT RT1 RYV 5PP RDE RWH RYC Q35 5PR RWR 5QV RQQ RGQ RGP RC9 5GC RQ8 5PX RM1 RMY 5PQ 5PW RRD RGM RGN 5PN 5P1 RWN 5PY RAJ RT6 5PT RQW RCX 5PV RWG RGR 5C2 RF4 RVL 5A9 RRP RNJ TAK 5K5 5A7 TAF 5K7 RV3 RYX RQM 5C3 RJ6 5K9 RC3 5HX RWK 5C1 RVR RP4 5A8 RJ1 5H1 5C9 5K6 5A4 5AT RQX 5HY RYJ 5K8 5LA RJZ RAX 5A5 5LD RJ2 5LF RRU Q36 5C5 RNH RAT RAP RV8 RPG 5NA 5M6 RT3 RAL RAN RV5 RYQ RQY 5LE RJ7 5M7 RNK RAS RPY RKE 5C4 RRV 5NC 5LG RKL RFW 5LC RGC NNV RTK 5LQ RXH RN7 RVV 5P7 RXC 5QA RDU 5P8 RXY RWF RPA 5L3 RPC RA2 RYD Q37 RXX RTP 5P5 RDR RX2 5P9 5P6 RYR RN5 5QG RWX 5QF RXQ 5QD RW1 5QC RD7 5QT RD8 5CQ RBF RTH RNU RHX 5QE 5FE RHU RHW RYE Q38 5L1 RHM RN1 RTQ RVN 5FL 5QN 5QJ 5QP RJ8 RWV 5QQ RBD RDY 5QM RTE 5QH RX5 RN3 RVJ 5M8 RBZ RK9 5F1 RD3 REF RH8 RBB RD1 RNZ RH5 5QL RA9 5A3 Q39 RYF 5K3 RBA RDZ TAL RA7 RA3 5QK RA4 T1310 T1160 T1240 T1190 T1460 T1450 X09 RYH T1150 T1430 T1440"""
codes_list = codes_string.split()

KFs = ["KF%s" % x for x in range(1,39)]
KFtable = "Table A2:"

# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        #res.append("<%s>" % lel.tag) ## don't want tags here!
        res.append(gettext_with_bi_tags(lel))
        #res.append("</%s>" % lel.tag) ## or here!
        if el.tail:
            res.append(el.tail)
    return "".join(res)

def getElemsUntil(ListOfElements,index,stopMatch):
    out = []
    for i,el in enumerate(ListOfElements[index:]):
        item = gettext_with_bi_tags(el).lstrip("* ")
        if item.startswith(stopMatch) and i>0:
            return out
        elif item[-1].isalpha() and i>0:
            out[-1] = out[-1] + item
        else:
            out.append(item)
    return out

for cl in codes_list[0:1]: # limited to first code for testing

    try:

        url = fullReport % cl
        pdfdata = urllib2.urlopen(url).read()
        ##print "The pdf file has %d bytes" % len(pdfdata)
    
        xmldata = scraperwiki.pdftoxml(pdfdata)
        ##print "After converting to xml it has %d bytes" % len(xmldata)
        ##print "The first 2000 characters are: ", xmldata[:2000]
    
        root = lxml.etree.fromstring(xmldata)
        pages = list(root)
    
        #print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]
        print "Report for %s has %s pages" % (cl,len(pages))

    except:
        print "ERROR: report for %s cannot be found" % cl
        break

    store = []
    for page in pages[50:52]:  #assume that only pages 51-52 have table A2
        
        elementList = list(page)

        for kf in KFs:
            for i,el in enumerate(elementList):
                #print el.attrib, el.tag, el.text, el.tail
                if el.tag == "text":
                    item = gettext_with_bi_tags(el)
                    if item.startswith(kf) or item.startswith("* " + kf):
                        store.append(getElemsUntil(elementList,i,"KF"))
                        break


    print "\n".join([str(x) for x in store])



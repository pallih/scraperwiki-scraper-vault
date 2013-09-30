import scraperwiki

import pycurl
import re
import StringIO
import sys
c = pycurl.Curl()

pdflist = []

#Ottieni prima pagina
SEARCHURL = 'http://www.bur.liguriainrete.it/Ricerca.asp'
POSTDATA = 'DTINIZIO=01%2F01%2F1901&DTFINE=31%2F12%2F2077&ANNO=&PARTE=&NUMBOLL=&TIPO=&SUPPL=&OGGETTO=&ARGO=&TIPOENTE=&ENTE=&TIPOATTO=&NUMATTO=&DTATTO=&TESTO=&submit1=Ricerca'
FILTRO = '"<%2Fi>%2C+Data+Bollettino+>%3D+<i>"01%2F01%2F1901"<%2Fi>%2C+Data+Bollettino+<%3D+<i>"31%2F12%2F2077'
c.setopt(pycurl.URL, SEARCHURL)
#c.setopt(pycurl.HTTPHEADER, ["Accept:"])
b = StringIO.StringIO()
c.setopt(pycurl.WRITEFUNCTION, b.write)
c.setopt(pycurl.FOLLOWLOCATION, 1)
c.setopt(pycurl.MAXREDIRS, 5)


c.setopt(pycurl.POST, 1)
c.setopt(pycurl.POSTFIELDS, POSTDATA)
c.setopt(pycurl.COOKIEJAR, "cookiejar")
c.perform()
htmlcode = b.getvalue()

#Process prima pagina
sys.stderr.write('Processing 1\n')
pagTotAll = re.findall('<a href="javascript:SceltaPagina\\(\\d+,(\\d+)\\);"',htmlcode)
pagTot = pagTotAll[0]
PosCorrAll = re.findall('<input TYPE="HIDDEN" NAME="PosCorr" VALUE="(.+)">',htmlcode)
PosCorr = PosCorrAll[0]
PosIniAll = re.findall('<input TYPE="HIDDEN" NAME="PosIni" VALUE="(.+)">',htmlcode)
PosIni = PosIniAll[0]

#Get pdf address 
occ = re.findall("javascript:ViewDoc\\('(http://.*.pdf)'\\)",htmlcode)
pdflist.extend(occ)
#print occ

c.setopt(pycurl.POST, 0)

for i in range(2,int(pagTot)+1):
        sys.stderr.write("Processing " + str(i) + ' of ' + str(int(pagTot)) + '\n')
        #Se deve cambiare PosIni
        if( i == int(PosIni) + 10 ):
                PosIni = str(int(PosIni) + 10);
        SEARCHURL = 'http://www.bur.liguriainrete.it/Ricerca.asp?qu=&pg=' + str(i) + '&filtro=' + FILTRO + '&tipo=BUR&PosCorr=' + PosCorr + '&PosIni=' + PosIni
        c.setopt(pycurl.URL, SEARCHURL)
        #c.setopt(pycurl.HTTPHEADER, ["Accept:"])
        b = StringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.MAXREDIRS, 5)

        c.perform()
        htmlcode = b.getvalue()
        pycurl.global_cleanup()


        PosCorrAll = re.findall('<input TYPE="HIDDEN" NAME="PosCorr" VALUE="(.+)">',htmlcode)
        PosCorr = PosCorrAll[0]
        PosIniAll = re.findall('<input TYPE="HIDDEN" NAME="PosIni" VALUE="(.+)">',htmlcode)
        PosIni = PosIniAll[0]

        #Get pdf address 
        occ = re.findall("javascript:ViewDoc\\('(http://.*)'\\)",htmlcode)
        #print occ
        pdflist.extend(occ)

#create list of dicts from list of strings 
data = [ {"URL":s}  for s in pdflist ]           


scraperwiki.sqlite.save(["URL"], data)
#for inte in pdflist:
#        print "<a href=\"" + inte + "\">" + inte + "</a><br />"

        

import scraperwiki

import pycurl
import re
import StringIO
import sys
c = pycurl.Curl()

pdflist = []

#Ottieni prima pagina
SEARCHURL = 'http://www.bur.liguriainrete.it/Ricerca.asp'
POSTDATA = 'DTINIZIO=01%2F01%2F1901&DTFINE=31%2F12%2F2077&ANNO=&PARTE=&NUMBOLL=&TIPO=&SUPPL=&OGGETTO=&ARGO=&TIPOENTE=&ENTE=&TIPOATTO=&NUMATTO=&DTATTO=&TESTO=&submit1=Ricerca'
FILTRO = '"<%2Fi>%2C+Data+Bollettino+>%3D+<i>"01%2F01%2F1901"<%2Fi>%2C+Data+Bollettino+<%3D+<i>"31%2F12%2F2077'
c.setopt(pycurl.URL, SEARCHURL)
#c.setopt(pycurl.HTTPHEADER, ["Accept:"])
b = StringIO.StringIO()
c.setopt(pycurl.WRITEFUNCTION, b.write)
c.setopt(pycurl.FOLLOWLOCATION, 1)
c.setopt(pycurl.MAXREDIRS, 5)


c.setopt(pycurl.POST, 1)
c.setopt(pycurl.POSTFIELDS, POSTDATA)
c.setopt(pycurl.COOKIEJAR, "cookiejar")
c.perform()
htmlcode = b.getvalue()

#Process prima pagina
sys.stderr.write('Processing 1\n')
pagTotAll = re.findall('<a href="javascript:SceltaPagina\\(\\d+,(\\d+)\\);"',htmlcode)
pagTot = pagTotAll[0]
PosCorrAll = re.findall('<input TYPE="HIDDEN" NAME="PosCorr" VALUE="(.+)">',htmlcode)
PosCorr = PosCorrAll[0]
PosIniAll = re.findall('<input TYPE="HIDDEN" NAME="PosIni" VALUE="(.+)">',htmlcode)
PosIni = PosIniAll[0]

#Get pdf address 
occ = re.findall("javascript:ViewDoc\\('(http://.*.pdf)'\\)",htmlcode)
pdflist.extend(occ)
#print occ

c.setopt(pycurl.POST, 0)

for i in range(2,int(pagTot)+1):
        sys.stderr.write("Processing " + str(i) + ' of ' + str(int(pagTot)) + '\n')
        #Se deve cambiare PosIni
        if( i == int(PosIni) + 10 ):
                PosIni = str(int(PosIni) + 10);
        SEARCHURL = 'http://www.bur.liguriainrete.it/Ricerca.asp?qu=&pg=' + str(i) + '&filtro=' + FILTRO + '&tipo=BUR&PosCorr=' + PosCorr + '&PosIni=' + PosIni
        c.setopt(pycurl.URL, SEARCHURL)
        #c.setopt(pycurl.HTTPHEADER, ["Accept:"])
        b = StringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.MAXREDIRS, 5)

        c.perform()
        htmlcode = b.getvalue()
        pycurl.global_cleanup()


        PosCorrAll = re.findall('<input TYPE="HIDDEN" NAME="PosCorr" VALUE="(.+)">',htmlcode)
        PosCorr = PosCorrAll[0]
        PosIniAll = re.findall('<input TYPE="HIDDEN" NAME="PosIni" VALUE="(.+)">',htmlcode)
        PosIni = PosIniAll[0]

        #Get pdf address 
        occ = re.findall("javascript:ViewDoc\\('(http://.*)'\\)",htmlcode)
        #print occ
        pdflist.extend(occ)

#create list of dicts from list of strings 
data = [ {"URL":s}  for s in pdflist ]           


scraperwiki.sqlite.save(["URL"], data)
#for inte in pdflist:
#        print "<a href=\"" + inte + "\">" + inte + "</a><br />"

        


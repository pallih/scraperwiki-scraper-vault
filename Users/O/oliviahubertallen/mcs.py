from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
import datetime
from unidecode import unidecode
from bs4 import BeautifulSoup

TABLENUMS = [1,2,5,31,22,13,16,19,4,3]

entry = """
<html xmlns:j="http://courts.state.md.us">
<head>
<META http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link type="text/css" rel="stylesheet" href="css/inquiry-detail.css">
<title>Case Information </title>
</head>
<body>
<div class="BodyWindow">
<div class="Header">DISTRICT COURT OF MARYLAND </div>
<div>
<center>
<a href="javascript:history.go(-1)">Go Back</a>
</center>
</div>
<table>
<tr>
<td>
<H5>Case Information</H5>
</td>
</tr>
</table>
<table>
<tr>
<td><span class="FirstColumnPrompt">Court System:</span></td><td><span class="Value">DISTRICT COURT FOR
                            BALTIMORE CITY  -
                            CRIMINAL  SYSTEM </span></td>
</tr>
</table>
<table>
<tr>
<td><span class="FirstColumnPrompt">Case Number:</span></td><td><span class="Value">4B02167750</span><span class="Prompt">Tracking No:</span><span class="Value">126105493393</span></td>
</tr>
<tr>
<td><span class="FirstColumnPrompt">Case Type:</span></td><td><span class="Value">CRIMINAL</span></td>
</tr>
<tr>
<td><span class="FirstColumnPrompt">District Code:</span></td><td><span class="Value">01</span><span class="Prompt">Location Code:</span><span class="Value">03</span></td>
</tr>
<tr>
<td><span class="FirstColumnPrompt">Document Type:</span></td><td><span class="Value">STATEMENT OF CHARGES</span><span class="Prompt">Issued Date:</span><span class="Value">03/29/2012</span></td>
</tr>
<tr>
<td><span class="FirstColumnPrompt">Case Status:</span></td><td><span class="Value">ACTIVE</span></td>
</tr>
</table>
<HR>
<table>
<tr>
<td>
<H5>Defendant Information</H5>
</td>
</tr>
</table>
<table>
<tr>
<td><span class="FirstColumnPrompt">Defendant Name:</span></td><td><span class="Value">ASENCIO, RANDOLFO</span></td>
</tr>
</table>
<table>
<tr>
<td><span class="FirstColumnPrompt">Race:</span></td><td><span class="Value">WHITE, CAUCASIAN, ASIATIC INDIAN, ARAB</span></td>
</tr>
<tr>
<td><span class="FirstColumnPrompt">Sex:</span></td><td><span class="Value">M</span><span class="Prompt">Height:</span><span class="Value">510</span><span class="Prompt">Weight:</span><span class="Value">165</span><span class="Prompt">DOB:</span><span class="Value">10/24/1974</span></td>
</tr>
</table>
<table>
<tr></tr>
<tr>
<td><span class="FirstColumnPrompt">Address:</span></td><td><span class="Value">5318 KING ARTHUR CIR</span></td>
</tr>
<tr>
<td><span class="FirstColumnPrompt">City:</span></td><td><span class="Value">ROSEDALE</span><span class="Prompt">State:</span><span class="Value">MD</span><span class="Prompt">Zip Code:</span><span class="Value">21237 - 0000</span></td>
</tr>
</table>
<hr>
<table>
<tr>
<td>
<H5>Court Scheduling Information</H5>
</td>
</tr>
</table>
<table>
<tr>
<td><span class="FirstColumnPrompt">Trial Date:</span></td><td><span class="Value">05/10/2012</span><span class="Prompt">Trial Time:</span><span class="Value">08:30 AM</span><span class="Prompt">Room:</span><span class="Value">1</span></td>
</tr>
</table>
<table>
<tr>
<td><span class="FirstColumnPrompt">Trial Type: </span></td><td><span class="Value"></span></td>
</tr>
<table></table>
<tr>
<td><span class="FirstColumnPrompt">Trial Location:</span></td><td><span class="Value">1400 E. NORTH AVE       BALTIMORE       21213-1400</span></td>
</tr>
</table>
<HR>
<table>
<tr>
<td>
<H5>Charge and Disposition Information</H5>
</td>
</tr>
</table>
<div class="InfoChargeStatement">
           (Each Charge is listed separately. The disposition is listed below the Charge)<BR>
</div>
<div class="AltBodyWindow1">
<table>
<tr>
<td><span class="FirstColumnPrompt">Charge No:</span></td><td><span class="Value">001</span><span class="Prompt">Description:</span><span class="Value">CDS:POSSESS-NOT MARIHUANA</span></td>
</tr>
</table>
<table>
<tr>
<td><span class="FirstColumnPrompt">Statute:</span></td><td><span class="Value">CR.5.601.(a)(1)</span><span class="Prompt">Description:</span><span class="Value">CDS:POSSESS-NOT MARIHUANA</span></td>
</tr>
<tr>
<td><span class="FirstColumnPrompt">Amended Date:</span></td><td><span class="Value"></span><span class="Prompt">CJIS Code:</span><span class="Value">4 3550</span><span class="Prompt">MO/PLL:</span><span class="Value"></span><span class="Prompt">Probable Cause:</span><span class="Value">X</span></td>
</tr>
</table>
<table>
<tr>
<td><span class="FirstColumnPrompt">Incident Date From: </span></td><td><span class="Value">03/29/2012</span></td><td><span class="Prompt">To: </span></td><td><span class="Value">03/29/2012</span></td><td><span class="Prompt">Victim Age: </span></td><td><span class="Value"></span></td>
</tr>
</table>
<table></table>
</div>
<HR>
<div class="AltBodyWindow1">
<table>
<tr>
<td><span class="FirstColumnPrompt">Charge No:</span></td><td><span class="Value">002</span><span class="Prompt">Description:</span><span class="Value">CDS:POSSESS-NOT MARIHUANA</span></td>
</tr>
</table>
<table>
<tr>
<td><span class="FirstColumnPrompt">Statute:</span></td><td><span class="Value">CR.5.601.(a)(1)</span><span class="Prompt">Description:</span><span class="Value">CDS:POSSESS-NOT MARIHUANA</span></td>
</tr>
<tr>
<td><span class="FirstColumnPrompt">Amended Date:</span></td><td><span class="Value"></span><span class="Prompt">CJIS Code:</span><span class="Value">4 3550</span><span class="Prompt">MO/PLL:</span><span class="Value"></span><span class="Prompt">Probable Cause:</span><span class="Value">X</span></td>
</tr>
</table>
<table>
<tr>
<td><span class="FirstColumnPrompt">Incident Date From: </span></td><td><span class="Value">03/29/2012</span></td><td><span class="Prompt">To: </span></td><td><span class="Value">03/29/2012</span></td><td><span class="Prompt">Victim Age: </span></td><td><span class="Value"></span></td>
</tr>
</table>
<table></table>
</div>
<HR>
<H5>Related Person Information</H5>
<div class="InfoChargeStatement">
           (Each Person related to the case other than the Defendant is shown)<BR>
</div>
<table>
<tr>
<td><span class="FirstColumnPrompt">Name:</span><span class="Value"></span></td>
</tr>
<tr>
<td><span class="FirstColumnPrompt">Connection:</span><span class="Value">WITNESS/POLICE OFFICER</span></td>
</tr>
</table>
<table></table>
<table>
<tr>
<td><span class="FirstColumnPrompt">Agency Code:</span></td><td><span class="Value">AD</span><span class="Prompt">Agency Sub-Code:</span><span class="Value">5902</span><span class="Prompt">Officer ID:</span><span class="Value">G223</span></td>
</tr>
</table>
<HR>
<table>
<tr>
<td><span class="FirstColumnPrompt">Name:</span><span class="Value">AUSTIN, BRYANT</span></td>
</tr>
<tr>
<td><span class="FirstColumnPrompt">Connection:</span><span class="Value">WITNESS/POLICE OFFICER</span></td>
</tr>
</table>
<table></table>
<table>
<tr>
<td><span class="FirstColumnPrompt">Agency Code:</span></td><td><span class="Value">AD</span><span class="Prompt">Agency Sub-Code:</span><span class="Value">5902</span><span class="Prompt">Officer ID:</span><span class="Value">I279</span></td>
</tr>
</table>
<HR>
<table>
<tr>
<td><span class="FirstColumnPrompt">Name:</span><span class="Value">SAVADEL, KEITH E</span></td>
</tr>
<tr>
<td><span class="FirstColumnPrompt">Connection:</span><span class="Value">COMPLAINANT/POLICE OFFICER</span></td>
</tr>
</table>
<table></table>
<table>
<tr>
<td><span class="FirstColumnPrompt">Agency Code:</span></td><td><span class="Value">AD</span><span class="Prompt">Agency Sub-Code:</span><span class="Value">5902</span><span class="Prompt">Officer ID:</span><span class="Value">I391</span></td>
</tr>
</table>
<HR>
<table>
<tr>
<td><span class="FirstColumnPrompt">Name:</span><span class="Value">SAVADEL, KEITH E OFC</span></td>
</tr>
<tr>
<td><span class="FirstColumnPrompt">Connection:</span><span class="Value">COMPLAINANT</span></td>
</tr>
</table>
<table></table>
<table>
<tr>
<td><span class="Value"></span><span class="Value"></span><span class="Value"></span></td>
</tr>
</table>
<HR>
<H5>Event History Information</H5>
<table BGColor="#E1E1E1" Align="center" border="0">
<tr>
<td>
<Bold>Event</Bold>
</td><td>
<Bold>Date </Bold>
</td><td>
<Bold>Comment</Bold>
</td>
</tr>
<tr>
<td><span class="Value">DOCI</span></td><td><span class="Value">03/29/2012</span></td><td><span class="Value">SC   ISSUED 120329</span></td>
</tr>
<tr>
<td><span class="Value">INIT</span></td><td><span class="Value">03/29/2012</span></td><td><span class="Value">120329;00000000.00;ROR ;100;    ;1321</span></td>
</tr>
<tr>
<td><span class="Value">RCAS</span></td><td><span class="Value">03/30/2012</span></td><td><span class="Value">0FQ75411</span></td>
</tr>
</table>
<BR>
<div class="InfoStatement">
This is an electronic case record. Full case information cannot be made available either because of legal restrictions on access to case records found in Maryland rules 16-1001 through 16-1011, or because of the practical difficulties inherent in reducing a case record into an electronic format.
     </div>
</div>
</body>
</html>
"""

html = fromstring(entry)
tables = html.cssselect('table')
for TABLENUM in TABLENUMS:
    for tr in tables [TABLENUM]:
        cellvalues = tr.text_content()
        print cellvalues

#soup = BeautifulSoup(entry)
#print (soup.find_all(text="Defendant Name"))

#print tostring(td)
#for table in table.cssselect('table'):
 #   cellvalues = table.text_content()





# blank
###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
import time
import datetime

#html = scraperwiki.scrape('http://et.diavgeia.gov.gr/f/all/')
#html = scraperwiki.scrape('http://et.diavgeia.gov.gr/f/all/ada/4%CE%99%CE%9A%CE%A4%CE%99%CE%91%CE%9A-6')

doc = ['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
'<html xmlns="http://www.w3.org/1999/xhtml">'
'<head>'
'    <meta http-equiv="content-type" content="text/html; charset=utf-8" />'
'    <title>Ανάρτηση Αποφάσεων στο Διαδίκτυο | Όλοι οι φορείς</title>'
'    '
'    <link rel="icon" href="http://et.diavgeia.gov.gr/f/all/images/favicon.ico" />'
'    <link rel="shortcut icon" href="http://et.diavgeia.gov.gr/f/all/images/favicon.ico" />'
'    <link rel="alternate" title="Διαύγεια RSS - Όλες οι αποφάσεις" href="http://et.diavgeia.gov.gr/f/all/rss" type="application/rss+xml" />'
'    <meta name="keywords" content="" />'
'    <meta name="description" content="" />'
''
'    <script type="text/javascript" src="http://et.diavgeia.gov.gr/f/all/js/jquery.js"></script> '
'    '
'    <link href="http://et.diavgeia.gov.gr/f/all/css/et.css" rel="stylesheet" type="text/css" />'
'    <link href="http://et.diavgeia.gov.gr/f/all/search/jscalendar/calendar-blue.css" rel="stylesheet" type="text/css" />'
''
'</head>'
'<body>'
''
'<div id="wrapper">'
'<br />'
'<div align="right">'
'</div>'
''
'<div align="right" class="search_bar">'
'<a href="http://et.diavgeia.gov.gr/f/all/search/index.php"><font color="black"><b>Αναζήτηση</b></font></a>'
''
'</div>'
''
'    <div id="header"><!--'
'        <div id="menu">'
'            <ul>'
'                <li><a target="_blank" href="http://www.primeminister.gr/">Πρωθυπουργός</a></li>'
'                <li><a target="_blank" href="http://www.primeminister.gr/government">Κυβέρνηση</a></li>'
'                <li><a target="_blank" href="http://www.ypes.gr">Υπουργείο</a></li>'
'                <li><a target="_blank" href="http://www.opengov.gr">Διαβουλεύσεις</a></li>'
'                   <li><a target="_blank" href="http://et.diavgeia.gov.gr">Ηλεκτρονική Εφημερίδα</a></li>'
'            </ul>'
'        </div> -->'
'        <!-- end div#menu -->'
'        <div id="logo">'
'            <img src="http://et.diavgeia.gov.gr/f/all/images/logo.png" title="Όλοι οι φορείς" />'
'            <br />'
'            <h1><a href="http://et.diavgeia.gov.gr">ΠΡΟΓΡΑΜΜΑ ΔΙΑΥΓΕΙΑ</a></h1>'
'            <br />'
''
'            <br />'
'            <br />'
'            <h2>Όλοι οι φορείς</h2>    '
'        </div>'
'        <!-- end div#logo -->'
'        <div id="diavgeia">'
'            <a href="http://www.et.gr">'
'                <img src="http://et.diavgeia.gov.gr/f/all/images/et_logo.png" title="Εθνικό Τυπογραφείο" />'
'            </a>'
''
'            <a href="http://diavgeia.gov.gr">'
'                <img src="http://et.diavgeia.gov.gr/f/all/images/diavgeia_s.jpg" title="Δι@ύγεια - Ανάρτηση Αποφάσεων στο Διαδίκτυο" />'
'            </a>'
'        </div>'
'    </div>'
'    <!-- end div#header -->'
'    <div id="page">'
'        <div id="page-bgtop">'
'            <div id="content">'
'                <div class="breadcrumb">'
'<a href="http://et.diavgeia.gov.gr/f/all/">Αρχική</a>'
' &raquo;  Βεβαίωση Απαλλαγής από Έγκριση Περιβαλλοντικών Όρων του έργου: «Φωτοβολταϊκό Πάρκο ισχύος 99,975kWp '
' του Δημολίτσα Νικόλαου επαγγελματία αγρότη, σε αγρόκτημα με αρ. ΚΑΕΚ 400160403048, στη θέση «Μπόϊδα-Μαύρη», '
' στο Τ.Δ. Θεσπρωτικού, του Δήμου Θεσπρωτικού, Ν.Πρέβεζας»'
'                </div>'
'                    <div class="single_doc">'
' <ul>'
'    <li> <span>ΑΔΑ</span>4ΙΚΤΙΑΚ-Φ </li>'
'    <li><span>Αριθμός Πρωτοκόλου</span>59544/4011 </li>'
'    <li><span>Θέμα</span>Βεβαίωση Απαλλαγής από Έγκριση Περιβαλλοντικών Όρων του έργου: «Φωτοβολταϊκό Πάρκο ισχύος 99,975kWp του Δημολίτσα Νικόλαου επαγγελματία αγρότη, σε αγρόκτημα με αρ. ΚΑΕΚ 400160403048, στη θέση «Μπόϊδα-Μαύρη», στο Τ.Δ. Θεσπρωτικού, του Δήμου Θεσπρωτικού, Ν.Πρέβεζας»</li>'
'    <li><span>Τελικός Υπογράφων</span>Διευθυντής - Κωνσταντίνος Κωνσταντής - </li>'
'    <li><span>Ημερομηνία Απόφασης</span>01/10/2010</li>'
'    <li><span>Ημερομηνία Ανάρτησης</span>02/10/2010 12:11:04</li>'
'    <li><span>Είδος Απόφασης</span>(ΠΡΑΞΗ ΤΗΣ ΠΕΡ. 19, ΠΑΡ. 4 ΑΡΘΡΟΥ 2 Ν. 3861/2010 )- Χωροθέτηση </li>'
'    <li><span>Φορέας</span>ΠΕΡΙΦΕΡΕΙΑ ΗΠΕΙΡΟΥ</li>'
'    <li><span>Μονάδα</span>Διεύθυνση Περιβάλλοντος &amp; Χωροταξίας</li>'
'    <li><span>Θεματική</span>'
'        <ul>'
'            <li>Ανανεώσιμες πηγές ενέργειας</li>'
'        </ul></li>'
'    <li><span>Αρχείο</span><a class="getdoc" href="http://static.diavgeia.gov.gr/doc/4ΙΚΤΙΑΚ-Φ">Λήψη Αρχείου</a></li>'
'</ul>'
'                    </div>'
'            </div>        '
'        </div>'
'    </div>'
'    <!-- end div#page -->'
'    <div id="footer">'
''
'        <p id="legal">'
'   '
''
'             Σχεδιάστηκε από  την <a href="http://www.opengov.gr" target="_blank"> Ομάδα Ηλεκτρονικής Διακυβέρνησης του Γραφείου του Πρωθυπουργού </a> σε συνεργασία με την <a href="http://www.epdm.gr" target="_blank"> Ειδική Γραμματεία Διοικητικής Μεταρρύθμισης</a>  και υλοποιήθηκε  με χρήση <a href="http://mathe.ellak.gr" target="_blank">ΕΛ/ΛΑΚ</a> λογισμικού  από την <a href="http://www.ktpae.gr">Κοινωνία της Πληροφορίας Α.Ε</a>  '
''
''
''
'<br />'
'    <a title="Πλην ειδικής αναφοράς, όλο το περιεχόμενο αυτού του διαδικτυακού τόπου είναι αδειοδοτημένο με Creative Commons" '
'            href="http://creativecommons.org/licenses/by/3.0/gr/" target="_blank">'
'            <img alt="Πλην ειδικής αναφοράς, όλο το περιεχόμενο αυτού του διαδικτυακού τόπου είναι αδειοδοτημένο με Creative Commons" '
'            src="http://et.diavgeia.gov.gr/f/all/images/cc.png"></a>'
''
'        </p>'
'    </div>'
'    <!-- end div#footer '
'    <div id="feedback"><a href="javascript: openwindow()"><img src="http://et.diavgeia.gov.gr/f/all/images/feedback.png"></a></div>'
'    <script language="javascript">'
'        function openwindow() {'
'            window.open("https://spreadsheets.google.com/viewform?formkey=dFJKemR4dU9feWdFZG9jMmNpM0ZKdVE6MA",'
'            "mywindow","location=0,status=0,scrollbars=1,width=820,height=1200");'
'        }'
'    </script>-->'
'</div>'
'<!-- end div#wrapper -->'
'</body>'
'</html>']

from BeautifulSoup import BeautifulSoup, Tag, NavigableString

soup = BeautifulSoup(''.join(doc))
#html = scraperwiki.scrape('http://et.diavgeia.gov.gr/f/all/ada/4%CE%99%CE%9A%CE%A4%CE%99%CE%91%CE%9A-6')
#soup = BeautifulSoup(html)

#print html
#print soup.prettify()


# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <td> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting
# the HTML that was inside <td></td> tags.
# We use BeautifulSoup, which is a Python library especially for scraping.
# -----------------------------------------------------------------------------

#from BeautifulSoup import BeautifulSoup
#soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
# myitems = soup.findAll('strong')

#myitems = soup.find(text='Τελευταίες Αποφάσεις').findNext('ul').li

#myitems = soup.findAll('li')
myitems = soup.find('div', id="content").findAll('li')
#print myitems

record = {}
for theitem in myitems:    
    span = theitem.span
    #print span
    if span:
        if span.text == "ΑΔΑ".decode('utf8') :
            span.extract() # remove <span></span>
            content = theitem.text
            #print content
            #print '<ada>' + content + '</ada>'
            record["ada"] = content
        elif span.text == "Αριθμός Πρωτοκόλου".decode('utf8') :
            span.extract() # remove <span></span>
            #print '<identifier>' + theitem.text + '</identifier>'
            record['identifier'] = theitem.text
        elif span.text == "Θέμα".decode('utf8') :
            span.extract() # remove <span></span>
            #print '<subject>' + theitem.text + '</subject>'
            record['subject'] = theitem.text
        elif span.text == "Ημερομηνία Απόφασης".decode('utf8') :
            span.extract() # remove <span></span>
            #print '<created>' + theitem.text + '</created>'
            #datetime.strptime(date_string, format) is equivalent to datetime(*(time.strptime(date_string, format)[0:6]))
            print '<created>' + theitem.text + '</created>'
            datestring=theitem.text
            day = int(datestring[:2])
            month = int(datestring[3:5])
            year = int (datestring[6:10])
            
                
            theDate = datetime.datetime(year,month,day)
            record['created'] = theDate
        elif span.text == "Ημερομηνία Ανάρτησης".decode('utf8') :
            span.extract() # remove <span></span>
            print '<dateAccepted>' + theitem.text + '</dateAccepted>'
            datestring=theitem.text
            day = int(datestring[:2])
            month = int(datestring[3:5])
            year = int (datestring[6:10])
            hour = int(datestring[11:13])
            #print hour
            minute = int(datestring[14:16])
            #print minute
            second = int (datestring[17:19])
            #print second
            theDateUp = datetime.datetime(year,month,day,hour,minute,second)
            #print theDateUp 
            record['created'] = theDateUp

            record['dateAccepted'] = theitem.text
        elif span.text == "Φορέας".decode('utf8') :
            span.extract() # remove <span></span>
            #print '<publisher>' + theitem.text + '</publisher>'
            record['publisher'] = theitem.text
        elif span.text == "Αρχείο".decode('utf8') :
            span.extract() # remove <span></span>
            print theitem.a.contents[0]
            print theitem.find('a')
            print theitem.find('a')['href']
            #print '<doclink>' + theitem.text + '</doclink>'
            record['doclink'] = theitem.a.href
print record
#scraperwiki.datastore.save(['ada'], record, theDate)
            
    
#for td in tds:
#     record = { "td" : td.text } # column name and value
#     scraperwiki.datastore.save(["td"], record) # save the records one by one


#myitems = soup.finda
#print myitems

#for theitem in myitems:
#    print myitem
#    print myitem.text

#tds = soup.findAll('td') # get all the <td> tags
#for td in tds:
#    print td # the full HTML tag
#    print td.text # just the text inside the HTML tag

# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -- UNCOMMENT THE TWO LINES BELOW
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.
# -----------------------------------------------------------------------------

#for td in tds:
#     record = { "td" : td.text } # column name and value
#     scraperwiki.datastore.save(["td"], record) # save the records one by one
    
# -----------------------------------------------------------------------------
# Go back to the Tutorials page and continue to Tutorial 3 to learn about
# more complex scraping methods.
# -----------------------------------------------------------------------------


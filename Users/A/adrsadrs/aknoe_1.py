import scraperwiki, re

scraperwiki.sqlite.attach('aknoe') 

print "<h1>Kaffeefahrten</h1>"

results = scraperwiki.sqlite.execute('select * from "aknoe".swdata')
for line in results["data"]:
    # Firmenname
    m = re.search("Firmenname\ (.*)\ Firmenadresse", line[1].replace("\n"," "))
    firmenname = m.group(1)
    # Gewinnbrief
    s = re.search("itteilung\ (.{25})", line[1].replace("\n"," "))
    s = re.search("itteilung\ (.*)\ Vermeintlicher", line[1].replace("\n"," ")) 
    try: gewinnbrief = '"' + s.group(1) + '" = '
    except: gewinnbrief = ""
    # Scheinfirma
    s = re.search("auf\ unter\ (.{25})", line[1].replace("\n"," "))
    try: scheinfirma = s.group(1) + "... = "
    except: scheinfirma = ""
    # Firmenadresse
    s = re.search("Firmenadresse\ (.{25})", line[1].replace("\n"," "))
    try: firmenadresse = ", " + s.group(1) + "..."
    except: firmenadresse = ""
    # Waren
    w = re.search("Ware 1(.*)Info", line[1].replace("\n"," "))
    if w: 
        waren = w.group(1).replace("Hersteller 1", "").replace("Hersteller 2", "").replace("Ware 2", "")
        waren = " <i>(Verkauf von Ware: %s)</i>" % waren
    else: waren = ""
    # PDFs
    if line[4]: 
        pdfs=" "
        for pdf in eval(line[4]):
            pdfs = pdfs + ('<a href="%s" target="_blank"><img src="http://user.phil-fak.uni-duesseldorf.de/~petersen/pdf-icon.gif" border="0"></a> ') % (pdf)
    else: pass
    print '<p>%s%s<a href="%s" target="_blank">%s</a>%s%s%s</p>' % (gewinnbrief, scheinfirma, line[0], firmenname, firmenadresse, waren, pdfs)
import scraperwiki, re

scraperwiki.sqlite.attach('aknoe') 

print "<h1>Kaffeefahrten</h1>"

results = scraperwiki.sqlite.execute('select * from "aknoe".swdata')
for line in results["data"]:
    # Firmenname
    m = re.search("Firmenname\ (.*)\ Firmenadresse", line[1].replace("\n"," "))
    firmenname = m.group(1)
    # Gewinnbrief
    s = re.search("itteilung\ (.{25})", line[1].replace("\n"," "))
    s = re.search("itteilung\ (.*)\ Vermeintlicher", line[1].replace("\n"," ")) 
    try: gewinnbrief = '"' + s.group(1) + '" = '
    except: gewinnbrief = ""
    # Scheinfirma
    s = re.search("auf\ unter\ (.{25})", line[1].replace("\n"," "))
    try: scheinfirma = s.group(1) + "... = "
    except: scheinfirma = ""
    # Firmenadresse
    s = re.search("Firmenadresse\ (.{25})", line[1].replace("\n"," "))
    try: firmenadresse = ", " + s.group(1) + "..."
    except: firmenadresse = ""
    # Waren
    w = re.search("Ware 1(.*)Info", line[1].replace("\n"," "))
    if w: 
        waren = w.group(1).replace("Hersteller 1", "").replace("Hersteller 2", "").replace("Ware 2", "")
        waren = " <i>(Verkauf von Ware: %s)</i>" % waren
    else: waren = ""
    # PDFs
    if line[4]: 
        pdfs=" "
        for pdf in eval(line[4]):
            pdfs = pdfs + ('<a href="%s" target="_blank"><img src="http://user.phil-fak.uni-duesseldorf.de/~petersen/pdf-icon.gif" border="0"></a> ') % (pdf)
    else: pass
    print '<p>%s%s<a href="%s" target="_blank">%s</a>%s%s%s</p>' % (gewinnbrief, scheinfirma, line[0], firmenname, firmenadresse, waren, pdfs)

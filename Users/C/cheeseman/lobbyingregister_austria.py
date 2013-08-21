import scraperwiki
import lxml.html
import re
from datetime import datetime, date, time


# TODO
# strip html from aufgabenbereich



# get html
baseURL = 'http://www.lobbyreg.justiz.gv.at/edikte/ir/iredi18.nsf/'
queryURL = baseURL + 'sucheap!OpenForm&subf=a'
#queryURL = baseURL + 'suchera!OpenForm&subf=r&RestrictToCategory=B'
html = scraperwiki.scrape(queryURL)
html = html.decode('utf-8')

root = lxml.html.fromstring(html)

# loop over table rows
for trs in root.cssselect("tbody tr"):
    tds = trs.cssselect("td")
    
    RegDep = tds[3].text_content()

    # get RegisterNumberURL
    htmlRegNum = lxml.html.tostring(tds[2], encoding='unicode')
    regNumURL = re.search('<a href="(.*)"\s*onclick.*>', htmlRegNum)
    regNumURL = regNumURL.group(1)

    # scrape register page
    htmlOrg = scraperwiki.scrape(baseURL + regNumURL)
    htmlOrg = htmlOrg.decode('utf-8')

    rootOrg = lxml.html.fromstring(htmlOrg)
    htmlInt = lxml.html.tostring(rootOrg, encoding='unicode')


    if RegDep == 'A1':

        # regex lobbyists
        htmlEmp = lxml.html.tostring(tds[4], encoding='unicode')
        lstEmp = re.findall('^<td>(.*<br>)+</td>$', htmlEmp)
        lstEmp = re.split(r'<br>', lstEmp[0])
        numEmp = len(lstEmp)-1
        lstEmp = ', '.join(lstEmp)


        # regex Tätigkeitsbereich
        # <dt title="Bezeichnung der beruflichen oder geschäftlichen Aktivitäten">Tätigkeitsbereich:</dt>
        # <dd>Stromerzeugung</dd></dl>

        areaOfDep = re.findall(r'tigkeitsbereich:</dt>\n<dd>(.*)</dd>', htmlInt)

        if areaOfDep:
            areaOfDep = re.sub('<br>', ' ', areaOfDep[0])
        else:
            areaOfDep = 'keine Angabe'

        # regex Lobbying Umsatz letztes Jahr
        # dt title="mit Lobbying-Tätigkeiten erzielter Umsatz im vorangegangenen Geschäftsjahr">Lobbying-Umsatz:</dt>
        # <dd>EUR 0,00</dd></dl>

        volSales = re.findall(r'Lobbying-Umsatz:</dt>\n<dd>EUR (.*)</dd>', htmlInt)
        if volSales: 
            volSales = volSales[0]
        else:
            volSales = 'keine Angabe'

        # regex Anzahl Aufträge
        # <dt title="Anzahl der bearbeiteten Lobbying-Aufträge im vorangegangenen Geschäftsjahr">Lobbying-Aufträge:</dt>
        # <dd>0</dd></dl>

        numOrders = re.findall(r'Lobbying-Auftr.*ge:</dt>\n<dd>(.*)</dd></dl>', htmlInt)
        if numOrders:
            numOrders = numOrders[0]
        else:
            numOrders = 'keine Angabe'

    else:
        numOrders = 'keine Angabe'
        volSales = 'keine Angabe'

    if RegDep == 'B':
        # regex lobbyists
        htmlEmp = lxml.html.tostring(tds[4], encoding='unicode')
        lstEmp = re.findall('^<td>(.*<br>)+</td>$', htmlEmp)
        lstEmp = re.split(r'<br>', lstEmp[0])
        numEmp = len(lstEmp)-1
        lstEmp = ', '.join(lstEmp)

        # regex Tätigkeitsbereich
        # <dt title="Bezeichnung der beruflichen oder geschäftlichen Aktivitäten">Tätigkeitsbereich:</dt>
        # <dd>Stromerzeugung</dd></dl>
        areaOfDep = re.findall(r'tigkeitsbereich:</dt>\n<dd>(.*)</dd>', htmlInt)

        if areaOfDep:
            areaOfDep = re.sub('<br>', ' ', areaOfDep[0])
        else:
            areaOfDep = 'keine Angabe'

        # regex Lobbying Aufwand
        # <dt title="Aufwand für Lobbying-Tätigkeiten im abgelaufenen Wirtschaftsjahr übersteigt EUR 100.000,-">Lobbying-Aufwand > € 100.000:</dt>
        # <dd>Nein</dd></dl>
        effortOver100th = re.findall(r'000:</dt>\n<dd>(.*)</dd></dl>', htmlInt)
        
        if effortOver100th:
            effortOver100th = effortOver100th[0]
        else:
            effortOver100th = 'keine Angabe'

    if(RegDep == 'C'):

        lstEmp = 'keine Angabe'

        # regex Anzahl Interessenvertreter own field
        # HTML: <dl><dt title="Gesamtzahl der überwiegend als Interessenvertreter tätigen Personen im vorangegangenen Geschäftsjahr">Anzahl Interessenvertreter:</dt>
        # <dd>1</dd></dl>
        numEmpOF = re.findall(r'Anzahl Interessenvertreter:</dt>\n<dd>(.*)</dd>', htmlInt)

        if numEmpOF:
            numEmpOF = int(numEmpOF[0])
        else:
            numEmpOF = 0

        # regex Anzahl Interessensvertreter inside textfield Unterorganisationen
        # <dt>Unterorganisation(en):</dt>
        # <dd>Rechtsanwaltskammer Burgenland<br>Sitz/Anschrift: Marktstraße 3, 7000 Eisenstadt<br>Gesetzliche Grundlage: Rechtsanwaltsordnung<br>Homepage: -<br>Anzahl Interessenvertreter: 1<br>Kosten der Interessenvertretung: 0,00<br>.<br>Rechtsanwaltskammer für Kärnten<br>Sitz/Anschrift: Theatergasse 4/I, 9020 Klagenfurt<br>Gesetzliche Grundlage: Rechtsanwaltsordnung<br>Homepage: http://www.rechtsanwaelte-kaernten.at<br>Anzahl Interessenvertreter: 1<br>Kosten der Interessenvertretung: 0,00<br></dd></dl>
        numEmpUF = re.findall(r'<dt>Unterorganisation.*</dt>\n<dd>(.*)</dd></dl>', htmlInt)

        if numEmpUF:
            numEmpUF = numEmpUF[0]

            # regex inside textfield
            # <br>Anzahl Interessenvertreter: 1<br>
            lstEmpUF = re.findall(r'Anzahl Interessenvertreter: ([0-9]+)<br>', numEmpUF)

            if lstEmpUF:           
                numEmpUF = 0

                for ele in lstEmpUF:
                    numEmpUF = numEmpUF + int(ele)
            else:
                numEmpUF = 0
        else:
            numEmpUF = 0

        # decide Anzahl Interessenvertreter between own field and inside textfield Unterorganisation

        if numEmpUF > numEmpOF:
            numEmp = numEmpUF
        elif numEmpOF >= numEmpUF:
            numEmp = numEmpOF
        else:
            numEmp = 0

        # regex for Aufgabenbereich
        # HTML: <dl><dt title="Umschreibung des vertraglichen oder statutarischen Aufgabenbereichs">Aufgabenbereich:</dt>
        # <dd>Der Verein, dessen Tätigkeit nicht auf Gewinn ausgerichtet ist, bezweckt die Information der Öffentlichkeit über alle das Zweirad betreffende Fragen, insbesondere die Sicherheit durch verbesserte Ausbildung, Ausrüstung und vernünftige Nutzung des Zweirades unter Ausschaltung von Risiken.</dd></dl>
        areaOfDep = re.findall(r'Aufgabenbereich:</dt>\n<dd>(.*)</dd></dl>', htmlInt)

        if areaOfDep:
            areaOfDep = re.sub('<br>', ' ', areaOfDep[0])
        else:
            areaOfDep = 'keine Angabe'



    if RegDep == 'D':
        lstEmp = 'keine Angabe'

        # regex for Anzahl Interessenvertreter
        # HTML: <dl><dt title="Gesamtzahl der überwiegend als Interessenvertreter tätigen Personen im vorangegangenen Geschäftsjahr">Anzahl Interessenvertreter:</dt>
        # <dd>1</dd></dl>
        numEmp = re.findall(r'Anzahl Interessenvertreter:</dt>\n<dd>(.*)</dd>', htmlInt)

        if numEmp:
            numEmp = numEmp[0]
        else:
            numEmp = 0

        # regex for Aufgabenbereich
        # HTML: <dl><dt title="Umschreibung des vertraglichen oder statutarischen Aufgabenbereichs">Aufgabenbereich:</dt>
        # <dd>TEXT TÄTIGKEITSBEREICH</dd></dl>
        areaOfDep = re.findall(r'Aufgabenbereich:</dt>\n<dd>(.*)</dd></dl>', htmlInt)

        if areaOfDep:
            areaOfDep = re.sub('<br>', ' ', areaOfDep[0])
        else:
            areaOfDep = 'keine Angabe'

    else:
        salesOver100th = 'keine Angabe'



    # data object
    data = {
        'RegisterNumber' : tds[2].text_content(),
        'RegisterNumberURL' : baseURL + regNumURL,
        'Name' : tds[1].text_content(),
        'RegisterDepartment' : RegDep,
        'Employees' : lstEmp,
        'NumberEmployees' : numEmp,
        'NumberFemaleEmployees' : 0,
        'VolOfSales' : volSales,
        'EffortOver100th' : effortOver100th,
        'NumOrders' : numOrders,
        'AreaOfOperations' : areaOfDep,
        'SectorEU' : 0,
        'SectorEurostat' : 0,
        'SectorUSA' : 0,
        'CreatedAt' : datetime.utcnow()
        #'CreatedAt' : time.strftime('%Y-%m-%d-%H-%M', gmtime())
    }

    # save to sqlite database
    scraperwiki.sqlite.save(unique_keys=['RegisterNumber', 'Name'], data=data)





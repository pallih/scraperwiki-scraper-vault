import scraperwiki
import re
from bs4 import BeautifulSoup # documentation at http://www.crummy.com/software/BeautifulSoup/bs4/doc/

# Names to check (short list)

directors = ['TORBEN HANSEN',
'THEO CONSTANTINIDIS',
'SIMON FIRTH',
'PETER JOEL CHARLES',
'GEORGE P BREWSTER',
'MICHAEL GUY',
'JAMES MICHAEL WILLIAM LINDLEY',
'RICHARD ALEXANDER BIGGS',
'BRUCE W MORTIMER',
'LAURENCE PATRICK MCLLWEE',
'JAN PIETER',
'SUTANU SAMANTA',
'SIMON NICHOLAS HEWITT LEWIS',
'DUDLEY JOHN PENNELL',
'JEFFREY ELLIS',
'MS ELISABETH TEO',
'GARY HAWKINS',
'JAMES DAVID HICKMAN',
'STEPHEN JOHN COOPER',
'JASON MILLER',
'PAUL PHEYSEY',
'VITTORIO MARTINO',
'JOHN BOISSIER',
'JOHN GRIFFIN',
'PHILIP HAY',
'ANDREW CRISS',
'JONATHAN MILBURN',
'PAUL KEITH SHEPPARD',
'ANTHONY HAMMOND',
'STUART WHITE',
'PETER COURTNEY',
'STUART FYFE',
'JULIAN MERCER',
'NIALL DOWLING',
'PHILIP HARRIS',
'CHRISTOPHER DAVID MURPHY',
'PATRICK CORR',
'ROBERT COOPER',
'TIMOTHY JAMES HOUGHTON',
'CHRISTOPHER OVER',
'DAVID PLOWMAN',
'SETH LOVIS',
'STEWART CAZIER',
'VIMAL RUA',
'ANDREW SEATON',
'RICHARD ADAM DAVIES',
'PAUL MULLINS',
'ALEJANDRO GONZALEZ RUIZ',
'RICHARD ROYDEN',
'CHRISTIAN STOIBER',
'WILLIAM BARTER',
'ARUN JAGANNATHAN',
'MARK STEPHEN HUMPHRIES',
'RICHARD WADDINGTON',
'KENNETH C SCOTT',
'ANDREW JOHN CARPENTER',
'EMMANOUIL LIODAKIS',
'GILBERT J HOLBOURN',
'DEAN JEFFREY SPIERS',
'RAZA KHAN',
'MS JENNIFER PONSONBY',
'DOMENICO AZZOLLINI',
'RORY POWE',
'DARAGH RICHARD HORGAN',
'LOUIS DE KOCK',
'PAUL ASHLEY WILLIAMS',
'MARC CHAPMAN',
'IAN GEORGE NICOLL',
'MARK CLIFFORD HOWARD',
'VINCENT COLIN TAYLOR',
'ANDREW CHARLES BAINES',
'NIGEL DOHERTY',
'RICHARD JAMES JASON FORD',
'JOHN OLNEY',
'RHOMAIOS VIRJANAND RAM',
'RASHID HOOSENALLY',
'ROBERT DAVID NELSON',
'DAVID QUINTON HENNING SHAW',
'Anthony Laubi',
'Roger Pioter Sniezek',
'Stefan ericsson',
'Michael Spalter',
'D Andrew Whittle',
'Mark Leader',
'Philip Charles Thompson',
'Stephen Jennions',
'Michele Tomasi',
'Rivinia Charmaine Ahearne',
'Mark Stephen Aspinall',
'Mark Teeger',
'Roy Anthony Gabbie',
'Bruce John Hanton',
'Thomas Demeure',
'Alan Jacobs',
'Ganesh Rajendra',
'Richard Herman',
'Tadgh Flood',
'Nicholas Martin Close',
'Dan Daniel Bebello',
'Toni Adele Dyson',
'Katie Brown',
'Colette Moscati',
'Ian William Mackaie',
'Carmine Di Conno',
'Philip Feibusch',
'Dominic James Ryder',
'Patrick Burnell',
'David Howard Morgan',
'Fergus Lynch',
'Stephen Jones',
'Andrew H Christie',
'Thomas Reid',
'Stefano ghersi',
'Sean Jonathan Notley',
'Domenico Crapanzano',
'Mark Gheerbrant banker',
'Nicholas John Coulson',
'Mark Warham',
'Nicholas Brown',
'Edward S Awty',
'Jason Fu',
'Andrew Scot Monro',
'Sheldon Fagelman',
'Gilbert J Holbourn',
'P Bakunowicz',
'Kenneth c Scott',
'Ben Luscombe',
'Graham Patrick Phillips',
'Claudio Pinto',
'Kieran Cotter',
'Guy Dudley Coughlan',
'Nicholas Geoffrey Wilford',
'Richard Brookshaw',
'Iain Cameron MacDonald',
'Joachim Dobrikat',
'Hugo Heath',
'Alessandro Attolico',
'Francis Michael Bridgeman',
'Andrea Giordani',
'Asif Ghiawadwala',
'David Fairweather',
'Manuel Carmel Mifsud',
'William Simon Alexander',
'Hugh Sloane',
'Nicholas J Hyde',
'Mark Nicholas Lewis Morgan',
'Geoffrey William Phillips'
]



for director in directors:
    
    link = 'https://company-director-check.co.uk/search?name=' + director.replace(' ','+') + '&posted=true&Search=Check+now' #' + director.replace(' ','+') + '
    print link
    
    html = scraperwiki.scrape(link)
    print html
    soup = BeautifulSoup(html)
    
    if soup.find("p", "directorName") is not None:
    
        ps = soup.find_all('p')
        print len(ps)
        print ps
        if len(ps) is 54:
            last_page = ps[52].find_all('a') 
            lastpage = last_page[1].get("href")
            lastpagenumberlist = re.findall(r'\d+', lastpage)
            lastpagenumber = int(lastpagenumberlist[0])
            print "Total pages: "
            print lastpagenumber 
        else:
            lastpagenumber = 1
        
        for link_per_page in range(1,lastpagenumber+1):

                print link_per_page
                in_link = 'https://company-director-check.co.uk/search?name=' + director.replace(' ','+') + '&page=' + str(link_per_page) +'' #' + director.replace(' ','+') + '
            
                in_html = scraperwiki.scrape(in_link)
                print in_html
                in_soup = BeautifulSoup(in_html)

                in_ps = in_soup.find_all('p')
                #print ps
                counter = 0
                for p in in_ps:
                    if p.a is not None:
                        counter = counter+1
                        span_text = p.a.get_text().strip()
                        print span_text
                        if (counter % 2) is 1:
                            name_found = span_text
                        else:
                            data = {"Name": name_found, "Company Name": span_text "Original Name": director}
                            scraperwiki.sqlite.save(["Name", "Company Name"], data)           

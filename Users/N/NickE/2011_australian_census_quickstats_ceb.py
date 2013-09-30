import scraperwiki
import lxml.html

a=[101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,401,402,403,404,405,406,407,408,409,410,411,501,502,503,504,505,506,507,508,509,510,511,512,513,514,515,601,602,603,604,605,701,702,801,802]
b=[]
for i in a:
    b.append("http://www.censusdata.abs.gov.au/census_services/getproduct/census/2011/quickstat/CED"+str(i)) 
for s in range(scraperwiki.sqlite.get_var('upto'), len(b)):
    html = scraperwiki.scrape(b[s])
    root = lxml.html.fromstring(html)
    ced = root.cssselect(".geo")[0]
    cedcode = (root.cssselect(".geoCode")[0].text).split('CED')
    cedcode = cedcode[1].split('(')
    cedcode = int(cedcode[0])
    scraperwiki.sqlite.save_var('upto', a.index(cedcode))
    population = root.cssselect(".summaryData")[0]
    male = root.cssselect(".summaryData")[1]
    female = root.cssselect(".summaryData")[2]
    age = root.cssselect(".summaryData")[3]
    families = root.cssselect(".summaryData")[4]    
    children = root.cssselect(".summaryData")[5]
    dwellings = root.cssselect(".summaryData")[6]
    avgpplhouse = root.cssselect(".summaryData")[7]
    income = root.cssselect(".summaryData")[8]
    mortgage = root.cssselect(".summaryData")[9]
    rent = root.cssselect(".summaryData")[10]
    vehicles = root.cssselect(".summaryData")[11]
    sourceurl = b[s]
    tables = []
    tablelength = len(root.cssselect("td"))
    for x in range(0, tablelength):
        tables.append(root.cssselect("td")[x].text)
    htmldump = lxml.etree.tostring(root)
    twoormorelang = htmldump.split('"Households where two or more languages are spoken", areaPercent: QuickStats.formatValue(')[1].split(')')[0]
    unemployed = tables[(tables.index('Unemployed') + 2)]
    workedfulltime = tables[(tables.index('Worked full-time') + 2)]
    workedparttime = tables[(tables.index('Worked part-time') + 2)]
    awayfromwork = tables[(tables.index('Away from work') + 2)]
    tertiary = tables[(tables.index('University or tertiary institution') + 2)]
    bothparentsbornoverseas = tables[(tables.index('Both parents born overseas') + 2)]
    oneparentbornoverseas = float(tables[(tables.index('Father only born overseas') + 2)]) + float(tables[(tables.index('Mother only born overseas') + 2)]) 
    
    print ced.text
    print b[s]

    data = {}
    data['ced'] = ced.text
    data['cedcode'] = cedcode
    data['population'] = population.text
    data['male'] = male.text
    data['female'] = female.text
    data['age'] = age.text
    data['families'] = families.text
    data['children'] = children.text
    data['dwellings'] = dwellings.text
    data['avgpplhouse'] = avgpplhouse.text
    data['income'] = income.text
    data['mortgage'] = mortgage.text
    data['rent'] = rent.text
    data['vehicles'] = vehicles.text
    data['workedfulltime'] = workedfulltime
    data['workedparttime'] = workedparttime
    data['awayfromwork'] = awayfromwork
    data['unemployed'] = unemployed
    data['tertiaryeducation'] = tertiary
    data['bothparentsbornoverseas'] = bothparentsbornoverseas
    data['oneparentbornoverseas'] = oneparentbornoverseas
    data['twoormorelanguages'] = twoormorelang
    data['source'] = b[s]
    scraperwiki.sqlite.save(unique_keys=["ced"], data=data)import scraperwiki
import lxml.html

a=[101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,401,402,403,404,405,406,407,408,409,410,411,501,502,503,504,505,506,507,508,509,510,511,512,513,514,515,601,602,603,604,605,701,702,801,802]
b=[]
for i in a:
    b.append("http://www.censusdata.abs.gov.au/census_services/getproduct/census/2011/quickstat/CED"+str(i)) 
for s in range(scraperwiki.sqlite.get_var('upto'), len(b)):
    html = scraperwiki.scrape(b[s])
    root = lxml.html.fromstring(html)
    ced = root.cssselect(".geo")[0]
    cedcode = (root.cssselect(".geoCode")[0].text).split('CED')
    cedcode = cedcode[1].split('(')
    cedcode = int(cedcode[0])
    scraperwiki.sqlite.save_var('upto', a.index(cedcode))
    population = root.cssselect(".summaryData")[0]
    male = root.cssselect(".summaryData")[1]
    female = root.cssselect(".summaryData")[2]
    age = root.cssselect(".summaryData")[3]
    families = root.cssselect(".summaryData")[4]    
    children = root.cssselect(".summaryData")[5]
    dwellings = root.cssselect(".summaryData")[6]
    avgpplhouse = root.cssselect(".summaryData")[7]
    income = root.cssselect(".summaryData")[8]
    mortgage = root.cssselect(".summaryData")[9]
    rent = root.cssselect(".summaryData")[10]
    vehicles = root.cssselect(".summaryData")[11]
    sourceurl = b[s]
    tables = []
    tablelength = len(root.cssselect("td"))
    for x in range(0, tablelength):
        tables.append(root.cssselect("td")[x].text)
    htmldump = lxml.etree.tostring(root)
    twoormorelang = htmldump.split('"Households where two or more languages are spoken", areaPercent: QuickStats.formatValue(')[1].split(')')[0]
    unemployed = tables[(tables.index('Unemployed') + 2)]
    workedfulltime = tables[(tables.index('Worked full-time') + 2)]
    workedparttime = tables[(tables.index('Worked part-time') + 2)]
    awayfromwork = tables[(tables.index('Away from work') + 2)]
    tertiary = tables[(tables.index('University or tertiary institution') + 2)]
    bothparentsbornoverseas = tables[(tables.index('Both parents born overseas') + 2)]
    oneparentbornoverseas = float(tables[(tables.index('Father only born overseas') + 2)]) + float(tables[(tables.index('Mother only born overseas') + 2)]) 
    
    print ced.text
    print b[s]

    data = {}
    data['ced'] = ced.text
    data['cedcode'] = cedcode
    data['population'] = population.text
    data['male'] = male.text
    data['female'] = female.text
    data['age'] = age.text
    data['families'] = families.text
    data['children'] = children.text
    data['dwellings'] = dwellings.text
    data['avgpplhouse'] = avgpplhouse.text
    data['income'] = income.text
    data['mortgage'] = mortgage.text
    data['rent'] = rent.text
    data['vehicles'] = vehicles.text
    data['workedfulltime'] = workedfulltime
    data['workedparttime'] = workedparttime
    data['awayfromwork'] = awayfromwork
    data['unemployed'] = unemployed
    data['tertiaryeducation'] = tertiary
    data['bothparentsbornoverseas'] = bothparentsbornoverseas
    data['oneparentbornoverseas'] = oneparentbornoverseas
    data['twoormorelanguages'] = twoormorelang
    data['source'] = b[s]
    scraperwiki.sqlite.save(unique_keys=["ced"], data=data)import scraperwiki
import lxml.html

a=[101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,401,402,403,404,405,406,407,408,409,410,411,501,502,503,504,505,506,507,508,509,510,511,512,513,514,515,601,602,603,604,605,701,702,801,802]
b=[]
for i in a:
    b.append("http://www.censusdata.abs.gov.au/census_services/getproduct/census/2011/quickstat/CED"+str(i)) 
for s in range(scraperwiki.sqlite.get_var('upto'), len(b)):
    html = scraperwiki.scrape(b[s])
    root = lxml.html.fromstring(html)
    ced = root.cssselect(".geo")[0]
    cedcode = (root.cssselect(".geoCode")[0].text).split('CED')
    cedcode = cedcode[1].split('(')
    cedcode = int(cedcode[0])
    scraperwiki.sqlite.save_var('upto', a.index(cedcode))
    population = root.cssselect(".summaryData")[0]
    male = root.cssselect(".summaryData")[1]
    female = root.cssselect(".summaryData")[2]
    age = root.cssselect(".summaryData")[3]
    families = root.cssselect(".summaryData")[4]    
    children = root.cssselect(".summaryData")[5]
    dwellings = root.cssselect(".summaryData")[6]
    avgpplhouse = root.cssselect(".summaryData")[7]
    income = root.cssselect(".summaryData")[8]
    mortgage = root.cssselect(".summaryData")[9]
    rent = root.cssselect(".summaryData")[10]
    vehicles = root.cssselect(".summaryData")[11]
    sourceurl = b[s]
    tables = []
    tablelength = len(root.cssselect("td"))
    for x in range(0, tablelength):
        tables.append(root.cssselect("td")[x].text)
    htmldump = lxml.etree.tostring(root)
    twoormorelang = htmldump.split('"Households where two or more languages are spoken", areaPercent: QuickStats.formatValue(')[1].split(')')[0]
    unemployed = tables[(tables.index('Unemployed') + 2)]
    workedfulltime = tables[(tables.index('Worked full-time') + 2)]
    workedparttime = tables[(tables.index('Worked part-time') + 2)]
    awayfromwork = tables[(tables.index('Away from work') + 2)]
    tertiary = tables[(tables.index('University or tertiary institution') + 2)]
    bothparentsbornoverseas = tables[(tables.index('Both parents born overseas') + 2)]
    oneparentbornoverseas = float(tables[(tables.index('Father only born overseas') + 2)]) + float(tables[(tables.index('Mother only born overseas') + 2)]) 
    
    print ced.text
    print b[s]

    data = {}
    data['ced'] = ced.text
    data['cedcode'] = cedcode
    data['population'] = population.text
    data['male'] = male.text
    data['female'] = female.text
    data['age'] = age.text
    data['families'] = families.text
    data['children'] = children.text
    data['dwellings'] = dwellings.text
    data['avgpplhouse'] = avgpplhouse.text
    data['income'] = income.text
    data['mortgage'] = mortgage.text
    data['rent'] = rent.text
    data['vehicles'] = vehicles.text
    data['workedfulltime'] = workedfulltime
    data['workedparttime'] = workedparttime
    data['awayfromwork'] = awayfromwork
    data['unemployed'] = unemployed
    data['tertiaryeducation'] = tertiary
    data['bothparentsbornoverseas'] = bothparentsbornoverseas
    data['oneparentbornoverseas'] = oneparentbornoverseas
    data['twoormorelanguages'] = twoormorelang
    data['source'] = b[s]
    scraperwiki.sqlite.save(unique_keys=["ced"], data=data)import scraperwiki
import lxml.html

a=[101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,401,402,403,404,405,406,407,408,409,410,411,501,502,503,504,505,506,507,508,509,510,511,512,513,514,515,601,602,603,604,605,701,702,801,802]
b=[]
for i in a:
    b.append("http://www.censusdata.abs.gov.au/census_services/getproduct/census/2011/quickstat/CED"+str(i)) 
for s in range(scraperwiki.sqlite.get_var('upto'), len(b)):
    html = scraperwiki.scrape(b[s])
    root = lxml.html.fromstring(html)
    ced = root.cssselect(".geo")[0]
    cedcode = (root.cssselect(".geoCode")[0].text).split('CED')
    cedcode = cedcode[1].split('(')
    cedcode = int(cedcode[0])
    scraperwiki.sqlite.save_var('upto', a.index(cedcode))
    population = root.cssselect(".summaryData")[0]
    male = root.cssselect(".summaryData")[1]
    female = root.cssselect(".summaryData")[2]
    age = root.cssselect(".summaryData")[3]
    families = root.cssselect(".summaryData")[4]    
    children = root.cssselect(".summaryData")[5]
    dwellings = root.cssselect(".summaryData")[6]
    avgpplhouse = root.cssselect(".summaryData")[7]
    income = root.cssselect(".summaryData")[8]
    mortgage = root.cssselect(".summaryData")[9]
    rent = root.cssselect(".summaryData")[10]
    vehicles = root.cssselect(".summaryData")[11]
    sourceurl = b[s]
    tables = []
    tablelength = len(root.cssselect("td"))
    for x in range(0, tablelength):
        tables.append(root.cssselect("td")[x].text)
    htmldump = lxml.etree.tostring(root)
    twoormorelang = htmldump.split('"Households where two or more languages are spoken", areaPercent: QuickStats.formatValue(')[1].split(')')[0]
    unemployed = tables[(tables.index('Unemployed') + 2)]
    workedfulltime = tables[(tables.index('Worked full-time') + 2)]
    workedparttime = tables[(tables.index('Worked part-time') + 2)]
    awayfromwork = tables[(tables.index('Away from work') + 2)]
    tertiary = tables[(tables.index('University or tertiary institution') + 2)]
    bothparentsbornoverseas = tables[(tables.index('Both parents born overseas') + 2)]
    oneparentbornoverseas = float(tables[(tables.index('Father only born overseas') + 2)]) + float(tables[(tables.index('Mother only born overseas') + 2)]) 
    
    print ced.text
    print b[s]

    data = {}
    data['ced'] = ced.text
    data['cedcode'] = cedcode
    data['population'] = population.text
    data['male'] = male.text
    data['female'] = female.text
    data['age'] = age.text
    data['families'] = families.text
    data['children'] = children.text
    data['dwellings'] = dwellings.text
    data['avgpplhouse'] = avgpplhouse.text
    data['income'] = income.text
    data['mortgage'] = mortgage.text
    data['rent'] = rent.text
    data['vehicles'] = vehicles.text
    data['workedfulltime'] = workedfulltime
    data['workedparttime'] = workedparttime
    data['awayfromwork'] = awayfromwork
    data['unemployed'] = unemployed
    data['tertiaryeducation'] = tertiary
    data['bothparentsbornoverseas'] = bothparentsbornoverseas
    data['oneparentbornoverseas'] = oneparentbornoverseas
    data['twoormorelanguages'] = twoormorelang
    data['source'] = b[s]
    scraperwiki.sqlite.save(unique_keys=["ced"], data=data)
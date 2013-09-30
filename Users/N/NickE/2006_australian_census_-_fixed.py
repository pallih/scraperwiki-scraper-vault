import scraperwiki
import lxml.etree
import lxml.html
import time

a=[33850,33900,33930,33960,34000,34050,34100,34150,34200,34250,34300,34350,34400,34420,34430,34450,34550,34570,34600,34700,34740,34760,34800,34830,34850,34900,34950,34970,35000,35050,35100,35150,35250,35300,35350,35450,35500,35550,35600,35650,35670,35700,35730,35750,35770,35800,35850,35900,35950,36050,36070,36100,36150,36200,36250,36300,36350,36400,36450,36470,36480,36550,36570,36600,36650,36700,36750,36800,36850,36900,36950,37000,37090,37110,37120,37150,37170,37200,37260,37300,37330,37400,37450,37500,37550,37570,37600,37650,39399,40070,40120,40220,40250,40310,40430,40520,40700,40910,41010,41060,41140,41190,41330,41560,41750,41830,41960,42030,42110,42250,42600,42750,43080,43220,43360,43570,43650,43710,43790,43920,44000,44060,44210,44340,44550,44620,44830,45040,45090,45120,45290,45340,45400,45540,45680,45890,46090,46300,46450,46510,46670,46860,46970,47140,47290,47490,47630,47700,47800,47910,47980,48050,48130,48260,48340,48410,48540,48750,48830,49399,50080,50210,50250,50280,50350,50420,50490,50560,50630,50770,50840,50910,50980,51050,51120,51190,51260,51310,51330,51400,51470,51540,51610,51680,51750,51820,51890,51960,52030,52100,52170,52240,52310,52380,52450,52520,52590,52660,52730,52800,52870,52940,53010,53080,53150,53220,53290,53360,53430,53500,53570,53640,53710,53780,53850,53920,53990,54060,54130,54170,54200,54280,54340,54410,54480,54550,54620,54690,54760,54830,54900,54970,55040,55110,55180,55250,55320,55390,55460,55530,55600,55670,55740,55810,55880,55950,56020,56090,56160,56230,56300,56370,56440,56510,56580,56620,56650,56720,56790,56860,56930,57000,57080,57140,57210,57280,57350,57420,57490,57560,57630,57700,57770,57840,57910,57980,58050,58120,58190,58260,58330,58400,58470,58510,58540,58570,58610,58680,58760,58820,58890,59030,59100,59170,59250,59310,59380,59450,59520,59590,59660,59730,60210,60410,60610,60810,61010,61210,61410,61510,61610,61810,62010,62210,62410,62610,62810,63010,63210,63410,63610,63810,64010,64210,64610,64810,65010,65210,65410,65610,65810,70200,70300,70330,70360,70400,70540,70570,70600,70700,70770,70790,71000,71350,72000,72100,72200,72240,72270,72300,72320,72340,72360,72380,72500,72530,72800,73030,73650,73800,74020,74030,74050,74600,74650,74700,75000,75050,79399,89399,99399]
b=[]
for i in a:
    b.append("http://www.censusdata.abs.gov.au/ABSNavigation/prenav/ProductSelect?newproducttype=QuickStats&btnSelectProduct=View+QuickStats+%3E&collection=Census&period=2006&areacode=LGA"+str(i)+"&geography=&method=&productlabel=&producttype=&topic=&navmapdisplayed=true&javascript=true&breadcrumb=LP&topholder=0&leftholder=0&currentaction=201&action=401&textversion=false")
for s in b:
    c=[]
    html = scraperwiki.scrape(s)
    root = lxml.html.fromstring(html)
    quickstats = root.cssselect("td")
    for div in quickstats:
         c.append (lxml.etree.tostring(div))

    try:
        incomePosition = c.index('<td width="418"><a href="/AUSSTATS/ABS@.nsf/vwDictionary/Household%20Income%20(HIND)?opendocument" title="Definition of Household Income (HIND)"><font color="#0000FF">Median household income ($/weekly)</font></a></td>')
    except:
        income = "na"
    else:
        income = c[(incomePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        rentPosition = c.index('<td width="418"><a href="/AUSSTATS/ABS@.nsf/vwDictionary/Rent%20(weekly)%20(RNTD)%20-%20Characteristics%202006?opendocument" title="Definition of Rent (weekly) (RNTD) - Characteristics 2006"><font color="#0000FF">Median rent ($/weekly)</font></a></td>')
    except:
        rent = "na"
    else:
        rent = c[(rentPosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        agePosition = c.index('<td width="418">Median age of persons</td>')
    except:
        age = "na"
    else:
        age = c[(agePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]
        
    try:
        populationPosition = c.index('<td width="418">Total persons (excluding overseas visitors)</td>')
    except:
        population = "na"
    else:
        population = c[(populationPosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        malePosition = c.index('<td width="418">Males</td>')
    except:
        male = "na"
    else:
        male = c[(malePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        femalePosition = c.index('<td width="418">Females</td>')
    except:
        female = "na"
    else:
        female = c[(femalePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        mortgagePosition = c.index('<td width="418"><a href="/AUSSTATS/ABS@.nsf/vwDictionary/Housing%20Loan%20Repayments%20(monthly)%20(HLRD)%20-%20Characteristics%202006?opendocument" title="Definition of Housing Loan Repayments (monthly) (HLRD) - Characteristics 2006"><font color="#0000FF">Median housing loan repayment ($/monthly)</font></a></td>')
    except:
        mortgage = "na"
    else:
        mortgage = c[(mortgagePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]
    
    try:
        avgpplhousePosition = c.index('<td width="418"><a href="/AUSSTATS/ABS@.nsf/vwDictionary/Household?opendocument" title="Definition of Household"><font color="#0000FF">Average household size</font></a></td>')
    except:
        avgpplhouse = "na"
    else:
        avgpplhouse = c[(avgpplhousePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    lgacode = root.cssselect(".locationcode")[0].text.split('LGA', 1)[1]
    lga = lxml.etree.tostring(root.cssselect("meta")[2]).split('content="', 1)[1].split('(Local',1)[0]
    

    print lga
    print lgacode
    print income
    print rent
    print age
    print population
    print male
    print female
    print mortgage
    print avgpplhouse
    
    data = {}
    data['lga'] = lga
    data['lgacode'] = lgacode
    data['population'] = population
    data['male'] = male
    data['female'] = female
    data['age'] = age
    data['avgpplhouse'] = avgpplhouse
    data['income'] = income
    data['mortgage'] = mortgage
    data['rent'] = rent
    scraperwiki.sqlite.save(unique_keys=["lga"], data=data)
    time.sleep(5)
import scraperwiki
import lxml.etree
import lxml.html
import time

a=[33850,33900,33930,33960,34000,34050,34100,34150,34200,34250,34300,34350,34400,34420,34430,34450,34550,34570,34600,34700,34740,34760,34800,34830,34850,34900,34950,34970,35000,35050,35100,35150,35250,35300,35350,35450,35500,35550,35600,35650,35670,35700,35730,35750,35770,35800,35850,35900,35950,36050,36070,36100,36150,36200,36250,36300,36350,36400,36450,36470,36480,36550,36570,36600,36650,36700,36750,36800,36850,36900,36950,37000,37090,37110,37120,37150,37170,37200,37260,37300,37330,37400,37450,37500,37550,37570,37600,37650,39399,40070,40120,40220,40250,40310,40430,40520,40700,40910,41010,41060,41140,41190,41330,41560,41750,41830,41960,42030,42110,42250,42600,42750,43080,43220,43360,43570,43650,43710,43790,43920,44000,44060,44210,44340,44550,44620,44830,45040,45090,45120,45290,45340,45400,45540,45680,45890,46090,46300,46450,46510,46670,46860,46970,47140,47290,47490,47630,47700,47800,47910,47980,48050,48130,48260,48340,48410,48540,48750,48830,49399,50080,50210,50250,50280,50350,50420,50490,50560,50630,50770,50840,50910,50980,51050,51120,51190,51260,51310,51330,51400,51470,51540,51610,51680,51750,51820,51890,51960,52030,52100,52170,52240,52310,52380,52450,52520,52590,52660,52730,52800,52870,52940,53010,53080,53150,53220,53290,53360,53430,53500,53570,53640,53710,53780,53850,53920,53990,54060,54130,54170,54200,54280,54340,54410,54480,54550,54620,54690,54760,54830,54900,54970,55040,55110,55180,55250,55320,55390,55460,55530,55600,55670,55740,55810,55880,55950,56020,56090,56160,56230,56300,56370,56440,56510,56580,56620,56650,56720,56790,56860,56930,57000,57080,57140,57210,57280,57350,57420,57490,57560,57630,57700,57770,57840,57910,57980,58050,58120,58190,58260,58330,58400,58470,58510,58540,58570,58610,58680,58760,58820,58890,59030,59100,59170,59250,59310,59380,59450,59520,59590,59660,59730,60210,60410,60610,60810,61010,61210,61410,61510,61610,61810,62010,62210,62410,62610,62810,63010,63210,63410,63610,63810,64010,64210,64610,64810,65010,65210,65410,65610,65810,70200,70300,70330,70360,70400,70540,70570,70600,70700,70770,70790,71000,71350,72000,72100,72200,72240,72270,72300,72320,72340,72360,72380,72500,72530,72800,73030,73650,73800,74020,74030,74050,74600,74650,74700,75000,75050,79399,89399,99399]
b=[]
for i in a:
    b.append("http://www.censusdata.abs.gov.au/ABSNavigation/prenav/ProductSelect?newproducttype=QuickStats&btnSelectProduct=View+QuickStats+%3E&collection=Census&period=2006&areacode=LGA"+str(i)+"&geography=&method=&productlabel=&producttype=&topic=&navmapdisplayed=true&javascript=true&breadcrumb=LP&topholder=0&leftholder=0&currentaction=201&action=401&textversion=false")
for s in b:
    c=[]
    html = scraperwiki.scrape(s)
    root = lxml.html.fromstring(html)
    quickstats = root.cssselect("td")
    for div in quickstats:
         c.append (lxml.etree.tostring(div))

    try:
        incomePosition = c.index('<td width="418"><a href="/AUSSTATS/ABS@.nsf/vwDictionary/Household%20Income%20(HIND)?opendocument" title="Definition of Household Income (HIND)"><font color="#0000FF">Median household income ($/weekly)</font></a></td>')
    except:
        income = "na"
    else:
        income = c[(incomePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        rentPosition = c.index('<td width="418"><a href="/AUSSTATS/ABS@.nsf/vwDictionary/Rent%20(weekly)%20(RNTD)%20-%20Characteristics%202006?opendocument" title="Definition of Rent (weekly) (RNTD) - Characteristics 2006"><font color="#0000FF">Median rent ($/weekly)</font></a></td>')
    except:
        rent = "na"
    else:
        rent = c[(rentPosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        agePosition = c.index('<td width="418">Median age of persons</td>')
    except:
        age = "na"
    else:
        age = c[(agePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]
        
    try:
        populationPosition = c.index('<td width="418">Total persons (excluding overseas visitors)</td>')
    except:
        population = "na"
    else:
        population = c[(populationPosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        malePosition = c.index('<td width="418">Males</td>')
    except:
        male = "na"
    else:
        male = c[(malePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        femalePosition = c.index('<td width="418">Females</td>')
    except:
        female = "na"
    else:
        female = c[(femalePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        mortgagePosition = c.index('<td width="418"><a href="/AUSSTATS/ABS@.nsf/vwDictionary/Housing%20Loan%20Repayments%20(monthly)%20(HLRD)%20-%20Characteristics%202006?opendocument" title="Definition of Housing Loan Repayments (monthly) (HLRD) - Characteristics 2006"><font color="#0000FF">Median housing loan repayment ($/monthly)</font></a></td>')
    except:
        mortgage = "na"
    else:
        mortgage = c[(mortgagePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]
    
    try:
        avgpplhousePosition = c.index('<td width="418"><a href="/AUSSTATS/ABS@.nsf/vwDictionary/Household?opendocument" title="Definition of Household"><font color="#0000FF">Average household size</font></a></td>')
    except:
        avgpplhouse = "na"
    else:
        avgpplhouse = c[(avgpplhousePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    lgacode = root.cssselect(".locationcode")[0].text.split('LGA', 1)[1]
    lga = lxml.etree.tostring(root.cssselect("meta")[2]).split('content="', 1)[1].split('(Local',1)[0]
    

    print lga
    print lgacode
    print income
    print rent
    print age
    print population
    print male
    print female
    print mortgage
    print avgpplhouse
    
    data = {}
    data['lga'] = lga
    data['lgacode'] = lgacode
    data['population'] = population
    data['male'] = male
    data['female'] = female
    data['age'] = age
    data['avgpplhouse'] = avgpplhouse
    data['income'] = income
    data['mortgage'] = mortgage
    data['rent'] = rent
    scraperwiki.sqlite.save(unique_keys=["lga"], data=data)
    time.sleep(5)
import scraperwiki
import lxml.etree
import lxml.html
import time

a=[33850,33900,33930,33960,34000,34050,34100,34150,34200,34250,34300,34350,34400,34420,34430,34450,34550,34570,34600,34700,34740,34760,34800,34830,34850,34900,34950,34970,35000,35050,35100,35150,35250,35300,35350,35450,35500,35550,35600,35650,35670,35700,35730,35750,35770,35800,35850,35900,35950,36050,36070,36100,36150,36200,36250,36300,36350,36400,36450,36470,36480,36550,36570,36600,36650,36700,36750,36800,36850,36900,36950,37000,37090,37110,37120,37150,37170,37200,37260,37300,37330,37400,37450,37500,37550,37570,37600,37650,39399,40070,40120,40220,40250,40310,40430,40520,40700,40910,41010,41060,41140,41190,41330,41560,41750,41830,41960,42030,42110,42250,42600,42750,43080,43220,43360,43570,43650,43710,43790,43920,44000,44060,44210,44340,44550,44620,44830,45040,45090,45120,45290,45340,45400,45540,45680,45890,46090,46300,46450,46510,46670,46860,46970,47140,47290,47490,47630,47700,47800,47910,47980,48050,48130,48260,48340,48410,48540,48750,48830,49399,50080,50210,50250,50280,50350,50420,50490,50560,50630,50770,50840,50910,50980,51050,51120,51190,51260,51310,51330,51400,51470,51540,51610,51680,51750,51820,51890,51960,52030,52100,52170,52240,52310,52380,52450,52520,52590,52660,52730,52800,52870,52940,53010,53080,53150,53220,53290,53360,53430,53500,53570,53640,53710,53780,53850,53920,53990,54060,54130,54170,54200,54280,54340,54410,54480,54550,54620,54690,54760,54830,54900,54970,55040,55110,55180,55250,55320,55390,55460,55530,55600,55670,55740,55810,55880,55950,56020,56090,56160,56230,56300,56370,56440,56510,56580,56620,56650,56720,56790,56860,56930,57000,57080,57140,57210,57280,57350,57420,57490,57560,57630,57700,57770,57840,57910,57980,58050,58120,58190,58260,58330,58400,58470,58510,58540,58570,58610,58680,58760,58820,58890,59030,59100,59170,59250,59310,59380,59450,59520,59590,59660,59730,60210,60410,60610,60810,61010,61210,61410,61510,61610,61810,62010,62210,62410,62610,62810,63010,63210,63410,63610,63810,64010,64210,64610,64810,65010,65210,65410,65610,65810,70200,70300,70330,70360,70400,70540,70570,70600,70700,70770,70790,71000,71350,72000,72100,72200,72240,72270,72300,72320,72340,72360,72380,72500,72530,72800,73030,73650,73800,74020,74030,74050,74600,74650,74700,75000,75050,79399,89399,99399]
b=[]
for i in a:
    b.append("http://www.censusdata.abs.gov.au/ABSNavigation/prenav/ProductSelect?newproducttype=QuickStats&btnSelectProduct=View+QuickStats+%3E&collection=Census&period=2006&areacode=LGA"+str(i)+"&geography=&method=&productlabel=&producttype=&topic=&navmapdisplayed=true&javascript=true&breadcrumb=LP&topholder=0&leftholder=0&currentaction=201&action=401&textversion=false")
for s in b:
    c=[]
    html = scraperwiki.scrape(s)
    root = lxml.html.fromstring(html)
    quickstats = root.cssselect("td")
    for div in quickstats:
         c.append (lxml.etree.tostring(div))

    try:
        incomePosition = c.index('<td width="418"><a href="/AUSSTATS/ABS@.nsf/vwDictionary/Household%20Income%20(HIND)?opendocument" title="Definition of Household Income (HIND)"><font color="#0000FF">Median household income ($/weekly)</font></a></td>')
    except:
        income = "na"
    else:
        income = c[(incomePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        rentPosition = c.index('<td width="418"><a href="/AUSSTATS/ABS@.nsf/vwDictionary/Rent%20(weekly)%20(RNTD)%20-%20Characteristics%202006?opendocument" title="Definition of Rent (weekly) (RNTD) - Characteristics 2006"><font color="#0000FF">Median rent ($/weekly)</font></a></td>')
    except:
        rent = "na"
    else:
        rent = c[(rentPosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        agePosition = c.index('<td width="418">Median age of persons</td>')
    except:
        age = "na"
    else:
        age = c[(agePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]
        
    try:
        populationPosition = c.index('<td width="418">Total persons (excluding overseas visitors)</td>')
    except:
        population = "na"
    else:
        population = c[(populationPosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        malePosition = c.index('<td width="418">Males</td>')
    except:
        male = "na"
    else:
        male = c[(malePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        femalePosition = c.index('<td width="418">Females</td>')
    except:
        female = "na"
    else:
        female = c[(femalePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        mortgagePosition = c.index('<td width="418"><a href="/AUSSTATS/ABS@.nsf/vwDictionary/Housing%20Loan%20Repayments%20(monthly)%20(HLRD)%20-%20Characteristics%202006?opendocument" title="Definition of Housing Loan Repayments (monthly) (HLRD) - Characteristics 2006"><font color="#0000FF">Median housing loan repayment ($/monthly)</font></a></td>')
    except:
        mortgage = "na"
    else:
        mortgage = c[(mortgagePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]
    
    try:
        avgpplhousePosition = c.index('<td width="418"><a href="/AUSSTATS/ABS@.nsf/vwDictionary/Household?opendocument" title="Definition of Household"><font color="#0000FF">Average household size</font></a></td>')
    except:
        avgpplhouse = "na"
    else:
        avgpplhouse = c[(avgpplhousePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    lgacode = root.cssselect(".locationcode")[0].text.split('LGA', 1)[1]
    lga = lxml.etree.tostring(root.cssselect("meta")[2]).split('content="', 1)[1].split('(Local',1)[0]
    

    print lga
    print lgacode
    print income
    print rent
    print age
    print population
    print male
    print female
    print mortgage
    print avgpplhouse
    
    data = {}
    data['lga'] = lga
    data['lgacode'] = lgacode
    data['population'] = population
    data['male'] = male
    data['female'] = female
    data['age'] = age
    data['avgpplhouse'] = avgpplhouse
    data['income'] = income
    data['mortgage'] = mortgage
    data['rent'] = rent
    scraperwiki.sqlite.save(unique_keys=["lga"], data=data)
    time.sleep(5)
import scraperwiki
import lxml.etree
import lxml.html
import time

a=[33850,33900,33930,33960,34000,34050,34100,34150,34200,34250,34300,34350,34400,34420,34430,34450,34550,34570,34600,34700,34740,34760,34800,34830,34850,34900,34950,34970,35000,35050,35100,35150,35250,35300,35350,35450,35500,35550,35600,35650,35670,35700,35730,35750,35770,35800,35850,35900,35950,36050,36070,36100,36150,36200,36250,36300,36350,36400,36450,36470,36480,36550,36570,36600,36650,36700,36750,36800,36850,36900,36950,37000,37090,37110,37120,37150,37170,37200,37260,37300,37330,37400,37450,37500,37550,37570,37600,37650,39399,40070,40120,40220,40250,40310,40430,40520,40700,40910,41010,41060,41140,41190,41330,41560,41750,41830,41960,42030,42110,42250,42600,42750,43080,43220,43360,43570,43650,43710,43790,43920,44000,44060,44210,44340,44550,44620,44830,45040,45090,45120,45290,45340,45400,45540,45680,45890,46090,46300,46450,46510,46670,46860,46970,47140,47290,47490,47630,47700,47800,47910,47980,48050,48130,48260,48340,48410,48540,48750,48830,49399,50080,50210,50250,50280,50350,50420,50490,50560,50630,50770,50840,50910,50980,51050,51120,51190,51260,51310,51330,51400,51470,51540,51610,51680,51750,51820,51890,51960,52030,52100,52170,52240,52310,52380,52450,52520,52590,52660,52730,52800,52870,52940,53010,53080,53150,53220,53290,53360,53430,53500,53570,53640,53710,53780,53850,53920,53990,54060,54130,54170,54200,54280,54340,54410,54480,54550,54620,54690,54760,54830,54900,54970,55040,55110,55180,55250,55320,55390,55460,55530,55600,55670,55740,55810,55880,55950,56020,56090,56160,56230,56300,56370,56440,56510,56580,56620,56650,56720,56790,56860,56930,57000,57080,57140,57210,57280,57350,57420,57490,57560,57630,57700,57770,57840,57910,57980,58050,58120,58190,58260,58330,58400,58470,58510,58540,58570,58610,58680,58760,58820,58890,59030,59100,59170,59250,59310,59380,59450,59520,59590,59660,59730,60210,60410,60610,60810,61010,61210,61410,61510,61610,61810,62010,62210,62410,62610,62810,63010,63210,63410,63610,63810,64010,64210,64610,64810,65010,65210,65410,65610,65810,70200,70300,70330,70360,70400,70540,70570,70600,70700,70770,70790,71000,71350,72000,72100,72200,72240,72270,72300,72320,72340,72360,72380,72500,72530,72800,73030,73650,73800,74020,74030,74050,74600,74650,74700,75000,75050,79399,89399,99399]
b=[]
for i in a:
    b.append("http://www.censusdata.abs.gov.au/ABSNavigation/prenav/ProductSelect?newproducttype=QuickStats&btnSelectProduct=View+QuickStats+%3E&collection=Census&period=2006&areacode=LGA"+str(i)+"&geography=&method=&productlabel=&producttype=&topic=&navmapdisplayed=true&javascript=true&breadcrumb=LP&topholder=0&leftholder=0&currentaction=201&action=401&textversion=false")
for s in b:
    c=[]
    html = scraperwiki.scrape(s)
    root = lxml.html.fromstring(html)
    quickstats = root.cssselect("td")
    for div in quickstats:
         c.append (lxml.etree.tostring(div))

    try:
        incomePosition = c.index('<td width="418"><a href="/AUSSTATS/ABS@.nsf/vwDictionary/Household%20Income%20(HIND)?opendocument" title="Definition of Household Income (HIND)"><font color="#0000FF">Median household income ($/weekly)</font></a></td>')
    except:
        income = "na"
    else:
        income = c[(incomePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        rentPosition = c.index('<td width="418"><a href="/AUSSTATS/ABS@.nsf/vwDictionary/Rent%20(weekly)%20(RNTD)%20-%20Characteristics%202006?opendocument" title="Definition of Rent (weekly) (RNTD) - Characteristics 2006"><font color="#0000FF">Median rent ($/weekly)</font></a></td>')
    except:
        rent = "na"
    else:
        rent = c[(rentPosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        agePosition = c.index('<td width="418">Median age of persons</td>')
    except:
        age = "na"
    else:
        age = c[(agePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]
        
    try:
        populationPosition = c.index('<td width="418">Total persons (excluding overseas visitors)</td>')
    except:
        population = "na"
    else:
        population = c[(populationPosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        malePosition = c.index('<td width="418">Males</td>')
    except:
        male = "na"
    else:
        male = c[(malePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        femalePosition = c.index('<td width="418">Females</td>')
    except:
        female = "na"
    else:
        female = c[(femalePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    try:
        mortgagePosition = c.index('<td width="418"><a href="/AUSSTATS/ABS@.nsf/vwDictionary/Housing%20Loan%20Repayments%20(monthly)%20(HLRD)%20-%20Characteristics%202006?opendocument" title="Definition of Housing Loan Repayments (monthly) (HLRD) - Characteristics 2006"><font color="#0000FF">Median housing loan repayment ($/monthly)</font></a></td>')
    except:
        mortgage = "na"
    else:
        mortgage = c[(mortgagePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]
    
    try:
        avgpplhousePosition = c.index('<td width="418"><a href="/AUSSTATS/ABS@.nsf/vwDictionary/Household?opendocument" title="Definition of Household"><font color="#0000FF">Average household size</font></a></td>')
    except:
        avgpplhouse = "na"
    else:
        avgpplhouse = c[(avgpplhousePosition + 1)].split('"right">', 1)[1].split('</div>', 1)[0]

    lgacode = root.cssselect(".locationcode")[0].text.split('LGA', 1)[1]
    lga = lxml.etree.tostring(root.cssselect("meta")[2]).split('content="', 1)[1].split('(Local',1)[0]
    

    print lga
    print lgacode
    print income
    print rent
    print age
    print population
    print male
    print female
    print mortgage
    print avgpplhouse
    
    data = {}
    data['lga'] = lga
    data['lgacode'] = lgacode
    data['population'] = population
    data['male'] = male
    data['female'] = female
    data['age'] = age
    data['avgpplhouse'] = avgpplhouse
    data['income'] = income
    data['mortgage'] = mortgage
    data['rent'] = rent
    scraperwiki.sqlite.save(unique_keys=["lga"], data=data)
    time.sleep(5)

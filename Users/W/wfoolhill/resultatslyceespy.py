# Retrieve the data from "http://www.education.gouv.fr/pid23933/indicateurs-de-resultats-des-lycees.html"
# More on "http://www.nosdonnees.fr/" (OpenData movement in France)

from lxml import etree
import re
import scraperwiki


class Department( object ):
    def __init__( self ):
        self.code = 0
        self.name = ""
        self.nbLycees = 0
        self.lCities = []
    def __repr__( self ):
        msg = u"département '%s' (%i):" % ( self.name, self.code )
        msg += u" %i villes" % ( len(self.lCities) )
        if self.nbLycees > 0:
            msg += u", %i lycées" % ( self.nbLycees )
        return msg.encode('utf-8')


class City( object ):
    def __init__( self ):
        self.name = ""
        self.lLycees = []
    def __repr__( self ):
        msg = u"ville '%s':" % ( self.name )
        if len(self.lLycees) < 2:
            msg += u" %i lycée" % ( len(self.lLycees) )
        else:
            msg += u" %i lycées" % ( len(self.lLycees) )
        return msg.encode('utf-8')


class Lycee( object ):
    def __init__( self ):
        self.name=  ""
        self.isPro = False
        self.href = ""
        self.dBac = {}  # dico which keys are 'serie' (S, ES, L...) and values are data about 'réussite au bac'
    def printBac( self ):
        for serie in self.dBac.keys():
            msg = u"série '%s':" % ( serie )
            for i in self.dBac[ serie ]:
                msg += u" %s" % ( i )
            print msg.encode('utf-8')
            

class OpenDataNatEduc( object ):
    def __init__( self ):
        self.url = "http://www.education.gouv.fr/pid23933/indicateurs-resultats-des-lycees.html?lycee=&ville=&departement=0&num=&annee=2&type=0&seriegt=&seriepro=&validation=1"
        self.tree = None
        self.parser = etree.HTMLParser()
        self.root = None
        self.deptCode = 0
        self.verbose = 0
        self.dFields2Choices = {}
        self.lDepts = []
        self.lYears = []
        self.lSeries = []
        self.lSectors = []

    def getFieldsAndChoices( self ):
        if self.verbose > 0:
            print "retrieve the departments, years, cursus, series and sectors from the HTML form..."
        self.tree = etree.parse( self.url, self.parser )
        self.root = self.tree.getroot()
        for e in self.root.findall( ".//select" ):
            self.dFields2Choices[ e.attrib["name"] ] = []
            for c in e.getchildren():
                if c.attrib["value"] not in [ "0", "" ]:
                    if c.attrib["value"].lstrip().rstrip() == "all":
                        self.dFields2Choices[ e.attrib["name"] ].append( [ c.attrib["value"].lstrip().rstrip(),
                                                                           u"Toutes séries" ] )
                    else:
                        self.dFields2Choices[ e.attrib["name"] ].append( [ c.attrib["value"].lstrip().rstrip(),
                                                                           c.text.lstrip().rstrip() ] )
                if c.attrib["value"].isdigit() \
                        and not c.attrib["label"].isdigit() \
                        and 1<=int(c.attrib["value"]) \
                        and re.search("[a-z]",c.attrib["label"])==None:
                    d = Department()
                    d.code = int(c.attrib["value"])
                    d.name = c.attrib["label"].lstrip().rstrip()
                    self.lDepts.append( d )
        if self.verbose > 0:
            print "nb of departments: %i" % ( len(self.lDepts) )
            if self.verbose > 1:
                for i in self.dFields2Choices:
                    print "field '%s': %i values" % ( i, len(self.dFields2Choices[i]) )
                    for j in self.dFields2Choices[i]:
                        print " %s %s" % ( j[0], j[1] )


    def getTotalNbLycees( self ):
        nb = 0
        for dept in self.lDepts:
            nb += dept.nbLycees
        return nb


    def getNbPages( self, tree ):
        """
        A department can have too many lycees for a single page.
        This method returns the number of pages one will have to parse.
        """
        nbPages = 1
        for c1 in tree.getroot().findall( ".//div" ):
            for c2 in c1.getchildren():
                if c2.attrib.has_key( "class" ) \
                        and c2.attrib["class"] == "recherche_pagination_indic_lycee":
                    for c3 in c2.getchildren():
                        if c3.attrib.has_key( "href" ) and c3.text.isdigit():
                            nbPages = int(c3.text)
        return nbPages
    
    
    def parsePage( self, dept, tree ):
        """
        Parse a HTML page for a department to retrieve the name of all its cities and lycees.
        """
        for c1 in tree.getroot().findall( ".//div" ):
            for c2 in c1.getchildren():
                if not c2.attrib.has_key( "class" ):
                    continue
                if c2.attrib["class"] == "result_pl" and dept.nbLycees == 0:
                    dept.nbLycees = int(c2.getchildren()[2].text)
                    if self.verbose > 1:
                        print "nb of lycees: %s" % ( dept.nbLycees )
                elif c2.attrib["class"] == "ville":
                    for c3 in c2.getchildren():
                        if c3.attrib[ "class" ] == "nom_ville":
                            cityName = c3.text.lstrip().rstrip()
                            if len(dept.lCities) > 0 and dept.lCities[-1].name == cityName:
                                city = dept.lCities[-1]
                            else:
                                city = City()
                                city.name = cityName
                                dept.lCities.append( city )
                        if c3.attrib[ "class" ] == "etablissement":
                            lycee = Lycee()
                            children = c3.getchildren()
                            if len(children) > 0:
                                lycee.name = children[0].text.lstrip().rstrip()
                                lycee.href = "http://www.education.gouv.fr" + children[0].attrib[ "href" ]
                            else:
                                lycee.name = c3.text.replace("(*)","").lstrip().rstrip()
                            if "PROFESSIONNEL" in lycee.name:
                                lycee.isPro = True
                            dept.lCities[-1].lLycees.append( lycee )


    def getDataPerDept( self ):
        """
        For each department, retrieve its cities and lycees by parsing (a) HMTL page(s).
        """
        if self.verbose > 0:
            print "for each department, retrieve its cities and lycees..."
        genericUrl = self.url.replace("departement=0","departement=%s").replace("?lycee","?currentPage=0&lycee")
        if self.deptCode == 0:
            lCodes = range(1,len(self.lDepts)+1)
        else:
            lCodes = [ self.deptCode ]
        for code in lCodes:
            dept = self.lDepts[ code-1 ]
            if self.verbose > 0:
                print "department '%s' (%s)" % ( dept.name, dept.code )
            t = etree.parse( genericUrl % ( dept.code ), self.parser )
            self.parsePage( dept, t )
            nbPages = self.getNbPages( t )
            for page in range(1,nbPages):
                url = genericUrl.replace("currentPage=0","currentPage=%i"%page) % ( dept.code )
                t = etree.parse( url, self.parser )
                self.parsePage( dept, t )
        if self.verbose > 0:
            print "total nb of lycees: %i" % ( self.getTotalNbLycees() )
            if self.deptCode != 0:
                print self.lDepts[ self.deptCode-1 ]
                for city in self.lDepts[ self.deptCode-1 ].lCities:
                    print city


    def getDataPerLycee( self ):
        """
        For each lycee, retrieve its data by parsing a HMTL page.
        """
        for dept in self.lDepts:
            for city in dept.lCities:
                for lycee in city.lLycees:
                    if lycee.href == "":
                        continue
                    t = etree.parse( lycee.href, self.parser )
                    if self.verbose > 0:
                        print "get 'bac' data for '%s' (%s)..." % ( lycee.name,
                                                                    dept )
                    lTables = t.xpath( "//table" )
                    for row in lTables[0]:
                        lCells = row.xpath('./td')
                        if lCells == []:
                            continue
                        lycee.dBac[ unicode(lCells[0].text) ] = []
                        for cell in lCells[1:]:
                            if cell.text == "ND" or cell.text == "" or cell.text == None:
                                lycee.dBac[ unicode(lCells[0].text) ].append( "NA" )
                            else:
                                lycee.dBac[ unicode(lCells[0].text) ].append( cell.text )
                    if self.verbose > 0:
                        lycee.printBac()
                        

    def saveDataInFile( self ):
        """
        Save all the data about lycees in a 'csv' file.
        """
        outFile = "outReussiteLycees.csv"
        if self.verbose > 0:
            print "save data in file '%s'..." % ( outFile )
        outFileHandler = open( outFile, "w" )

        ## write the column names
        msg = u"departement,ville,lycee"
        for field in ["seriegt","seriepro"]:
            for choice in self.dFields2Choices[ field ]:
                for number in [ u"tauxConstate",
                                u"tauxAttenduRefAcademie",
                                u"valeurAjouteeAcademie",
                                u"tauxAttenduRefNationale",
                                u"valeurAjouteeRefNationale",
                                u"nbElevesPresentsBac" ]:
                    msg += ",%s_%s_%s" % ( field, choice[1], number )
        outFileHandler.write( "%s\n" % ( msg.encode('utf-8') ) )
        
        ## write the data for each lycee
        for dept in self.lDepts:
            for city in dept.lCities:
                for lycee in city.lLycees:
                    msg = "%s,%s,%s" % ( dept.name.encode('utf-8'),
                                            city.name,
                                            lycee.name )
                    for field in [ u"seriegt", u"seriepro" ]:
                        for choice in self.dFields2Choices[ field ]:
                            serie = unicode(choice[1])
                            if serie != u"Toutes séries":
                                if lycee.dBac.has_key( serie ):
                                    for i in range(0,6):
                                        msg += ",%s" % ( lycee.dBac[ serie ][i] )
                                else:
                                    for i in range(0,6):
                                        msg += ",NA"
                            else:
                                if field == u"seriegt" and lycee.isPro:
                                    for i in range(0,6):
                                        msg += ",NA"
                                elif field == u"seriegt" and not lycee.isPro:
                                    if lycee.dBac.has_key( serie ):
                                        for i in range(0,6):
                                            msg += ",%s" % ( lycee.dBac[ serie ][i] )
                                    else:
                                        for i in range(0,6):
                                            msg += ",NA"
                                elif field == u"seriepro" and lycee.isPro:
                                    if lycee.dBac.has_key( serie ):
                                        for i in range(0,6):
                                            msg += ",%s" % ( lycee.dBac[ serie ][i] )
                                    else:
                                        for i in range(0,6):
                                            msg += ",NA"
                                elif field == u"seriepro" and not lycee.isPro:
                                    for i in range(0,6):
                                        msg += ",NA"
                    outFileHandler.write( "%s\n" % msg )
        outFileHandler.close()


    def saveDataInScraperWiki( self ):
        """
        Need to use scraperwiki.datastore.save(unique_keys=[], data={}, date=None, latlng=[None,None])
        Saves a dictionary, data, to the datastore. unique_keys is a list of keys appearing in the dictionary used to determine if if a record should be inserted or updated. date and latlng are optional special fields for indexing each record. 
        """
        dTest = { "key1": [1,2], "key2": [3,4], "key3": [1,1] }
#        scraperwiki.datastore.save( dTest.keys(), dTest )
        dData = {}
        dData[ "departement" ] = []
        dData[ "ville" ] = []
        dData[ "lycee" ] = []
        for d in self.lDepts:
            for c in d.lCities:
                for l in c.lLycees:
                    dData[ "departement" ].append( d.name )
                    dData[ "ville" ].append( c.name )
                    dData[ "lycee" ].append( l.name )
        scraperwiki.datastore.save( dData.keys(), dData )


    def run( self ):
        self.getFieldsAndChoices()
        self.getDataPerDept()
        self.getDataPerLycee()
        self.saveDataInScraperWiki()
#        self.saveDataInFile()


i = OpenDataNatEduc()
#i.deptCode = 1   # comment this line to retrieve the data for all departments, here only lycees from the "AIN" department will be retrieved
i.verbose = 1
i.run()

# Retrieve the data from "http://www.education.gouv.fr/pid23933/indicateurs-de-resultats-des-lycees.html"
# More on "http://www.nosdonnees.fr/" (OpenData movement in France)

from lxml import etree
import re
import scraperwiki


class Department( object ):
    def __init__( self ):
        self.code = 0
        self.name = ""
        self.nbLycees = 0
        self.lCities = []
    def __repr__( self ):
        msg = u"département '%s' (%i):" % ( self.name, self.code )
        msg += u" %i villes" % ( len(self.lCities) )
        if self.nbLycees > 0:
            msg += u", %i lycées" % ( self.nbLycees )
        return msg.encode('utf-8')


class City( object ):
    def __init__( self ):
        self.name = ""
        self.lLycees = []
    def __repr__( self ):
        msg = u"ville '%s':" % ( self.name )
        if len(self.lLycees) < 2:
            msg += u" %i lycée" % ( len(self.lLycees) )
        else:
            msg += u" %i lycées" % ( len(self.lLycees) )
        return msg.encode('utf-8')


class Lycee( object ):
    def __init__( self ):
        self.name=  ""
        self.isPro = False
        self.href = ""
        self.dBac = {}  # dico which keys are 'serie' (S, ES, L...) and values are data about 'réussite au bac'
    def printBac( self ):
        for serie in self.dBac.keys():
            msg = u"série '%s':" % ( serie )
            for i in self.dBac[ serie ]:
                msg += u" %s" % ( i )
            print msg.encode('utf-8')
            

class OpenDataNatEduc( object ):
    def __init__( self ):
        self.url = "http://www.education.gouv.fr/pid23933/indicateurs-resultats-des-lycees.html?lycee=&ville=&departement=0&num=&annee=2&type=0&seriegt=&seriepro=&validation=1"
        self.tree = None
        self.parser = etree.HTMLParser()
        self.root = None
        self.deptCode = 0
        self.verbose = 0
        self.dFields2Choices = {}
        self.lDepts = []
        self.lYears = []
        self.lSeries = []
        self.lSectors = []

    def getFieldsAndChoices( self ):
        if self.verbose > 0:
            print "retrieve the departments, years, cursus, series and sectors from the HTML form..."
        self.tree = etree.parse( self.url, self.parser )
        self.root = self.tree.getroot()
        for e in self.root.findall( ".//select" ):
            self.dFields2Choices[ e.attrib["name"] ] = []
            for c in e.getchildren():
                if c.attrib["value"] not in [ "0", "" ]:
                    if c.attrib["value"].lstrip().rstrip() == "all":
                        self.dFields2Choices[ e.attrib["name"] ].append( [ c.attrib["value"].lstrip().rstrip(),
                                                                           u"Toutes séries" ] )
                    else:
                        self.dFields2Choices[ e.attrib["name"] ].append( [ c.attrib["value"].lstrip().rstrip(),
                                                                           c.text.lstrip().rstrip() ] )
                if c.attrib["value"].isdigit() \
                        and not c.attrib["label"].isdigit() \
                        and 1<=int(c.attrib["value"]) \
                        and re.search("[a-z]",c.attrib["label"])==None:
                    d = Department()
                    d.code = int(c.attrib["value"])
                    d.name = c.attrib["label"].lstrip().rstrip()
                    self.lDepts.append( d )
        if self.verbose > 0:
            print "nb of departments: %i" % ( len(self.lDepts) )
            if self.verbose > 1:
                for i in self.dFields2Choices:
                    print "field '%s': %i values" % ( i, len(self.dFields2Choices[i]) )
                    for j in self.dFields2Choices[i]:
                        print " %s %s" % ( j[0], j[1] )


    def getTotalNbLycees( self ):
        nb = 0
        for dept in self.lDepts:
            nb += dept.nbLycees
        return nb


    def getNbPages( self, tree ):
        """
        A department can have too many lycees for a single page.
        This method returns the number of pages one will have to parse.
        """
        nbPages = 1
        for c1 in tree.getroot().findall( ".//div" ):
            for c2 in c1.getchildren():
                if c2.attrib.has_key( "class" ) \
                        and c2.attrib["class"] == "recherche_pagination_indic_lycee":
                    for c3 in c2.getchildren():
                        if c3.attrib.has_key( "href" ) and c3.text.isdigit():
                            nbPages = int(c3.text)
        return nbPages
    
    
    def parsePage( self, dept, tree ):
        """
        Parse a HTML page for a department to retrieve the name of all its cities and lycees.
        """
        for c1 in tree.getroot().findall( ".//div" ):
            for c2 in c1.getchildren():
                if not c2.attrib.has_key( "class" ):
                    continue
                if c2.attrib["class"] == "result_pl" and dept.nbLycees == 0:
                    dept.nbLycees = int(c2.getchildren()[2].text)
                    if self.verbose > 1:
                        print "nb of lycees: %s" % ( dept.nbLycees )
                elif c2.attrib["class"] == "ville":
                    for c3 in c2.getchildren():
                        if c3.attrib[ "class" ] == "nom_ville":
                            cityName = c3.text.lstrip().rstrip()
                            if len(dept.lCities) > 0 and dept.lCities[-1].name == cityName:
                                city = dept.lCities[-1]
                            else:
                                city = City()
                                city.name = cityName
                                dept.lCities.append( city )
                        if c3.attrib[ "class" ] == "etablissement":
                            lycee = Lycee()
                            children = c3.getchildren()
                            if len(children) > 0:
                                lycee.name = children[0].text.lstrip().rstrip()
                                lycee.href = "http://www.education.gouv.fr" + children[0].attrib[ "href" ]
                            else:
                                lycee.name = c3.text.replace("(*)","").lstrip().rstrip()
                            if "PROFESSIONNEL" in lycee.name:
                                lycee.isPro = True
                            dept.lCities[-1].lLycees.append( lycee )


    def getDataPerDept( self ):
        """
        For each department, retrieve its cities and lycees by parsing (a) HMTL page(s).
        """
        if self.verbose > 0:
            print "for each department, retrieve its cities and lycees..."
        genericUrl = self.url.replace("departement=0","departement=%s").replace("?lycee","?currentPage=0&lycee")
        if self.deptCode == 0:
            lCodes = range(1,len(self.lDepts)+1)
        else:
            lCodes = [ self.deptCode ]
        for code in lCodes:
            dept = self.lDepts[ code-1 ]
            if self.verbose > 0:
                print "department '%s' (%s)" % ( dept.name, dept.code )
            t = etree.parse( genericUrl % ( dept.code ), self.parser )
            self.parsePage( dept, t )
            nbPages = self.getNbPages( t )
            for page in range(1,nbPages):
                url = genericUrl.replace("currentPage=0","currentPage=%i"%page) % ( dept.code )
                t = etree.parse( url, self.parser )
                self.parsePage( dept, t )
        if self.verbose > 0:
            print "total nb of lycees: %i" % ( self.getTotalNbLycees() )
            if self.deptCode != 0:
                print self.lDepts[ self.deptCode-1 ]
                for city in self.lDepts[ self.deptCode-1 ].lCities:
                    print city


    def getDataPerLycee( self ):
        """
        For each lycee, retrieve its data by parsing a HMTL page.
        """
        for dept in self.lDepts:
            for city in dept.lCities:
                for lycee in city.lLycees:
                    if lycee.href == "":
                        continue
                    t = etree.parse( lycee.href, self.parser )
                    if self.verbose > 0:
                        print "get 'bac' data for '%s' (%s)..." % ( lycee.name,
                                                                    dept )
                    lTables = t.xpath( "//table" )
                    for row in lTables[0]:
                        lCells = row.xpath('./td')
                        if lCells == []:
                            continue
                        lycee.dBac[ unicode(lCells[0].text) ] = []
                        for cell in lCells[1:]:
                            if cell.text == "ND" or cell.text == "" or cell.text == None:
                                lycee.dBac[ unicode(lCells[0].text) ].append( "NA" )
                            else:
                                lycee.dBac[ unicode(lCells[0].text) ].append( cell.text )
                    if self.verbose > 0:
                        lycee.printBac()
                        

    def saveDataInFile( self ):
        """
        Save all the data about lycees in a 'csv' file.
        """
        outFile = "outReussiteLycees.csv"
        if self.verbose > 0:
            print "save data in file '%s'..." % ( outFile )
        outFileHandler = open( outFile, "w" )

        ## write the column names
        msg = u"departement,ville,lycee"
        for field in ["seriegt","seriepro"]:
            for choice in self.dFields2Choices[ field ]:
                for number in [ u"tauxConstate",
                                u"tauxAttenduRefAcademie",
                                u"valeurAjouteeAcademie",
                                u"tauxAttenduRefNationale",
                                u"valeurAjouteeRefNationale",
                                u"nbElevesPresentsBac" ]:
                    msg += ",%s_%s_%s" % ( field, choice[1], number )
        outFileHandler.write( "%s\n" % ( msg.encode('utf-8') ) )
        
        ## write the data for each lycee
        for dept in self.lDepts:
            for city in dept.lCities:
                for lycee in city.lLycees:
                    msg = "%s,%s,%s" % ( dept.name.encode('utf-8'),
                                            city.name,
                                            lycee.name )
                    for field in [ u"seriegt", u"seriepro" ]:
                        for choice in self.dFields2Choices[ field ]:
                            serie = unicode(choice[1])
                            if serie != u"Toutes séries":
                                if lycee.dBac.has_key( serie ):
                                    for i in range(0,6):
                                        msg += ",%s" % ( lycee.dBac[ serie ][i] )
                                else:
                                    for i in range(0,6):
                                        msg += ",NA"
                            else:
                                if field == u"seriegt" and lycee.isPro:
                                    for i in range(0,6):
                                        msg += ",NA"
                                elif field == u"seriegt" and not lycee.isPro:
                                    if lycee.dBac.has_key( serie ):
                                        for i in range(0,6):
                                            msg += ",%s" % ( lycee.dBac[ serie ][i] )
                                    else:
                                        for i in range(0,6):
                                            msg += ",NA"
                                elif field == u"seriepro" and lycee.isPro:
                                    if lycee.dBac.has_key( serie ):
                                        for i in range(0,6):
                                            msg += ",%s" % ( lycee.dBac[ serie ][i] )
                                    else:
                                        for i in range(0,6):
                                            msg += ",NA"
                                elif field == u"seriepro" and not lycee.isPro:
                                    for i in range(0,6):
                                        msg += ",NA"
                    outFileHandler.write( "%s\n" % msg )
        outFileHandler.close()


    def saveDataInScraperWiki( self ):
        """
        Need to use scraperwiki.datastore.save(unique_keys=[], data={}, date=None, latlng=[None,None])
        Saves a dictionary, data, to the datastore. unique_keys is a list of keys appearing in the dictionary used to determine if if a record should be inserted or updated. date and latlng are optional special fields for indexing each record. 
        """
        dTest = { "key1": [1,2], "key2": [3,4], "key3": [1,1] }
#        scraperwiki.datastore.save( dTest.keys(), dTest )
        dData = {}
        dData[ "departement" ] = []
        dData[ "ville" ] = []
        dData[ "lycee" ] = []
        for d in self.lDepts:
            for c in d.lCities:
                for l in c.lLycees:
                    dData[ "departement" ].append( d.name )
                    dData[ "ville" ].append( c.name )
                    dData[ "lycee" ].append( l.name )
        scraperwiki.datastore.save( dData.keys(), dData )


    def run( self ):
        self.getFieldsAndChoices()
        self.getDataPerDept()
        self.getDataPerLycee()
        self.saveDataInScraperWiki()
#        self.saveDataInFile()


i = OpenDataNatEduc()
#i.deptCode = 1   # comment this line to retrieve the data for all departments, here only lycees from the "AIN" department will be retrieved
i.verbose = 1
i.run()


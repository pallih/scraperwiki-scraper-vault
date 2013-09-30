import scraperwiki
import urllib2
from lxml import etree
from xml.dom.minidom import parseString

# Escondido
City_Esc = [92025,92026,92027,92029,92030,92033,92046]

# Poway
City_P = [92064,92074]

# Local San Diego
City_SDloc = [92127,92128,92129,92131]

# San Marcos
City_SM = [92069,92078,92079,92096]

# Vista
City_V = [92081,92083,92084,92085]

# Oceanside
City_O = [92049,92051,92052,92054,92055,92056,92057,92058]

# Fallbook
City_F = [92028,92088]

# Carlsbad
City_C = [92008,92009,92010,92011,92013,92018]

# Encinitas
City_E = [92023,92024]

# Solana Beach
City_S = [92075]

# Del Mar
City_DM = [92014]

URLstart = "http://api2.yp.com/listings/v1/search?searchloc="
URLend = "&term=commercial+real+estate&sort=distance&listingcount=50&key=5c08b9f6fda6feae004e30aa3386684c"

'''
zips = City_Esc + City_P + City_SDloc + City_SM + City_V + City_O + City_F + City_C + City_E + City_S + City_DM
for zip in zips:
    #download the file:
    URL = URLstart + str(zip) + URLend
    file = urllib2.urlopen(URL)
    #convert to string:
    data = file.read()
    #close file because we dont need it anymore:
    file.close()

    #parse the xml you downloaded
    dom = parseString(data)
    #retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
    Listings = dom.getElementsByTagName('searchListing')
    print str(zip) + "   " + str(len(Listings))

'''
URL = "http://api2.yp.com/listings/v1/search?searchloc=92025&radius=25&term=commercial+real+estate&sort=distance&listingcount=50&pagenum=7&key=5c08b9f6fda6feae004e30aa3386684c"

#def search_yp(URL)
file = urllib2.urlopen(URL)
#convert to string:
data = file.read()
#close file because we dont need it anymore:
file.close()
#parse the xml you downloaded
dom = parseString(data)
#retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
Listings = dom.getElementsByTagName('searchListing')
print str(len(Listings))




import scraperwiki
import urllib2
from lxml import etree
from xml.dom.minidom import parseString

# Escondido
City_Esc = [92025,92026,92027,92029,92030,92033,92046]

# Poway
City_P = [92064,92074]

# Local San Diego
City_SDloc = [92127,92128,92129,92131]

# San Marcos
City_SM = [92069,92078,92079,92096]

# Vista
City_V = [92081,92083,92084,92085]

# Oceanside
City_O = [92049,92051,92052,92054,92055,92056,92057,92058]

# Fallbook
City_F = [92028,92088]

# Carlsbad
City_C = [92008,92009,92010,92011,92013,92018]

# Encinitas
City_E = [92023,92024]

# Solana Beach
City_S = [92075]

# Del Mar
City_DM = [92014]

URLstart = "http://api2.yp.com/listings/v1/search?searchloc="
URLend = "&term=commercial+real+estate&sort=distance&listingcount=50&key=5c08b9f6fda6feae004e30aa3386684c"

'''
zips = City_Esc + City_P + City_SDloc + City_SM + City_V + City_O + City_F + City_C + City_E + City_S + City_DM
for zip in zips:
    #download the file:
    URL = URLstart + str(zip) + URLend
    file = urllib2.urlopen(URL)
    #convert to string:
    data = file.read()
    #close file because we dont need it anymore:
    file.close()

    #parse the xml you downloaded
    dom = parseString(data)
    #retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
    Listings = dom.getElementsByTagName('searchListing')
    print str(zip) + "   " + str(len(Listings))

'''
URL = "http://api2.yp.com/listings/v1/search?searchloc=92025&radius=25&term=commercial+real+estate&sort=distance&listingcount=50&pagenum=7&key=5c08b9f6fda6feae004e30aa3386684c"

#def search_yp(URL)
file = urllib2.urlopen(URL)
#convert to string:
data = file.read()
#close file because we dont need it anymore:
file.close()
#parse the xml you downloaded
dom = parseString(data)
#retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
Listings = dom.getElementsByTagName('searchListing')
print str(len(Listings))





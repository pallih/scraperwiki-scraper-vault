import scraperwiki
import re
import lxml.html


############################################################################
#
# This next section was taken from the site listed here
#
#  COPYRIGHT:  (C) 2012 John A Stevenson / @volcan01010
#           Magnus Hagdorn
#  WEBSITE: http://all-geo.org/volcan01010
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  http://www.gnu.org/licenses/gpl-3.0.html
#
#############################################################################/
 
__all__ = ['to_osgb36', 'from_osgb36']
 
try:
    import numpy as np
except ImportError:
    print "Numpy not installed.  Numpy comes with most scientific python packages."
 
import re
 
# Region codes for 100 km grid squares.
_regions=[['HL','HM','HN','HO','HP','JL','JM'],
      ['HQ','HR','HS','HT','HU','JQ','JR'],
      ['HV','HW','HX','HY','HZ','JV','JW'],
      ['NA','NB','NC','ND','NE','OA','OB'],
      ['NF','NG','NH','NJ','NK','OF','OG'],
      ['NL','NM','NN','NO','NP','OL','OM'],
      ['NQ','NR','NS','NT','NU','OQ','OR'],
      ['NV','NW','NX','NY','NZ','OV','OW'],
      ['SA','SB','SC','SD','SE','TA','TB'],
      ['SF','SG','SH','SJ','SK','TF','TG'],
      ['SL','SM','SN','SO','SP','TL','TM'],
      ['SQ','SR','SS','ST','SU','TQ','TR'],
      ['SV','SW','SX','SY','SZ','TV','TW']]
# Reshuffle so indices correspond to offsets
_regions=np.array( [ _regions[x] for x in range(12,-1,-1) ] )
_regions=_regions.transpose()
 
#-------------------------------------------------------------------------------
def to_osgb36(coords):
    """Reformat British National Grid references to OSGB36 numeric coordinates.
    Grid references can be 4, 6, 8 or 10 figures.  Returns a tuple of x, y.
 
    Examples:
 
    Single value
    >>> to_osgb36('NT2755072950')
    (327550, 672950)
 
    For multiple values, use the zip function
    >>> gridrefs = ['HU431392', 'SJ637560', 'TV374354']
    >>> xy=to_osgb36(gridrefs)
    >>> x, y = zip(*xy)
    >>> x
    (443100, 363700, 537400)
    >>> y
    (1139200, 356000, 35400)
    """
    #
    # Check for individual coord, or list, tuple or array of coords
    #
    if type(coords)==list:
        return [to_osgb36(c) for c in coords]
    elif type(coords)==tuple:
        return tuple([to_osgb36(c) for c in coords])
    elif type(coords)==type(np.array('string')):
        return np.array([ to_osgb36(str(c))  for c in list(coords) ])
    #
    # Input is grid reference...
    #
    elif type(coords)==str and re.match(r'^[A-Za-z]{2}(\d{6}|\d{8}|\d{10})$', coords):
        region=coords[0:2].upper()
        x_box, y_box = np.where(_regions==region)
        try: # Catch bad region codes
            x_offset = 100000 * x_box[0] # Convert index in 'regions' to offset
            y_offset = 100000 * y_box[0]
        except IndexError:
            raise ValueError('Invalid 100km grid square code')
        nDigits = (len(coords)-2)/2
        factor = 10**(5-nDigits)
        x,y = (int(coords[2:2+nDigits])*factor + x_offset,
               int(coords[2+nDigits:2+2*nDigits])*factor + y_offset)

        #print int(coords[2:2+nDigits])*factor + x_offset
        #print int(coords[2+nDigits:2+2*nDigits])*factor + y_offset


        return x, y
    #
    # Catch invalid input
    #
    else:
        raise TypeError('Valid inputs are 6,8 or 10-fig references as strings')
 
######################################################################
#
# Next section borrowed from 
#
# http://hannahfry.co.uk/2012/02/01/converting-british-national-grid-to-latitude-and-longitude-ii/
#
#
######################################################################

from math import sqrt, pi, sin, cos, tan, atan2 as arctan2

def OSGB36toWGS84(E,N):

    #E, N are the British national grid coordinates - eastings and northings
    a, b = 6377563.396, 6356256.909     #The Airy 180 semi-major and semi-minor axes used for OSGB36 (m)
    F0 = 0.9996012717                   #scale factor on the central meridian
    lat0 = 49*pi/180                    #Latitude of true origin (radians)
    lon0 = -2*pi/180                    #Longtitude of true origin and central meridian (radians)
    N0, E0 = -100000, 400000            #Northing & easting of true origin (m)
    e2 = 1 - (b*b)/(a*a)                #eccentricity squared
    n = (a-b)/(a+b)

    #Initialise the iterative variables
    lat,M = lat0, 0

    while N-N0-M >= 0.00001: #Accurate to 0.01mm
        lat = (N-N0-M)/(a*F0) + lat;
        M1 = (1 + n + (5/4)*n**2 + (5/4)*n**3) * (lat-lat0)
        M2 = (3*n + 3*n**2 + (21/8)*n**3) * sin(lat-lat0) * cos(lat+lat0)
        M3 = ((15/8)*n**2 + (15/8)*n**3) * sin(2*(lat-lat0)) * cos(2*(lat+lat0))
        M4 = (35/24)*n**3 * sin(3*(lat-lat0)) * cos(3*(lat+lat0))
        #meridional arc
        M = b * F0 * (M1 - M2 + M3 - M4)          

    #transverse radius of curvature
    nu = a*F0/sqrt(1-e2*sin(lat)**2)

    #meridional radius of curvature
    rho = a*F0*(1-e2)*(1-e2*sin(lat)**2)**(-1.5)
    eta2 = nu/rho-1

    secLat = 1./cos(lat)
    VII = tan(lat)/(2*rho*nu)
    VIII = tan(lat)/(24*rho*nu**3)*(5+3*tan(lat)**2+eta2-9*tan(lat)**2*eta2)
    IX = tan(lat)/(720*rho*nu**5)*(61+90*tan(lat)**2+45*tan(lat)**4)
    X = secLat/nu
    XI = secLat/(6*nu**3)*(nu/rho+2*tan(lat)**2)
    XII = secLat/(120*nu**5)*(5+28*tan(lat)**2+24*tan(lat)**4)
    XIIA = secLat/(5040*nu**7)*(61+662*tan(lat)**2+1320*tan(lat)**4+720*tan(lat)**6)
    dE = E-E0

    #These are on the wrong ellipsoid currently: Airy1830. (Denoted by _1)
    lat_1 = lat - VII*dE**2 + VIII*dE**4 - IX*dE**6
    lon_1 = lon0 + X*dE - XI*dE**3 + XII*dE**5 - XIIA*dE**7

    #Want to convert to the GRS80 ellipsoid.
    #First convert to cartesian from spherical polar coordinates
    H = 0 #Third spherical coord.
    x_1 = (nu/F0 + H)*cos(lat_1)*cos(lon_1)
    y_1 = (nu/F0+ H)*cos(lat_1)*sin(lon_1)
    z_1 = ((1-e2)*nu/F0 +H)*sin(lat_1)

    #Perform Helmut transform (to go between Airy 1830 (_1) and GRS80 (_2))
    s = -20.4894*10**-6 #The scale factor -1
    tx, ty, tz = 446.448, -125.157, + 542.060 #The translations along x,y,z axes respectively
    rxs,rys,rzs = 0.1502,  0.2470,  0.8421  #The rotations along x,y,z respectively, in seconds
    rx, ry, rz = rxs*pi/(180*3600.), rys*pi/(180*3600.), rzs*pi/(180*3600.) #In radians
    x_2 = tx + (1+s)*x_1 + (-rz)*y_1 + (ry)*z_1
    y_2 = ty + (rz)*x_1  + (1+s)*y_1 + (-rx)*z_1
    z_2 = tz + (-ry)*x_1 + (rx)*y_1 +  (1+s)*z_1

    #Back to spherical polar coordinates from cartesian
    #Need some of the characteristics of the new ellipsoid    
    a_2, b_2 =6378137.000, 6356752.3141 #The GSR80 semi-major and semi-minor axes used for WGS84(m)
    e2_2 = 1- (b_2*b_2)/(a_2*a_2)   #The eccentricity of the GRS80 ellipsoid
    p = sqrt(x_2**2 + y_2**2)

    #Lat is obtained by an iterative proceedure:   
    lat = arctan2(z_2,(p*(1-e2_2))) #Initial value
    latold = 2*pi
    while abs(lat - latold)>10**-16:
        lat, latold = latold, lat
        nu_2 = a_2/sqrt(1-e2_2*sin(latold)**2)
        lat = arctan2(z_2+e2_2*nu_2*sin(latold), p)

    #Lon and height are then pretty easy
    lon = arctan2(y_2,x_2)
    H = p/cos(lat) - nu_2

    #Uncomment this line if you want to print the results
    #print [(lat-lat_1)*180/pi, (lon - lon_1)*180/pi]

    #Convert to degrees
    lat = lat*180/pi
    lon = lon*180/pi

    #Job's a good'n.
    return lat, lon


############################################################
# 
# Code below written by Ian Watt and Paul Niven
#  at Aberdeen Culture Hack (#ach13 on Tiwtter)
# 29-30 June 2013
#
#
#############################################################
start_next = 0

#initialise global variables
rec_title = ""
Current_status = ""
Author=""
SMR_Number = ""
Site_Type = ""
Period = ""
Parish= ""
Map_Ref = ""
RCAHMS = ""
Biblio_Ref = ""
image_link = ""
image_dec = ""
rec_body = ""
East_North = ""
Lat_Lon = ""
ID = 0
Alt_Site = ""

def scrape_sub(url_in):
    
    global  start_next, image_link, image_desc, rec_body, rec_title, Current_status, Author,SMR_Number, Site_Type, Period, Parish, Map_Ref, RCAHMS, Biblio_Ref, East_North, Lat_Lon, ID, Alt_Site
    print url_in
    sub_html = scraperwiki.scrape(url_in)
    sub_html = sub_html.replace("<br />", "\n")
    sub_root = lxml.html.fromstring(sub_html)

    ID = re.findall(r'\d+', url_in)[0]

    #for el in root.cssselect("div#content-app-body"):
    #    print el
    #root = lxml.html.fromstring(html) # turn our HTML into an lxml object
    #tds = root.cssselect('td') # get all the <td> tags
    #for td in tds:
    #    print lxml.html.tostring(td) # the full HTML tag
    #    print td.text                # just the text inside the HTML tag

    # Get the main HTML
    main_body = sub_root.cssselect("div.grid_6#main-content")[0]
    
    # Get the TITLE
    rec_title = str(main_body.cssselect("h2")[0].text)

    # Check to see if there is an IMAGE
    image_found = False
    image =  main_body.cssselect("img")
    if len(image)>0:
        # There is an IMAGE
        image_found = True
        # Grab the IMAGE URL
        image_link = "http://www.aberdeencity.gov.uk" + image[0].attrib['src']
        # Grab the IMAGE_DESC
        image_desc = main_body.cssselect("img")[0].attrib['alt']
        # Set the paragraph seacrh to start at 1
        para_start = 1+1
    else:
        # Set the paragraph search to start at 2
        para_start = 2+1

    paras = main_body.cssselect("p")     

    if image_found == True:
        range_start = 1
    else:
        range_start = 0

    range_end = len(paras)

    for i in range(range_start, range_end):

        spans = paras[i].cssselect("span")

        if len(spans) == 0:
            #print "Found BODY: " + paras[i].text
            rec_body = paras[i].text
        else:
            #print "Found SPAN for: " + spans[0].text
            #print spans[0].text + spans[1].text

            header = spans[0].text
            #print "Checking HEADER: '" + header + "'"

            if header == "Current Status: ":
                Current_status = spans[1].text
            elif header == "Author and Date: ":
                Author = spans[1].text
            elif header == "SMR Number: ":
                SMR_Number = spans[1].text
            elif header == "Site Type(s): ":
                Site_Type = spans[1].text
            elif header == "Period(s): ":
                Period = spans[1].text
            elif header == "Parish: ":
                Parish = spans[1].text
            elif header == "Map Reference: ":
                 Map_Ref= spans[1].text
            elif header == "RCAHMS Number(s): ":
                 RCAHMS = spans[1].text
            elif header == "Bibliographical Reference: ":
                 Biblio_Ref = spans[1].text
            elif header == "Alternative Site name(s): ":
                 Alt_Site = spans[1].text
            else:
                print "** ERROR: Unknown header - '" + spans[0].text + "'"

    # Convert Co-Ords
    if Map_Ref <> "":
        East_North = to_osgb36(Map_Ref)
        Lat_Lon = OSGB36toWGS84(East_North[0], East_North[1])


    # Print out this records details
    print "ID: " + ID
    print "TITLE: " + rec_title
    #print "CURRENT STATUS: " + Current_status
    #print "AUTHOR: " + Author
    #print "SMR NUMBER: " + SMR_Number
    #print "SITE TYPE: " + Site_Type
    #print "PERIOD: " + Period
    #print "PARISH: " + Parish
    #print "MAP REF: " + Map_Ref
    #print "RCAHMS: " + RCAHMS
    #print "BIBLIO REF: " + Biblio_Ref
    print "IMAGE LINK: " + image_link
    #print "IMAGE DESC: " + image_desc
    #print "REC BODY: " + rec_body
    #print "EAST NORTH: " + str(East_North[0]) + "," + str(East_North[1])
    #print "LAT LON: " + str(Lat_Lon[0]) + "," + str(Lat_Lon[1])
    #print "ALT SITE: " + Alt_Site

    if rec_title != "None":
        print "Saving Record ID: " + ID + "  TITLE: " + rec_title

        scraperwiki.sqlite.save(unique_keys=["ID"], data={"ID":ID, "Title":rec_title, "Status":Current_status, "Author":Author, "SMR_Number":SMR_Number, "Site_Type": Site_Type, "Period": Period, "Parish":Parish, "Map_Ref":Map_Ref, "RCAHMS":RCAHMS, "Biblio_Ref":Biblio_Ref, "Image_Link":image_link, "Image_Desc":image_desc, "Record_Body": rec_body, "Alt_Site": Alt_Site, "Latitude":str(Lat_Lon[0]), "Longitude": str(Lat_Lon[1]), "Easting": str(East_North[0]), "Northing": str(East_North[1]) })
    else:
        print "Skipping Record ID: " + ID


# the following lines were used to fake some records for #ach13 
#
#
#list_ids = (1838, 1744, 2329, 1856, 1634, 1645, 1650, 1658, 1750, 1751, 1840, 2498)
#
#for i in list_ids:    
#   print i
#    scrape_sub("http://www.aberdeencity.gov.uk/xsm_SmrDetail.asp?id=" + str(i))
#####################################################################################    


for el in root.cssselect("div#content-app#-body a"):
    print el
    scrape_sub("http://www.aberdeencity.gov.uk/" + el.attrib['href'])

# test single page scrapes
#
#scrape_sub("http://www.aberdeencity.gov.uk/xsm_SmrDetail.asp?id=2385")
#scrape_sub("http://www.aberdeencity.gov.uk/xsm_SmrDetail.asp?id=2518")




import scraperwiki
import re
import lxml.html


############################################################################
#
# This next section was taken from the site listed here
#
#  COPYRIGHT:  (C) 2012 John A Stevenson / @volcan01010
#           Magnus Hagdorn
#  WEBSITE: http://all-geo.org/volcan01010
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  http://www.gnu.org/licenses/gpl-3.0.html
#
#############################################################################/
 
__all__ = ['to_osgb36', 'from_osgb36']
 
try:
    import numpy as np
except ImportError:
    print "Numpy not installed.  Numpy comes with most scientific python packages."
 
import re
 
# Region codes for 100 km grid squares.
_regions=[['HL','HM','HN','HO','HP','JL','JM'],
      ['HQ','HR','HS','HT','HU','JQ','JR'],
      ['HV','HW','HX','HY','HZ','JV','JW'],
      ['NA','NB','NC','ND','NE','OA','OB'],
      ['NF','NG','NH','NJ','NK','OF','OG'],
      ['NL','NM','NN','NO','NP','OL','OM'],
      ['NQ','NR','NS','NT','NU','OQ','OR'],
      ['NV','NW','NX','NY','NZ','OV','OW'],
      ['SA','SB','SC','SD','SE','TA','TB'],
      ['SF','SG','SH','SJ','SK','TF','TG'],
      ['SL','SM','SN','SO','SP','TL','TM'],
      ['SQ','SR','SS','ST','SU','TQ','TR'],
      ['SV','SW','SX','SY','SZ','TV','TW']]
# Reshuffle so indices correspond to offsets
_regions=np.array( [ _regions[x] for x in range(12,-1,-1) ] )
_regions=_regions.transpose()
 
#-------------------------------------------------------------------------------
def to_osgb36(coords):
    """Reformat British National Grid references to OSGB36 numeric coordinates.
    Grid references can be 4, 6, 8 or 10 figures.  Returns a tuple of x, y.
 
    Examples:
 
    Single value
    >>> to_osgb36('NT2755072950')
    (327550, 672950)
 
    For multiple values, use the zip function
    >>> gridrefs = ['HU431392', 'SJ637560', 'TV374354']
    >>> xy=to_osgb36(gridrefs)
    >>> x, y = zip(*xy)
    >>> x
    (443100, 363700, 537400)
    >>> y
    (1139200, 356000, 35400)
    """
    #
    # Check for individual coord, or list, tuple or array of coords
    #
    if type(coords)==list:
        return [to_osgb36(c) for c in coords]
    elif type(coords)==tuple:
        return tuple([to_osgb36(c) for c in coords])
    elif type(coords)==type(np.array('string')):
        return np.array([ to_osgb36(str(c))  for c in list(coords) ])
    #
    # Input is grid reference...
    #
    elif type(coords)==str and re.match(r'^[A-Za-z]{2}(\d{6}|\d{8}|\d{10})$', coords):
        region=coords[0:2].upper()
        x_box, y_box = np.where(_regions==region)
        try: # Catch bad region codes
            x_offset = 100000 * x_box[0] # Convert index in 'regions' to offset
            y_offset = 100000 * y_box[0]
        except IndexError:
            raise ValueError('Invalid 100km grid square code')
        nDigits = (len(coords)-2)/2
        factor = 10**(5-nDigits)
        x,y = (int(coords[2:2+nDigits])*factor + x_offset,
               int(coords[2+nDigits:2+2*nDigits])*factor + y_offset)

        #print int(coords[2:2+nDigits])*factor + x_offset
        #print int(coords[2+nDigits:2+2*nDigits])*factor + y_offset


        return x, y
    #
    # Catch invalid input
    #
    else:
        raise TypeError('Valid inputs are 6,8 or 10-fig references as strings')
 
######################################################################
#
# Next section borrowed from 
#
# http://hannahfry.co.uk/2012/02/01/converting-british-national-grid-to-latitude-and-longitude-ii/
#
#
######################################################################

from math import sqrt, pi, sin, cos, tan, atan2 as arctan2

def OSGB36toWGS84(E,N):

    #E, N are the British national grid coordinates - eastings and northings
    a, b = 6377563.396, 6356256.909     #The Airy 180 semi-major and semi-minor axes used for OSGB36 (m)
    F0 = 0.9996012717                   #scale factor on the central meridian
    lat0 = 49*pi/180                    #Latitude of true origin (radians)
    lon0 = -2*pi/180                    #Longtitude of true origin and central meridian (radians)
    N0, E0 = -100000, 400000            #Northing & easting of true origin (m)
    e2 = 1 - (b*b)/(a*a)                #eccentricity squared
    n = (a-b)/(a+b)

    #Initialise the iterative variables
    lat,M = lat0, 0

    while N-N0-M >= 0.00001: #Accurate to 0.01mm
        lat = (N-N0-M)/(a*F0) + lat;
        M1 = (1 + n + (5/4)*n**2 + (5/4)*n**3) * (lat-lat0)
        M2 = (3*n + 3*n**2 + (21/8)*n**3) * sin(lat-lat0) * cos(lat+lat0)
        M3 = ((15/8)*n**2 + (15/8)*n**3) * sin(2*(lat-lat0)) * cos(2*(lat+lat0))
        M4 = (35/24)*n**3 * sin(3*(lat-lat0)) * cos(3*(lat+lat0))
        #meridional arc
        M = b * F0 * (M1 - M2 + M3 - M4)          

    #transverse radius of curvature
    nu = a*F0/sqrt(1-e2*sin(lat)**2)

    #meridional radius of curvature
    rho = a*F0*(1-e2)*(1-e2*sin(lat)**2)**(-1.5)
    eta2 = nu/rho-1

    secLat = 1./cos(lat)
    VII = tan(lat)/(2*rho*nu)
    VIII = tan(lat)/(24*rho*nu**3)*(5+3*tan(lat)**2+eta2-9*tan(lat)**2*eta2)
    IX = tan(lat)/(720*rho*nu**5)*(61+90*tan(lat)**2+45*tan(lat)**4)
    X = secLat/nu
    XI = secLat/(6*nu**3)*(nu/rho+2*tan(lat)**2)
    XII = secLat/(120*nu**5)*(5+28*tan(lat)**2+24*tan(lat)**4)
    XIIA = secLat/(5040*nu**7)*(61+662*tan(lat)**2+1320*tan(lat)**4+720*tan(lat)**6)
    dE = E-E0

    #These are on the wrong ellipsoid currently: Airy1830. (Denoted by _1)
    lat_1 = lat - VII*dE**2 + VIII*dE**4 - IX*dE**6
    lon_1 = lon0 + X*dE - XI*dE**3 + XII*dE**5 - XIIA*dE**7

    #Want to convert to the GRS80 ellipsoid.
    #First convert to cartesian from spherical polar coordinates
    H = 0 #Third spherical coord.
    x_1 = (nu/F0 + H)*cos(lat_1)*cos(lon_1)
    y_1 = (nu/F0+ H)*cos(lat_1)*sin(lon_1)
    z_1 = ((1-e2)*nu/F0 +H)*sin(lat_1)

    #Perform Helmut transform (to go between Airy 1830 (_1) and GRS80 (_2))
    s = -20.4894*10**-6 #The scale factor -1
    tx, ty, tz = 446.448, -125.157, + 542.060 #The translations along x,y,z axes respectively
    rxs,rys,rzs = 0.1502,  0.2470,  0.8421  #The rotations along x,y,z respectively, in seconds
    rx, ry, rz = rxs*pi/(180*3600.), rys*pi/(180*3600.), rzs*pi/(180*3600.) #In radians
    x_2 = tx + (1+s)*x_1 + (-rz)*y_1 + (ry)*z_1
    y_2 = ty + (rz)*x_1  + (1+s)*y_1 + (-rx)*z_1
    z_2 = tz + (-ry)*x_1 + (rx)*y_1 +  (1+s)*z_1

    #Back to spherical polar coordinates from cartesian
    #Need some of the characteristics of the new ellipsoid    
    a_2, b_2 =6378137.000, 6356752.3141 #The GSR80 semi-major and semi-minor axes used for WGS84(m)
    e2_2 = 1- (b_2*b_2)/(a_2*a_2)   #The eccentricity of the GRS80 ellipsoid
    p = sqrt(x_2**2 + y_2**2)

    #Lat is obtained by an iterative proceedure:   
    lat = arctan2(z_2,(p*(1-e2_2))) #Initial value
    latold = 2*pi
    while abs(lat - latold)>10**-16:
        lat, latold = latold, lat
        nu_2 = a_2/sqrt(1-e2_2*sin(latold)**2)
        lat = arctan2(z_2+e2_2*nu_2*sin(latold), p)

    #Lon and height are then pretty easy
    lon = arctan2(y_2,x_2)
    H = p/cos(lat) - nu_2

    #Uncomment this line if you want to print the results
    #print [(lat-lat_1)*180/pi, (lon - lon_1)*180/pi]

    #Convert to degrees
    lat = lat*180/pi
    lon = lon*180/pi

    #Job's a good'n.
    return lat, lon


############################################################
# 
# Code below written by Ian Watt and Paul Niven
#  at Aberdeen Culture Hack (#ach13 on Tiwtter)
# 29-30 June 2013
#
#
#############################################################
start_next = 0

#initialise global variables
rec_title = ""
Current_status = ""
Author=""
SMR_Number = ""
Site_Type = ""
Period = ""
Parish= ""
Map_Ref = ""
RCAHMS = ""
Biblio_Ref = ""
image_link = ""
image_dec = ""
rec_body = ""
East_North = ""
Lat_Lon = ""
ID = 0
Alt_Site = ""

def scrape_sub(url_in):
    
    global  start_next, image_link, image_desc, rec_body, rec_title, Current_status, Author,SMR_Number, Site_Type, Period, Parish, Map_Ref, RCAHMS, Biblio_Ref, East_North, Lat_Lon, ID, Alt_Site
    print url_in
    sub_html = scraperwiki.scrape(url_in)
    sub_html = sub_html.replace("<br />", "\n")
    sub_root = lxml.html.fromstring(sub_html)

    ID = re.findall(r'\d+', url_in)[0]

    #for el in root.cssselect("div#content-app-body"):
    #    print el
    #root = lxml.html.fromstring(html) # turn our HTML into an lxml object
    #tds = root.cssselect('td') # get all the <td> tags
    #for td in tds:
    #    print lxml.html.tostring(td) # the full HTML tag
    #    print td.text                # just the text inside the HTML tag

    # Get the main HTML
    main_body = sub_root.cssselect("div.grid_6#main-content")[0]
    
    # Get the TITLE
    rec_title = str(main_body.cssselect("h2")[0].text)

    # Check to see if there is an IMAGE
    image_found = False
    image =  main_body.cssselect("img")
    if len(image)>0:
        # There is an IMAGE
        image_found = True
        # Grab the IMAGE URL
        image_link = "http://www.aberdeencity.gov.uk" + image[0].attrib['src']
        # Grab the IMAGE_DESC
        image_desc = main_body.cssselect("img")[0].attrib['alt']
        # Set the paragraph seacrh to start at 1
        para_start = 1+1
    else:
        # Set the paragraph search to start at 2
        para_start = 2+1

    paras = main_body.cssselect("p")     

    if image_found == True:
        range_start = 1
    else:
        range_start = 0

    range_end = len(paras)

    for i in range(range_start, range_end):

        spans = paras[i].cssselect("span")

        if len(spans) == 0:
            #print "Found BODY: " + paras[i].text
            rec_body = paras[i].text
        else:
            #print "Found SPAN for: " + spans[0].text
            #print spans[0].text + spans[1].text

            header = spans[0].text
            #print "Checking HEADER: '" + header + "'"

            if header == "Current Status: ":
                Current_status = spans[1].text
            elif header == "Author and Date: ":
                Author = spans[1].text
            elif header == "SMR Number: ":
                SMR_Number = spans[1].text
            elif header == "Site Type(s): ":
                Site_Type = spans[1].text
            elif header == "Period(s): ":
                Period = spans[1].text
            elif header == "Parish: ":
                Parish = spans[1].text
            elif header == "Map Reference: ":
                 Map_Ref= spans[1].text
            elif header == "RCAHMS Number(s): ":
                 RCAHMS = spans[1].text
            elif header == "Bibliographical Reference: ":
                 Biblio_Ref = spans[1].text
            elif header == "Alternative Site name(s): ":
                 Alt_Site = spans[1].text
            else:
                print "** ERROR: Unknown header - '" + spans[0].text + "'"

    # Convert Co-Ords
    if Map_Ref <> "":
        East_North = to_osgb36(Map_Ref)
        Lat_Lon = OSGB36toWGS84(East_North[0], East_North[1])


    # Print out this records details
    print "ID: " + ID
    print "TITLE: " + rec_title
    #print "CURRENT STATUS: " + Current_status
    #print "AUTHOR: " + Author
    #print "SMR NUMBER: " + SMR_Number
    #print "SITE TYPE: " + Site_Type
    #print "PERIOD: " + Period
    #print "PARISH: " + Parish
    #print "MAP REF: " + Map_Ref
    #print "RCAHMS: " + RCAHMS
    #print "BIBLIO REF: " + Biblio_Ref
    print "IMAGE LINK: " + image_link
    #print "IMAGE DESC: " + image_desc
    #print "REC BODY: " + rec_body
    #print "EAST NORTH: " + str(East_North[0]) + "," + str(East_North[1])
    #print "LAT LON: " + str(Lat_Lon[0]) + "," + str(Lat_Lon[1])
    #print "ALT SITE: " + Alt_Site

    if rec_title != "None":
        print "Saving Record ID: " + ID + "  TITLE: " + rec_title

        scraperwiki.sqlite.save(unique_keys=["ID"], data={"ID":ID, "Title":rec_title, "Status":Current_status, "Author":Author, "SMR_Number":SMR_Number, "Site_Type": Site_Type, "Period": Period, "Parish":Parish, "Map_Ref":Map_Ref, "RCAHMS":RCAHMS, "Biblio_Ref":Biblio_Ref, "Image_Link":image_link, "Image_Desc":image_desc, "Record_Body": rec_body, "Alt_Site": Alt_Site, "Latitude":str(Lat_Lon[0]), "Longitude": str(Lat_Lon[1]), "Easting": str(East_North[0]), "Northing": str(East_North[1]) })
    else:
        print "Skipping Record ID: " + ID


# the following lines were used to fake some records for #ach13 
#
#
#list_ids = (1838, 1744, 2329, 1856, 1634, 1645, 1650, 1658, 1750, 1751, 1840, 2498)
#
#for i in list_ids:    
#   print i
#    scrape_sub("http://www.aberdeencity.gov.uk/xsm_SmrDetail.asp?id=" + str(i))
#####################################################################################    


for el in root.cssselect("div#content-app#-body a"):
    print el
    scrape_sub("http://www.aberdeencity.gov.uk/" + el.attrib['href'])

# test single page scrapes
#
#scrape_sub("http://www.aberdeencity.gov.uk/xsm_SmrDetail.asp?id=2385")
#scrape_sub("http://www.aberdeencity.gov.uk/xsm_SmrDetail.asp?id=2518")




import scraperwiki
import re
import lxml.html


############################################################################
#
# This next section was taken from the site listed here
#
#  COPYRIGHT:  (C) 2012 John A Stevenson / @volcan01010
#           Magnus Hagdorn
#  WEBSITE: http://all-geo.org/volcan01010
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  http://www.gnu.org/licenses/gpl-3.0.html
#
#############################################################################/
 
__all__ = ['to_osgb36', 'from_osgb36']
 
try:
    import numpy as np
except ImportError:
    print "Numpy not installed.  Numpy comes with most scientific python packages."
 
import re
 
# Region codes for 100 km grid squares.
_regions=[['HL','HM','HN','HO','HP','JL','JM'],
      ['HQ','HR','HS','HT','HU','JQ','JR'],
      ['HV','HW','HX','HY','HZ','JV','JW'],
      ['NA','NB','NC','ND','NE','OA','OB'],
      ['NF','NG','NH','NJ','NK','OF','OG'],
      ['NL','NM','NN','NO','NP','OL','OM'],
      ['NQ','NR','NS','NT','NU','OQ','OR'],
      ['NV','NW','NX','NY','NZ','OV','OW'],
      ['SA','SB','SC','SD','SE','TA','TB'],
      ['SF','SG','SH','SJ','SK','TF','TG'],
      ['SL','SM','SN','SO','SP','TL','TM'],
      ['SQ','SR','SS','ST','SU','TQ','TR'],
      ['SV','SW','SX','SY','SZ','TV','TW']]
# Reshuffle so indices correspond to offsets
_regions=np.array( [ _regions[x] for x in range(12,-1,-1) ] )
_regions=_regions.transpose()
 
#-------------------------------------------------------------------------------
def to_osgb36(coords):
    """Reformat British National Grid references to OSGB36 numeric coordinates.
    Grid references can be 4, 6, 8 or 10 figures.  Returns a tuple of x, y.
 
    Examples:
 
    Single value
    >>> to_osgb36('NT2755072950')
    (327550, 672950)
 
    For multiple values, use the zip function
    >>> gridrefs = ['HU431392', 'SJ637560', 'TV374354']
    >>> xy=to_osgb36(gridrefs)
    >>> x, y = zip(*xy)
    >>> x
    (443100, 363700, 537400)
    >>> y
    (1139200, 356000, 35400)
    """
    #
    # Check for individual coord, or list, tuple or array of coords
    #
    if type(coords)==list:
        return [to_osgb36(c) for c in coords]
    elif type(coords)==tuple:
        return tuple([to_osgb36(c) for c in coords])
    elif type(coords)==type(np.array('string')):
        return np.array([ to_osgb36(str(c))  for c in list(coords) ])
    #
    # Input is grid reference...
    #
    elif type(coords)==str and re.match(r'^[A-Za-z]{2}(\d{6}|\d{8}|\d{10})$', coords):
        region=coords[0:2].upper()
        x_box, y_box = np.where(_regions==region)
        try: # Catch bad region codes
            x_offset = 100000 * x_box[0] # Convert index in 'regions' to offset
            y_offset = 100000 * y_box[0]
        except IndexError:
            raise ValueError('Invalid 100km grid square code')
        nDigits = (len(coords)-2)/2
        factor = 10**(5-nDigits)
        x,y = (int(coords[2:2+nDigits])*factor + x_offset,
               int(coords[2+nDigits:2+2*nDigits])*factor + y_offset)

        #print int(coords[2:2+nDigits])*factor + x_offset
        #print int(coords[2+nDigits:2+2*nDigits])*factor + y_offset


        return x, y
    #
    # Catch invalid input
    #
    else:
        raise TypeError('Valid inputs are 6,8 or 10-fig references as strings')
 
######################################################################
#
# Next section borrowed from 
#
# http://hannahfry.co.uk/2012/02/01/converting-british-national-grid-to-latitude-and-longitude-ii/
#
#
######################################################################

from math import sqrt, pi, sin, cos, tan, atan2 as arctan2

def OSGB36toWGS84(E,N):

    #E, N are the British national grid coordinates - eastings and northings
    a, b = 6377563.396, 6356256.909     #The Airy 180 semi-major and semi-minor axes used for OSGB36 (m)
    F0 = 0.9996012717                   #scale factor on the central meridian
    lat0 = 49*pi/180                    #Latitude of true origin (radians)
    lon0 = -2*pi/180                    #Longtitude of true origin and central meridian (radians)
    N0, E0 = -100000, 400000            #Northing & easting of true origin (m)
    e2 = 1 - (b*b)/(a*a)                #eccentricity squared
    n = (a-b)/(a+b)

    #Initialise the iterative variables
    lat,M = lat0, 0

    while N-N0-M >= 0.00001: #Accurate to 0.01mm
        lat = (N-N0-M)/(a*F0) + lat;
        M1 = (1 + n + (5/4)*n**2 + (5/4)*n**3) * (lat-lat0)
        M2 = (3*n + 3*n**2 + (21/8)*n**3) * sin(lat-lat0) * cos(lat+lat0)
        M3 = ((15/8)*n**2 + (15/8)*n**3) * sin(2*(lat-lat0)) * cos(2*(lat+lat0))
        M4 = (35/24)*n**3 * sin(3*(lat-lat0)) * cos(3*(lat+lat0))
        #meridional arc
        M = b * F0 * (M1 - M2 + M3 - M4)          

    #transverse radius of curvature
    nu = a*F0/sqrt(1-e2*sin(lat)**2)

    #meridional radius of curvature
    rho = a*F0*(1-e2)*(1-e2*sin(lat)**2)**(-1.5)
    eta2 = nu/rho-1

    secLat = 1./cos(lat)
    VII = tan(lat)/(2*rho*nu)
    VIII = tan(lat)/(24*rho*nu**3)*(5+3*tan(lat)**2+eta2-9*tan(lat)**2*eta2)
    IX = tan(lat)/(720*rho*nu**5)*(61+90*tan(lat)**2+45*tan(lat)**4)
    X = secLat/nu
    XI = secLat/(6*nu**3)*(nu/rho+2*tan(lat)**2)
    XII = secLat/(120*nu**5)*(5+28*tan(lat)**2+24*tan(lat)**4)
    XIIA = secLat/(5040*nu**7)*(61+662*tan(lat)**2+1320*tan(lat)**4+720*tan(lat)**6)
    dE = E-E0

    #These are on the wrong ellipsoid currently: Airy1830. (Denoted by _1)
    lat_1 = lat - VII*dE**2 + VIII*dE**4 - IX*dE**6
    lon_1 = lon0 + X*dE - XI*dE**3 + XII*dE**5 - XIIA*dE**7

    #Want to convert to the GRS80 ellipsoid.
    #First convert to cartesian from spherical polar coordinates
    H = 0 #Third spherical coord.
    x_1 = (nu/F0 + H)*cos(lat_1)*cos(lon_1)
    y_1 = (nu/F0+ H)*cos(lat_1)*sin(lon_1)
    z_1 = ((1-e2)*nu/F0 +H)*sin(lat_1)

    #Perform Helmut transform (to go between Airy 1830 (_1) and GRS80 (_2))
    s = -20.4894*10**-6 #The scale factor -1
    tx, ty, tz = 446.448, -125.157, + 542.060 #The translations along x,y,z axes respectively
    rxs,rys,rzs = 0.1502,  0.2470,  0.8421  #The rotations along x,y,z respectively, in seconds
    rx, ry, rz = rxs*pi/(180*3600.), rys*pi/(180*3600.), rzs*pi/(180*3600.) #In radians
    x_2 = tx + (1+s)*x_1 + (-rz)*y_1 + (ry)*z_1
    y_2 = ty + (rz)*x_1  + (1+s)*y_1 + (-rx)*z_1
    z_2 = tz + (-ry)*x_1 + (rx)*y_1 +  (1+s)*z_1

    #Back to spherical polar coordinates from cartesian
    #Need some of the characteristics of the new ellipsoid    
    a_2, b_2 =6378137.000, 6356752.3141 #The GSR80 semi-major and semi-minor axes used for WGS84(m)
    e2_2 = 1- (b_2*b_2)/(a_2*a_2)   #The eccentricity of the GRS80 ellipsoid
    p = sqrt(x_2**2 + y_2**2)

    #Lat is obtained by an iterative proceedure:   
    lat = arctan2(z_2,(p*(1-e2_2))) #Initial value
    latold = 2*pi
    while abs(lat - latold)>10**-16:
        lat, latold = latold, lat
        nu_2 = a_2/sqrt(1-e2_2*sin(latold)**2)
        lat = arctan2(z_2+e2_2*nu_2*sin(latold), p)

    #Lon and height are then pretty easy
    lon = arctan2(y_2,x_2)
    H = p/cos(lat) - nu_2

    #Uncomment this line if you want to print the results
    #print [(lat-lat_1)*180/pi, (lon - lon_1)*180/pi]

    #Convert to degrees
    lat = lat*180/pi
    lon = lon*180/pi

    #Job's a good'n.
    return lat, lon


############################################################
# 
# Code below written by Ian Watt and Paul Niven
#  at Aberdeen Culture Hack (#ach13 on Tiwtter)
# 29-30 June 2013
#
#
#############################################################
start_next = 0

#initialise global variables
rec_title = ""
Current_status = ""
Author=""
SMR_Number = ""
Site_Type = ""
Period = ""
Parish= ""
Map_Ref = ""
RCAHMS = ""
Biblio_Ref = ""
image_link = ""
image_dec = ""
rec_body = ""
East_North = ""
Lat_Lon = ""
ID = 0
Alt_Site = ""

def scrape_sub(url_in):
    
    global  start_next, image_link, image_desc, rec_body, rec_title, Current_status, Author,SMR_Number, Site_Type, Period, Parish, Map_Ref, RCAHMS, Biblio_Ref, East_North, Lat_Lon, ID, Alt_Site
    print url_in
    sub_html = scraperwiki.scrape(url_in)
    sub_html = sub_html.replace("<br />", "\n")
    sub_root = lxml.html.fromstring(sub_html)

    ID = re.findall(r'\d+', url_in)[0]

    #for el in root.cssselect("div#content-app-body"):
    #    print el
    #root = lxml.html.fromstring(html) # turn our HTML into an lxml object
    #tds = root.cssselect('td') # get all the <td> tags
    #for td in tds:
    #    print lxml.html.tostring(td) # the full HTML tag
    #    print td.text                # just the text inside the HTML tag

    # Get the main HTML
    main_body = sub_root.cssselect("div.grid_6#main-content")[0]
    
    # Get the TITLE
    rec_title = str(main_body.cssselect("h2")[0].text)

    # Check to see if there is an IMAGE
    image_found = False
    image =  main_body.cssselect("img")
    if len(image)>0:
        # There is an IMAGE
        image_found = True
        # Grab the IMAGE URL
        image_link = "http://www.aberdeencity.gov.uk" + image[0].attrib['src']
        # Grab the IMAGE_DESC
        image_desc = main_body.cssselect("img")[0].attrib['alt']
        # Set the paragraph seacrh to start at 1
        para_start = 1+1
    else:
        # Set the paragraph search to start at 2
        para_start = 2+1

    paras = main_body.cssselect("p")     

    if image_found == True:
        range_start = 1
    else:
        range_start = 0

    range_end = len(paras)

    for i in range(range_start, range_end):

        spans = paras[i].cssselect("span")

        if len(spans) == 0:
            #print "Found BODY: " + paras[i].text
            rec_body = paras[i].text
        else:
            #print "Found SPAN for: " + spans[0].text
            #print spans[0].text + spans[1].text

            header = spans[0].text
            #print "Checking HEADER: '" + header + "'"

            if header == "Current Status: ":
                Current_status = spans[1].text
            elif header == "Author and Date: ":
                Author = spans[1].text
            elif header == "SMR Number: ":
                SMR_Number = spans[1].text
            elif header == "Site Type(s): ":
                Site_Type = spans[1].text
            elif header == "Period(s): ":
                Period = spans[1].text
            elif header == "Parish: ":
                Parish = spans[1].text
            elif header == "Map Reference: ":
                 Map_Ref= spans[1].text
            elif header == "RCAHMS Number(s): ":
                 RCAHMS = spans[1].text
            elif header == "Bibliographical Reference: ":
                 Biblio_Ref = spans[1].text
            elif header == "Alternative Site name(s): ":
                 Alt_Site = spans[1].text
            else:
                print "** ERROR: Unknown header - '" + spans[0].text + "'"

    # Convert Co-Ords
    if Map_Ref <> "":
        East_North = to_osgb36(Map_Ref)
        Lat_Lon = OSGB36toWGS84(East_North[0], East_North[1])


    # Print out this records details
    print "ID: " + ID
    print "TITLE: " + rec_title
    #print "CURRENT STATUS: " + Current_status
    #print "AUTHOR: " + Author
    #print "SMR NUMBER: " + SMR_Number
    #print "SITE TYPE: " + Site_Type
    #print "PERIOD: " + Period
    #print "PARISH: " + Parish
    #print "MAP REF: " + Map_Ref
    #print "RCAHMS: " + RCAHMS
    #print "BIBLIO REF: " + Biblio_Ref
    print "IMAGE LINK: " + image_link
    #print "IMAGE DESC: " + image_desc
    #print "REC BODY: " + rec_body
    #print "EAST NORTH: " + str(East_North[0]) + "," + str(East_North[1])
    #print "LAT LON: " + str(Lat_Lon[0]) + "," + str(Lat_Lon[1])
    #print "ALT SITE: " + Alt_Site

    if rec_title != "None":
        print "Saving Record ID: " + ID + "  TITLE: " + rec_title

        scraperwiki.sqlite.save(unique_keys=["ID"], data={"ID":ID, "Title":rec_title, "Status":Current_status, "Author":Author, "SMR_Number":SMR_Number, "Site_Type": Site_Type, "Period": Period, "Parish":Parish, "Map_Ref":Map_Ref, "RCAHMS":RCAHMS, "Biblio_Ref":Biblio_Ref, "Image_Link":image_link, "Image_Desc":image_desc, "Record_Body": rec_body, "Alt_Site": Alt_Site, "Latitude":str(Lat_Lon[0]), "Longitude": str(Lat_Lon[1]), "Easting": str(East_North[0]), "Northing": str(East_North[1]) })
    else:
        print "Skipping Record ID: " + ID


# the following lines were used to fake some records for #ach13 
#
#
#list_ids = (1838, 1744, 2329, 1856, 1634, 1645, 1650, 1658, 1750, 1751, 1840, 2498)
#
#for i in list_ids:    
#   print i
#    scrape_sub("http://www.aberdeencity.gov.uk/xsm_SmrDetail.asp?id=" + str(i))
#####################################################################################    


for el in root.cssselect("div#content-app#-body a"):
    print el
    scrape_sub("http://www.aberdeencity.gov.uk/" + el.attrib['href'])

# test single page scrapes
#
#scrape_sub("http://www.aberdeencity.gov.uk/xsm_SmrDetail.asp?id=2385")
#scrape_sub("http://www.aberdeencity.gov.uk/xsm_SmrDetail.asp?id=2518")




import scraperwiki
import re
import lxml.html


############################################################################
#
# This next section was taken from the site listed here
#
#  COPYRIGHT:  (C) 2012 John A Stevenson / @volcan01010
#           Magnus Hagdorn
#  WEBSITE: http://all-geo.org/volcan01010
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  http://www.gnu.org/licenses/gpl-3.0.html
#
#############################################################################/
 
__all__ = ['to_osgb36', 'from_osgb36']
 
try:
    import numpy as np
except ImportError:
    print "Numpy not installed.  Numpy comes with most scientific python packages."
 
import re
 
# Region codes for 100 km grid squares.
_regions=[['HL','HM','HN','HO','HP','JL','JM'],
      ['HQ','HR','HS','HT','HU','JQ','JR'],
      ['HV','HW','HX','HY','HZ','JV','JW'],
      ['NA','NB','NC','ND','NE','OA','OB'],
      ['NF','NG','NH','NJ','NK','OF','OG'],
      ['NL','NM','NN','NO','NP','OL','OM'],
      ['NQ','NR','NS','NT','NU','OQ','OR'],
      ['NV','NW','NX','NY','NZ','OV','OW'],
      ['SA','SB','SC','SD','SE','TA','TB'],
      ['SF','SG','SH','SJ','SK','TF','TG'],
      ['SL','SM','SN','SO','SP','TL','TM'],
      ['SQ','SR','SS','ST','SU','TQ','TR'],
      ['SV','SW','SX','SY','SZ','TV','TW']]
# Reshuffle so indices correspond to offsets
_regions=np.array( [ _regions[x] for x in range(12,-1,-1) ] )
_regions=_regions.transpose()
 
#-------------------------------------------------------------------------------
def to_osgb36(coords):
    """Reformat British National Grid references to OSGB36 numeric coordinates.
    Grid references can be 4, 6, 8 or 10 figures.  Returns a tuple of x, y.
 
    Examples:
 
    Single value
    >>> to_osgb36('NT2755072950')
    (327550, 672950)
 
    For multiple values, use the zip function
    >>> gridrefs = ['HU431392', 'SJ637560', 'TV374354']
    >>> xy=to_osgb36(gridrefs)
    >>> x, y = zip(*xy)
    >>> x
    (443100, 363700, 537400)
    >>> y
    (1139200, 356000, 35400)
    """
    #
    # Check for individual coord, or list, tuple or array of coords
    #
    if type(coords)==list:
        return [to_osgb36(c) for c in coords]
    elif type(coords)==tuple:
        return tuple([to_osgb36(c) for c in coords])
    elif type(coords)==type(np.array('string')):
        return np.array([ to_osgb36(str(c))  for c in list(coords) ])
    #
    # Input is grid reference...
    #
    elif type(coords)==str and re.match(r'^[A-Za-z]{2}(\d{6}|\d{8}|\d{10})$', coords):
        region=coords[0:2].upper()
        x_box, y_box = np.where(_regions==region)
        try: # Catch bad region codes
            x_offset = 100000 * x_box[0] # Convert index in 'regions' to offset
            y_offset = 100000 * y_box[0]
        except IndexError:
            raise ValueError('Invalid 100km grid square code')
        nDigits = (len(coords)-2)/2
        factor = 10**(5-nDigits)
        x,y = (int(coords[2:2+nDigits])*factor + x_offset,
               int(coords[2+nDigits:2+2*nDigits])*factor + y_offset)

        #print int(coords[2:2+nDigits])*factor + x_offset
        #print int(coords[2+nDigits:2+2*nDigits])*factor + y_offset


        return x, y
    #
    # Catch invalid input
    #
    else:
        raise TypeError('Valid inputs are 6,8 or 10-fig references as strings')
 
######################################################################
#
# Next section borrowed from 
#
# http://hannahfry.co.uk/2012/02/01/converting-british-national-grid-to-latitude-and-longitude-ii/
#
#
######################################################################

from math import sqrt, pi, sin, cos, tan, atan2 as arctan2

def OSGB36toWGS84(E,N):

    #E, N are the British national grid coordinates - eastings and northings
    a, b = 6377563.396, 6356256.909     #The Airy 180 semi-major and semi-minor axes used for OSGB36 (m)
    F0 = 0.9996012717                   #scale factor on the central meridian
    lat0 = 49*pi/180                    #Latitude of true origin (radians)
    lon0 = -2*pi/180                    #Longtitude of true origin and central meridian (radians)
    N0, E0 = -100000, 400000            #Northing & easting of true origin (m)
    e2 = 1 - (b*b)/(a*a)                #eccentricity squared
    n = (a-b)/(a+b)

    #Initialise the iterative variables
    lat,M = lat0, 0

    while N-N0-M >= 0.00001: #Accurate to 0.01mm
        lat = (N-N0-M)/(a*F0) + lat;
        M1 = (1 + n + (5/4)*n**2 + (5/4)*n**3) * (lat-lat0)
        M2 = (3*n + 3*n**2 + (21/8)*n**3) * sin(lat-lat0) * cos(lat+lat0)
        M3 = ((15/8)*n**2 + (15/8)*n**3) * sin(2*(lat-lat0)) * cos(2*(lat+lat0))
        M4 = (35/24)*n**3 * sin(3*(lat-lat0)) * cos(3*(lat+lat0))
        #meridional arc
        M = b * F0 * (M1 - M2 + M3 - M4)          

    #transverse radius of curvature
    nu = a*F0/sqrt(1-e2*sin(lat)**2)

    #meridional radius of curvature
    rho = a*F0*(1-e2)*(1-e2*sin(lat)**2)**(-1.5)
    eta2 = nu/rho-1

    secLat = 1./cos(lat)
    VII = tan(lat)/(2*rho*nu)
    VIII = tan(lat)/(24*rho*nu**3)*(5+3*tan(lat)**2+eta2-9*tan(lat)**2*eta2)
    IX = tan(lat)/(720*rho*nu**5)*(61+90*tan(lat)**2+45*tan(lat)**4)
    X = secLat/nu
    XI = secLat/(6*nu**3)*(nu/rho+2*tan(lat)**2)
    XII = secLat/(120*nu**5)*(5+28*tan(lat)**2+24*tan(lat)**4)
    XIIA = secLat/(5040*nu**7)*(61+662*tan(lat)**2+1320*tan(lat)**4+720*tan(lat)**6)
    dE = E-E0

    #These are on the wrong ellipsoid currently: Airy1830. (Denoted by _1)
    lat_1 = lat - VII*dE**2 + VIII*dE**4 - IX*dE**6
    lon_1 = lon0 + X*dE - XI*dE**3 + XII*dE**5 - XIIA*dE**7

    #Want to convert to the GRS80 ellipsoid.
    #First convert to cartesian from spherical polar coordinates
    H = 0 #Third spherical coord.
    x_1 = (nu/F0 + H)*cos(lat_1)*cos(lon_1)
    y_1 = (nu/F0+ H)*cos(lat_1)*sin(lon_1)
    z_1 = ((1-e2)*nu/F0 +H)*sin(lat_1)

    #Perform Helmut transform (to go between Airy 1830 (_1) and GRS80 (_2))
    s = -20.4894*10**-6 #The scale factor -1
    tx, ty, tz = 446.448, -125.157, + 542.060 #The translations along x,y,z axes respectively
    rxs,rys,rzs = 0.1502,  0.2470,  0.8421  #The rotations along x,y,z respectively, in seconds
    rx, ry, rz = rxs*pi/(180*3600.), rys*pi/(180*3600.), rzs*pi/(180*3600.) #In radians
    x_2 = tx + (1+s)*x_1 + (-rz)*y_1 + (ry)*z_1
    y_2 = ty + (rz)*x_1  + (1+s)*y_1 + (-rx)*z_1
    z_2 = tz + (-ry)*x_1 + (rx)*y_1 +  (1+s)*z_1

    #Back to spherical polar coordinates from cartesian
    #Need some of the characteristics of the new ellipsoid    
    a_2, b_2 =6378137.000, 6356752.3141 #The GSR80 semi-major and semi-minor axes used for WGS84(m)
    e2_2 = 1- (b_2*b_2)/(a_2*a_2)   #The eccentricity of the GRS80 ellipsoid
    p = sqrt(x_2**2 + y_2**2)

    #Lat is obtained by an iterative proceedure:   
    lat = arctan2(z_2,(p*(1-e2_2))) #Initial value
    latold = 2*pi
    while abs(lat - latold)>10**-16:
        lat, latold = latold, lat
        nu_2 = a_2/sqrt(1-e2_2*sin(latold)**2)
        lat = arctan2(z_2+e2_2*nu_2*sin(latold), p)

    #Lon and height are then pretty easy
    lon = arctan2(y_2,x_2)
    H = p/cos(lat) - nu_2

    #Uncomment this line if you want to print the results
    #print [(lat-lat_1)*180/pi, (lon - lon_1)*180/pi]

    #Convert to degrees
    lat = lat*180/pi
    lon = lon*180/pi

    #Job's a good'n.
    return lat, lon


############################################################
# 
# Code below written by Ian Watt and Paul Niven
#  at Aberdeen Culture Hack (#ach13 on Tiwtter)
# 29-30 June 2013
#
#
#############################################################
start_next = 0

#initialise global variables
rec_title = ""
Current_status = ""
Author=""
SMR_Number = ""
Site_Type = ""
Period = ""
Parish= ""
Map_Ref = ""
RCAHMS = ""
Biblio_Ref = ""
image_link = ""
image_dec = ""
rec_body = ""
East_North = ""
Lat_Lon = ""
ID = 0
Alt_Site = ""

def scrape_sub(url_in):
    
    global  start_next, image_link, image_desc, rec_body, rec_title, Current_status, Author,SMR_Number, Site_Type, Period, Parish, Map_Ref, RCAHMS, Biblio_Ref, East_North, Lat_Lon, ID, Alt_Site
    print url_in
    sub_html = scraperwiki.scrape(url_in)
    sub_html = sub_html.replace("<br />", "\n")
    sub_root = lxml.html.fromstring(sub_html)

    ID = re.findall(r'\d+', url_in)[0]

    #for el in root.cssselect("div#content-app-body"):
    #    print el
    #root = lxml.html.fromstring(html) # turn our HTML into an lxml object
    #tds = root.cssselect('td') # get all the <td> tags
    #for td in tds:
    #    print lxml.html.tostring(td) # the full HTML tag
    #    print td.text                # just the text inside the HTML tag

    # Get the main HTML
    main_body = sub_root.cssselect("div.grid_6#main-content")[0]
    
    # Get the TITLE
    rec_title = str(main_body.cssselect("h2")[0].text)

    # Check to see if there is an IMAGE
    image_found = False
    image =  main_body.cssselect("img")
    if len(image)>0:
        # There is an IMAGE
        image_found = True
        # Grab the IMAGE URL
        image_link = "http://www.aberdeencity.gov.uk" + image[0].attrib['src']
        # Grab the IMAGE_DESC
        image_desc = main_body.cssselect("img")[0].attrib['alt']
        # Set the paragraph seacrh to start at 1
        para_start = 1+1
    else:
        # Set the paragraph search to start at 2
        para_start = 2+1

    paras = main_body.cssselect("p")     

    if image_found == True:
        range_start = 1
    else:
        range_start = 0

    range_end = len(paras)

    for i in range(range_start, range_end):

        spans = paras[i].cssselect("span")

        if len(spans) == 0:
            #print "Found BODY: " + paras[i].text
            rec_body = paras[i].text
        else:
            #print "Found SPAN for: " + spans[0].text
            #print spans[0].text + spans[1].text

            header = spans[0].text
            #print "Checking HEADER: '" + header + "'"

            if header == "Current Status: ":
                Current_status = spans[1].text
            elif header == "Author and Date: ":
                Author = spans[1].text
            elif header == "SMR Number: ":
                SMR_Number = spans[1].text
            elif header == "Site Type(s): ":
                Site_Type = spans[1].text
            elif header == "Period(s): ":
                Period = spans[1].text
            elif header == "Parish: ":
                Parish = spans[1].text
            elif header == "Map Reference: ":
                 Map_Ref= spans[1].text
            elif header == "RCAHMS Number(s): ":
                 RCAHMS = spans[1].text
            elif header == "Bibliographical Reference: ":
                 Biblio_Ref = spans[1].text
            elif header == "Alternative Site name(s): ":
                 Alt_Site = spans[1].text
            else:
                print "** ERROR: Unknown header - '" + spans[0].text + "'"

    # Convert Co-Ords
    if Map_Ref <> "":
        East_North = to_osgb36(Map_Ref)
        Lat_Lon = OSGB36toWGS84(East_North[0], East_North[1])


    # Print out this records details
    print "ID: " + ID
    print "TITLE: " + rec_title
    #print "CURRENT STATUS: " + Current_status
    #print "AUTHOR: " + Author
    #print "SMR NUMBER: " + SMR_Number
    #print "SITE TYPE: " + Site_Type
    #print "PERIOD: " + Period
    #print "PARISH: " + Parish
    #print "MAP REF: " + Map_Ref
    #print "RCAHMS: " + RCAHMS
    #print "BIBLIO REF: " + Biblio_Ref
    print "IMAGE LINK: " + image_link
    #print "IMAGE DESC: " + image_desc
    #print "REC BODY: " + rec_body
    #print "EAST NORTH: " + str(East_North[0]) + "," + str(East_North[1])
    #print "LAT LON: " + str(Lat_Lon[0]) + "," + str(Lat_Lon[1])
    #print "ALT SITE: " + Alt_Site

    if rec_title != "None":
        print "Saving Record ID: " + ID + "  TITLE: " + rec_title

        scraperwiki.sqlite.save(unique_keys=["ID"], data={"ID":ID, "Title":rec_title, "Status":Current_status, "Author":Author, "SMR_Number":SMR_Number, "Site_Type": Site_Type, "Period": Period, "Parish":Parish, "Map_Ref":Map_Ref, "RCAHMS":RCAHMS, "Biblio_Ref":Biblio_Ref, "Image_Link":image_link, "Image_Desc":image_desc, "Record_Body": rec_body, "Alt_Site": Alt_Site, "Latitude":str(Lat_Lon[0]), "Longitude": str(Lat_Lon[1]), "Easting": str(East_North[0]), "Northing": str(East_North[1]) })
    else:
        print "Skipping Record ID: " + ID


# the following lines were used to fake some records for #ach13 
#
#
#list_ids = (1838, 1744, 2329, 1856, 1634, 1645, 1650, 1658, 1750, 1751, 1840, 2498)
#
#for i in list_ids:    
#   print i
#    scrape_sub("http://www.aberdeencity.gov.uk/xsm_SmrDetail.asp?id=" + str(i))
#####################################################################################    


for el in root.cssselect("div#content-app#-body a"):
    print el
    scrape_sub("http://www.aberdeencity.gov.uk/" + el.attrib['href'])

# test single page scrapes
#
#scrape_sub("http://www.aberdeencity.gov.uk/xsm_SmrDetail.asp?id=2385")
#scrape_sub("http://www.aberdeencity.gov.uk/xsm_SmrDetail.asp?id=2518")





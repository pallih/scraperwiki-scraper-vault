require 'zip/zip'
require 'open-uri'
require 'csv'
require 'yaml'

module EastingNorthing
  # arguments are easting, northing
  # returns a hash of WGS84 lat and long - eg {"lat"=>51.234, "long" =>"0.1234"}
  def self.eastingNorthingToLatLong(easting, northing)
    
    east = easting
    north = northing
  
  
    a = 6377563.396
    b = 6356256.910              # Airy 1830 major & minor semi-axes
    f0 = 0.9996012717                             # NatGrid scale factor on central meridian
    lat0 = 49*Math::PI/180 
    lon0 = -2*Math::PI/180  # NatGrid true origin
    n0 = -100000 
    e0 = 400000                     # northing & easting of true origin, metres
    e2 = 1 - (b*b)/(a*a)                          # eccentricity squared
    n = (a-b)/(a+b) 
    n2 = n*n 
    n3 = n*n*n
  
    lat=lat0
    m=0
    while (north-n0-m >= 0.00001) do 
      lat = (north-n0-m)/(a*f0) + lat
  
      ma = (1 + n + (5/4)*n2 + (5/4)*n3) * (lat-lat0)
      mb = (3*n + 3*n*n + (21/8)*n3) * Math.sin(lat-lat0) * Math.cos(lat+lat0)
      mc = ((15/8)*n2 + (15/8)*n3) * Math.sin(2*(lat-lat0)) * Math.cos(2*(lat+lat0))
      md = (35/24)*n3 * Math.sin(3*(lat-lat0)) * Math.cos(3*(lat+lat0))
      m = b * f0 * (ma - mb + mc - md)                # meridional arc
  
    end
  
    cosLat = Math.cos(lat)
    sinLat = Math.sin(lat)
    nu = a*f0/Math.sqrt(1-e2*sinLat*sinLat)              # transverse radius of curvature
    rho = a*f0*(1-e2)/((1-e2*sinLat*sinLat)**1.5)  # meridional radius of curvature
    eta2 = nu/rho-1
  
    tanLat = Math.tan(lat)
    tan2lat = tanLat*tanLat
    tan4lat = tan2lat*tan2lat
    tan6lat = tan4lat*tan2lat
    secLat = 1/cosLat
    nu3 = nu*nu*nu
    nu5 = nu3*nu*nu
    nu7 = nu5*nu*nu
    vii = tanLat/(2*rho*nu)
    viii = tanLat/(24*rho*nu3)*(5+3*tan2lat+eta2-9*tan2lat*eta2)
    ix = tanLat/(720*rho*nu5)*(61+90*tan2lat+45*tan4lat)
    x = secLat/nu
    xi = secLat/(6*nu3)*(nu/rho+2*tan2lat)
    xii = secLat/(120*nu5)*(5+28*tan2lat+24*tan4lat)
    xiia = secLat/(5040*nu7)*(61+662*tan2lat+1320*tan4lat+720*tan6lat)
  
    dE = (east-e0)
    dE2 = dE*dE
    dE3 = dE2*dE
    dE4 = dE2*dE2
    dE5 = dE3*dE2
    dE6 = dE4*dE2
    dE7 = dE5*dE2
    lat = lat - vii*dE2 + viii*dE4 - ix*dE6
    lon = lon0 + x*dE - xi*dE3 + xii*dE5 - xiia*dE7
      
    # convert OSGB36 to WGS84
    wgs84lat = convertOSGB36toWGS84(toDeg(lat),toDeg(lon),0)[0]
    wgs84long = convertOSGB36toWGS84(toDeg(lat),toDeg(lon),0)[1]
    return {"lat"=>wgs84lat, "long"=>wgs84long}
  
  end
  
  # arguments are WGS84 lat, long
  # returns hash of OS easting, northing (to nearest metre) eg {"easting"=>123456, "northing"=>123456}
  def self.latLongToEastingNorthing(lat,long)
  
    height = 0
    osgb36point = convertWGS84toOSGB36(lat,long, height)
    oslat = osgb36point[0]
    oslon = osgb36point[1]
    osh = osgb36point[2]
  
    osUKgridPoint = LatLongToOSGrid(oslat,oslon)
    easting  = osUKgridPoint[0].round
    northing = osUKgridPoint[1].round
   
  
    return {"easting"=>easting,"northing"=>northing}
  end
  
  
  # supporting code - don't need to call this directly
  #---------------------------------------------------------------------------------------------
  
  # Some UK Ordnance Survey coordinate conversions in pure ruby.
  #
  # WGS84 lat/lons -> OSGB64 lat/lons-> OS Eastings & Northings 
  
  
  # http://www.movable-type.co.uk/scripts/latlong-convert-coords.html
  # (c) Chris Veness 2005-2010  Released under an LGPL license
  # http://www.fsf.org/licensing/licenses/lgpl.html
  # Ported to ruby by Harry Wood
    
    
  #ellipse parameters
  @e = { :wgs84 =>   { :a=> 6378137,     :b=> 6356752.3142, :f=> 1 / 298.257223563 },
        :airy1830 => { :a=> 6377563.396, :b=> 6356256.910,  :f=> 1 / 299.3249646   } };
  
  #helmert transform parameters
  @h = { :wgs84toOSGB36 => { :tx=> -446.448,  :ty=>  125.157,  :tz=> -542.060,  # m
                             :rx=>  -0.1502,  :ry=>   -0.2470, :rz=>  -0.8421,  # sec
                             :s=>   20.4894 },                                  # ppm
         :osgb36toWGS84 => { :tx=>  446.448,  :ty=> -125.157,  :tz=>  542.060,
                             :rx=>    0.1502, :ry=>    0.2470, :rz=>    0.8421,
                             :s=>   -20.4894 } };
  
                 
  def self.convertOSGB36toWGS84(p1lat, p1lon, p1height) 
     p2 = convert(p1lat, p1lon, p1height, @e[:airy1830], @h[:osgb36toWGS84], @e[:wgs84]);
     return p2;
  end
  
  
  def self.convertWGS84toOSGB36(p1lat, p1lon, p1height)
     p2 = convert(p1lat, p1lon, p1height, @e[:wgs84], @h[:wgs84toOSGB36], @e[:airy1830]);
     return p2;
  end
  
  def self.convert(p1lat, p1lon, p1height, e1, t, e2)
     # -- convert polar to cartesian coordinates (using ellipse 1)
   
     p1lat = toRad(p1lat); p1lon = toRad(p1lon); 
   
     a = e1[:a]; b = e1[:b];
     
     sinPhi = Math.sin(p1lat); cosPhi = Math.cos(p1lat);
     sinLambda = Math.sin(p1lon); cosLambda = Math.cos(p1lon);
     h = p1height;
     
     eSq = (a*a - b*b) / (a*a);
     nu = a / Math.sqrt(1 - eSq*sinPhi*sinPhi);
     
     x1 = (nu+h) * cosPhi * cosLambda;
     y1 = (nu+h) * cosPhi * sinLambda;
     z1 = ((1-eSq)*nu + h) * sinPhi;
     
   
     # -- apply helmert transform using appropriate params
     
     tx = t[:tx]; ty = t[:ty]; tz = t[:tz];
     rx = t[:rx] / 3600 * Math::PI/180;  #normalise seconds to radians
     ry = t[:ry] / 3600 * Math::PI/180;
     rz = t[:rz] / 3600 * Math::PI/180;
     s1 = t[:s] / 1e6 + 1;              #normalise ppm to (s+1)
   
     #apply transform
     x2 = tx + x1*s1 - y1*rz + z1*ry;
     y2 = ty + x1*rz + y1*s1 - z1*rx;
     z2 = tz - x1*ry + y1*rx + z1*s1;
   
   
     # -- convert cartesian to polar coordinates (using ellipse 2)
   
     a = e2[:a]; b = e2[:b];
     precision = 4 / a;  # results accurate to around 4 metres
   
     eSq = (a*a - b*b) / (a*a);
     p = Math.sqrt(x2*x2 + y2*y2);
     phi = Math.atan2(z2, p*(1-eSq)); phiP = 2 * Math::PI;
     while ( (phi-phiP).abs > precision) do
        nu = a / Math.sqrt(1 - eSq*Math.sin(phi)*Math.sin(phi));
        phiP = phi;
        phi = Math.atan2(z2 + eSq*nu*Math.sin(phi), p);
     end
     lambda = Math.atan2(y2, x2);
     h = p/Math.cos(phi) - nu;
     
     #return array [lat,lon,height]
     return [ toDeg(phi), toDeg(lambda), h ]; 
  end
  
    
  
  
  # http://www.movable-type.co.uk/scripts/latlong-gridref.html
  # (c) Chris Veness 2005-2010  Released under an LGPL license
  # http://www.fsf.org/licensing/licenses/lgpl.html
  # Ported to ruby by Harry Wood
  
  # OSGB36 lat lon to OS UK grid eastings & northings
  
  #
  def self.LatLongToOSGrid(lat, long)
     lat = toRad(lat);
     lon = toRad(long);
     
     a = 6377563.396; b = 6356256.910          # Airy 1830 major & minor semi-axes
     f0 = 0.9996012717                         # NatGrid scale factor on central meridian
     lat0 = toRad(49); lon0 = toRad(-2)        # NatGrid true origin
     n0 = -100000; e0 = 400000;                # northing & easting of true origin, metres
     e2 = 1 - (b*b) / (a*a);                   # eccentricity squared
     n = (a-b) / (a+b); n2 = n*n; n3 = n*n*n;
     
     cosLat = Math.cos(lat); sinLat = Math.sin(lat);
     nu = a*f0/Math.sqrt(1-e2*sinLat*sinLat);              # transverse radius of curvature
     rho = a*f0*(1-e2) / ( (1-e2*sinLat*sinLat) ** 1.5);  # meridional radius of curvature
     eta2 = nu/rho-1;
     
     ma = (1 + n + (5/4)*n2 + (5/4)*n3) * (lat-lat0);
     mb = (3*n + 3*n*n + (21/8)*n3) * Math.sin(lat-lat0) * Math.cos(lat+lat0);
     mc = ((15/8)*n2 + (15/8)*n3) * Math.sin(2*(lat-lat0)) * Math.cos(2*(lat+lat0));
     md = (35/24)*n3 * Math.sin(3*(lat-lat0)) * Math.cos(3*(lat+lat0));
     m = b * f0 * (ma - mb + mc - md);              # meridional arc
     
     cos3lat = cosLat*cosLat*cosLat;
     cos5lat = cos3lat*cosLat*cosLat;
     tan2lat = Math.tan(lat)*Math.tan(lat);
     tan4lat = tan2lat*tan2lat;
     
     i = m + n0;
     ii = (nu/2)*sinLat*cosLat;
     iii = (nu/24)*sinLat*cos3lat*(5-tan2lat+9*eta2);
     iiiA = (nu/720)*sinLat*cos5lat*(61-58*tan2lat+tan4lat);
     iv = nu*cosLat;
     v = (nu/6)*cos3lat*(nu/rho-tan2lat);
     vi = (nu/120) * cos5lat * (5 - 18*tan2lat + tan4lat + 14*eta2 - 58*tan2lat*eta2);
     
     dLon = lon-lon0;
     dLon2 = dLon*dLon
     dLon3 = dLon2*dLon
     dLon4 = dLon3*dLon
     dLon5 = dLon4*dLon
     dLon6 = dLon5*dLon
     
     n = i + ii*dLon2 + iii*dLon4 + iiiA*dLon6;
     e = e0 + iv*dLon + v*dLon3 + vi*dLon5;
    
     return [ e, n ]   #return raw easting and northings instead
     
     #return gridrefNumToLet( e, n, 8) 
  end
  
  def self.toRad(degrees)
     return degrees * Math::PI / 180;
  end
  
  def self.toDeg(rads)
     return rads * 180 / Math::PI 
  end
  
  #convert numeric grid reference (in metres) to standard-form grid ref
  def self.gridrefNumToLet(e, n, digits) 
     #get the 100km-grid indices
     e100k = (e / 100000).floor; n100k = (n / 100000).floor;
     
     return '' if (e100k<0 or e100k>6 or n100k<0 or n100k>12)
                                                                  
     #translate those into numeric equivalents of the grid letters
     l1 = (19-n100k) - (19-n100k) % 5 + ((e100k+10) / 5).floor;
     l2 = (19-n100k) * 5 % 25 + e100k % 5;
     
     # compensate for skipped 'I' and build grid letter-pairs         
     l1=l1+1 if (l1 > 7)
     l2=l2+1 if (l2 > 7) 
     letPair =  (l1 +'A'[0]).chr +  (l2 +'A'[0]).chr ;
   
     # strip 100km-grid indices from easting & northing, and reduce precision
     e = ( (e % 100000) / (10 ** (5 - digits / 2)) ).floor;
     n = ( (n % 100000) / (10 ** (5 - digits / 2)) ).floor;
     
     gridRef = letPair + e.to_s.rjust(digits / 2) + n.to_s.rjust(digits / 2)
   
     return gridRef;
  end
end

uri = 'http://www.whatdotheyknow.com/request/30917/response/184518/attach/3/Whittaker%20Annex.txt'
result = open(uri)

CSV.parse(result) do |row|
  record = {}
  
  record[:category] = row[0].force_encoding("BINARY").gsub("\xEF\xBB\xBF", "") rescue nil
  record[:location] = row[1]
  record[:outcode] = row[2]
  record[:id] = row[4]
  record[:easting] = row[5].to_i
  record[:northing] = row[6].to_i

  latlng = EastingNorthing.eastingNorthingToLatLong(record[:easting], record[:northing])
            
  record[:lat] = latlng["lat"]
  record[:lng] = latlng["long"]
  record[:depot] = row[7]
  record[:depotid] = row[8]
  record[:type] = row[9]
  record[:collection1] = row[10]
  record[:collection2] = row[11]

  if record[:id].nil? || record[:id].empty? 
    record[:id] = row[1]
  end
  
  unless record[:id].nil? || record[:id].empty? 
    ScraperWiki.save([:id], record)
  end
endrequire 'zip/zip'
require 'open-uri'
require 'csv'
require 'yaml'

module EastingNorthing
  # arguments are easting, northing
  # returns a hash of WGS84 lat and long - eg {"lat"=>51.234, "long" =>"0.1234"}
  def self.eastingNorthingToLatLong(easting, northing)
    
    east = easting
    north = northing
  
  
    a = 6377563.396
    b = 6356256.910              # Airy 1830 major & minor semi-axes
    f0 = 0.9996012717                             # NatGrid scale factor on central meridian
    lat0 = 49*Math::PI/180 
    lon0 = -2*Math::PI/180  # NatGrid true origin
    n0 = -100000 
    e0 = 400000                     # northing & easting of true origin, metres
    e2 = 1 - (b*b)/(a*a)                          # eccentricity squared
    n = (a-b)/(a+b) 
    n2 = n*n 
    n3 = n*n*n
  
    lat=lat0
    m=0
    while (north-n0-m >= 0.00001) do 
      lat = (north-n0-m)/(a*f0) + lat
  
      ma = (1 + n + (5/4)*n2 + (5/4)*n3) * (lat-lat0)
      mb = (3*n + 3*n*n + (21/8)*n3) * Math.sin(lat-lat0) * Math.cos(lat+lat0)
      mc = ((15/8)*n2 + (15/8)*n3) * Math.sin(2*(lat-lat0)) * Math.cos(2*(lat+lat0))
      md = (35/24)*n3 * Math.sin(3*(lat-lat0)) * Math.cos(3*(lat+lat0))
      m = b * f0 * (ma - mb + mc - md)                # meridional arc
  
    end
  
    cosLat = Math.cos(lat)
    sinLat = Math.sin(lat)
    nu = a*f0/Math.sqrt(1-e2*sinLat*sinLat)              # transverse radius of curvature
    rho = a*f0*(1-e2)/((1-e2*sinLat*sinLat)**1.5)  # meridional radius of curvature
    eta2 = nu/rho-1
  
    tanLat = Math.tan(lat)
    tan2lat = tanLat*tanLat
    tan4lat = tan2lat*tan2lat
    tan6lat = tan4lat*tan2lat
    secLat = 1/cosLat
    nu3 = nu*nu*nu
    nu5 = nu3*nu*nu
    nu7 = nu5*nu*nu
    vii = tanLat/(2*rho*nu)
    viii = tanLat/(24*rho*nu3)*(5+3*tan2lat+eta2-9*tan2lat*eta2)
    ix = tanLat/(720*rho*nu5)*(61+90*tan2lat+45*tan4lat)
    x = secLat/nu
    xi = secLat/(6*nu3)*(nu/rho+2*tan2lat)
    xii = secLat/(120*nu5)*(5+28*tan2lat+24*tan4lat)
    xiia = secLat/(5040*nu7)*(61+662*tan2lat+1320*tan4lat+720*tan6lat)
  
    dE = (east-e0)
    dE2 = dE*dE
    dE3 = dE2*dE
    dE4 = dE2*dE2
    dE5 = dE3*dE2
    dE6 = dE4*dE2
    dE7 = dE5*dE2
    lat = lat - vii*dE2 + viii*dE4 - ix*dE6
    lon = lon0 + x*dE - xi*dE3 + xii*dE5 - xiia*dE7
      
    # convert OSGB36 to WGS84
    wgs84lat = convertOSGB36toWGS84(toDeg(lat),toDeg(lon),0)[0]
    wgs84long = convertOSGB36toWGS84(toDeg(lat),toDeg(lon),0)[1]
    return {"lat"=>wgs84lat, "long"=>wgs84long}
  
  end
  
  # arguments are WGS84 lat, long
  # returns hash of OS easting, northing (to nearest metre) eg {"easting"=>123456, "northing"=>123456}
  def self.latLongToEastingNorthing(lat,long)
  
    height = 0
    osgb36point = convertWGS84toOSGB36(lat,long, height)
    oslat = osgb36point[0]
    oslon = osgb36point[1]
    osh = osgb36point[2]
  
    osUKgridPoint = LatLongToOSGrid(oslat,oslon)
    easting  = osUKgridPoint[0].round
    northing = osUKgridPoint[1].round
   
  
    return {"easting"=>easting,"northing"=>northing}
  end
  
  
  # supporting code - don't need to call this directly
  #---------------------------------------------------------------------------------------------
  
  # Some UK Ordnance Survey coordinate conversions in pure ruby.
  #
  # WGS84 lat/lons -> OSGB64 lat/lons-> OS Eastings & Northings 
  
  
  # http://www.movable-type.co.uk/scripts/latlong-convert-coords.html
  # (c) Chris Veness 2005-2010  Released under an LGPL license
  # http://www.fsf.org/licensing/licenses/lgpl.html
  # Ported to ruby by Harry Wood
    
    
  #ellipse parameters
  @e = { :wgs84 =>   { :a=> 6378137,     :b=> 6356752.3142, :f=> 1 / 298.257223563 },
        :airy1830 => { :a=> 6377563.396, :b=> 6356256.910,  :f=> 1 / 299.3249646   } };
  
  #helmert transform parameters
  @h = { :wgs84toOSGB36 => { :tx=> -446.448,  :ty=>  125.157,  :tz=> -542.060,  # m
                             :rx=>  -0.1502,  :ry=>   -0.2470, :rz=>  -0.8421,  # sec
                             :s=>   20.4894 },                                  # ppm
         :osgb36toWGS84 => { :tx=>  446.448,  :ty=> -125.157,  :tz=>  542.060,
                             :rx=>    0.1502, :ry=>    0.2470, :rz=>    0.8421,
                             :s=>   -20.4894 } };
  
                 
  def self.convertOSGB36toWGS84(p1lat, p1lon, p1height) 
     p2 = convert(p1lat, p1lon, p1height, @e[:airy1830], @h[:osgb36toWGS84], @e[:wgs84]);
     return p2;
  end
  
  
  def self.convertWGS84toOSGB36(p1lat, p1lon, p1height)
     p2 = convert(p1lat, p1lon, p1height, @e[:wgs84], @h[:wgs84toOSGB36], @e[:airy1830]);
     return p2;
  end
  
  def self.convert(p1lat, p1lon, p1height, e1, t, e2)
     # -- convert polar to cartesian coordinates (using ellipse 1)
   
     p1lat = toRad(p1lat); p1lon = toRad(p1lon); 
   
     a = e1[:a]; b = e1[:b];
     
     sinPhi = Math.sin(p1lat); cosPhi = Math.cos(p1lat);
     sinLambda = Math.sin(p1lon); cosLambda = Math.cos(p1lon);
     h = p1height;
     
     eSq = (a*a - b*b) / (a*a);
     nu = a / Math.sqrt(1 - eSq*sinPhi*sinPhi);
     
     x1 = (nu+h) * cosPhi * cosLambda;
     y1 = (nu+h) * cosPhi * sinLambda;
     z1 = ((1-eSq)*nu + h) * sinPhi;
     
   
     # -- apply helmert transform using appropriate params
     
     tx = t[:tx]; ty = t[:ty]; tz = t[:tz];
     rx = t[:rx] / 3600 * Math::PI/180;  #normalise seconds to radians
     ry = t[:ry] / 3600 * Math::PI/180;
     rz = t[:rz] / 3600 * Math::PI/180;
     s1 = t[:s] / 1e6 + 1;              #normalise ppm to (s+1)
   
     #apply transform
     x2 = tx + x1*s1 - y1*rz + z1*ry;
     y2 = ty + x1*rz + y1*s1 - z1*rx;
     z2 = tz - x1*ry + y1*rx + z1*s1;
   
   
     # -- convert cartesian to polar coordinates (using ellipse 2)
   
     a = e2[:a]; b = e2[:b];
     precision = 4 / a;  # results accurate to around 4 metres
   
     eSq = (a*a - b*b) / (a*a);
     p = Math.sqrt(x2*x2 + y2*y2);
     phi = Math.atan2(z2, p*(1-eSq)); phiP = 2 * Math::PI;
     while ( (phi-phiP).abs > precision) do
        nu = a / Math.sqrt(1 - eSq*Math.sin(phi)*Math.sin(phi));
        phiP = phi;
        phi = Math.atan2(z2 + eSq*nu*Math.sin(phi), p);
     end
     lambda = Math.atan2(y2, x2);
     h = p/Math.cos(phi) - nu;
     
     #return array [lat,lon,height]
     return [ toDeg(phi), toDeg(lambda), h ]; 
  end
  
    
  
  
  # http://www.movable-type.co.uk/scripts/latlong-gridref.html
  # (c) Chris Veness 2005-2010  Released under an LGPL license
  # http://www.fsf.org/licensing/licenses/lgpl.html
  # Ported to ruby by Harry Wood
  
  # OSGB36 lat lon to OS UK grid eastings & northings
  
  #
  def self.LatLongToOSGrid(lat, long)
     lat = toRad(lat);
     lon = toRad(long);
     
     a = 6377563.396; b = 6356256.910          # Airy 1830 major & minor semi-axes
     f0 = 0.9996012717                         # NatGrid scale factor on central meridian
     lat0 = toRad(49); lon0 = toRad(-2)        # NatGrid true origin
     n0 = -100000; e0 = 400000;                # northing & easting of true origin, metres
     e2 = 1 - (b*b) / (a*a);                   # eccentricity squared
     n = (a-b) / (a+b); n2 = n*n; n3 = n*n*n;
     
     cosLat = Math.cos(lat); sinLat = Math.sin(lat);
     nu = a*f0/Math.sqrt(1-e2*sinLat*sinLat);              # transverse radius of curvature
     rho = a*f0*(1-e2) / ( (1-e2*sinLat*sinLat) ** 1.5);  # meridional radius of curvature
     eta2 = nu/rho-1;
     
     ma = (1 + n + (5/4)*n2 + (5/4)*n3) * (lat-lat0);
     mb = (3*n + 3*n*n + (21/8)*n3) * Math.sin(lat-lat0) * Math.cos(lat+lat0);
     mc = ((15/8)*n2 + (15/8)*n3) * Math.sin(2*(lat-lat0)) * Math.cos(2*(lat+lat0));
     md = (35/24)*n3 * Math.sin(3*(lat-lat0)) * Math.cos(3*(lat+lat0));
     m = b * f0 * (ma - mb + mc - md);              # meridional arc
     
     cos3lat = cosLat*cosLat*cosLat;
     cos5lat = cos3lat*cosLat*cosLat;
     tan2lat = Math.tan(lat)*Math.tan(lat);
     tan4lat = tan2lat*tan2lat;
     
     i = m + n0;
     ii = (nu/2)*sinLat*cosLat;
     iii = (nu/24)*sinLat*cos3lat*(5-tan2lat+9*eta2);
     iiiA = (nu/720)*sinLat*cos5lat*(61-58*tan2lat+tan4lat);
     iv = nu*cosLat;
     v = (nu/6)*cos3lat*(nu/rho-tan2lat);
     vi = (nu/120) * cos5lat * (5 - 18*tan2lat + tan4lat + 14*eta2 - 58*tan2lat*eta2);
     
     dLon = lon-lon0;
     dLon2 = dLon*dLon
     dLon3 = dLon2*dLon
     dLon4 = dLon3*dLon
     dLon5 = dLon4*dLon
     dLon6 = dLon5*dLon
     
     n = i + ii*dLon2 + iii*dLon4 + iiiA*dLon6;
     e = e0 + iv*dLon + v*dLon3 + vi*dLon5;
    
     return [ e, n ]   #return raw easting and northings instead
     
     #return gridrefNumToLet( e, n, 8) 
  end
  
  def self.toRad(degrees)
     return degrees * Math::PI / 180;
  end
  
  def self.toDeg(rads)
     return rads * 180 / Math::PI 
  end
  
  #convert numeric grid reference (in metres) to standard-form grid ref
  def self.gridrefNumToLet(e, n, digits) 
     #get the 100km-grid indices
     e100k = (e / 100000).floor; n100k = (n / 100000).floor;
     
     return '' if (e100k<0 or e100k>6 or n100k<0 or n100k>12)
                                                                  
     #translate those into numeric equivalents of the grid letters
     l1 = (19-n100k) - (19-n100k) % 5 + ((e100k+10) / 5).floor;
     l2 = (19-n100k) * 5 % 25 + e100k % 5;
     
     # compensate for skipped 'I' and build grid letter-pairs         
     l1=l1+1 if (l1 > 7)
     l2=l2+1 if (l2 > 7) 
     letPair =  (l1 +'A'[0]).chr +  (l2 +'A'[0]).chr ;
   
     # strip 100km-grid indices from easting & northing, and reduce precision
     e = ( (e % 100000) / (10 ** (5 - digits / 2)) ).floor;
     n = ( (n % 100000) / (10 ** (5 - digits / 2)) ).floor;
     
     gridRef = letPair + e.to_s.rjust(digits / 2) + n.to_s.rjust(digits / 2)
   
     return gridRef;
  end
end

uri = 'http://www.whatdotheyknow.com/request/30917/response/184518/attach/3/Whittaker%20Annex.txt'
result = open(uri)

CSV.parse(result) do |row|
  record = {}
  
  record[:category] = row[0].force_encoding("BINARY").gsub("\xEF\xBB\xBF", "") rescue nil
  record[:location] = row[1]
  record[:outcode] = row[2]
  record[:id] = row[4]
  record[:easting] = row[5].to_i
  record[:northing] = row[6].to_i

  latlng = EastingNorthing.eastingNorthingToLatLong(record[:easting], record[:northing])
            
  record[:lat] = latlng["lat"]
  record[:lng] = latlng["long"]
  record[:depot] = row[7]
  record[:depotid] = row[8]
  record[:type] = row[9]
  record[:collection1] = row[10]
  record[:collection2] = row[11]

  if record[:id].nil? || record[:id].empty? 
    record[:id] = row[1]
  end
  
  unless record[:id].nil? || record[:id].empty? 
    ScraperWiki.save([:id], record)
  end
end
import scraperwiki
import urllib
import StringIO
import csv

# This is data that was obtained from this FOI request:
# http://www.whatdotheyknow.com/request/tribal_asset_management_database
    
def LoadAssetList():
    assetlisturl = "http://www.whatdotheyknow.com/request/18466/response/50987/attach/3/FOI%20AssetList%20BPpremise.csv.txt"
    #fin = urllib.urlopen(assetlisturl)
    print assetlisturl
    fin = StringIO.StringIO(scraperwiki.scrape(assetlisturl))
    c = csv.reader(fin.readlines())
    headers = c.next()
    print headers
    for line in c:
        data = dict(zip(headers, line))
        easting = int(data.pop("Easting"))
        northing = int(data.pop("Northing"))
        if easting != 0 and northing != 0:
            data["latlng"] = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
        scraperwiki.datastore.save(unique_keys=["UPRN"], data=data)
    fin.close()


LoadAssetList()import scraperwiki
import urllib
import StringIO
import csv

# This is data that was obtained from this FOI request:
# http://www.whatdotheyknow.com/request/tribal_asset_management_database
    
def LoadAssetList():
    assetlisturl = "http://www.whatdotheyknow.com/request/18466/response/50987/attach/3/FOI%20AssetList%20BPpremise.csv.txt"
    #fin = urllib.urlopen(assetlisturl)
    print assetlisturl
    fin = StringIO.StringIO(scraperwiki.scrape(assetlisturl))
    c = csv.reader(fin.readlines())
    headers = c.next()
    print headers
    for line in c:
        data = dict(zip(headers, line))
        easting = int(data.pop("Easting"))
        northing = int(data.pop("Northing"))
        if easting != 0 and northing != 0:
            data["latlng"] = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
        scraperwiki.datastore.save(unique_keys=["UPRN"], data=data)
    fin.close()


LoadAssetList()import scraperwiki
import urllib
import StringIO
import csv

# This is data that was obtained from this FOI request:
# http://www.whatdotheyknow.com/request/tribal_asset_management_database
    
def LoadAssetList():
    assetlisturl = "http://www.whatdotheyknow.com/request/18466/response/50987/attach/3/FOI%20AssetList%20BPpremise.csv.txt"
    #fin = urllib.urlopen(assetlisturl)
    print assetlisturl
    fin = StringIO.StringIO(scraperwiki.scrape(assetlisturl))
    c = csv.reader(fin.readlines())
    headers = c.next()
    print headers
    for line in c:
        data = dict(zip(headers, line))
        easting = int(data.pop("Easting"))
        northing = int(data.pop("Northing"))
        if easting != 0 and northing != 0:
            data["latlng"] = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
        scraperwiki.datastore.save(unique_keys=["UPRN"], data=data)
    fin.close()


LoadAssetList()import scraperwiki
import urllib
import StringIO
import csv

# This is data that was obtained from this FOI request:
# http://www.whatdotheyknow.com/request/tribal_asset_management_database
    
def LoadAssetList():
    assetlisturl = "http://www.whatdotheyknow.com/request/18466/response/50987/attach/3/FOI%20AssetList%20BPpremise.csv.txt"
    #fin = urllib.urlopen(assetlisturl)
    print assetlisturl
    fin = StringIO.StringIO(scraperwiki.scrape(assetlisturl))
    c = csv.reader(fin.readlines())
    headers = c.next()
    print headers
    for line in c:
        data = dict(zip(headers, line))
        easting = int(data.pop("Easting"))
        northing = int(data.pop("Northing"))
        if easting != 0 and northing != 0:
            data["latlng"] = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
        scraperwiki.datastore.save(unique_keys=["UPRN"], data=data)
    fin.close()


LoadAssetList()import scraperwiki
import urllib
import StringIO
import csv

# This is data that was obtained from this FOI request:
# http://www.whatdotheyknow.com/request/tribal_asset_management_database
    
def LoadAssetList():
    assetlisturl = "http://www.whatdotheyknow.com/request/18466/response/50987/attach/3/FOI%20AssetList%20BPpremise.csv.txt"
    #fin = urllib.urlopen(assetlisturl)
    print assetlisturl
    fin = StringIO.StringIO(scraperwiki.scrape(assetlisturl))
    c = csv.reader(fin.readlines())
    headers = c.next()
    print headers
    for line in c:
        data = dict(zip(headers, line))
        easting = int(data.pop("Easting"))
        northing = int(data.pop("Northing"))
        if easting != 0 and northing != 0:
            data["latlng"] = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
        scraperwiki.datastore.save(unique_keys=["UPRN"], data=data)
    fin.close()


LoadAssetList()import scraperwiki
import urllib
import StringIO
import csv

# This is data that was obtained from this FOI request:
# http://www.whatdotheyknow.com/request/tribal_asset_management_database
    
def LoadAssetList():
    assetlisturl = "http://www.whatdotheyknow.com/request/18466/response/50987/attach/3/FOI%20AssetList%20BPpremise.csv.txt"
    #fin = urllib.urlopen(assetlisturl)
    print assetlisturl
    fin = StringIO.StringIO(scraperwiki.scrape(assetlisturl))
    c = csv.reader(fin.readlines())
    headers = c.next()
    print headers
    for line in c:
        data = dict(zip(headers, line))
        easting = int(data.pop("Easting"))
        northing = int(data.pop("Northing"))
        if easting != 0 and northing != 0:
            data["latlng"] = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
        scraperwiki.datastore.save(unique_keys=["UPRN"], data=data)
    fin.close()


LoadAssetList()import scraperwiki
import urllib
import StringIO
import csv

# This is data that was obtained from this FOI request:
# http://www.whatdotheyknow.com/request/tribal_asset_management_database
    
def LoadAssetList():
    assetlisturl = "http://www.whatdotheyknow.com/request/18466/response/50987/attach/3/FOI%20AssetList%20BPpremise.csv.txt"
    #fin = urllib.urlopen(assetlisturl)
    print assetlisturl
    fin = StringIO.StringIO(scraperwiki.scrape(assetlisturl))
    c = csv.reader(fin.readlines())
    headers = c.next()
    print headers
    for line in c:
        data = dict(zip(headers, line))
        easting = int(data.pop("Easting"))
        northing = int(data.pop("Northing"))
        if easting != 0 and northing != 0:
            data["latlng"] = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
        scraperwiki.datastore.save(unique_keys=["UPRN"], data=data)
    fin.close()


LoadAssetList()
# code to be ported to scraperlibs once complete

require 'json'
require 'uri'
require 'net/http'

$apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"
$apilimit = 500

def get_url(url)
    puts url
    Net::HTTP.get(URI.parse(url))
end

def getKeys(name)
    url = "%sgetkeys?&name=%s" % [$apiurl, name]
    ljson = get_url(url)
    return JSON.parse(ljson)
end

def generateData(urlbase, limit, offset)
    count = 0
    loffset = 0
    while true
        if limit == -1
            llimit = $apilimit
        else
            llimit = [$apilimit, limit-count].min
        end

        url = "%s&limit=%s&offset=%d" % [urlbase, llimit, offset+loffset]
        ljson = get_url(url)
        lresult = JSON.parse(ljson)
        for row in lresult
            yield row
        end

        count += len(lresult)
           
       
        if limit != -1 and count >= limit    # exceeded the limit
            break
                                                        end

        loffset += llimit
    end
end

def getData(name, limit=-1, offset=0)
    urlbase = "%sgetdata?name=%s" % [$apiurl, name]
    return generateData(urlbase, limit, offset)
end

def getDataByDate(name, start_date, end_date, limit=-1, offset=0)
    urlbase = "%sgetdatabydate?name=%s&start_date=%s&end_date=%s" % [$apiurl, name, start_date, end_date]
    return generateData(urlbase, limit, offset)
end

def getDataByLocation(name, lat, lng, limit=-1, offset=0)
    urlbase = "%sgetdatabylocation?name=%s&lat=%f&lng=%f" % [$apiurl, name, lat, lng]
    return generateData(urlbase, limit, offset)
end
    
def search(name, filterdict, limit=-1, offset=0)
    raise "unfinished"
    #filter = map(lambda x: "%s,%s" % [urllib.quote(x[0]), urllib.quote(x[1])], filterdict.items()).join("|")
    urlbase = "%ssearch?name=%s&filter=%s" % [$apiurl, name, filter]
    return generateData(urlbase, limit, offset)
end

def Tests()
    $apilimit = 50  # easier to test

    name1 = "uk-offshore-oil-wells"
    name2 = "uk-lottery-grants"
    
    print getKeys(name1)
    
    getData(name1, limit=110).each_with_index do |s,i|
        print i, s
    end
        
    print "get data by date"
    getDataByDate(name2, start_date="2009-01-01", end_date="2009-01-12").each_with_index do |s,i|
        print i, s
    end

    print "get data by location"
    getDataByLocation(name1, lat=59.033358, lng=1.0486569, limit=60).each_with_index do |s,i|
        print i, s
    end
    
    print "search test"
    filterdict = {'Distributing_Body' => 'UK Sport', "Region" => "London"}
    search(name2, filterdict, offset=5, limit=17).each_with_index do |s,i|
        print i, s
    end
end
        
#Tests()
name1 = "uk-offshore-oil-wells"
for i, s in enumerate(getDataByLocation(name1, lat=59.033358, lng=1.0486569, limit=60))
    print i, s
end

# code to be ported to scraperlibs once complete

require 'json'
require 'uri'
require 'net/http'

$apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"
$apilimit = 500

def get_url(url)
    puts url
    Net::HTTP.get(URI.parse(url))
end

def getKeys(name)
    url = "%sgetkeys?&name=%s" % [$apiurl, name]
    ljson = get_url(url)
    return JSON.parse(ljson)
end

def generateData(urlbase, limit, offset)
    count = 0
    loffset = 0
    while true
        if limit == -1
            llimit = $apilimit
        else
            llimit = [$apilimit, limit-count].min
        end

        url = "%s&limit=%s&offset=%d" % [urlbase, llimit, offset+loffset]
        ljson = get_url(url)
        lresult = JSON.parse(ljson)
        for row in lresult
            yield row
        end

        count += len(lresult)
           
       
        if limit != -1 and count >= limit    # exceeded the limit
            break
                                                        end

        loffset += llimit
    end
end

def getData(name, limit=-1, offset=0)
    urlbase = "%sgetdata?name=%s" % [$apiurl, name]
    return generateData(urlbase, limit, offset)
end

def getDataByDate(name, start_date, end_date, limit=-1, offset=0)
    urlbase = "%sgetdatabydate?name=%s&start_date=%s&end_date=%s" % [$apiurl, name, start_date, end_date]
    return generateData(urlbase, limit, offset)
end

def getDataByLocation(name, lat, lng, limit=-1, offset=0)
    urlbase = "%sgetdatabylocation?name=%s&lat=%f&lng=%f" % [$apiurl, name, lat, lng]
    return generateData(urlbase, limit, offset)
end
    
def search(name, filterdict, limit=-1, offset=0)
    raise "unfinished"
    #filter = map(lambda x: "%s,%s" % [urllib.quote(x[0]), urllib.quote(x[1])], filterdict.items()).join("|")
    urlbase = "%ssearch?name=%s&filter=%s" % [$apiurl, name, filter]
    return generateData(urlbase, limit, offset)
end

def Tests()
    $apilimit = 50  # easier to test

    name1 = "uk-offshore-oil-wells"
    name2 = "uk-lottery-grants"
    
    print getKeys(name1)
    
    getData(name1, limit=110).each_with_index do |s,i|
        print i, s
    end
        
    print "get data by date"
    getDataByDate(name2, start_date="2009-01-01", end_date="2009-01-12").each_with_index do |s,i|
        print i, s
    end

    print "get data by location"
    getDataByLocation(name1, lat=59.033358, lng=1.0486569, limit=60).each_with_index do |s,i|
        print i, s
    end
    
    print "search test"
    filterdict = {'Distributing_Body' => 'UK Sport', "Region" => "London"}
    search(name2, filterdict, offset=5, limit=17).each_with_index do |s,i|
        print i, s
    end
end
        
#Tests()
name1 = "uk-offshore-oil-wells"
for i, s in enumerate(getDataByLocation(name1, lat=59.033358, lng=1.0486569, limit=60))
    print i, s
end


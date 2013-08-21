# code to be ported to scraperlibs once complete

# Ruby version of http://scraperwiki.com/views/php-api-access/edit/
# and http://scraperwiki.com/views/python-api-access/edit/ 
# here

require 'generator'
require 'json'
require 'cgi'

$apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"

def generateData(urlbase, limit, offset)
  apilimit = 500
  g = Generator.new do |g|
    count = 0
    while true
      if limit == -1
        step = apilimit
      else
        step = apilimit < (limit - count) ? apilimit : limit - count
      end

      url = "#{urlbase}&limit=#{step}&offset=#{offset+count}"
      records = JSON.parse(ScraperWiki.scrape(url))
      for r in records
        g.yield r
      end

      count += records.length

      if records.length < step
        # run out of records
        puts "Run out of records"
        break
      end

      if limit != -1 and count >= limit
        # exceeded the limit
        puts "Limit exceeded"
        break
                        end
    end
  end
end


def getKeys(name)
    url = "#{$apiurl}getkeys?&name=#{name}"
    return JSON.parse(ScraperWiki.scrape(url))
end

def getData(name, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdata?name=#{name}"
  return generateData(urlbase, limit, offset)
end

def getDataByDate(name, start_date, end_date, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdatabydate?name=#{name}&start_date=#{start_date}&end_date=#{end_date}"
  return generateData(urlbase, limit, offset)
end

def getDataByLocation(name, lat, lng, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdatabydate?name=#{name}&lat=#{lat}&lng=#{lng}"
  return generateData(urlbase, limit, offset)
end

def search(name, filtermap, limit=-1, offset=0)
  res = []
  filtermap.each do |k, v|
    key = CGI.escape k
    value = CGI.escape v
    res.push "#{key},#{value}"
  end
  filter = res.join("|")
  puts filter
  return
  urlbase = "#{$apiurl}search?name=#{name}&filter=#{filter}"
  return generateData(urlbase, limit, offset)
end

getKeys('ben-folds-tour-dates').each do |k|
  puts k
end

getData('ben-folds-tour-dates').each do |d|
  puts d['city']
end
# code to be ported to scraperlibs once complete

# Ruby version of http://scraperwiki.com/views/php-api-access/edit/
# and http://scraperwiki.com/views/python-api-access/edit/ 
# here

require 'generator'
require 'json'
require 'cgi'

$apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"

def generateData(urlbase, limit, offset)
  apilimit = 500
  g = Generator.new do |g|
    count = 0
    while true
      if limit == -1
        step = apilimit
      else
        step = apilimit < (limit - count) ? apilimit : limit - count
      end

      url = "#{urlbase}&limit=#{step}&offset=#{offset+count}"
      records = JSON.parse(ScraperWiki.scrape(url))
      for r in records
        g.yield r
      end

      count += records.length

      if records.length < step
        # run out of records
        puts "Run out of records"
        break
      end

      if limit != -1 and count >= limit
        # exceeded the limit
        puts "Limit exceeded"
        break
                        end
    end
  end
end


def getKeys(name)
    url = "#{$apiurl}getkeys?&name=#{name}"
    return JSON.parse(ScraperWiki.scrape(url))
end

def getData(name, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdata?name=#{name}"
  return generateData(urlbase, limit, offset)
end

def getDataByDate(name, start_date, end_date, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdatabydate?name=#{name}&start_date=#{start_date}&end_date=#{end_date}"
  return generateData(urlbase, limit, offset)
end

def getDataByLocation(name, lat, lng, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdatabydate?name=#{name}&lat=#{lat}&lng=#{lng}"
  return generateData(urlbase, limit, offset)
end

def search(name, filtermap, limit=-1, offset=0)
  res = []
  filtermap.each do |k, v|
    key = CGI.escape k
    value = CGI.escape v
    res.push "#{key},#{value}"
  end
  filter = res.join("|")
  puts filter
  return
  urlbase = "#{$apiurl}search?name=#{name}&filter=#{filter}"
  return generateData(urlbase, limit, offset)
end

getKeys('ben-folds-tour-dates').each do |k|
  puts k
end

getData('ben-folds-tour-dates').each do |d|
  puts d['city']
end
# code to be ported to scraperlibs once complete

# Ruby version of http://scraperwiki.com/views/php-api-access/edit/
# and http://scraperwiki.com/views/python-api-access/edit/ 
# here

require 'generator'
require 'json'
require 'cgi'

$apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"

def generateData(urlbase, limit, offset)
  apilimit = 500
  g = Generator.new do |g|
    count = 0
    while true
      if limit == -1
        step = apilimit
      else
        step = apilimit < (limit - count) ? apilimit : limit - count
      end

      url = "#{urlbase}&limit=#{step}&offset=#{offset+count}"
      records = JSON.parse(ScraperWiki.scrape(url))
      for r in records
        g.yield r
      end

      count += records.length

      if records.length < step
        # run out of records
        puts "Run out of records"
        break
      end

      if limit != -1 and count >= limit
        # exceeded the limit
        puts "Limit exceeded"
        break
                        end
    end
  end
end


def getKeys(name)
    url = "#{$apiurl}getkeys?&name=#{name}"
    return JSON.parse(ScraperWiki.scrape(url))
end

def getData(name, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdata?name=#{name}"
  return generateData(urlbase, limit, offset)
end

def getDataByDate(name, start_date, end_date, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdatabydate?name=#{name}&start_date=#{start_date}&end_date=#{end_date}"
  return generateData(urlbase, limit, offset)
end

def getDataByLocation(name, lat, lng, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdatabydate?name=#{name}&lat=#{lat}&lng=#{lng}"
  return generateData(urlbase, limit, offset)
end

def search(name, filtermap, limit=-1, offset=0)
  res = []
  filtermap.each do |k, v|
    key = CGI.escape k
    value = CGI.escape v
    res.push "#{key},#{value}"
  end
  filter = res.join("|")
  puts filter
  return
  urlbase = "#{$apiurl}search?name=#{name}&filter=#{filter}"
  return generateData(urlbase, limit, offset)
end

getKeys('ben-folds-tour-dates').each do |k|
  puts k
end

getData('ben-folds-tour-dates').each do |d|
  puts d['city']
end
# code to be ported to scraperlibs once complete

# Ruby version of http://scraperwiki.com/views/php-api-access/edit/
# and http://scraperwiki.com/views/python-api-access/edit/ 
# here

require 'generator'
require 'json'
require 'cgi'

$apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"

def generateData(urlbase, limit, offset)
  apilimit = 500
  g = Generator.new do |g|
    count = 0
    while true
      if limit == -1
        step = apilimit
      else
        step = apilimit < (limit - count) ? apilimit : limit - count
      end

      url = "#{urlbase}&limit=#{step}&offset=#{offset+count}"
      records = JSON.parse(ScraperWiki.scrape(url))
      for r in records
        g.yield r
      end

      count += records.length

      if records.length < step
        # run out of records
        puts "Run out of records"
        break
      end

      if limit != -1 and count >= limit
        # exceeded the limit
        puts "Limit exceeded"
        break
                        end
    end
  end
end


def getKeys(name)
    url = "#{$apiurl}getkeys?&name=#{name}"
    return JSON.parse(ScraperWiki.scrape(url))
end

def getData(name, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdata?name=#{name}"
  return generateData(urlbase, limit, offset)
end

def getDataByDate(name, start_date, end_date, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdatabydate?name=#{name}&start_date=#{start_date}&end_date=#{end_date}"
  return generateData(urlbase, limit, offset)
end

def getDataByLocation(name, lat, lng, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdatabydate?name=#{name}&lat=#{lat}&lng=#{lng}"
  return generateData(urlbase, limit, offset)
end

def search(name, filtermap, limit=-1, offset=0)
  res = []
  filtermap.each do |k, v|
    key = CGI.escape k
    value = CGI.escape v
    res.push "#{key},#{value}"
  end
  filter = res.join("|")
  puts filter
  return
  urlbase = "#{$apiurl}search?name=#{name}&filter=#{filter}"
  return generateData(urlbase, limit, offset)
end

getKeys('ben-folds-tour-dates').each do |k|
  puts k
end

getData('ben-folds-tour-dates').each do |d|
  puts d['city']
end
# code to be ported to scraperlibs once complete

# Ruby version of http://scraperwiki.com/views/php-api-access/edit/
# and http://scraperwiki.com/views/python-api-access/edit/ 
# here

require 'generator'
require 'json'
require 'cgi'

$apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"

def generateData(urlbase, limit, offset)
  apilimit = 500
  g = Generator.new do |g|
    count = 0
    while true
      if limit == -1
        step = apilimit
      else
        step = apilimit < (limit - count) ? apilimit : limit - count
      end

      url = "#{urlbase}&limit=#{step}&offset=#{offset+count}"
      records = JSON.parse(ScraperWiki.scrape(url))
      for r in records
        g.yield r
      end

      count += records.length

      if records.length < step
        # run out of records
        puts "Run out of records"
        break
      end

      if limit != -1 and count >= limit
        # exceeded the limit
        puts "Limit exceeded"
        break
                        end
    end
  end
end


def getKeys(name)
    url = "#{$apiurl}getkeys?&name=#{name}"
    return JSON.parse(ScraperWiki.scrape(url))
end

def getData(name, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdata?name=#{name}"
  return generateData(urlbase, limit, offset)
end

def getDataByDate(name, start_date, end_date, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdatabydate?name=#{name}&start_date=#{start_date}&end_date=#{end_date}"
  return generateData(urlbase, limit, offset)
end

def getDataByLocation(name, lat, lng, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdatabydate?name=#{name}&lat=#{lat}&lng=#{lng}"
  return generateData(urlbase, limit, offset)
end

def search(name, filtermap, limit=-1, offset=0)
  res = []
  filtermap.each do |k, v|
    key = CGI.escape k
    value = CGI.escape v
    res.push "#{key},#{value}"
  end
  filter = res.join("|")
  puts filter
  return
  urlbase = "#{$apiurl}search?name=#{name}&filter=#{filter}"
  return generateData(urlbase, limit, offset)
end

getKeys('ben-folds-tour-dates').each do |k|
  puts k
end

getData('ben-folds-tour-dates').each do |d|
  puts d['city']
end
# code to be ported to scraperlibs once complete

# Ruby version of http://scraperwiki.com/views/php-api-access/edit/
# and http://scraperwiki.com/views/python-api-access/edit/ 
# here

require 'generator'
require 'json'
require 'cgi'

$apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"

def generateData(urlbase, limit, offset)
  apilimit = 500
  g = Generator.new do |g|
    count = 0
    while true
      if limit == -1
        step = apilimit
      else
        step = apilimit < (limit - count) ? apilimit : limit - count
      end

      url = "#{urlbase}&limit=#{step}&offset=#{offset+count}"
      records = JSON.parse(ScraperWiki.scrape(url))
      for r in records
        g.yield r
      end

      count += records.length

      if records.length < step
        # run out of records
        puts "Run out of records"
        break
      end

      if limit != -1 and count >= limit
        # exceeded the limit
        puts "Limit exceeded"
        break
                        end
    end
  end
end


def getKeys(name)
    url = "#{$apiurl}getkeys?&name=#{name}"
    return JSON.parse(ScraperWiki.scrape(url))
end

def getData(name, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdata?name=#{name}"
  return generateData(urlbase, limit, offset)
end

def getDataByDate(name, start_date, end_date, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdatabydate?name=#{name}&start_date=#{start_date}&end_date=#{end_date}"
  return generateData(urlbase, limit, offset)
end

def getDataByLocation(name, lat, lng, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdatabydate?name=#{name}&lat=#{lat}&lng=#{lng}"
  return generateData(urlbase, limit, offset)
end

def search(name, filtermap, limit=-1, offset=0)
  res = []
  filtermap.each do |k, v|
    key = CGI.escape k
    value = CGI.escape v
    res.push "#{key},#{value}"
  end
  filter = res.join("|")
  puts filter
  return
  urlbase = "#{$apiurl}search?name=#{name}&filter=#{filter}"
  return generateData(urlbase, limit, offset)
end

getKeys('ben-folds-tour-dates').each do |k|
  puts k
end

getData('ben-folds-tour-dates').each do |d|
  puts d['city']
end
# code to be ported to scraperlibs once complete

# Ruby version of http://scraperwiki.com/views/php-api-access/edit/
# and http://scraperwiki.com/views/python-api-access/edit/ 
# here

require 'generator'
require 'json'
require 'cgi'

$apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"

def generateData(urlbase, limit, offset)
  apilimit = 500
  g = Generator.new do |g|
    count = 0
    while true
      if limit == -1
        step = apilimit
      else
        step = apilimit < (limit - count) ? apilimit : limit - count
      end

      url = "#{urlbase}&limit=#{step}&offset=#{offset+count}"
      records = JSON.parse(ScraperWiki.scrape(url))
      for r in records
        g.yield r
      end

      count += records.length

      if records.length < step
        # run out of records
        puts "Run out of records"
        break
      end

      if limit != -1 and count >= limit
        # exceeded the limit
        puts "Limit exceeded"
        break
                        end
    end
  end
end


def getKeys(name)
    url = "#{$apiurl}getkeys?&name=#{name}"
    return JSON.parse(ScraperWiki.scrape(url))
end

def getData(name, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdata?name=#{name}"
  return generateData(urlbase, limit, offset)
end

def getDataByDate(name, start_date, end_date, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdatabydate?name=#{name}&start_date=#{start_date}&end_date=#{end_date}"
  return generateData(urlbase, limit, offset)
end

def getDataByLocation(name, lat, lng, limit=-1, offset=0)
  urlbase = "#{$apiurl}getdatabydate?name=#{name}&lat=#{lat}&lng=#{lng}"
  return generateData(urlbase, limit, offset)
end

def search(name, filtermap, limit=-1, offset=0)
  res = []
  filtermap.each do |k, v|
    key = CGI.escape k
    value = CGI.escape v
    res.push "#{key},#{value}"
  end
  filter = res.join("|")
  puts filter
  return
  urlbase = "#{$apiurl}search?name=#{name}&filter=#{filter}"
  return generateData(urlbase, limit, offset)
end

getKeys('ben-folds-tour-dates').each do |k|
  puts k
end

getData('ben-folds-tour-dates').each do |d|
  puts d['city']
end

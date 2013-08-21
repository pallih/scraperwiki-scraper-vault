require "rubygems"
require 'open-uri'
require 'json'

def indicator
  "NY.GDP.PCAP.CD"
end

def field_name
  "gdp_per_capita"
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/#{indicator}?format=json&rpp=100&date=" + date
end

def download
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts url(country)
    begin
      results = JSON.parse(open(url(country)) {|f| f.read})
      results = results[1]
      unless !results || results.empty? 
        puts results.inspect
        results.each do |result|
          r = {
            "id" => x,
            "iso2code" => result["country"]["id"],
            "name" => result["country"]["value"],
            "#{field_name}" => result["value"],
            "decimal" => result["decimal"],
            "date" => result["date"]
          }
          puts r.inspect
          ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
          x = x + 1
        end
      end
    rescue Exception => e
      puts "There was a problem downloading #{country} : #{e}"
    end
    
  end
end

download

require "rubygems"
require 'open-uri'
require 'json'

def indicator
  "NY.GDP.PCAP.CD"
end

def field_name
  "gdp_per_capita"
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/#{indicator}?format=json&rpp=100&date=" + date
end

def download
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts url(country)
    begin
      results = JSON.parse(open(url(country)) {|f| f.read})
      results = results[1]
      unless !results || results.empty? 
        puts results.inspect
        results.each do |result|
          r = {
            "id" => x,
            "iso2code" => result["country"]["id"],
            "name" => result["country"]["value"],
            "#{field_name}" => result["value"],
            "decimal" => result["decimal"],
            "date" => result["date"]
          }
          puts r.inspect
          ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
          x = x + 1
        end
      end
    rescue Exception => e
      puts "There was a problem downloading #{country} : #{e}"
    end
    
  end
end

download

require "rubygems"
require 'open-uri'
require 'json'

def indicator
  "NY.GDP.PCAP.CD"
end

def field_name
  "gdp_per_capita"
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/#{indicator}?format=json&rpp=100&date=" + date
end

def download
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts url(country)
    begin
      results = JSON.parse(open(url(country)) {|f| f.read})
      results = results[1]
      unless !results || results.empty? 
        puts results.inspect
        results.each do |result|
          r = {
            "id" => x,
            "iso2code" => result["country"]["id"],
            "name" => result["country"]["value"],
            "#{field_name}" => result["value"],
            "decimal" => result["decimal"],
            "date" => result["date"]
          }
          puts r.inspect
          ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
          x = x + 1
        end
      end
    rescue Exception => e
      puts "There was a problem downloading #{country} : #{e}"
    end
    
  end
end

download

require "rubygems"
require 'open-uri'
require 'json'

def indicator
  "NY.GDP.PCAP.CD"
end

def field_name
  "gdp_per_capita"
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/#{indicator}?format=json&rpp=100&date=" + date
end

def download
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts url(country)
    begin
      results = JSON.parse(open(url(country)) {|f| f.read})
      results = results[1]
      unless !results || results.empty? 
        puts results.inspect
        results.each do |result|
          r = {
            "id" => x,
            "iso2code" => result["country"]["id"],
            "name" => result["country"]["value"],
            "#{field_name}" => result["value"],
            "decimal" => result["decimal"],
            "date" => result["date"]
          }
          puts r.inspect
          ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
          x = x + 1
        end
      end
    rescue Exception => e
      puts "There was a problem downloading #{country} : #{e}"
    end
    
  end
end

download

require "rubygems"
require 'open-uri'
require 'json'

def indicator
  "NY.GDP.PCAP.CD"
end

def field_name
  "gdp_per_capita"
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/#{indicator}?format=json&rpp=100&date=" + date
end

def download
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts url(country)
    begin
      results = JSON.parse(open(url(country)) {|f| f.read})
      results = results[1]
      unless !results || results.empty? 
        puts results.inspect
        results.each do |result|
          r = {
            "id" => x,
            "iso2code" => result["country"]["id"],
            "name" => result["country"]["value"],
            "#{field_name}" => result["value"],
            "decimal" => result["decimal"],
            "date" => result["date"]
          }
          puts r.inspect
          ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
          x = x + 1
        end
      end
    rescue Exception => e
      puts "There was a problem downloading #{country} : #{e}"
    end
    
  end
end

download

require "rubygems"
require 'open-uri'
require 'json'

def indicator
  "NY.GDP.PCAP.CD"
end

def field_name
  "gdp_per_capita"
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/#{indicator}?format=json&rpp=100&date=" + date
end

def download
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts url(country)
    begin
      results = JSON.parse(open(url(country)) {|f| f.read})
      results = results[1]
      unless !results || results.empty? 
        puts results.inspect
        results.each do |result|
          r = {
            "id" => x,
            "iso2code" => result["country"]["id"],
            "name" => result["country"]["value"],
            "#{field_name}" => result["value"],
            "decimal" => result["decimal"],
            "date" => result["date"]
          }
          puts r.inspect
          ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
          x = x + 1
        end
      end
    rescue Exception => e
      puts "There was a problem downloading #{country} : #{e}"
    end
    
  end
end

download

require "rubygems"
require 'open-uri'
require 'json'

def indicator
  "NY.GDP.PCAP.CD"
end

def field_name
  "gdp_per_capita"
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/#{indicator}?format=json&rpp=100&date=" + date
end

def download
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts url(country)
    begin
      results = JSON.parse(open(url(country)) {|f| f.read})
      results = results[1]
      unless !results || results.empty? 
        puts results.inspect
        results.each do |result|
          r = {
            "id" => x,
            "iso2code" => result["country"]["id"],
            "name" => result["country"]["value"],
            "#{field_name}" => result["value"],
            "decimal" => result["decimal"],
            "date" => result["date"]
          }
          puts r.inspect
          ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
          x = x + 1
        end
      end
    rescue Exception => e
      puts "There was a problem downloading #{country} : #{e}"
    end
    
  end
end

download

require "rubygems"
require 'open-uri'
require 'json'

def indicator
  "NY.GDP.PCAP.CD"
end

def field_name
  "gdp_per_capita"
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/#{indicator}?format=json&rpp=100&date=" + date
end

def download
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts url(country)
    begin
      results = JSON.parse(open(url(country)) {|f| f.read})
      results = results[1]
      unless !results || results.empty? 
        puts results.inspect
        results.each do |result|
          r = {
            "id" => x,
            "iso2code" => result["country"]["id"],
            "name" => result["country"]["value"],
            "#{field_name}" => result["value"],
            "decimal" => result["decimal"],
            "date" => result["date"]
          }
          puts r.inspect
          ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
          x = x + 1
        end
      end
    rescue Exception => e
      puts "There was a problem downloading #{country} : #{e}"
    end
    
  end
end

download

require "rubygems"
require 'open-uri'
require 'json'

def indicator
  "NY.GDP.PCAP.CD"
end

def field_name
  "gdp_per_capita"
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/#{indicator}?format=json&rpp=100&date=" + date
end

def download
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts url(country)
    begin
      results = JSON.parse(open(url(country)) {|f| f.read})
      results = results[1]
      unless !results || results.empty? 
        puts results.inspect
        results.each do |result|
          r = {
            "id" => x,
            "iso2code" => result["country"]["id"],
            "name" => result["country"]["value"],
            "#{field_name}" => result["value"],
            "decimal" => result["decimal"],
            "date" => result["date"]
          }
          puts r.inspect
          ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
          x = x + 1
        end
      end
    rescue Exception => e
      puts "There was a problem downloading #{country} : #{e}"
    end
    
  end
end

download

require "rubygems"
require 'open-uri'
require 'json'

def indicator
  "NY.GDP.PCAP.CD"
end

def field_name
  "gdp_per_capita"
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/#{indicator}?format=json&rpp=100&date=" + date
end

def download
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts url(country)
    begin
      results = JSON.parse(open(url(country)) {|f| f.read})
      results = results[1]
      unless !results || results.empty? 
        puts results.inspect
        results.each do |result|
          r = {
            "id" => x,
            "iso2code" => result["country"]["id"],
            "name" => result["country"]["value"],
            "#{field_name}" => result["value"],
            "decimal" => result["decimal"],
            "date" => result["date"]
          }
          puts r.inspect
          ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
          x = x + 1
        end
      end
    rescue Exception => e
      puts "There was a problem downloading #{country} : #{e}"
    end
    
  end
end

download

require "rubygems"
require 'open-uri'
require 'json'

def indicator
  "NY.GDP.PCAP.CD"
end

def field_name
  "gdp_per_capita"
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/#{indicator}?format=json&rpp=100&date=" + date
end

def download
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts url(country)
    begin
      results = JSON.parse(open(url(country)) {|f| f.read})
      results = results[1]
      unless !results || results.empty? 
        puts results.inspect
        results.each do |result|
          r = {
            "id" => x,
            "iso2code" => result["country"]["id"],
            "name" => result["country"]["value"],
            "#{field_name}" => result["value"],
            "decimal" => result["decimal"],
            "date" => result["date"]
          }
          puts r.inspect
          ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
          x = x + 1
        end
      end
    rescue Exception => e
      puts "There was a problem downloading #{country} : #{e}"
    end
    
  end
end

download

require "rubygems"
require 'open-uri'
require 'json'

def indicator
  "NY.GDP.PCAP.CD"
end

def field_name
  "gdp_per_capita"
end

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/#{indicator}?format=json&rpp=100&date=" + date
end

def download
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts url(country)
    begin
      results = JSON.parse(open(url(country)) {|f| f.read})
      results = results[1]
      unless !results || results.empty? 
        puts results.inspect
        results.each do |result|
          r = {
            "id" => x,
            "iso2code" => result["country"]["id"],
            "name" => result["country"]["value"],
            "#{field_name}" => result["value"],
            "decimal" => result["decimal"],
            "date" => result["date"]
          }
          puts r.inspect
          ScraperWiki.save_sqlite(unique_keys=["id"], data=r)
          x = x + 1
        end
      end
    rescue Exception => e
      puts "There was a problem downloading #{country} : #{e}"
    end
    
  end
end

download


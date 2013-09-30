require "rubygems"
require 'open-uri'
require 'json'

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def population_url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/SP.POP.TOTL?format=json&rpp=100&date=" + date
end

def download_population
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts population_url(country)
    begin
      pops = JSON.parse(open(population_url(country)) {|f| f.read})
      pops = pops[1]
      unless !pops || pops.empty? 
        puts pops.inspect
        pops.each do |pop|
          r = {
            "id" => x,
            "iso2code" => pop["country"]["id"],
            "name" => pop["country"]["value"],
            "population" => pop["value"],
            "decimal" => pop["decimal"],
            "date" => pop["date"]
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

download_population

require "rubygems"
require 'open-uri'
require 'json'

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def population_url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/SP.POP.TOTL?format=json&rpp=100&date=" + date
end

def download_population
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts population_url(country)
    begin
      pops = JSON.parse(open(population_url(country)) {|f| f.read})
      pops = pops[1]
      unless !pops || pops.empty? 
        puts pops.inspect
        pops.each do |pop|
          r = {
            "id" => x,
            "iso2code" => pop["country"]["id"],
            "name" => pop["country"]["value"],
            "population" => pop["value"],
            "decimal" => pop["decimal"],
            "date" => pop["date"]
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

download_population

require "rubygems"
require 'open-uri'
require 'json'

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def population_url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/SP.POP.TOTL?format=json&rpp=100&date=" + date
end

def download_population
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts population_url(country)
    begin
      pops = JSON.parse(open(population_url(country)) {|f| f.read})
      pops = pops[1]
      unless !pops || pops.empty? 
        puts pops.inspect
        pops.each do |pop|
          r = {
            "id" => x,
            "iso2code" => pop["country"]["id"],
            "name" => pop["country"]["value"],
            "population" => pop["value"],
            "decimal" => pop["decimal"],
            "date" => pop["date"]
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

download_population

require "rubygems"
require 'open-uri'
require 'json'

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def population_url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/SP.POP.TOTL?format=json&rpp=100&date=" + date
end

def download_population
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts population_url(country)
    begin
      pops = JSON.parse(open(population_url(country)) {|f| f.read})
      pops = pops[1]
      unless !pops || pops.empty? 
        puts pops.inspect
        pops.each do |pop|
          r = {
            "id" => x,
            "iso2code" => pop["country"]["id"],
            "name" => pop["country"]["value"],
            "population" => pop["value"],
            "decimal" => pop["decimal"],
            "date" => pop["date"]
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

download_population

require "rubygems"
require 'open-uri'
require 'json'

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def population_url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/SP.POP.TOTL?format=json&rpp=100&date=" + date
end

def download_population
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts population_url(country)
    begin
      pops = JSON.parse(open(population_url(country)) {|f| f.read})
      pops = pops[1]
      unless !pops || pops.empty? 
        puts pops.inspect
        pops.each do |pop|
          r = {
            "id" => x,
            "iso2code" => pop["country"]["id"],
            "name" => pop["country"]["value"],
            "population" => pop["value"],
            "decimal" => pop["decimal"],
            "date" => pop["date"]
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

download_population

require "rubygems"
require 'open-uri'
require 'json'

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def population_url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/SP.POP.TOTL?format=json&rpp=100&date=" + date
end

def download_population
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts population_url(country)
    begin
      pops = JSON.parse(open(population_url(country)) {|f| f.read})
      pops = pops[1]
      unless !pops || pops.empty? 
        puts pops.inspect
        pops.each do |pop|
          r = {
            "id" => x,
            "iso2code" => pop["country"]["id"],
            "name" => pop["country"]["value"],
            "population" => pop["value"],
            "decimal" => pop["decimal"],
            "date" => pop["date"]
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

download_population

require "rubygems"
require 'open-uri'
require 'json'

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def population_url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/SP.POP.TOTL?format=json&rpp=100&date=" + date
end

def download_population
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts population_url(country)
    begin
      pops = JSON.parse(open(population_url(country)) {|f| f.read})
      pops = pops[1]
      unless !pops || pops.empty? 
        puts pops.inspect
        pops.each do |pop|
          r = {
            "id" => x,
            "iso2code" => pop["country"]["id"],
            "name" => pop["country"]["value"],
            "population" => pop["value"],
            "decimal" => pop["decimal"],
            "date" => pop["date"]
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

download_population

require "rubygems"
require 'open-uri'
require 'json'

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def population_url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/SP.POP.TOTL?format=json&rpp=100&date=" + date
end

def download_population
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts population_url(country)
    begin
      pops = JSON.parse(open(population_url(country)) {|f| f.read})
      pops = pops[1]
      unless !pops || pops.empty? 
        puts pops.inspect
        pops.each do |pop|
          r = {
            "id" => x,
            "iso2code" => pop["country"]["id"],
            "name" => pop["country"]["value"],
            "population" => pop["value"],
            "decimal" => pop["decimal"],
            "date" => pop["date"]
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

download_population

require "rubygems"
require 'open-uri'
require 'json'

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def population_url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/SP.POP.TOTL?format=json&rpp=100&date=" + date
end

def download_population
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts population_url(country)
    begin
      pops = JSON.parse(open(population_url(country)) {|f| f.read})
      pops = pops[1]
      unless !pops || pops.empty? 
        puts pops.inspect
        pops.each do |pop|
          r = {
            "id" => x,
            "iso2code" => pop["country"]["id"],
            "name" => pop["country"]["value"],
            "population" => pop["value"],
            "decimal" => pop["decimal"],
            "date" => pop["date"]
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

download_population

require "rubygems"
require 'open-uri'
require 'json'

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def population_url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/SP.POP.TOTL?format=json&rpp=100&date=" + date
end

def download_population
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts population_url(country)
    begin
      pops = JSON.parse(open(population_url(country)) {|f| f.read})
      pops = pops[1]
      unless !pops || pops.empty? 
        puts pops.inspect
        pops.each do |pop|
          r = {
            "id" => x,
            "iso2code" => pop["country"]["id"],
            "name" => pop["country"]["value"],
            "population" => pop["value"],
            "decimal" => pop["decimal"],
            "date" => pop["date"]
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

download_population

require "rubygems"
require 'open-uri'
require 'json'

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def population_url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/SP.POP.TOTL?format=json&rpp=100&date=" + date
end

def download_population
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts population_url(country)
    begin
      pops = JSON.parse(open(population_url(country)) {|f| f.read})
      pops = pops[1]
      unless !pops || pops.empty? 
        puts pops.inspect
        pops.each do |pop|
          r = {
            "id" => x,
            "iso2code" => pop["country"]["id"],
            "name" => pop["country"]["value"],
            "population" => pop["value"],
            "decimal" => pop["decimal"],
            "date" => pop["date"]
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

download_population

require "rubygems"
require 'open-uri'
require 'json'

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def population_url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/SP.POP.TOTL?format=json&rpp=100&date=" + date
end

def download_population
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts population_url(country)
    begin
      pops = JSON.parse(open(population_url(country)) {|f| f.read})
      pops = pops[1]
      unless !pops || pops.empty? 
        puts pops.inspect
        pops.each do |pop|
          r = {
            "id" => x,
            "iso2code" => pop["country"]["id"],
            "name" => pop["country"]["value"],
            "population" => pop["value"],
            "decimal" => pop["decimal"],
            "date" => pop["date"]
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

download_population

require "rubygems"
require 'open-uri'
require 'json'

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def population_url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/SP.POP.TOTL?format=json&rpp=100&date=" + date
end

def download_population
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts population_url(country)
    begin
      pops = JSON.parse(open(population_url(country)) {|f| f.read})
      pops = pops[1]
      unless !pops || pops.empty? 
        puts pops.inspect
        pops.each do |pop|
          r = {
            "id" => x,
            "iso2code" => pop["country"]["id"],
            "name" => pop["country"]["value"],
            "population" => pop["value"],
            "decimal" => pop["decimal"],
            "date" => pop["date"]
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

download_population

require "rubygems"
require 'open-uri'
require 'json'

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def population_url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/SP.POP.TOTL?format=json&rpp=100&date=" + date
end

def download_population
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts population_url(country)
    begin
      pops = JSON.parse(open(population_url(country)) {|f| f.read})
      pops = pops[1]
      unless !pops || pops.empty? 
        puts pops.inspect
        pops.each do |pop|
          r = {
            "id" => x,
            "iso2code" => pop["country"]["id"],
            "name" => pop["country"]["value"],
            "population" => pop["value"],
            "decimal" => pop["decimal"],
            "date" => pop["date"]
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

download_population

require "rubygems"
require 'open-uri'
require 'json'

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def population_url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/SP.POP.TOTL?format=json&rpp=100&date=" + date
end

def download_population
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts population_url(country)
    begin
      pops = JSON.parse(open(population_url(country)) {|f| f.read})
      pops = pops[1]
      unless !pops || pops.empty? 
        puts pops.inspect
        pops.each do |pop|
          r = {
            "id" => x,
            "iso2code" => pop["country"]["id"],
            "name" => pop["country"]["value"],
            "population" => pop["value"],
            "decimal" => pop["decimal"],
            "date" => pop["date"]
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

download_population

require "rubygems"
require 'open-uri'
require 'json'

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def population_url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/SP.POP.TOTL?format=json&rpp=100&date=" + date
end

def download_population
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts population_url(country)
    begin
      pops = JSON.parse(open(population_url(country)) {|f| f.read})
      pops = pops[1]
      unless !pops || pops.empty? 
        puts pops.inspect
        pops.each do |pop|
          r = {
            "id" => x,
            "iso2code" => pop["country"]["id"],
            "name" => pop["country"]["value"],
            "population" => pop["value"],
            "decimal" => pop["decimal"],
            "date" => pop["date"]
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

download_population

require "rubygems"
require 'open-uri'
require 'json'

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def population_url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/SP.POP.TOTL?format=json&rpp=100&date=" + date
end

def download_population
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts population_url(country)
    begin
      pops = JSON.parse(open(population_url(country)) {|f| f.read})
      pops = pops[1]
      unless !pops || pops.empty? 
        puts pops.inspect
        pops.each do |pop|
          r = {
            "id" => x,
            "iso2code" => pop["country"]["id"],
            "name" => pop["country"]["value"],
            "population" => pop["value"],
            "decimal" => pop["decimal"],
            "date" => pop["date"]
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

download_population

require "rubygems"
require 'open-uri'
require 'json'

def countries_uri
  "http://api.worldbank.org/countries?format=json&per_page=300"
end

def countries
  countries = JSON.parse(open(countries_uri) {|f| f.read})
  countries[1].map do |country|
    country["iso2Code"]
  end.sort
end

def population_url(country, date = "2000:#{Time.now.year}")
  "http://api.worldbank.org/countries/#{country}/indicators/SP.POP.TOTL?format=json&rpp=100&date=" + date
end

def download_population
  ScraperWiki.sqliteexecute("delete from swdata") 
  x = 1
  countries.each do |country|
    puts population_url(country)
    begin
      pops = JSON.parse(open(population_url(country)) {|f| f.read})
      pops = pops[1]
      unless !pops || pops.empty? 
        puts pops.inspect
        pops.each do |pop|
          r = {
            "id" => x,
            "iso2code" => pop["country"]["id"],
            "name" => pop["country"]["value"],
            "population" => pop["value"],
            "decimal" => pop["decimal"],
            "date" => pop["date"]
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

download_population


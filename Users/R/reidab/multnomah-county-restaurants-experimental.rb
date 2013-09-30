# encoding: UTF-8
require 'mechanize'
require 'nokogiri'
require 'json'
require 'uri'
require 'open-uri'

Mechanize.html_parser = Nokogiri::HTML

# Useful ruby utilities for ScraperWiki
module ScraperWookie

  # Provides geocoding functionality
  # Stolen and ported from https://scraperwiki.com/scrapers/geocoding_examples/
  module Geocoder
    def self.load_json(url)
      result_json = open(url).read
      result = JSON.parse(result_json)
    rescue Exception => e
      puts "Error getting geocoder result: #{e.inspect}"
      return nil
    end

    # Geocodes the given address using an Esri Locator service
    # - Currently USA addresses only
    # - Unlimited geocoding using the method below (there are restrictions on batch geocoding: http://www.arcgis.com/home/item.html?id=41e621023bed4304b2a78e9d8b5ce67d )
    # 
    # @param [String] address
    # @return [Hash, nil] a hash with :latitude and :longitude or nil if no result is found
    module Esri
      def self.geocode(address)
        geocode_url = 'http://tasks.arcgisonline.com/ArcGIS/rest/services/Locators/TA_Streets_US_10/GeocodeServer/findAddressCandidates?Single+Line+Input='+URI.escape(address)+'&outFields=&outSR=&f=json'
        results = Geocoder.load_json(geocode_url)

        if result['candidates'] && !result['candidates'].empty? 
          return {
            :latitude => result['candidates'][0]['location']['y'],
            :longitude => result['candidates'][0]['location']['x']
          }
        else
          return nil
        end
      end
    end

    # Geocodes the given address using Google maps
    # - Works world wide (at least in the countries listed here: http://gmaps-samples.googlecode.com/svn/trunk/mapcoverage_filtered.html)
    # - limited to 2,500 requests in a 24 hour period (more details here: http://code.google.com/apis/maps/faq.html#geocoder_limit)
    #
    # @param [String] address
    # @return [Hash, nil] a hash with :latitude and :longitude or nil if no result is found
    module Google
      def self.geocode(address)
        geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+URI.escape(address)+'&sensor=false&output=json'
        result = Geocoder.load_json(geocode_url)

        if result['status'] && result['status'] != 'ZERO_RESULTS'
          return {
            :latitude => result['results'][0]['geometry']['location']['lat'],
            :longitude => result['results'][0]['geometry']['location']['lng']
          }
        else
          return nil
        end
      end
    end
  end

  # A lightweight ORM for the ScraperWiki datastore
  class Model
    def self.keys(*attrs)
      return @keys if attrs.empty? 

      @keys = attrs
      self.class_eval do
        attr_accessor *attrs
      end
    end

    def self.unique_keys(*attrs)
      return @unique_keys if attrs.empty? 
      @key_names = attrs
    end

    def self.table_name(name = nil)
      return @table_name if name.nil? 
      @table_name = name
    end

    def self.find(conditions)
      conditions = conditions.map{|key, value| "#{key} = '#{value}'"}.join(" AND ") if where.is_a?(Hash)
      where_clause = " WHERE #{conditions}" if conditions

      ScraperWiki.select("* FROM #{table_name}#{where_clause}").map{|row| self.new(row)}
    end

    def self.get(which)
      if self.unique_keys.count > 1
        raise(StandardError, "this model has a multi-part primary key, so get is not supported")
      else
        self.find(self.unique_keys.first => which).first
      end
    end

    def self.all
      self.find
    end

    def initialize(attrs = {})
      self.attributes = attrs
    end

    def attributes
      values = self.class.keys.map{|key| self.send(key)}
      Hash[*self.class.keys.zip(values).flatten]
    end

    def attributes=(attr_hash)
      attr_hash.each do |key, value|
        self.send("#{key}=", value)
      end
    end
    
    def save
      nil_out_blank_values
      ScraperWiki.save(self.class.unique_keys, self.attributes, self.class.table_name.to_s)

      # Might need to catch encoding errors…
      # begin
      #   ScraperWiki.save_sqlite(unique_keys=[:id], data=restaurant_data, table_name='restaurants')
      # rescue Encoding::UndefinedConversionError => e
      #   puts "Error saving restaurant: #{restaurant_data.inspect}\n#{e.inspect}"
      # end
    end

    def delete
      ScraperWiki.sqliteexecute("DELETE FROM #{self.class.table_name} WHERE #{self.class.unique_keys.map{|key| "#{key} = '#{self.send(key)}'"}.join(" AND ")}")
    end

  private
    def nil_out_blank_values
      self.attributes.each do |key, value|
        self.send("key=", nil) if value == ''
      end
    end
  end
end


module HealthScraper
  class Scraper
    def initialize
      @agent = Mechanize.new
      return self
    end

    def retry_until_successful(&block)
      begin
        yield
      rescue Timeout::Error => e
        puts "[-!-] Timeout fetching page, retrying..."
        retry
      rescue Net::HTTPInternalServerError => e
        puts "[-!-] 500 Internal Server Error fetching page, retrying..."
        retry
      end
    end

    def fetch_restaurants
      puts "===> Fetching search page"
      search_page = @agent.get("http://www3.multco.us/MCHealthInspect/ListSearch.aspx")

      index_page = search_page.forms.first.submit( search_page.forms.first.buttons.first )

      loop do
        restaurants_on_page = []
        doc = Nokogiri::HTML( index_page.body )
        
        
        break unless index_page.forms.first.buttons.select{|b| b.name == 'Next'}.first
        retry_until_successful do
          index_page = click_button(index_page, 'Next')
        end
break
      end
    end

    def parse_index_row(row)
      return nil unless restaurant_id = row.search('a').count > 0 && row.search('a').attr('href').value.match(/id=(.*)/)

      Restaurant.new(Hash[
        *[:id, :name, :street_address, :city, :zip_code].zip( 
          [restaurant_id[1]] + row.search('td').map{|cell| cell.inner_html.gsub(%r{<.*?>}, "").strip}
        ).flatten
      ])
    end
  end

  class Restaurant < ScraperWookie::Model
    table_name :restaurants
    keys :id, :name, :street_address, :city, :zip_code, :latitude, :longitude
    unique_keys :id

    def save
      geocode unless geocoded?
      super
    end

    def geocoded?
      self.latitude && self.longitude
    end

    def geocode
      if cached_coordinates
        self.latitude = cached_coordinates.latitude
        self.longitude = cached_coordinates.longitude
      else
        return nil if restaurant['street_address'] == "&nbsp;"
        address = "#{street_address}, #{zip_code}"

        if coordinates = ScraperWookie::Geocoder::Google.geocode(address)
          self.latitude = coordinates[:latitude]
          self.longitude = coordinates[:longitude]
        end
      end
    end

    def cached_coordinates
      @cached_coordinates ||= RestaurantCoordinates.find(:restaurant_id => self.id).first

      if @cached_coordinates.latitude.nil? 
        return nil
      else
        return @cached_coordinates
      end
    end
  end

  class RestaurantCoordinates < ScraperWookie::Model
    table_name :restaurant_coordinates
    keys :restaurant_id, :latitude, :longitude
    unique_keys :restaurant_id
  end

end

scraper = HealthScraper::Scraper.new
scraper.fetch_restaurants# encoding: UTF-8
require 'mechanize'
require 'nokogiri'
require 'json'
require 'uri'
require 'open-uri'

Mechanize.html_parser = Nokogiri::HTML

# Useful ruby utilities for ScraperWiki
module ScraperWookie

  # Provides geocoding functionality
  # Stolen and ported from https://scraperwiki.com/scrapers/geocoding_examples/
  module Geocoder
    def self.load_json(url)
      result_json = open(url).read
      result = JSON.parse(result_json)
    rescue Exception => e
      puts "Error getting geocoder result: #{e.inspect}"
      return nil
    end

    # Geocodes the given address using an Esri Locator service
    # - Currently USA addresses only
    # - Unlimited geocoding using the method below (there are restrictions on batch geocoding: http://www.arcgis.com/home/item.html?id=41e621023bed4304b2a78e9d8b5ce67d )
    # 
    # @param [String] address
    # @return [Hash, nil] a hash with :latitude and :longitude or nil if no result is found
    module Esri
      def self.geocode(address)
        geocode_url = 'http://tasks.arcgisonline.com/ArcGIS/rest/services/Locators/TA_Streets_US_10/GeocodeServer/findAddressCandidates?Single+Line+Input='+URI.escape(address)+'&outFields=&outSR=&f=json'
        results = Geocoder.load_json(geocode_url)

        if result['candidates'] && !result['candidates'].empty? 
          return {
            :latitude => result['candidates'][0]['location']['y'],
            :longitude => result['candidates'][0]['location']['x']
          }
        else
          return nil
        end
      end
    end

    # Geocodes the given address using Google maps
    # - Works world wide (at least in the countries listed here: http://gmaps-samples.googlecode.com/svn/trunk/mapcoverage_filtered.html)
    # - limited to 2,500 requests in a 24 hour period (more details here: http://code.google.com/apis/maps/faq.html#geocoder_limit)
    #
    # @param [String] address
    # @return [Hash, nil] a hash with :latitude and :longitude or nil if no result is found
    module Google
      def self.geocode(address)
        geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+URI.escape(address)+'&sensor=false&output=json'
        result = Geocoder.load_json(geocode_url)

        if result['status'] && result['status'] != 'ZERO_RESULTS'
          return {
            :latitude => result['results'][0]['geometry']['location']['lat'],
            :longitude => result['results'][0]['geometry']['location']['lng']
          }
        else
          return nil
        end
      end
    end
  end

  # A lightweight ORM for the ScraperWiki datastore
  class Model
    def self.keys(*attrs)
      return @keys if attrs.empty? 

      @keys = attrs
      self.class_eval do
        attr_accessor *attrs
      end
    end

    def self.unique_keys(*attrs)
      return @unique_keys if attrs.empty? 
      @key_names = attrs
    end

    def self.table_name(name = nil)
      return @table_name if name.nil? 
      @table_name = name
    end

    def self.find(conditions)
      conditions = conditions.map{|key, value| "#{key} = '#{value}'"}.join(" AND ") if where.is_a?(Hash)
      where_clause = " WHERE #{conditions}" if conditions

      ScraperWiki.select("* FROM #{table_name}#{where_clause}").map{|row| self.new(row)}
    end

    def self.get(which)
      if self.unique_keys.count > 1
        raise(StandardError, "this model has a multi-part primary key, so get is not supported")
      else
        self.find(self.unique_keys.first => which).first
      end
    end

    def self.all
      self.find
    end

    def initialize(attrs = {})
      self.attributes = attrs
    end

    def attributes
      values = self.class.keys.map{|key| self.send(key)}
      Hash[*self.class.keys.zip(values).flatten]
    end

    def attributes=(attr_hash)
      attr_hash.each do |key, value|
        self.send("#{key}=", value)
      end
    end
    
    def save
      nil_out_blank_values
      ScraperWiki.save(self.class.unique_keys, self.attributes, self.class.table_name.to_s)

      # Might need to catch encoding errors…
      # begin
      #   ScraperWiki.save_sqlite(unique_keys=[:id], data=restaurant_data, table_name='restaurants')
      # rescue Encoding::UndefinedConversionError => e
      #   puts "Error saving restaurant: #{restaurant_data.inspect}\n#{e.inspect}"
      # end
    end

    def delete
      ScraperWiki.sqliteexecute("DELETE FROM #{self.class.table_name} WHERE #{self.class.unique_keys.map{|key| "#{key} = '#{self.send(key)}'"}.join(" AND ")}")
    end

  private
    def nil_out_blank_values
      self.attributes.each do |key, value|
        self.send("key=", nil) if value == ''
      end
    end
  end
end


module HealthScraper
  class Scraper
    def initialize
      @agent = Mechanize.new
      return self
    end

    def retry_until_successful(&block)
      begin
        yield
      rescue Timeout::Error => e
        puts "[-!-] Timeout fetching page, retrying..."
        retry
      rescue Net::HTTPInternalServerError => e
        puts "[-!-] 500 Internal Server Error fetching page, retrying..."
        retry
      end
    end

    def fetch_restaurants
      puts "===> Fetching search page"
      search_page = @agent.get("http://www3.multco.us/MCHealthInspect/ListSearch.aspx")

      index_page = search_page.forms.first.submit( search_page.forms.first.buttons.first )

      loop do
        restaurants_on_page = []
        doc = Nokogiri::HTML( index_page.body )
        
        
        break unless index_page.forms.first.buttons.select{|b| b.name == 'Next'}.first
        retry_until_successful do
          index_page = click_button(index_page, 'Next')
        end
break
      end
    end

    def parse_index_row(row)
      return nil unless restaurant_id = row.search('a').count > 0 && row.search('a').attr('href').value.match(/id=(.*)/)

      Restaurant.new(Hash[
        *[:id, :name, :street_address, :city, :zip_code].zip( 
          [restaurant_id[1]] + row.search('td').map{|cell| cell.inner_html.gsub(%r{<.*?>}, "").strip}
        ).flatten
      ])
    end
  end

  class Restaurant < ScraperWookie::Model
    table_name :restaurants
    keys :id, :name, :street_address, :city, :zip_code, :latitude, :longitude
    unique_keys :id

    def save
      geocode unless geocoded?
      super
    end

    def geocoded?
      self.latitude && self.longitude
    end

    def geocode
      if cached_coordinates
        self.latitude = cached_coordinates.latitude
        self.longitude = cached_coordinates.longitude
      else
        return nil if restaurant['street_address'] == "&nbsp;"
        address = "#{street_address}, #{zip_code}"

        if coordinates = ScraperWookie::Geocoder::Google.geocode(address)
          self.latitude = coordinates[:latitude]
          self.longitude = coordinates[:longitude]
        end
      end
    end

    def cached_coordinates
      @cached_coordinates ||= RestaurantCoordinates.find(:restaurant_id => self.id).first

      if @cached_coordinates.latitude.nil? 
        return nil
      else
        return @cached_coordinates
      end
    end
  end

  class RestaurantCoordinates < ScraperWookie::Model
    table_name :restaurant_coordinates
    keys :restaurant_id, :latitude, :longitude
    unique_keys :restaurant_id
  end

end

scraper = HealthScraper::Scraper.new
scraper.fetch_restaurants
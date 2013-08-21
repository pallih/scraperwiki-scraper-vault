# Parses stream of power outage information from Consolidated Edison 

#require 'rubygems'
require 'httparty'
require 'json'
require 'hashie'
# require 'pp'

# Class written by Cameron Cundiff, modified by Martin Burch
# Available on Github at https://github.com/ckundo/coned

class Coned
  include HTTParty

  base_uri "http://apps.coned.com"
  format :json

# modified to share directory as an instance variable

  attr_reader :data , :directory

  def fetch
    @directory = self.class.get(
      "/stormcenter_external/stormcenter_externaldata/data/interval_generation_data/metadata.xml", 
      :format => :xml).parsed_response['root']['directory']
      
    url = "/stormcenter_external/stormcenter_externaldata/data/interval_generation_data/#{@directory}/report.js"
    response = JSON.parse( self.class.get(url, :format => :text).parsed_response )
    @data = Hashie::Mash.new( response ).file_data.curr_custs_aff.areas.first
  end

  def bronx
    @data.areas[0]
  end

  def brooklyn
    @data.areas[1]
  end

  def manhattan
    @data.areas[2]
  end

  def queens
    @data.areas[3]
  end

  def staten_island
    @data.areas[4]
  end

  def westchester
    @data.areas[5]
  end

end

# Create a new power outage information object and fetch the data


begin
  c = Coned.new
  c.fetch
  fetchtime = Time.now
  # For each borough (parent area) and neighborhood (child area) save the area's data to database


  c.data.areas.each { |a|

  ScraperWiki::save_sqlite(unique_keys=[], data={"Fetch" => "#{fetchtime}", "Update"=>"#{c.directory}", "Borough" => "#{a.area_name}", "Neighborhood" => "", "Customers_Served" => "#{a.total_custs}", "Estimated_Restoration" => "#{a.etr}","etrmillis" => "#{a.etrmillis}", "Customers_Out" =>"#{a.custs_out}" , "Latitude" => "#{a.latitude}", "Longitude" => "#{a.longitude}"}, table_name="NYC")

    a.areas.each { |b|

  ScraperWiki::save_sqlite(unique_keys=[], data={"Fetch" => "#{fetchtime}", "Update"=>"#{c.directory}", "Borough" => "#{a.area_name}", "Neighborhood" => "#{b.area_name}", "Customers_Served" => "#{b.total_custs}", "Estimated_Restoration" => "#{b.etr}","etrmillis" => "#{b.etrmillis}", "Customers_Out" =>"#{b.custs_out}" , "Latitude" => "#{b.latitude}", "Longitude" => "#{b.longitude}"}, table_name="NYC")   
    }
  }
rescue Timeout::Error
  puts "Timeout waiting for ConEd's servers. We're retrying."
  sleep(5)
  retry
end
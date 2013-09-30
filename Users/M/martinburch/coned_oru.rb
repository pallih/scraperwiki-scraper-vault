require 'scrapers/polylines_library'
require 'httparty'
require 'json'


class ConEdApp
  include HTTParty

  base_uri "http://apps.coned.com"
  format :json
  attr_reader :directory, :response

  def fetchdirectory
    @directory = self.class.get(
    "/stormcenter_external_oru/stormcenter_external_orudata/data/interval_generation_data/metadata.xml",
    :format => :xml).parsed_response['root']['directory']
  end

  def fetchfile (map_block)
    url = "/stormcenter_external_oru/stormcenter_external_orudata/data/interval_generation_data/#{@directory}/outages/#{map_block}.js"
    begin
      response = self.class.get(url, :format => :text)
    rescue Timeout::Error, Errno::ECONNRESET, EOFError
      puts "Timeout or error waiting for response. We're retrying."
      sleep(5)
      retry
    end
      case response.code
        when 200
          puts "Data response"
          response = JSON.parse( response.parsed_response )
          response = response['file_data']
        else
          puts "No response"
          response = []
      end

  end

end

def isunique (item,update)


  statement = "* from Detail WHERE `Update` = \"#{update}\" and Customers_Out = #{item['desc'][0]['cust_a'].delete ','} and Estimated_Restoration = \"#{item['desc'][0]['etr']}\" and Cause = \"#{item['desc'][0]['cause']}\" and Latitude = \"#{item['coords'][0]}\" and Longitude = \"#{item['coords'][1]}\" "
  begin
    data = ScraperWiki::select(statement)
  rescue
    sleep(5)
    retry
  end
  if data.inspect == "[]"
    return true
  else
    return false
  end


end

ScraperWiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `Detail` (`Update` text, `Customers_Out` integer, `Longitude` text, `Latitude` text, `Estimated_Restoration` text,  `Cause` text)")

$a = ConEdApp.new
$a.fetchdirectory

starting_map_quadrants = ["03201011","03023233","03023232"]

@recursion_level = 0

def recursive_parser (file_list)
    puts "We're working on #{file_list}"
    for file_name in file_list
      puts "We're working on #{file_name}"
      result_hash = $a.fetchfile(file_name)
      @new_file_list = []
          for item in result_hash
            update = $a.directory
                puts "We're working on this item: #{item}"
                item['decoded_geom'] = Polylines::Decoder.decode_polyline("#{item['geom'][0]['p']}")
                
                item['coords'] = []                

                item['coords'][0] = item['decoded_geom'].fetch(0).fetch(0)
                item['coords'][1] = item['decoded_geom'].fetch(0).fetch(1)

                item['desc'][0]['cust_a'] = item['desc'][0]['cust_a'].delete ","

                # We can get the coords from the zoomIntoIcon part of HREF, but not on the closest zoom level
                #item['coords'] = item['desc'][0]['href'].split(',')
                #item['coords'][0] = item['coords'][0].delete("zoomIntoIcon(")
                #item['coords'][1] = item['coords'][1].delete(")")

            if item['title'] == "Outage Information" and isunique(item,update) == true
                begin
                  ScraperWiki::save_sqlite(unique_keys=[], data={"Update"=>"#{update}", "Customers_Out" => "#{item['desc'][0]['cust_a'].delete ','}", "Estimated_Restoration" => "#{item['desc'][0]['etr']}", "Cause" => "#{item['desc'][0]['cause']}", "Latitude" => "#{item['coords'][0]}", "Longitude" => "#{item['coords'][1]}"}, table_name="Detail")     
                rescue
                  sleep(5)
                  retry
                end
            end
            if item['title'] == "Area Outages" and @new_file_list == [] # and @recursion_level < 1
              @recursion_level += 1
              for sub_quadrant in 0..3
                new_file_name = "#{file_name}#{sub_quadrant}"
                @new_file_list << new_file_name
              end
            end
          end

      if @new_file_list != []
        recursive_parser(@new_file_list)
      end   

    end
 end

recursive_parser(starting_map_quadrants)
require 'scrapers/polylines_library'
require 'httparty'
require 'json'


class ConEdApp
  include HTTParty

  base_uri "http://apps.coned.com"
  format :json
  attr_reader :directory, :response

  def fetchdirectory
    @directory = self.class.get(
    "/stormcenter_external_oru/stormcenter_external_orudata/data/interval_generation_data/metadata.xml",
    :format => :xml).parsed_response['root']['directory']
  end

  def fetchfile (map_block)
    url = "/stormcenter_external_oru/stormcenter_external_orudata/data/interval_generation_data/#{@directory}/outages/#{map_block}.js"
    begin
      response = self.class.get(url, :format => :text)
    rescue Timeout::Error, Errno::ECONNRESET, EOFError
      puts "Timeout or error waiting for response. We're retrying."
      sleep(5)
      retry
    end
      case response.code
        when 200
          puts "Data response"
          response = JSON.parse( response.parsed_response )
          response = response['file_data']
        else
          puts "No response"
          response = []
      end

  end

end

def isunique (item,update)


  statement = "* from Detail WHERE `Update` = \"#{update}\" and Customers_Out = #{item['desc'][0]['cust_a'].delete ','} and Estimated_Restoration = \"#{item['desc'][0]['etr']}\" and Cause = \"#{item['desc'][0]['cause']}\" and Latitude = \"#{item['coords'][0]}\" and Longitude = \"#{item['coords'][1]}\" "
  begin
    data = ScraperWiki::select(statement)
  rescue
    sleep(5)
    retry
  end
  if data.inspect == "[]"
    return true
  else
    return false
  end


end

ScraperWiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `Detail` (`Update` text, `Customers_Out` integer, `Longitude` text, `Latitude` text, `Estimated_Restoration` text,  `Cause` text)")

$a = ConEdApp.new
$a.fetchdirectory

starting_map_quadrants = ["03201011","03023233","03023232"]

@recursion_level = 0

def recursive_parser (file_list)
    puts "We're working on #{file_list}"
    for file_name in file_list
      puts "We're working on #{file_name}"
      result_hash = $a.fetchfile(file_name)
      @new_file_list = []
          for item in result_hash
            update = $a.directory
                puts "We're working on this item: #{item}"
                item['decoded_geom'] = Polylines::Decoder.decode_polyline("#{item['geom'][0]['p']}")
                
                item['coords'] = []                

                item['coords'][0] = item['decoded_geom'].fetch(0).fetch(0)
                item['coords'][1] = item['decoded_geom'].fetch(0).fetch(1)

                item['desc'][0]['cust_a'] = item['desc'][0]['cust_a'].delete ","

                # We can get the coords from the zoomIntoIcon part of HREF, but not on the closest zoom level
                #item['coords'] = item['desc'][0]['href'].split(',')
                #item['coords'][0] = item['coords'][0].delete("zoomIntoIcon(")
                #item['coords'][1] = item['coords'][1].delete(")")

            if item['title'] == "Outage Information" and isunique(item,update) == true
                begin
                  ScraperWiki::save_sqlite(unique_keys=[], data={"Update"=>"#{update}", "Customers_Out" => "#{item['desc'][0]['cust_a'].delete ','}", "Estimated_Restoration" => "#{item['desc'][0]['etr']}", "Cause" => "#{item['desc'][0]['cause']}", "Latitude" => "#{item['coords'][0]}", "Longitude" => "#{item['coords'][1]}"}, table_name="Detail")     
                rescue
                  sleep(5)
                  retry
                end
            end
            if item['title'] == "Area Outages" and @new_file_list == [] # and @recursion_level < 1
              @recursion_level += 1
              for sub_quadrant in 0..3
                new_file_name = "#{file_name}#{sub_quadrant}"
                @new_file_list << new_file_name
              end
            end
          end

      if @new_file_list != []
        recursive_parser(@new_file_list)
      end   

    end
 end

recursive_parser(starting_map_quadrants)

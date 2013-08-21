require 'httparty'
require 'json'

class ConEdApp
  include HTTParty

  base_uri "http://apps.coned.com"
  format :json
  attr_reader :directory, :response

  def fetchdirectory
    @directory = self.class.get(
    "/stormcenter_external/stormcenter_externaldata/data/interval_generation_data/metadata.xml",
    :format => :xml).parsed_response['root']['directory']
  end

  def fetchfile (map_block)
    url = "/stormcenter_external/stormcenter_externaldata/data/interval_generation_data/#{@directory}/outages/#{map_block}.js"
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
  statement = "* from Detail3 WHERE `Update` = \"#{update}\" and Customers_Out = #{item['desc'][0]['cust_a'].delete ','} and Estimated_Restoration = \"#{item['desc'][0]['etr']}\" and Cause = \"#{item['desc'][0]['cause']}\" and Latitude = \"#{item['geom'][0]['p'][0]}\" and Longitude = \"#{item['geom'][0]['p'][1]}\" "
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

ScraperWiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `Detail3` (`Update` text, `Customers_Out` integer, `Longitude` text, `Latitude` text, `Estimated_Restoration` text,  `Cause` text)")

$a = ConEdApp.new
$a.fetchdirectory

starting_map_quadrants = ["03201011","03023233"]

@recursion_level = 0

def recursive_parser (file_list)
    puts "We're working on #{file_list}"
    for file_name in file_list
      puts "We're working on #{file_name}"
      result_hash = $a.fetchfile(file_name)
      @new_file_list = []
          for item in result_hash
            puts "We're working on this item: #{item}"
            update = $a.directory
            if item['title'] == "Outage Information" and isunique(item,update) == true
                item['desc'][0]['cust_a'] = item['desc'][0]['cust_a'].delete ","
                begin
                  ScraperWiki::save_sqlite(unique_keys=[], data={"Update"=>"#{update}", "Customers_Out" => "#{item['desc'][0]['cust_a'].delete ','}", "Estimated_Restoration" => "#{item['desc'][0]['etr']}", "Cause" => "#{item['desc'][0]['cause']}", "Latitude" => "#{item['geom'][0]['p'][0]}", "Longitude" => "#{item['geom'][0]['p'][1]}"}, table_name="Detail3")   
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
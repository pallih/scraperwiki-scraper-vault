require 'httparty'
require 'rss'
require 'open-uri'

# http://www.lipower.org/stormcenter/outagemap.html

class LIPAApp
  include HTTParty

  base_uri "http://stormcenter.lipower.org"
  format :json
  attr_reader :directory, :response

  def fetchdirectory
    @directory = self.class.get(
    "/data/interval_generation_data/metadata.xml",
    :format => :xml).parsed_response['root']['directory']
  end

  def fetchfile (map_block)
    url = "/data/interval_generation_data/#{@directory}/outages/#{map_block}.xml"
    begin
      response = self.class.get(url, :format => :xml)
    rescue Timeout::Error, Errno::ECONNRESET, EOFError
      puts "Timeout or error waiting for response. We're retrying."
      sleep(5)
      retry
    end
      case response.code
        when 200
          #puts "Data response"
          response = response.parsed_response
          if not response['rss']['item']
            puts "No items in response"
            response = []
          end 
          return response
        else
          #puts "No response"
          response = []
          return response
      end

  end

end

def isunique (item,update)
  statement = "* from Detail2 WHERE `Update` = \"#{update}\" and Customers_Out = \"#{item['cust_a']}\" and Estimated_Restoration = \"#{item['etr']}\" and ID = \"#{item['id']}\" and Location = \"#{item['point']}\" and crew = \"#{item['crew']}\" "
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

ScraperWiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `Detail2` (`Customers_Out` text, `Update` text, `crew` text, `Location` text, `Estimated_Restoration` text, `ID` text)")

$a = LIPAApp.new
$a.fetchdirectory

starting_map_quadrants = ["0320101","0302332","0320110","0302323"]

@recursion_level = 0

def recursive_parser (file_list)
    #puts "We're working on #{file_list}"
    for file_name in file_list
      #puts "We're working on #{file_name}"
      file = $a.fetchfile(file_name)
      @new_file_list = []
      if file != []
          for item in file['rss']['item']
            #puts "We're working on this item: #{item}"
            begin
              detail = item['description'].split('<br/>')
            rescue TypeError
              puts "skipping malformed item"
              puts item
              break
            end
            update = $a.directory
            if detail[0].include? "Outage Information"
                item['id'] = detail[1].sub('<b>ID:</b> ', '')
                item['cust_a'] = detail[2].sub('<b>Customers Affected:</b> ', '')
                item['etr'] = detail[3].sub('<b>Estimated Restoration:</b> ', '')
                item['crew'] = detail[4].sub('<b>Crew Status:</b> ', '')
                if isunique(item,update) == true
                  begin
                    ScraperWiki::save_sqlite(unique_keys=[], data={"Update"=>"#{update}", "Customers_Out" => "#{item['cust_a']}", "Estimated_Restoration" => "#{item['etr']}", "ID" => "#{item['id']}", "Location" => "#{item['point']}", "crew" => "#{item['crew']}"}, table_name="Detail2")   
                  rescue
                    sleep(5)
                    retry
                  end
                end
            end
            if detail[0].include? "Area Outages" and @new_file_list == [] # and @recursion_level < 1
              @recursion_level += 1
              for sub_quadrant in 0..3
                new_file_name = "#{file_name}#{sub_quadrant}"
                @new_file_list << new_file_name
              end
            end
          end

          end

      if @new_file_list != []
        recursive_parser(@new_file_list)
      end   

    end
 end

recursive_parser(starting_map_quadrants)require 'httparty'
require 'rss'
require 'open-uri'

# http://www.lipower.org/stormcenter/outagemap.html

class LIPAApp
  include HTTParty

  base_uri "http://stormcenter.lipower.org"
  format :json
  attr_reader :directory, :response

  def fetchdirectory
    @directory = self.class.get(
    "/data/interval_generation_data/metadata.xml",
    :format => :xml).parsed_response['root']['directory']
  end

  def fetchfile (map_block)
    url = "/data/interval_generation_data/#{@directory}/outages/#{map_block}.xml"
    begin
      response = self.class.get(url, :format => :xml)
    rescue Timeout::Error, Errno::ECONNRESET, EOFError
      puts "Timeout or error waiting for response. We're retrying."
      sleep(5)
      retry
    end
      case response.code
        when 200
          #puts "Data response"
          response = response.parsed_response
          if not response['rss']['item']
            puts "No items in response"
            response = []
          end 
          return response
        else
          #puts "No response"
          response = []
          return response
      end

  end

end

def isunique (item,update)
  statement = "* from Detail2 WHERE `Update` = \"#{update}\" and Customers_Out = \"#{item['cust_a']}\" and Estimated_Restoration = \"#{item['etr']}\" and ID = \"#{item['id']}\" and Location = \"#{item['point']}\" and crew = \"#{item['crew']}\" "
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

ScraperWiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `Detail2` (`Customers_Out` text, `Update` text, `crew` text, `Location` text, `Estimated_Restoration` text, `ID` text)")

$a = LIPAApp.new
$a.fetchdirectory

starting_map_quadrants = ["0320101","0302332","0320110","0302323"]

@recursion_level = 0

def recursive_parser (file_list)
    #puts "We're working on #{file_list}"
    for file_name in file_list
      #puts "We're working on #{file_name}"
      file = $a.fetchfile(file_name)
      @new_file_list = []
      if file != []
          for item in file['rss']['item']
            #puts "We're working on this item: #{item}"
            begin
              detail = item['description'].split('<br/>')
            rescue TypeError
              puts "skipping malformed item"
              puts item
              break
            end
            update = $a.directory
            if detail[0].include? "Outage Information"
                item['id'] = detail[1].sub('<b>ID:</b> ', '')
                item['cust_a'] = detail[2].sub('<b>Customers Affected:</b> ', '')
                item['etr'] = detail[3].sub('<b>Estimated Restoration:</b> ', '')
                item['crew'] = detail[4].sub('<b>Crew Status:</b> ', '')
                if isunique(item,update) == true
                  begin
                    ScraperWiki::save_sqlite(unique_keys=[], data={"Update"=>"#{update}", "Customers_Out" => "#{item['cust_a']}", "Estimated_Restoration" => "#{item['etr']}", "ID" => "#{item['id']}", "Location" => "#{item['point']}", "crew" => "#{item['crew']}"}, table_name="Detail2")   
                  rescue
                    sleep(5)
                    retry
                  end
                end
            end
            if detail[0].include? "Area Outages" and @new_file_list == [] # and @recursion_level < 1
              @recursion_level += 1
              for sub_quadrant in 0..3
                new_file_name = "#{file_name}#{sub_quadrant}"
                @new_file_list << new_file_name
              end
            end
          end

          end

      if @new_file_list != []
        recursive_parser(@new_file_list)
      end   

    end
 end

recursive_parser(starting_map_quadrants)
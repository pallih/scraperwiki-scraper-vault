# encoding: UTF-8
require 'mechanize'
require 'nokogiri'
require 'json'
require 'uri'
require 'open-uri'
Mechanize.html_parser = Nokogiri::HTML

class HealthScraper
  def initialize
    @agent = Mechanize.new
    return self
  end
  
  def fetch_restaurants
    puts "===> Fetching search page"
    search_page = @agent.get("http://www3.multco.us/MCHealthInspect/ListSearch.aspx")
    
    puts "===> "
    index_page = search_page.forms.first.submit( search_page.forms.first.buttons.first )
    
    loop do
      Nokogiri::HTML( index_page.body ).search('#ResultsDataGrid tr').each do |row|
        if restaurant_data = parse_index_row(row)
          begin
            ScraperWiki.save_sqlite(unique_keys=[:id], data=restaurant_data, table_name='restaurants')
          rescue Encoding::UndefinedConversionError => e
            puts "Error saving restaurant: #{restaurant_data.inspect}\n#{e.inspect}"
          end
          puts "Saved: #{restaurant_data[:name]}"
        end
      end
      
      break unless index_page.forms.first.buttons.select{|b| b.name == 'Next'}.first
      
      successful = false
      until successful do
        begin
          index_page = click_button(index_page, 'Next')
        rescue Timeout::Error => e
          puts "[-!-] Timeout fetching page, retrying..."
        rescue Net::HTTPInternalServerError => e
          puts "[-!-] 500 Internal Server Error fetching page, retrying..."
        else
          successful = true
        end
      end
    end
    
    puts "==========================="
  end
  
  def geocode_restaurants
    # ensure that the restaurant_coordinates table exists
    ScraperWiki.save_sqlite(unique_keys=[:restaurant_id], data={:restaurant_id => "0", :latitude => "0", :longitude => "0"}, table_name='restaurant_coordinates')
    ScraperWiki.sqliteexecute('DELETE FROM "restaurant_coordinates" WHERE restaurant_id = "0"')
    ScraperWiki.save_sqlite(unique_keys=[:id], data={:id => "0", :latitude => "0", :longitude => "0"}, table_name='restaurants')
    ScraperWiki.sqliteexecute('DELETE FROM "restaurants" WHERE id = "0"')

    restaurants = ScraperWiki.select("* from restaurants where latitude is null")
    restaurants.each do |restaurant|
      coordinates = ScraperWiki.select("latitude, longitude FROM restaurant_coordinates WHERE restaurant_id = '#{restaurant['id']}'")
      coordinates = coordinates.first
      if coordinates.nil? || coordinates['latitude'].nil? 
        next if restaurant['street_address'] == "&nbsp;"
        address = "#{restaurant['street_address']}, #{restaurant['zip_code']}"
        # geocode_url = 'http://tasks.arcgisonline.com/ArcGIS/rest/services/Locators/TA_Streets_US_10/GeocodeServer/findAddressCandidates?Single+Line+Input='+URI.escape(address)+'&outFields=&outSR=&f=json'
        geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+URI.escape(address)+'&sensor=false&output=json'
        puts geocode_url

        begin
          result_json = open(geocode_url).read
          result = JSON.parse(result_json)
        rescue Exception => e
          puts "Error getting geocoder result: #{e.inspect}"
          next
        end

        if result['candidates'] && !result['candidates'].empty? 
          latitude = result['candidates'][0]['location']['y']
          longitude = result['candidates'][0]['location']['x']
        elsif result['status'] && result['status'] != 'ZERO_RESULTS'
          latitude = result['results'][0]['geometry']['location']['lat']
          longitude = result['results'][0]['geometry']['location']['lng']
        end

        coordinates = {
          :latitude => latitude,
          :longitude => longitude
        }

        ScraperWiki.save_sqlite(unique_keys=[:restaurant_id], data={:restaurant_id => restaurant['id']}.merge(coordinates), table_name='restaurant_coordinates')
      end

      if coordinates['latitude']
        restaurant = restaurant.merge(coordinates)
        puts "Adding coordiantes to: #{restaurant.inspect}"
        ScraperWiki.save_sqlite(unique_keys=[:id], data=restaurant, table_name='restaurants')
      end
    end
  end

  def fetch_all_inspections
    ScraperWiki.attach('multnomah-county-restaurants')
    restaurants = ScraperWiki.select("* from `multnomah-county-restaurants`.restaurants")
    ScraperWiki.save_sqlite(unique_keys=[:id], data=restaurants, table_name='restaurants')

    restaurants.each do |restaurant|
      fetch_inspections_for(restaurant)
    end
  end
  
  def fetch_inspections_for(restaurant)
    url = "http://www3.multco.us/MCHealthInspect/ListSearch.aspx?id=#{restaurant['id']}"
    puts "Fetching inspections for #{restaurant['name']} at #{url}"
    inspection_page = @agent.get(url)

    inspection_count = inspection_page.search('span#Label4 b').text.to_i
    
    if inspection_count > 0
      loop do
        inspection_data = parse_inspection_page(inspection_page)
        inspection_data[:restaurant_id] = restaurant['id']
        notes = inspection_data.delete(:inspection_notes)
        
        ScraperWiki.save_sqlite(unique_keys=[:id],
                                data=inspection_data,
                                table_name='inspections')
        puts "Saved: #{inspection_data.inspect}"

        ScraperWiki.save_sqlite(unique_keys=[:rule, :rule_violations, :violation_comments, :corrective_text, :corrective_comments],
                                data=notes,
                                table_name='inspection_notes')
        puts "Saved: #{notes.inspect}"
        
        break unless inspection_page.forms.first.buttons.select{|b| b.name == 'NextInspection'}.first
        
        successful = false
        until successful do
          begin
            inspection_page = click_button(inspection_page, 'NextInspection')
          rescue Timeout::Error => e
            puts "[-!-] Timeout fetching page, retrying..."
          else
            successful = true
          end
        end
      end
    end
  rescue Net::HTTP::Persistent::Error
    puts "[-!-] Connection Reset fetching page, skipping..."
  rescue Net::HTTPInternalServerError
    puts "[-!-] 500 Internal Server Error fetching page, skipping..."
  end
  
  private
  def click_button(page, button_name)
    page.forms.first.submit(
      page.forms.first.buttons.select{|b| b.name == button_name}.first
    )
  end
  
  def parse_index_row(row)
    return nil unless restaurant_id = row.search('a').count > 0 && row.search('a').attr('href').value.match(/id=(.*)/)

    Hash[
      *[:id, :name, :street_address, :city, :zip_code, :latitude, :longitude].zip( 
        [restaurant_id[1]] + row.search('td').map{|cell| cell.inner_html.gsub(%r{<.*?>}, "").strip} +[nil,nil]
      ).flatten
    ]
  end
  
  def parse_inspection_page(inspection_page)
    doc = Nokogiri::HTML(inspection_page.body)
    rows = doc.search('#DetailsView table tr').map{|row| 
            row.search('td, th').map{|cell| 
                cell.inner_text.gsub(/\u00a0/,'').strip 
              }
            }
    summary = Hash[*rows[0].zip(rows[1]).flatten]
    
    notes = []
    rows.each_with_index do |row, i|
      if row.sort == ["", "Law/Rule", "Rule Violations", "Violation Comments"].sort
        notes << {
          :rule => rows[i+1][0],
          :rule_violations => rows[i+1][1],
          :violation_comments => rows[i+1][2],
          :corrective_text => rows[i+3][1],
          :corrective_comments => rows[i+3][1]
        }
      end
    end
  
    return {
      :id => summary["Inspection#"],
      :type => summary["Type"],
      :date => Date.strptime(summary["Date"], "%m/%d/%Y").to_s,
      :score => summary["Final Score"].to_i > 0 ? summary["Final Score"].to_i : nil,
      :inspection_notes => notes
    }
  end
end

HealthScraper.new.fetch_all_inspections
# encoding: UTF-8
require 'mechanize'
require 'nokogiri'
require 'json'
require 'uri'
require 'open-uri'
Mechanize.html_parser = Nokogiri::HTML

class HealthScraper
  def initialize
    @agent = Mechanize.new
    return self
  end
  
  def fetch_restaurants
    puts "===> Fetching search page"
    search_page = @agent.get("http://www3.multco.us/MCHealthInspect/ListSearch.aspx")
    
    puts "===> "
    index_page = search_page.forms.first.submit( search_page.forms.first.buttons.first )
    
    loop do
      Nokogiri::HTML( index_page.body ).search('#ResultsDataGrid tr').each do |row|
        if restaurant_data = parse_index_row(row)
          begin
            ScraperWiki.save_sqlite(unique_keys=[:id], data=restaurant_data, table_name='restaurants')
          rescue Encoding::UndefinedConversionError => e
            puts "Error saving restaurant: #{restaurant_data.inspect}\n#{e.inspect}"
          end
          puts "Saved: #{restaurant_data[:name]}"
        end
      end
      
      break unless index_page.forms.first.buttons.select{|b| b.name == 'Next'}.first
      
      successful = false
      until successful do
        begin
          index_page = click_button(index_page, 'Next')
        rescue Timeout::Error => e
          puts "[-!-] Timeout fetching page, retrying..."
        rescue Net::HTTPInternalServerError => e
          puts "[-!-] 500 Internal Server Error fetching page, retrying..."
        else
          successful = true
        end
      end
    end
    
    puts "==========================="
  end
  
  def geocode_restaurants
    # ensure that the restaurant_coordinates table exists
    ScraperWiki.save_sqlite(unique_keys=[:restaurant_id], data={:restaurant_id => "0", :latitude => "0", :longitude => "0"}, table_name='restaurant_coordinates')
    ScraperWiki.sqliteexecute('DELETE FROM "restaurant_coordinates" WHERE restaurant_id = "0"')
    ScraperWiki.save_sqlite(unique_keys=[:id], data={:id => "0", :latitude => "0", :longitude => "0"}, table_name='restaurants')
    ScraperWiki.sqliteexecute('DELETE FROM "restaurants" WHERE id = "0"')

    restaurants = ScraperWiki.select("* from restaurants where latitude is null")
    restaurants.each do |restaurant|
      coordinates = ScraperWiki.select("latitude, longitude FROM restaurant_coordinates WHERE restaurant_id = '#{restaurant['id']}'")
      coordinates = coordinates.first
      if coordinates.nil? || coordinates['latitude'].nil? 
        next if restaurant['street_address'] == "&nbsp;"
        address = "#{restaurant['street_address']}, #{restaurant['zip_code']}"
        # geocode_url = 'http://tasks.arcgisonline.com/ArcGIS/rest/services/Locators/TA_Streets_US_10/GeocodeServer/findAddressCandidates?Single+Line+Input='+URI.escape(address)+'&outFields=&outSR=&f=json'
        geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+URI.escape(address)+'&sensor=false&output=json'
        puts geocode_url

        begin
          result_json = open(geocode_url).read
          result = JSON.parse(result_json)
        rescue Exception => e
          puts "Error getting geocoder result: #{e.inspect}"
          next
        end

        if result['candidates'] && !result['candidates'].empty? 
          latitude = result['candidates'][0]['location']['y']
          longitude = result['candidates'][0]['location']['x']
        elsif result['status'] && result['status'] != 'ZERO_RESULTS'
          latitude = result['results'][0]['geometry']['location']['lat']
          longitude = result['results'][0]['geometry']['location']['lng']
        end

        coordinates = {
          :latitude => latitude,
          :longitude => longitude
        }

        ScraperWiki.save_sqlite(unique_keys=[:restaurant_id], data={:restaurant_id => restaurant['id']}.merge(coordinates), table_name='restaurant_coordinates')
      end

      if coordinates['latitude']
        restaurant = restaurant.merge(coordinates)
        puts "Adding coordiantes to: #{restaurant.inspect}"
        ScraperWiki.save_sqlite(unique_keys=[:id], data=restaurant, table_name='restaurants')
      end
    end
  end

  def fetch_all_inspections
    ScraperWiki.attach('multnomah-county-restaurants')
    restaurants = ScraperWiki.select("* from `multnomah-county-restaurants`.restaurants")
    ScraperWiki.save_sqlite(unique_keys=[:id], data=restaurants, table_name='restaurants')

    restaurants.each do |restaurant|
      fetch_inspections_for(restaurant)
    end
  end
  
  def fetch_inspections_for(restaurant)
    url = "http://www3.multco.us/MCHealthInspect/ListSearch.aspx?id=#{restaurant['id']}"
    puts "Fetching inspections for #{restaurant['name']} at #{url}"
    inspection_page = @agent.get(url)

    inspection_count = inspection_page.search('span#Label4 b').text.to_i
    
    if inspection_count > 0
      loop do
        inspection_data = parse_inspection_page(inspection_page)
        inspection_data[:restaurant_id] = restaurant['id']
        notes = inspection_data.delete(:inspection_notes)
        
        ScraperWiki.save_sqlite(unique_keys=[:id],
                                data=inspection_data,
                                table_name='inspections')
        puts "Saved: #{inspection_data.inspect}"

        ScraperWiki.save_sqlite(unique_keys=[:rule, :rule_violations, :violation_comments, :corrective_text, :corrective_comments],
                                data=notes,
                                table_name='inspection_notes')
        puts "Saved: #{notes.inspect}"
        
        break unless inspection_page.forms.first.buttons.select{|b| b.name == 'NextInspection'}.first
        
        successful = false
        until successful do
          begin
            inspection_page = click_button(inspection_page, 'NextInspection')
          rescue Timeout::Error => e
            puts "[-!-] Timeout fetching page, retrying..."
          else
            successful = true
          end
        end
      end
    end
  rescue Net::HTTP::Persistent::Error
    puts "[-!-] Connection Reset fetching page, skipping..."
  rescue Net::HTTPInternalServerError
    puts "[-!-] 500 Internal Server Error fetching page, skipping..."
  end
  
  private
  def click_button(page, button_name)
    page.forms.first.submit(
      page.forms.first.buttons.select{|b| b.name == button_name}.first
    )
  end
  
  def parse_index_row(row)
    return nil unless restaurant_id = row.search('a').count > 0 && row.search('a').attr('href').value.match(/id=(.*)/)

    Hash[
      *[:id, :name, :street_address, :city, :zip_code, :latitude, :longitude].zip( 
        [restaurant_id[1]] + row.search('td').map{|cell| cell.inner_html.gsub(%r{<.*?>}, "").strip} +[nil,nil]
      ).flatten
    ]
  end
  
  def parse_inspection_page(inspection_page)
    doc = Nokogiri::HTML(inspection_page.body)
    rows = doc.search('#DetailsView table tr').map{|row| 
            row.search('td, th').map{|cell| 
                cell.inner_text.gsub(/\u00a0/,'').strip 
              }
            }
    summary = Hash[*rows[0].zip(rows[1]).flatten]
    
    notes = []
    rows.each_with_index do |row, i|
      if row.sort == ["", "Law/Rule", "Rule Violations", "Violation Comments"].sort
        notes << {
          :rule => rows[i+1][0],
          :rule_violations => rows[i+1][1],
          :violation_comments => rows[i+1][2],
          :corrective_text => rows[i+3][1],
          :corrective_comments => rows[i+3][1]
        }
      end
    end
  
    return {
      :id => summary["Inspection#"],
      :type => summary["Type"],
      :date => Date.strptime(summary["Date"], "%m/%d/%Y").to_s,
      :score => summary["Final Score"].to_i > 0 ? summary["Final Score"].to_i : nil,
      :inspection_notes => notes
    }
  end
end

HealthScraper.new.fetch_all_inspections

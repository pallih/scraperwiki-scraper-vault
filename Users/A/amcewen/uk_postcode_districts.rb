# Scraper to extract all of the first-half postcode options from the list on Wikipedia
require 'nokogiri'

area_url = "http://en.wikipedia.org/wiki/List_of_postcode_areas_in_the_United_Kingdom"
parsed_area_url = URI.parse(area_url)
area_page = ScraperWiki.scrape(area_url)
area_doc = Nokogiri::HTML(area_page)

@record_count = 0

# Get all the postcode areas (e.g. L, WA, EC)
area_doc.css("table.wikitable a").each do |link|
  if !link['title'].nil? && link['title'].match(/postcode area/)
    puts link['href']
    # Now pull down the page with all the districts for this area
    district_page = ScraperWiki.scrape(parsed_area_url.merge(link['href']).to_s)
    district_doc = Nokogiri::HTML(district_page)
    district_doc.css("table.wikitable tr").each do |district|
      if district.css("th").size == 1
        # It's one of the rows (the main header has multiple <th> elements)
        record = { 'postcode_district' => district.css("th").inner_text.gsub(/\[.*\]/, "").gsub(/\(.*\)/, "").gsub(/\–/, "-").strip }
        if record['postcode_district'].match(/^\w\w?\d\d?\w?$/)
          if district.css("td").size >= 2
            # We've got all the other info we'd want (for some, e.g. S19, there isn't that info available)
            record['postal_town'] = district.css("td")[0].inner_text
            record['coverage'] = district.css("td")[1].inner_text
          end
          @record_count = @record_count + 1
          puts "#{@record_count}: "+record['postcode_district']
          ScraperWiki.save_sqlite(['postcode_district'], record, "uk_postcode_districts")
        elsif record['postcode_district'].match(/^\w\w?\d\d?\-\w\w?\d\d?$/)
          # Some postcodes (e.g. B1-B4) are of the grouped with a -
          match_info = record['postcode_district'].match(/^(\w\w?)(\d\d?)\-\w\w?(\d\d?)$/)
          (match_info[2]..match_info[3]).each do |num|
            record['postcode_district'] = match_info[1]+num.to_s
            if district.css("td").size >= 2
               # We've got all the other info we'd want (for some, e.g. S19, there isn't that info available)
               record['postal_town'] = district.css("td")[0].inner_text
               record['coverage'] = district.css("td")[1].inner_text
            end
            @record_count = @record_count + 1
            puts "#{@record_count}: "+record['postcode_district']
            ScraperWiki.save_sqlite(['postcode_district'], record, "uk_postcode_districts")
          end
        elsif record['postcode_district'].match(/^KA/)
          puts "Skipping KA codes"
        elsif record['postcode_district'] != ""
          raise "Error: "+record['postcode_district']
        end
      end
    end
  end
end

# Now add the KAxx codes we skipped earlier (because the Wikipedia page for it isn't formatted very well and this is just easier)
(1..30).each do |district|
  @record_count = @record_count + 1
  record = { 'postcode_district' => "KA#{district}" }
  puts "#{@record_count}: "+record['postcode_district']
  ScraperWiki.save_sqlite(['postcode_district'], record, "uk_postcode_districts")
end

# Scraper to extract all of the first-half postcode options from the list on Wikipedia
require 'nokogiri'

area_url = "http://en.wikipedia.org/wiki/List_of_postcode_areas_in_the_United_Kingdom"
parsed_area_url = URI.parse(area_url)
area_page = ScraperWiki.scrape(area_url)
area_doc = Nokogiri::HTML(area_page)

@record_count = 0

# Get all the postcode areas (e.g. L, WA, EC)
area_doc.css("table.wikitable a").each do |link|
  if !link['title'].nil? && link['title'].match(/postcode area/)
    puts link['href']
    # Now pull down the page with all the districts for this area
    district_page = ScraperWiki.scrape(parsed_area_url.merge(link['href']).to_s)
    district_doc = Nokogiri::HTML(district_page)
    district_doc.css("table.wikitable tr").each do |district|
      if district.css("th").size == 1
        # It's one of the rows (the main header has multiple <th> elements)
        record = { 'postcode_district' => district.css("th").inner_text.gsub(/\[.*\]/, "").gsub(/\(.*\)/, "").gsub(/\–/, "-").strip }
        if record['postcode_district'].match(/^\w\w?\d\d?\w?$/)
          if district.css("td").size >= 2
            # We've got all the other info we'd want (for some, e.g. S19, there isn't that info available)
            record['postal_town'] = district.css("td")[0].inner_text
            record['coverage'] = district.css("td")[1].inner_text
          end
          @record_count = @record_count + 1
          puts "#{@record_count}: "+record['postcode_district']
          ScraperWiki.save_sqlite(['postcode_district'], record, "uk_postcode_districts")
        elsif record['postcode_district'].match(/^\w\w?\d\d?\-\w\w?\d\d?$/)
          # Some postcodes (e.g. B1-B4) are of the grouped with a -
          match_info = record['postcode_district'].match(/^(\w\w?)(\d\d?)\-\w\w?(\d\d?)$/)
          (match_info[2]..match_info[3]).each do |num|
            record['postcode_district'] = match_info[1]+num.to_s
            if district.css("td").size >= 2
               # We've got all the other info we'd want (for some, e.g. S19, there isn't that info available)
               record['postal_town'] = district.css("td")[0].inner_text
               record['coverage'] = district.css("td")[1].inner_text
            end
            @record_count = @record_count + 1
            puts "#{@record_count}: "+record['postcode_district']
            ScraperWiki.save_sqlite(['postcode_district'], record, "uk_postcode_districts")
          end
        elsif record['postcode_district'].match(/^KA/)
          puts "Skipping KA codes"
        elsif record['postcode_district'] != ""
          raise "Error: "+record['postcode_district']
        end
      end
    end
  end
end

# Now add the KAxx codes we skipped earlier (because the Wikipedia page for it isn't formatted very well and this is just easier)
(1..30).each do |district|
  @record_count = @record_count + 1
  record = { 'postcode_district' => "KA#{district}" }
  puts "#{@record_count}: "+record['postcode_district']
  ScraperWiki.save_sqlite(['postcode_district'], record, "uk_postcode_districts")
end


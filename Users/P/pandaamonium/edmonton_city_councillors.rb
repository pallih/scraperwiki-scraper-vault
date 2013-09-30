require 'open-uri'
require 'nokogiri'
require 'json'

class Nokogiri::XML::Node
  def normalized_text
    self.text.to_s.chomp.strip
  end
end

class EdmontonScrapper
  BASE_URL   = 'http://www.edmonton.ca'
  SOURCE_URL = BASE_URL + '/city_government/city_organization/city-councillors.aspx'
  MAYOR_URL  = BASE_URL + '/city_government/city_organization/the-mayor.aspx'

  class << self
    def scrap_data(&block)
      yield mayor_data
      councillor_data { |data| yield data }
    end

    private

    def mayor_data
      mayor_doc = Nokogiri::HTML(open(MAYOR_URL)).at_css('#contentArea')

      photo = mayor_doc.at_css("h1 + p img")
      photo_url = BASE_URL + photo.attr('src')
      name = photo.attr('title').gsub(/^.*mayor\s*/i, '')

      data = {
        'name'           => name,
        'source_url'     => SOURCE_URL,
        'photo_url'      => photo_url,
        'boundary_url'   => '/boundaries/census-subdivisions/4811061/',
        'district_id'    => 0,
        'elected_office' => "Mayor",
        'url'            => MAYOR_URL,
        'offices' => [
          {
            'postal' => scrap_address(mayor_doc.at_css("address p")),
          },
        ]
      }

      data_plus_contact(data, mayor_doc.css('table.contactListing tr'))
    end

    def councillor_data(&block)
      Nokogiri::HTML(open(SOURCE_URL)).css('#contentArea table[height]').each do |rep_box|
        [:left, :right].each do |side|
          details_url, name, office, photo_url = scrap_list_page(rep_box, side)

          data = {
            'name'           => name,
            'source_url'     => SOURCE_URL,
            'photo_url'      => photo_url,
            'district_name'  => office,
            'district_id'    => office.match(/\d+/)[0],
            'elected_office' => "Councillor",
            'url'            => details_url,
          }.merge(councillor_details(details_url))

          yield data
        end
      end
    end

    def scrap_list_page(rep_box, side)
      idx = side.eql?(:left) ? 1 : 2

      details_link = rep_box.at_css("tr[3] td[#{idx}] a")
      details_url  = BASE_URL + details_link.attr('href')
      name         = details_link.normalized_text
      office       = rep_box.at_css("tr[1] th[#{idx}] h2").normalized_text
      photo_url    = BASE_URL + rep_box.at_css("tr[2] td[#{idx}] a img").attr('src')

      return details_url, name, office, photo_url
    end

    def councillor_details(details_url)
      details_doc = Nokogiri::HTML(open(details_url))

      data = {
        'offices' => [
          {
            'postal' => scrap_address(details_doc.at_css('#contentArea address p')),
          },
        ]
      }

      data_plus_contact(data, details_doc.css('#contentArea table.contactListing tr'))
    end

    def scrap_address(address_section)
      address_parts = address_section.children
      [
        address_parts[0].normalized_text, # Suite
        address_parts[2].normalized_text, # Street
        address_parts[4].normalized_text, # city, region, zip code (not always)
        (address_parts[6].normalized_text unless address_parts[6].nil?), # if provided, contains zip code
      ].compact.join("\n")
    end

    def data_plus_contact(data, contact_rows)
      contact_rows.each do |row|
        case row.at_css('th').text
          when /phone/i
            data['offices'].first['tel'] = row.at_css('td').children.first.normalized_text
          when /fax/i
            data['offices'].first['fax'] = row.at_css('td').normalized_text
          when /email/i
            data['email'] = row.at_css('td').normalized_text
        end
      end

      data['offices'] = data['offices'].to_json
      data
    end
  end
end

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

EdmontonScrapper.scrap_data do |data|
  ScraperWiki.save_sqlite(['district_id'], data)
end
require 'open-uri'
require 'nokogiri'
require 'json'

class Nokogiri::XML::Node
  def normalized_text
    self.text.to_s.chomp.strip
  end
end

class EdmontonScrapper
  BASE_URL   = 'http://www.edmonton.ca'
  SOURCE_URL = BASE_URL + '/city_government/city_organization/city-councillors.aspx'
  MAYOR_URL  = BASE_URL + '/city_government/city_organization/the-mayor.aspx'

  class << self
    def scrap_data(&block)
      yield mayor_data
      councillor_data { |data| yield data }
    end

    private

    def mayor_data
      mayor_doc = Nokogiri::HTML(open(MAYOR_URL)).at_css('#contentArea')

      photo = mayor_doc.at_css("h1 + p img")
      photo_url = BASE_URL + photo.attr('src')
      name = photo.attr('title').gsub(/^.*mayor\s*/i, '')

      data = {
        'name'           => name,
        'source_url'     => SOURCE_URL,
        'photo_url'      => photo_url,
        'boundary_url'   => '/boundaries/census-subdivisions/4811061/',
        'district_id'    => 0,
        'elected_office' => "Mayor",
        'url'            => MAYOR_URL,
        'offices' => [
          {
            'postal' => scrap_address(mayor_doc.at_css("address p")),
          },
        ]
      }

      data_plus_contact(data, mayor_doc.css('table.contactListing tr'))
    end

    def councillor_data(&block)
      Nokogiri::HTML(open(SOURCE_URL)).css('#contentArea table[height]').each do |rep_box|
        [:left, :right].each do |side|
          details_url, name, office, photo_url = scrap_list_page(rep_box, side)

          data = {
            'name'           => name,
            'source_url'     => SOURCE_URL,
            'photo_url'      => photo_url,
            'district_name'  => office,
            'district_id'    => office.match(/\d+/)[0],
            'elected_office' => "Councillor",
            'url'            => details_url,
          }.merge(councillor_details(details_url))

          yield data
        end
      end
    end

    def scrap_list_page(rep_box, side)
      idx = side.eql?(:left) ? 1 : 2

      details_link = rep_box.at_css("tr[3] td[#{idx}] a")
      details_url  = BASE_URL + details_link.attr('href')
      name         = details_link.normalized_text
      office       = rep_box.at_css("tr[1] th[#{idx}] h2").normalized_text
      photo_url    = BASE_URL + rep_box.at_css("tr[2] td[#{idx}] a img").attr('src')

      return details_url, name, office, photo_url
    end

    def councillor_details(details_url)
      details_doc = Nokogiri::HTML(open(details_url))

      data = {
        'offices' => [
          {
            'postal' => scrap_address(details_doc.at_css('#contentArea address p')),
          },
        ]
      }

      data_plus_contact(data, details_doc.css('#contentArea table.contactListing tr'))
    end

    def scrap_address(address_section)
      address_parts = address_section.children
      [
        address_parts[0].normalized_text, # Suite
        address_parts[2].normalized_text, # Street
        address_parts[4].normalized_text, # city, region, zip code (not always)
        (address_parts[6].normalized_text unless address_parts[6].nil?), # if provided, contains zip code
      ].compact.join("\n")
    end

    def data_plus_contact(data, contact_rows)
      contact_rows.each do |row|
        case row.at_css('th').text
          when /phone/i
            data['offices'].first['tel'] = row.at_css('td').children.first.normalized_text
          when /fax/i
            data['offices'].first['fax'] = row.at_css('td').normalized_text
          when /email/i
            data['email'] = row.at_css('td').normalized_text
        end
      end

      data['offices'] = data['offices'].to_json
      data
    end
  end
end

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

EdmontonScrapper.scrap_data do |data|
  ScraperWiki.save_sqlite(['district_id'], data)
end

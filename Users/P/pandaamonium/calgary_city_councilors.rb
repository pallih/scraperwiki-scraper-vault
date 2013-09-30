require 'open-uri'
require 'nokogiri'
require 'mechanize'
require 'json'

class Nokogiri::XML::Node
  def normalized_text
    self.text.to_s.chomp.strip
  end
end

class CalgaryScrapper
  BASE_URL   = 'http://www.calgary.ca'
  SOURCE_URL = BASE_URL + '/General/Pages/Calgary-City-Council.aspx'

  class << self
    def scrap_data(&block)
      Nokogiri::HTML(open(SOURCE_URL)).css('.ms-rtestate-read.ms-rte-wpbox').each do |rep_box|
        details_link = rep_box.at_css('.cocis-image-caption a')
        name         = details_link.normalized_text
        office       = rep_box.at_css('.cocis-image-caption strong').normalized_text
        photo_url    = BASE_URL + rep_box.at_css('.cocis-image a img').attr('src')

        data = {
          'name'       => name,
          'source_url' => SOURCE_URL,
          'photo_url'  => photo_url,
        }

        case office
          when /(\w+) (\d+) (\w*)/i
            district_title, district_id, elected_office = [$1, $2, $3]
            yield data.merge(alderman_details(details_link, district_title, district_id, elected_office))
          when /mayor/i
            yield data.merge(mayor_details(details_link, office))
          else
            fail "Office string not matched to any pattern"
        end
      end
    end

    private

    def alderman_details(details_link, district_title, district_id, elected_office)
      details_url = BASE_URL + details_link.attr('href')
      details_doc = Nokogiri::HTML(open(details_url))

      if contact_html = details_doc.at_css('.cocis-rte-Element-DIV-Sidebar-Right')
        contact_info_parts = contact_html.children.map(&:normalized_text)
        postal_info = "#{contact_info_parts[2]}\n#{contact_info_parts[4]}"
        phone_info  = contact_info_parts.find{|x| x[/phone:\s+/i]}.gsub(/phone:\s+/i, '')
        fax_info    = contact_info_parts.find{|x| x[/fax:\s+/i]}.gsub(/fax:\s+/i, '')
      else
        contact_html = details_doc.at_css('#contactInfo')
        contact_info_parts = contact_html.children.select{ |e| e.name == 'p' }.map(&:children)
        postal_info = "#{contact_info_parts[0][0]}\n#{contact_info_parts[0][2]}"
        phones = contact_info_parts[1].select{|x| x.to_s.gsub(/\D/, '').size == 10}
        phone_info  = phones[0].to_s.strip
        fax_info    = phones[1].to_s.strip
      end

      {
        'district_name'  => "#{district_title} #{district_id}",
        'district_id'    => district_id.to_i,
        'elected_office' => elected_office,
        'url'            => details_url,
        'offices'        => [
          {
            'postal' => postal_info,
            'tel'    => phone_info,
            'fax'    => fax_info,
          },
        ].to_json
      }
    end

    def mayor_details(details_link, office)
      agent              = Mechanize.new
      details_url        = details_link.attr('href')
      mayor_contact_page = agent.get(details_url).link_with(:text => /contact us/i).click
      details_doc        = Nokogiri::HTML(mayor_contact_page.body)

      contact_info       = details_doc.at_css(".alt-contact-holder")
      contact_info_parts = contact_info.children

      {
        'district_id'    => 0,
        'boundary_url'   => '/boundaries/census-subdivisions/4806016/',
        'elected_office' => office,
        'url'            => details_url,
        'email'          => contact_info.css('a[href^=mailto]').attr('href').to_s.gsub(/^mailto:/, ''),
        'offices'        => [
          {
            'postal' => [
              contact_info_parts[10].normalized_text, # office
              contact_info_parts[12].normalized_text, # P.O. Box
              contact_info_parts[14].normalized_text, # city, region, postal code
            ].join("\n"),
            'tel'    => contact_info_parts[2].normalized_text,
            'fax'    => contact_info_parts[5].normalized_text,
          },
        ].to_json
      }
    end
  end
end

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

CalgaryScrapper.scrap_data do |data|
  ScraperWiki.save_sqlite(['district_id'], data)
end
require 'open-uri'
require 'nokogiri'
require 'mechanize'
require 'json'

class Nokogiri::XML::Node
  def normalized_text
    self.text.to_s.chomp.strip
  end
end

class CalgaryScrapper
  BASE_URL   = 'http://www.calgary.ca'
  SOURCE_URL = BASE_URL + '/General/Pages/Calgary-City-Council.aspx'

  class << self
    def scrap_data(&block)
      Nokogiri::HTML(open(SOURCE_URL)).css('.ms-rtestate-read.ms-rte-wpbox').each do |rep_box|
        details_link = rep_box.at_css('.cocis-image-caption a')
        name         = details_link.normalized_text
        office       = rep_box.at_css('.cocis-image-caption strong').normalized_text
        photo_url    = BASE_URL + rep_box.at_css('.cocis-image a img').attr('src')

        data = {
          'name'       => name,
          'source_url' => SOURCE_URL,
          'photo_url'  => photo_url,
        }

        case office
          when /(\w+) (\d+) (\w*)/i
            district_title, district_id, elected_office = [$1, $2, $3]
            yield data.merge(alderman_details(details_link, district_title, district_id, elected_office))
          when /mayor/i
            yield data.merge(mayor_details(details_link, office))
          else
            fail "Office string not matched to any pattern"
        end
      end
    end

    private

    def alderman_details(details_link, district_title, district_id, elected_office)
      details_url = BASE_URL + details_link.attr('href')
      details_doc = Nokogiri::HTML(open(details_url))

      if contact_html = details_doc.at_css('.cocis-rte-Element-DIV-Sidebar-Right')
        contact_info_parts = contact_html.children.map(&:normalized_text)
        postal_info = "#{contact_info_parts[2]}\n#{contact_info_parts[4]}"
        phone_info  = contact_info_parts.find{|x| x[/phone:\s+/i]}.gsub(/phone:\s+/i, '')
        fax_info    = contact_info_parts.find{|x| x[/fax:\s+/i]}.gsub(/fax:\s+/i, '')
      else
        contact_html = details_doc.at_css('#contactInfo')
        contact_info_parts = contact_html.children.select{ |e| e.name == 'p' }.map(&:children)
        postal_info = "#{contact_info_parts[0][0]}\n#{contact_info_parts[0][2]}"
        phones = contact_info_parts[1].select{|x| x.to_s.gsub(/\D/, '').size == 10}
        phone_info  = phones[0].to_s.strip
        fax_info    = phones[1].to_s.strip
      end

      {
        'district_name'  => "#{district_title} #{district_id}",
        'district_id'    => district_id.to_i,
        'elected_office' => elected_office,
        'url'            => details_url,
        'offices'        => [
          {
            'postal' => postal_info,
            'tel'    => phone_info,
            'fax'    => fax_info,
          },
        ].to_json
      }
    end

    def mayor_details(details_link, office)
      agent              = Mechanize.new
      details_url        = details_link.attr('href')
      mayor_contact_page = agent.get(details_url).link_with(:text => /contact us/i).click
      details_doc        = Nokogiri::HTML(mayor_contact_page.body)

      contact_info       = details_doc.at_css(".alt-contact-holder")
      contact_info_parts = contact_info.children

      {
        'district_id'    => 0,
        'boundary_url'   => '/boundaries/census-subdivisions/4806016/',
        'elected_office' => office,
        'url'            => details_url,
        'email'          => contact_info.css('a[href^=mailto]').attr('href').to_s.gsub(/^mailto:/, ''),
        'offices'        => [
          {
            'postal' => [
              contact_info_parts[10].normalized_text, # office
              contact_info_parts[12].normalized_text, # P.O. Box
              contact_info_parts[14].normalized_text, # city, region, postal code
            ].join("\n"),
            'tel'    => contact_info_parts[2].normalized_text,
            'fax'    => contact_info_parts[5].normalized_text,
          },
        ].to_json
      }
    end
  end
end

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

CalgaryScrapper.scrap_data do |data|
  ScraperWiki.save_sqlite(['district_id'], data)
end

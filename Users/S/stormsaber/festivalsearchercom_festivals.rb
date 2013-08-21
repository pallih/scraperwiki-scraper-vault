require 'rubygems'
require 'mechanize'
require 'pp'

class XmlParser < Mechanize::File
  attr_reader :xml
  def initialize(uri = nil, response = nil, body = nil, code = nil)
    @xml = Nokogiri::XML(body)
    super uri, response, body, code
  end
end

a = Mechanize.new { |agent|
  agent.user_agent_alias = 'Mac Safari'
}
a.pluggable_parser['application/xml'] = XmlParser
a.pluggable_parser.default = XmlParser

Source = 'http://www.festivalsearcher.com/'
Index = 'festivallists.aspx?region=uk'
Sourcename = 'FestivalSeacher'
GeocodeResource = 'http://www.uk-postcodes.com/latlng/'

p "Scraping " + Sourcename + '..'
index = a.get(Source + Index)

index.search('#ctl00_main_festivalslistgrid tr').each do |tr|
  link = tr.search('td a')[0]

  if link
    p 'Fetching ' + Source + link['href'] + '...'
    page = a.get(Source + link['href'])
    
    p 'Found ' + page.search('title').text
    festival_data = { }
    
    festival_data[:festival_name] = page.search('#ctl00_main_FormView1_FestivalNameLabel').text

    node = page.search('#ctl00_main_FormView1_WikipediaLinkImage')
    unless node.empty? 
      festival_data[:wikipedia] = node.attr('href').value
      wikipedia_page = a.get(festival_data[:wikipedia])

      wikipedia_page.search('.infobox tr').each do |tr|
        case tr.search('th').text
        when 'Years active'
          festival_data[:years_active] = tr.search('td').text
        when 'Date(s)'
          festival_data[:dates] = tr.search('td').text
        when 'Genre'
          genres = Array.new
          tr.search('a').each do |genrelinks|
            genres << genrelinks.text
          end
          festival_data[:genres] = genres
        end
      end
      passed_toc = false
      description = ''
      wikipedia_page.search('#mw-content-text').each do |element|
        unless passed_toc
          if element.attr('id') and element.attr('id') == 'toc'
              passed_toc = true
          end
          if element.name = 'p'
            description = description + element.text
          end
        end
      end
      festival_data[:description] = description unless description == ''
    end


    festival_data[:start_date] = page.search('[itemprop="startDate"]').attr('content').value
    festival_data[:end_date] = page.search('[itemprop="endDate"]').attr('content').value

    node = page.search('#ctl00_main_FormView1_CityLabel')
    festival_data[:county] = node.text unless node.empty? 

    node = page.search('#ctl00_main_FormView1_Capacity')
    festival_data[:capacity] = node.text unless node.empty? 
    
    lat = page.search('meta[itemprop="latitude"]') 
    long = page.search('meta[itemprop="longitude"]')
    unless lat.empty? or long.empty? 
      lat = lat.attr('content').value
      long = long.attr('content').value
      festival_data[:latitude] = lat
      festival_data[:longtitude] = long

      postcode_page = a.get(GeocodeResource + lat + "," + long + ".xml")
      festival_data[:postcode] = postcode_page.xml.search("postcode").text
    end
    
    node = page.search('#ctl00_main_FormView1_WebsiteLinkImage') 
    festival_data[:website] = node.attr('href').value unless node.empty? 
        
    node = page.search('#ctl00_main_FormView1_FacebookLinkImage')
    festival_data[:facebook] = node.attr('href').value unless node.empty? 
    
    node = page.search('#ctl00_main_FormView1_TwitterLinkImage') 
    festival_data[:twitter] = node.attr('href').value unless node.empty? 
    
    node = page.search('#ctl00_main_FormView1_YoutubeLinkImage')
    festival_data[:youtube] = node.attr('href').value unless node.empty? 
   
    bands = Array.new
    page.search('#lineup ul span[itemprop="name"]').each do |bandname|
       bands << bandname.text
    end
    festival_data[:lineup] = bands
    
    tickets = Array.new
    page.search('[itemprop="offers"]').each do |ticket|
      ticket_type = {}
      ticket_type[:type] = ticket.search('[itemprop="name"]').text
      ticket_type[:amount] = ticket.search('[itemprop="price"]').text
      tickets << ticket_type
    end
    festival_data[:ticket_types] = tickets
    
    #puts festival_data.to_json

    ScraperWiki::save_sqlite(unique_keys=[:festival_name], data=festival_data)   
  end
end

pp ScraperWiki::show_tables()
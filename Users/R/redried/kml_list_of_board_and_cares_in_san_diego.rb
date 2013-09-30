# Blank Ruby
sourcescraper = 'board_and_cares_in_san_diego'

ScraperWiki::attach(sourcescraper)
bnc = ScraperWiki::select("name,addr1,addr2,phone,lat,long,capacity,vacancies,license from #{sourcescraper}.swdata order by name")

# Outputs a KML file for importing into Google Maps
require 'mechanize'

builder = Nokogiri::XML::Builder.new do |xml|
    xml.kml( 'xmlns' => 'http://www.opengis.net/kml/2.2' ) {
      xml.Document {
        
        xml.Style.hasVacancy! {
                xml.IconStyle {
                      xml.color "ffff0000"
                      xml.colorMode "normal" 
                      xml.scale 1.1
                      xml.Icon {
                            xml.href "http://maps.google.com/mapfiles/kml/paddle/red-circle_maps.png"
                      }
                }
               
        }
        
        for row in bnc 
            next if ! row['long'] || ! row['lat']
            xml.Placemark {
                xml.name row['name']
                if row['vacancies'].to_i != 0
                     xml.styleUrl "#hasVacancy"
                end

                xml.description {
                    if (row['addr1'] && row['addr2'])
                        @html = Nokogiri::HTML::DocumentFragment::parse ""
                        Nokogiri::HTML::Builder.with(@html) do |h|
                                h.div {
                                   h.p row['addr1']
                                   h.p row['addr2']
                                }
                                
                                h.blockquote "Phone: "+row['phone']
                                h.blockquote "Capacity: "+row['capacity']

                                # Count is string in form 'dddd'.  Add up digits to get total number of vacancies.
                                h.blockquote "Vacancies: " + row['vacancies'].each_char.inject(0) { |total, n| total += n.to_i }.to_s
                                
                                h.blockquote "License #: " + row['license']
                        end
                        
                        xml.cdata(@html.to_html)
                    end
                }
                xml.Point {
                
                    xml.coordinates row['long'] + "," + row['lat'] + ",0"
                }
            }
        end
 
        } # end Document
    } # end KML
end

ScraperWiki::httpresponseheader("Content-Type", "application/vnd.google-earth.kml+xml")
puts builder.to_xml
# Blank Ruby
sourcescraper = 'board_and_cares_in_san_diego'

ScraperWiki::attach(sourcescraper)
bnc = ScraperWiki::select("name,addr1,addr2,phone,lat,long,capacity,vacancies,license from #{sourcescraper}.swdata order by name")

# Outputs a KML file for importing into Google Maps
require 'mechanize'

builder = Nokogiri::XML::Builder.new do |xml|
    xml.kml( 'xmlns' => 'http://www.opengis.net/kml/2.2' ) {
      xml.Document {
        
        xml.Style.hasVacancy! {
                xml.IconStyle {
                      xml.color "ffff0000"
                      xml.colorMode "normal" 
                      xml.scale 1.1
                      xml.Icon {
                            xml.href "http://maps.google.com/mapfiles/kml/paddle/red-circle_maps.png"
                      }
                }
               
        }
        
        for row in bnc 
            next if ! row['long'] || ! row['lat']
            xml.Placemark {
                xml.name row['name']
                if row['vacancies'].to_i != 0
                     xml.styleUrl "#hasVacancy"
                end

                xml.description {
                    if (row['addr1'] && row['addr2'])
                        @html = Nokogiri::HTML::DocumentFragment::parse ""
                        Nokogiri::HTML::Builder.with(@html) do |h|
                                h.div {
                                   h.p row['addr1']
                                   h.p row['addr2']
                                }
                                
                                h.blockquote "Phone: "+row['phone']
                                h.blockquote "Capacity: "+row['capacity']

                                # Count is string in form 'dddd'.  Add up digits to get total number of vacancies.
                                h.blockquote "Vacancies: " + row['vacancies'].each_char.inject(0) { |total, n| total += n.to_i }.to_s
                                
                                h.blockquote "License #: " + row['license']
                        end
                        
                        xml.cdata(@html.to_html)
                    end
                }
                xml.Point {
                
                    xml.coordinates row['long'] + "," + row['lat'] + ",0"
                }
            }
        end
 
        } # end Document
    } # end KML
end

ScraperWiki::httpresponseheader("Content-Type", "application/vnd.google-earth.kml+xml")
puts builder.to_xml

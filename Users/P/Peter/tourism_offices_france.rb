require 'nokogiri'




def scrape_page(url)
html = ScraperWiki.scrape( url )
html_doc = Nokogiri::HTML(html)

#Name of Office

name_of_office = []
@address = []

html_doc.xpath('//div[@class="item"]').each do | method_span |  
     method_span.search('h2').each do |h2|
     @name = h2.inner_html.chomp
     end
     method_span.search('p').each do |p|
     @address << p.inner_html.gsub(/<br>/, "")
     end
    @address = @address.first.chomp.partition("Téléphone :")
    @place = @address.first.chomp
    @telephone = @address.last.chomp
    @address = []
    
ScraperWiki.save_sqlite(unique_keys=["Name of Office"], data={"Name of Office"=> @name, "Location" => @place, "Region" => @region, "Telephone"=> @telephone})              
end



html_doc.xpath('//div[@class="item border"]').each do | method_span |  
    method_span.search('h2').each do |h2|
     @name = h2.inner_html.chomp
     end
     method_span.search('p').each do |p|
     @address << p.inner_html.gsub(/<br>/, "")
     end
    @address = @address.first.chomp.partition("Téléphone :")
    @place = @address.first.chomp
    @telephone = @address.last.chomp
    @address = []
    
ScraperWiki.save_sqlite(unique_keys=["Name of Office"], data={"Name of Office"=> @name, "Location" => @place, "Region" => @region, "Telephone"=> @telephone})   
end


end






def scrape_and_look_for_next_link(url)
 begin

    @next_link = "false"
    scrape_page(url)

    html = ScraperWiki.scrape(url)
    page = Nokogiri::HTML(html)

    page.search('a').each do |a|
      if a.inner_html.to_s.include? "Suivant"
            puts a.inner_html
            puts a
      @next_link = a
      end
    end

    if @next_link != "false"
      #puts @next_link
      next_url = @base_url + @next_link['href'].chomp.gsub(/\s/, '+').removeaccents
      #puts next_url
      scrape_and_look_for_next_link(next_url)
      end

rescue Timeout::Error
retry
rescue 
retry
end


end




def get_names
html = ScraperWiki.scrape("http://www.tourisme.fr/L-annuaire")
doc = Nokogiri::HTML(html)

@@names = doc.xpath('//map[@name="Map-grande"]/area').map { |name| name['alt']}
puts @@names
end



# RemoveAccents version 1.0.3 (c) 2008-2009 Solutions Informatiques Techniconseils inc.
# 
# This module adds 2 methods to the string class. 
# Up-to-date version and documentation available at:
#
# http://www.techniconseils.ca/en/scripts-remove-accents-ruby.php
#
# This script is available under the following license :
# Creative Commons Attribution-Share Alike 2.5.
#
# See full license and details at :
# http://creativecommons.org/licenses/by-sa/2.5/ca/
#
# Version history:
#   * 1.0.3 : July 23 2009
#               Corrected some incorrect character codes. Source is now wikipedia at:
#                 http://en.wikipedia.org/wiki/ISO/IEC_8859-1#Related_character_maps
#               Thanks to Raimon Fernandez for pointing out the incorrect codes.
#   * 1.0.2 : October 29 2008
#               Slightly optimized version of urlize - Jonathan Grenier (jgrenier@techniconseils.ca)
#   * 1.0.1 : October 29 2008
#               First public revision - Jonathan Grenier (jgrenier@techniconseils.ca)
#

class String
  # The extended characters map used by removeaccents. The accented characters 
  # are coded here using their numerical equivalent to sidestep encoding issues.
  # These correspond to ISO-8859-1 encoding.
  ACCENTS_MAPPING = {
    'E' => [200,201,202,203],
    'e' => [232,233,234,235],
    'A' => [192,193,194,195,196,197],
    'a' => [224,225,226,227,228,229,230],
    'C' => [199],
    'c' => [231],
    'O' => [210,211,212,213,214,216],
    'o' => [242,243,244,245,246,248],
    'I' => [204,205,206,207],
    'i' => [236,237,238,239],
    'U' => [217,218,219,220],
    'u' => [249,250,251,252],
    'N' => [209],
    'n' => [241],
    'Y' => [221],
    'y' => [253,255],
    'AE' => [306],
    'ae' => [346],
    'OE' => [188],
    'oe' => [189]
  }
  
  
  # Remove the accents from the string. Uses String::ACCENTS_MAPPING as the source map.
  def removeaccents    
    str = String.new(self)
    String::ACCENTS_MAPPING.each {|letter,accents|
      packed = accents.pack('U*')
      rxp = Regexp.new("[#{packed}]", nil, 'U')
      str.gsub!(rxp, letter)
    }
    
    str
  end
  
  
  # Convert a string to a format suitable for a URL without ever using escaped characters.
  # It calls strip, removeaccents, downcase (optional) then removes the spaces (optional)
  # and finally removes any characters matching the default regexp (/[^-_A-Za-z0-9]/).
  #
  # Options
  #
  # * :downcase => call downcase on the string (defaults to true)
  # * :convert_spaces => Convert space to underscore (defaults to false)
  # * :regexp => The regexp matching characters that will be converting to an empty string (defaults to /[^-_A-Za-z0-9]/)
  def urlize(options = {})
    options[:downcase] ||= true
    options[:convert_spaces] ||= false
    options[:regexp] ||= /[^-_A-Za-z0-9]/
    
    str = self.strip.removeaccents
    str.downcase! if options[:downcase]
    str.gsub!(/\ /,'_') if options[:convert_spaces]
    str.gsub(options[:regexp], '')
  end
end












get_names

i = 0
while i < (@@names.length)

place_url = @@names[i]
puts place_url.to_s.chomp.gsub(/\s/, '+').removeaccents
@region = place_url.to_s
puts @region

@base_url = "http://www.tourisme.fr/"
initial = "L-annuaire/Resultat-de-votre-recherche?src%5Bzone%5D="
#place_url = "Languedoc-roussillon"
suffix_url = "&x=28&y=3"

starting_url = @base_url + initial + place_url.to_s.chomp.gsub(/\s/, '+').removeaccents + suffix_url

puts starting_url

scrape_and_look_for_next_link(starting_url)

i += 1
end 







#html_doc.search('h2').each do |h2|
#puts h2.inner_html
#end




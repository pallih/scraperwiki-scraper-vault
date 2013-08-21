# Blank Ruby

# Blank Ruby

require 'net/http'
require 'rexml/document'
require 'scraperwiki'
require 'date'
require 'csv'

class REXML::Element

 def inner_texts
  REXML::XPath.match(self,'.//text()')
 end

 def inner_text
  REXML::XPath.match(self,'.//text()').join 
 end

end


until_date = Date.today

since_date = Date.parse('24 May 2012')
#until_date = Date.parse('31 December 2012')

datesarray = (since_date..until_date).map{ |date| date.strftime("%Y-%m-%e") }

datesarray.each{
|day|

day = day.gsub(" ", "0")

day_versions = Array.new

day_versions[0] = day
day_versions[1] = day + "a"
day_versions[2] = day + "b"
day_versions[3] = day + "c"
day_versions[4] = day + "d"
day_versions[5] = day + "e"
day_versions[6] = day + "f"
day_versions[7] = day + "g"
day_versions[8] = day + "h"
day_versions[9] = day + "i"
day_versions[10] = day + "j"
day_versions[11] = day + "k"
day_versions[12] = day + "l"
day_versions[13] = day + "m"
day_versions[14] = day + "n"
day_versions[15] = day + "o"
day_versions[16] = day + "p"
day_versions[17] = day + "q"
day_versions[18] = day + "r"
day_versions[19] = day + "s"
day_versions[20] = day + "t"
day_versions[21] = day + "u"

day_versions.each{
|day_string|
error = false

puts day

#url = 'http://ukparse.kforge.net/parldata/scrapedxml/wms/ministerial' + day_string + '.xml'
url = 'http://ukparse.kforge.net/parldata/scrapedxml/lordswms/lordswms' + day_string + '.xml'

uri = URI.parse(url)
response = Net::HTTP.get_response(uri);

begin
xmlDoc = REXML::Document.new response.body
rescue REXML::ParseException => msg
  puts "Failed: #{msg}"
  puts "Skipping day.."
  error = true
end

if !error


xmlDoc.elements.each('publicwhip/speech') { 
  |status|

  status.elements.each{
    |status2|
    puts "%s \n" % 
      [
        status2.text,
        status2.children,
        status2.inner_texts
      ]

    #Initialise text
    temp_text = " "
    unless status2.nil? 
    temp_text = status2.text
    end

    for i in 1..status2.children.length-1

    # if they are weird elements
    unless status2.children[i].nil? 
     puts "Inside: %s - %s" % [status2.children[i],temp_text]
      #if status2.children[i].to_s.length > 0
        temp_text = temp_text.to_s + status2.children[i].to_s
      #end
    end

    end

    unless status2.attributes["pid"].nil? 
    data = {
      id: status.attributes["id"],
      speakername: status.attributes["speakername"],
      speakerid: status.attributes["speakerid"],
      speakeroffice: status.attributes["speakeroffice"],
      text: temp_text,
      #text: status2.text,
      pid: status2.attributes["pid"],
      date: day
    }
    end

    ScraperWiki::save_sqlite(['pid'],data) 

}

  
}

end

}

}

require 'mechanize'
require 'csv'

$a = Mechanize.new
$a.user_agent_alias = 'Windows IE 8'

BNC_URL = 'http://211sandiego.communityos.org/cms/board-and-care_availability'
GEOCODE_URL = 'http://maps.google.com/maps/geo'

bnc = {}

rows = $a.get(BNC_URL).search("#content").search('table//tr')

# Delete beginning of mp array up to 1st element with class xl67
index_first_find = 0

rows.each_with_index do |tr,n|
        if ! tr.search(".xl67").empty? 
                index_first_find = n
                break
        end
end

rows = rows.slice(index_first_find, rows.length - index_first_find)

tmp = Hash.new("")

class String
        def strip_utf8()
                self.gsub(/(^[[:space:]]+)|([[:space:]]+$)/, '')
        end
end

rows.each do |tr|
        
        # Headings start with "Facility Name" in bold
        if ! tr.search('.//strong[contains(text(), "Facility Name")]').empty? 
          puts "Skipping " + tr.text
          next
        end
        
        # Sections start with in bold
        if tr.search('strong').text.strip_utf8.match(/^\s*(East|South|North)\s*$/)     
          puts "Skipping " + tr.text
          next
        end
    
        # These rows are formatted differently than the rest.  GRRRR.
        # All the info is in one row.
        if tr.search('td').first.text.match(/(374601462|370808541)/)
                puts "Special case: " + tr.text
                next
        end

        tr.search('td').each_with_index do |td,n|
     
                # Name, url, address, license are in the first TD cell of the row
                if n == 0
                        tmp['addr2'], tmp['license'] = td.text.scan(/(^.*)License:\s*(\d+)/m).flatten
                        if ! tmp['addr2'].nil? 
                                tmp['addr2'] = tmp['addr2'].strip_utf8
                                tmp['zip'] = tmp['addr2'].scan(/(\d+)$/).flatten.first
                        end
                        td.xpath('.//a').each do |link|
                                tmp['url'] = link.attribute('href').value
                                tmp['name'] = link.text.strip_utf8
                        end

                         # License is found in the last of the rows: if found, time to write out result and reset      
                        if (!tmp['license'])
                                if tmp['url'] ; tmp['addr1'] = td.text.strip_utf8 ; end
                        else
                                # Rename the availabilty columns
                                tmp['vacancies'] = tmp['avail_0'].to_s +
                                                   tmp['avail_1'].to_s +
                                                   tmp['avail_2'].to_s +
                                                   tmp['avail_3'].to_s
                                
                                tmp.reject! { |k| k.match(/^avail_/) }

                                bnc[tmp['license']] = tmp.clone
                                tmp.clear
                        end
                end
                if n == 3
                        if (td.text.match(/\S+/))
                                tmp['phone'] = td.text.strip_utf8
                        end
                end
                if n == 4
                        if (td.text.match(/\S+/))
                                tmp['capacity'] = td.text.strip_utf8
                        end
                end
                if [5,6,7,8].include?  n
                        if (td.text.match(/\S+/))
                                 tmp['avail_'+(n-5).to_s] = td.text.strip_utf8
                        end
                end
        end

end



def geocode_this(addr1, addr2)
    u = $a.get(GEOCODE_URL, { :q => addr1 + ' ' + addr2,
                              :output => 'csv' })
    doc = CSV::parse(u.body)
    if doc[0].first == "200" 
       [ doc[0][2], doc[0][3] ]
    else
       puts doc[0].first, doc.inspect
       []
    end
end

bnc.each do |key, row|
    
     row['lat'], row['long'] = geocode_this(row['addr1'], row['addr2'])
     sleep 0.5          # Give the geocoder a break 
     ScraperWiki::save_sqlite(['license'], row) 
#puts row.inspect
 # puts row.inspect
end


#######################################################################
# Focussing on the basics for now, trying to scrape individual pages
# Once I've got that stabilised, I'll try fetching the page list from
# http://www.leighrayment.com/commons.htm
# loop round the lot and dump the data out
# Hopefully!
#######################################################################

require 'nokogiri'

def get_data url, tries=0
  #ScraperWiki.scrape seems to choke periodically, this retries it a few times before
  #giving up on it
 
  max = 5

  begin
    return ScraperWiki.scrape(url)
  rescue
    if tries >= max
      raise "error retrieving data"
    else
      tries += 1
      sleep(1)
      get_data(url, tries)
    end
  end
end

# retrieve a page
starting_url = 'http://www.leighrayment.com/commons/Acommons1.htm'
html = get_data(starting_url)

@name = ""
@date = ""
@member = []

def clean_mp_data()
  #store = []
  #while @member.count > 0
  #  temp = @member.pop()
  #  store << temp.split(",")[0]
  #end
  #@member = store.reverse
  @member
end

def mp_name(input)
  if input =~ /(\[kt[^\]]*\])/
    return input.gsub($1, "").strip
  end
  input
end

doc = Nokogiri::HTML(html)
doc.xpath('//tr').each do |row|
  cells = row.xpath("td")
  data_cell = cells[2].xpath("text()").to_s
  data_cell.gsub!("&amp;", "&") if data_cell
  cell1 = cells[0].xpath("text()").to_s
  extra_info = cells[2].xpath("./font/text()").to_s
  if data_cell != "" and data_cell == data_cell.upcase
    case data_cell
      when /\d{4}/, /HOUSE\s+OF\s+COMMONS/, /BEGINNING\s+WITH/, /SPLIT\s+IN/, /REPRESENTATION\s+REDUCED/
        #skip, for now
      else
        if @date != "" and @member != []
          clean_mp_data()
          members = @member.join("; ")
          members = members.gsub(" ,", ", ").gsub(",later", ", later").squeeze(" ")
          puts "constituency: #{@name}; election: #{@date}; member(s): #{members.gsub(/\;\s+\|/, "")}"
          @member = []
          @date = ""
        end
        @name = data_cell
    end
  elsif cell1 =~ /(?:\d+\s+)?[A-Z][a-z]{2}\s+\d{4}/
    if @date != "" and @member != []
      clean_mp_data()
      members = @member.join("; ")
      members = members.gsub(" ,", ", ").gsub(",later", ", later").squeeze(" ")
      puts "constituency: #{@name}; election: #{@date}; member(s): #{members.gsub(/\;\s+\|/, "")}"
      @member = []
    end
    @date = cell1
    
    if @member.count > 0
      last = @member.pop
      @member << last
      if data_cell =~ /^\s*later/ or (last =~ /later|styled/ and !(last.rstrip[last.rstrip.length-9..last.rstrip.length] =~ /\(to \d{4}\)/))
        @member << " #{data_cell}".squeeze(" ")
      else
        @member << data_cell unless data_cell == ""
      end  
    else
      name = mp_name(data_cell)
      @member << name unless name == ""
    end
    @member << extra_info unless extra_info == ""
  elsif data_cell.strip != ""
    unless data_cell =~ /information|note\s+at\s+the\s+foot\s+of\s+this\s+page|Last\s+updated|Name|See also|comprising|Anstruther Wester,Crail/
      if @member.count > 0
        last = @member.pop
        @member << last
        if data_cell =~ /^\s*later/ or (last =~ /later|styled/ and !(last.rstrip[last.rstrip.length-9..last.rstrip.length] =~ /\(to \d{4}\)/))
          @member << "| #{data_cell}".squeeze(" ")
        else
          @member << data_cell unless data_cell == ""
        end
      else
        name = mp_name(data_cell)
        @member << name unless name == ""
      end
      @member << extra_info unless extra_info == ""
    end
  end
end

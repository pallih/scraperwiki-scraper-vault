# require 'rubygems'
# require 'mechanize'
require 'nokogiri'
require 'enumerator' # in case of old ruby version

# agent = Mechanize.new

url = "http://www.klicktel.de/branchen/rechtsanwaelte-familienrecht-muenster-westf-3304264-66026719.html"
# start_page = agent.get(url)
start_page = Nokogiri::HTML(ScraperWiki.scrape(url))

# return pairs of phone type and phone number
def parse_phones(table_element)
  results = []
  # super fragile?
  table_element.search(".//td").reject { |td|
    td['colspan'] == "2" || td['height'] == '1' || td.content.strip == ""
  }.each_slice(2) do |slice|
    type = slice[0].content.gsub(":","").strip
    number = slice[1].content.gsub(":","").strip
    results << [type, number]
  end
  results
end

# get all the links to "senators.asp"
links = start_page.search("a").select { |x| 
  x['href'] =~ /^senators.asp\?/ }

links.each do |link|
  result = {}
  result['url'] = "http://www.aph.gov.au/Senate/senators/homepages/" + link['href']
  
  # page = agent.get(result['url'])
  page = Nokogiri::HTML(ScraperWiki.scrape(result['url']))
  
  # split to get province and name from link (it's easier than the info page)
  full_name, province = link.content.split(/\s+\-\s+/)
  result['province'] = province.gsub(/senator\s+for/i,"").strip
  
  last_name, first_name = full_name.split(",")
  result['last_name'] = last_name.strip
  result['first_name'] = first_name.gsub(/the\s+hon/i,"").strip
  
  # this part super fragile since they have bad markup
  content_xpath = "//td[@width='85%']" # xpath to content area
  
  # nokogiri doesn't support xpath not equals for attributes
  # last paragraph is the "top" link
  paragraphs = page.search(content_xpath + "//p").reject { |p|
    p['class'] == 'footer' }[0..-1]
  tables = page.search(content_xpath + "//table")
  
  paragraphs.each do |paragraph|
    strong = paragraph.search("strong")[0]
    next unless strong
    key = strong.content.gsub(":","").strip
    # if links or external links, get the next ul, which is the list of links
    if key =~ /links/i
      ul = paragraph.next_element
      next if ul.name != 'ul'
      
      result[key] = ul.search('li a').map { |a|
        # we could get the full biography and first speech if we wanted
        # next if a.content =~ /biography/i
        a.content.strip + ", " + a['href']
      }.join(" ; ")
    else
      # unlink the strong
      strong.unlink
      if key =~ /electorate office/i
        maybe_br = paragraph.children[0]
        maybe_br.unlink if maybe_br.name == 'br'
        paragraph.search("br").each do |br|
          br.content = "LINEBREAK"
        end
        result["#{key} address"] = paragraph.content.strip.
          gsub(/(LINEBREAK)+/,", ").gsub(/\s+/, " ").gsub(" , ", ", ")

        # check if there is another address. Assume only two max.
        p_or_table = paragraph.next_element
        if p_or_table.name == 'p'
          p_or_table.search("br").each do |br|
            br.content = "LINEBREAK"
          end
          result["#{key} address 2"] = p_or_table.content.strip.
            gsub(/(LINEBREAK)+/,", ").gsub(/\s+/, " ").gsub(" , ", ", ")
          
          table = p_or_table.next_element
          if table.name == 'table'
            parse_phones(table).each do |phone|
              result["#{key} #{phone[0]}"] = phone[1]
            end
          end
        elsif p_or_table.name == 'table'
          parse_phones(p_or_table).each do |phone|
            result["#{key} #{phone[0]}"] = phone[1]
          end
        end
      elsif key =~ /email/i
        email_link = paragraph.search("a")[0]
        result[key] = paragraph.search("a")[0]['href']
      elsif key =~ /position/i
        result['positions'] = paragraph.content.strip.gsub(/\s{2,}/, "; ")
      else
        # otherwise, just take the content
        result[key] = paragraph.content.strip
      end
                                                                                                                                end
  end
  
  tables.each do |table|
    # usually only two tables?
    # one is the electorate office phone numbers which we already did
    # the other is another phone table, there could be more?
    header = table.search("strong")[0]
    next unless header
    key = header.content.gsub(":","").strip
    parse_phones(table).each do |phone|
      result["#{key} #{phone[0]}"] = phone[1]
    end
  end
  
  # result.each_pair do |k,v|
    # puts "#{k} ||| #{v}"
  # end
  
  final_result = {}
  result.each_pair do |k,v|
    final_result[k.gsub(" ", "_")] = v
  end

  ScraperWiki.save(final_result.keys, final_result)
end
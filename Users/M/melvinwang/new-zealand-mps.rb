# require 'rubygems'
# require 'mechanize'
require 'nokogiri'
require 'enumerator'

# agent = Mechanize.new
# start_page = agent.get("http://www.parliament.nz/en-NZ/MPP/MPs/MPs/Default.htm?pf=&sf=&lgc=1")

start_page = Nokogiri::HTML(ScraperWiki.scrape("http://www.parliament.nz/en-NZ/MPP/MPs/MPs/Default.htm?pf=&sf=&lgc=1"))

start_page.search("table.listing tbody tr").each do |tr|
  result = {}
  
  td0, td1 = tr.search("td")
  next unless td0 && td1
  
  mp_link = tr.search("td a")[0]
  next unless mp_link
  
  result['url'] = "http://www.parliament.nz" + mp_link['href']
  result['last_name'], result['first_name'] = mp_link.content.split(",").map { |x| x.strip }
  
  result['party'], result['electorate'] = td1.content.split(",").map { |x| x.strip }

  puts "working on #{result['first_name']} #{result['last_name']}"

  # TODO: could use URI/CGI libraries to combine
  # page = agent.get(result["url"]).search("html")[0]
  page = Nokogiri::HTML(ScraperWiki.scrape(result["url"]))
  
  # left side
  page.search("div.section div.section").each do |section|
    h2 = section.search("h2")[0]
    next unless h2
    key = h2.content.strip
    
    ul = section.search("ul")[0]
    ps = section.search("p")
    if ul
      # join the li's. we don't have any way of sanitizing tags though
      data = ul.search("li").map { |x| x.content.strip }.join(" ; ")
    else
      # join the p's
      data = ps.map { |x| x.content.strip }.join(" ; ")
    end
    
    result[key.gsub(/\s+/, "_")] = data
  end
  
  info_tile_rows = page.search("div.infoTiles table tbody").last.search("tr").to_a
  info_tile_rows.each_slice(2) do |slice|
    next unless slice[1] # we must be off by one...
    key = slice[0].content.strip
    
    if key =~ /contact details/i
      # address needs to be stripped of brs
      slice[1].search("br").each do |br|
        br.name = "b"
        br.content = "LINEBREAK"
      end
      data = slice[1].content.strip.gsub(/(LINEBREAK)+/,", ")
    elsif slice[1].search("ul")[0]
      # list could contain links
      data = slice[1].search("li").map { |x|
        a = x.search("a")[0]
        a ? x.content.strip + ", " + a['href'] : x.content.strip  
      }.join(" ; ")
    else
      data = slice[1].content.strip.gsub(/\s+/, " ")
    end
    
    result[key.gsub(/\s+/, "_")] = data
  end

=begin
  result.each_pair do |k,v|
    puts "#{k} |||||| #{v}"
  end
=end
  
  ScraperWiki.save(result.keys, result)
end

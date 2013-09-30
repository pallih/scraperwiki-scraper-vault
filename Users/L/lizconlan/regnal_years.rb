require 'nokogiri'
require 'time'
require 'date'
require 'httpclient'
require 'zlib'

def scrape(url, agent_string=nil)
  if agent_string
    client = HTTPClient.new(:agent_name => agent_string)
  else
    client = HTTPClient.new
  end
  client.ssl_config.verify_mode = OpenSSL::SSL::VERIFY_NONE
  if HTTPClient.respond_to?("client.transparent_gzip_decompression=")
    client.transparent_gzip_decompression = true
  end

  html = client.get_content(url)

  unless HTTPClient.respond_to?("client.transparent_gzip_decompression=")
    begin
      gz = Zlib::GzipReader.new(StringIO.new(html))    
      return gz.read
    rescue
      return html
    end
  end
  html
end

def roman_to_integer(roman)
  case roman
    when "I"
      return 1
    when "II"
      return 2
    when "III"
      return 3
    when "IV"
      return 4
    when "V"
      return 5
    when "VI"
      return 6
    when "VII"
      return 7
    when "VIII"
      return 8
    else
      nil
  end
end

def abbreviate(monarch, year)
  m_abbrev = ""
  case monarch
    when "John", "Richard I", "Henry II", "Stephen", "Henry I", "William II", "William I"
      return "-" #predates Parliamentary use so not calculated
    when /Philip and Mary/
      m_abbrev = "Ph. & M."
    when /William and Mary/
      m_abbrev = "Will. & Mar."
    when /James/
      m_abbrev = "Ja."
    when /William/, /Elizabeth/, /Victoria/
      m_abbrev = "#{monarch[0..3]}."
    else
      m_abbrev = "#{monarch[0..2]}."
  end
  unless monarch == "Mary I"
    numeral = roman_to_integer(monarch.split(" ").last)
    if numeral
      m_abbrev = "#{m_abbrev} #{numeral}"
    end
  end
  "#{year} #{m_abbrev}"
end

## currently not working
#html = ScraperWiki.scrape("http://en.wikipedia.org/wiki/Regnal_years_of_English_monarchs")


## debug
#p HTTPClient::VERSION

#agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.54.16 (KHTML, like Gecko) Version/5.1.4 Safari/534.54.16"
html = scrape("http://en.wikipedia.org/wiki/Regnal_years_of_English_monarchs")

html.force_encoding("UTF-8")
doc = Nokogiri::HTML(html)

ascension_days = {}

footnotes = doc.xpath("//ol[@style='list-style:upper-alpha']/li")
ascension_day_info = footnotes[0].xpath("ul/li")
ascension_day_info.each do |ascension_day|
  data = ascension_day.text.split(" \u2013 ")
  ascension_days[data[0]] = data[1]
end

rows = doc.xpath("//table[@class='wikitable']/tr")

## debug stuff
#p rows.size
# rows = []
#p html.inspect

rows.each do |row|
  monarch = ""
  first_year = ""
  last_year = ""
  year_start = ""
  year_end = ""
  reign_end = ""
  cells = row.xpath("td")
  cells.each_with_index do |node, offset|
    case offset
    when 0
      monarch = node.text
    when 1
      years = node.text
    when 2
      first_year = node.text.to_i
    when 3
      year_start = node.text
      if year_start =~ /(\d+ [A-Z][a-z]+)/
        year_start = $1
      end
    when 4
      year_end = node.text
      year_end.gsub!(/\[([^\]])*\]/, "")
      year_end.strip!
    when 5
      reign_end = node.text
      reign_end.gsub!(/\[([^\]])*\]/, "")
      if reign_end =~ / (\d{4})/
        last_year = $1
      end
    end
  end

  unless cells.empty? 
   # p monarch
   # p "reigned: #{first_year} - #{last_year}"
   # p "year starts: #{year_start}"
   # p "reign ended: #{reign_end}"

    i = 1
    save = 0
    stop_year = 0
    if last_year.to_i == 0
      stop_year = Time.now.year()
    else
      stop_year = last_year.to_i
    end

    record = {}
    (first_year.to_i..stop_year.to_i).each do |year|
      if monarch == "John"
        year_start = ascension_days["Year #{i}"][0..-6]
      end

      reign_year = ""
      unless monarch == '"Philip and Mary"'
        reign_year = i.to_s
      else
        reign_year = "#{i} & #{i+1}"
      end
      abbreviation = abbreviate(monarch, reign_year)
      if ((year_end =~ /varied/ or reign_end == "...") and year == stop_year) or (reign_end != "..." and (year_end =~ /varied/).nil? and Date.parse("#{year_end} #{year+1}") > Date.parse(reign_end))
        record = {'monarch' => monarch.gsub('"',''), 'year' => reign_year, 'year_start' => "#{year_start} #{year}", 'year_end' => reign_end, 'abbreviation' => abbreviation}
        ScraperWiki.save(['monarch', 'year'], record)
        break
      else
        if monarch == "John"
          next_ascension_day = ascension_days["Year #{i+1}"]
          parts = next_ascension_day.split(" ")
          year_end = "#{parts[0].to_i-1} #{parts[1]}"
        end
        record = {'monarch' => monarch.gsub('"',''), 'year' => reign_year, 'year_start' => "#{year_start} #{year}", 'year_end' => "#{year_end} #{year+1}", 'abbreviation' => abbreviation}
        ScraperWiki.save(['monarch', 'year'], record)
      end
      i += 1
    end
    # p ""
  end
endrequire 'nokogiri'
require 'time'
require 'date'
require 'httpclient'
require 'zlib'

def scrape(url, agent_string=nil)
  if agent_string
    client = HTTPClient.new(:agent_name => agent_string)
  else
    client = HTTPClient.new
  end
  client.ssl_config.verify_mode = OpenSSL::SSL::VERIFY_NONE
  if HTTPClient.respond_to?("client.transparent_gzip_decompression=")
    client.transparent_gzip_decompression = true
  end

  html = client.get_content(url)

  unless HTTPClient.respond_to?("client.transparent_gzip_decompression=")
    begin
      gz = Zlib::GzipReader.new(StringIO.new(html))    
      return gz.read
    rescue
      return html
    end
  end
  html
end

def roman_to_integer(roman)
  case roman
    when "I"
      return 1
    when "II"
      return 2
    when "III"
      return 3
    when "IV"
      return 4
    when "V"
      return 5
    when "VI"
      return 6
    when "VII"
      return 7
    when "VIII"
      return 8
    else
      nil
  end
end

def abbreviate(monarch, year)
  m_abbrev = ""
  case monarch
    when "John", "Richard I", "Henry II", "Stephen", "Henry I", "William II", "William I"
      return "-" #predates Parliamentary use so not calculated
    when /Philip and Mary/
      m_abbrev = "Ph. & M."
    when /William and Mary/
      m_abbrev = "Will. & Mar."
    when /James/
      m_abbrev = "Ja."
    when /William/, /Elizabeth/, /Victoria/
      m_abbrev = "#{monarch[0..3]}."
    else
      m_abbrev = "#{monarch[0..2]}."
  end
  unless monarch == "Mary I"
    numeral = roman_to_integer(monarch.split(" ").last)
    if numeral
      m_abbrev = "#{m_abbrev} #{numeral}"
    end
  end
  "#{year} #{m_abbrev}"
end

## currently not working
#html = ScraperWiki.scrape("http://en.wikipedia.org/wiki/Regnal_years_of_English_monarchs")


## debug
#p HTTPClient::VERSION

#agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.54.16 (KHTML, like Gecko) Version/5.1.4 Safari/534.54.16"
html = scrape("http://en.wikipedia.org/wiki/Regnal_years_of_English_monarchs")

html.force_encoding("UTF-8")
doc = Nokogiri::HTML(html)

ascension_days = {}

footnotes = doc.xpath("//ol[@style='list-style:upper-alpha']/li")
ascension_day_info = footnotes[0].xpath("ul/li")
ascension_day_info.each do |ascension_day|
  data = ascension_day.text.split(" \u2013 ")
  ascension_days[data[0]] = data[1]
end

rows = doc.xpath("//table[@class='wikitable']/tr")

## debug stuff
#p rows.size
# rows = []
#p html.inspect

rows.each do |row|
  monarch = ""
  first_year = ""
  last_year = ""
  year_start = ""
  year_end = ""
  reign_end = ""
  cells = row.xpath("td")
  cells.each_with_index do |node, offset|
    case offset
    when 0
      monarch = node.text
    when 1
      years = node.text
    when 2
      first_year = node.text.to_i
    when 3
      year_start = node.text
      if year_start =~ /(\d+ [A-Z][a-z]+)/
        year_start = $1
      end
    when 4
      year_end = node.text
      year_end.gsub!(/\[([^\]])*\]/, "")
      year_end.strip!
    when 5
      reign_end = node.text
      reign_end.gsub!(/\[([^\]])*\]/, "")
      if reign_end =~ / (\d{4})/
        last_year = $1
      end
    end
  end

  unless cells.empty? 
   # p monarch
   # p "reigned: #{first_year} - #{last_year}"
   # p "year starts: #{year_start}"
   # p "reign ended: #{reign_end}"

    i = 1
    save = 0
    stop_year = 0
    if last_year.to_i == 0
      stop_year = Time.now.year()
    else
      stop_year = last_year.to_i
    end

    record = {}
    (first_year.to_i..stop_year.to_i).each do |year|
      if monarch == "John"
        year_start = ascension_days["Year #{i}"][0..-6]
      end

      reign_year = ""
      unless monarch == '"Philip and Mary"'
        reign_year = i.to_s
      else
        reign_year = "#{i} & #{i+1}"
      end
      abbreviation = abbreviate(monarch, reign_year)
      if ((year_end =~ /varied/ or reign_end == "...") and year == stop_year) or (reign_end != "..." and (year_end =~ /varied/).nil? and Date.parse("#{year_end} #{year+1}") > Date.parse(reign_end))
        record = {'monarch' => monarch.gsub('"',''), 'year' => reign_year, 'year_start' => "#{year_start} #{year}", 'year_end' => reign_end, 'abbreviation' => abbreviation}
        ScraperWiki.save(['monarch', 'year'], record)
        break
      else
        if monarch == "John"
          next_ascension_day = ascension_days["Year #{i+1}"]
          parts = next_ascension_day.split(" ")
          year_end = "#{parts[0].to_i-1} #{parts[1]}"
        end
        record = {'monarch' => monarch.gsub('"',''), 'year' => reign_year, 'year_start' => "#{year_start} #{year}", 'year_end' => "#{year_end} #{year+1}", 'abbreviation' => abbreviation}
        ScraperWiki.save(['monarch', 'year'], record)
      end
      i += 1
    end
    # p ""
  end
end
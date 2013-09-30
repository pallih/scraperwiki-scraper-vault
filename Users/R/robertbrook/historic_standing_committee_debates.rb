require 'nokogiri'
require 'net/http'
require 'uri'

def get_url(url, try=1)
  max_attempts = 5
  begin
    return Net::HTTP.get_response(url)
  rescue Timeout::Error
    sleep(20)
    if try < max_attempts
      get_url(url, try + 1)
    else
      raise "Timed out trying to reach #{url}"
    end
  end
end

def format_member_name(input)
  return "" if input.nil? 
  
  #dump anything enclosed in brackets
  input = input.gsub(/\([^\)]*\)/, "")

  #get rid of * character in name
  input = input.gsub("*", "")

  return "" if input.length == 0

  if input.index(",").to_i > 0
    name = input.split(",")
    if name[1].nil? #deal with odd markup
      member_name = name[0].strip
    else
      member_name = "#{name[1].strip} #{name[0].strip}"
    end
  else
    member_name = input
  end
  case member_name
    when "Hon. Members", /The/
      return ""
    else
      return member_name
  end
end

# define the order our columns are displayed in the datastore
#ScraperWiki.save_metadata("data_columns", ["href", "part-one", "part-two", "part-three", "bills", "members", "http-response", "content-length"])

starting_url = 'http://www.parliament.uk/business/publications/parliamentary-archives/archives-electronic/parliamentary-debates/historic-standing-committee-debates/'
html = ScraperWiki.scrape(starting_url)

doc = Nokogiri::HTML(html)

doc.search('div.inner ul li a').each do |a|
    uri = URI.parse(a['href'])
    if uri.host == "data.parliament.uk"
        response = get_url(URI.parse(a['href']))
        members = []
        bills = []
        if response.code == "200"
            
            doc_xml = Nokogiri::XML(response.body)
            doc_xml.xpath('//member/text()').each do |member|
              member_name = format_member_name(member.content)
              members << member_name unless member_name == ""
            end
            members = members.uniq.join("; ")
            
            doc_xml.xpath('//bill/text()').each do |bill|
              bills << bill.content
            end
            bills = bills.uniq.join("; ")

        end
        # record = {'members' => members.uniq.join("; "), 'bills' => bills.uniq.join("; "),  'http-response' => response.code, 'content-length' => response.content_length, 'href' => a['href'], 'part-one' => a.inner_html.split(' - ')[0], 'part-two' => a.inner_html.split(' - ')[1], 'part-three' => a.inner_html.split(' - ')[2]}
        record = {'members' => members, 'bills' => bills, 'href' => a['href'], 'title' => a.inner_html}
    
        ScraperWiki.save(['href'], record)
    end
end
require 'nokogiri'
require 'net/http'
require 'uri'

def get_url(url, try=1)
  max_attempts = 5
  begin
    return Net::HTTP.get_response(url)
  rescue Timeout::Error
    sleep(20)
    if try < max_attempts
      get_url(url, try + 1)
    else
      raise "Timed out trying to reach #{url}"
    end
  end
end

def format_member_name(input)
  return "" if input.nil? 
  
  #dump anything enclosed in brackets
  input = input.gsub(/\([^\)]*\)/, "")

  #get rid of * character in name
  input = input.gsub("*", "")

  return "" if input.length == 0

  if input.index(",").to_i > 0
    name = input.split(",")
    if name[1].nil? #deal with odd markup
      member_name = name[0].strip
    else
      member_name = "#{name[1].strip} #{name[0].strip}"
    end
  else
    member_name = input
  end
  case member_name
    when "Hon. Members", /The/
      return ""
    else
      return member_name
  end
end

# define the order our columns are displayed in the datastore
#ScraperWiki.save_metadata("data_columns", ["href", "part-one", "part-two", "part-three", "bills", "members", "http-response", "content-length"])

starting_url = 'http://www.parliament.uk/business/publications/parliamentary-archives/archives-electronic/parliamentary-debates/historic-standing-committee-debates/'
html = ScraperWiki.scrape(starting_url)

doc = Nokogiri::HTML(html)

doc.search('div.inner ul li a').each do |a|
    uri = URI.parse(a['href'])
    if uri.host == "data.parliament.uk"
        response = get_url(URI.parse(a['href']))
        members = []
        bills = []
        if response.code == "200"
            
            doc_xml = Nokogiri::XML(response.body)
            doc_xml.xpath('//member/text()').each do |member|
              member_name = format_member_name(member.content)
              members << member_name unless member_name == ""
            end
            members = members.uniq.join("; ")
            
            doc_xml.xpath('//bill/text()').each do |bill|
              bills << bill.content
            end
            bills = bills.uniq.join("; ")

        end
        # record = {'members' => members.uniq.join("; "), 'bills' => bills.uniq.join("; "),  'http-response' => response.code, 'content-length' => response.content_length, 'href' => a['href'], 'part-one' => a.inner_html.split(' - ')[0], 'part-two' => a.inner_html.split(' - ')[1], 'part-three' => a.inner_html.split(' - ')[2]}
        record = {'members' => members, 'bills' => bills, 'href' => a['href'], 'title' => a.inner_html}
    
        ScraperWiki.save(['href'], record)
    end
end

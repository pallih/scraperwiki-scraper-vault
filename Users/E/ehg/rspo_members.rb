require 'nokogiri'
 
class RSPOMembersScraper
  BASE_URL = "http://www.rspo.org"
  
  def self.members
    @members = Members.new if @members.nil? 
    @members
  end

  def self.start
    scrape_member_list "#{BASE_URL}/?page=0&q=membersearch"
  end

  def self.scrape_member_list(url)
    puts "Scraping memberlist..." if console_log?
    html = ScraperWiki::scrape url
    until (next_link = members_list_next_link(html)).nil? 
      html = ScraperWiki::scrape "#{BASE_URL}#{next_link}"
      members = extract_members html
      members.each { |m| add_to_members_array scrape_member_info(m) }
      self.members.save
      self.members.clear
    end
  end

  def self.add_to_members_array(member)
    members << member
  end

  def self.members_list_next_link(html)
    doc = Nokogiri::HTML(html, nil, 'utf-8')
    link = doc.search(".pager-next a").first
    return nil if link.nil? 
    link.attr(:href)
  end

  def self.extract_members(html)
    links = []
    doc = Nokogiri::HTML(html, nil, 'utf-8')
    member_rows = doc.search "table.views-table tbody tr"
    member_rows.each do |row|
      link = row.search(".views-field-field-name-value a").first
      links << "#{BASE_URL}#{link.attr(:href)}"
    end
    links
  end

  def self.scrape_member_info(url)
    puts "Scraping member info..." if console_log?
    extract_member_details ScraperWiki::scrape url
  end

  def self.extract_member_details(html)
    member = {}
    doc = Nokogiri::HTML(html, nil, 'utf-8')
    member['name'] = doc.search("div#main-inner2 div.inner h1.title").first
    member['name'] = member['name'].text unless member['name'].nil? 

    country_node = doc.search("div.field-field-country").first
    country_node.search(".field-label-inline-first").first.remove unless country_node.nil? 

    member['country'] = country_node
    member['country'] = country_node.text.strip unless member['country'].nil? 
    
    address_nodes = doc.search("div.field-field-address .field-item p")
    member['address'] = address_nodes.inject("") { |lines, line| lines << line.text + "\n" }
    member['address'].strip!
    
    category_node = doc.search("div.field-field-category").first
    category_node.search(".field-label-inline-first").first.remove unless category_node.nil? 
    member['category'] = category_node.text.strip unless category_node.nil? 
    
    member['member_since'] = doc.search(".field-field-approved-date .date-display-single").first
    member['member_since'] = Date.strptime member['member_since'].text, '%d/%m/%Y' unless member['member_since'].nil? 
    member
  end

  class Members < Array
    def <<(obj)
      super obj if valid_member?(obj)
    end

    def save
      ScraperWiki::save_sqlite ['name'], self
    end

    def valid_member?(obj)
      return false if obj.nil? 
      return false if obj['name'].nil? 
      true
    end
  end

  def self.console_log? 
    SHOW_CONSOLE_MESSAGES
  rescue NameError
    false
  end
end

SHOW_CONSOLE_MESSAGES = true
RSPOMembersScraper.start

require 'nokogiri'
 
class RSPOMembersScraper
  BASE_URL = "http://www.rspo.org"
  
  def self.members
    @members = Members.new if @members.nil? 
    @members
  end

  def self.start
    scrape_member_list "#{BASE_URL}/?page=0&q=membersearch"
  end

  def self.scrape_member_list(url)
    puts "Scraping memberlist..." if console_log?
    html = ScraperWiki::scrape url
    until (next_link = members_list_next_link(html)).nil? 
      html = ScraperWiki::scrape "#{BASE_URL}#{next_link}"
      members = extract_members html
      members.each { |m| add_to_members_array scrape_member_info(m) }
      self.members.save
      self.members.clear
    end
  end

  def self.add_to_members_array(member)
    members << member
  end

  def self.members_list_next_link(html)
    doc = Nokogiri::HTML(html, nil, 'utf-8')
    link = doc.search(".pager-next a").first
    return nil if link.nil? 
    link.attr(:href)
  end

  def self.extract_members(html)
    links = []
    doc = Nokogiri::HTML(html, nil, 'utf-8')
    member_rows = doc.search "table.views-table tbody tr"
    member_rows.each do |row|
      link = row.search(".views-field-field-name-value a").first
      links << "#{BASE_URL}#{link.attr(:href)}"
    end
    links
  end

  def self.scrape_member_info(url)
    puts "Scraping member info..." if console_log?
    extract_member_details ScraperWiki::scrape url
  end

  def self.extract_member_details(html)
    member = {}
    doc = Nokogiri::HTML(html, nil, 'utf-8')
    member['name'] = doc.search("div#main-inner2 div.inner h1.title").first
    member['name'] = member['name'].text unless member['name'].nil? 

    country_node = doc.search("div.field-field-country").first
    country_node.search(".field-label-inline-first").first.remove unless country_node.nil? 

    member['country'] = country_node
    member['country'] = country_node.text.strip unless member['country'].nil? 
    
    address_nodes = doc.search("div.field-field-address .field-item p")
    member['address'] = address_nodes.inject("") { |lines, line| lines << line.text + "\n" }
    member['address'].strip!
    
    category_node = doc.search("div.field-field-category").first
    category_node.search(".field-label-inline-first").first.remove unless category_node.nil? 
    member['category'] = category_node.text.strip unless category_node.nil? 
    
    member['member_since'] = doc.search(".field-field-approved-date .date-display-single").first
    member['member_since'] = Date.strptime member['member_since'].text, '%d/%m/%Y' unless member['member_since'].nil? 
    member
  end

  class Members < Array
    def <<(obj)
      super obj if valid_member?(obj)
    end

    def save
      ScraperWiki::save_sqlite ['name'], self
    end

    def valid_member?(obj)
      return false if obj.nil? 
      return false if obj['name'].nil? 
      true
    end
  end

  def self.console_log? 
    SHOW_CONSOLE_MESSAGES
  rescue NameError
    false
  end
end

SHOW_CONSOLE_MESSAGES = true
RSPOMembersScraper.start


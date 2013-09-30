require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'enumerator'
require 'date'
##
# Class SimpleStruct
#
class SimpleStruct
  def self.add_attributes(*attributes)
    attr_accessor *attributes
    @attributes = [] if @attributes.nil? 
    @attributes += attributes
  end
  
  # Attributes are inherited from the parents
  def self.attributes
    if superclass.instance_variable_get('@attributes')
      superclass.instance_variable_get('@attributes') + @attributes
    else
      @attributes
    end
  end
  
  def initialize(options = {})
    attributes_set(options)
  end
  
  # Throws an exception if attribute is not known. Otherwise does nothing.
  def check_attribute!(attribute)
    #raise "Unexpected attribute #{attribute} used" unless self.class.attributes && self.class.attributes.include?(attribute)
  end
  
  def attribute_set(attribute, value)
    check_attribute!(attribute)
    send(attribute.to_s + "=", value)
  end
  
  # Returns the value of an attribute
  def attribute_get(attribute)
    check_attribute!(attribute)
    send(attribute.to_s)
  end 
  
  def attributes_set(options)
    options.each do |attribute, value|
      attribute_set(attribute, value)
    end
  end
  
  # Returns a hash of attribute names and values
  def attributes_get
    h = {}
    self.class.attributes.each do |a|
      h[a] = attribute_get(a)
    end
    h
  end
  
  def==(other)
    return false unless other.kind_of?(SimpleStruct)
    attributes_get == other.attributes_get
  end
end

##
# Class::PlanningAuthorityResults
#
class PlanningAuthorityResults < SimpleStruct
  add_attributes :name, :short_name, :applications
  
  def initialize(options = {})
    @applications = []
    super options
  end
  
  def <<(da)
    @applications << da
  end
  
  def to_xml(options = {})
    options[:indent] ||= 2
    xml = options[:builder] ||= Builder::XmlMarkup.new(:indent => options[:indent])
    xml.instruct! unless options[:skip_instruct]
    xml.planning do
      xml.authority_name name
      xml.authority_short_name short_name
      xml.applications do
        applications.each do |application|
          xml << application.to_xml(:builder => Builder::XmlMarkup.new(:indent => options[:indent], :margin => 2))
        end
      end
    end
  end
end

##
# Class::DevelopmentApplication
#
class DevelopmentApplication < SimpleStruct
  add_attributes :application_id, :description, :address, :addresses, :on_notice_from, :on_notice_to, :info_url, :comment_url, :date_received
  def initialize(options = {})
    @addresses = []
    super
  end
  
  def address
    raise "Can not use address when there are several addresses" if addresses.size > 1
    addresses.first
  end
  
  def address=(a)
    @addresses = [a]
  end

  def info_url=(url)
    @info_url = parse_url(url)
  end
  
  def comment_url=(url)
    @comment_url = parse_url(url)
  end
  
  def on_notice_from=(date)
    @on_notice_from = parse_date(date)
  end
  
  def on_notice_to=(date)
    @on_notice_to = parse_date(date)
  end
  
  def date_received=(date)
    @date_received = parse_date(date)
  end
  
  def to_xml(options = {})
    options[:indent] ||= 2
    xml = options[:builder] ||= Builder::XmlMarkup.new(:indent => options[:indent])
    addresses.each do |a|
      xml.application do
        xml.council_reference application_id
        xml.address a
        xml.description description
        xml.info_url info_url
        xml.comment_url comment_url
        xml.date_received date_received
        xml.on_notice_from on_notice_from if on_notice_from
        xml.on_notice_to on_notice_to if on_notice_to
      end
    end
    # Hack to return type of object you would normally expect
    xml.text!("")
  end
  
  private
  
  def parse_date(date)
    if date && !date.kind_of?(Date)
      begin
        Date.parse(date)
      rescue
        nil
      end
    else
      date
    end
  end
  
  def parse_url(url)
    if url && !url.kind_of?(URI)
      URI.parse(url)
    else
      url
    end
  end
end

##
#Class::ScraperBase
#
class ScraperBase
  attr_reader :planning_authority_short_name, :state, :scraperwiki_name
  
  def initialize(name, short_name, state)
    @planning_authority_name, @planning_authority_short_name, @state = name, short_name, state
  end
  
  # Append the state/territory onto the planning authority name
  def planning_authority_name
    planning_authority_name_no_state + ", " + state
  end
  
  def planning_authority_name_no_state
    @planning_authority_name
  end
  
  # A version of the short name that is encoded for use in url's
  def planning_authority_short_name_encoded
    planning_authority_short_name.downcase.gsub(' ', '_').gsub(/\W/, '')
  end 
end
##
# Class::Scraper
#

class Scraper < ScraperBase
  attr_reader :agent

  def initialize(name, short_name, state)
    super
    @agent = Mechanize.new
  end
  
  def extract_relative_url(html)
    agent.page.uri + URI.parse(html.at('a').attributes['href'])
  end
  
  def email_url(to, subject, body = nil)
    v = "mailto:#{to}?subject=#{URI.escape(subject)}"
    v += "&Body=#{URI.escape(body)}" if body
    v
  end
  
  def simplify_whitespace(str)
    str.gsub(/[\n\t\r]/, " ").squeeze(" ")
  end
  
  def results_as_xml(date)
    results(date).to_xml
  end
  
  def results(date)
    PlanningAuthorityResults.new(:name => planning_authority_name, :short_name => planning_authority_short_name,
      :applications => applications(date))
  end
end

##
# Class::ACTScraper
#
class ACTScraper < Scraper
  def applications(date)
    url = "http://www.actpla.act.gov.au/topics/your_say/comment/pubnote"
    page = agent.get(url)
    # The way that Mechanize is invoking Nokogiri for parsing the html is for some reason not working with this html which
    # is malformed: See http://validator.w3.org/check?uri=http://apps.actpla.act.gov.au/pubnote/index.asp&charset=(detect+automatically)&doctype=Inline&group=0
    # It's chopping out the content that we're interested in. So, doing the parsing explicitly so we can control how it's done.
    page = Nokogiri::HTML(page.body)
    
    # Walking through the lines. Every 7 lines is a new application
    applications = []
    page.search('table')[1].search('tr').each_slice(7) do |lines|
      # First double check that each line has the correct form
      labels = lines.map do |line|
        if line.at('strong')
          line.at('strong').inner_text
        elsif line.at('b')
          line.at('b').inner_text
        end
      end
      
      raise "Unexpected form for suburb line" unless lines[0].at('a').has_attribute?('name')
      raise "Unexpected form application_id line" unless labels[1] == "Development Application:"
      raise "Unexpected form address line" unless labels[2] == "Address:"
      raise "Unexpected form block line" unless labels[3] == "Block: "
      raise "Unexpected form description line" unless labels[4] == "Proposal:"
      raise "Unexpected form on notice to line" unless labels[5] == "Period for representations closes:"
      raise "Unexpected form info url line" unless lines[6].at('a').inner_text == "Click here to view the plans"
      
      lines[1].at('strong').remove
      lines[2].at('strong').remove
      lines[4].at('strong').remove
      lines[5].at('strong').remove
      stripped = lines.map{|l| l.inner_text.strip}
      
      applications << DevelopmentApplication.new(
        :application_id => stripped[1],
        :address => stripped[2] + ", " + stripped[0] + ", " + state,
        :description => stripped[4],
        :on_notice_to => (stripped[5] if stripped[5] != ""),
        :info_url => extract_relative_url(lines[6]),
        :comment_url => url)  
    end
    applications.each do |app|
      row = {
        :application_id => app.application_id,
        :address => app.address,
        :description => app.description,
        :on_notice_to => app.on_notice_to,
        :info_url => app.info_url,
        :comment_url => app.comment_url
      }
      
      ScraperWiki.save_sqlite([:application_id], row)
    end
    #puts applications[0].inspect
    #puts applications[0].application_id
    #puts applications.inspect
    #applications
  end
end

new_scraper = ACTScraper.new("ACT Planning & Land Authority", "ACT", "ACT")
new_scraper.applications(Date.today)

=begin
  ##
  # Enherit example
  #
  class Rectangle
    def initialize(width, height)
      @width, @height = width, height
    end
    def area
      @width * @height
    end
  end
  class Square < Rectangle
    def initialize(width)
      super(width, width)
    end
  end
  puts "aaaaaaaaaaaa"
  puts Square.new(10).area #=> 100
=endrequire 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'enumerator'
require 'date'
##
# Class SimpleStruct
#
class SimpleStruct
  def self.add_attributes(*attributes)
    attr_accessor *attributes
    @attributes = [] if @attributes.nil? 
    @attributes += attributes
  end
  
  # Attributes are inherited from the parents
  def self.attributes
    if superclass.instance_variable_get('@attributes')
      superclass.instance_variable_get('@attributes') + @attributes
    else
      @attributes
    end
  end
  
  def initialize(options = {})
    attributes_set(options)
  end
  
  # Throws an exception if attribute is not known. Otherwise does nothing.
  def check_attribute!(attribute)
    #raise "Unexpected attribute #{attribute} used" unless self.class.attributes && self.class.attributes.include?(attribute)
  end
  
  def attribute_set(attribute, value)
    check_attribute!(attribute)
    send(attribute.to_s + "=", value)
  end
  
  # Returns the value of an attribute
  def attribute_get(attribute)
    check_attribute!(attribute)
    send(attribute.to_s)
  end 
  
  def attributes_set(options)
    options.each do |attribute, value|
      attribute_set(attribute, value)
    end
  end
  
  # Returns a hash of attribute names and values
  def attributes_get
    h = {}
    self.class.attributes.each do |a|
      h[a] = attribute_get(a)
    end
    h
  end
  
  def==(other)
    return false unless other.kind_of?(SimpleStruct)
    attributes_get == other.attributes_get
  end
end

##
# Class::PlanningAuthorityResults
#
class PlanningAuthorityResults < SimpleStruct
  add_attributes :name, :short_name, :applications
  
  def initialize(options = {})
    @applications = []
    super options
  end
  
  def <<(da)
    @applications << da
  end
  
  def to_xml(options = {})
    options[:indent] ||= 2
    xml = options[:builder] ||= Builder::XmlMarkup.new(:indent => options[:indent])
    xml.instruct! unless options[:skip_instruct]
    xml.planning do
      xml.authority_name name
      xml.authority_short_name short_name
      xml.applications do
        applications.each do |application|
          xml << application.to_xml(:builder => Builder::XmlMarkup.new(:indent => options[:indent], :margin => 2))
        end
      end
    end
  end
end

##
# Class::DevelopmentApplication
#
class DevelopmentApplication < SimpleStruct
  add_attributes :application_id, :description, :address, :addresses, :on_notice_from, :on_notice_to, :info_url, :comment_url, :date_received
  def initialize(options = {})
    @addresses = []
    super
  end
  
  def address
    raise "Can not use address when there are several addresses" if addresses.size > 1
    addresses.first
  end
  
  def address=(a)
    @addresses = [a]
  end

  def info_url=(url)
    @info_url = parse_url(url)
  end
  
  def comment_url=(url)
    @comment_url = parse_url(url)
  end
  
  def on_notice_from=(date)
    @on_notice_from = parse_date(date)
  end
  
  def on_notice_to=(date)
    @on_notice_to = parse_date(date)
  end
  
  def date_received=(date)
    @date_received = parse_date(date)
  end
  
  def to_xml(options = {})
    options[:indent] ||= 2
    xml = options[:builder] ||= Builder::XmlMarkup.new(:indent => options[:indent])
    addresses.each do |a|
      xml.application do
        xml.council_reference application_id
        xml.address a
        xml.description description
        xml.info_url info_url
        xml.comment_url comment_url
        xml.date_received date_received
        xml.on_notice_from on_notice_from if on_notice_from
        xml.on_notice_to on_notice_to if on_notice_to
      end
    end
    # Hack to return type of object you would normally expect
    xml.text!("")
  end
  
  private
  
  def parse_date(date)
    if date && !date.kind_of?(Date)
      begin
        Date.parse(date)
      rescue
        nil
      end
    else
      date
    end
  end
  
  def parse_url(url)
    if url && !url.kind_of?(URI)
      URI.parse(url)
    else
      url
    end
  end
end

##
#Class::ScraperBase
#
class ScraperBase
  attr_reader :planning_authority_short_name, :state, :scraperwiki_name
  
  def initialize(name, short_name, state)
    @planning_authority_name, @planning_authority_short_name, @state = name, short_name, state
  end
  
  # Append the state/territory onto the planning authority name
  def planning_authority_name
    planning_authority_name_no_state + ", " + state
  end
  
  def planning_authority_name_no_state
    @planning_authority_name
  end
  
  # A version of the short name that is encoded for use in url's
  def planning_authority_short_name_encoded
    planning_authority_short_name.downcase.gsub(' ', '_').gsub(/\W/, '')
  end 
end
##
# Class::Scraper
#

class Scraper < ScraperBase
  attr_reader :agent

  def initialize(name, short_name, state)
    super
    @agent = Mechanize.new
  end
  
  def extract_relative_url(html)
    agent.page.uri + URI.parse(html.at('a').attributes['href'])
  end
  
  def email_url(to, subject, body = nil)
    v = "mailto:#{to}?subject=#{URI.escape(subject)}"
    v += "&Body=#{URI.escape(body)}" if body
    v
  end
  
  def simplify_whitespace(str)
    str.gsub(/[\n\t\r]/, " ").squeeze(" ")
  end
  
  def results_as_xml(date)
    results(date).to_xml
  end
  
  def results(date)
    PlanningAuthorityResults.new(:name => planning_authority_name, :short_name => planning_authority_short_name,
      :applications => applications(date))
  end
end

##
# Class::ACTScraper
#
class ACTScraper < Scraper
  def applications(date)
    url = "http://www.actpla.act.gov.au/topics/your_say/comment/pubnote"
    page = agent.get(url)
    # The way that Mechanize is invoking Nokogiri for parsing the html is for some reason not working with this html which
    # is malformed: See http://validator.w3.org/check?uri=http://apps.actpla.act.gov.au/pubnote/index.asp&charset=(detect+automatically)&doctype=Inline&group=0
    # It's chopping out the content that we're interested in. So, doing the parsing explicitly so we can control how it's done.
    page = Nokogiri::HTML(page.body)
    
    # Walking through the lines. Every 7 lines is a new application
    applications = []
    page.search('table')[1].search('tr').each_slice(7) do |lines|
      # First double check that each line has the correct form
      labels = lines.map do |line|
        if line.at('strong')
          line.at('strong').inner_text
        elsif line.at('b')
          line.at('b').inner_text
        end
      end
      
      raise "Unexpected form for suburb line" unless lines[0].at('a').has_attribute?('name')
      raise "Unexpected form application_id line" unless labels[1] == "Development Application:"
      raise "Unexpected form address line" unless labels[2] == "Address:"
      raise "Unexpected form block line" unless labels[3] == "Block: "
      raise "Unexpected form description line" unless labels[4] == "Proposal:"
      raise "Unexpected form on notice to line" unless labels[5] == "Period for representations closes:"
      raise "Unexpected form info url line" unless lines[6].at('a').inner_text == "Click here to view the plans"
      
      lines[1].at('strong').remove
      lines[2].at('strong').remove
      lines[4].at('strong').remove
      lines[5].at('strong').remove
      stripped = lines.map{|l| l.inner_text.strip}
      
      applications << DevelopmentApplication.new(
        :application_id => stripped[1],
        :address => stripped[2] + ", " + stripped[0] + ", " + state,
        :description => stripped[4],
        :on_notice_to => (stripped[5] if stripped[5] != ""),
        :info_url => extract_relative_url(lines[6]),
        :comment_url => url)  
    end
    applications.each do |app|
      row = {
        :application_id => app.application_id,
        :address => app.address,
        :description => app.description,
        :on_notice_to => app.on_notice_to,
        :info_url => app.info_url,
        :comment_url => app.comment_url
      }
      
      ScraperWiki.save_sqlite([:application_id], row)
    end
    #puts applications[0].inspect
    #puts applications[0].application_id
    #puts applications.inspect
    #applications
  end
end

new_scraper = ACTScraper.new("ACT Planning & Land Authority", "ACT", "ACT")
new_scraper.applications(Date.today)

=begin
  ##
  # Enherit example
  #
  class Rectangle
    def initialize(width, height)
      @width, @height = width, height
    end
    def area
      @width * @height
    end
  end
  class Square < Rectangle
    def initialize(width)
      super(width, width)
    end
  end
  puts "aaaaaaaaaaaa"
  puts Square.new(10).area #=> 100
=end
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
    raise "Unexpected attribute #{attribute} used" unless self.class.attributes && self.class.attributes.include?(attribute)
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
#Class::AlburyScraper
#
class AlburyScraper < Scraper
  def applications(date)
    # Doesn't seem to work without that nodeNum. I wonder what it is.
    url = "https://eservice.alburycity.nsw.gov.au/eservice/advertisedDAs.do?nodeNum=252"
    # We can't give a link directly to an application. Bummer. So, giving link to the search page
    info_url = "https://eservice.alburycity.nsw.gov.au/eservice/daEnquiryInit.do?nodeNum=252"
    comment_url = "http://www.alburycity.nsw.gov.au/www/html/704-register-of-development-applications-determined-by-the-council.asp"
    page = agent.get(url)
    
    # The applications are grouped by suburb. So, stepping through so we can track the current suburb
    current_suburb = nil
    applications = []
    page.at('#fullcontent .bodypanel').children.each do |block|
      case block.name
      when "text", "comment", "script"
        # Do nothing
      when "h4"
        current_suburb = block.inner_text.strip
      when "table"
        address = block.search('tr')[0].inner_text.strip + ", " + current_suburb + ", " + state
        description = block.search('tr')[1].search('td')[2].inner_text.strip
        application_id = block.search('tr')[3].search('td')[2].inner_text.strip
        on_notice_text = block.search('tr')[4].search('td')[2].inner_text.strip
        if on_notice_text =~ /(\d+\/\d+\/\d+)\s+Submissions close\s+(\d+\/\d+\/\d+)/
          on_notice_from, on_notice_to = $~[1..2]
        else
          raise "Unexpected form for text: #{on_notice_text}"
        end
        applications << DevelopmentApplication.new(
          :address => address,
          :description => description,
          :application_id => application_id,
          :on_notice_from => on_notice_from,
          :on_notice_to => on_notice_to,
          :info_url => info_url,
          :comment_url => comment_url)
      else
        raise "Unexpected type: #{block.name}"
      end
    end
    puts "test 01"
    #applications
    #puts applications.inspect
  end
end

new_scraper = AlburyScraper.new("Albury City Council", "Albury", "NSW")
new_scraper.applications(Date.new(2012,3,4))
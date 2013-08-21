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
#
#
class BoroondaraScraper < Scraper
  # Boroondara don't provide a search by date, so we have to use their fetch by 
  # last week and this week. Hopefully this is enough for the alerting service
  BASE_URLS = ["http://eservices.boroondara.vic.gov.au/EPlanning/Pages/XC.Track/SearchApplication.aspx?d=lastweek&k=LodgementDate&t=PlnPermit",
               "http://eservices.boroondara.vic.gov.au/EPlanning/Pages/XC.Track/SearchApplication.aspx?d=thisweek&k=LodgementDate&t=PlnPermit"]

  # A general page (applicable to all applications) for downloading an "objections" form
  COMMENT_URL = "http://boroondara.vic.gov.au/your_council/building-planning/stat-planning/resources/objections"
  
  def extract_applications_from_page(page, date)
  applications = []
        links = page.links_with(:href => /SearchApplication.aspx\?id=\d+/)
        links.each do |link|
            app_page = link.click
            da = DevelopmentApplication.new(:info_url => app_page.uri)
            da.application_id = app_page.search('h1')[1].inner_text.strip.sub(/Reference number: /, "")
            da.comment_url = COMMENT_URL
            rows = app_page.search('.detail')
            rows.each do |row|
                label = row.at('.detailleft').inner_text.strip
                value = row.at('.detailright')
                case label
                    when /properties/i
                        da.address = value.at('a').inner_text.strip #site incorrectly repeats the same address
                    when /submitted/i
                        da.date_received = value.inner_text.strip    

                    when /description/i
                        da.description = value.inner_text.strip.sub(/planning permit/i, "")    
                end

            end
           applications << da
        end    
  applications
  end


  def applications(date)

    applications = []

    BASE_URLS.each do |url|

      page = agent.get(url)
      form = page.forms.first
      page = form.submit(form.button_with(:name => /BtnAgree/)) # only needed for the first page

      # get the first page of applications
      applications += extract_applications_from_page(page, date)

      # the paging is done via onlick javascript
      next_links = page.search("//a[@onclick]")
      next_links.each do |link|
        # for each onclick we extract the parameters and pass these in a GET request
        link.to_s.match /'pager','(\d+\|.*)'/
        link_mod = page.uri.to_s + "&__EVENTTARGET=pager&__EVENTARGUMENT=#{$1}"
      newpage = agent.get(link_mod)

        # and extract the applications from the newpage
        applications+= extract_applications_from_page(newpage, date)
      end
    end
  applications
  applications.each do |app|
      row = {
        :application_id => app.application_id,
        :address => app.address,
        :description => app.description,
        :on_notice_to => app.on_notice_to,
        :info_url => app.info_url,
        :comment_url => app.comment_url,
        :date_received => app.date_received
      }
      
      ScraperWiki.save_sqlite([:application_id], row)
  end
  #puts applications.inspect
  #puts applications.length
  end
end

new_scraper = BoroondaraScraper.new("Boroondara City Council", "Boroondara (City)", "VIC")
new_scraper.applications(Date.today)
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
class InfoMasterScraper < Scraper
  def raw_table_values(date, url, rows_to_skip_at_start, table_search = 'span > table', rows_to_skip_at_end = 0)
    range = rows_to_skip_at_start..(-1-rows_to_skip_at_end)
    rows = get_page(date, url).search(table_search).search('tr')
    return [] if rows.nil? || rows.size < rows_to_skip_at_start
    values = rows[range].map {|row| row.search('td')}
    values.delete_if {|row| row.inner_text =~ /\A\s*\Z/} #some InfoMaster installations insert a blank every second row, we can just remove these
    first_row = values.first
    return [] if first_row.nil? || first_row.first.inner_text =~ /no applications found/i || first_row.first.inner_text =~ /no results found/i || first_row.first.inner_text =~ /no records matching/i
    values
  end
  
  def get_page(date, url)
    page = agent.get(url)
    
    # Click the Ok button on the form
    form = page.forms_with(:name => /frmMasterView|frmMasterPlan|frmApplicationMaster/).first
    form.submit(form.button_with(:name => /btnOk|Yes|Button1|Agree/))

    # Get the page again
    page = agent.get(url)

    search_form = page.forms_with(:name => /frmMasterView|frmMasterPlan|frmApplicationMaster/).first
    
    if search_form.field_with(:name => /txtFrom/).nil? 
      search_form[search_form.field_with(:name => /drDates:txtDay1/).name] = date.day
      search_form[search_form.field_with(:name => /drDates:txtMonth1/).name] = date.month
      search_form[search_form.field_with(:name => /drDates:txtYear1/).name] = date.year
      search_form[search_form.field_with(:name => /drDates:txtDay2/).name] = date.day
      search_form[search_form.field_with(:name => /drDates:txtMonth2/).name] = date.month
      search_form[search_form.field_with(:name => /drDates:txtYear2/).name] = date.year
    else
      search_form[search_form.field_with(:name => /txtFrom/).name] = "#{date.day}/#{date.month}/#{date.year}"
      search_form[search_form.field_with(:name => /txtTo/).name] = "#{date.day}/#{date.month}/#{date.year}"
    end

    search_form.submit(search_form.button_with(:name => /btnSearch|SearchBtn/))
    # TODO: Need to handle what happens when the results span multiple pages. Can this happen?
  end
  
  def extract_date_received(html)
    inner(html)
  end
  
  def extract_application_id(html)
    simplify_whitespace(inner(html))
  end
  
  def extract_address_without_state(html, lines = 0..0)
    simplify_whitespace(split_lines(html)[lines].join(" "))
  end
  
  def extract_address(html, lines = 0..0)
    extract_address_without_state(html, lines) + ", " + state
  end
  
  def extract_description(html, lines = -1..-1)
    split_lines(html)[lines].join("\n").strip
  end
  
  def extract_info_url(html)
    html.at('a').attributes['href']
  end
  
  def inner(html)
    html.inner_html.strip
  end
  
  def convert_html_entities(str)
    HTMLEntities.new.decode(str)
  end
  
  def split_lines(html)
    html.inner_html.split('<br>').map{|s| convert_html_entities(strip_html_tags(s)).strip.gsub("\r", "\n")}
  end
  
  def strip_html_tags(str)
    str.gsub(/<\/?[^>]*>/, "")
  end
end

##
#Class::HornsbyScraper
#
class HornsbyScraper < InfoMasterScraper
  def applications(date)
    base_path = "http://hsconline.hornsby.nsw.gov.au/appenquiry/modules/applicationmaster/"
    base_url = base_path + "default.aspx"
    raw_table_values(date, "#{base_url}?page=search", 1).map do |values|
      
      #Example description column in applications listing:
      #NUM ROAD SUBURB STATE POSTCODE
      #DESCRIPTION TEXT
      #Applicant: ...

      da = DevelopmentApplication.new(
        :application_id => extract_application_id(values[1]),
        :date_received => extract_date_received(values[2]),
        :address => extract_address_without_state(values[3]),
        :description => extract_description(values[3],1..1)
      )
      
      application_number = da.application_id
      application_year=""
      
      da.info_url = URI.escape(base_path + extract_info_url(values[0]))
      da.comment_url = da.info_url
      da
      puts "pvlam"
      puts da.inspect
    end
  end
end

new_scraper = HornsbyScraper.new("Hornsby Shire Council", "Hornsby", "NSW")
new_scraper.applications(Date.new(2012,3,3))
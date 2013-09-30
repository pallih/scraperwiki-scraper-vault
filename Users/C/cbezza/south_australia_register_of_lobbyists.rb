require 'pdf-reader'   
require 'open-uri'
require 'yaml'
class Array
  def to_yaml_style
    :inline
  end
end

##########  This section contains the callback code that processes the PDF file contents  ######
class PageTextReceiver
  attr_accessor :content, :page_counter
  def initialize
    @content = []
    @page_counter = 0
  end
  # Called when page parsing starts
  def begin_page(arg = nil)
    @page_counter += 1
    @content << ""
  end
  # record text that is drawn on the page
  def show_text(string, *params)
    if string != ""
      @content.last << string
    end
  end

  def end_text_object(*params)
    @content << ""
  end

  # there's a few text callbacks, so make sure we process them all
  alias :super_show_text :show_text
  alias :move_to_next_line_and_show_text :show_text
  alias :set_spacing_next_line_show_text :show_text
  # this final text callback takes slightly different arguments
  def show_text_with_positioning(*params)
    params = params.first
    params.each { |str| show_text(str) if str.kind_of?(String)}
  end
end
################  End of TextReceiver #############################

base_url = "http://www.premcab.sa.gov.au/lobbyist/"
html = ScraperWiki.scrape("http://www.premcab.sa.gov.au/lobbyist/registered_listing.html")

# Next we use Nokogiri to extract the values from the HTML source.

require 'nokogiri'
page = Nokogiri::HTML(html)

urls = page.at('#table1').search('a').map {|a| a.attributes['href']}

# resume from the last incomplete url if the scraper was terminated
resumeFromHere = false
last_url = ScraperWiki.get_var("last_url", "")
if last_url == "" then resumeFromHere = true end

urls.each do |url|
  url = base_url + url
  if url == last_url or last_url == "" then resumeFromHere = true end
  if resumeFromHere
    print "Fetching #{url}"
    ScraperWiki.save_var("last_url", url)
  
    lines = []
    lobbyist = {"employees" => [], "clients" => [], "owners" => []}
    #######  Instantiate the receiver and the reader
    receiver = PageTextReceiver.new
    pdf_reader = PDF::Reader.new 
    begin
    pdf = open(url)
    pdf_reader.parse(pdf, receiver)
    lineno = 0
    receiver.content.each do |line|    
       line = line.strip
       lineno = lineno + 1
       case line
       when "", "View Lobbyist Details", "Lobbyist Details",/By completing this form/
       when /(.*)Details last updated\:(.*)/
           #special case
           lineparts = line.split("Details last updated\:")
           if lineparts.length == 2
               lobbyist["last_updated"] = lineparts[1]
           end
       when /:/, "Client Details", "Owner Details", "Details of all persons or employees who conduct lobbying activities", "Details last updated:"
         puts "Loading header: #{line}"
         lines << line
       else
         puts "Loading line: #{line}"
         lines[-1] += " " + line
       end
     end
   
     in_employees = false
     in_clients = false
     in_owners = false

     name_next = false     
     position_next = false  

     lines.each do |line|
       line = line.strip
       #puts "Processing line: #{line}"
       case line
       when /^Business Entity Name: (.*)/
         lobbyist["business_name"] = $~[1].strip
         puts "Processing records for #{lobbyist['business_name']} #{url}"
       when /^ABN: (.*)/
         lobbyist["abn"] = $~[1].to_s.strip.delete(' ').delete('.').to_i
       when /^ACN: (.*)/
         lobbyist["abn"] = $~[1].strip # not strictly true but unique identifier
       when /^Trading Name: (.*)/
         if $~[1].strip != nil then
           lobbyist["trading_name"] = $~[1].strip
         end
       when "Trading Name:"
         puts "Empty trading name in #{lobbyist['business_name']} #{lobbyist['abn']}, Line =  #{line}"
       when "Details of all persons or employees who conduct lobbying activities"
         in_employees = true
         in_clients = false
         in_owners = false
       when "Client Details"
         in_employees = false
         in_clients = true
         in_owners = false
       when "Owner Details"
         in_employees = false
         in_clients = false
         in_owners = true
       when /^Name: (.*)/
         name = { "name" => $~[1].strip }
         if in_employees
           lobbyist["employees"] << name
         elsif in_clients
           lobbyist["clients"] << name
         elsif in_owners
           lobbyist["owners"] << name
         else
           raise "Name in an unexpected place '#{line}' #{lineno}"
         end
       when /^Position: (.*)/
         if in_employees
           lobbyist["employees"].last["position"] = $~[1].strip
         else
           raise "Position in an unexpected place '#{line}' #{lineno}"
         end
       when /^Details last updated: (.*)/
         lobbyist["last_updated"] = $~[1].strip      
       when /^including: (.*)/ # special case for some lobbying consortium
         lobbyist["clients"] << "The Australian Institute of Architects"
         lobbyist["clients"] << "Consult Australia"
         lobbyist["clients"] << "CPA Australia"
         lobbyist["clients"] << "Engineers Australia"
         lobbyist["clients"] << "The Institute of Chartered Accountants in Australia"
         lobbyist["clients"] << "The National Institute of Accountants"
         lobbyist["clients"] << "Professions Australia"
         lobbyist["clients"] << "Deloitte"
         lobbyist["clients"] << "Ernst & Young"
         lobbyist["clients"] << "KPMG"
         lobbyist["clients"] << "PricewaterhouseCoopers"
       when /Owner Details Adelaide/,/Please see the following page for owner detail/
           lobbyist["owners"] << "See #{url} for details"
           break; #KPMG have pages and pages of owners
       when /Name:/
           name_next = true
       when /Position:/
           position_next = true
       else
          if name_next
            name = { "name" => line.strip }
            if in_employees
              lobbyist["employees"] << name
               name_next = false
            elsif in_clients
              lobbyist["clients"] << name
               name_next = false
            elsif in_owners
              lobbyist["owners"] << name
               name_next = false
            else
              raise "Name in an unexpected place '#{line}' #{lineno}"
            end
          end
          if position_next
            if in_employees
              lobbyist["employees"].last["position"] = $~[1].strip
              position_next = false
            else
              raise "Position in an unexpected place '#{line}' #{lineno}"
            end
          end
          raise "Don't know what to do with: '#{line}' #{lineno}"  
           
       end
     end 
     lobbyist["employees"] = lobbyist["employees"].to_yaml
     lobbyist["clients"] = lobbyist["clients"].to_yaml
     lobbyist["owners"] = lobbyist["owners"].to_yaml
    
     ScraperWiki.save(unique_keys=["business_name","abn"],data=lobbyist)
     rescue Timeout::Error => e
        print "Timeout on #{url}"
     end
  else
    print "Skipping #{url} \n"
  end
end
ScraperWiki.save_var("last_url", "")require 'pdf-reader'   
require 'open-uri'
require 'yaml'
class Array
  def to_yaml_style
    :inline
  end
end

##########  This section contains the callback code that processes the PDF file contents  ######
class PageTextReceiver
  attr_accessor :content, :page_counter
  def initialize
    @content = []
    @page_counter = 0
  end
  # Called when page parsing starts
  def begin_page(arg = nil)
    @page_counter += 1
    @content << ""
  end
  # record text that is drawn on the page
  def show_text(string, *params)
    if string != ""
      @content.last << string
    end
  end

  def end_text_object(*params)
    @content << ""
  end

  # there's a few text callbacks, so make sure we process them all
  alias :super_show_text :show_text
  alias :move_to_next_line_and_show_text :show_text
  alias :set_spacing_next_line_show_text :show_text
  # this final text callback takes slightly different arguments
  def show_text_with_positioning(*params)
    params = params.first
    params.each { |str| show_text(str) if str.kind_of?(String)}
  end
end
################  End of TextReceiver #############################

base_url = "http://www.premcab.sa.gov.au/lobbyist/"
html = ScraperWiki.scrape("http://www.premcab.sa.gov.au/lobbyist/registered_listing.html")

# Next we use Nokogiri to extract the values from the HTML source.

require 'nokogiri'
page = Nokogiri::HTML(html)

urls = page.at('#table1').search('a').map {|a| a.attributes['href']}

# resume from the last incomplete url if the scraper was terminated
resumeFromHere = false
last_url = ScraperWiki.get_var("last_url", "")
if last_url == "" then resumeFromHere = true end

urls.each do |url|
  url = base_url + url
  if url == last_url or last_url == "" then resumeFromHere = true end
  if resumeFromHere
    print "Fetching #{url}"
    ScraperWiki.save_var("last_url", url)
  
    lines = []
    lobbyist = {"employees" => [], "clients" => [], "owners" => []}
    #######  Instantiate the receiver and the reader
    receiver = PageTextReceiver.new
    pdf_reader = PDF::Reader.new 
    begin
    pdf = open(url)
    pdf_reader.parse(pdf, receiver)
    lineno = 0
    receiver.content.each do |line|    
       line = line.strip
       lineno = lineno + 1
       case line
       when "", "View Lobbyist Details", "Lobbyist Details",/By completing this form/
       when /(.*)Details last updated\:(.*)/
           #special case
           lineparts = line.split("Details last updated\:")
           if lineparts.length == 2
               lobbyist["last_updated"] = lineparts[1]
           end
       when /:/, "Client Details", "Owner Details", "Details of all persons or employees who conduct lobbying activities", "Details last updated:"
         puts "Loading header: #{line}"
         lines << line
       else
         puts "Loading line: #{line}"
         lines[-1] += " " + line
       end
     end
   
     in_employees = false
     in_clients = false
     in_owners = false

     name_next = false     
     position_next = false  

     lines.each do |line|
       line = line.strip
       #puts "Processing line: #{line}"
       case line
       when /^Business Entity Name: (.*)/
         lobbyist["business_name"] = $~[1].strip
         puts "Processing records for #{lobbyist['business_name']} #{url}"
       when /^ABN: (.*)/
         lobbyist["abn"] = $~[1].to_s.strip.delete(' ').delete('.').to_i
       when /^ACN: (.*)/
         lobbyist["abn"] = $~[1].strip # not strictly true but unique identifier
       when /^Trading Name: (.*)/
         if $~[1].strip != nil then
           lobbyist["trading_name"] = $~[1].strip
         end
       when "Trading Name:"
         puts "Empty trading name in #{lobbyist['business_name']} #{lobbyist['abn']}, Line =  #{line}"
       when "Details of all persons or employees who conduct lobbying activities"
         in_employees = true
         in_clients = false
         in_owners = false
       when "Client Details"
         in_employees = false
         in_clients = true
         in_owners = false
       when "Owner Details"
         in_employees = false
         in_clients = false
         in_owners = true
       when /^Name: (.*)/
         name = { "name" => $~[1].strip }
         if in_employees
           lobbyist["employees"] << name
         elsif in_clients
           lobbyist["clients"] << name
         elsif in_owners
           lobbyist["owners"] << name
         else
           raise "Name in an unexpected place '#{line}' #{lineno}"
         end
       when /^Position: (.*)/
         if in_employees
           lobbyist["employees"].last["position"] = $~[1].strip
         else
           raise "Position in an unexpected place '#{line}' #{lineno}"
         end
       when /^Details last updated: (.*)/
         lobbyist["last_updated"] = $~[1].strip      
       when /^including: (.*)/ # special case for some lobbying consortium
         lobbyist["clients"] << "The Australian Institute of Architects"
         lobbyist["clients"] << "Consult Australia"
         lobbyist["clients"] << "CPA Australia"
         lobbyist["clients"] << "Engineers Australia"
         lobbyist["clients"] << "The Institute of Chartered Accountants in Australia"
         lobbyist["clients"] << "The National Institute of Accountants"
         lobbyist["clients"] << "Professions Australia"
         lobbyist["clients"] << "Deloitte"
         lobbyist["clients"] << "Ernst & Young"
         lobbyist["clients"] << "KPMG"
         lobbyist["clients"] << "PricewaterhouseCoopers"
       when /Owner Details Adelaide/,/Please see the following page for owner detail/
           lobbyist["owners"] << "See #{url} for details"
           break; #KPMG have pages and pages of owners
       when /Name:/
           name_next = true
       when /Position:/
           position_next = true
       else
          if name_next
            name = { "name" => line.strip }
            if in_employees
              lobbyist["employees"] << name
               name_next = false
            elsif in_clients
              lobbyist["clients"] << name
               name_next = false
            elsif in_owners
              lobbyist["owners"] << name
               name_next = false
            else
              raise "Name in an unexpected place '#{line}' #{lineno}"
            end
          end
          if position_next
            if in_employees
              lobbyist["employees"].last["position"] = $~[1].strip
              position_next = false
            else
              raise "Position in an unexpected place '#{line}' #{lineno}"
            end
          end
          raise "Don't know what to do with: '#{line}' #{lineno}"  
           
       end
     end 
     lobbyist["employees"] = lobbyist["employees"].to_yaml
     lobbyist["clients"] = lobbyist["clients"].to_yaml
     lobbyist["owners"] = lobbyist["owners"].to_yaml
    
     ScraperWiki.save(unique_keys=["business_name","abn"],data=lobbyist)
     rescue Timeout::Error => e
        print "Timeout on #{url}"
     end
  else
    print "Skipping #{url} \n"
  end
end
ScraperWiki.save_var("last_url", "")
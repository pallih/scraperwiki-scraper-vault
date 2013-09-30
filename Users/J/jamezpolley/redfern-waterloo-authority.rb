require 'rubygems'
require 'mechanize'
require 'date'

agent = Mechanize.new
url = 'http://www.redfernwaterloo.nsw.gov.au/development_applications/development_proposals_on_exhibition.htm'
page = agent.get(url)

class Saver
  def initialize
    #If you want to trample on existing data, set this to true
    @trample_data = false
    @references = (ScraperWiki.select("council_reference from swdata") rescue nil)
  end

  def save(record)
    if record
      if @trample_data || @references.nil? || !@references.include?(record['council_reference'])
        ScraperWiki.save_sqlite(['council_reference'], record)
      else
        puts "Skipping already saved record " + record['council_reference']
      end
    end
  end
end

def scrubbed(text)
  text = text.gsub(/[\r\n]/){$1}
  text = text.gsub(/\t/){' '}
  text = text.gsub(/ +/){' '}
  return text
end

record_saver = Saver.new

record = nil

page.search('table table table table table table table table tr').each do |r|
  next unless r.search('td')[1]
  header = scrubbed r.search('td')[0].search('b').inner_text
  data = r.search('td')[1]
  case
    when header =~ /Application/ then
      record_saver.save record
      council_reference = scrubbed data.search('a')[0].inner_text
      record = {
        'info_url' => url,
        'date_scraped' => Date.today.to_s,
        'council_reference' => council_reference,
        'comment_url' => "mailto:redfernwaterloo@rwa.nsw.gov.au",
      }
    when header == "Location" then record['address'] = scrubbed data.inner_text + ", NSW"
    when header == "Proposal" then record['description'] = scrubbed data.inner_text
    when header == "Exhibition Dates" then
       full_date_string = scrubbed data.inner_text
       from_date_string, to_date_string = full_date_string.split(" to ")
       to_date, to_month, to_year = to_date_string.split

       case
         when from_date_string.split.size == 1 then
           from_date = from_date_string
           from_month = to_month
           from_year = to_year
         when from_date_string.split.size == 2 then
           from_date, from_month = from_date_string.split
           from_year = to_year
         when from_date_string.split.size == 3 then
           from_date, from_month, from_year = from_date_string.split
       end

       record['on_notice_from'] = Date.parse("#{from_date} #{from_month} #{from_year}").to_s
       record['on_notice_to'] = Date.parse("#{to_date} #{to_month} #{to_year}").to_s
  end
end

record_saver.save record



require 'rubygems'
require 'mechanize'
require 'date'

agent = Mechanize.new
url = 'http://www.redfernwaterloo.nsw.gov.au/development_applications/development_proposals_on_exhibition.htm'
page = agent.get(url)

class Saver
  def initialize
    #If you want to trample on existing data, set this to true
    @trample_data = false
    @references = (ScraperWiki.select("council_reference from swdata") rescue nil)
  end

  def save(record)
    if record
      if @trample_data || @references.nil? || !@references.include?(record['council_reference'])
        ScraperWiki.save_sqlite(['council_reference'], record)
      else
        puts "Skipping already saved record " + record['council_reference']
      end
    end
  end
end

def scrubbed(text)
  text = text.gsub(/[\r\n]/){$1}
  text = text.gsub(/\t/){' '}
  text = text.gsub(/ +/){' '}
  return text
end

record_saver = Saver.new

record = nil

page.search('table table table table table table table table tr').each do |r|
  next unless r.search('td')[1]
  header = scrubbed r.search('td')[0].search('b').inner_text
  data = r.search('td')[1]
  case
    when header =~ /Application/ then
      record_saver.save record
      council_reference = scrubbed data.search('a')[0].inner_text
      record = {
        'info_url' => url,
        'date_scraped' => Date.today.to_s,
        'council_reference' => council_reference,
        'comment_url' => "mailto:redfernwaterloo@rwa.nsw.gov.au",
      }
    when header == "Location" then record['address'] = scrubbed data.inner_text + ", NSW"
    when header == "Proposal" then record['description'] = scrubbed data.inner_text
    when header == "Exhibition Dates" then
       full_date_string = scrubbed data.inner_text
       from_date_string, to_date_string = full_date_string.split(" to ")
       to_date, to_month, to_year = to_date_string.split

       case
         when from_date_string.split.size == 1 then
           from_date = from_date_string
           from_month = to_month
           from_year = to_year
         when from_date_string.split.size == 2 then
           from_date, from_month = from_date_string.split
           from_year = to_year
         when from_date_string.split.size == 3 then
           from_date, from_month, from_year = from_date_string.split
       end

       record['on_notice_from'] = Date.parse("#{from_date} #{from_month} #{from_year}").to_s
       record['on_notice_to'] = Date.parse("#{to_date} #{to_month} #{to_year}").to_s
  end
end

record_saver.save record




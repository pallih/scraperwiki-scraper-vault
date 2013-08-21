require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'typhoeus'
require 'date'
require 'yaml'

ScraperWiki.sqliteexecute('CREATE TABLE IF NOT EXISTS `academics` (`id` text, `name` text)')
ScraperWiki.sqliteexecute('CREATE TABLE IF NOT EXISTS `areas` (`area` text)')
ScraperWiki.sqliteexecute('CREATE TABLE IF NOT EXISTS `academicstoareas` (`academicid` text, `area` text)')

def get_academics(a)
  doc = Nokogiri.HTML(a.page.body)

  academics = doc.search('.search_result_box')
  
  academics.each do |academic|
    details = {}
    
    details['id'] = academic.search('a')[0][:href].scan(/\/expertdirectory\/emailAnExpert.do\?expertId=(.+)/)[0][0]
    details['name'] = academic.search('.slim-heading')[0].inner_text

    areas = (academic.search('.boxstyle')[0].inner_text).split(';')

    areas.each do |area|
      area_hash = {}

      area_hash['name'] = area.strip
      area_hash['academicid'] = details['id']
      
      ScraperWiki::save_sqlite(unique_keys=["area"], data={:area => area.strip}, table_name="areas")    
      ScraperWiki::sqliteexecute("INSERT INTO academicstoareas values (?,?)", [details['id'], area.strip])           
    end
  
    ScraperWiki::save_sqlite(unique_keys=["id"], data=details, table_name="academics")           

  end

  form = a.page.form_with(:name=>'expertsForDepartmentForm') 
  
  button = form.button_with(:value=>'Next Page')

  unless button.nil? 
    
    form.submit(button)
    get_academics(a)
    
  end

end

BASE_URL = 'http://experts.warwick.ac.uk'

url = BASE_URL + '/expertdirectory/index.do'

a = Mechanize.new
a.get(url)

doc = Nokogiri.HTML(a.page.body)

depts = doc.search('.search_results_box div a')

depts.each do |dept|
  
  url = BASE_URL + dept[:href]
  
  a = Mechanize.new
  a.get(url)

  get_academics(a)

end
# this stuff just allows you
# to run the script outside ScraperWiki
begin
  ScraperWiki
  rescue NameError
    require 'rest_client'
    ScraperWiki = Class.new do
      def self.scrape(url)
        RestClient.get(url)
      end

      def self.save(unique_keys=[],data={})
        p data
      end
    end
end

require 'nokogiri'

def escape_csv(string)
  string.gsub(/,/,'/')
end


class Crunch
  def initialize(page)
    @crunch = Nokogiri::HTML(ScraperWiki.scrape("http://www.crunchbase.com/companies?c=a&q=funded"))
  end
  
  def parse
    @crunch.css(".col2_table_listing a").each do |company_link|
      crunch_link = "http://www.crunchbase.com" + company_link.attr("href")
      company = {'name' => escape_csv(company_link.content),'url' => crunch_link, 'employees' => company_people(crunch_link), 'funding' => company_funding(crunch_link)}
      ScraperWiki.save(['url', 'name', 'employees', 'funding'], company)
    end
  end
  
  def company_people(company_link)
    p "trying #{company_link} employees"
    employees = []
    titles = []
    company_page = Nokogiri::HTML(ScraperWiki.scrape(company_link))
    company_page.css(".col1_people_name a").each do |person|
      employees << escape_csv(person.content)
    end
    company_page.css(".col1_people_title").each do |title|
      titles << escape_csv(title.content)
    end
    employees_with_titles = []
    (0..employees.length).each do |number|
      if employees[number]
        employees_with_titles << "#{employees[number]} #{titles[number].gsub(/(.+)/,'(\1)') if titles[number]}"
      end
    end
    employees_with_titles.join(", ").strip
  end
  
  def company_funding(company_link)
    p "trying #{company_link} funding"
    funding = []
#    funders = []
    company_page = Nokogiri::HTML(ScraperWiki.scrape(company_link))
    funding_content = company_page.xpath('//h2[//*[contains(text(), "Funding")]]')


    funding_content.css("title").each do |fund|
#    company_page.css("text(Overall Funding Rounds Total) title").each do |fund|
      funding << escape_csv(fund.content)
    p "trying #{company_link} funding #{funding.length}"
    end
#    company_page.css(".col1_funding_round_total title").each do |fund|
#      funders << escape_csv(funder.content)
#    end
#    funding_with_funders = []
#    (0..funding.length).each do |number|
#      if funding[number]
#        funding_with_funders << "#{funding[number]} #{funders[number].gsub(/(.+)/,'(\1)') if funders[number]}"
#      end
#    end
#    funding_with_funders.join(", ").strip
    funding.join(", ").strip
  end

end


 1.upto(5).each { |page| 
  c = Crunch.new(page) 
  c.parse
 }# this stuff just allows you
# to run the script outside ScraperWiki
begin
  ScraperWiki
  rescue NameError
    require 'rest_client'
    ScraperWiki = Class.new do
      def self.scrape(url)
        RestClient.get(url)
      end

      def self.save(unique_keys=[],data={})
        p data
      end
    end
end

require 'nokogiri'

def escape_csv(string)
  string.gsub(/,/,'/')
end


class Crunch
  def initialize(page)
    @crunch = Nokogiri::HTML(ScraperWiki.scrape("http://www.crunchbase.com/companies?c=a&q=funded"))
  end
  
  def parse
    @crunch.css(".col2_table_listing a").each do |company_link|
      crunch_link = "http://www.crunchbase.com" + company_link.attr("href")
      company = {'name' => escape_csv(company_link.content),'url' => crunch_link, 'employees' => company_people(crunch_link), 'funding' => company_funding(crunch_link)}
      ScraperWiki.save(['url', 'name', 'employees', 'funding'], company)
    end
  end
  
  def company_people(company_link)
    p "trying #{company_link} employees"
    employees = []
    titles = []
    company_page = Nokogiri::HTML(ScraperWiki.scrape(company_link))
    company_page.css(".col1_people_name a").each do |person|
      employees << escape_csv(person.content)
    end
    company_page.css(".col1_people_title").each do |title|
      titles << escape_csv(title.content)
    end
    employees_with_titles = []
    (0..employees.length).each do |number|
      if employees[number]
        employees_with_titles << "#{employees[number]} #{titles[number].gsub(/(.+)/,'(\1)') if titles[number]}"
      end
    end
    employees_with_titles.join(", ").strip
  end
  
  def company_funding(company_link)
    p "trying #{company_link} funding"
    funding = []
#    funders = []
    company_page = Nokogiri::HTML(ScraperWiki.scrape(company_link))
    funding_content = company_page.xpath('//h2[//*[contains(text(), "Funding")]]')


    funding_content.css("title").each do |fund|
#    company_page.css("text(Overall Funding Rounds Total) title").each do |fund|
      funding << escape_csv(fund.content)
    p "trying #{company_link} funding #{funding.length}"
    end
#    company_page.css(".col1_funding_round_total title").each do |fund|
#      funders << escape_csv(funder.content)
#    end
#    funding_with_funders = []
#    (0..funding.length).each do |number|
#      if funding[number]
#        funding_with_funders << "#{funding[number]} #{funders[number].gsub(/(.+)/,'(\1)') if funders[number]}"
#      end
#    end
#    funding_with_funders.join(", ").strip
    funding.join(", ").strip
  end

end


 1.upto(5).each { |page| 
  c = Crunch.new(page) 
  c.parse
 }
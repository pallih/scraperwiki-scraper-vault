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
    @crunch = Nokogiri::HTML(ScraperWiki.scrape("http://www.crunchbase.com/search/advanced/companies/690884?page=#{page}"))
  end
  
  def parse
    @crunch.css(".search_result_name a").each do |company_link|
      crunch_link = "http://www.crunchbase.com" + company_link.attr("href")
      company = {'name' => escape_csv(company_link.content), 'phone' => escape_csv(company_link.content) ,'url' => crunch_link, 'employees' => company_people(crunch_link)}
      ScraperWiki.save(['url', 'name', 'employees'], company)
    end
  end
  
  def company_people(company_link)
    p "trying #{company_link}"
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
  
end


1.upto(5).each { |page| 
  c = Crunch.new(page) 
  c.parse
}
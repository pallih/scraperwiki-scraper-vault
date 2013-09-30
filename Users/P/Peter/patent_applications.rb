# Blank Ruby
#Searches for Patent Applications...


# Blank Ruby



require 'open-uri'
require 'csv'
require 'net/http'
require 'mechanize'
require 'nokogiri'


def fill_out_form

#Set up mechanize and create browser
agent = Mechanize.new
agent.keep_alive = false
agent.user_agent = 'Mac Mozilla'
agent.user_agent_alias = 'Mac Mozilla'
agent.redirect_ok = false
agent.follow_meta_refresh = true

begin
#Get initial page:
agent.get('http://appft.uspto.gov/netahtml/PTO/search-adv.html')

#puts agent.page.body

#Input search query
agent.page.forms.first.fields[7].value=('IN/(Crawford-John) and IS/(CA) and IC/(Burbank or Topanga)')

#Submit form
@response = agent.page.forms.first.submit
#puts @result.body




rescue => e
puts e.class
puts e
retry
rescue Timeout::Error
puts "Timeout"
retry
end

end

########################################################



#Scrape data here...
def scrape_table(page_body)
  

   numbers =  page_body.search('table').search('tr').search('td[2]').collect {|n| n.text.chomp.strip}
   titles =   page_body.search('table').search('tr').search('td[3]').collect {|n| n.text.chomp.strip}



    1.upto(numbers.length-1) do |i|
       @record = {}
       @record['Number'] = numbers[i].to_s.strip.chomp.gsub(/[(,?!\'":.)]/, '')
       @record['Title'] = titles[i].to_s.strip.chomp.squeeze
       get_pdf(@record['Number'])


       puts @record

 
      #Save records
      #ScraperWiki.save(['Number'], @record)
  

    end
  




#get next page

    @name = ''
  @response.forms.first.buttons.each do |b|
      if b.name.include? "Next" 
        @name = b.name
        puts @name
      end
  end

    if @response.forms.first.button_with(:name=> @name ).nil? == false
        @response = @response.forms.first.click_button(@response.forms.first.button_with(:name=>@name))
        scrape_table(@response)
    end
end

#########################################################


def get_pdf(patent_number)
begin

base_url = "http://www.pat2pdf.org/"

agent = Mechanize.new
agent.keep_alive = false
agent.user_agent = 'Mac Mozilla'
agent.user_agent_alias = 'Mac Mozilla'
agent.redirect_ok = false
agent.follow_meta_refresh = true

agent.get("http://www.pat2pdf.org/pat2pdf/foo.pl?number=#{patent_number}")
doc = Nokogiri::HTML(agent.page.body)

link = doc.xpath("//div[@id='content']/ul/li/a").map {|a| a['href']}
puts base_url + link.first.to_s.strip.chomp
pdf = open(base_url + link.first.to_s.strip.chomp)
puts pdf.class
@record['pdf'] = pdf



rescue => e
puts e.class
puts e
retry
rescue Timeout::Error
puts "Timeout"
retry
end



end







fill_out_form
scrape_table(@response)


# Blank Ruby
#Searches for Patent Applications...


# Blank Ruby



require 'open-uri'
require 'csv'
require 'net/http'
require 'mechanize'
require 'nokogiri'


def fill_out_form

#Set up mechanize and create browser
agent = Mechanize.new
agent.keep_alive = false
agent.user_agent = 'Mac Mozilla'
agent.user_agent_alias = 'Mac Mozilla'
agent.redirect_ok = false
agent.follow_meta_refresh = true

begin
#Get initial page:
agent.get('http://appft.uspto.gov/netahtml/PTO/search-adv.html')

#puts agent.page.body

#Input search query
agent.page.forms.first.fields[7].value=('IN/(Crawford-John) and IS/(CA) and IC/(Burbank or Topanga)')

#Submit form
@response = agent.page.forms.first.submit
#puts @result.body




rescue => e
puts e.class
puts e
retry
rescue Timeout::Error
puts "Timeout"
retry
end

end

########################################################



#Scrape data here...
def scrape_table(page_body)
  

   numbers =  page_body.search('table').search('tr').search('td[2]').collect {|n| n.text.chomp.strip}
   titles =   page_body.search('table').search('tr').search('td[3]').collect {|n| n.text.chomp.strip}



    1.upto(numbers.length-1) do |i|
       @record = {}
       @record['Number'] = numbers[i].to_s.strip.chomp.gsub(/[(,?!\'":.)]/, '')
       @record['Title'] = titles[i].to_s.strip.chomp.squeeze
       get_pdf(@record['Number'])


       puts @record

 
      #Save records
      #ScraperWiki.save(['Number'], @record)
  

    end
  




#get next page

    @name = ''
  @response.forms.first.buttons.each do |b|
      if b.name.include? "Next" 
        @name = b.name
        puts @name
      end
  end

    if @response.forms.first.button_with(:name=> @name ).nil? == false
        @response = @response.forms.first.click_button(@response.forms.first.button_with(:name=>@name))
        scrape_table(@response)
    end
end

#########################################################


def get_pdf(patent_number)
begin

base_url = "http://www.pat2pdf.org/"

agent = Mechanize.new
agent.keep_alive = false
agent.user_agent = 'Mac Mozilla'
agent.user_agent_alias = 'Mac Mozilla'
agent.redirect_ok = false
agent.follow_meta_refresh = true

agent.get("http://www.pat2pdf.org/pat2pdf/foo.pl?number=#{patent_number}")
doc = Nokogiri::HTML(agent.page.body)

link = doc.xpath("//div[@id='content']/ul/li/a").map {|a| a['href']}
puts base_url + link.first.to_s.strip.chomp
pdf = open(base_url + link.first.to_s.strip.chomp)
puts pdf.class
@record['pdf'] = pdf



rescue => e
puts e.class
puts e
retry
rescue Timeout::Error
puts "Timeout"
retry
end



end







fill_out_form
scrape_table(@response)



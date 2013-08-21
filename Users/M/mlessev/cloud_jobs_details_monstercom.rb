# Blank Ruby
# encoding: utf-8

require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'
require 'uri'
require 'net/http'
require 'scraperwiki/datastore'
require 'httpclient'
require 'scraperwiki/scraper_require'


#ScraperWiki::attach("it_glossary")
#ScraperWiki::sqliteexecute("drop table search_keyword") rescue rr = 0
#ScraperWiki::sqliteexecute("create table search_keyword as select * from it_glossary.search_keyword")

#ScraperWiki::sqliteexecute("delete from cloud_possitions where search_keyword in ('AWS+C3', 'Foundry')")
#ScraperWiki::sqliteexecute("delete from cloud_job_details where id not in (select id from cloud_possitions)")

#ScraperWiki::commit()

#words = ['Rackspace']
#words = ['Bluelock']

words = ['cloud', 'IaaS', 'PaaS', 'SaaS', 'azure', '__22Amazon+Web+Services__22', 'AWS+API', '__22AWS+EC2__22', '__22AWS+S3__22', '__22Google+App+Engine__22', 'Rackspace', 'OpenStack', '__22PHP+Fog__22', 'Heroku', 'AppHarbor', 'Salesforce', 'NoSQL', 'Exadata', 'Exalogic', 'Joyent', '__22Cloud+Foundry__22', 'Terremark', 'GoGrid', 'Navisite', '__22IBM+SmartCloud__22', 'OpSource', '__22Dimension+Data+cloud__22', '__22oracle+cloud__22', 'scraperwiki', '__22SAP+Hana__22', 'Savvis', 'Bluelock', 'Engineyard', 'OpenShift', 'CloudBees', 'CloudSwing']

today = Date.today(sg=Date::ITALY).to_s
yesterday = (Date.today(sg=Date::ENGLAND) -1).to_s
cur_week = Date.today(sg=Date::ITALY).cweek.to_s
cur_year = Date.today(sg=Date::ITALY).year.to_s
cur_month = Date.today(sg=Date::ITALY).month.to_s

if 1 > 0 then  
# get cloud open possitions
words.each do |word|
  saved_rows = 0
  total_rows = 0
  returned_rows = ''
  page = 1
#  url = "http://jobsearch.monster.com/search/?q=" + word + "&sort=dt.rv.di" 
  url = "http://jobsearch.monster.com/jobs/?q=" + word + "&sort=dt.rv.di&cy=us"
  #url_pages.force_encoding("UTF-8")
  #p word + ' -> ' + saved_rows.to_s
  
  while url.length > 0 
    doc = Nokogiri.HTML(open(url))
    returned_rows = doc.search('div[@id="resultsCountHeader"]/h1').inner_text.strip
    doc_rows = doc.search('table[@class="listingsTable"]/tbody/tr[@class="odd"]')
    doc_rows += doc.search('table[@class="listingsTable"]/tbody/tr[@class="even"]')
    doc_rows += doc.search('table[@class="listingsTable"]/tbody/tr[@class="odd sponsoredListing"]')
    doc_rows += doc.search('table[@class="listingsTable"]/tbody/tr[@class="even sponsoredListing"]')

    doc_rows.each do |vv|
      job_name = vv.search 'td[@scope="row"]/div/div[@class="jobTitleContainer"]/a'
      job_id = job_name.at("a").attributes["name"].value.strip rescue job_id = '-1'
      url_inner = job_name.at("a").attributes["href"].value.strip rescue url_inner = "www.abv.bg"
      company_name = vv.search 'td[@scope="row"]/div/div[@class="companyContainer"]/div/div[@class="companyConfidential"]'
      salary = vv.search 'td[@scope="row"]/div/div[@class="companyContainer"]/div/div[@class="fnt13"]'
      location = vv.search 'td/div/div[@class="jobLocationSingleLine"]/a'
      if location.inner_text.strip.length < 2 then
        location = vv.search 'td/div/div[@class="jobLocationSingleLine"]'  
        # p location
      end 
      location_text = location.at("a").attributes["title"].value.strip rescue location_text = location.inner_text.strip
      location_href = location.at("a").attributes["href"].value.strip rescue location_href = ''

      salary_text = salary.inner_text.strip
      salary_from = ''
      salary_to = ''
      if salary_text.length > 2 then
        salary_from = salary_text.split("-")[0].strip rescue salary_from = ''
        salary_to = salary_text.split("-")[1].strip rescue salary_to = ''
      end

      data = {
        week: cur_week,
        year: cur_year,
        month: cur_month,
        id: job_id,
        search_keyword: word,
        publish_data: '',
        text_body: job_name.at("a").attributes["title"].value.strip,
        location: location_text,
        location_href: location_href,
        company_name: company_name.inner_text.strip,
        company_href: '',
        job_link: url_inner,
        salary: salary_text,
        salary_from: salary_from.sub(',', '').to_f,
        salary_to: salary_to.sub(',', '').to_f 
      }

      #puts data.to_json
      ScraperWiki::save_sqlite(unique_keys=['id', 'week', 'search_keyword', 'year', 'month'], data, table_name="cloud_possitions", verbose=0)

      url_inner = job_name.at("a").attributes["href"].value.strip
      res = ScraperWiki::select( "count(id) as flag from cloud_job_details where id = '" + job_id + "'")
      exist_flag = 0
      for d in res
        exist_flag = d["flag"]
      end # for

      if exist_flag == 0 then
        open_flag = 1
        doc_inner = Nokogiri.HTML(open(url_inner)) rescue open_flag = 0
        if open_flag == 0 then
          p url_inner
        else
          job_body = doc_inner.search 'div[@id="jobcopy"]/div[@id="jobBodyContent"]'
    
          if job_body.inner_text.strip.length < 5 then
            job_body = doc_inner.search 'span[@id="TrackingJobBody"]'
          end
    
          inner_data = {
            id: job_id,
            job_link: url_inner,
            job_name: job_name.at("a").attributes["title"].value.strip,
            key: job_body.inner_text.strip,
            value: job_body.inner_html.strip
          }
          
          #puts inner_data.to_json
          ScraperWiki::save_sqlite(unique_keys=['id'], inner_data, table_name="cloud_job_details", verbose=0)
          saved_rows = saved_rows + 1
        end #if open_flag == 0
      end # if exist_flag > 0
      total_rows = total_rows + 1
    end # doc_rows
    
    url = ''
    doc.search('span[@class="navLinks"]/span/a[@class="box afterSelected"]').each do |v|
      url = v.attributes["href"].value
    end
    #p word + ' -> p' + page.to_s + '(' + saved_rows.to_s  + ')'
    page += 1

  end # while
  p word + ' -> (saved) ' + saved_rows.to_s + '(' + total_rows.to_s + ') - ' + returned_rows
end  # word

end #if

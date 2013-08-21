# coding: utf-8

require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'
require 'pp'
require 'uri'
require 'net/http'
require 'scraperwiki/datastore'
require 'httpclient'
require 'scraperwiki/scraper_require'

#ScraperWiki::attach("it_glossary")

#ScraperWiki::sqliteexecute("drop table search_keyword") rescue rr = 0
#ScraperWiki::sqliteexecute("create table search_keyword as select * from it_glossary.search_keyword")

#ScraperWiki::sqliteexecute("drop table if exists it_glossary")
#ScraperWiki::sqliteexecute("CREATE TABLE it_glossary (`gloss` text, `word` text, `abbr` text, `key` text, `word_link` text)")
#ScraperWiki::sqliteexecute("insert into it_glossary select gloss, word, abbr, key, word_link from it_glossary.it_glossary")


# ScraperWiki::sqliteexecute("drop table if exists cloud_job_details_fts")
#ScraperWiki::sqliteexecute("CREATE VIRTUAL TABLE cloud_job_details_fts USING fts3(id text, key text, value text)")
#ScraperWiki::sqliteexecute("INSERT INTO cloud_job_details_fts select id, key, value from cloud_job_details")

#ScraperWiki::sqliteexecute("delete from cloud_possitions where search_keyword in ('Dropbox', 'hana', 'Dimension+Data', 'Foundry') ")
#ScraperWiki::sqliteexecute("delete from cloud_job_details where id not in (select id from cloud_possitions)")

#ScraperWiki::commit()

words = ['cloud', 'IaaS', 'PaaS', 'SaaS', 'azure', 'Amazon+Web+Services', 'AWS+API', 'AWS+EC2', 'AWS+S3', 'Google+App+Engine', 'Rackspace', 'OpenStack', 'PHP+Fog', 'Heroku', 'AppHarbor', 'Salesforce', 'NoSQL', 'Exadata', 'Exalogic', 'Joyent', 'Cloud+Foundry', 'Terremark', 'GoGrid', 'Navisite', 'IBM+SmartCloud', 'OpSource', 'Dimension+Data+cloud', 'oracle+cloud', 'scraperwiki', 'SAP+Hana', 'Savvis', 'Bluelock', 'Engineyard', 'OpenShift', 'CloudBees', 'CloudSwing']


today = Date.today(sg=Date::ITALY).to_s
yesterday = (Date.today(sg=Date::ENGLAND) -1).to_s
cur_week = Date.today(sg=Date::ITALY).cweek.to_s
cur_year = Date.today(sg=Date::ITALY).year.to_s
cur_month = Date.today(sg=Date::ITALY).month.to_s

words.each do |word|

  url = "http://www.jobtiger.bg/obiavi-za-rabota/?keyword=" + word + "&jtref=megahome"
  url_pages = "http://www.jobtiger.bg/obiavi-za-rabota/?keyword=" + word + "&_pagerRows=30&_page=$$$##mm"

  doc_page = Nokogiri.HTML(open(url))
  total_rows = doc_page.search 'table/tr/td[@class="first"]/b'
  #p total_rows.inner_text.strip

  if total_rows.empty? == false then

    rows = total_rows.inner_text.strip.to_i
    cur_page = 1
    p word + ' -> ' + rows.to_s

    while rows > 0
      doc = Nokogiri.HTML(open(url_pages.sub('$$$##mm', cur_page.to_s)))

      doc.search('table[@class="pager_details"]/tr').each do |v|
        cells = v.search 'td'

        job_id= cells[0].search 'table/tr/td'
        location = v.search 'td[@class="job_regions"]'
        job_date = v.search 'td[@class="rel_period"]'

        if cells.count > 8

          cur_link = ("http://www.jobtiger.bg" + job_id[1].at("a").attributes["href"].value).sub('http://www.jobtiger.bghttp://www.jobtiger.bg', 'http://www.jobtiger.bg')
          cur_link = cur_link.sub('http://www.jobtiger.bgwww.jobtiger.bg', 'http://www.jobtiger.bg')

          doc_inner = Nokogiri.HTML(open(cur_link))

          detiles = doc_inner.search 'table[@id="detailTbl"]/tr/td[@class="val"]'
          if detiles.inner_text.strip != ''
            inner_data = {
              id: job_id[1].at("a").attributes["id"].value,
              key: detiles.inner_text.strip,
              value: detiles.inner_html.strip
            }
            #puts inner_data.to_json
            ScraperWiki::save_sqlite(unique_keys=['id'], inner_data, table_name="cloud_job_details", verbose=0)
          else
#            p cur_link
            detiles = doc_inner.search 'div[@class="container"]'

            inner_data = {
              id: job_id[1].at("a").attributes["id"].value,
              key: '',
              value: detiles.inner_html.strip
            }
          end

          data = {
            id: job_id[1].at("a").attributes["id"].value,
            publish_data: job_date[0].inner_text.strip,
            text_body: cells[2].inner_text.strip,
            location: location[0].inner_text.strip,
            company_name: cells[5].inner_text.strip,
            job_link: ("http://www.jobtiger.bg" + job_id[1].at("a").attributes["href"].value).sub('http://www.jobtiger.bghttp://www.jobtiger.bg', 'http://www.jobtiger.bg'),
            week: cur_week,
            year: cur_year,
            month: cur_month,
            search_keyword: word
          }
          #puts data.to_json
          ScraperWiki::save_sqlite(unique_keys=['id','week', 'search_keyword', 'year', 'month'], data, table_name="cloud_possitions", verbose=0)
        end
      end

      cur_page = cur_page + 1
      rows     = rows - 30
      #p rows.to_s + ' -> ' + cur_page.to_s
    end   
  else
    p word + ' -> 0'
  end
end


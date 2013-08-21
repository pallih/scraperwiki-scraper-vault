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

ScraperWiki::attach("cloud_jobs_details_monstercom")

#ScraperWiki::attach("it_glossary")
#ScraperWiki::sqliteexecute("drop table search_keyword") rescue rr = 0

#ScraperWiki::sqliteexecute("create table cloud_possitions as select * from cloud_jobs_details_monstercom.cloud_possitions")

ScraperWiki::sqliteexecute("create table cloud_job_details as select id, job_name, job_link, key from cloud_jobs_details_monstercom.cloud_job_details where rowID between 1 and 8000 order by rowID ")

#cloud_job_details` (`value` text, `job_link` text, `id` text, `key` text, `job_name` text)

#ScraperWiki::sqliteexecute("delete from cloud_possitions where search_keyword in ('AWS+EC2', 'AWS+C3')")
#ScraperWiki::sqliteexecute("delete from cloud_job_details where id not in (select id from cloud_possitions)")

#ScraperWiki::commit()
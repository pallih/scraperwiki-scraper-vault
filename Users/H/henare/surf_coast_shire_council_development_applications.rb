require 'mechanize'
require 'date'

agent = Mechanize.new
url = 'http://www.surfcoast.vic.gov.au/My_Property/Building_Planning/Planning/Applications_On_Public_Exhibition'
page = agent.get url

page.at(:table).search(:tr).each_with_index do |r,i|
  next if i == 0 # Skip the first row header

  council_reference = r.search(:td)[0].inner_text.gsub(/\u00a0/,'')

  if (ScraperWiki.select("* from swdata where `council_reference`='#{council_reference}'").empty? rescue true)
    detail_page_url = r.at(:a).attr(:href)
    begin
      detail_page = agent.get detail_page_url
    rescue URI::InvalidURIError
      puts "DA #{council_reference} has a broken detail page, skipping"
      next
    end

    record = {
      council_reference: council_reference,
      address: detail_page.at(:h1).inner_text.strip + ", VIC",
      on_notice_from: Date.parse(r.search(:td)[3].inner_text.split('-')[0]),
      on_notice_to: Date.parse(r.search(:td)[3].inner_text.split('-')[1]),
      description: detail_page.at('.general_content').at(:p).at(:strong).next.inner_text.strip,
      info_url: detail_page_url,
      comment_url: detail_page_url,
      date_scraped: Date.today
    }

    ScraperWiki.save_sqlite([:council_reference], record)
  else
    puts "Skipping already saved record " + council_reference
  end
 end

require 'mechanize'
require 'date'

agent = Mechanize.new
url = 'http://www.surfcoast.vic.gov.au/My_Property/Building_Planning/Planning/Applications_On_Public_Exhibition'
page = agent.get url

page.at(:table).search(:tr).each_with_index do |r,i|
  next if i == 0 # Skip the first row header

  council_reference = r.search(:td)[0].inner_text.gsub(/\u00a0/,'')

  if (ScraperWiki.select("* from swdata where `council_reference`='#{council_reference}'").empty? rescue true)
    detail_page_url = r.at(:a).attr(:href)
    begin
      detail_page = agent.get detail_page_url
    rescue URI::InvalidURIError
      puts "DA #{council_reference} has a broken detail page, skipping"
      next
    end

    record = {
      council_reference: council_reference,
      address: detail_page.at(:h1).inner_text.strip + ", VIC",
      on_notice_from: Date.parse(r.search(:td)[3].inner_text.split('-')[0]),
      on_notice_to: Date.parse(r.search(:td)[3].inner_text.split('-')[1]),
      description: detail_page.at('.general_content').at(:p).at(:strong).next.inner_text.strip,
      info_url: detail_page_url,
      comment_url: detail_page_url,
      date_scraped: Date.today
    }

    ScraperWiki.save_sqlite([:council_reference], record)
  else
    puts "Skipping already saved record " + council_reference
  end
 end

require 'mechanize'
require 'date'

agent = Mechanize.new
url = 'http://www.surfcoast.vic.gov.au/My_Property/Building_Planning/Planning/Applications_On_Public_Exhibition'
page = agent.get url

page.at(:table).search(:tr).each_with_index do |r,i|
  next if i == 0 # Skip the first row header

  council_reference = r.search(:td)[0].inner_text.gsub(/\u00a0/,'')

  if (ScraperWiki.select("* from swdata where `council_reference`='#{council_reference}'").empty? rescue true)
    detail_page_url = r.at(:a).attr(:href)
    begin
      detail_page = agent.get detail_page_url
    rescue URI::InvalidURIError
      puts "DA #{council_reference} has a broken detail page, skipping"
      next
    end

    record = {
      council_reference: council_reference,
      address: detail_page.at(:h1).inner_text.strip + ", VIC",
      on_notice_from: Date.parse(r.search(:td)[3].inner_text.split('-')[0]),
      on_notice_to: Date.parse(r.search(:td)[3].inner_text.split('-')[1]),
      description: detail_page.at('.general_content').at(:p).at(:strong).next.inner_text.strip,
      info_url: detail_page_url,
      comment_url: detail_page_url,
      date_scraped: Date.today
    }

    ScraperWiki.save_sqlite([:council_reference], record)
  else
    puts "Skipping already saved record " + council_reference
  end
 end

require 'mechanize'
require 'date'

agent = Mechanize.new
url = 'http://www.surfcoast.vic.gov.au/My_Property/Building_Planning/Planning/Applications_On_Public_Exhibition'
page = agent.get url

page.at(:table).search(:tr).each_with_index do |r,i|
  next if i == 0 # Skip the first row header

  council_reference = r.search(:td)[0].inner_text.gsub(/\u00a0/,'')

  if (ScraperWiki.select("* from swdata where `council_reference`='#{council_reference}'").empty? rescue true)
    detail_page_url = r.at(:a).attr(:href)
    begin
      detail_page = agent.get detail_page_url
    rescue URI::InvalidURIError
      puts "DA #{council_reference} has a broken detail page, skipping"
      next
    end

    record = {
      council_reference: council_reference,
      address: detail_page.at(:h1).inner_text.strip + ", VIC",
      on_notice_from: Date.parse(r.search(:td)[3].inner_text.split('-')[0]),
      on_notice_to: Date.parse(r.search(:td)[3].inner_text.split('-')[1]),
      description: detail_page.at('.general_content').at(:p).at(:strong).next.inner_text.strip,
      info_url: detail_page_url,
      comment_url: detail_page_url,
      date_scraped: Date.today
    }

    ScraperWiki.save_sqlite([:council_reference], record)
  else
    puts "Skipping already saved record " + council_reference
  end
 end


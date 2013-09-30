require 'active_support/core_ext/enumerable'
require 'nokogiri'
require 'json'
require 'open-uri'

LISTING_PAGE = 'http://www.crunchbase.com/companies?c=%s&q=hardware'
API_PAGE = 'http://api.crunchbase.com/v/1%s.json'
companies = []
funders = Hash.new(0)

%w(a b c d e f g h i j k l m n o p q r s t u v w x y z other).each do |page|
  html = open(LISTING_PAGE % page).read
  doc = Nokogiri::HTML(html)
  list = doc.css('table.col2_table_listing a').map { |a| { name: a.inner_text, link: a['href'] } }
  companies += list
end

companies.each do |company|
  data = JSON.parse(open(API_PAGE % company[:link]).read)
  next unless data['funding_rounds'].size > 0
  company[:total_funding] = data['funding_rounds'].map { |r| r['raised_amount'] }.compact.inject(0){|sum,x| sum + x }
  investments = []
  data['funding_rounds'].each do |round|
    round['investments'].each do |investment|
      permalink = %w(company financial_org person).map { |e| "/#{e.sub('_org', '-organization')}/#{investment[e]['permalink']}" if investment[e] }.compact.first
      investments << { round: round['round_code'], company: company[:link], investor: permalink, year: round['funded_year'] }
      funders[permalink] += 1
    end
  end
  ScraperWiki::save_sqlite ['round', 'company', 'investor'], investments, 'investments'
  ScraperWiki::save_sqlite ['link'], company.merge(year: data['founded_year']), 'companies'
end

ScraperWiki::save_sqlite ['link'], funders.map { |l,n| { link: l, investments: n } }, 'funders'
require 'active_support/core_ext/enumerable'
require 'nokogiri'
require 'json'
require 'open-uri'

LISTING_PAGE = 'http://www.crunchbase.com/companies?c=%s&q=hardware'
API_PAGE = 'http://api.crunchbase.com/v/1%s.json'
companies = []
funders = Hash.new(0)

%w(a b c d e f g h i j k l m n o p q r s t u v w x y z other).each do |page|
  html = open(LISTING_PAGE % page).read
  doc = Nokogiri::HTML(html)
  list = doc.css('table.col2_table_listing a').map { |a| { name: a.inner_text, link: a['href'] } }
  companies += list
end

companies.each do |company|
  data = JSON.parse(open(API_PAGE % company[:link]).read)
  next unless data['funding_rounds'].size > 0
  company[:total_funding] = data['funding_rounds'].map { |r| r['raised_amount'] }.compact.inject(0){|sum,x| sum + x }
  investments = []
  data['funding_rounds'].each do |round|
    round['investments'].each do |investment|
      permalink = %w(company financial_org person).map { |e| "/#{e.sub('_org', '-organization')}/#{investment[e]['permalink']}" if investment[e] }.compact.first
      investments << { round: round['round_code'], company: company[:link], investor: permalink, year: round['funded_year'] }
      funders[permalink] += 1
    end
  end
  ScraperWiki::save_sqlite ['round', 'company', 'investor'], investments, 'investments'
  ScraperWiki::save_sqlite ['link'], company.merge(year: data['founded_year']), 'companies'
end

ScraperWiki::save_sqlite ['link'], funders.map { |l,n| { link: l, investments: n } }, 'funders'

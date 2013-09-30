require 'nokogiri'
require 'open-uri'
require 'timeout'
require 'date'

def analyze_page(url, data)
  doc = Nokogiri::HTML(open(url))
  data['date'] = (date = doc.at_css('p.date')) ? date.content : nil
  data['path'] = doc.at_css('p#path').content
  data['subtitle'] = (subtitle = doc.at_css('p.standfirst')) ? subtitle.content : nil
  data['content'] = doc.css('p.content')
end

urls = ['http://www.rikenresearch.riken.jp/eng/archive/section/research',
        'http://www.rikenresearch.riken.jp/eng/archive/section/hom',
        'http://www.rikenresearch.riken.jp/eng/archive/section/frontline',
        'http://www.rikenresearch.riken.jp/eng/archive/section/news-feature',
        'http://www.rikenresearch.riken.jp/eng/archive/section/riken-people',
        'http://www.rikenresearch.riken.jp/eng/archive/section/roundup',
        'http://www.rikenresearch.riken.jp/eng/archive/section/history',
        'http://www.rikenresearch.riken.jp/eng/archive/section/grants',
        'http://www.rikenresearch.riken.jp/eng/archive/section/sp',
        'http://www.rikenresearch.riken.jp/eng/archive/section/profile'
       ]

$articles = []

urls.each do |url|
  root_uri = URI.parse(url)
  html = open(url)

  doc = Nokogiri::HTML(html)
  
  $articles = $articles + doc.css("ul#results li").map { |node|
    {
      'title' => node.at_css("a").content,
      'url' => root_uri.merge(URI.parse(node.at_css("a").attribute("href"))),
      'type' => node.at_css("h4").content
    }
  }
end

$articles.each do |article|
  retries = 10
  url = article['url']
  puts "URL: " + url.to_s
  analyze_page(url, article)
end

ScraperWiki.save_sqlite(unique_keys=['url'], data=$articles)
require 'nokogiri'
require 'open-uri'
require 'timeout'
require 'date'

def analyze_page(url, data)
  doc = Nokogiri::HTML(open(url))
  data['date'] = (date = doc.at_css('p.date')) ? date.content : nil
  data['path'] = doc.at_css('p#path').content
  data['subtitle'] = (subtitle = doc.at_css('p.standfirst')) ? subtitle.content : nil
  data['content'] = doc.css('p.content')
end

urls = ['http://www.rikenresearch.riken.jp/eng/archive/section/research',
        'http://www.rikenresearch.riken.jp/eng/archive/section/hom',
        'http://www.rikenresearch.riken.jp/eng/archive/section/frontline',
        'http://www.rikenresearch.riken.jp/eng/archive/section/news-feature',
        'http://www.rikenresearch.riken.jp/eng/archive/section/riken-people',
        'http://www.rikenresearch.riken.jp/eng/archive/section/roundup',
        'http://www.rikenresearch.riken.jp/eng/archive/section/history',
        'http://www.rikenresearch.riken.jp/eng/archive/section/grants',
        'http://www.rikenresearch.riken.jp/eng/archive/section/sp',
        'http://www.rikenresearch.riken.jp/eng/archive/section/profile'
       ]

$articles = []

urls.each do |url|
  root_uri = URI.parse(url)
  html = open(url)

  doc = Nokogiri::HTML(html)
  
  $articles = $articles + doc.css("ul#results li").map { |node|
    {
      'title' => node.at_css("a").content,
      'url' => root_uri.merge(URI.parse(node.at_css("a").attribute("href"))),
      'type' => node.at_css("h4").content
    }
  }
end

$articles.each do |article|
  retries = 10
  url = article['url']
  puts "URL: " + url.to_s
  analyze_page(url, article)
end

ScraperWiki.save_sqlite(unique_keys=['url'], data=$articles)

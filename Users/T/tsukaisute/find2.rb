require 'kconv'
require 'nokogiri'
require 'rss/1.0'
require 'cgi'

def main()
  keywords = ['触手', '異種姦', '戦う変身ヒロイン']
  thread_links(keywords).each do |link|
    save_image_links(link)
    sleep 3
  end
end

def thread_links(keywords)
  links = []
  keywords.each do |keyword|
    url = "http://find.2ch.net/rss.php/#{CGI.escape(keyword.toeuc)}?ie=EUC-JP"
    html = ScraperWiki.scrape(url)
    rss = RSS::Parser.parse(html, false)
    rss.items.each do |item|
      #puts item.title, item.link
      links.push item.link
    end
  end
  links.uniq
end

def save_image_links(thread_link)
  html = ScraperWiki.scrape(thread_link)
  doc = Nokogiri::HTML(html)
  title = doc.css('head title').first.content
  puts title
  ary = []
  doc.css('dd').each {|dd|
    description = dd.inner_html.toutf8
    description.gsub(/ttp:\S+\.(jpg|jpeg|png|gif|bmp)/im) {|m|
      image_url = 'h' + m.to_s
      #puts image_url
      #puts description
      data = {
        'image_url'   => image_url,
        'page_url'    => thread_link,
        'page_title'  => title,
        'description' => description
      }
      #puts data.to_json
      ScraperWiki.save_sqlite(unique_keys=['image_url', 'page_url'], data=data)
    }
  }
rescue
  puts $!
end

main
require 'kconv'
require 'nokogiri'
require 'rss/1.0'
require 'cgi'

def main()
  keywords = ['触手', '異種姦', '戦う変身ヒロイン']
  thread_links(keywords).each do |link|
    save_image_links(link)
    sleep 3
  end
end

def thread_links(keywords)
  links = []
  keywords.each do |keyword|
    url = "http://find.2ch.net/rss.php/#{CGI.escape(keyword.toeuc)}?ie=EUC-JP"
    html = ScraperWiki.scrape(url)
    rss = RSS::Parser.parse(html, false)
    rss.items.each do |item|
      #puts item.title, item.link
      links.push item.link
    end
  end
  links.uniq
end

def save_image_links(thread_link)
  html = ScraperWiki.scrape(thread_link)
  doc = Nokogiri::HTML(html)
  title = doc.css('head title').first.content
  puts title
  ary = []
  doc.css('dd').each {|dd|
    description = dd.inner_html.toutf8
    description.gsub(/ttp:\S+\.(jpg|jpeg|png|gif|bmp)/im) {|m|
      image_url = 'h' + m.to_s
      #puts image_url
      #puts description
      data = {
        'image_url'   => image_url,
        'page_url'    => thread_link,
        'page_title'  => title,
        'description' => description
      }
      #puts data.to_json
      ScraperWiki.save_sqlite(unique_keys=['image_url', 'page_url'], data=data)
    }
  }
rescue
  puts $!
end

main

require 'kconv'
require 'nokogiri'
require 'cgi'

def main()
  keywords = ['触手', '異種']
  thread_links(keywords).each do |link|
    save_image_links(link)
    sleep 1
  end
end

def thread_links(keywords)
  links = []
  keywords.each do |keyword|
    url = "http://nico2ch.com/t/#{CGI.escape(keyword)}"
    html = ScraperWiki.scrape(url)
    doc = Nokogiri::HTML(html)
    doc.css('div#left_box div.list_box ul li h3 a:nth-child(1)').each do |link|
      links.push link.attr('href')
    end
  end
  links.uniq
end

def save_image_links(thread_link)
  #puts '---'
  html = ScraperWiki.scrape(thread_link)
  encoding = nil
  if thread_link.match(/fc2\.com|livedoor/)
    html = html.toutf8.gsub(/shift_jis|euc-jp/i, 'utf-8')
    #puts html
  end
  doc = Nokogiri::HTML(html)
  title = doc.css('title').first.content
  #puts title
  doc.css('a').each do |a|
    link = a['href']
    if link && link.match(/\.(jpg|jpeg|png|gif|bmp)$/i)
      a.css('img:nth-child(1)').each do
        if (thread_link.match(/zipdeyaruo\.blog42\.fc2\.com/))
          link = zipdeyaruo_image_url(link)
          sleep 2
        end
        data = {
          'image_url'   => link,
          'page_url'    => thread_link,
          'page_title'  => title,
          'description' => ""
        }
        ScraperWiki.save_sqlite(unique_keys=['image_url', 'page_url'], data=data)
      end
    end
  end
rescue
  puts $!
end

def zipdeyaruo_image_url(image_page_link)
  html = ScraperWiki.scrape(image_page_link)
  doc = Nokogiri::HTML(html)
  src = image_page_link
  doc.css('div.imgBlock > img').each do |img|
    src = img['src']
  end
  src
end

main
require 'kconv'
require 'nokogiri'
require 'cgi'

def main()
  keywords = ['触手', '異種']
  thread_links(keywords).each do |link|
    save_image_links(link)
    sleep 1
  end
end

def thread_links(keywords)
  links = []
  keywords.each do |keyword|
    url = "http://nico2ch.com/t/#{CGI.escape(keyword)}"
    html = ScraperWiki.scrape(url)
    doc = Nokogiri::HTML(html)
    doc.css('div#left_box div.list_box ul li h3 a:nth-child(1)').each do |link|
      links.push link.attr('href')
    end
  end
  links.uniq
end

def save_image_links(thread_link)
  #puts '---'
  html = ScraperWiki.scrape(thread_link)
  encoding = nil
  if thread_link.match(/fc2\.com|livedoor/)
    html = html.toutf8.gsub(/shift_jis|euc-jp/i, 'utf-8')
    #puts html
  end
  doc = Nokogiri::HTML(html)
  title = doc.css('title').first.content
  #puts title
  doc.css('a').each do |a|
    link = a['href']
    if link && link.match(/\.(jpg|jpeg|png|gif|bmp)$/i)
      a.css('img:nth-child(1)').each do
        if (thread_link.match(/zipdeyaruo\.blog42\.fc2\.com/))
          link = zipdeyaruo_image_url(link)
          sleep 2
        end
        data = {
          'image_url'   => link,
          'page_url'    => thread_link,
          'page_title'  => title,
          'description' => ""
        }
        ScraperWiki.save_sqlite(unique_keys=['image_url', 'page_url'], data=data)
      end
    end
  end
rescue
  puts $!
end

def zipdeyaruo_image_url(image_page_link)
  html = ScraperWiki.scrape(image_page_link)
  doc = Nokogiri::HTML(html)
  src = image_page_link
  doc.css('div.imgBlock > img').each do |img|
    src = img['src']
  end
  src
end

main

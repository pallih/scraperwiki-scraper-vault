# encoding: utf-8

require 'nokogiri'

def url(path)
  "http://500px.com#{path}"
end

def scrape(section = 'popular', page = 1)
  html = ScraperWiki::scrape url("/#{section}?page=#{page}")
  doc  = Nokogiri::HTML html

  doc.search(".photo_thumb .photo").each do |p|
    id  = p['id'].gsub('photo_thumb_', '').to_i
  
    thumbnail_src = p.at_css('a img').attr('src')
    thumbnail_url = url(p.at_css('a').attr('href').gsub("?from=#{section}", ''))

    user_url  = url(p.css('.info a').attr('href'))
    user_name = p.at_css('.info a').text

    title_el  = p.at_css('.title a')
    title     = title_el.nil?? "" : title_el.text

    rating_el = p.at_css('.rating')
    rating    = rating_el.nil?? 0.0 : rating_el.text.to_s.to_f

    data = {
      id: id,
      thumbnail_src: thumbnail_src,
      thumbnail_url: thumbnail_url,
      user_url: user_url,
      user_name: user_name,
      title: title,
      rating: rating
    }

    unless data[:id].nil? 
      ScraperWiki::save_sqlite unique_keys=["id"], data=data, table_name=section
      puts "#{section}: #{data.to_json}"
    end
  end
end

page_number = Integer(rand()*9)+1

scrape('editors', page_number)
scrape('popular', page_number)# encoding: utf-8

require 'nokogiri'

def url(path)
  "http://500px.com#{path}"
end

def scrape(section = 'popular', page = 1)
  html = ScraperWiki::scrape url("/#{section}?page=#{page}")
  doc  = Nokogiri::HTML html

  doc.search(".photo_thumb .photo").each do |p|
    id  = p['id'].gsub('photo_thumb_', '').to_i
  
    thumbnail_src = p.at_css('a img').attr('src')
    thumbnail_url = url(p.at_css('a').attr('href').gsub("?from=#{section}", ''))

    user_url  = url(p.css('.info a').attr('href'))
    user_name = p.at_css('.info a').text

    title_el  = p.at_css('.title a')
    title     = title_el.nil?? "" : title_el.text

    rating_el = p.at_css('.rating')
    rating    = rating_el.nil?? 0.0 : rating_el.text.to_s.to_f

    data = {
      id: id,
      thumbnail_src: thumbnail_src,
      thumbnail_url: thumbnail_url,
      user_url: user_url,
      user_name: user_name,
      title: title,
      rating: rating
    }

    unless data[:id].nil? 
      ScraperWiki::save_sqlite unique_keys=["id"], data=data, table_name=section
      puts "#{section}: #{data.to_json}"
    end
  end
end

page_number = Integer(rand()*9)+1

scrape('editors', page_number)
scrape('popular', page_number)
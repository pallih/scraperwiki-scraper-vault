require 'net/http'
require 'uri'
require 'nokogiri'

all_datasets_rss = ScraperWiki.scrape("http://www.datasf.org/rss.php?category=0")

doc = Nokogiri::XML.parse(all_datasets_rss)

pages = doc.xpath('//item').map do |i|
  item = {
    "details_url" => i.xpath('link').text,
    "title" => i.xpath('title').text,
    "comments" => i.xpath('comments').text,
    "published" => i.xpath('pubDate').text,
    "description" => i.xpath('description').text
  }
  begin
    html = ScraperWiki.scrape(item['details_url'])
    details = Nokogiri::HTML.parse(html) rescue "error!"
  rescue Timeout::Error
    details = "error!"
  end
  if details == "error!"
    p "#{details} - #{item['details_url']}"
    next
  end
  item['url'] = details.css('.title h2 a')[0].attributes['href'].value
  raw_attrs = details.css('.storycontent')[0].inner_html
  raw_attrs.split('<br>').each do |z| 
    next unless z.match('<b>')
    attr = z.strip.gsub('</b>', '<b>').split('<b>')
    next unless attr && attr.size > 0
    key = attr[1]
    val = attr[2]
    next unless val
    item[key.gsub(/[^[:alnum:]]/, '')] = val.strip
  end
  ScraperWiki.save(unique_keys=['title'], data=item)
  item
end

url = URI.parse('http://gispub02.sfgov.org/website/sfshare/index2.asp')
request = Net::HTTP::Post.new(url.path)
request.set_form_data({
  "accept"=>"asdfo2idsf2id"
})
response = Net::HTTP.new(url.host, url.port).start {|http| http.request(request)}
shapefiles_doc = Nokogiri::HTML.parse(response.body)
shapefiles = []
shapefiles_doc.css('table')[3].css('tr').each do |tr|
  if tr.inner_html =~ /\.zip/i
    tr.css('a').each do |l|
      if l.attributes['href'].text =~ /\.zip/i
        item = {
          "title" => l.text,
          "description" => tr.css('td')[1].text,
          "url" => "http://gispub02.sfgov.org/website/sfshare/" + l.attributes['href'].text
        }
        ScraperWiki.save(unique_keys=['title'], data=item)
      end
    end
  end
endrequire 'net/http'
require 'uri'
require 'nokogiri'

all_datasets_rss = ScraperWiki.scrape("http://www.datasf.org/rss.php?category=0")

doc = Nokogiri::XML.parse(all_datasets_rss)

pages = doc.xpath('//item').map do |i|
  item = {
    "details_url" => i.xpath('link').text,
    "title" => i.xpath('title').text,
    "comments" => i.xpath('comments').text,
    "published" => i.xpath('pubDate').text,
    "description" => i.xpath('description').text
  }
  begin
    html = ScraperWiki.scrape(item['details_url'])
    details = Nokogiri::HTML.parse(html) rescue "error!"
  rescue Timeout::Error
    details = "error!"
  end
  if details == "error!"
    p "#{details} - #{item['details_url']}"
    next
  end
  item['url'] = details.css('.title h2 a')[0].attributes['href'].value
  raw_attrs = details.css('.storycontent')[0].inner_html
  raw_attrs.split('<br>').each do |z| 
    next unless z.match('<b>')
    attr = z.strip.gsub('</b>', '<b>').split('<b>')
    next unless attr && attr.size > 0
    key = attr[1]
    val = attr[2]
    next unless val
    item[key.gsub(/[^[:alnum:]]/, '')] = val.strip
  end
  ScraperWiki.save(unique_keys=['title'], data=item)
  item
end

url = URI.parse('http://gispub02.sfgov.org/website/sfshare/index2.asp')
request = Net::HTTP::Post.new(url.path)
request.set_form_data({
  "accept"=>"asdfo2idsf2id"
})
response = Net::HTTP.new(url.host, url.port).start {|http| http.request(request)}
shapefiles_doc = Nokogiri::HTML.parse(response.body)
shapefiles = []
shapefiles_doc.css('table')[3].css('tr').each do |tr|
  if tr.inner_html =~ /\.zip/i
    tr.css('a').each do |l|
      if l.attributes['href'].text =~ /\.zip/i
        item = {
          "title" => l.text,
          "description" => tr.css('td')[1].text,
          "url" => "http://gispub02.sfgov.org/website/sfshare/" + l.attributes['href'].text
        }
        ScraperWiki.save(unique_keys=['title'], data=item)
      end
    end
  end
end
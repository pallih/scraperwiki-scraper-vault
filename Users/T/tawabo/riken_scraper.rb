# encoding: utf-8
require 'nokogiri'
require 'open-uri'
require 'timeout'
require 'date'

def strip_styles(doc)
  doc.xpath('//@style').remove
end

def analyze_pr(url, data)

  doc = Nokogiri::HTML(open(url))

  data['url'] = url
  if (type = doc.at_css('.press_ttl') ? 'press' :
            (doc.at_css('.results_ttl')  ? 'results' :
            (doc.at_css('.oshirase_ttl') ? 'oshirase' : nil)))
    data['type'] = type

    date = doc.at_css('.press_date').content
    /平成(.*?)年(.*?)月(.*?)日/.match(date)
    data['date'] = DateTime.new($1.to_i + 1988, $2.to_i, $3.to_i)
    data['title'] = doc.at_css('.' + type + '_ttl').content
    data['subtitle'] = doc.at_css('.' + type + '_sttl').content
    if (pps = doc.search("ul.press_point"))
      data['press_points'] = pps
    end
    data['kakomi'] = doc.at_css('.kakomi').tap { |d| strip_styles(d).inner_html unless d.nil?  }
    data['body'] = doc.at_css('ol.press_term').tap { |d| strip_styles(d).inner_html unless d.nil?  }
    data['contact'] = doc.at_css('.press_contact').tap { |d| strip_styles(d).inner_html unless d.nil? }
  else
    data['type'] = 'undefined'
    raise "undefined press release type for url " + url
  end
end

url = 'http://www.riken.jp/r-world/info/release/press/2011/index.html'
root_uri = URI.parse('http://www.riken.jp/r-world/info/release/press/2011/')

html = open(url)

doc = Nokogiri::HTML(html)
puts doc.text

press_releases = doc.css("tr > td > a[href]").first(10).map { |node|
  {
    'title' => node.text,
    'url' => root_uri.merge(node['href'])
  }
}

press_releases.each do |pr|
  retries = 10
  puts pr['url']
  url = pr['url']
  if (url.host == 'www.riken.jp')
    begin
      open(url) do |pr_html|
        pr_doc = Nokogiri::HTML(pr_html)
        pr_url = (detail_url = pr_doc.at_css(".press_publisher > a[href]")) ?  url.merge!(detail_url['href']) : url
        puts "URL: " + pr_url.to_s
        analyze_pr(pr_url, pr)
      end
    rescue => e
      puts "Raised error: " + e.to_s
    rescue Timeout::Error => e
      puts "Timeout, trying again"
      retries -= 1
      if retries > 0
        sleep 0.42 and retry
      else
        raise
      end
    end
  else
    pr['type'] = 'external'
  end
end

ScraperWiki.save_sqlite(unique_keys=['url'], data=press_releases)

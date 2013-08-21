# Blank Ruby

# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_doc(doc)
  result = []

#table = doc.xpath("//div[@class='noprint res']") #kokode syutokusita data ni kaigyou ga hairanai!!!

  doc.xpath("//div[@class='noprint res']").map do |ta|



name = ta.search("//span[@class='pp-place-title']/a/span")[1].text
address= ta.search("//span[@class='pp-headline-item pp-headline-address']/span")[1].text
tel= ta.search("//span[@class='telephone']/nobr")[1].text
url2= ta.search("//span[@class='pp-place-title']/a")[1].get_attribute("href")

    

    result << {
      'name'     => name,
      'address' => address,
      'tel'    => tel,
      'url2' => "http://maps.google.co.jp" << url2
    }
end

  result
end


def parse_doc2(doc)
  result = []

#table = doc.xpath("//div[@class='noprint res']") #kokode syutokusita data ni kaigyou ga hairanai!!!

  doc.xpath("//div[@class='noprint res']").map do |ta|



name = ta.search("//span[@class='pp-place-title']/a/span")[2].text
address= ta.search("//span[@class='pp-headline-item pp-headline-address']/span")[2].text
tel= ta.search("//span[@class='telephone']/nobr")[2].text
url2= ta.search("//span[@class='pp-place-title']/a")[2].get_attribute("href")

    

    result << {
      'name'     => name,
      'address' => address,
      'tel'    => tel,
      'url2' => "http://maps.google.co.jp" << url2
    }
end

  result
end

def parse_doc3(doc)
  result = []

#table = doc.xpath("//div[@class='noprint res']") #kokode syutokusita data ni kaigyou ga hairanai!!!

  doc.xpath("//div[@class='noprint res']").map do |ta|



name = ta.search("//span[@class='pp-place-title']/a/span")[3].text
address= ta.search("//span[@class='pp-headline-item pp-headline-address']/span")[3].text
tel= ta.search("//span[@class='telephone']/nobr")[3].text
url2= ta.search("//span[@class='pp-place-title']/a")[3].get_attribute("href")

    

    result << {
      'name'     => name,
      'address' => address,
      'tel'    => tel,
      'url2' => "http://maps.google.co.jp" << url2
    }
end

  result
end

def parse_doc4(doc)
  result = []

#table = doc.xpath("//div[@class='noprint res']") #kokode syutokusita data ni kaigyou ga hairanai!!!

  doc.xpath("//div[@class='noprint res']").map do |ta|



name = ta.search("//span[@class='pp-place-title']/a/span")[4].text
address= ta.search("//span[@class='pp-headline-item pp-headline-address']/span")[4].text
tel= ta.search("//span[@class='telephone']/nobr")[4].text
url2= ta.search("//span[@class='pp-place-title']/a")[4].get_attribute("href")

    

    result << {
      'name'     => name,
      'address' => address,
      'tel'    => tel,
      'url2' => "http://maps.google.co.jp" << url2
    }
end

  result
end

def parse_doc5(doc)
  result = []

#table = doc.xpath("//div[@class='noprint res']") #kokode syutokusita data ni kaigyou ga hairanai!!!

  doc.xpath("//div[@class='noprint res']").map do |ta|



name = ta.search("//span[@class='pp-place-title']/a/span")[5].text
address= ta.search("//span[@class='pp-headline-item pp-headline-address']/span")[5].text
tel= ta.search("//span[@class='telephone']/nobr")[5].text
url2= ta.search("//span[@class='pp-place-title']/a")[5].get_attribute("href")



    result << {
      'name'     => name,
      'address' => address,
      'tel'    => tel,
      'url2' => "http://maps.google.co.jp" << url2
    }
end

  result
end

def parse_doc6(doc)
  result = []

#table = doc.xpath("//div[@class='noprint res']") #kokode syutokusita data ni kaigyou ga hairanai!!!

  doc.xpath("//div[@class='noprint res']").map do |ta|



name = ta.search("//span[@class='pp-place-title']/a/span")[6].text
address= ta.search("//span[@class='pp-headline-item pp-headline-address']/span")[6].text
tel= ta.search("//span[@class='telephone']/nobr")[6].text
url2= ta.search("//span[@class='pp-place-title']/a")[6].get_attribute("href")

    


    result << {
      'name'     => name,
      'address' => address,
      'tel'    => tel,
      'url2' => "http://maps.google.co.jp" << url2
    }
end

  result
end

def parse_doc7(doc)
  result = []

#table = doc.xpath("//div[@class='noprint res']") #kokode syutokusita data ni kaigyou ga hairanai!!!

  doc.xpath("//div[@class='noprint res']").map do |ta|



name = ta.search("//span[@class='pp-place-title']/a/span")[7].text
address= ta.search("//span[@class='pp-headline-item pp-headline-address']/span")[7].text
tel= ta.search("//span[@class='telephone']/nobr")[7].text
url2= ta.search("//span[@class='pp-place-title']/a")[7].get_attribute("href")

    


    result << {
      'name'     => name,
      'address' => address,
      'tel'    => tel,
      'url2' => "http://maps.google.co.jp" << url2
    }
end

  result
end

def parse_doc8(doc)
  result = []

#table = doc.xpath("//div[@class='noprint res']") #kokode syutokusita data ni kaigyou ga hairanai!!!

  doc.xpath("//div[@class='noprint res']").map do |ta|



name = ta.search("//span[@class='pp-place-title']/a/span")[8].text
address= ta.search("//span[@class='pp-headline-item pp-headline-address']/span")[8].text
tel= ta.search("//span[@class='telephone']/nobr")[8].text
url2= ta.search("//span[@class='pp-place-title']/a")[8].get_attribute("href")

    


    result << {
      'name'     => name,
      'address' => address,
      'tel'    => tel,
      'url2' => "http://maps.google.co.jp" << url2
    }
end

  result
end

def parse_doc9(doc)
  result = []

#table = doc.xpath("//div[@class='noprint res']") #kokode syutokusita data ni kaigyou ga hairanai!!!

  doc.xpath("//div[@class='noprint res']").map do |ta|



name = ta.search("//span[@class='pp-place-title']/a/span")[9].text
address= ta.search("//span[@class='pp-headline-item pp-headline-address']/span")[9].text
tel= ta.search("//span[@class='telephone']/nobr")[9].text
url2= ta.search("//span[@class='pp-place-title']/a")[9].get_attribute("href")

    


    result << {
      'name'     => name,
      'address' => address,
      'tel'    => tel,
      'url2' => "http://maps.google.co.jp" << url2
    }
end

  result
end

def parse_doc10(doc)
  result = []

#table = doc.xpath("//div[@class='noprint res']") #kokode syutokusita data ni kaigyou ga hairanai!!!

  doc.xpath("//div[@class='noprint res']").map do |ta|



name = ta.search("//span[@class='pp-place-title']/a/span")[0].text
address= ta.search("//span[@class='pp-headline-item pp-headline-address']/span")[0].text
tel= ta.search("//span[@class='telephone']/nobr")[0].text
url2= ta.search("//span[@class='pp-place-title']/a")[0].get_attribute("href")

    


    result << {
      'name'     => name,
      'address' => address,
      'tel'    => tel,
      'url2' => "http://maps.google.co.jp" << url2
    }
end

  result
end


urls = (1..100).map {|i| "http://maps.google.co.jp/maps?q=%E5%AE%85%E9%85%8D%E5%BC%81%E5%BD%93%E3%80%80%E6%9D%B1%E4%BA%AC&hl=ja&authuser=0&ie=UTF8&vps=1&brcurrent=h3,0x605d1b87f02e57e7:0x2e01618b22571b89&sa=N&start=#{i}0"}

urls.each do |url|
  puts "Fetching #{url}"
  doc = Nokogiri::HTML.parse(open(url), 'Shift_JIS')
  data = parse_doc(doc)
  ScraperWiki.save(['name', 'address', 'tel', 'url2'], data)
  data = parse_doc2(doc)
  ScraperWiki.save(['name', 'address', 'tel', 'url2'], data)
  data = parse_doc3(doc)
  ScraperWiki.save(['name', 'address', 'tel', 'url2'], data)
  data = parse_doc4(doc)
  ScraperWiki.save(['name', 'address', 'tel', 'url2'], data)
  data = parse_doc5(doc)
  ScraperWiki.save(['name', 'address', 'tel', 'url2'], data)
  data = parse_doc6(doc)
  ScraperWiki.save(['name', 'address', 'tel', 'url2'], data)
  data = parse_doc7(doc)
  ScraperWiki.save(['name', 'address', 'tel', 'url2'], data)
  data = parse_doc8(doc)
  ScraperWiki.save(['name', 'address', 'tel', 'url2'], data)
  data = parse_doc9(doc)
  ScraperWiki.save(['name', 'address', 'tel', 'url2'], data)
  data = parse_doc10(doc)
  
  # (name, furigana) is not unique indeed
  ScraperWiki.save(['name', 'address', 'tel', 'url2'], data)
end
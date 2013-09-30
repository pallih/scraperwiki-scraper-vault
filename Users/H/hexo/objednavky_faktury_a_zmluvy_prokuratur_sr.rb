require 'rubygems'
require 'nokogiri'
require 'open-uri'

#html = ScraperWiki.scrape("http://www.genpro.gov.sk/objednavky--faktury-a-zmluvy")
SITE = "http://www.genpro.gov.sk"
html = ScraperWiki.scrape("#{SITE}/objednavky--faktury-a-zmluvy")

require 'pp'

class Dummy
  def text
    ''
  end
end

def parse_it(doc, t)
  institution = doc.at_xpath('//td[@class="middle-holder2"]/h1').text
  doc.xpath('//table[@class="tab-kontakt"]/tbody/tr').each do |tr|
    next if tr.xpath('.//td[@class="pozadie-okrove1"]').children.size != 0
    next if tr.xpath('.//td/h3').children.size != 0 #h3[@class="pozadie-okrove1"]').children.size != 0
    tds = tr.xpath('.//td')

    data = {"date"       => (tds[1].text.strip),
        "supplier"    => (tds[2].text.strip),
        "subject"     => (tds[3].text.strip),
        "price"       => ((tds[4] || Dummy.new).text.strip),
        "institution" => institution}
    ScraperWiki.save_sqlite(unique_keys = [], data = data, table_name = t)
  end
end

def parse_zsnh(doc)
  institution = doc.at_xpath('//td[@class="middle-holder2"]/h1').text
  doc.xpath('//table[@class="tab-kontakt"]/tbody/tr').each do |tr|
    next if tr.xpath('.//td[@class="pozadie-okrove1"]').children.size != 0
    next if tr.xpath('.//td/h3').children.size != 0 #h3[@class="pozadie-okrove1"]').children.size != 0
    tds = tr.xpath('.//td')

    data = {"date"       => (tds[0].text.strip),
        "supplier"    => (tds[1].text.strip),
        "subject"     => (tds[2].text.strip),
        "price"       => ((tds[3] || Dummy.new).text.strip),
        "institution" => institution}
    ScraperWiki.save_sqlite(unique_keys = [], data = data, table_name = 'zsnh')
  end

end

def parse_elektr_aukcie(doc)
  institution = doc.at_xpath('//td[@class="middle-holder2"]/h1').text
  doc.xpath('//table[@class="tab-kontakt"]/tbody/tr').each do |tr|
    next if tr.xpath('.//td[@class="pozadie-okrove1"]').children.size != 0
    next if tr.xpath('.//td/h3').children.size != 0 #h3[@class="pozadie-okrove1"]').children.size != 0
    tds = tr.xpath('.//td')

    data = {"date"       => (tds[1].text.strip),
        "supplier"    => (tds[2].text.strip),
        "subject"     => (tds[3].text.strip),
        "price_before" => ((tds[4] || Dummy.new).text.strip),
        "price_after"  => ((tds[5] || Dummy.new).text.strip),
        "institution" => institution}
    ScraperWiki.save_sqlite(unique_keys = [], data = data, table_name = "elaukcie")
  end
end

doc = Nokogiri::HTML(html)
navig = doc.xpath('//ul[@class="navigacia"]/li/a')
navig.each do |nav|
  html = open(SITE + nav['href'])
  doc = Nokogiri::HTML(html)
  doc.xpath('//li[@class="activ"]/ul/li/a').each do |lnk_node|
    case lnk_node
    when /objedn\303\241vky/u then
      htm = ScraperWiki.scrape(SITE + lnk_node['href'])
      dc  = Nokogiri::HTML(htm)
      parse_it(dc, "objednavky")
    when /fakt\303\272ry/u then
      htm = ScraperWiki.scrape(SITE + lnk_node['href'])
      dc  = Nokogiri::HTML(htm)
      parse_it(dc, "faktury")
    when /z\303\241kazky s n\303\255zkymi hodnotami/u then
      htm = ScraperWiki.scrape(SITE + lnk_node['href'])
      dc  = Nokogiri::HTML(htm)
      parse_zsnh(dc)
    when /zmluvy/u then
      htm = ScraperWiki.scrape(SITE + lnk_node['href'])
      dc  = Nokogiri::HTML(htm)
      parse_it(dc, "zmluvy")
    when /elektronick\303\251 aukcie/u then
      htm = ScraperWiki.scrape(SITE + lnk_node['href'])
      dc  = Nokogiri::HTML(htm)
      parse_elektr_aukcie(dc)
    end
  end
end

require 'rubygems'
require 'nokogiri'
require 'open-uri'

#html = ScraperWiki.scrape("http://www.genpro.gov.sk/objednavky--faktury-a-zmluvy")
SITE = "http://www.genpro.gov.sk"
html = ScraperWiki.scrape("#{SITE}/objednavky--faktury-a-zmluvy")

require 'pp'

class Dummy
  def text
    ''
  end
end

def parse_it(doc, t)
  institution = doc.at_xpath('//td[@class="middle-holder2"]/h1').text
  doc.xpath('//table[@class="tab-kontakt"]/tbody/tr').each do |tr|
    next if tr.xpath('.//td[@class="pozadie-okrove1"]').children.size != 0
    next if tr.xpath('.//td/h3').children.size != 0 #h3[@class="pozadie-okrove1"]').children.size != 0
    tds = tr.xpath('.//td')

    data = {"date"       => (tds[1].text.strip),
        "supplier"    => (tds[2].text.strip),
        "subject"     => (tds[3].text.strip),
        "price"       => ((tds[4] || Dummy.new).text.strip),
        "institution" => institution}
    ScraperWiki.save_sqlite(unique_keys = [], data = data, table_name = t)
  end
end

def parse_zsnh(doc)
  institution = doc.at_xpath('//td[@class="middle-holder2"]/h1').text
  doc.xpath('//table[@class="tab-kontakt"]/tbody/tr').each do |tr|
    next if tr.xpath('.//td[@class="pozadie-okrove1"]').children.size != 0
    next if tr.xpath('.//td/h3').children.size != 0 #h3[@class="pozadie-okrove1"]').children.size != 0
    tds = tr.xpath('.//td')

    data = {"date"       => (tds[0].text.strip),
        "supplier"    => (tds[1].text.strip),
        "subject"     => (tds[2].text.strip),
        "price"       => ((tds[3] || Dummy.new).text.strip),
        "institution" => institution}
    ScraperWiki.save_sqlite(unique_keys = [], data = data, table_name = 'zsnh')
  end

end

def parse_elektr_aukcie(doc)
  institution = doc.at_xpath('//td[@class="middle-holder2"]/h1').text
  doc.xpath('//table[@class="tab-kontakt"]/tbody/tr').each do |tr|
    next if tr.xpath('.//td[@class="pozadie-okrove1"]').children.size != 0
    next if tr.xpath('.//td/h3').children.size != 0 #h3[@class="pozadie-okrove1"]').children.size != 0
    tds = tr.xpath('.//td')

    data = {"date"       => (tds[1].text.strip),
        "supplier"    => (tds[2].text.strip),
        "subject"     => (tds[3].text.strip),
        "price_before" => ((tds[4] || Dummy.new).text.strip),
        "price_after"  => ((tds[5] || Dummy.new).text.strip),
        "institution" => institution}
    ScraperWiki.save_sqlite(unique_keys = [], data = data, table_name = "elaukcie")
  end
end

doc = Nokogiri::HTML(html)
navig = doc.xpath('//ul[@class="navigacia"]/li/a')
navig.each do |nav|
  html = open(SITE + nav['href'])
  doc = Nokogiri::HTML(html)
  doc.xpath('//li[@class="activ"]/ul/li/a').each do |lnk_node|
    case lnk_node
    when /objedn\303\241vky/u then
      htm = ScraperWiki.scrape(SITE + lnk_node['href'])
      dc  = Nokogiri::HTML(htm)
      parse_it(dc, "objednavky")
    when /fakt\303\272ry/u then
      htm = ScraperWiki.scrape(SITE + lnk_node['href'])
      dc  = Nokogiri::HTML(htm)
      parse_it(dc, "faktury")
    when /z\303\241kazky s n\303\255zkymi hodnotami/u then
      htm = ScraperWiki.scrape(SITE + lnk_node['href'])
      dc  = Nokogiri::HTML(htm)
      parse_zsnh(dc)
    when /zmluvy/u then
      htm = ScraperWiki.scrape(SITE + lnk_node['href'])
      dc  = Nokogiri::HTML(htm)
      parse_it(dc, "zmluvy")
    when /elektronick\303\251 aukcie/u then
      htm = ScraperWiki.scrape(SITE + lnk_node['href'])
      dc  = Nokogiri::HTML(htm)
      parse_elektr_aukcie(dc)
    end
  end
end


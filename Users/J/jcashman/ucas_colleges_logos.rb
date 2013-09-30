require 'open-uri'
require 'nokogiri'
require 'mechanize'

url = 'http://search.ucas.com/cgi-bin/hsrun/search/search/search.hjx;start=search.HsCodeSearch.run?y=2013&w=H'

agent = Mechanize.new
page = agent.get(url)
search_form = page.form_with(:name => "Form1")
select = search_form.field_with(:name => "cmbInst")

def scrape_courses(page, code)
  university_name = page.search('//a[@class="bodyTitle"]').first.text
  page.search('//div[@class="bodyText"]/table/tr').each do |tr|
    link = tr.at_css('a')
    if link and tr.at_css('span.bodyTextSmallGrey')
      course = link.text
      course_code = $1 if tr.at_css('span.bodyTextSmallGrey').text =~ /\((.+)\)/
      course_type = tr.at_css('font.bodyText').text
      hash = { 
        'key' => "#{code}-#{course_code}-#{course}",
        'course' => link.text, 
        'course_code' => course_code, 
        'course_type' => course_type, 
        'university_name' => university_name, 
        'university_code' => code
      }
     ScraperWiki.save_sqlite(unique_keys=['key'], data=hash)
      
    end
  end
end

uni_codes = select.options.map { |c| c.to_s }

#uni_codes = ['S76',  'S77',  'S78',  'S79',  'S82',  'S84',  'S85',  'S90',  'S93',  'S96',  'S98',  'T10',  'T20',  'T80',  'T85',  'T90',  'U20',  'U40',  'U65',  'U80',  'U95',  'W05',  'W08',  'W12',  'W17',  'W20',  'W25',  'W35',  'W36',  'W50',  'W51',  'W52',  'W65',  'W67',  'W73',  'W74',  'W75',  'W76',  'W80',  'W81',  'W85',  'Y50',  'Y70',  'Y75',  'Y80']


uni_codes.each do |code|
  next if code == ''
  
  search_form = page.form_with(:name => "Form1")
  select.value = code
  
  search_results = agent.submit(search_form)
  while search_results do
    scrape_courses(search_results, code)
    next_page = page.search('//a[text()="next page"]').first
    search_results = next_page.nil? ? nil : agent.click(next_page)
  end
end

require 'open-uri'
require 'nokogiri'
require 'mechanize'

url = 'http://search.ucas.com/cgi-bin/hsrun/search/search/search.hjx;start=search.HsCodeSearch.run?y=2013&w=H'

agent = Mechanize.new
page = agent.get(url)
search_form = page.form_with(:name => "Form1")
select = search_form.field_with(:name => "cmbInst")

def scrape_courses(page, code)
  university_name = page.search('//a[@class="bodyTitle"]').first.text
  page.search('//div[@class="bodyText"]/table/tr').each do |tr|
    link = tr.at_css('a')
    if link and tr.at_css('span.bodyTextSmallGrey')
      course = link.text
      course_code = $1 if tr.at_css('span.bodyTextSmallGrey').text =~ /\((.+)\)/
      course_type = tr.at_css('font.bodyText').text
      hash = { 
        'key' => "#{code}-#{course_code}-#{course}",
        'course' => link.text, 
        'course_code' => course_code, 
        'course_type' => course_type, 
        'university_name' => university_name, 
        'university_code' => code
      }
     ScraperWiki.save_sqlite(unique_keys=['key'], data=hash)
      
    end
  end
end

uni_codes = select.options.map { |c| c.to_s }

#uni_codes = ['S76',  'S77',  'S78',  'S79',  'S82',  'S84',  'S85',  'S90',  'S93',  'S96',  'S98',  'T10',  'T20',  'T80',  'T85',  'T90',  'U20',  'U40',  'U65',  'U80',  'U95',  'W05',  'W08',  'W12',  'W17',  'W20',  'W25',  'W35',  'W36',  'W50',  'W51',  'W52',  'W65',  'W67',  'W73',  'W74',  'W75',  'W76',  'W80',  'W81',  'W85',  'Y50',  'Y70',  'Y75',  'Y80']


uni_codes.each do |code|
  next if code == ''
  
  search_form = page.form_with(:name => "Form1")
  select.value = code
  
  search_results = agent.submit(search_form)
  while search_results do
    scrape_courses(search_results, code)
    next_page = page.search('//a[text()="next page"]').first
    search_results = next_page.nil? ? nil : agent.click(next_page)
  end
end


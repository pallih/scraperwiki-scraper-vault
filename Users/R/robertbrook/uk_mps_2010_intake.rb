require 'nokogiri'

starting_url = 'http://duckduckgo.com/c/UK_MPs_2010%E2%80%93'
html = ScraperWiki.scrape(starting_url)

doc = Nokogiri::HTML(html)
doc.search('div.cr1.cm').each do |cm|
    #p cm
    #cm.search('div.ci2 img').each do |ci2|
      #puts ci2
    #end

    mp_name = ""
    mp_url = ""

    cm.search('div.cl1s a').each do |a|
      mp_name = a.inner_html
      mp_url = a.attr('href')
    end
    
    record = {'mp_name' => mp_name, 'ddg_url' => 'http://duckduckgo.com' + mp_url} if mp_name != ""
    ScraperWiki.save(['mp_name'], record)
end

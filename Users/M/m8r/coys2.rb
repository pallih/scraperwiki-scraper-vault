# Blank Ruby

def read_page(url)
  puts "this is the read page function"
  puts url
  #html1 = ScraperWiki.scrape(dir_base_html_with_name)           
  html1 = ScraperWiki.scrape(url)   
  doc1 = Nokogiri::HTML(html1)
  #for v in doc1.search("li")
  #  puts v
  #end
  doc1.css('li').each do |link|
    puts link.content
    puts "link content in read page"
  end
  #does_exist(url)
  puts "END OF THE READ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
end


#director_name = "patrick rippin"
# LOTS OF RESULTS MATCHING NAME
$director_name = "john buchanan"

# FORMAT DIRECTOR NAME
$director_name.gsub!(/ / , '+')
puts $director_name

#coy_base_html = "http://coys.co.nz/search/?q="

$time_to_exit = 0
$dir_base_html = "http://coys.co.nz/director-search/?q="
$page_number = 0
$page_str = '0'
$page_suffix = "&o=" + $page_str

dir_base_html_with_name = $dir_base_html + $director_name + $page_suffix
puts dir_base_html_with_name

require 'nokogiri'          
  puts "***********************************************"
  read_page(dir_base_html_with_name)  
  puts 'calling the next scrape with value of ....'
  puts $page_number
  #scrape_next_page(dir_base_html_with_name, $page_number)         



# Blank Ruby

def read_page(url)
  puts "this is the read page function"
  puts url
  #html1 = ScraperWiki.scrape(dir_base_html_with_name)           
  html1 = ScraperWiki.scrape(url)   
  doc1 = Nokogiri::HTML(html1)
  #for v in doc1.search("li")
  #  puts v
  #end
  doc1.css('li').each do |link|
    puts link.content
    puts "link content in read page"
  end
  #does_exist(url)
  puts "END OF THE READ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
end


#director_name = "patrick rippin"
# LOTS OF RESULTS MATCHING NAME
$director_name = "john buchanan"

# FORMAT DIRECTOR NAME
$director_name.gsub!(/ / , '+')
puts $director_name

#coy_base_html = "http://coys.co.nz/search/?q="

$time_to_exit = 0
$dir_base_html = "http://coys.co.nz/director-search/?q="
$page_number = 0
$page_str = '0'
$page_suffix = "&o=" + $page_str

dir_base_html_with_name = $dir_base_html + $director_name + $page_suffix
puts dir_base_html_with_name

require 'nokogiri'          
  puts "***********************************************"
  read_page(dir_base_html_with_name)  
  puts 'calling the next scrape with value of ....'
  puts $page_number
  #scrape_next_page(dir_base_html_with_name, $page_number)         




# Aim is to identify pool of companies and their co-owners for a nominated individual.
# Ownership may be historical.
# Need to identify if there is more than individual/where a name is common.

# Blank Ruby

def read_page(director_name)
  if $first_time == 0
     $page_number = 0
     $first_time = 1
  end
  $page_str  = $page_number.to_s
  $page_suffix = "&o=" + $page_str
  dir_base_html_with_name = $dir_base_html + director_name + $page_suffix 
  puts "this is the read page function"
      html1 = ScraperWiki.scrape(dir_base_html_with_name)   
      doc1 = Nokogiri::HTML(html1)
      doc1.css('li').each do |link|
        data = {
      'data_a' => link.content
      }
        puts link.content
        #link.content.to_json
        ScraperWiki.save_sqlite(unique_keys=['data_a'], data=data) 
        puts "link content in read page"
      end
  puts dir_base_html_with_name
  does_exist(dir_base_html_with_name)      
  $page_number = $page_number + 10
  puts $page_number
  puts "that was page number"
  $page_str = $page_number.to_s
  new_page_number = $page_str
  str_page = new_page_number.to_s
  $page_suffix = "&o=" + $page_str
    if $page_number == 50
      return
    end
  read_page($director_name)
end

def does_exist(url)
  puts "this is the does exist func"
  potential_html = ScraperWiki.scrape(url)
  doc1 = Nokogiri::HTML(potential_html)
  doc1.css('li').each do |link|
    puts link.content
    if link.content = "No results."
      puts "No results"
      $time_to_exit = 1
     return
    else
      puts "we are happy to continue"
      html1 = ScraperWiki.scrape(dir_base_html_with_name)   
      #doc1 = Nokogiri::HTML(html1)
      #doc1.css('li').each do |link|
      #  puts link.content
      #  puts "link content in read page"
      #end
      #scrape_next_page(url)
    end
  end
end


# FUNCTION/PRODUCEDURE 
def scrape_next_page(url , page)
  puts "this is a function"
  puts page
  puts "that was the current page"
  #iterand += 10
  puts "where is the new...."
  page = $page_number + 10 
  $page_number = page
  puts page
  new_page_number = page.to_s
  #new_page_number = current_page+10
  str_page = new_page_number.to_s
  #read_page(url)
  new_page_suffix = "&o=" + str_page 
  new_page_url = $dir_base_html + $director_name + new_page_suffix
  puts new_page_url
  does_exist(new_page_url)
  if $time_to_exit == 0
  read_page(new_page_url)
  else
  puts "should exit about now"
  end
end

##############################
# no records found
##############################
#$director_name = "rippun patrick"
# one company record returned
$director_name = "pat rippin"
# one individual 2 company records
 $director_name = "ABERHART Morris"
#$director_name = "john buchanan"

# FORMAT DIRECTOR NAME
$director_name.gsub!(/ / , '+')
puts $director_name

#coy_base_html = "http://coys.co.nz/search/?q="

$time_to_exit = 0
$dir_base_html = "http://coys.co.nz/director-search/?q="
$page_number = 0
$page_str = '0'
$page_suffix = "&o=" + $page_str
$first_time = 0

#dir_base_html_with_name = $dir_base_html + $director_name + $page_suffix

#puts dir_base_html_with_name

#puts html1

#html = ScraperWiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")           
#puts html

require 'nokogiri'          
  puts "***********************************************"
  read_page($director_name)
  
  

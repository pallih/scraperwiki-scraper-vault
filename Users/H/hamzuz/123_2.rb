  # open the required libraries
  require 'rubygems'
  require 'nokogiri'
  require 'open-uri'

#BASE_WIKIPEDIA_URL = "http://en.wikipedia.org"
#LIST_URL = "#{BASE_WIKIPEDIA_URL}/wiki/List_of_Nobel_laureates"

  list_of_profiles_page = Nokogiri::HTML(open('http://xfree.co.il/new_list_clean.htm', 'User-Agent' => 'ruby'))
 
  an_array_of_links = list_of_profiles_page.xpath("//a")

  an_array_of_links.each do |link_to_test|

  link_to_member_journal = link_to_test["href"] +"/journal"


# now let's fetch that page
begin
  member_journal_page = Nokogiri::HTML(open(link_to_member_journal,'User-Agent' => 'ruby' ))
rescue Exception=>e
  #puts "Error: #{e}"
else
  
all_closed_trade_dates = member_journal_page.xpath("//span[@class='date']")


 if all_closed_trade_dates && all_closed_trade_dates[0] #if trader made any trades? than...
  # change dates string with attributes into just text values
  date=all_closed_trade_dates[1].text
  #extract the last text string (==yaer)
  date_year = date.split[-1]
  # is the text string == 2013
  if date_year == "2013"
  
  #goto member statistics & parse it
  puts link_to_member_statistics = link_to_test["href"] +"/statistics"
  member_statistics = Nokogiri::HTML(open(link_to_member_statistics,'User-Agent' => 'ruby' ))
  gain_loss = member_statistics.xpath("//div[@class='data-wrapper']").text #done
  accuracy = member_statistics.xpath("//dt[@class='wins']").text 
  accuracy_percentage=member_statistics.xpath("//dd[@class='wins']").text 
  in_depth_stats_block=member_statistics.xpath("//div[@class='in-depth-stats block']").text.split
  total_pips = in_depth_stats_block[25]
  total_trades = in_depth_stats_block[4]
  
    puts "Gain/Loss: #{gain_loss}"
    puts "Last Closed Trade: #{date}"
    puts "Win Accuracy : #{accuracy} (#{accuracy_percentage})"
    puts "Total Trades: #{total_trades}"
    puts "Open trades: #{in_depth_stats_block[7]}"
    puts "Canceled trades: #{in_depth_stats_block[13]}"
    puts "Total pips: #{total_pips}"
    puts "Best trade (pips): #{in_depth_stats_block[49]}"
    puts "Average win (pips): #{in_depth_stats_block[65]}"
    puts "Average loss (pips): #{in_depth_stats_block[69]}"

  end #done: are the trades were excuted at 2013
  end #done: if trader made any trades?
ensure
end # done: begin/rescue


#************************************-----------------------------------**************************************


end #done: an_array_of_links.each


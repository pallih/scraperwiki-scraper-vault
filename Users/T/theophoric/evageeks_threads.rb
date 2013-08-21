require 'rubygems'
require 'mechanize'

ScraperWiki::attach("evageeks_forumlist", "src")

forumlist = ScraperWiki::select("* from src.swdata")


# initialize new mechanize agent, login, open page at member list
base_url = "http://forum.evageeks.org"

agent = Mechanize.new

for forum in forumlist do
  puts "FORUM - [#{forum["_identifier"]}] - #{forum["title"]} - #{forum["href"]}"
  forum_id = forum["forum_id"]
  threadlist_page = agent.get(base_url + forum["href"])
  page_counter = 1
  fields = %w{_identifier thread_id title href author post_count view_count last_post_time}
  while threadlist_page.links_with(:text => "Next").any? 
    puts "[#{forum_id}] - #{forum["title"]} - Page #{page_counter}"
    threadlist_page.search("//tr[starts-with(@id, 'topic_')]").each_with_index do |thread_tr, i|
      thread_tds = thread_tr.search(".row1, .row2,.row3, .row3Right")
#      thread_tds.each_with_index do |thread_td, j|
#        puts "[#{i}][#{j}] = #{thread_td.text}"
#      end
      link = thread_tds[1].search("a.topictitle").first
      unless link.nil? 
        title = link.text.to_s.downcase
        puts "\t[#{page_counter}][#{i}] - #{title}"
        href = link.attribute("href").text
        thread_id = href.match(/thread\/(\d+)/)[1].to_i
        _identifier = "f-#{forum_id}_t-#{thread_id}"
        post_count = thread_tds[2].text.to_i
        view_count = thread_tds[3].text.to_i
        author_username = thread_tds[4].text
        author = {:username => author_username}
        author_link = thread_tds[4].search("span.name a").first
        unless author_link.nil? 
          author_href = author_link.attribute("href").text
          author[:href] = author_href
          author[:user_id] = author_href.match(/&u=(\d+)/)[1].to_i                
        end
        last_post_time = DateTime.parse(thread_tds[5].text)
        data = {}
        fields.each do |field|
          data[field] = eval(field)
        end
        ScraperWiki::save_sqlite(['_identifier'], data)
      end
    end
    page_counter = page_counter + 1
    threadlist_page = threadlist_page.links_with(:text => "Next").first.click
  end
end



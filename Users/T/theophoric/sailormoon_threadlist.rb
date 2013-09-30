require 'rubygems'
require 'mechanize'



# initialize new mechanize agent, login, open page at member list
base_url = "http://sailormoonforum.com"
login_url = base_url + "/ucp.php?mode=login"
forumlist_page = "http://sailormoonforum.com/index.php"
agent = Mechanize.new

login_page = agent.get(login_url)
login_form = login_page.forms.first
login_form.username = "ai53final"
login_form.password = "ai53final"
login_form.redirect = "index.php"
redirect_page = agent.submit(login_form, login_form.buttons.first)



forum_id = "1"
threadlist_page = agent.get(base_url + "./viewforum.php?f=1")
page_counter = 1
while threadlist_page.links_with(:text => "Next").any? 
  puts "[#{forum_id}] - Page #{page_counter}"
  threadlist_page.search("tr").each_with_index do |thread_tr, i|
    td_row1s = thread_tr.search("td.row1")
    td_row2s = thread_tr.search("td.row2")
    if(td_row1s.any?  && td_row2s.any?)
      
      link = td_row1s[2].search("a.topictitle").first
      if link.nil? 
        puts "LINK NOT FOUND -\n #{td_row1s[1].inspect}"
      else
        title = link.text.to_s.downcase
        puts "\t[#{page_counter}][#{i}] - #{title}"
        href = link.attribute("href").text
        thread_id = href.match(/&t=(\d+)/)[1].to_i
        _identifier = "f-#{forum_id}_t-#{thread_id}"
        author_username = td_row2s[0].text
        author = {:username => author_username}
        author_link = td_row2s[0].search("a").first
        unless author_link.nil? 
          author_href = author_link.attribute("href").text
          author[:href] = author_href,
          author[:user_id] = author_href.match(/&u=(\d+)/)[1].to_i                
        end
        post_count = td_row1s[3].text.to_i
        view_count = td_row2s[1].text.to_i
            last_post_time = DateTime.parse(td_row1s[4].search("p").first.text)

        fields = %w{_identifier thread_id title href author post_count view_count last_post_time}
        data = {}
        fields.each do |field|
          data[field] = eval(field)
        end
        ScraperWiki::save_sqlite(['_identifier'], data)
      end
    end
  end
  page_counter = page_counter + 1
  threadlist_page = threadlist_page.links_with(:text => "Next").first.click
end


require 'rubygems'
require 'mechanize'



# initialize new mechanize agent, login, open page at member list
base_url = "http://sailormoonforum.com"
login_url = base_url + "/ucp.php?mode=login"
forumlist_page = "http://sailormoonforum.com/index.php"
agent = Mechanize.new

login_page = agent.get(login_url)
login_form = login_page.forms.first
login_form.username = "ai53final"
login_form.password = "ai53final"
login_form.redirect = "index.php"
redirect_page = agent.submit(login_form, login_form.buttons.first)



forum_id = "1"
threadlist_page = agent.get(base_url + "./viewforum.php?f=1")
page_counter = 1
while threadlist_page.links_with(:text => "Next").any? 
  puts "[#{forum_id}] - Page #{page_counter}"
  threadlist_page.search("tr").each_with_index do |thread_tr, i|
    td_row1s = thread_tr.search("td.row1")
    td_row2s = thread_tr.search("td.row2")
    if(td_row1s.any?  && td_row2s.any?)
      
      link = td_row1s[2].search("a.topictitle").first
      if link.nil? 
        puts "LINK NOT FOUND -\n #{td_row1s[1].inspect}"
      else
        title = link.text.to_s.downcase
        puts "\t[#{page_counter}][#{i}] - #{title}"
        href = link.attribute("href").text
        thread_id = href.match(/&t=(\d+)/)[1].to_i
        _identifier = "f-#{forum_id}_t-#{thread_id}"
        author_username = td_row2s[0].text
        author = {:username => author_username}
        author_link = td_row2s[0].search("a").first
        unless author_link.nil? 
          author_href = author_link.attribute("href").text
          author[:href] = author_href,
          author[:user_id] = author_href.match(/&u=(\d+)/)[1].to_i                
        end
        post_count = td_row1s[3].text.to_i
        view_count = td_row2s[1].text.to_i
            last_post_time = DateTime.parse(td_row1s[4].search("p").first.text)

        fields = %w{_identifier thread_id title href author post_count view_count last_post_time}
        data = {}
        fields.each do |field|
          data[field] = eval(field)
        end
        ScraperWiki::save_sqlite(['_identifier'], data)
      end
    end
  end
  page_counter = page_counter + 1
  threadlist_page = threadlist_page.links_with(:text => "Next").first.click
end



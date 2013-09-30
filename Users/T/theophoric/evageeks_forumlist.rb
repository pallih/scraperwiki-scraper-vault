require 'rubygems'
require 'mechanize'

# initialize new mechanize agent, login, open page at member list
base_url = "http://forum.evageeks.org/"
agent = Mechanize.new



forumlist_page = agent.get(base_url)


# iterate through the paginated listing until the end


forumlist_page.search("tr").each_with_index do |forum_tr, i|
  td_row1s = forum_tr.search("td.row1")
  td_row2s = forum_tr.search("td.row2")
  if(td_row1s.any?  && td_row2s.any?)
    link = td_row1s[1].search("a.forumlink").first
    unless link.nil? 
      href = link.attribute("href").text
      forum_id = href.match(/forum\/(\w+)/)[1]
      _identifier = "f-#{forum_id}"
      title = link.text.downcase
      description = td_row1s[1].search("span.genmed").text
      thread_count = td_row2s[0].text.to_i
      post_count = td_row2s[1].text.to_i
      last_post_time = DateTime.parse(td_row2s[2].text)
      data = {
        :_identifier => _identifier,
        :forum_id => forum_id,
        :href => href,
        :title => title,
        :description => description,
        :thread_count => thread_count,
        :post_count => post_count,
        :last_post_time => last_post_time
      }
      ScraperWiki::save_sqlite(%w{_identifier forum_id}, data)
    end
  end
end

require 'rubygems'
require 'mechanize'

# initialize new mechanize agent, login, open page at member list
base_url = "http://forum.evageeks.org/"
agent = Mechanize.new



forumlist_page = agent.get(base_url)


# iterate through the paginated listing until the end


forumlist_page.search("tr").each_with_index do |forum_tr, i|
  td_row1s = forum_tr.search("td.row1")
  td_row2s = forum_tr.search("td.row2")
  if(td_row1s.any?  && td_row2s.any?)
    link = td_row1s[1].search("a.forumlink").first
    unless link.nil? 
      href = link.attribute("href").text
      forum_id = href.match(/forum\/(\w+)/)[1]
      _identifier = "f-#{forum_id}"
      title = link.text.downcase
      description = td_row1s[1].search("span.genmed").text
      thread_count = td_row2s[0].text.to_i
      post_count = td_row2s[1].text.to_i
      last_post_time = DateTime.parse(td_row2s[2].text)
      data = {
        :_identifier => _identifier,
        :forum_id => forum_id,
        :href => href,
        :title => title,
        :description => description,
        :thread_count => thread_count,
        :post_count => post_count,
        :last_post_time => last_post_time
      }
      ScraperWiki::save_sqlite(%w{_identifier forum_id}, data)
    end
  end
end


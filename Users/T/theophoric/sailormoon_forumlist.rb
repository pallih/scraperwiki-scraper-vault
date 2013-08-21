require 'rubygems'
require 'mechanize'

# initialize new mechanize agent, login, open page at member list
base_url = "http://sailormoonforum.com/"
login_url = base_url + "ucp.php?mode=login"
forumlist_page = base_url + "index.php"
agent = Mechanize.new

login_page = agent.get(login_url)
login_form = login_page.forms.first
login_form.username = "ai53final"
login_form.password = "ai53final"
login_form.redirect = "index.php"
redirect_page = agent.submit(login_form, login_form.buttons.first)




forumlist_page = redirect_page.links_with(:href => Regexp.new("^./index.php")).first.click


# iterate through the paginated listing until the end


forumlist_page.search("tr").each_with_index do |forum_tr, i|
  if([6,(8..13).to_a, (15..18).to_a].flatten.include? (i))
    forum_tds = forum_tr.search("td")
    link = forum_tds[1].search("a.forumlink").first
    unless link.nil? 
      href = link.attribute("href").text
      forum_id = href.match(/\?f=(\d+)/)[1].to_i
      _identifier = "f-#{forum_id}"
      title = link.text.downcase
      description = forum_tds[1].search("p.forumdesc").text.downcase
      thread_count = forum_tds[2].text.to_i
      post_count = forum_tds[3].text.to_i
      last_post_time = DateTime.parse(forum_tds[4].search("p").first.text)
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

# custom links
data = {
  :_identifier => "f-41",
  :forum_id => 41,
  :href => "./viewforum.php?f=41",
  :title => "roleplay corner",
  :description =>"This subforum is for all roleplay-related threads. It's here as a trial. If it is popular enough after a month or two, it'll stick around, otherwise all of its threads will be moved back into the main Sailor Moon Fandom forum.",
  :thread_count => 16,
  :post_count => 1942,
  :last_post_time => DateTime.parse("Sat May 05, 2012 4:17 pm")
}
ScraperWiki::save_sqlite(%w{_identifier forum_id}, data)



require 'rubygems'
require 'mechanize'



# initialize new mechanize agent, open page at member list
url = "http://forum.evageeks.org/memberlist.php?mode=posts&order=DESC"
agent = Mechanize.new
current_page = agent.get(url)

# iterate through the paginated listing until the end
while current_page.links_with(:text => "Next").any? 
  current_page.links_with(:class => "gen", :href => /^\/profile/).each do |profile_link|
    begin
      agent.transact do
        username = profile_link.text
        puts "Loading profile data for " + username

        profile_page = profile_link.click
        posts_per_day = profile_page.search("//tr[3]/td[2]/span").map(&:text)[0].match(/\/ ([0-9,\.]+)/)[1]
        href = profile_link.href
        user_id = href.match(/&u=(\d+)/)[1].to_i
        _identifier = "u-#{user_id}"  
        user_fields = profile_page.search("//tr/td/b/span")
        member_since, post_count, gender, location, occupation, interests, age = user_fields[2..8].map(&:text)
        data = {:_identifier => _identifier, :user_id => user_id, :username => username, :member_since => Date.parse(member_since).to_s, :post_count => post_count, :gender => gender, :location => location,:interests => interests.downcase, :age => age.to_i, :href => href, :posts_per_day => posts_per_day.to_f}

        ScraperWiki::save_sqlite(['username'], data)
      end
    rescue => e
      puts "#{e.class}: #{e.message}"
    end
  end
  current_page = current_page.links_with(:text => "Next").first.click
end
require 'rubygems'
require 'mechanize'



# initialize new mechanize agent, open page at member list
url = "http://forum.evageeks.org/memberlist.php?mode=posts&order=DESC"
agent = Mechanize.new
current_page = agent.get(url)

# iterate through the paginated listing until the end
while current_page.links_with(:text => "Next").any? 
  current_page.links_with(:class => "gen", :href => /^\/profile/).each do |profile_link|
    begin
      agent.transact do
        username = profile_link.text
        puts "Loading profile data for " + username

        profile_page = profile_link.click
        posts_per_day = profile_page.search("//tr[3]/td[2]/span").map(&:text)[0].match(/\/ ([0-9,\.]+)/)[1]
        href = profile_link.href
        user_id = href.match(/&u=(\d+)/)[1].to_i
        _identifier = "u-#{user_id}"  
        user_fields = profile_page.search("//tr/td/b/span")
        member_since, post_count, gender, location, occupation, interests, age = user_fields[2..8].map(&:text)
        data = {:_identifier => _identifier, :user_id => user_id, :username => username, :member_since => Date.parse(member_since).to_s, :post_count => post_count, :gender => gender, :location => location,:interests => interests.downcase, :age => age.to_i, :href => href, :posts_per_day => posts_per_day.to_f}

        ScraperWiki::save_sqlite(['username'], data)
      end
    rescue => e
      puts "#{e.class}: #{e.message}"
    end
  end
  current_page = current_page.links_with(:text => "Next").first.click
end

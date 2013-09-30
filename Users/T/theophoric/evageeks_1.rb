require 'rubygems'
require 'mechanize'



# initialize new mechanize agent, login, open page at member list
login_url = "http://sailormoonforum.com/ucp.php?mode=login"
memberlist_list = "http://sailormoonforum.com/memberlist.php"
agent = Mechanize.new

login_page = agent.get(login_url)
login_form = login_page.forms.first
login_form.username = "ai53final"
login_form.password = "ai53final"
login_form.redirect = "memberlist.php"
redirect_page = agent.submit(login_form, login_form.buttons.first)

memberlist_page = redirect_page.links_with(:text => " Members").first.click
memberlist_page = agent.get(" http://sailormoonforum.com/memberlist.php?mode=&start=2640")

# iterate through the paginated listing until the end
while memberlist_page.links_with(:text => "Next").any? 
  memberlist_page.links_with(:href => Regexp.new("^./memberlist.php.mode=viewprofile")).each do |profile_link|
    begin
      agent.transact do
        data = {}
        username = profile_link.text
        href = profile_link.href
        user_id = href.match(/&u=(\d+)/)[1].to_i
        _identifier = "u-#{user_id}"
        data["user_id"] = user_id
        data["_identifier"] = _identifier
        data["username"] = username
        puts "Loading profile data for " + username

        profile_page = profile_link.click
        profile_fields = profile_page.search('//*[contains(concat( " ", @class, " " ), concat( " ", "genmed", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "gen", " " ))]').to_a.collect(&:text)
        profile_fields.each_with_index do |text, i|
            text = text.to_s.strip.downcase.gsub(" ","_").gsub(":","")
            if %w{joined last_visited}.include?(text)
              next_field = profile_fields[i+1]
              data[text] = Date.parse(profile_fields[i+1]) unless next_field.to_s.length < 5
            elsif %w{location occupation interests age website gender}.include?(text)
              next_field = profile_fields[i+1]
              data[text] = next_field unless %w{location occupation interests age website gender}.include? (next_field.to_s.strip.downcase.gsub(" ","_").gsub(":",""))
            elsif text == "total_posts"
              data["post_count"] = profile_fields[i+1].to_i
              data["posts_per_day"] = profile_fields[i+2].match(/\/ ([0-9,\.]+)/)[1].to_f
            end
        end

        ScraperWiki::save_sqlite(['username'], data)

      end
    rescue => e
      puts "#{e.class}: #{e.message}"
    end
  end
  memberlist_page = memberlist_page.links_with(:text => "Next").last.click
end
require 'rubygems'
require 'mechanize'



# initialize new mechanize agent, login, open page at member list
login_url = "http://sailormoonforum.com/ucp.php?mode=login"
memberlist_list = "http://sailormoonforum.com/memberlist.php"
agent = Mechanize.new

login_page = agent.get(login_url)
login_form = login_page.forms.first
login_form.username = "ai53final"
login_form.password = "ai53final"
login_form.redirect = "memberlist.php"
redirect_page = agent.submit(login_form, login_form.buttons.first)

memberlist_page = redirect_page.links_with(:text => " Members").first.click
memberlist_page = agent.get(" http://sailormoonforum.com/memberlist.php?mode=&start=2640")

# iterate through the paginated listing until the end
while memberlist_page.links_with(:text => "Next").any? 
  memberlist_page.links_with(:href => Regexp.new("^./memberlist.php.mode=viewprofile")).each do |profile_link|
    begin
      agent.transact do
        data = {}
        username = profile_link.text
        href = profile_link.href
        user_id = href.match(/&u=(\d+)/)[1].to_i
        _identifier = "u-#{user_id}"
        data["user_id"] = user_id
        data["_identifier"] = _identifier
        data["username"] = username
        puts "Loading profile data for " + username

        profile_page = profile_link.click
        profile_fields = profile_page.search('//*[contains(concat( " ", @class, " " ), concat( " ", "genmed", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "gen", " " ))]').to_a.collect(&:text)
        profile_fields.each_with_index do |text, i|
            text = text.to_s.strip.downcase.gsub(" ","_").gsub(":","")
            if %w{joined last_visited}.include?(text)
              next_field = profile_fields[i+1]
              data[text] = Date.parse(profile_fields[i+1]) unless next_field.to_s.length < 5
            elsif %w{location occupation interests age website gender}.include?(text)
              next_field = profile_fields[i+1]
              data[text] = next_field unless %w{location occupation interests age website gender}.include? (next_field.to_s.strip.downcase.gsub(" ","_").gsub(":",""))
            elsif text == "total_posts"
              data["post_count"] = profile_fields[i+1].to_i
              data["posts_per_day"] = profile_fields[i+2].match(/\/ ([0-9,\.]+)/)[1].to_f
            end
        end

        ScraperWiki::save_sqlite(['username'], data)

      end
    rescue => e
      puts "#{e.class}: #{e.message}"
    end
  end
  memberlist_page = memberlist_page.links_with(:text => "Next").last.click
end

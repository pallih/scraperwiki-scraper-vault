# Import h() for html escaping
require 'erb'
require 'active_support/core_ext/string/output_safety'
include ERB::Util

# Style
puts %^
<style TYPE="text/css">

body {
    color: #333333;
    font-family: "Lora",Georgia,"Times New Roman",Times,serif;
    font-size: 17px;
    line-height: 26px;
    margin: none;
}

ul {
    padding: 0 !important;
    margin: none;
}

#group_details {
    font-size: 70%;
}

div#scraperwikipane {
    left:10px;
}

h3 {
    height: 10px;
}


.first_sidebar_heading {
    padding-top: 35px;
}

.subsequent_sidebar_heading {
    padding-bottom: 10px;
}

</style>
^

# Spacing
puts "<br />"

# Info
puts "<h3 class='first_sidebar_heading'>Group Details</h3>"

puts %^<pre id="group_details">
{
  when_do_we_meet_up:
    <a href="http://www.meetup.com/rubyireland/" target="_parent">3rd Tue of every month</a>,
  googlegroup: <a href="http://groups.google.com/group/ruby_ireland" target="_parent">ruby_ireland</a>,
  twitter: <a href="http://twitter.com/rubyireland" target="_parent">@rubyireland</a>,
  hashtag: #rubyireland,
  irc: #ruby.ie on freenode,
  related_communities: [
    <a href="http://belfastruby.com/" target="_parent">Belfast Ruby</a>,
    <a href="http://www.rubyireland.com/cork.html" target="_parent">Ruby Cork</a>
  ],
  todo: <a href="http://bit.ly/ritodo" target="_parent">list</a>,
  workers: <a href="http://www.workingwithrails.com/browse/people/country/Ireland" target="_parent">with rails</a>
}
</pre>
^

# Jobs
sourcescraper = 'rubyjobs_ie_scraper'
ScraperWiki::attach(sourcescraper)
data = ScraperWiki::select( "* from rubyjobs_ie_scraper.swdata")

puts "<h3 class='subsequent_sidebar_heading'>Latest Ruby Jobs</h3>"

puts "<ul>"

#JSON::parse(data.first['sponsor_list']).each do |sponsor|
data.each_with_index do |job, i|
  next if i > 4 # display max jobs

  puts "<li>"
  # We don't use the specific job href as we dont't trust any input from rubyjobs.ie
  puts %^<a href="http://www.rubyjobs.ie" target="_blank">#{h(job['title'])}</a> at #{h(job['company'])}^
  puts "#{h(job['blurb'])}"
  puts "</li>"

  #All available data
  #puts "#{job['title']}"
  #puts "#{job['company']}"
  #puts "#{job['location']}"
  #puts "#{job['created_at']}"
end

puts "</ul>"

# Sponsors
sourcescraper = 'ruby_ireland_sponsors_scraper'
ScraperWiki::attach(sourcescraper)
data = ScraperWiki::select( "* from ruby_ireland_sponsors_scraper.swdata")

puts "<h3 class='subsequent_sidebar_heading'>Sponsors</h3>"

puts "<ul style='list-style:none;'>"

JSON::parse(data.first['sponsor_list']).each do |sponsor|
  puts "<li>"
  puts %^<a href="#{sponsor['url']}" target="_blank"><img src="#{sponsor['img_url']}"></a>^
  puts "<p>"
  puts %^<a href="#{sponsor['url']}" target="_blank">#{sponsor['name']}</a>^
  puts "#{sponsor['blurb']}"
  puts "</p>"
  puts "</li>"

  #All available data
  #puts "#{sponsor['name']}"
  #puts "#{sponsor['url']}"
  #puts "#{sponsor['blurb']}"
  #puts "#{sponsor['img_url']}"
end

puts "</ul>"



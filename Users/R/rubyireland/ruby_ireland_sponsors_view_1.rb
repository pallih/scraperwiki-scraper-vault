sourcescraper = 'rubyjobs_ie_scraper'
ScraperWiki::attach(sourcescraper)

data = ScraperWiki::select( "* from rubyjobs_ie_scraper.swdata")

puts %^
<style TYPE="text/css">

body {
    color: #333333;
    font-family: "Lora",Georgia,"Times New Roman",Times,serif;
    font-size: 17px;
    line-height: 26px;
}
</style>
^

puts %^
<pre>
{
  when_do_we_meet_up: "3rd Tuesday of every month at 7pm",
  next_meetup: <a href="www.meetup.com/rubyireland/">meetup.com/rubyireland</a>,
  googlegroup: <a href="http://groups.google.com/group/ruby_ireland">ruby_ireland</a>,
  twitter: <a href="http://twitter.com/rubyireland">@rubyireland</a>,
  hashtag: #rubyireland,
  related_communities: [
    <a href="http://belfastruby.com/">Belfast Ruby</a>,
    'Ruby Cork'
  ],
  todo: <a href="http://bit.ly/ritodo">list</a>,
  workers: <a href="http://www.workingwithrails.com/browse/people/country/Ireland">doing rails</a>
}
</pre>
^

puts "<br />"
puts "<br />"
puts "<br />"

puts "<ul style='list-style: none;'>"

#JSON::parse(data.first['sponsor_list']).each do |sponsor|
data.each_with_index do |job, i|
  next if i > 4 # display max jobs

  puts "<li>"
  puts %^<a href="http://www.rubyjobs.ie" target="_blank">#{job['title']} at #{job['company']}</a>^
  puts "#{job['blurb']}"
  puts "</li>"

  #All available data
  #puts "#{job['title']}"
  #puts "#{job['company']}"
  #puts "#{job['location']}"
  #puts "#{job['created_at']}"
end

puts "</ul>"

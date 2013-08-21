require 'cgi'

sourcescraper = 'linuxconfau_2012_programme'
ScraperWiki.attach(sourcescraper)

puts "
<link rel='stylesheet' href='https://media.scraperwiki.com/CACHE/css/fa757dd34f80.css' type='text/css' />
<div id='page_outer'>
  <div id='page_inner'>
"

if ENV["URLQUERY"]
  query_string = CGI.parse(ENV["URLQUERY"])
  word = CGI.escape(query_string['word'][0])
  unless word.empty? 
    number_of_talks = ScraperWiki.sqliteexecute("select count('Id') from swdata where Description like '%#{word}%'")["data"][0][0]

    puts "<h1>There are #{number_of_talks} talks that mention #{word} in the abstract</h1><br>"
  end
end

puts "
  <form action='' method='get'>
    <h2>How many LCA2012 talks mention...<input type='text' name='word'/><input type='submit' value='Tell me!' /></h2>
  </form>
"

puts "
  </div>
</div>
"
###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
img_root = 'http://mastodonoverblower.tadalist.com'
starting_url = 'http://mastodonoverblower.tadalist.com/lists/1846465/public'
html = ScraperWiki.scrape(starting_url)

record = {}

#top level: the whole list div, class="ListHeader"

# use Nokogiri to get all <tr>
doc = Nokogiri::HTML(html)

doc.search('tr').each do |tr|
    puts tr.object_id
    todoid = tr.object_id

    #make the img point to a fully qualified URI
    checkbox_img = tr.css('td.check img').first    
    fulluri = "#{img_root}#{checkbox_img['src']}"
    #puts fulluri
    checkbox_img['src'] = fulluri

    checkbox = tr.css('td.check').first
    #checkbox['src'] = fulluri
    puts checkbox.inner_html
    record['checkbox'] = checkbox.inner_html

    todo = tr.css('td.itemtext')
    puts todo
    record['todo'] = todo
    ScraperWiki.save(unique_keys=['todoid', 'checkbox',  'todo'], data={"todoid" => todoid, "checkbox" => checkbox.inner_html, "todo" => todo.inner_html})
 
end 
 
doc.search('div.ListHeader').each do |todolist|
#      <h1>Sasona Technology</h1>
 
    listname = todolist.css('h1').first
    puts listname.content
    description = todolist.css('p').first
    puts description.content

    listhtml = doc.css('div.Left div.col')
    puts listhtml

    ScraperWiki.save(unique_keys=['listname',  'description', 'listhtml'], data={"listname" => listname.content, "description" => description.content, "listhtml" => listhtml})
end


###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
#starting_url = 'http://mastodonoverblower.tadalist.com/lists/1846465'
starting_url = 'http://mastodonoverblower.tadalist.com/lists/1846465/public'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all tables
#doc = Nokogiri::HTML(html)
#doc.search('table').each do |td|
#    puts td.inner_html
#    record = {'table' => td.inner_html}
#    ScraperWiki.save(['table'], record)
#end

# use Nokogiri to get all <td>
#doc = Nokogiri::HTML(html)
#doc.search('td').each do |td|
#    puts td.inner_html
#    record = {'td' => td.inner_html}
#    ScraperWiki.save(['td'], record)
#end

#using css selector to get todo items
#doc = Nokogiri::HTML(html)
#doc.css('td.itemtext').each do |td_with_itemtext_class|
#    puts td_with_itemtext_class.content
#    record = {'todo' => td_with_itemtext_class.content}
#    ScraperWiki.save(['todo'], record)
#end

#using css selector to get todo items
#doc = Nokogiri::HTML(html)
#doc.css('td.itemtext').each do |td_with_itemtext_class|
 #    puts td_with_itemtext_class.content
 #    record = {'todo' => td_with_itemtext_class.content}
 #    ScraperWiki.save(['todo'], record)
#end

#record = {'table' => "<table>"}
#puts "<table>"
#ScraperWiki.save(['table'], record)

record = {}

#top level: the whole list div, class="ListHeader"

# use Nokogiri to get all <tr>
doc = Nokogiri::HTML(html)
doc.search('div.ListHeader').each do |todolist|
#      <h1>Sasona Technology</h1>

    listname = todolist.css('h1').first
    puts listname.content
    description = todolist.css('p').first
    puts description.content
    ScraperWiki.save(unique_keys=['listname',  'description'], data={"listname" => listname.content, "description" => description.content})

#    ScraperWiki.save(unique_keys=['listname', 'checkbox', 'todo'], data={"listname" => listname, "checkbox" => cb, "todo" => todo})
  
# use Nokogiri to get all <tr>
#doc = Nokogiri::HTML(html)
#doc.search('tr').each do |tr|
    #puts doc.css('tr').first
#    todolist.css('tr').each do |tr|
#        puts tr
#        checkbox = tr.css('td.check')
#        puts checkbox.content
#        record['checkbox'] = checkbox.content

#        todo = tr.css('td.itemtext')
#        puts todo.content
#        record['todo'] = todo.content
#
#        tr.search('td').each do |td|
#        puts tr.inner_html
#        record = {'tr' => tr.inner_html}
#        ScraperWiki.save(['tr'], record)
#    end

end

doc.search('tr').each do |tr|
    puts tr.id
    todoid = tr.id

    checkbox = tr.css('td.check')
    puts checkbox.inner_html
    record['checkbox'] = checkbox.inner_html

    todo = tr.css('td.itemtext')
    puts todo
    record['todo'] = todo
    ScraperWiki.save(unique_keys=['todoid', 'checkbox',  'todo'], data={"todoid" => todoid, "checkbox" => checkbox.inner_html, "todo" => todo.inner_html})
 
end 

#record = {'table' => "</table>"}
#puts "</table>"
#ScraperWiki.save(['table'], record)
 
###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
#starting_url = 'http://mastodonoverblower.tadalist.com/lists/1846465'
starting_url = 'http://mastodonoverblower.tadalist.com/lists/1846465/public'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all tables
#doc = Nokogiri::HTML(html)
#doc.search('table').each do |td|
#    puts td.inner_html
#    record = {'table' => td.inner_html}
#    ScraperWiki.save(['table'], record)
#end

# use Nokogiri to get all <td>
#doc = Nokogiri::HTML(html)
#doc.search('td').each do |td|
#    puts td.inner_html
#    record = {'td' => td.inner_html}
#    ScraperWiki.save(['td'], record)
#end

#using css selector to get todo items
#doc = Nokogiri::HTML(html)
#doc.css('td.itemtext').each do |td_with_itemtext_class|
#    puts td_with_itemtext_class.content
#    record = {'todo' => td_with_itemtext_class.content}
#    ScraperWiki.save(['todo'], record)
#end

#using css selector to get todo items
#doc = Nokogiri::HTML(html)
#doc.css('td.itemtext').each do |td_with_itemtext_class|
 #    puts td_with_itemtext_class.content
 #    record = {'todo' => td_with_itemtext_class.content}
 #    ScraperWiki.save(['todo'], record)
#end

#record = {'table' => "<table>"}
#puts "<table>"
#ScraperWiki.save(['table'], record)

record = {}

#top level: the whole list div, class="ListHeader"

# use Nokogiri to get all <tr>
doc = Nokogiri::HTML(html)
doc.search('div.ListHeader').each do |todolist|
#      <h1>Sasona Technology</h1>

    listname = todolist.css('h1').first
    puts listname.content
    description = todolist.css('p').first
    puts description.content
    ScraperWiki.save(unique_keys=['listname',  'description'], data={"listname" => listname.content, "description" => description.content})

#    ScraperWiki.save(unique_keys=['listname', 'checkbox', 'todo'], data={"listname" => listname, "checkbox" => cb, "todo" => todo})
  
# use Nokogiri to get all <tr>
#doc = Nokogiri::HTML(html)
#doc.search('tr').each do |tr|
    #puts doc.css('tr').first
#    todolist.css('tr').each do |tr|
#        puts tr
#        checkbox = tr.css('td.check')
#        puts checkbox.content
#        record['checkbox'] = checkbox.content

#        todo = tr.css('td.itemtext')
#        puts todo.content
#        record['todo'] = todo.content
#
#        tr.search('td').each do |td|
#        puts tr.inner_html
#        record = {'tr' => tr.inner_html}
#        ScraperWiki.save(['tr'], record)
#    end

end

doc.search('tr').each do |tr|
    puts tr.id
    todoid = tr.id

    checkbox = tr.css('td.check')
    puts checkbox.inner_html
    record['checkbox'] = checkbox.inner_html

    todo = tr.css('td.itemtext')
    puts todo
    record['todo'] = todo
    ScraperWiki.save(unique_keys=['todoid', 'checkbox',  'todo'], data={"todoid" => todoid, "checkbox" => checkbox.inner_html, "todo" => todo.inner_html})
 
end 

#record = {'table' => "</table>"}
#puts "</table>"
#ScraperWiki.save(['table'], record)
 

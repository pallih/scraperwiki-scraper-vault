# Blank Ruby

require 'mechanize'
 
class Mechanize::Form
  def postback target, argument
    self['__EVENTTARGET'], self['__EVENTARGUMENT'] = target, argument
    submit
  end
end

agent = Mechanize.new
page = agent.get 'http://bbsmates.com/browsebbs.aspx?BBSName=&AreaCode=314'
 
table = page.at('table#Table1 tr:first-child td:nth-child(2) table.Box1 tr:first-child td table tr')

page.links_with(:href => /Page\$\d+/).each do |link|
  puts link.href
  target, argument = link.href.scan(/'([^']*)'/).flatten
  page = page.form.postback target, argument
  new_page = page.at('table#Table1')
  puts new_page
end







# Blank Ruby

require 'mechanize'
 
class Mechanize::Form
  def postback target, argument
    self['__EVENTTARGET'], self['__EVENTARGUMENT'] = target, argument
    submit
  end
end

agent = Mechanize.new
page = agent.get 'http://bbsmates.com/browsebbs.aspx?BBSName=&AreaCode=314'
 
table = page.at('table#Table1 tr:first-child td:nth-child(2) table.Box1 tr:first-child td table tr')

page.links_with(:href => /Page\$\d+/).each do |link|
  puts link.href
  target, argument = link.href.scan(/'([^']*)'/).flatten
  page = page.form.postback target, argument
  new_page = page.at('table#Table1')
  puts new_page
end







# Blank Ruby

require 'mechanize'
 
class Mechanize::Form
  def postback target, argument
    self['__EVENTTARGET'], self['__EVENTARGUMENT'] = target, argument
    submit
  end
end

agent = Mechanize.new
page = agent.get 'http://bbsmates.com/browsebbs.aspx?BBSName=&AreaCode=314'
 
table = page.at('table#Table1 tr:first-child td:nth-child(2) table.Box1 tr:first-child td table tr')

page.links_with(:href => /Page\$\d+/).each do |link|
  puts link.href
  target, argument = link.href.scan(/'([^']*)'/).flatten
  page = page.form.postback target, argument
  new_page = page.at('table#Table1')
  puts new_page
end








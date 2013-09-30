# Get MySpace Friends

require 'mechanize'

agent = Mechanize.new

myspaceID = "173613124"

page = agent.get("http://www.klicktel.de/branchen/rechtsanwaelte-familienrecht-muenster-westf-3304264-66026719.html")

friendset = page.search("//a[contains(@id, 'friendLink')]")
friends = []
friendset.each do |friend|
  friends << { :name => friend.children.text, :url => friend.attributes["href"].value,  :myspaceID => myspaceID}
end

friends.each do |friend|
  ScraperWiki.save(["myspaceID", "name"], friend)
end

# Get MySpace Friends

require 'mechanize'

agent = Mechanize.new

myspaceID = "173613124"

page = agent.get("http://www.klicktel.de/branchen/rechtsanwaelte-familienrecht-muenster-westf-3304264-66026719.html")

friendset = page.search("//a[contains(@id, 'friendLink')]")
friends = []
friendset.each do |friend|
  friends << { :name => friend.children.text, :url => friend.attributes["href"].value,  :myspaceID => myspaceID}
end

friends.each do |friend|
  ScraperWiki.save(["myspaceID", "name"], friend)
end


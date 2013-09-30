# Shadowlands Scrapper
require 'nokogiri'
require 'active_support/all'


#Methods I got Methodology
module MyMethods

  def MyMethods.display_element(element, attr = nil)
    if element
      puts "Tag: #{element.name}"
      puts "String: #{element.to_s}"
      puts "Attribute: #{element.attr(attr)}" if attr
      true
    else
      puts "Nil"
      false
    end
  end

  def MyMethods.dedash(string)
    if string.include? ("-")
      string.to(string.index("-") - 1).chomp
    else
      string.chomp
    end
  end

end

#I have class... Declarations
class State #Used for each State page
  attr_accessor :name, :url, :hauntings
  cattr_accessor :states
  self.states = []
  
  def initialize(name = "", url = "", hauntings = [])
    self.name = name
    self.url = url
    self.hauntings = hauntings
  end

  def to_s
    "State |-- Name: #{name} | URL: #{url} --|"
  end

  def self.remove_state(name)
    states.each { |state| states.delete(state) if state.name == name }
  end

end

class Haunting #Each Instance of Haunting can return a tuple for entry into SQLite datastore
  attr_accessor :location, :name, :description, :state_name

  def initialize(name, location, description, state_name)
    self.name = name
    self.location = location
    self.description = description
    self.state_name = state_name
  end

  def to_s
    "== #{name} -- #{location}, #{state_name} -- #{description[0..19]}... =="
  end
  
  #Return a Dictionary for entry into SQLite
  def tuple
    Hash["Name" => name, "Location" => location, "State" => state_name, "Description" => description]
  end

  #Return a Array that is used as a unique key when saving to SQLite
  def unique_key
    Array["Name","Location"]    
  end
end


#Scrape Data to create a list of States

html = ScraperWiki::scrape("http://theshadowlands.net/places/")
doc = Nokogiri::HTML(html)

# Scrape array of states with urls
State.states = []
state_count = 0
doc.xpath('//table[1]//a').each do |anchor|
  if anchor.text == "" or anchor.text == "Review This Site" or anchor.text.include?("Haunted")
    puts "Value Ignored"
  else
    state = State.new(anchor.text, anchor.attributes['href'])
    State.states << state
    state_count += 1
    puts "#{state_count} : #{state.to_s}"
  end
end

State.remove_state("California")
State.states << State.new("California", "http://theshadowlands.net/places/california1.htm")
State.states << State.new("California", "http://theshadowlands.net/places/california2.htm")
State.states << State.new("California", "http://theshadowlands.net/places/california3.htm")

State.remove_state("Texas")
State.states << State.new("Texas", "http://theshadowlands.net/places/texas1.htm")
State.states << State.new("Texas", "http://theshadowlands.net/places/texas2.htm")

puts "#{State.states.length} States found."

# Got to each state page and build a dictionary of hautings.
State.states.each do |state|
#state = State.states[0] 
  puts "||-- Begin #{state.to_s}--||"
  state_html = ScraperWiki::scrape(state.url)
  state_doc = Nokogiri::HTML(state_html)
  haunting_count = 1
  state_name = state.name 
  state_doc.xpath("//font[@color='#ff9900']").each do |location_ft|
    
    #puts "==location (Parent Tag) location_ft.parent=="
    #MyMethods.display_element(location_ft.parent,'color')
    if (location_ft.next and location_ft.next.attr('color') == "#ff6666") or (location_ft.children[1] and location_ft.children[1].attr('color') == "#ff6666")
      
      #puts "==location location_ft==" 
      #MyMethods.display_element(location_ft,'color')
      location = location_ft.children[0].to_s
      location = MyMethods.dedash(location) 
      #puts location      

      
      if location_ft.next and location_ft.next.attr('color') == "#ff6666"
        #puts "--name Option 1 location_ft.next--" 
        #MyMethods.display_element(location_ft.next,'color')
        name_ft = location_ft.next
      elsif location_ft.children[1] and location_ft.children[1].attr('color') == "#ff6666"
        #puts "--name Option 2 location_ft.children[1]--"
        #MyMethods.display_element(location_ft.children[1],'color')
        name_ft = location_ft.children[1]
      else
        puts "No name found."
        name_ft = location_ft
        name = ""
      end
      unless name_ft == location_ft
        name = name_ft.children[0].to_s 
        name = MyMethods.dedash(name) 
      end
      #puts name
      
      if name_ft.children[1]
        #puts "--Description Option 1: name_ft.children[1]--"
        #MyMethods.display_element(name_ft.children[1],'color')
        description_ft = name_ft.children[1]
      elsif name_ft.next
        #puts "--Description Option 2: name_ft.next--"
        #MyMethods.display_element(name_ft.next,'color')
        description_ft = name_ft.next
      else
      end
      #Additional Location Information catch      
      
      if description_ft and description_ft.name == 'u'
        name << ": #{description_ft.children[0].to_s}"
        puts "Appended addional name information - #{name}"
        description_ft = description_ft.next if description_ft.next
      end

      description_ft = description_ft.children[0] if description_ft.children[0]
      
      description = ""
      until description_ft.to_s == "<br>" or description_ft.to_s.length < 1 do
        if description_ft.to_s.include? "<br>"
          description << description_ft.to_s.to(description_ft.to_s.index("<br>") - 1)
          break
        end
        description << description_ft.to_s #haunting.description
        description_ft = description_ft.next if description_ft
        puts description_ft.to_s
      end
      #puts description

      haunting = Haunting.new(name, location, description, state_name)
      state.hauntings << haunting
      puts "##{haunting_count} #{haunting.to_s}"
    else
      puts "Validation Failed - Previous Tag: #{location_ft.previous.to_s}"
    end
 

    
    
    haunting_count += 1
    #break if haunting_count >= 50
  end
  puts "||-- End #{state.name} -- Hauntings: #{state.hauntings.length} --||"
end


#Write Hauntings to SQLite Data store
State.states.each do |state|
  #state = State.states[0]
  puts "Storing #{state.hauntings.length} hauntingins from #{state.name} to SQLite"
  state.hauntings.each do |haunting|
  ScraperWiki::save_sqlite(haunting.unique_key, haunting.tuple)
    puts "Stored #{haunting.to_s}."
  end
end

State.states.each {|state| puts "Number of hauntings in #{state.name}: #{state.hauntings.length}"}
    
# Shadowlands Scrapper
require 'nokogiri'
require 'active_support/all'


#Methods I got Methodology
module MyMethods

  def MyMethods.display_element(element, attr = nil)
    if element
      puts "Tag: #{element.name}"
      puts "String: #{element.to_s}"
      puts "Attribute: #{element.attr(attr)}" if attr
      true
    else
      puts "Nil"
      false
    end
  end

  def MyMethods.dedash(string)
    if string.include? ("-")
      string.to(string.index("-") - 1).chomp
    else
      string.chomp
    end
  end

end

#I have class... Declarations
class State #Used for each State page
  attr_accessor :name, :url, :hauntings
  cattr_accessor :states
  self.states = []
  
  def initialize(name = "", url = "", hauntings = [])
    self.name = name
    self.url = url
    self.hauntings = hauntings
  end

  def to_s
    "State |-- Name: #{name} | URL: #{url} --|"
  end

  def self.remove_state(name)
    states.each { |state| states.delete(state) if state.name == name }
  end

end

class Haunting #Each Instance of Haunting can return a tuple for entry into SQLite datastore
  attr_accessor :location, :name, :description, :state_name

  def initialize(name, location, description, state_name)
    self.name = name
    self.location = location
    self.description = description
    self.state_name = state_name
  end

  def to_s
    "== #{name} -- #{location}, #{state_name} -- #{description[0..19]}... =="
  end
  
  #Return a Dictionary for entry into SQLite
  def tuple
    Hash["Name" => name, "Location" => location, "State" => state_name, "Description" => description]
  end

  #Return a Array that is used as a unique key when saving to SQLite
  def unique_key
    Array["Name","Location"]    
  end
end


#Scrape Data to create a list of States

html = ScraperWiki::scrape("http://theshadowlands.net/places/")
doc = Nokogiri::HTML(html)

# Scrape array of states with urls
State.states = []
state_count = 0
doc.xpath('//table[1]//a').each do |anchor|
  if anchor.text == "" or anchor.text == "Review This Site" or anchor.text.include?("Haunted")
    puts "Value Ignored"
  else
    state = State.new(anchor.text, anchor.attributes['href'])
    State.states << state
    state_count += 1
    puts "#{state_count} : #{state.to_s}"
  end
end

State.remove_state("California")
State.states << State.new("California", "http://theshadowlands.net/places/california1.htm")
State.states << State.new("California", "http://theshadowlands.net/places/california2.htm")
State.states << State.new("California", "http://theshadowlands.net/places/california3.htm")

State.remove_state("Texas")
State.states << State.new("Texas", "http://theshadowlands.net/places/texas1.htm")
State.states << State.new("Texas", "http://theshadowlands.net/places/texas2.htm")

puts "#{State.states.length} States found."

# Got to each state page and build a dictionary of hautings.
State.states.each do |state|
#state = State.states[0] 
  puts "||-- Begin #{state.to_s}--||"
  state_html = ScraperWiki::scrape(state.url)
  state_doc = Nokogiri::HTML(state_html)
  haunting_count = 1
  state_name = state.name 
  state_doc.xpath("//font[@color='#ff9900']").each do |location_ft|
    
    #puts "==location (Parent Tag) location_ft.parent=="
    #MyMethods.display_element(location_ft.parent,'color')
    if (location_ft.next and location_ft.next.attr('color') == "#ff6666") or (location_ft.children[1] and location_ft.children[1].attr('color') == "#ff6666")
      
      #puts "==location location_ft==" 
      #MyMethods.display_element(location_ft,'color')
      location = location_ft.children[0].to_s
      location = MyMethods.dedash(location) 
      #puts location      

      
      if location_ft.next and location_ft.next.attr('color') == "#ff6666"
        #puts "--name Option 1 location_ft.next--" 
        #MyMethods.display_element(location_ft.next,'color')
        name_ft = location_ft.next
      elsif location_ft.children[1] and location_ft.children[1].attr('color') == "#ff6666"
        #puts "--name Option 2 location_ft.children[1]--"
        #MyMethods.display_element(location_ft.children[1],'color')
        name_ft = location_ft.children[1]
      else
        puts "No name found."
        name_ft = location_ft
        name = ""
      end
      unless name_ft == location_ft
        name = name_ft.children[0].to_s 
        name = MyMethods.dedash(name) 
      end
      #puts name
      
      if name_ft.children[1]
        #puts "--Description Option 1: name_ft.children[1]--"
        #MyMethods.display_element(name_ft.children[1],'color')
        description_ft = name_ft.children[1]
      elsif name_ft.next
        #puts "--Description Option 2: name_ft.next--"
        #MyMethods.display_element(name_ft.next,'color')
        description_ft = name_ft.next
      else
      end
      #Additional Location Information catch      
      
      if description_ft and description_ft.name == 'u'
        name << ": #{description_ft.children[0].to_s}"
        puts "Appended addional name information - #{name}"
        description_ft = description_ft.next if description_ft.next
      end

      description_ft = description_ft.children[0] if description_ft.children[0]
      
      description = ""
      until description_ft.to_s == "<br>" or description_ft.to_s.length < 1 do
        if description_ft.to_s.include? "<br>"
          description << description_ft.to_s.to(description_ft.to_s.index("<br>") - 1)
          break
        end
        description << description_ft.to_s #haunting.description
        description_ft = description_ft.next if description_ft
        puts description_ft.to_s
      end
      #puts description

      haunting = Haunting.new(name, location, description, state_name)
      state.hauntings << haunting
      puts "##{haunting_count} #{haunting.to_s}"
    else
      puts "Validation Failed - Previous Tag: #{location_ft.previous.to_s}"
    end
 

    
    
    haunting_count += 1
    #break if haunting_count >= 50
  end
  puts "||-- End #{state.name} -- Hauntings: #{state.hauntings.length} --||"
end


#Write Hauntings to SQLite Data store
State.states.each do |state|
  #state = State.states[0]
  puts "Storing #{state.hauntings.length} hauntingins from #{state.name} to SQLite"
  state.hauntings.each do |haunting|
  ScraperWiki::save_sqlite(haunting.unique_key, haunting.tuple)
    puts "Stored #{haunting.to_s}."
  end
end

State.states.each {|state| puts "Number of hauntings in #{state.name}: #{state.hauntings.length}"}
    

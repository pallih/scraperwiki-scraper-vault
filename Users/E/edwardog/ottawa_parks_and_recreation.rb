require "rubygems"
require "yaml"
require 'mechanize'

a = Mechanize.new { |agent|
  agent.user_agent_alias = 'Mac Safari'
}

complexes = {}

a.get('http://apps102.ottawa.ca/Start/StartSelectLanguage.asp?Referrer=http://apps102.ottawa.ca/Activities/ActivitiesCourseDetails.asp') do |language_page|
 a.click(language_page.link_with(:text => /Welcome/))

  a.get('http://apps102.ottawa.ca/Activities/ActivitiesAdvSearch.asp') do |page|
    page.search("select[@name='Complexes']").children.each do |complex|
      complexes[complex.text] = complex['value']
    end
    complexes.delete("(All)")
    
    complexes.keys.each do |name|
      ScraperWiki.save_sqlite(unique_keys=['complex'], data={'complex' => name})
    end
    
    complex = complexes[complexes.keys.first]
    
    search_form = page.form('Form_Search')
    search_form.field_with(:name => 'Complexes').options.detect {|o| o.value == complex }.select
    
    page = a.submit(form)
    
    puts page.content
  end
endrequire "rubygems"
require "yaml"
require 'mechanize'

a = Mechanize.new { |agent|
  agent.user_agent_alias = 'Mac Safari'
}

complexes = {}

a.get('http://apps102.ottawa.ca/Start/StartSelectLanguage.asp?Referrer=http://apps102.ottawa.ca/Activities/ActivitiesCourseDetails.asp') do |language_page|
 a.click(language_page.link_with(:text => /Welcome/))

  a.get('http://apps102.ottawa.ca/Activities/ActivitiesAdvSearch.asp') do |page|
    page.search("select[@name='Complexes']").children.each do |complex|
      complexes[complex.text] = complex['value']
    end
    complexes.delete("(All)")
    
    complexes.keys.each do |name|
      ScraperWiki.save_sqlite(unique_keys=['complex'], data={'complex' => name})
    end
    
    complex = complexes[complexes.keys.first]
    
    search_form = page.form('Form_Search')
    search_form.field_with(:name => 'Complexes').options.detect {|o| o.value == complex }.select
    
    page = a.submit(form)
    
    puts page.content
  end
end
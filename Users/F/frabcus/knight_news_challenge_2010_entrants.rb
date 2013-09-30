require 'nokogiri'
require 'uri'
require 'mechanize'

def go_to_entries(agent, base_url)
  agent.get(base_url)
  agent.page.link_with(:text => "Entries").click
end

def scrape_page(page, agent, base_url)
  puts "==================================="
  puts "Page " + page.to_s

  go_to_entries(agent, base_url)
  if page != 1 # is already clicked
    puts "not page 1"
    lnk = agent.page.link_with(:text => page.to_s)
    return false if !lnk
    lnk.click
  end
  html = agent.page.content
  puts html

  doc = Nokogiri::HTML(html)
  index_end = doc.search('.ItemContentContainer').size - 1
  
  for i in 0..index_end
    inner_agent = Mechanize.new
    go_to_entries(inner_agent, base_url)
    if page != 1 # is already clicked
      inner_agent.page.link_with(:text => page.to_s).click
    end
    c = doc.search('.ItemContentContainer')[i]

    puts "-------------------------------"
    data = {}
    data['title'] = c.search('a')[0].inner_html
    details_link_text = c.search('a')[0].inner_text
    details_link = c.search('a')[0]
    part_url = details_link['href']
    data['details_url'] = URI.join(base_url, part_url)
    data['user'] = c.search('a')[1].inner_html
    data['user_url'] = URI.join(base_url, c.search('a')[1]['href'])
    full_stars = c.css("img[src='App_Themes/Knight2010Proposals/images/star_sm_full.gif']").size
    half_stars = c.css("img[src='App_Themes/Knight2010Proposals/images/star_sm_half.gif']").size
    data['stars'] = full_stars.to_f + 0.5 * half_stars.to_f
    data['creation_date'] = Date.parse(c.search('.itemcreationdate')[0].inner_html)
    data['views'] = c.search('.viewcounter')[0].inner_html

    puts "details_link_text: " +  details_link_text
    puts "agent.page.content: " + inner_agent.page.content
    inner_agent.page.link_with(:text => details_link_text).click
    details_html = inner_agent.page.content
    puts details_html
    if details_html == ""
      # nothing comes out for some
      
      puts "XXX error, no content for this one"
    else
      puts "done details print"
      details_doc = Nokogiri::HTML(details_html)
      data['amount_requested'] = details_doc.search('.answer')[1].inner_html.gsub(/[$,]/, "").to_i
      data['expected_time'] = details_doc.search('.answer')[2].inner_html
      data['total_cost'] = details_doc.search('.answer')[3].inner_html.gsub(/[$,]/, "").to_i
    end

    puts data.to_json
    ScraperWiki.save(unique_keys=['details_url',], data=data)
  end

  return true
end

base_url = "http://generalprop.newschallenge.org/"
agent = Mechanize.new
page = 1
while scrape_page(page, agent, base_url):
  page = page + 1
end



require 'nokogiri'
require 'uri'
require 'mechanize'

def go_to_entries(agent, base_url)
  agent.get(base_url)
  agent.page.link_with(:text => "Entries").click
end

def scrape_page(page, agent, base_url)
  puts "==================================="
  puts "Page " + page.to_s

  go_to_entries(agent, base_url)
  if page != 1 # is already clicked
    puts "not page 1"
    lnk = agent.page.link_with(:text => page.to_s)
    return false if !lnk
    lnk.click
  end
  html = agent.page.content
  puts html

  doc = Nokogiri::HTML(html)
  index_end = doc.search('.ItemContentContainer').size - 1
  
  for i in 0..index_end
    inner_agent = Mechanize.new
    go_to_entries(inner_agent, base_url)
    if page != 1 # is already clicked
      inner_agent.page.link_with(:text => page.to_s).click
    end
    c = doc.search('.ItemContentContainer')[i]

    puts "-------------------------------"
    data = {}
    data['title'] = c.search('a')[0].inner_html
    details_link_text = c.search('a')[0].inner_text
    details_link = c.search('a')[0]
    part_url = details_link['href']
    data['details_url'] = URI.join(base_url, part_url)
    data['user'] = c.search('a')[1].inner_html
    data['user_url'] = URI.join(base_url, c.search('a')[1]['href'])
    full_stars = c.css("img[src='App_Themes/Knight2010Proposals/images/star_sm_full.gif']").size
    half_stars = c.css("img[src='App_Themes/Knight2010Proposals/images/star_sm_half.gif']").size
    data['stars'] = full_stars.to_f + 0.5 * half_stars.to_f
    data['creation_date'] = Date.parse(c.search('.itemcreationdate')[0].inner_html)
    data['views'] = c.search('.viewcounter')[0].inner_html

    puts "details_link_text: " +  details_link_text
    puts "agent.page.content: " + inner_agent.page.content
    inner_agent.page.link_with(:text => details_link_text).click
    details_html = inner_agent.page.content
    puts details_html
    if details_html == ""
      # nothing comes out for some
      
      puts "XXX error, no content for this one"
    else
      puts "done details print"
      details_doc = Nokogiri::HTML(details_html)
      data['amount_requested'] = details_doc.search('.answer')[1].inner_html.gsub(/[$,]/, "").to_i
      data['expected_time'] = details_doc.search('.answer')[2].inner_html
      data['total_cost'] = details_doc.search('.answer')[3].inner_html.gsub(/[$,]/, "").to_i
    end

    puts data.to_json
    ScraperWiki.save(unique_keys=['details_url',], data=data)
  end

  return true
end

base_url = "http://generalprop.newschallenge.org/"
agent = Mechanize.new
page = 1
while scrape_page(page, agent, base_url):
  page = page + 1
end




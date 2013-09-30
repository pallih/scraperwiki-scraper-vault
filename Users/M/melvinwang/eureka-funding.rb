# require 'rubygems'
# require 'mechanize'
require 'nokogiri'

# agent = Mechanize.new

# assume fewer than 10000 projects? easy to change
# 310-2381 ok
(2587..9999).each do |n|
  puts "Working on #{n}"
  url = "http://www.eurekanetwork.org/project/-/id/#{n}"
  # page = agent.get(url)
  page = Nokogiri::HTML(ScraperWiki.scrape(url))

  contents = page.search('div#mainContent div.portlet-content-container')[0]

  # puts "next" if contents.content.include? "This is the default error page"
  next if contents.content.include? "This is the default error page"

  summary = contents.search('div#sum')[0]
  outline = contents.search('div#outline')[0]

  next unless contents && summary && outline
  
  result = {}
  
  # parse summary
  result['title'] = summary.search("h2")[0].content.strip
  result['abstract'] = summary.search('h3')[0].content.strip
  summary_td0 = summary.search("table td")[0]
  summary_td0.search("span.highlight_green").each do |s|
    key = s.content.sub(">","").strip
    result[key] = s.next.type == 'br' ? "" : s.next.content.strip
  end
  
  summary_td1 = summary.search("table td")[1]
  
  summary_td1_p0 = summary_td1.search("p")[0]
  main_contact_name = summary_td1_p0.search("strong")[0]
  result['Main contact'] = main_contact_name.content.strip
  main_contact_name.unlink
  result['Main contact information'] = summary_td1_p0.content.strip
  
  summary_td1_p1 = summary_td1.search("p")[1]
  main_contact_person = summary_td1_p1.search("strong")[0]
  result['Main contact person'] = main_contact_person.content.strip
  main_contact_person.unlink
  result['Main contact title'] = summary_td1_p1.content.sub(">","").strip
  
  summary_td1_p2 = summary_td1.search("p")[2]
  summary_td1_p2.search("span.highlight_green")[0].unlink
  result['Organization type'] = summary_td1_p2.content.sub(">","").strip

  # parse outline
  outline.search("h2").each do |h2|
    key = h2.content.strip
    result[key] = h2.next_element.content.strip
  end
  # parse participants
  # there could be many participants, surely less than 50?
  (1..50).each do |p|
    participant_td = contents.search("div#part#{p} table td")[0]
    next unless participant_td

    p0 = participant_td.search("p")[0]
    if p0
      contact_name = p0.search("strong")[0]
      if contact_name
        result["Participant #{p}"] = contact_name.content.strip
        contact_name.unlink
      end
      result["Participant #{p} contact information"] = p0.content.strip
    end

    p1 = participant_td.search("p")[1]
    if p1
      contact_person = p1.search("strong")[0]
      if contact_person
        result["Participant #{p} contact person"] = contact_person.content.strip
        contact_person.unlink
      end
      result["Participant #{p} contact title"] = p1.content.sub(">","").strip
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                end

    p2 = participant_td.search("p")[2]
    if p2
      p2.search("span.highlight_green")[0].unlink
      result["Participant #{p} organization type"] = p2.content.sub(">","").strip
        end

    participant_p0 = contents.search("div#part#{p} > p")[0]
    result["Participant #{p} expertise"] = participant_p0.content.strip if participant_p0
    participant_p1 = contents.search("div#part#{p} > p")[1]
    result["Participant #{p} contribution to project"] = participant_p1.content.strip if participant_p1
  end
  
  # parse other stuff? acronym, number
  result['acronym'] = contents.search("//meta[@name='acronym']")[0]['content'].strip
  result['id'] = n
  result['url'] = url
  
  # result.each_pair do |k,v|
    # puts "#{k} |||||| #{v}"
  # end

  final_result = {}
  result.each_pair do |k,v|
    new_k = k.gsub(/\s+/, "_")
    final_result[new_k] = v
  end

  # puts result.keys
  # puts result

  ScraperWiki.save(final_result.keys, final_result)
end
# require 'rubygems'
# require 'mechanize'
require 'nokogiri'

# agent = Mechanize.new

# assume fewer than 10000 projects? easy to change
# 310-2381 ok
(2587..9999).each do |n|
  puts "Working on #{n}"
  url = "http://www.eurekanetwork.org/project/-/id/#{n}"
  # page = agent.get(url)
  page = Nokogiri::HTML(ScraperWiki.scrape(url))

  contents = page.search('div#mainContent div.portlet-content-container')[0]

  # puts "next" if contents.content.include? "This is the default error page"
  next if contents.content.include? "This is the default error page"

  summary = contents.search('div#sum')[0]
  outline = contents.search('div#outline')[0]

  next unless contents && summary && outline
  
  result = {}
  
  # parse summary
  result['title'] = summary.search("h2")[0].content.strip
  result['abstract'] = summary.search('h3')[0].content.strip
  summary_td0 = summary.search("table td")[0]
  summary_td0.search("span.highlight_green").each do |s|
    key = s.content.sub(">","").strip
    result[key] = s.next.type == 'br' ? "" : s.next.content.strip
  end
  
  summary_td1 = summary.search("table td")[1]
  
  summary_td1_p0 = summary_td1.search("p")[0]
  main_contact_name = summary_td1_p0.search("strong")[0]
  result['Main contact'] = main_contact_name.content.strip
  main_contact_name.unlink
  result['Main contact information'] = summary_td1_p0.content.strip
  
  summary_td1_p1 = summary_td1.search("p")[1]
  main_contact_person = summary_td1_p1.search("strong")[0]
  result['Main contact person'] = main_contact_person.content.strip
  main_contact_person.unlink
  result['Main contact title'] = summary_td1_p1.content.sub(">","").strip
  
  summary_td1_p2 = summary_td1.search("p")[2]
  summary_td1_p2.search("span.highlight_green")[0].unlink
  result['Organization type'] = summary_td1_p2.content.sub(">","").strip

  # parse outline
  outline.search("h2").each do |h2|
    key = h2.content.strip
    result[key] = h2.next_element.content.strip
  end
  # parse participants
  # there could be many participants, surely less than 50?
  (1..50).each do |p|
    participant_td = contents.search("div#part#{p} table td")[0]
    next unless participant_td

    p0 = participant_td.search("p")[0]
    if p0
      contact_name = p0.search("strong")[0]
      if contact_name
        result["Participant #{p}"] = contact_name.content.strip
        contact_name.unlink
      end
      result["Participant #{p} contact information"] = p0.content.strip
    end

    p1 = participant_td.search("p")[1]
    if p1
      contact_person = p1.search("strong")[0]
      if contact_person
        result["Participant #{p} contact person"] = contact_person.content.strip
        contact_person.unlink
      end
      result["Participant #{p} contact title"] = p1.content.sub(">","").strip
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                end

    p2 = participant_td.search("p")[2]
    if p2
      p2.search("span.highlight_green")[0].unlink
      result["Participant #{p} organization type"] = p2.content.sub(">","").strip
        end

    participant_p0 = contents.search("div#part#{p} > p")[0]
    result["Participant #{p} expertise"] = participant_p0.content.strip if participant_p0
    participant_p1 = contents.search("div#part#{p} > p")[1]
    result["Participant #{p} contribution to project"] = participant_p1.content.strip if participant_p1
  end
  
  # parse other stuff? acronym, number
  result['acronym'] = contents.search("//meta[@name='acronym']")[0]['content'].strip
  result['id'] = n
  result['url'] = url
  
  # result.each_pair do |k,v|
    # puts "#{k} |||||| #{v}"
  # end

  final_result = {}
  result.each_pair do |k,v|
    new_k = k.gsub(/\s+/, "_")
    final_result[new_k] = v
  end

  # puts result.keys
  # puts result

  ScraperWiki.save(final_result.keys, final_result)
end

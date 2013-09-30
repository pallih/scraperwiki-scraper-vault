require 'rss/2.0'
require 'mechanize'
require 'date'

# Just get rid of the status_id param if you want it all, baby
applications_on_exhibition_url = 'http://majorprojects.planning.nsw.gov.au/index.pl?action=search&status_id=6&rss=1'

feed = RSS::Parser.parse applications_on_exhibition_url
agent = Mechanize.new

def get_value_from_td_label(label, label_tds)
  label_cell = label_tds.detect { |e| e.inner_text.strip == label }
  label_cell.next.next.inner_text.strip if label_cell
end

feed.channel.items.each do |item|
  application = agent.get item.link

  title = application.at('.vpa_header').at(:h2).inner_text
  application_description = application.at('.description').inner_text.split('Other assessments against this site')[0].strip
  description = application_description.empty? ? title : "#{title} - #{application_description}"

  label_tds = application.search('.label_td')

  on_notice_from_text = get_value_from_td_label('Exhibition Start', label_tds)
  on_notice_to_text = get_value_from_td_label('Exhibition End', label_tds)

  record = {
    :description       => description,
    :address           => get_value_from_td_label('Location', label_tds),
    :council_reference => get_value_from_td_label('Application Number', label_tds),
    :on_notice_from    => (Date.strptime(on_notice_from_text, '%d/%m/%Y') if on_notice_from_text),
    :on_notice_to      => (Date.strptime(on_notice_to_text, '%d/%m/%Y') if on_notice_to_text),
    :info_url          => item.link,
    :comment_url       => item.link,
    :date_scraped      => Date.today.to_s
  }

  # Skip saving when there is no council_reference or no address
  if record[:council_reference] && record[:address]
    if ScraperWiki.select("* from swdata where `council_reference`='#{record[:council_reference]}'").empty? 
      ScraperWiki.save_sqlite([:council_reference], record)
    else
      puts "Skipping already saved record " + record[:council_reference]
    end
  else
    puts "Skipping application due to missing council_reference or address at #{item.link}"
  end
end

require 'rss/2.0'
require 'mechanize'
require 'date'

# Just get rid of the status_id param if you want it all, baby
applications_on_exhibition_url = 'http://majorprojects.planning.nsw.gov.au/index.pl?action=search&status_id=6&rss=1'

feed = RSS::Parser.parse applications_on_exhibition_url
agent = Mechanize.new

def get_value_from_td_label(label, label_tds)
  label_cell = label_tds.detect { |e| e.inner_text.strip == label }
  label_cell.next.next.inner_text.strip if label_cell
end

feed.channel.items.each do |item|
  application = agent.get item.link

  title = application.at('.vpa_header').at(:h2).inner_text
  application_description = application.at('.description').inner_text.split('Other assessments against this site')[0].strip
  description = application_description.empty? ? title : "#{title} - #{application_description}"

  label_tds = application.search('.label_td')

  on_notice_from_text = get_value_from_td_label('Exhibition Start', label_tds)
  on_notice_to_text = get_value_from_td_label('Exhibition End', label_tds)

  record = {
    :description       => description,
    :address           => get_value_from_td_label('Location', label_tds),
    :council_reference => get_value_from_td_label('Application Number', label_tds),
    :on_notice_from    => (Date.strptime(on_notice_from_text, '%d/%m/%Y') if on_notice_from_text),
    :on_notice_to      => (Date.strptime(on_notice_to_text, '%d/%m/%Y') if on_notice_to_text),
    :info_url          => item.link,
    :comment_url       => item.link,
    :date_scraped      => Date.today.to_s
  }

  # Skip saving when there is no council_reference or no address
  if record[:council_reference] && record[:address]
    if ScraperWiki.select("* from swdata where `council_reference`='#{record[:council_reference]}'").empty? 
      ScraperWiki.save_sqlite([:council_reference], record)
    else
      puts "Skipping already saved record " + record[:council_reference]
    end
  else
    puts "Skipping application due to missing council_reference or address at #{item.link}"
  end
end

require 'rss/2.0'
require 'mechanize'
require 'date'

# Just get rid of the status_id param if you want it all, baby
applications_on_exhibition_url = 'http://majorprojects.planning.nsw.gov.au/index.pl?action=search&status_id=6&rss=1'

feed = RSS::Parser.parse applications_on_exhibition_url
agent = Mechanize.new

def get_value_from_td_label(label, label_tds)
  label_cell = label_tds.detect { |e| e.inner_text.strip == label }
  label_cell.next.next.inner_text.strip if label_cell
end

feed.channel.items.each do |item|
  application = agent.get item.link

  title = application.at('.vpa_header').at(:h2).inner_text
  application_description = application.at('.description').inner_text.split('Other assessments against this site')[0].strip
  description = application_description.empty? ? title : "#{title} - #{application_description}"

  label_tds = application.search('.label_td')

  on_notice_from_text = get_value_from_td_label('Exhibition Start', label_tds)
  on_notice_to_text = get_value_from_td_label('Exhibition End', label_tds)

  record = {
    :description       => description,
    :address           => get_value_from_td_label('Location', label_tds),
    :council_reference => get_value_from_td_label('Application Number', label_tds),
    :on_notice_from    => (Date.strptime(on_notice_from_text, '%d/%m/%Y') if on_notice_from_text),
    :on_notice_to      => (Date.strptime(on_notice_to_text, '%d/%m/%Y') if on_notice_to_text),
    :info_url          => item.link,
    :comment_url       => item.link,
    :date_scraped      => Date.today.to_s
  }

  # Skip saving when there is no council_reference or no address
  if record[:council_reference] && record[:address]
    if ScraperWiki.select("* from swdata where `council_reference`='#{record[:council_reference]}'").empty? 
      ScraperWiki.save_sqlite([:council_reference], record)
    else
      puts "Skipping already saved record " + record[:council_reference]
    end
  else
    puts "Skipping application due to missing council_reference or address at #{item.link}"
  end
end

require 'rss/2.0'
require 'mechanize'
require 'date'

# Just get rid of the status_id param if you want it all, baby
applications_on_exhibition_url = 'http://majorprojects.planning.nsw.gov.au/index.pl?action=search&status_id=6&rss=1'

feed = RSS::Parser.parse applications_on_exhibition_url
agent = Mechanize.new

def get_value_from_td_label(label, label_tds)
  label_cell = label_tds.detect { |e| e.inner_text.strip == label }
  label_cell.next.next.inner_text.strip if label_cell
end

feed.channel.items.each do |item|
  application = agent.get item.link

  title = application.at('.vpa_header').at(:h2).inner_text
  application_description = application.at('.description').inner_text.split('Other assessments against this site')[0].strip
  description = application_description.empty? ? title : "#{title} - #{application_description}"

  label_tds = application.search('.label_td')

  on_notice_from_text = get_value_from_td_label('Exhibition Start', label_tds)
  on_notice_to_text = get_value_from_td_label('Exhibition End', label_tds)

  record = {
    :description       => description,
    :address           => get_value_from_td_label('Location', label_tds),
    :council_reference => get_value_from_td_label('Application Number', label_tds),
    :on_notice_from    => (Date.strptime(on_notice_from_text, '%d/%m/%Y') if on_notice_from_text),
    :on_notice_to      => (Date.strptime(on_notice_to_text, '%d/%m/%Y') if on_notice_to_text),
    :info_url          => item.link,
    :comment_url       => item.link,
    :date_scraped      => Date.today.to_s
  }

  # Skip saving when there is no council_reference or no address
  if record[:council_reference] && record[:address]
    if ScraperWiki.select("* from swdata where `council_reference`='#{record[:council_reference]}'").empty? 
      ScraperWiki.save_sqlite([:council_reference], record)
    else
      puts "Skipping already saved record " + record[:council_reference]
    end
  else
    puts "Skipping application due to missing council_reference or address at #{item.link}"
  end
end


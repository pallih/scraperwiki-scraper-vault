require 'json'
require 'open-uri'

base_url = 'http://www.planningalerts.org.au/comments.js'

# HACK: Hard coding page numbers for the moment, needs to detect new
# applications for this to continue to work
(1..6).each do |page|
  comments = JSON.parse open("#{base_url}?page=#{page}").read

  comments.each do |comment|
    record = comment['comment'].delete 'application'
    record['application_id'] = record.delete 'id'
    record.merge! comment['comment']
    record['url'] = "http://www.planningalerts.org.au/applications/#{record['application_id']}"
    ScraperWiki::save_sqlite ['id'], record
  end
end
require 'json'
require 'open-uri'

base_url = 'http://www.planningalerts.org.au/comments.js'

# HACK: Hard coding page numbers for the moment, needs to detect new
# applications for this to continue to work
(1..6).each do |page|
  comments = JSON.parse open("#{base_url}?page=#{page}").read

  comments.each do |comment|
    record = comment['comment'].delete 'application'
    record['application_id'] = record.delete 'id'
    record.merge! comment['comment']
    record['url'] = "http://www.planningalerts.org.au/applications/#{record['application_id']}"
    ScraperWiki::save_sqlite ['id'], record
  end
end

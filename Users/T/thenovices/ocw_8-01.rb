# Blank Ruby

require 'mechanize'
require 'nokogiri'

BASE_URL = "http://ocw.mit.edu"
MODULES_URL = BASE_URL + "/courses/physics/8-01sc-physics-i-classical-mechanics-fall-2010/modules-overview/"

agent = Mechanize.new
modules = agent.get(MODULES_URL).search("div#scholar_container p a")
modules.each do |m|
  # Get the id and name for the module
  dot = m.text.index('.')
  id = m.text[3...dot]
  name = m.text[(dot+2)..-1]

  puts "#{id}: #{name}"

  agent.get(BASE_URL + m["href"])

  html = Nokogiri::HTML(agent.page.body)
  objectives = html.css(".open li")
  notes = html.at_css(".toggle_container a")
  clips = html.css(".mediatext:nth-child(2) p:nth-child(2) a:nth-child(1)")
  transcripts = html.css(".mediatext:nth-child(2) a:nth-child(3)")
  help_clips = html.css('.toggle_container:nth-child(8) script')

  clips.size.times do |i|
    clip, transcript = clips[i], transcripts[i]
    clip_id = "#{id}_#{i+1}"
    clip_name = clip.text.strip
    transcript_url = BASE_URL + transcript["href"]

    params = clip["onclick"].strip.match(/\((.*)\)/)[1].split(',')
    yt_id = params[0].strip[1..-2].match(/\/v\/(.*)\Z/)[1]
    start = params[4].to_i
    stop = params[5].to_i

    clip_data = {
      "clip_id" => clip_id,
      "module_id" => id,
      "clip_name" => clip_name,
      "transcript_url" => transcript_url,
      "youtube_id" => yt_id,
      "start" => start,
      "stop" => stop
    }
    p clip_data
    ScraperWiki.save(unique_keys=['clip_id'], data=clip_data, table_name="clips")
  end

  help_clips.size.times do |i|
    clip_id = "#{id}_#{i+1}help"
    clip_name = "Help Session #{i+1} for module #{id}"
    params = help_clips[i].text.match(/\((.*)\)/)[1].split(',')
    yt_id = params[1].strip[1..-2].match(/\/v\/(.*)\Z/)[1]

    help_clip_data = {
      "clip_id" => clip_id,
      "module_id" => id,
      "clip_name" => clip_name,
      "youtube_id" => yt_id,
    }
    p help_clip_data
    ScraperWiki.save(unique_keys=['clip_id'], data=help_clip_data, table_name="help_clips")
  end

  objectives = objectives.map{ |o| %W/"#{o.text}"/}.join(",") # Store as CSV
  notes_title = notes.text.strip
  notes_url = BASE_URL + notes["href"]

  module_data = {
    "id" => id,
    "name" => name,
    "objectives" => objectives,
    "notes_title" => notes_title,
    "notes_url" => notes_url
  }
  p module_data
  ScraperWiki.save(unique_keys=['id'], data=module_data, table_name="modules")
end
# Blank Ruby

require 'mechanize'
require 'nokogiri'

BASE_URL = "http://ocw.mit.edu"
MODULES_URL = BASE_URL + "/courses/physics/8-01sc-physics-i-classical-mechanics-fall-2010/modules-overview/"

agent = Mechanize.new
modules = agent.get(MODULES_URL).search("div#scholar_container p a")
modules.each do |m|
  # Get the id and name for the module
  dot = m.text.index('.')
  id = m.text[3...dot]
  name = m.text[(dot+2)..-1]

  puts "#{id}: #{name}"

  agent.get(BASE_URL + m["href"])

  html = Nokogiri::HTML(agent.page.body)
  objectives = html.css(".open li")
  notes = html.at_css(".toggle_container a")
  clips = html.css(".mediatext:nth-child(2) p:nth-child(2) a:nth-child(1)")
  transcripts = html.css(".mediatext:nth-child(2) a:nth-child(3)")
  help_clips = html.css('.toggle_container:nth-child(8) script')

  clips.size.times do |i|
    clip, transcript = clips[i], transcripts[i]
    clip_id = "#{id}_#{i+1}"
    clip_name = clip.text.strip
    transcript_url = BASE_URL + transcript["href"]

    params = clip["onclick"].strip.match(/\((.*)\)/)[1].split(',')
    yt_id = params[0].strip[1..-2].match(/\/v\/(.*)\Z/)[1]
    start = params[4].to_i
    stop = params[5].to_i

    clip_data = {
      "clip_id" => clip_id,
      "module_id" => id,
      "clip_name" => clip_name,
      "transcript_url" => transcript_url,
      "youtube_id" => yt_id,
      "start" => start,
      "stop" => stop
    }
    p clip_data
    ScraperWiki.save(unique_keys=['clip_id'], data=clip_data, table_name="clips")
  end

  help_clips.size.times do |i|
    clip_id = "#{id}_#{i+1}help"
    clip_name = "Help Session #{i+1} for module #{id}"
    params = help_clips[i].text.match(/\((.*)\)/)[1].split(',')
    yt_id = params[1].strip[1..-2].match(/\/v\/(.*)\Z/)[1]

    help_clip_data = {
      "clip_id" => clip_id,
      "module_id" => id,
      "clip_name" => clip_name,
      "youtube_id" => yt_id,
    }
    p help_clip_data
    ScraperWiki.save(unique_keys=['clip_id'], data=help_clip_data, table_name="help_clips")
  end

  objectives = objectives.map{ |o| %W/"#{o.text}"/}.join(",") # Store as CSV
  notes_title = notes.text.strip
  notes_url = BASE_URL + notes["href"]

  module_data = {
    "id" => id,
    "name" => name,
    "objectives" => objectives,
    "notes_title" => notes_title,
    "notes_url" => notes_url
  }
  p module_data
  ScraperWiki.save(unique_keys=['id'], data=module_data, table_name="modules")
end

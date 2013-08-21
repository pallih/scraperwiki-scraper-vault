require 'nokogiri'
require 'open-uri'

# parse main page to get array of page links

doc = ScraperWiki.scrape('http://gelconference.com/videos/')

targetList = Nokogiri::HTML.parse(doc).css('dt a').collect do |target|
  targetList = target['href']
end

# for each link, open url and store info

targetList.each do |targetUrl|
  targetDoc = Nokogiri::HTML(open(targetUrl))
  targetData = targetDoc.css('#video_holder').collect do |targetContent|
    record = {}
    record['talkUrl']          = targetUrl
    record['talkTitle']        = targetContent.css('h1').inner_text
    record['talkVimeo']        = targetContent.css('object').inner_html.split('clip_id=')[1].split('&')[0]
    record['talkDescription']  = targetContent.css('.description').inner_html.strip
    record['talkPosted']       = targetContent.css('#video_meta .dates').inner_text.split(': ')[1].split('Recorded')[0].strip
    record['talkEvent']        = targetContent.css('#video_meta .dates a').inner_text
    record['talkTags']         = targetContent.css('#video_meta .tags').inner_text.split('Tags:')[1].gsub(/\s+/, '').sub(',', ', ')

    # Print out the data we've gathered
    p record

    # Finally, save the record to the datastore - 'talkVimeo' is our unique key
    ScraperWiki.save(['talkVimeo'], record)
  end
end


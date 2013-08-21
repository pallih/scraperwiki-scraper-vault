require 'nokogiri'

podcast_urls = ['http://www.npr.org/blogs/money']

def get_podcasts(page, podcast)
  page.css('.blogpost').each do |blogpost|
    has_audio = blogpost.css('a.download').length > 0
    if has_audio
      title = blogpost.css('.storytitle h1 a').text
      mp3 = blogpost.css('a.download').attr('href').text
      date = blogpost.css('.datestamp').text
      ScraperWiki.save(unique_keys=['mp3',], data={'podcast' => podcast, 'title' => title, 'mp3' => mp3, 'date' => date})
    end
  end
end

def get_next_page(page, first_page)
  if first_page
    next_link = page.css('.blognavindex .next')
  else
    next_link = page.css('.archivenav .prev')
  end
  next_link.length > 0 ? next_link.attr('href').text : false
end

podcast_urls.each do |podcast|
  page = Nokogiri::HTML.parse(ScraperWiki.scrape(podcast))
  get_podcasts(page, podcast)
  first_page = true
  while next_page = get_next_page(page, first_page) do
    first_page = false
    break unless next_page
    next_page = 'http://www.npr.org' + next_page
    p next_page
    page = Nokogiri::HTML.parse(ScraperWiki.scrape(next_page))
    get_podcasts(page, podcast)
  end
end
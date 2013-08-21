require 'mechanize'

@agent = Mechanize.new

# Takes a string and returns an absolute URL when url might be relative to source_url
def absolute_url(url, source_url)
  url = URI.parse url
  url.absolute? ? url : URI.parse(source_url).merge(url)
end

def park_urls
  url = 'http://www.nretas.nt.gov.au/national-parks-and-reserves/parks/find/completelisting'

  page = @agent.get url

  page.search('#content ul').search('a').map do |a|
    absolute_url a.attr('href'), url
  end
end

pp park_urls


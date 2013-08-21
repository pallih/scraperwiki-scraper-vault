require 'nokogiri'
require 'open-uri'

def doc uri
  html = open(uri).read
  doc = Nokogiri::HTML(html)
  [doc, html]
end

def each_in_sitemap uri, filter=nil
  doc(uri)[0].search('loc').each do |loc|
    url = loc.inner_text
    yield url if !filter || url[filter]
    nil
  end
end

def each_organisation_page
  index_uri = 'http://influenceexplorer.com/sitemap.xml'
  each_in_sitemap(index_uri, /organization/) do |sitemap_uri|
    each_in_sitemap(sitemap_uri) do |uri|
      yield uri
      nil
    end
    nil
  end
end

def wikipedia_uri html
  (html[/(http:\/\/en.wikipedia.org\/wiki\/[^"]+)"/] ?  $1 : nil)
end

def inner_text node
  node.inner_text.gsub("\n",' ').gsub("\t",' ').squeeze(' ').strip
end

def lobbying_title_and_amount doc
  if lobbying_heading = doc.search('h3').detect {|h3| h3.inner_text[/Lobbying/]}
    #title = inner_text(lobbying_heading)
    #title[/(\d\d\d\d)[^\d]+(\d\d\d\d)/]
    start_year = 0 # $1
    end_year = 0 # $2
    amount = inner_text(lobbying_heading.parent.at('span.amount'))

    if amount[/\$([\d,]+)\s(\w+)/]
      { "$ #{$2} Lobbying" => $1, "Lobbying period" => "#{start_year}-#{end_year}" }
    else
      {}
    end
  else
    {}
  end
end

DO_THESE = ["http://influenceexplorer.com/organization/force-protection-industries/"]

def data_from uri
  id_uri = uri.sub(/\/[^\/]+$/, '/' )
  if !DO_THESE.include? id_uri
  doc, html = doc(uri)
  {
    'Name' => inner_text(doc.at('h2')),
    'Influence Explorer URI' => uri.sub(/\/[^\/]+$/, '/' ),
    'Influence Explorer URL' => uri,
    'Wikipedia URI' => wikipedia_uri(html)
  }.merge(
     lobbying_title_and_amount(doc)
  )
  else
    nil
  end
end

def have_record? uri
  record = ScraperWiki.select('* from swdata where "Influence Explorer URL" = "' + uri + '" limit 1')
  record.size == 1
end

each_organisation_page do |uri|
  begin
    if have_record? uri
      print '.'
    else
      record = data_from(uri)
      if record
      print uri
      $stdout.flush
      ScraperWiki.save(['Influence Explorer URI'], record) 
      else
      print '-'
      end
    end
  rescue Exception => e
    puts e.to_s + e.backtrace.join("\n")
  end
  nil
end

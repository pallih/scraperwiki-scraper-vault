require 'nokogiri'
require 'uri'

def get_description doc
  if doc && (abstract = doc.at('div[@property="dc:abstract"]'))
    abstract.inner_html
  else
    ''
  end
end

def doc_format uri
  case uri
    when /pdf$/i
      'PDF'
    when /rft$/i
      'RFT'
    when /doc$/i
      'DOC'
    when /xls$/i
      'XLS'
    when /ppt$/i
      'PPT'
    else
      ''
  end
end

def doc_size title
  if title.strip[/\((.+)\)$/]
    title.sub!( /\((.+)\)$/, '' )
    title.strip!
    $1
  else
    ''
  end
end

def get_documents base_uri, doc
  if doc && (ul = doc.at('ul#documents'))
    ul.search('a').collect do |a|
      uri = URI.parse(base_uri).merge(a['href']).to_s
      title = a.inner_text
      format = doc_format(uri)
      size = doc_size(title)

      record = {
        'consultation' => base_uri,
        'title' => title,
        'URI' => uri,
        'format' => format,
        'size' => size
      }
      ScraperWiki.save_sqlite(['URI'], record, 'documents')
      [title, uri, format, size]
    end
  else
    []
  end
end

def add_consultation title, uri, start_date, end_date, base_uri
  puts uri
  doc = nil
  published_date = ''

  html = ScraperWiki.scrape(uri)
  doc = Nokogiri::HTML(html.gsub('&nbsp;',' '))

  description = get_description doc
  documents = get_documents uri, doc

  record = {
    'department' => '',
    'title' => title,
    'published_date' => published_date,
    'start_date' => start_date,
    'end_date' => end_date,
    'URI' => uri,
    'description' => description,
    'sponsor' => '',
    'agency' => 'Intellectual Property Office',
    'documents' => [documents, documents.size].inspect
  }
  ScraperWiki.save_sqlite(['URI'], record, 'consultations')

end

def handle_link a, base_uri
  row = a.parent.parent
  cells = row.search('td')
  start_date = cells[3].inner_text
  end_date = cells[4].inner_text
  uri = base_uri.merge(a['href']).to_s
  title = a.inner_text
  add_consultation title, uri, start_date, end_date, base_uri
end


uri = 'http://www.ipo.gov.uk/pro-policy/consult/consult-live.htm'
base_uri = URI.parse(uri)

html = ScraperWiki.scrape uri
doc = Nokogiri::HTML html

doc.search('#content td a').each do |a|
  handle_link(a, base_uri) if a['href']
end
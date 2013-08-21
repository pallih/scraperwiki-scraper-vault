require 'nokogiri'
require 'uri'

def clean text
  text.gsub!("\342\200\231", "'")
  text.gsub!("\342\200\176", "'")
  text.gsub!("\342\200\177", "'")
  text.gsub!("\342\200\230", "'")
  text.gsub!("\342\200\231", "'")
  text.gsub!("\342\200\232", ',')
  text.gsub!("\342\200\233", "'")
  text.gsub!("\342\200\234", '"')
  text.gsub!("\342\200\235", '"')
  text.gsub!("\342\200\041", '-')
  text.gsub!("\342\200\174", '-')
  text.gsub!("\342\200\220", '-')
  text.gsub!("\342\200\223", '-')
  text.gsub!("\342\200\224", '--')
  text.gsub!("\342\200\225", '--')
  text.gsub!("\342\200\042", '--')
  text.gsub!("\342\200\246", '...')
  text
end

def date_from text
  if text.sub('Extended to ','').strip[/(\d\d)\/(\d\d)\/(\d\d)$/]
    "20#{$3}-#{$2}-#{$1}"
  else
    ''
  end
end

def blank? node
  node.inner_text.strip.size == 0
end

def get_description doc
  description = if abstract = doc.at('div[@property="dc:abstract"]')
    if blank?(abstract)
      paragraph = abstract.next
      while paragraph && (blank?(paragraph) || paragraph.name == 'h2')
        paragraph = paragraph.next
      end
      paragraph.to_s
    else
      abstract.inner_html
    end
  else
    if h1 = doc.at('#primaryContentFull > h1')
      paragraph = h1.next
      while paragraph && (blank?(paragraph) || paragraph.inner_text.strip.squeeze(' ')[/^(.+date:?\s+)?\d\d.+\d\d\d\d$/] || paragraph.inner_text.strip[/^Closing date/])
        paragraph = paragraph.next
      end
      paragraph.to_s
    else
      ''
    end
  end
  
  description.gsub(/<p>\s+/,'<p>').gsub(/\s+<\/p>/,'</p>')
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
  if title[/\(.+\s(.+)\)$/]
    title.sub!( /\(.+\s(.+)\)$/, '' )
    title.strip!
    $1
  else
    ''
  end
end

def doc_info a, base_uri
  title = clean(a.inner_text)
  uri = URI.parse(base_uri).merge(a['href']).to_s
  format = doc_format uri

  size = doc_size title
  size = '' if size == 'window'

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

def get_documents doc, base_uri
  documents = doc.search('#primaryContentFull a').select do |a|
    uri = a['href']
    uri && !uri[/a(d|b)obe.com/] && !uri[/mailto/] && !uri[/^#/] && !a.inner_text[/accessibility\spage/]
  end
  documents.map {|a| doc_info a, base_uri }
end

def get_date type, doc, default
  if date = doc.at(%Q|span[@property="dc:#{type}"]|)
    date['content']
  else
    default
  end
end

def add_consultation title, uri, start_date, end_date, base_uri
  puts uri
  if html = ScraperWiki.scrape(uri)
    doc = Nokogiri::HTML(html.gsub('&nbsp;',' '))
    
    published_date = ''
    if doc.at('h1[@property="dc:title"]')
      title = doc.at('h1[@property="dc:title"]').inner_text
      published_date = get_date('issued', doc, published_date)
      start_date = get_date('available', doc, start_date)
      end_date = get_date('valid', doc, end_date)
    end

    description = get_description doc
    documents = get_documents doc, uri
  
    record = {
      'department' => 'HM Treasury',
      'title' => clean(title),
      'published_date' => published_date,
      'start_date' => start_date,
      'end_date' => end_date,
      'URI' => uri,
      'description' => description,
      'sponsor' => '',
      'agency' => '',
      'documents' => [documents, documents.size].inspect
    }
    ScraperWiki.save_sqlite(['URI'], record, 'consultations')
  end
end

def handle_link a, base_uri
  title = a.inner_text
  uri = base_uri.merge(a['href']).to_s
  label = a.next
  label = label.next if (label && label.name == 'br')

  if label && label.name == 'text' && label.inner_text.strip.squeeze(' ')[/Launch date:? (.+) Closing date:? (.+)/]
    start_date = date_from $1
    end_date = date_from $2
    add_consultation title, uri, start_date, end_date, base_uri
  elsif uri[/consult_/] && !uri[/consult_fullindex/] && ![/nationalarchives/]
    add_consultation title, uri, nil, nil, base_uri 
  end
end

uri = 'http://www.hm-treasury.gov.uk/consult_fullindex.htm'
base_uri = URI.parse(uri)

html = ScraperWiki.scrape(uri).gsub('&nbsp;',' ')
doc = Nokogiri::HTML html

doc.at('#primaryContent').search('a').each do |a|
  handle_link a, base_uri
end
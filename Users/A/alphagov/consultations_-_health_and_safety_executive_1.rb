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

def blank? node
  node.inner_text.strip.size == 0
end

def title_from doc
  if doc && ( (title = doc.at('span[@property="dc:title"]')) || (title = doc.at('h1[@property="dc:title"]')) )
    title
  else
    nil
  end
end

def get_description doc
  if doc && (abstract = doc.at('p[@property="dc:abstract"]'))
    abstract.inner_html
  elsif title = title_from(doc)
    label = title.next
    label = label.next if blank?(label)
    if label.name == 'text'
      label.inner_text
    else
      label.inner_html
    end
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
  begin
    uri = URI.parse(base_uri).merge(a['href']).to_s
  rescue
    puts 'bad uri: ' + a['href']
    uri = a['href']
  end
  format = doc_format(uri)
  size = doc_size(title)

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
  if title = title_from(doc)
    parent = title.parent
    parent = parent.parent if parent.name == 'h1'
    documents = parent.search('ul a').select do |a|
      a['href']
    end
    documents.map {|a| doc_info a, base_uri }
  else
    []
  end
end

def add_consultation title, uri, start_date, end_date, base_uri
  puts uri
  doc = nil
  published_date = ''

  begin
    if title != 'User consultation'
      html = ScraperWiki.scrape(uri)
      doc = Nokogiri::HTML(html.gsub('&nbsp;',' '))
      if doc_title = title_from(doc)
        title = doc_title.inner_text
      end
    end
  
    description = get_description doc
    documents = get_documents doc, uri
  
    record = {
      'department' => '',
      'title' => clean(title),
      'published_date' => published_date,
      'start_date' => start_date,
      'end_date' => end_date,
      'URI' => uri,
      'description' => description,
      'sponsor' => '',
      'agency' => 'Health and Safety Executive',
      'documents' => [documents, documents.size].inspect
    }
    ScraperWiki.save_sqlite(['URI'], record, 'consultations')
  rescue Exception => e
    puts e.to_s
  end
end

def handle_link a, base_uri
  title = a.inner_text
  uri = base_uri.merge(a['href']).to_s
  label = a.parent

  if label && (label.inner_text.strip.squeeze(' ')[/(began|started) on (.+) and (ended|will end) on (.+)\./])
    start_date = $2
    end_date = $4
    add_consultation title, uri, start_date, end_date, base_uri
  elsif label && label.inner_text[/User consultation/]
    add_consultation 'User consultation', uri, '', '', base_uri   
  else
    puts label
  end
end

uri = 'http://www.hse.gov.uk/consult/live.htm'
base_uri = URI.parse(uri)
html = ScraperWiki.scrape(uri)
doc = Nokogiri::HTML html

doc.at('#contentContainer').search('li a').each do |a|
  handle_link a, base_uri
end

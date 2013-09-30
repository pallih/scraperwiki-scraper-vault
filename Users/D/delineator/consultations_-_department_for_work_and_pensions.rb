require 'nokogiri'
require 'uri'
require 'mechanize'

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

def remote_file_exists?(url)
  begin
    agent = Mechanize.new
    page = agent.get(url)
    code = page.code
    if code == "200"
      page.body
    else
      false
    end
  rescue
    false
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

def get_documents base_uri, title, doc
  if base_uri[/pdf$/]
    [title, base_uri, 'PDF','']
  else
    doc.search('.dwp > li > a').collect do |a|
      title = clean(a.inner_text)
      uri = URI.parse(base_uri).merge( URI.encode(a['href']) ).to_s
      format = doc_format uri

      label = a.next
      size = if label && label.name == 'text' && (value = label.inner_text[/\(([^)]+)\)/,1]) && value[/\d/]
               value
             else
               ''
             end

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
  end
end

def get_description doc
  abstract = doc.at('div[@property="dc:abstract"]') ? doc.at('div[@property="dc:abstract"]').inner_html : nil
  audience = doc.at('div[@property="dc:audience"]') ? doc.at('div[@property="dc:audience"]').inner_html : nil

  description = []

  if abstract.nil? && doc.at('#content > h1')
    summary = doc.at('#content > h1').next
    while summary && summary.name != 'h2'
      description << ((summary.name == 'text') ? summary.inner_text : summary.inner_html)
      summary = summary.next
    end
    description = description.map {|x| x.strip}
    description.delete_if {|x| x.nil? || x.size == 0}

    description = ['<p>' + description.join("</p><p>") + '</p>'] unless description.first[/<p>/]
  end

  description += [abstract, audience]
  description.compact.join("\n\n")
end

def add_consultation title, uri, start_date, end_date, base_uri
  if html = remote_file_exists?(uri)
    doc = Nokogiri::HTML(html, nil, 'utf-8')
    description = get_description doc
    documents = get_documents uri, title, doc
  
    record = {
      'department' => 'Department for Work and Pensions',
      'title' => clean(title),
      'published_date' => '',
      'end_date' => end_date,
      'URI' => uri,
      'description' => description,
      'start_date' => start_date,
      'sponsor' => '',
      'agency' => '',
      'documents' => [documents, documents.size].inspect
    }
    ScraperWiki.save_sqlite(['URI'], record, 'consultations')
  end
end

def date_from text
  if text.sub('Extended to ','').strip[/(\d\d)\/(\d\d)\/(\d\d)$/]
    "20#{$3}-#{$2}-#{$1}"
  else
    ''
  end
end

def do_year year
  uri = "http://www.dwp.gov.uk/consultations/#{year}/"
  base_uri = URI.parse(uri)  

  html = ScraperWiki.scrape(uri)
  doc = Nokogiri::HTML(html)

  doc.search('.listTable tr').each do |tr|
    if tr.at('td')
      cells = tr.search('td')
      link = cells.last.at('a')
      uri = base_uri.merge(link['href']).to_s
      title = link.inner_text

      start_date = date_from cells.first.inner_text
      end_date = date_from cells[1].inner_text

      add_consultation title, uri, start_date, end_date, base_uri
    end
  end
end

current_year = Date.today.year

2010.upto(current_year) do |year|
  do_year year
endrequire 'nokogiri'
require 'uri'
require 'mechanize'

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

def remote_file_exists?(url)
  begin
    agent = Mechanize.new
    page = agent.get(url)
    code = page.code
    if code == "200"
      page.body
    else
      false
    end
  rescue
    false
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

def get_documents base_uri, title, doc
  if base_uri[/pdf$/]
    [title, base_uri, 'PDF','']
  else
    doc.search('.dwp > li > a').collect do |a|
      title = clean(a.inner_text)
      uri = URI.parse(base_uri).merge( URI.encode(a['href']) ).to_s
      format = doc_format uri

      label = a.next
      size = if label && label.name == 'text' && (value = label.inner_text[/\(([^)]+)\)/,1]) && value[/\d/]
               value
             else
               ''
             end

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
  end
end

def get_description doc
  abstract = doc.at('div[@property="dc:abstract"]') ? doc.at('div[@property="dc:abstract"]').inner_html : nil
  audience = doc.at('div[@property="dc:audience"]') ? doc.at('div[@property="dc:audience"]').inner_html : nil

  description = []

  if abstract.nil? && doc.at('#content > h1')
    summary = doc.at('#content > h1').next
    while summary && summary.name != 'h2'
      description << ((summary.name == 'text') ? summary.inner_text : summary.inner_html)
      summary = summary.next
    end
    description = description.map {|x| x.strip}
    description.delete_if {|x| x.nil? || x.size == 0}

    description = ['<p>' + description.join("</p><p>") + '</p>'] unless description.first[/<p>/]
  end

  description += [abstract, audience]
  description.compact.join("\n\n")
end

def add_consultation title, uri, start_date, end_date, base_uri
  if html = remote_file_exists?(uri)
    doc = Nokogiri::HTML(html, nil, 'utf-8')
    description = get_description doc
    documents = get_documents uri, title, doc
  
    record = {
      'department' => 'Department for Work and Pensions',
      'title' => clean(title),
      'published_date' => '',
      'end_date' => end_date,
      'URI' => uri,
      'description' => description,
      'start_date' => start_date,
      'sponsor' => '',
      'agency' => '',
      'documents' => [documents, documents.size].inspect
    }
    ScraperWiki.save_sqlite(['URI'], record, 'consultations')
  end
end

def date_from text
  if text.sub('Extended to ','').strip[/(\d\d)\/(\d\d)\/(\d\d)$/]
    "20#{$3}-#{$2}-#{$1}"
  else
    ''
  end
end

def do_year year
  uri = "http://www.dwp.gov.uk/consultations/#{year}/"
  base_uri = URI.parse(uri)  

  html = ScraperWiki.scrape(uri)
  doc = Nokogiri::HTML(html)

  doc.search('.listTable tr').each do |tr|
    if tr.at('td')
      cells = tr.search('td')
      link = cells.last.at('a')
      uri = base_uri.merge(link['href']).to_s
      title = link.inner_text

      start_date = date_from cells.first.inner_text
      end_date = date_from cells[1].inner_text

      add_consultation title, uri, start_date, end_date, base_uri
    end
  end
end

current_year = Date.today.year

2010.upto(current_year) do |year|
  do_year year
end
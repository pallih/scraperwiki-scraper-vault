require 'scraperwiki'
require 'nokogiri'

def correct_regex?(regex, return_count, string)
  results = string.scan(regex)
  results && results[0] && results[0].count == return_count
end

def cleanup_number(original)
  if original
    new = original.gsub('(','')
    new = new.gsub(') ',')')
    new = new.gsub(')','-')
    new = new.gsub('/','-')
    new = new.gsub('.','-')
  else
    original
  end
end

html = ScraperWiki.scrape('http://www.wineinstitute.org/resources/external-links/regional-winery-grower-associations-of-california')
doc = Nokogiri::HTML(html)
for item in doc.search('dl.resources')
  name = item.search('dt')[0].inner_text
  link = item.search('dt a').count > 0 ? item.search('dt a')[0]['href'] : nil
  contact_name = nil
  email_address = nil
  phone_number = nil
  fax_number = nil

  for line in item.search('dd')
    if line.inner_text.include?('Contact:')
      #puts line.inner_text
      contact_name = line.inner_text.sub('Contact: ','')
      email_address = line.search('a')[0]['href'].sub('mailto:','') if line.search('a').count > 0
    elsif line.inner_text.include?('Phone:')
      regex1 = /Phone: (.+)\s*Fax: (.+)(?:\\*n*)\s*Email: (.+)(?:\\*n*)\s*Website: (.+)/
      regex2 = /Phone: (.+)\s*Fax: (.+)(?:\\*n*)\s*Email: (.+)(?:\\*n*)\s*/
      regex3 = /Phone: (.+)\s*Fax: (.+)(?:\\*n*)\s*/
      regex4 = /Phone: (.+)\s*/
      cleaned_line = line.inner_text.chomp
      if correct_regex?(regex1, 4, cleaned_line)
        results = cleaned_line.scan(regex1)[0]
        phone_number = results[0].strip
        fax_number = results[1].strip
        email_address = results[2].strip
        website_url = results[3].strip
      elsif correct_regex?(regex2, 3, cleaned_line)
        results = cleaned_line.scan(regex2)[0]
        phone_number = results[0].strip
        fax_number = results[1].strip
        email_address = results[2].strip
      elsif correct_regex?(regex3, 2, cleaned_line)
        results = cleaned_line.scan(regex3)[0]
        phone_number = results[0].strip
        fax_number = results[1].strip
      else
        results = cleaned_line.scan(regex4)[0]
        phone_number = results[0].strip
      end
      #puts results.inspect
    elsif line.inner_text.include?('Email:')
      email_address = line.search('a')[0]['href'].sub('mailto:','') if line.search('a').count > 0
    end
  end

  data = {
    'name' => name,
    'website_url' => link,
    'contact_name' => contact_name,
    'email_address' => email_address,
    'phone_number' => cleanup_number(phone_number),
    'fax_number' => cleanup_number(fax_number)
  }
  puts data.to_json
  ScraperWiki.save_sqlite(unique_keys=['name'], data=data)
end
require 'scraperwiki'
require 'nokogiri'

def correct_regex?(regex, return_count, string)
  results = string.scan(regex)
  results && results[0] && results[0].count == return_count
end

def cleanup_number(original)
  if original
    new = original.gsub('(','')
    new = new.gsub(') ',')')
    new = new.gsub(')','-')
    new = new.gsub('/','-')
    new = new.gsub('.','-')
  else
    original
  end
end

html = ScraperWiki.scrape('http://www.wineinstitute.org/resources/external-links/regional-winery-grower-associations-of-california')
doc = Nokogiri::HTML(html)
for item in doc.search('dl.resources')
  name = item.search('dt')[0].inner_text
  link = item.search('dt a').count > 0 ? item.search('dt a')[0]['href'] : nil
  contact_name = nil
  email_address = nil
  phone_number = nil
  fax_number = nil

  for line in item.search('dd')
    if line.inner_text.include?('Contact:')
      #puts line.inner_text
      contact_name = line.inner_text.sub('Contact: ','')
      email_address = line.search('a')[0]['href'].sub('mailto:','') if line.search('a').count > 0
    elsif line.inner_text.include?('Phone:')
      regex1 = /Phone: (.+)\s*Fax: (.+)(?:\\*n*)\s*Email: (.+)(?:\\*n*)\s*Website: (.+)/
      regex2 = /Phone: (.+)\s*Fax: (.+)(?:\\*n*)\s*Email: (.+)(?:\\*n*)\s*/
      regex3 = /Phone: (.+)\s*Fax: (.+)(?:\\*n*)\s*/
      regex4 = /Phone: (.+)\s*/
      cleaned_line = line.inner_text.chomp
      if correct_regex?(regex1, 4, cleaned_line)
        results = cleaned_line.scan(regex1)[0]
        phone_number = results[0].strip
        fax_number = results[1].strip
        email_address = results[2].strip
        website_url = results[3].strip
      elsif correct_regex?(regex2, 3, cleaned_line)
        results = cleaned_line.scan(regex2)[0]
        phone_number = results[0].strip
        fax_number = results[1].strip
        email_address = results[2].strip
      elsif correct_regex?(regex3, 2, cleaned_line)
        results = cleaned_line.scan(regex3)[0]
        phone_number = results[0].strip
        fax_number = results[1].strip
      else
        results = cleaned_line.scan(regex4)[0]
        phone_number = results[0].strip
      end
      #puts results.inspect
    elsif line.inner_text.include?('Email:')
      email_address = line.search('a')[0]['href'].sub('mailto:','') if line.search('a').count > 0
    end
  end

  data = {
    'name' => name,
    'website_url' => link,
    'contact_name' => contact_name,
    'email_address' => email_address,
    'phone_number' => cleanup_number(phone_number),
    'fax_number' => cleanup_number(fax_number)
  }
  puts data.to_json
  ScraperWiki.save_sqlite(unique_keys=['name'], data=data)
end

# Members of the Legislative Assembly of New Brunswick
# If you really want to get the photo url it is available following the url for each MLA.
require 'iconv'
require 'open-uri'
require 'nokogiri'

BASE_URL = 'http://www1.gnb.ca/legis/bios1'
MLA_LIST_SOURCE = BASE_URL + '/index-e.asp'
OFFICE = 'MLA'
PARTY_LONG_NAME = { 'L' => 'Liberal', 'PC' => 'Conservative' }

# will yield a Hash with the MLA's data
def fetch_mla_list(source, &block)
  doc = Nokogiri::HTML(open(source))
  
  table = find_mlas_table(doc)
  table.css('tr').each do |tr| 
    mla_data = mla_data_from_table_row(tr)
    yield mla_data if mla_data
  end  
end

def find_mlas_table(doc)
  container_div = doc.css('div')[15]
  container_div.css('table')[1]
end

def mla_data_from_table_row(tr)
   _, district_td, name_and_party_td, email_td = tr.children.css('td').to_a     
   return if name_and_party_td.text.strip == 'Vacant'
   district = district_td.content
   name, prefix, party, url = parse_name_party_and_url(name_and_party_td)
   email = email_td.content
   
   data = { district_name: clean_string(district), 
     name: clean_string(name),
     party_name: clean_string(party),
     elected_office: OFFICE, 
     source_url: MLA_LIST_SOURCE,
     email: clean_string(email),
     url: clean_string(url), 
    }
  data.merge!({extra: {honorific_prefix: prefix}.to_json}) if prefix
  data
end

def parse_name_party_and_url(td)
 content = clean_string(td.content)
 pattern = /\(.+\)/
 party =  content.match(pattern).to_a.first
 name = content.gsub(party, '')
 prefix = name[/\AHon./]
 name = name.strip.gsub(/\AHon\.[[:space:]]+|,[[:space:]]Q\.C\.\z/, '')
 party.gsub!(/\(|\)/, '')
 party = PARTY_LONG_NAME[party] if PARTY_LONG_NAME.keys.include?(party)
 path = td.css('a').first['href']
 url = generate_url_from_path(path)

 [name, prefix, party, url]
end

# This function is very fragile, if something goes wrong chances are the problem is here.
# For some reason Nokogiri is removing parts of the query string in the path inside the href
# attributes, I attemped to reconstruct them here since url is optional you can just drop it if it gives
# trouble.
def generate_url_from_path(path)
 file = 'bio-e.asp' 

 args = path.gsub("./\"#{file}\"?", '')
 _, id, lang, legislature_no = args.split('=')
 params = "IDNo=#{id}&version=#{lang}&legisNO=#{legislature_no}"
 
 "#{BASE_URL}/#{file}?#{params}"
end

def clean_string(str)
 str.gsub(/\A[[:space:]]+|[[:space:]]+\z/, '')
end

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end
fetch_mla_list(MLA_LIST_SOURCE){ |mla_data| ScraperWiki.save_sqlite(['district_name'], mla_data) }

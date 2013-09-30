# coding: utf-8

# Run from root of https://github.com/opennorth/represent-canada-data and upload to:
# http://public.slashpoundbang.com/csds.json
=begin
require 'iconv'
require 'json'
require 'rgeo/shapefile'
filename = File.join('fed', 'csd', 'gcsd000a11a_e.shp')
csds = {}
RGeo::Shapefile::Reader.open(filename) do |file|
  file.each do |record|
    csds[record['CSDUID'].to_i] = {
      name: Iconv.conv('UTF-8', 'ISO-8859-1', record['CSDNAME']),
      type: Iconv.conv('UTF-8', 'ISO-8859-1', record['CSDTYPE']),
      mrc:  Iconv.conv('UTF-8', 'ISO-8859-1', record['CDNAME']),
      province: Iconv.conv('UTF-8', 'ISO-8859-1', record['PRNAME']),
    }
  end
end
File.open('csds.json', 'w') do |f|
  f.write csds.to_json
end
=end

require 'json'
require 'open-uri'
require 'time'

require 'nokogiri'

BASE_URL = 'http://www.mamrot.gouv.qc.ca/'
LIST_URL = BASE_URL + 'repertoire-des-municipalites/fiche/municipalite/'

def log(message)
  puts message
  ScraperWiki.save_sqlite([:timestamp], {
    timestamp: Time.now.to_f,
    message: message,
  }, 'messages')
end

# Get the list of Québec municipalities from MAMROT.
# @note The list of municipalities changes very rarely, so run every 6 months.
time = ScraperWiki.get_var('municipalities:last_run', Time.at(0).to_s)
if Time.parse(time) < Time.now - 15_778_463
  puts "Get Québec municipalities (last scraped at #{time})"
  ScraperWiki.sqliteexecute 'DELETE FROM municipalities'
  Nokogiri::HTML(open(LIST_URL)).css('#c11 tbody tr').each do |tr|
    tds = tr.css('td')
    data = {
      code: tds[0].text,
      name: tds[2].text,
      type: tds[1].text,
      mrc: tds[3].text,
      region: tds[4].text,
      url: BASE_URL + tds[2].at_css('a')[:href],
    }
    ScraperWiki.save_sqlite(['code'], data, 'municipalities')
  end
  ScraperWiki.save_var('municipalities:last_run', Time.now)
end

puts 'Get Census subdivisions'
CENSUS_SUBDIVISIONS = JSON.parse(open('http://public.slashpoundbang.com/csds.json').read)

# Map municipality types to Census subdivision types.
#
# Élections Québec: CT, M, P, V, VL
# MAMROT: Canton, Cantons unis, Municipalité, Paroisse, Village, Ville
# Census subdivisions: CT, CU, MÉ, NO, PE, V, VL
# Census subdivisions (First Nations): IRI, S-É, TC, TI, TK, VC, VK, VN
#
# @see http://www12.statcan.gc.ca/census-recensement/2006/ref/symb-ab-acr-eng.cfm#cst
TYPE_MAP = {
  'Canton'       => 'CT',
  'Cantons unis' => 'CU',
  'M'            => 'MÉ',
  'Municipalité' => 'MÉ',
  'P'            => 'PE',
  'Paroisse'     => 'PE',
  'Ville'        => 'V',
  'Village'      => 'VL',
}

# Map municipality names to Census subdivision names.
NAME_MAP = {
  'Ham-Sud'                      => 'Saint-Joseph-de-Ham-Sud', # Statistics Canada is outdated (2011)
  'Pike River'                   => 'Saint-Pierre-de-Véronne-à-Pike-River', # Statistics Canada is outdated (2012)
  'Saint-Nérée-de-Bellechasse'   => 'Saint-Nérée', # Statistics Canada is outdated (2012)
  'Cascapédia–Saint-Jules' => 'Saint-Jules', # Statistics Canada is outdated (2000)

  # Dashes.
  'Métabetchouan—Lac-à-la-Croix' => 'Métabetchouan--Lac-à-la-Croix',
  'Métabetchouan–Lac-à-la-Croix' => 'Métabetchouan--Lac-à-la-Croix',
  'Port-Daniel—Gascons'          => 'Port-Daniel--Gascons',
  'Port-Daniel–Gascons'          => 'Port-Daniel--Gascons',
  'Saint-Côme—Linière'           => 'Saint-Côme--Linière',
  'Saint-Côme–Linière'           => 'Saint-Côme--Linière',
  'Saint-Faustin—Lac-Carré'      => 'Saint-Faustin--Lac-Carré',
  'Saint-Faustin–Lac-Carré'      => 'Saint-Faustin--Lac-Carré',
  'Saint-Lin—Laurentides'        => 'Saint-Lin--Laurentides',
  'Saint-Lin–Laurentides'        => 'Saint-Lin--Laurentides',
}

# Map MRCs to Census subdivision MRCs.
MRC_MAP = {
  'La Côte-de-Beaupré \ Communauté métropolitaine de Québec' => 'La Côte-de-Beaupré',
  'Les Chenaux' => 'Francheville', # Statistics Canada is outdated (2002)
}

def match_census_subdivision(list)
  result = {}
  list.each do |data|
    name = NAME_MAP[data['name']] || data['name']
    type = TYPE_MAP[data['type']] || data['type']
    mrc = MRC_MAP[data['mrc']] || data['mrc']
    # Élections Québec doesn't provide MRC.
    matches = CENSUS_SUBDIVISIONS.select do |_,x|
      x['name'] == name && x['type'] == type && x['mrc'] == mrc
    end
    if matches.empty? 
      matches = CENSUS_SUBDIVISIONS.select do |_,x|
        x['name'] == name && x['type'] == type
      end
    end
    if matches.empty? 
      matches = CENSUS_SUBDIVISIONS.select do |_,x|
        x['name'] == name
      end
    end
    case matches.size
    when 1
      result[matches.keys.first] = data
    when 0
      log "No Census subdivision found with name '#{name}', type '#{type}', MRC '#{mrc}'"
    else
      log "Multiple Census subdivisions found with '#{name}', type '#{type}', MRC '#{mrc}'"
    end
  end
  result
end

# Map Québec municipalities to Census subdivisions.
puts 'Match Québec municipalities'
csds = match_census_subdivision ScraperWiki.select('* from municipalities')

=begin
# Map municipalities with districts to Census subdivisions.
puts 'Match Québec municipalities with districts'
list = Nokogiri::HTML(open('http://www.electionsquebec.qc.ca/francais/municipal/carte-electorale/liste-des-municipalites-divisees-en-districts-electoraux.php?index=1')).at_css('.zone-contenu .boite-grise')
# Remove strong tags, but leave their inner text.
# @note using #replace will result in two adjacent text nodes
list.css('strong').each do |node|
  node.next.content = node.text + node.next.text
  node.remove
end
argument = list.children.select{|node| node.node_name == 'text'}.map do |node|
  name, type = node.text.strip.match(/\A([^,]+), (.+)\z/)[1..2]
  if name == "L'Ange-Gardien"
    {'name' => name, 'type' => type, 'mrc' => "Les Collines-de-l'Outaouais"}
  else
    {'name' => name, 'type' => type}
  end
end
csds_with_districts = match_census_subdivision argument
=end

POSITION_MAP = {
  'Maire'           => 'Mayor',
  'Administrateur'  => 'Administrator',
  'Administratrice' => 'Administrator',
}
POSTAL_CODE_REGEX = /([A-Z][0-9][A-Z][,\n ]?[0-9][A-Z][0-9])?\z/

# @todo Using a meaningless unique_key is not ideal. Will result in duplicates
# appearing at end of list if the list of representatives shrinks.
puts 'Scrape mayors and councillors'
index = 0
csds.each do |csduid,data|
  # Skip municipalities with districts. We will scrape them separately.
  #next if csds_with_districts.keys.include? csduid

  url = LIST_URL + data['code']
  doc = Nokogiri::HTML(open(url))
  tab = doc.at_css('#onglet-information')
  strong = tab.at_xpath('//strong[starts-with(text(), "Population")]')
  if strong and strong.next
    ScraperWiki.save_sqlite(['code'], data.merge({
      population: strong.next.text.gsub(/[[:space:]]/, '').to_i,
    }), 'municipalities')
  else
    log "Couldn't get population of CSD #{csduid}"
  end

  tab = doc.at_css('#onglet-organisation')

  coordonnees = doc.at_css('.dans-cette-page')
  liens = doc.at_css('.liens')
  url_a = liens.at_css('a[target="_blank"]')
  fax = coordonnees.text[/Télécopieur[[:space:]:]+([\d -]+)/, 1]

  postal = coordonnees.at_css('p:has(br)').inner_html.gsub(/[[:space:]]*<br>/, "\n")
  unless postal[/(QC|\(?Qu[ée]bec\)?)[,\n ]*#{POSTAL_CODE_REGEX}/]
    postal = postal.sub(POSTAL_CODE_REGEX, ' QC  \1').strip
  end

  shared = {
    offices: [{
      postal: postal,
      tel: coordonnees.text[/Téléphone[[:space:]:]+([\d -]+)/, 1].strip,
      fax: fax && fax.strip,
    }].to_json,
    email: liens.at_css('a[href^="mailto"]')[:href].sub('mailto:', ''),
    url: url_a && url_a[:href],
    source_url: url,
    district_id: csduid,
    district_name: NAME_MAP[data['name']] || data['name'],
  }

  strong = nil
  position = nil
  ['Maire', 'Administrateur', 'Administratrice'].each do |label|
    strong = tab.at_xpath(%(//strong[starts-with(text(), "#{label}")]))
    if strong
      position = POSITION_MAP[label]
      break
    end
  end

  if strong and strong.next
    name = strong.next.text.gsub(/\A[[:space:]]+|[[:space:]]+\z/, '').sub(/\A(Mme|Père|Soeur) /, '').sub(/ \(p\.i\.\)\z/, '')
    unless name == 'Poste vacant'
      ScraperWiki.save_sqlite(['index'], shared.merge({
        index: index,
        name: name.sub(/\AMme /, ''),
        elected_office: position,
      }))
      index += 1
    end
  else
    log "No mayor found at #{url}"
  end

  span = tab.at_xpath('//span[starts-with(text(), "Conseillers et conseillères")]')
  if span and span.parent.next_element and span.parent.next_element.name == 'ol'
    span.parent.next_element.css('li').each do |li|
      unless ['Poste vacant', 'Sans objet'].include? li.text
        ScraperWiki.save_sqlite(['index'], shared.merge({
          index: index,
          name: li.text.sub(/\AMme /, ''),
          elected_office: 'Councillor',
        }))
        index += 1
      end
    end
  else
    log "No councillors found at #{url}" 
  end
end
ScraperWiki.sqliteexecute %(DELETE FROM swdata WHERE "index" > #{index})

# Validate first and last names:
# puts db['swdata'].find({name: /^\S+/}, {fields: :name}).to_a.map{|x| x['name'][/^\S+/]}.reject{|x| x[/\A\p{Lu}\p{Ll}+(-\p{Lu}\p{Ll}+)?\z/]}.uniq.sort
# puts db['swdata'].find({name: /\S+$/}, {fields: :name}).to_a.map{|x| x['name'][/\S+$/]}.reject{|x| x[/\A(\p{Lu}+|(D'|De|Du|L'|Le|Mac|Mc|O')?\p{Lu}\p{Ll}+(-\p{Lu}\p{Ll}+)*)\z/]}.uniq.sort
# puts db['swdata'].find({name: / .+ /}, {fields: :name}).to_a.map{|x| x['name']}.sort

# Get the total population represented:
# db['municipalities'].find({'name' => {'$nin' => csds_with_districts}}).reduce(0){|sum,x| sum + x['population'].to_i}
# coding: utf-8

# Run from root of https://github.com/opennorth/represent-canada-data and upload to:
# http://public.slashpoundbang.com/csds.json
=begin
require 'iconv'
require 'json'
require 'rgeo/shapefile'
filename = File.join('fed', 'csd', 'gcsd000a11a_e.shp')
csds = {}
RGeo::Shapefile::Reader.open(filename) do |file|
  file.each do |record|
    csds[record['CSDUID'].to_i] = {
      name: Iconv.conv('UTF-8', 'ISO-8859-1', record['CSDNAME']),
      type: Iconv.conv('UTF-8', 'ISO-8859-1', record['CSDTYPE']),
      mrc:  Iconv.conv('UTF-8', 'ISO-8859-1', record['CDNAME']),
      province: Iconv.conv('UTF-8', 'ISO-8859-1', record['PRNAME']),
    }
  end
end
File.open('csds.json', 'w') do |f|
  f.write csds.to_json
end
=end

require 'json'
require 'open-uri'
require 'time'

require 'nokogiri'

BASE_URL = 'http://www.mamrot.gouv.qc.ca/'
LIST_URL = BASE_URL + 'repertoire-des-municipalites/fiche/municipalite/'

def log(message)
  puts message
  ScraperWiki.save_sqlite([:timestamp], {
    timestamp: Time.now.to_f,
    message: message,
  }, 'messages')
end

# Get the list of Québec municipalities from MAMROT.
# @note The list of municipalities changes very rarely, so run every 6 months.
time = ScraperWiki.get_var('municipalities:last_run', Time.at(0).to_s)
if Time.parse(time) < Time.now - 15_778_463
  puts "Get Québec municipalities (last scraped at #{time})"
  ScraperWiki.sqliteexecute 'DELETE FROM municipalities'
  Nokogiri::HTML(open(LIST_URL)).css('#c11 tbody tr').each do |tr|
    tds = tr.css('td')
    data = {
      code: tds[0].text,
      name: tds[2].text,
      type: tds[1].text,
      mrc: tds[3].text,
      region: tds[4].text,
      url: BASE_URL + tds[2].at_css('a')[:href],
    }
    ScraperWiki.save_sqlite(['code'], data, 'municipalities')
  end
  ScraperWiki.save_var('municipalities:last_run', Time.now)
end

puts 'Get Census subdivisions'
CENSUS_SUBDIVISIONS = JSON.parse(open('http://public.slashpoundbang.com/csds.json').read)

# Map municipality types to Census subdivision types.
#
# Élections Québec: CT, M, P, V, VL
# MAMROT: Canton, Cantons unis, Municipalité, Paroisse, Village, Ville
# Census subdivisions: CT, CU, MÉ, NO, PE, V, VL
# Census subdivisions (First Nations): IRI, S-É, TC, TI, TK, VC, VK, VN
#
# @see http://www12.statcan.gc.ca/census-recensement/2006/ref/symb-ab-acr-eng.cfm#cst
TYPE_MAP = {
  'Canton'       => 'CT',
  'Cantons unis' => 'CU',
  'M'            => 'MÉ',
  'Municipalité' => 'MÉ',
  'P'            => 'PE',
  'Paroisse'     => 'PE',
  'Ville'        => 'V',
  'Village'      => 'VL',
}

# Map municipality names to Census subdivision names.
NAME_MAP = {
  'Ham-Sud'                      => 'Saint-Joseph-de-Ham-Sud', # Statistics Canada is outdated (2011)
  'Pike River'                   => 'Saint-Pierre-de-Véronne-à-Pike-River', # Statistics Canada is outdated (2012)
  'Saint-Nérée-de-Bellechasse'   => 'Saint-Nérée', # Statistics Canada is outdated (2012)
  'Cascapédia–Saint-Jules' => 'Saint-Jules', # Statistics Canada is outdated (2000)

  # Dashes.
  'Métabetchouan—Lac-à-la-Croix' => 'Métabetchouan--Lac-à-la-Croix',
  'Métabetchouan–Lac-à-la-Croix' => 'Métabetchouan--Lac-à-la-Croix',
  'Port-Daniel—Gascons'          => 'Port-Daniel--Gascons',
  'Port-Daniel–Gascons'          => 'Port-Daniel--Gascons',
  'Saint-Côme—Linière'           => 'Saint-Côme--Linière',
  'Saint-Côme–Linière'           => 'Saint-Côme--Linière',
  'Saint-Faustin—Lac-Carré'      => 'Saint-Faustin--Lac-Carré',
  'Saint-Faustin–Lac-Carré'      => 'Saint-Faustin--Lac-Carré',
  'Saint-Lin—Laurentides'        => 'Saint-Lin--Laurentides',
  'Saint-Lin–Laurentides'        => 'Saint-Lin--Laurentides',
}

# Map MRCs to Census subdivision MRCs.
MRC_MAP = {
  'La Côte-de-Beaupré \ Communauté métropolitaine de Québec' => 'La Côte-de-Beaupré',
  'Les Chenaux' => 'Francheville', # Statistics Canada is outdated (2002)
}

def match_census_subdivision(list)
  result = {}
  list.each do |data|
    name = NAME_MAP[data['name']] || data['name']
    type = TYPE_MAP[data['type']] || data['type']
    mrc = MRC_MAP[data['mrc']] || data['mrc']
    # Élections Québec doesn't provide MRC.
    matches = CENSUS_SUBDIVISIONS.select do |_,x|
      x['name'] == name && x['type'] == type && x['mrc'] == mrc
    end
    if matches.empty? 
      matches = CENSUS_SUBDIVISIONS.select do |_,x|
        x['name'] == name && x['type'] == type
      end
    end
    if matches.empty? 
      matches = CENSUS_SUBDIVISIONS.select do |_,x|
        x['name'] == name
      end
    end
    case matches.size
    when 1
      result[matches.keys.first] = data
    when 0
      log "No Census subdivision found with name '#{name}', type '#{type}', MRC '#{mrc}'"
    else
      log "Multiple Census subdivisions found with '#{name}', type '#{type}', MRC '#{mrc}'"
    end
  end
  result
end

# Map Québec municipalities to Census subdivisions.
puts 'Match Québec municipalities'
csds = match_census_subdivision ScraperWiki.select('* from municipalities')

=begin
# Map municipalities with districts to Census subdivisions.
puts 'Match Québec municipalities with districts'
list = Nokogiri::HTML(open('http://www.electionsquebec.qc.ca/francais/municipal/carte-electorale/liste-des-municipalites-divisees-en-districts-electoraux.php?index=1')).at_css('.zone-contenu .boite-grise')
# Remove strong tags, but leave their inner text.
# @note using #replace will result in two adjacent text nodes
list.css('strong').each do |node|
  node.next.content = node.text + node.next.text
  node.remove
end
argument = list.children.select{|node| node.node_name == 'text'}.map do |node|
  name, type = node.text.strip.match(/\A([^,]+), (.+)\z/)[1..2]
  if name == "L'Ange-Gardien"
    {'name' => name, 'type' => type, 'mrc' => "Les Collines-de-l'Outaouais"}
  else
    {'name' => name, 'type' => type}
  end
end
csds_with_districts = match_census_subdivision argument
=end

POSITION_MAP = {
  'Maire'           => 'Mayor',
  'Administrateur'  => 'Administrator',
  'Administratrice' => 'Administrator',
}
POSTAL_CODE_REGEX = /([A-Z][0-9][A-Z][,\n ]?[0-9][A-Z][0-9])?\z/

# @todo Using a meaningless unique_key is not ideal. Will result in duplicates
# appearing at end of list if the list of representatives shrinks.
puts 'Scrape mayors and councillors'
index = 0
csds.each do |csduid,data|
  # Skip municipalities with districts. We will scrape them separately.
  #next if csds_with_districts.keys.include? csduid

  url = LIST_URL + data['code']
  doc = Nokogiri::HTML(open(url))
  tab = doc.at_css('#onglet-information')
  strong = tab.at_xpath('//strong[starts-with(text(), "Population")]')
  if strong and strong.next
    ScraperWiki.save_sqlite(['code'], data.merge({
      population: strong.next.text.gsub(/[[:space:]]/, '').to_i,
    }), 'municipalities')
  else
    log "Couldn't get population of CSD #{csduid}"
  end

  tab = doc.at_css('#onglet-organisation')

  coordonnees = doc.at_css('.dans-cette-page')
  liens = doc.at_css('.liens')
  url_a = liens.at_css('a[target="_blank"]')
  fax = coordonnees.text[/Télécopieur[[:space:]:]+([\d -]+)/, 1]

  postal = coordonnees.at_css('p:has(br)').inner_html.gsub(/[[:space:]]*<br>/, "\n")
  unless postal[/(QC|\(?Qu[ée]bec\)?)[,\n ]*#{POSTAL_CODE_REGEX}/]
    postal = postal.sub(POSTAL_CODE_REGEX, ' QC  \1').strip
  end

  shared = {
    offices: [{
      postal: postal,
      tel: coordonnees.text[/Téléphone[[:space:]:]+([\d -]+)/, 1].strip,
      fax: fax && fax.strip,
    }].to_json,
    email: liens.at_css('a[href^="mailto"]')[:href].sub('mailto:', ''),
    url: url_a && url_a[:href],
    source_url: url,
    district_id: csduid,
    district_name: NAME_MAP[data['name']] || data['name'],
  }

  strong = nil
  position = nil
  ['Maire', 'Administrateur', 'Administratrice'].each do |label|
    strong = tab.at_xpath(%(//strong[starts-with(text(), "#{label}")]))
    if strong
      position = POSITION_MAP[label]
      break
    end
  end

  if strong and strong.next
    name = strong.next.text.gsub(/\A[[:space:]]+|[[:space:]]+\z/, '').sub(/\A(Mme|Père|Soeur) /, '').sub(/ \(p\.i\.\)\z/, '')
    unless name == 'Poste vacant'
      ScraperWiki.save_sqlite(['index'], shared.merge({
        index: index,
        name: name.sub(/\AMme /, ''),
        elected_office: position,
      }))
      index += 1
    end
  else
    log "No mayor found at #{url}"
  end

  span = tab.at_xpath('//span[starts-with(text(), "Conseillers et conseillères")]')
  if span and span.parent.next_element and span.parent.next_element.name == 'ol'
    span.parent.next_element.css('li').each do |li|
      unless ['Poste vacant', 'Sans objet'].include? li.text
        ScraperWiki.save_sqlite(['index'], shared.merge({
          index: index,
          name: li.text.sub(/\AMme /, ''),
          elected_office: 'Councillor',
        }))
        index += 1
      end
    end
  else
    log "No councillors found at #{url}" 
  end
end
ScraperWiki.sqliteexecute %(DELETE FROM swdata WHERE "index" > #{index})

# Validate first and last names:
# puts db['swdata'].find({name: /^\S+/}, {fields: :name}).to_a.map{|x| x['name'][/^\S+/]}.reject{|x| x[/\A\p{Lu}\p{Ll}+(-\p{Lu}\p{Ll}+)?\z/]}.uniq.sort
# puts db['swdata'].find({name: /\S+$/}, {fields: :name}).to_a.map{|x| x['name'][/\S+$/]}.reject{|x| x[/\A(\p{Lu}+|(D'|De|Du|L'|Le|Mac|Mc|O')?\p{Lu}\p{Ll}+(-\p{Lu}\p{Ll}+)*)\z/]}.uniq.sort
# puts db['swdata'].find({name: / .+ /}, {fields: :name}).to_a.map{|x| x['name']}.sort

# Get the total population represented:
# db['municipalities'].find({'name' => {'$nin' => csds_with_districts}}).reduce(0){|sum,x| sum + x['population'].to_i}

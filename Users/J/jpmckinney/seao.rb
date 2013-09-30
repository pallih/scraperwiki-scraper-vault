# coding: utf-8
require 'date'
require 'time'
require 'mechanize'

# 2012-07-11: 58,238 records to scrape.

# This scraper uses publication date and type as filters.
#
# Other filtering options are:
# * Donneur d'ouvrage (organisation): thousands
# * Région de livraison: 39 values
# * Catégorie (categorie): 56 values
# * Classification UNSPC: 55 values
#
# The other filters are either not effective at getting the number of results
# returned under 200 (e.g. statut), or are not enumerable (e.g. titre).

# 601 records are all of:
# * type: "Attribution de contrat de gré à gré"
# * statut: "Attribué"
# * publication: 2011-09-13
# * fermeture: 2011-09-13
# * categorie: "Services pédagogiques et formation"
# * organisation: Ministère de l'Emploi de la Solidarité sociale
#
# If necessary, we can scrape these records by the sequence of No. Ref.,
# possibly starting at 525244. As is, we only get 200 of them.

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

TYPE_MAP = { # totals as of 2012-07-13
  "Adjudication suite \u00e0 un appel d'offres sur invitation" => 10, #  8584
  "Attribution de contrat de gr\u00e9 \u00e0 gr\u00e9"         => 9,  #  9150
  "Avis d'accr\u00e9ditation"                                  => 13, #     1
  "Avis d'homologation de produits"                            => 6,  #    29
  "Avis d'attribution"                                         => 1,  #    50
  "Avis d'appel d'offres"                                      => 3,  # 39551
  "Avis d'appel d'int\u00e9r\u00eat"                           => 7,  #   259
  "Avis d'adjudication pour achats mandat\u00e9s"              => 11, #     0
  "Avis d'intention"                                           => 2,  #   292
  "Avis de qualification de fournisseurs"                      => 5,  #   169
  "Demande d'information"                                      => 4,  #    32
  "Documents normatifs"                                        => 12, #    17
}

def agent
  @agent ||= begin
    a = Mechanize.new
    a.agent.http.verify_mode = OpenSSL::SSL::VERIFY_NONE
    a
  end
end

def log(message)
  puts message
  ScraperWiki.save_sqlite([:timestamp], {
    timestamp: Time.now.to_f,
    message: message,
  }, 'messages')
end

# Scrapes all data matching the given filters.
#
# @param [Hash] options the search filters
# @option options [Date] :from a date
# @option options [Date] :to a date
# @option options [String] :type a type
def search(options = {})
  from = options[:from]
  to = options[:to]
  type = options[:type]

  if type
    log "Searching from #{from} to #{to} with type #{type}..."
  else
    log "Searching from #{from} to #{to}..."
  end

  # Prepare the search form.
  page = agent.get 'https://seao.ca/Recherche/rech_avancee_y.aspx'
  # Enable desired filters and disable defaults.
  page.forms[0]['UCSearchAdvancePlus1:HDtrSearchNumberPlusT'] = 0
  page.forms[0]['UCSearchAdvancePlus1:HDtrSearchKeywordsPlusT'] = 0
  page.forms[0]['UCSearchAdvancePlus1:HDtrSearchDateTypePlusT'] = 1 if from || to
  page.forms[0]['UCSearchAdvancePlus1:HDtrSearchOpTypePlusT'] = 1 if type

  # Set the filters.
  if from
    page.forms[0]['UCSearchAdvancePlus1:dtxtFromDate:Year'] = from.year
    page.forms[0]['UCSearchAdvancePlus1:dtxtFromDate:Month'] = from.month
    page.forms[0]['UCSearchAdvancePlus1:dtxtFromDate:Day'] = from.day
  end
  if to
    page.forms[0]['UCSearchAdvancePlus1:dtxtToDate:Year'] = to.year
    page.forms[0]['UCSearchAdvancePlus1:dtxtToDate:Month'] = to.month
    page.forms[0]['UCSearchAdvancePlus1:dtxtToDate:Day'] = to.day
  end
  if type
    page.forms[0]['UCSearchAdvancePlus1:typeDropDownList'] = TYPE_MAP[type]
  end

  # Display the maximum rows per page.
  page.forms[0]['UCSearchAdvancePlus1:pageSizeDropDownList'] = 100
  button = page.forms[0].buttons.find{|x| x.name == 'UCSearchAdvancePlus1:searchAdv1Button'}

  # The server responses to a form submission with a page that contains a JavaScript redirect.
  page = agent.get page.forms[0].submit(button).body[/"(.+)"/, 1]
  doc = page.parser

  box = doc.at_css('#UCMessageBox1_labelMessage')
  matched = box && box.text[/Plus de (\d+)/, 1].to_i

  # If you request 100 results per page, up to 200 results will be returned, instead of the reported 150.
  if matched && matched > 200 && type.nil? 
    log "#{matched} results found from #{from} to #{to}."
    [ "Adjudication suite \u00e0 un appel d'offres sur invitation",
      "Attribution de contrat de gr\u00e9 \u00e0 gr\u00e9",
      "Avis d'accr\u00e9ditation",
      "Avis d'appel d'int\u00e9r\u00eat",
      "Avis d'appel d'offres",
      "Avis d'attribution",
      "Avis d'homologation de produits",
      "Avis d'intention",
      "Avis de qualification de fournisseurs",
      "Demande d'information",
    ].each do |type|
      search options.merge(type: type)
    end
  elsif matched && matched > 200 # type already set
    log "#{matched} results found from #{from} to #{to} with type #{type}."
    ScraperWiki.save_sqlite([:key], {
      key: "#{from}-#{to}-#{TYPE_MAP[type]}",
      from: from,
      to: to,
      type: type,
      message: 'Too many matches',
      argument: matched,
      updated_at: Time.now,
    }, 'reprocess')
    scrape(page)
  else
    returned = doc.at_css('#uCSearchResults1_PublishedOpportunityNumResultslbl').text.to_i
    if returned.zero? 
      log "No results."
    else 
      log "Expected SEAO to limit to 150 results." if returned > 150
      log "#{matched || returned} results returned."
      scrape(page)
    end
  end
end

# Scrapes a page of records and paginates to the next page.
#
# @param [Mechanize::Page] page a page to scrape
def scrape(page)
  doc = page.parser
  trs = doc.at_css('#uCSearchResults1_SortOptions').next.css('tr:gt(1)')
  log "Scraping #{trs.size} rows..."

  trs.each do |tr|
    td   = tr.at_css('td:eq(2)')
    a    = td.at_css('a')
    span = td.at_css('.titreAvis')
    type, categorie = span.next_element.next.text.strip.gsub(/[[:space:]]+/, ' ').split(' - ', 2)

    ScraperWiki.save_sqlite([:id], {
      id: a.next.text[/\d+/], # No. Ref.
      no: a.text,
      uri: 'http://seao.ca' + a[:href],
      titre: span.text.strip,
      type: type,
      categorie: categorie,
      organisation: td.at_css('b').text.gsub(/[[:space:]]+/, ' ').sub(/(?<!inc)\.+\z/, '').strip,
      statut: tr.at_css('td:eq(3)').text.strip,
      # Store times as if they were UTC.
      publication: Time.parse(tr.at_css('td:eq(4)').text.strip),
      fermeture: Time.parse(tr.at_css('td:eq(5)').text.strip),
      updated_at: Time.now,
    })
  end

  selected = doc.at_css('#UCSearchResults1_UCPager2_lstPages option[selected]')
  if selected # if there are pages
    option = selected.next
    if option # if there is a next page
      log "Getting next page (#{option[:value]})..."
      page.forms[0]['UCSearchResults1:UCPager2:lstPages'] = option[:value]
      page.forms[0]['__EVENTTARGET'] = 'UCSearchResults1$UCPager2$lstPages'
      page.forms[0]['__EVENTARGUMENT'] = ''
      scrape page.forms[0].submit
    end
  end
end

# If the last run scraped today's data, start from the beginning.
#
# @return [Date] the date from which to start the scraping run
def start
  date = Date.parse(ScraperWiki.get_var('date', '2011-06-01'))
  if date == Date.today
    date = Date.new(2011, 6, 1)
    ScraperWiki.save_var('date', date.to_s)
  end
  date
end

if start == Date.new(2011, 6, 1)
  search from: Date.new(2005, 1, 1), to: Date.new(2011, 5, 31)
end
start.upto(Date.today).each do |date|
  ScraperWiki.save_var('date', date.to_s)
  search from: date, to: date
end

# Restart on next run if appropriate.
start

# coding: utf-8
require 'date'
require 'time'
require 'mechanize'

# 2012-07-11: 58,238 records to scrape.

# This scraper uses publication date and type as filters.
#
# Other filtering options are:
# * Donneur d'ouvrage (organisation): thousands
# * Région de livraison: 39 values
# * Catégorie (categorie): 56 values
# * Classification UNSPC: 55 values
#
# The other filters are either not effective at getting the number of results
# returned under 200 (e.g. statut), or are not enumerable (e.g. titre).

# 601 records are all of:
# * type: "Attribution de contrat de gré à gré"
# * statut: "Attribué"
# * publication: 2011-09-13
# * fermeture: 2011-09-13
# * categorie: "Services pédagogiques et formation"
# * organisation: Ministère de l'Emploi de la Solidarité sociale
#
# If necessary, we can scrape these records by the sequence of No. Ref.,
# possibly starting at 525244. As is, we only get 200 of them.

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

TYPE_MAP = { # totals as of 2012-07-13
  "Adjudication suite \u00e0 un appel d'offres sur invitation" => 10, #  8584
  "Attribution de contrat de gr\u00e9 \u00e0 gr\u00e9"         => 9,  #  9150
  "Avis d'accr\u00e9ditation"                                  => 13, #     1
  "Avis d'homologation de produits"                            => 6,  #    29
  "Avis d'attribution"                                         => 1,  #    50
  "Avis d'appel d'offres"                                      => 3,  # 39551
  "Avis d'appel d'int\u00e9r\u00eat"                           => 7,  #   259
  "Avis d'adjudication pour achats mandat\u00e9s"              => 11, #     0
  "Avis d'intention"                                           => 2,  #   292
  "Avis de qualification de fournisseurs"                      => 5,  #   169
  "Demande d'information"                                      => 4,  #    32
  "Documents normatifs"                                        => 12, #    17
}

def agent
  @agent ||= begin
    a = Mechanize.new
    a.agent.http.verify_mode = OpenSSL::SSL::VERIFY_NONE
    a
  end
end

def log(message)
  puts message
  ScraperWiki.save_sqlite([:timestamp], {
    timestamp: Time.now.to_f,
    message: message,
  }, 'messages')
end

# Scrapes all data matching the given filters.
#
# @param [Hash] options the search filters
# @option options [Date] :from a date
# @option options [Date] :to a date
# @option options [String] :type a type
def search(options = {})
  from = options[:from]
  to = options[:to]
  type = options[:type]

  if type
    log "Searching from #{from} to #{to} with type #{type}..."
  else
    log "Searching from #{from} to #{to}..."
  end

  # Prepare the search form.
  page = agent.get 'https://seao.ca/Recherche/rech_avancee_y.aspx'
  # Enable desired filters and disable defaults.
  page.forms[0]['UCSearchAdvancePlus1:HDtrSearchNumberPlusT'] = 0
  page.forms[0]['UCSearchAdvancePlus1:HDtrSearchKeywordsPlusT'] = 0
  page.forms[0]['UCSearchAdvancePlus1:HDtrSearchDateTypePlusT'] = 1 if from || to
  page.forms[0]['UCSearchAdvancePlus1:HDtrSearchOpTypePlusT'] = 1 if type

  # Set the filters.
  if from
    page.forms[0]['UCSearchAdvancePlus1:dtxtFromDate:Year'] = from.year
    page.forms[0]['UCSearchAdvancePlus1:dtxtFromDate:Month'] = from.month
    page.forms[0]['UCSearchAdvancePlus1:dtxtFromDate:Day'] = from.day
  end
  if to
    page.forms[0]['UCSearchAdvancePlus1:dtxtToDate:Year'] = to.year
    page.forms[0]['UCSearchAdvancePlus1:dtxtToDate:Month'] = to.month
    page.forms[0]['UCSearchAdvancePlus1:dtxtToDate:Day'] = to.day
  end
  if type
    page.forms[0]['UCSearchAdvancePlus1:typeDropDownList'] = TYPE_MAP[type]
  end

  # Display the maximum rows per page.
  page.forms[0]['UCSearchAdvancePlus1:pageSizeDropDownList'] = 100
  button = page.forms[0].buttons.find{|x| x.name == 'UCSearchAdvancePlus1:searchAdv1Button'}

  # The server responses to a form submission with a page that contains a JavaScript redirect.
  page = agent.get page.forms[0].submit(button).body[/"(.+)"/, 1]
  doc = page.parser

  box = doc.at_css('#UCMessageBox1_labelMessage')
  matched = box && box.text[/Plus de (\d+)/, 1].to_i

  # If you request 100 results per page, up to 200 results will be returned, instead of the reported 150.
  if matched && matched > 200 && type.nil? 
    log "#{matched} results found from #{from} to #{to}."
    [ "Adjudication suite \u00e0 un appel d'offres sur invitation",
      "Attribution de contrat de gr\u00e9 \u00e0 gr\u00e9",
      "Avis d'accr\u00e9ditation",
      "Avis d'appel d'int\u00e9r\u00eat",
      "Avis d'appel d'offres",
      "Avis d'attribution",
      "Avis d'homologation de produits",
      "Avis d'intention",
      "Avis de qualification de fournisseurs",
      "Demande d'information",
    ].each do |type|
      search options.merge(type: type)
    end
  elsif matched && matched > 200 # type already set
    log "#{matched} results found from #{from} to #{to} with type #{type}."
    ScraperWiki.save_sqlite([:key], {
      key: "#{from}-#{to}-#{TYPE_MAP[type]}",
      from: from,
      to: to,
      type: type,
      message: 'Too many matches',
      argument: matched,
      updated_at: Time.now,
    }, 'reprocess')
    scrape(page)
  else
    returned = doc.at_css('#uCSearchResults1_PublishedOpportunityNumResultslbl').text.to_i
    if returned.zero? 
      log "No results."
    else 
      log "Expected SEAO to limit to 150 results." if returned > 150
      log "#{matched || returned} results returned."
      scrape(page)
    end
  end
end

# Scrapes a page of records and paginates to the next page.
#
# @param [Mechanize::Page] page a page to scrape
def scrape(page)
  doc = page.parser
  trs = doc.at_css('#uCSearchResults1_SortOptions').next.css('tr:gt(1)')
  log "Scraping #{trs.size} rows..."

  trs.each do |tr|
    td   = tr.at_css('td:eq(2)')
    a    = td.at_css('a')
    span = td.at_css('.titreAvis')
    type, categorie = span.next_element.next.text.strip.gsub(/[[:space:]]+/, ' ').split(' - ', 2)

    ScraperWiki.save_sqlite([:id], {
      id: a.next.text[/\d+/], # No. Ref.
      no: a.text,
      uri: 'http://seao.ca' + a[:href],
      titre: span.text.strip,
      type: type,
      categorie: categorie,
      organisation: td.at_css('b').text.gsub(/[[:space:]]+/, ' ').sub(/(?<!inc)\.+\z/, '').strip,
      statut: tr.at_css('td:eq(3)').text.strip,
      # Store times as if they were UTC.
      publication: Time.parse(tr.at_css('td:eq(4)').text.strip),
      fermeture: Time.parse(tr.at_css('td:eq(5)').text.strip),
      updated_at: Time.now,
    })
  end

  selected = doc.at_css('#UCSearchResults1_UCPager2_lstPages option[selected]')
  if selected # if there are pages
    option = selected.next
    if option # if there is a next page
      log "Getting next page (#{option[:value]})..."
      page.forms[0]['UCSearchResults1:UCPager2:lstPages'] = option[:value]
      page.forms[0]['__EVENTTARGET'] = 'UCSearchResults1$UCPager2$lstPages'
      page.forms[0]['__EVENTARGUMENT'] = ''
      scrape page.forms[0].submit
    end
  end
end

# If the last run scraped today's data, start from the beginning.
#
# @return [Date] the date from which to start the scraping run
def start
  date = Date.parse(ScraperWiki.get_var('date', '2011-06-01'))
  if date == Date.today
    date = Date.new(2011, 6, 1)
    ScraperWiki.save_var('date', date.to_s)
  end
  date
end

if start == Date.new(2011, 6, 1)
  search from: Date.new(2005, 1, 1), to: Date.new(2011, 5, 31)
end
start.upto(Date.today).each do |date|
  ScraperWiki.save_var('date', date.to_s)
  search from: date, to: date
end

# Restart on next run if appropriate.
start


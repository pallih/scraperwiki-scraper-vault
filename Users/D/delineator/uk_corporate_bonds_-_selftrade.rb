require 'open-uri'
require 'nokogiri'

def doc
  html = open('http://trading.selftrade.co.uk/market-data/gilts-bonds/bonds.php').read
  doc = Nokogiri::HTML html
end

def headers
 @headers ||= ["name", "symbol", "latest_price", "price_movement", "last_update", "price_delta", "maturity_date", "income_yield", "gross_redem_yield", "change_1_week1", "trade_type"]
end

def date
  @date ||= Time.now.strftime('%Y-%m-%d')
end

def get_value field, node
  case field
  when 'price_movement'
    nil
  when 'trade_type'
    if node.at('img')
      title = node.at('img')['title']
      title.split(' ').first
    else
      'none'
    end
  else
    node.text.strip
  end
end

def get_bond row
  bond = { 'date' => date }
  cells = row.search('td')
  cells.each_with_index do |node, i|
    field = headers[i]
    value = get_value(field, node)
    bond[field] = value if value
  end

  populate_bond bond  
  bond
end

def populate_bond_field key, name, doc, bond
  begin
    value = doc.at(%Q|th[text()="#{name}"]|).parent.at('td').text.strip
    bond[key] = block_given? ? yield(value) : value
  rescue
  end
end

def populate_bond bond
  #uri = "http://www.selftrade.co.uk/search.php?searchType=simple&query=#{bond['name']}"
  uri = "http://www.selftrade.co.uk/search/index.php?q=#{bond['name']}"
  uri = URI.encode(uri)
  puts uri
  html = open(uri).read
  if html
    doc = Nokogiri::HTML html
    begin
      populate_bond_field('tidn', 'My Account Symbol', doc, bond) {|x| x.split('.').first }
      populate_bond_field('isin', 'ISIN', doc, bond)
      populate_bond_field('coupon', 'Coupon', doc, bond)
    rescue
    end
  end
end

def get_bonds
  doc.at('table').search('tbody/tr').map do |row|
    bond = get_bond(row)
    ScraperWiki::save_sqlite(['date','symbol'], bond)
  end
end

get_bonds


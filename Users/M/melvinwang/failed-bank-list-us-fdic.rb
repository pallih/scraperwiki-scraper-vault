require 'mechanize'

agent = Mechanize.new
page = agent.get("http://www.fdic.gov/bank/individual/failed/banklist.html")

table = page.search("table.sortable")

headers = table.search("thead tr")[0].search("th").map { |th|
  th.content.gsub(" ", "_").strip
}

rows = table.search("tbody tr")
rows.each do |row|
  cells = row.search("td")
  data_hash = {}
  cells.to_a.each_index do |i|
    key = headers[i]
    val = cells[i].content.strip
    data_hash[key] = val
  end
  ScraperWiki.save(data_hash.keys, data_hash)
end

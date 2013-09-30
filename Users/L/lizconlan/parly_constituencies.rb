require 'nokogiri'

letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "y"]


letters.each do |letter|
  html = ScraperWiki.scrape("http://hansard.millbanksystems.com/constituencies/#{letter}")
  html.force_encoding("UTF-8")
  doc = Nokogiri::HTML(html)

  list = doc.xpath("//div[@class='page']/ol/li/a")

  list.each do |node|
    text = node.text
    link = node.attributes["href"].value

    if text =~ /( (\d{4})-(\d{4})?)/
      created = $2
      abolished = $3
      to_from = $1
    end

    name = text.gsub(to_from, "").strip

    record = {'name' => name, 'created' => created, 'abolished' => abolished, 'link' => link}
    ScraperWiki.save(['link'], record)
  end
endrequire 'nokogiri'

letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "y"]


letters.each do |letter|
  html = ScraperWiki.scrape("http://hansard.millbanksystems.com/constituencies/#{letter}")
  html.force_encoding("UTF-8")
  doc = Nokogiri::HTML(html)

  list = doc.xpath("//div[@class='page']/ol/li/a")

  list.each do |node|
    text = node.text
    link = node.attributes["href"].value

    if text =~ /( (\d{4})-(\d{4})?)/
      created = $2
      abolished = $3
      to_from = $1
    end

    name = text.gsub(to_from, "").strip

    record = {'name' => name, 'created' => created, 'abolished' => abolished, 'link' => link}
    ScraperWiki.save(['link'], record)
  end
end
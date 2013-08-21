require 'nokogiri'

letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "y", "z"]


letters.each do |letter|
  html = ScraperWiki.scrape("http://hansard.millbanksystems.com/people/#{letter}")
  html.force_encoding("UTF-8")
  doc = Nokogiri::HTML(html)

  list = doc.xpath("//div[@class='page']/ol")

  list.children.each do |node|
    if node.name == "li"
      anchor = node.at("a")

      link = anchor.attributes["href"].value
      name_data = anchor.text.gsub("\n", " ").strip
      note = node.xpath("span").text.gsub("\n", " ").strip

      surname = name_data[0..name_data.index(",")-1]
      firstname = name_data[name_data.index(",")+1..name_data.index("(")-1].strip
      title = name_data[name_data.index("(")+1..name_data.index(")")-1]
      dates = note.split("-")
      born = dates[0] ? dates[0].strip : ''
      died = dates[1] ? dates[1].strip : ''

      record = {'surname' => surname, 'forenames' => firstname, 'title' => title, 'born' => born, 'died' => died, 'link' => link}
      ScraperWiki.save(['link'], record)
    end
  end
end
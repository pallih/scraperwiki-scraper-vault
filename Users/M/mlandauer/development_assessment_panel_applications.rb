require "open-uri"
require 'nokogiri'
require "scrapers/ruby_pdf_helper"

info_url = "http://daps.planning.wa.gov.au/8.asp"
url = "http://daps.planning.wa.gov.au/data/current%20dap%20applications/Current%20DAP%20Application.pdf"

doc = Nokogiri::XML(PdfHelper.pdftoxml(open(url) {|f| f.read}))

doc.search('page').each do |p|
  PdfHelper.extract_table_from_pdf_text(p.search('text[font="1"]')).each do |row|
    record = {
      "council_reference" => row[0],
      "description" => row[4].gsub("\n", ""),
      "address" => row[5] + ", WA",
      "date_scraped" => Date.today.to_s,
      "info_url" => info_url,
      "comment_url" => info_url,
    }
    record["date_received"] = Date.strptime(row[7].strip, "%d/%m/%Y").to_s if row[7]

    if (ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? rescue true)
      ScraperWiki.save_sqlite(['council_reference'], record)
    else
      puts "Skipping already saved record " + record['council_reference']
    end
  end
end
require "open-uri"
require 'nokogiri'
require "scrapers/ruby_pdf_helper"

info_url = "http://daps.planning.wa.gov.au/8.asp"
url = "http://daps.planning.wa.gov.au/data/current%20dap%20applications/Current%20DAP%20Application.pdf"

doc = Nokogiri::XML(PdfHelper.pdftoxml(open(url) {|f| f.read}))

doc.search('page').each do |p|
  PdfHelper.extract_table_from_pdf_text(p.search('text[font="1"]')).each do |row|
    record = {
      "council_reference" => row[0],
      "description" => row[4].gsub("\n", ""),
      "address" => row[5] + ", WA",
      "date_scraped" => Date.today.to_s,
      "info_url" => info_url,
      "comment_url" => info_url,
    }
    record["date_received"] = Date.strptime(row[7].strip, "%d/%m/%Y").to_s if row[7]

    if (ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? rescue true)
      ScraperWiki.save_sqlite(['council_reference'], record)
    else
      puts "Skipping already saved record " + record['council_reference']
    end
  end
end

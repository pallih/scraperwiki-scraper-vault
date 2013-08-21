require "mechanize"
require "scrapers/ruby_pdf_helper"

info_url = "http://www.cityofperth.wa.gov.au/web/Business/Building-and-Development-Applications-Received/"

def clean_whitespace(a)
  a.gsub("\n", " ").squeeze(" ").strip
end

def extract_applications_from_pdf(content, info_url)
  info_url = "http://www.cityofperth.wa.gov.au/web/Business/Building-and-Development-Applications-Received/"

  doc = Nokogiri::XML(PdfHelper.pdftoxml(content))
  doc.search('page').each do |p|
    # Have to hardcode the column extents here because the automated finding doesn't work because
    # some of the text from the different columns overlap each other. Ugh...
    columns = [[92, 342], [343, 585], [645, 696], [726, 775], [825, 882], [908, 911]]
    PdfHelper.extract_table_from_pdf_text(p.search('text[font="2"]'), columns).each do |row|
      record = {
        "date_received" => Date.strptime(row[0].split(" ")[0], "%d/%m/%Y").to_s,
        "address" => clean_whitespace(row[0].split(" ")[1..-1].join(" ")),
        "description" => clean_whitespace(row[1]),
        "council_reference" => row[4].strip,
        "date_scraped" => Date.today.to_s,
        "info_url" => info_url,
        "comment_url" => info_url,
      }
      p record
      #if (ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? rescue true)
      #  ScraperWiki.save_sqlite(['council_reference'], record)
      #else
      #  puts "Skipping already saved record " + record['council_reference']
      #end
    end
  end
end

agent = Mechanize.new
page = agent.get(info_url)

# Only get the 4 most recent week's applications
page.search("a").find_all{|a| a.inner_text =~ /For the period/}[0..3].each do |a|
  page = agent.get(a["href"])
  extract_applications_from_pdf(page.content, info_url)
end

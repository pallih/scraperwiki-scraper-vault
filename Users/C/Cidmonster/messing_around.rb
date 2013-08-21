# Blank Ruby
require 'nokogiri' doc = Nokogiri::HTML(html) for v in doc.search("div[@align='left'] tr.tcont") cells = v.search('td') data = { 'country' => cells[0].inner_html, 'years_in_school' => cells[4].inner_html.to_i } puts data.to_json end

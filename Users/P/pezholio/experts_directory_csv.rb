#ScraperWiki::httpresponseheader('Content-Type', 'text/csv')
require 'csv'

ScraperWiki::attach("university_of_warwick_experts_directory")
 
academics = ScraperWiki::select("* from academics")

csv = CSV.generate do |csv|
  csv << ["Area", "Academic Name"]
  academics.each do |academic|
    areas = ScraperWiki::select("* from academicstoareas where academicid = '#{academic['id']}'") 
    areas.each do |area|
      csv << [area['area'], academic['name']]
    end
  end 
end

puts csv



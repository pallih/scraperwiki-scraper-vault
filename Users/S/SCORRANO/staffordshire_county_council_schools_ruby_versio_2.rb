require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'

BASE_URL = "http://education.staffordshire.gov.uk/Directories/SchoolDirectory/"

url = "http://education.staffordshire.gov.uk/Directories/SchoolDirectory/Search.aspx?txtName=&txtArea=&lstSchoolType=All&lstDistricts=All&txtPostcode=&recordCount=458&pageId=0"

doc = Nokogiri.HTML(open(url))

panel = doc.search('#Panel1 > table h3')[0].inner_text

pages = panel.split("of")[1].to_i

pages.times do |i|
  
  doc = Nokogiri.HTML(open("http://education.staffordshire.gov.uk/Directories/SchoolDirectory/Search.aspx?txtName=&txtArea=&lstSchoolType=All&lstDistricts=All&txtPostcode=&recordCount=458&pageId=#{i + 1}"))

  rows = doc.search('tr.topicRow')

  rows.each do |row|
    link = row.search('a')[0]
    
    school = {}
    
    school[:name] = link.inner_text
    school[:url] = BASE_URL + link[:href]
    school[:district] = row.search('td')[2].inner_text.strip
    
    doc = Nokogiri.HTML(open(school[:url]))

    details_hash = doc.search('#tblDetails tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text.strip if tr.search('td').count > 1;hsh}
    puts details_hash

    if details_hash["WWW Address"] == "Add your Schools Web site by clicking this link!"
      details_hash["WWW Address"] = nil
    end

    school[:dfes] = details_hash["DfES Number"]
    school[:address1] = details_hash["Address (Line 1)"] rescue nil
    school[:address2] = details_hash["Address (Line 2)"] rescue nil
    school[:address3] = details_hash["Address (Line 3)"] rescue nil
    school[:town] = details_hash["Town"] rescue nil
    school[:postcode] = details_hash["Post Code"] rescue nil
    school[:tel] = details_hash["Telephone"] rescue nil
    school[:fax] = details_hash["Fax"] rescue nil
    school[:web] = details_hash["WWW Address"] rescue nil
    school[:email] = details_hash["E-Mail"] rescue nil
    school[:type] = details_hash["School Type"] rescue nil
    school[:headteacher] = details_hash["Head Teacher"] rescue nil

    easting = doc.search('#MapControl1_hidCentreEasting')[0][:value] rescue nil
    northing = doc.search('#MapControl1_hidCentreNorthing')[0][:value] rescue nil

    unless easting.nil? 
      json = JSON.parse(open("http://www.uk-postcodes.com/eastingnorthing.php?easting=#{easting}&northing=#{northing}").string)
end
end
endrequire 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'

BASE_URL = "http://education.staffordshire.gov.uk/Directories/SchoolDirectory/"

url = "http://education.staffordshire.gov.uk/Directories/SchoolDirectory/Search.aspx?txtName=&txtArea=&lstSchoolType=All&lstDistricts=All&txtPostcode=&recordCount=458&pageId=0"

doc = Nokogiri.HTML(open(url))

panel = doc.search('#Panel1 > table h3')[0].inner_text

pages = panel.split("of")[1].to_i

pages.times do |i|
  
  doc = Nokogiri.HTML(open("http://education.staffordshire.gov.uk/Directories/SchoolDirectory/Search.aspx?txtName=&txtArea=&lstSchoolType=All&lstDistricts=All&txtPostcode=&recordCount=458&pageId=#{i + 1}"))

  rows = doc.search('tr.topicRow')

  rows.each do |row|
    link = row.search('a')[0]
    
    school = {}
    
    school[:name] = link.inner_text
    school[:url] = BASE_URL + link[:href]
    school[:district] = row.search('td')[2].inner_text.strip
    
    doc = Nokogiri.HTML(open(school[:url]))

    details_hash = doc.search('#tblDetails tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text.strip if tr.search('td').count > 1;hsh}
    puts details_hash

    if details_hash["WWW Address"] == "Add your Schools Web site by clicking this link!"
      details_hash["WWW Address"] = nil
    end

    school[:dfes] = details_hash["DfES Number"]
    school[:address1] = details_hash["Address (Line 1)"] rescue nil
    school[:address2] = details_hash["Address (Line 2)"] rescue nil
    school[:address3] = details_hash["Address (Line 3)"] rescue nil
    school[:town] = details_hash["Town"] rescue nil
    school[:postcode] = details_hash["Post Code"] rescue nil
    school[:tel] = details_hash["Telephone"] rescue nil
    school[:fax] = details_hash["Fax"] rescue nil
    school[:web] = details_hash["WWW Address"] rescue nil
    school[:email] = details_hash["E-Mail"] rescue nil
    school[:type] = details_hash["School Type"] rescue nil
    school[:headteacher] = details_hash["Head Teacher"] rescue nil

    easting = doc.search('#MapControl1_hidCentreEasting')[0][:value] rescue nil
    northing = doc.search('#MapControl1_hidCentreNorthing')[0][:value] rescue nil

    unless easting.nil? 
      json = JSON.parse(open("http://www.uk-postcodes.com/eastingnorthing.php?easting=#{easting}&northing=#{northing}").string)
end
end
end
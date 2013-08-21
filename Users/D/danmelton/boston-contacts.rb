# work in progress...

require 'open-uri'
require 'nokogiri'
require 'net/http'
require 'uri'


def formData(departmentId)
  getRequest = ScraperWiki.scrape('http://www.cityofboston.gov/contact/')
  doc = Nokogiri::HTML.parse(getRequest)
  departments = []
  viewstate, eventvalidation = doc.css("#__VIEWSTATE")[0].attributes["value"].value, doc.css("#__EVENTVALIDATION")[0].attributes["value"].value
  doc.css("select[name='#{departmentId}']").each do |select|
    departments = select.css("option").map do |option|
      {
        "id" => option.attributes["value"].value,
        "name" => option.text,
        "viewstate"=> viewstate,
        "eventvalidation"=> eventvalidation
      }
    end
  end 
  departments
end

departmentIds = ["ctl00$ContentPlaceHolder1$DDLCityCounc", "ctl00$ContentPlaceHolder1$DDLDeptHead","ctl00$ContentPlaceHolder1$DDLDepartments", "ctl00$ContentPlaceHolder1$DDLLiasion"]


departmentIds.each do |departmentId|
  
  departments = formData(departmentId)
  departments.each do |department|
    if department["id"]!="0"
    url = URI.parse('http://www.cityofboston.gov/contact/default.aspx')
    postRequest = Net::HTTP::Post.new(url.path)
    postRequest.set_form_data({  
      "_EVENTTARGET" => "",
      "__EVENTARGUMENT" => "",
      "__LASTFOCUS" => "",
      "__VIEWSTATE" => department["viewstate"],
      "__EVENTVALIDATION" => department["eventvalidation"],
      "#{departmentId}" => department["id"]
    })

    response = Net::HTTP.new(url.host, url.port).start {|http| http.request(postRequest)}
    doc = Nokogiri::HTML.parse(response.body)
    
    contact = doc.css("#ctl00_ContentPlaceHolder1_LblDirector").inner_html.gsub('<b>', '').gsub('</b>', '') unless doc.css("#ctl00_ContentPlaceHolder1_LblDirector").nil? 
    dept = doc.css("#ctl00_ContentPlaceHolder1_LblDeptName").inner_html.gsub('<b>', '').gsub('</b>', '') unless doc.css("#ctl00_ContentPlaceHolder1_LblDeptName").nil? 
    address = doc.css("#ctl00_ContentPlaceHolder1_LblAdd1").inner_html.gsub('<br>', ' ') unless doc.css("#ctl00_ContentPlaceHolder1_LblAdd1").inner_html.nil? 
    phone = doc.css("#ctl00_ContentPlaceHolder1_LblPH").inner_html.gsub('<b>Telephone:</b>','') unless doc.css("#ctl00_ContentPlaceHolder1_LblPH").nil? 
    fax = doc.css("#ctl00_ContentPlaceHolder1_LblFx").inner_html.gsub('<b>Facsimile:</b>','') unless doc.css("#ctl00_ContentPlaceHolder1_LblFx").nil? 
    durl = doc.at_css("#ctl00_ContentPlaceHolder1_LblURL a").attributes["href"].value unless doc.at_css("#ctl00_ContentPlaceHolder1_LblURL a").nil? 
    email = doc.at_css("#ctl00_ContentPlaceHolder1_LblEmail a").attributes["href"].value.gsub('mailto:', '') unless doc.at_css("#ctl00_ContentPlaceHolder1_LblEmail a").nil? 

    record = {"organization" => dept, "contact" => contact, "address" => address, "phone" => phone, "fax" => fax, "url" => durl, "email" => email }

    ScraperWiki.save(['organization'], record)
    end
  end
#end the departments run
  end
#end the contact areas run



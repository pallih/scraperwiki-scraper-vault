require "rubygems"
require "nokogiri"

ScraperWiki.attach("sourcewell_applications", "src_app")
ScraperWiki.attach("sourcewell_announcements_1", "src_ann")

apps = ScraperWiki.select("* from src_app.swdata")
all_announcements = Hash.new{ |h,k| h[k] = [] }
ScraperWiki.select("* from src_ann.swdata").each do |announcement|
  all_announcements[announcement["appid"].to_i] << announcement
end

xml = Nokogiri::XML::Document.new
xml.root = xml.create_element("sourcewell-apps")
apps.select do |fields|
  not fields["downloaded-on"].to_s.strip.empty? 
end.sort_by do |fields|
  fields["application-id"].to_i
end.each do |fields|
  xml.root << app = xml.create_element("app")

  app["id"] = fields["application-id"]
  app["downloaded-on"] = fields["downloaded-on"]

  fields.delete("downloaded-on")
  fields.each do |field_name, field_value|
    if field_name == "description"
      app << parent = xml.create_element(field_name)
      parent << Nokogiri::XML::DocumentFragment.parse(field_value)
    else
      app << xml.create_element(field_name, field_value)
    end
  end

  app << announcements = xml.create_element("announcements")
  all_announcements[fields["application-id"].to_i].sort_by do |ann_data|
    ann_data["timestamp"]
  end.each do |ann_data|
    announcements << ann = xml.create_element("announcement", ann_data["version"])
    ann["timestamp"] = ann_data["timestamp"]+"Z"
  end
end

ScraperWiki.httpresponseheader("Content-Type", "application/xml")
puts xml

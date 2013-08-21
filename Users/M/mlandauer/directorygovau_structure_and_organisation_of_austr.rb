require 'open-uri'
require 'nokogiri'

# Download Directory.gov.au full data export from data.gov.au
doc = Nokogiri::XML(open("http://data.gov.au/bye?http://datasets.data.gov.au/directoryexport.xml"))

#doc.search('organization').each do |org|
#  simple_tags = ["name", "text", "website", "acronym", "location", "phone", "keyword", "mail"]
#  valid_child_tags = simple_tags + ["organizationalUnit", "organization", "person"]
#  record = {
#    uuid: org["UUID"],
#  }
#  simple_tags.each do |tag|
#    record[tag.to_sym] = org.at(tag).inner_html if org.at(tag)
#  end
#  child_tags = org.children.map{|c| c.name}
#  unexpected_child_tags = child_tags - valid_child_tags
#  unless unexpected_child_tags.empty? 
#    raise "Unexpected child tags #{unexpected_child_tags.join(', ')}"
#  end
#  #p record
#end

#unexpected_child_tags = []
#doc.search('organizationalUnit').each do |org|
#  simple_tags = ["name", "text", "mediaReleases", "description", "location", "website", "postalAddress", "phone", "fax", "keyword", "mail", "afterHoursPhone", "acronym", "tty", "tollFreePhone", "comment", "seeAlso", "publications", "annualReport", "informationPublicationScheme"]
#  valid_child_tags = simple_tags + ["organizationalUnit", "role", "person", "subject"]
#  record = {
#    uuid: org["UUID"],
#  }
#  simple_tags.each do |tag|
#    record[tag.to_sym] = org.at(tag).inner_html if org.at(tag)
#  end
#  child_tags = org.children.map{|c| c.name}
#  unexpected_child_tags += child_tags - valid_child_tags
#  if org.parent.name == "organization"
#    record[:organization_parent_uuid] = org.parent["UUID"]
#  elsif org.parent.name == "organizationalUnit"
#    record[:organizational_unit_parent_uuid] = org.parent["UUID"]
#  else
#    raise "Unexpected parent tag: #{org.parent.name}"
#  end
#  record[:parent_name] = org.parent.at('name').inner_html
#  ScraperWiki::save_sqlite(["uuid"], record, "organizational_unit")
#end
#unless unexpected_child_tags.empty? 
#  raise "Unexpected child tags #{unexpected_child_tags.uniq.join(', ')}"
#end

def visit_node(node)
  case node.name
  when "document", "directoryExport"
    node.children.each {|c| visit_node(c)}
  when "organization"
    visit_organization(node)
  when "text"
  else
    raise "Unexpected node #{node.name}"
  end
end

def visit_organization(node)
  #puts "Organization: #{node.at('name').inner_text}"
  expected_children = ["text", "name", "location", "phone", "mail", "website", "acronym", "keyword", "person", "organization", "organizationalUnit"]
  unexpected_children = node.children.map{|c| c.name} - expected_children
  raise "Unexpected nodes #{unexpected_children.uniq.join(', ')}" unless unexpected_children.empty? 
  node.children.each do |c|
    case c.name
    when "organization"
      visit_organization(c)
    when "organizationalUnit"
      visit_organizational_unit(c)
    end
  end
end

def visit_organizational_unit(node)
  record = {}
  simple_tags = ["name", "description", "mediaReleases", "location", "website", "postalAddress", "phone", "fax", "comment", "mail","acronym", "publications", "tollFreePhone", "tty", "annualReport", "informationPublicationScheme", "seeAlso", "afterHoursPhone"]
  expected_children = simple_tags + ["text", "organizationalUnit", "role", "keyword", "person", "subject"]
  unexpected_children = node.children.map{|c| c.name} - expected_children
  raise "Unexpected nodes #{unexpected_children.uniq.join(', ')}" unless unexpected_children.empty? 
  node.children.each do |c|
    if simple_tags.include?(c.name)
      record[c.name.to_sym] = c.inner_text
    end
  end
  if record.count == 1 && record.has_key?(:name)
    # This is not a department yet. Look deeper
    node.children.each do |c|
      if c.name == "organizationalUnit"
        visit_organizational_unit(c)
      end
    end
  else
    ScraperWiki::save_sqlite(["name"], record)
  end
end

visit_node(doc)
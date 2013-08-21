require "rubygems"
require "nokogiri"

$ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')

class SourceWell
  def get_app(app_id)
    response = ScraperWiki.scrape("http://sourcewell.berlios.de/appbyid.php?id=#{ app_id }&SourceWell_Session=1")
    if response and not response=~/Application \(ID: [0-9]+\) does not exist./
      # http://po-ru.com/diary/fixing-invalid-utf-8-in-ruby-revisited/
      response = $ic.iconv(response + ' ')[0..-2]

      html = Nokogiri::HTML(response)
      data_table = html.at_xpath("//table//table//table//table")
      
      fields = []
      fields << [ "application-id", app_id.to_s ]

      version = data_table.at_xpath("//tr/td[b='Version:']/following-sibling::td").content
      title = html.at_xpath("//head/title").content.gsub(/^SourceWell - |#{version}/, "").strip

      fields << [ "title", title ]

      description = data_table.xpath("./preceding-sibling::p[not(b[@class='small']) and (normalize-space(.) or *)]")
      fields << [ "description", description.to_xml ]

      data_table.xpath(".//tr").each do |tr|
        tds = tr.xpath("td")
        field_name = tds[0].content.strip
        field_value = tds[1].content.strip
        link = tds[1].at_xpath("a")

        case field_name
          when "Announcements:", "Share:", "Others by Author:", "Application ID:"
            # skip

          when "License:"
            fields << [ "license",     link.content ]
            fields << [ "license-url", link["href"] ]

          when "Section/Category:"
            section, category = field_value.split("/")
            fields << [ "section",  section ]
            fields << [ "category", category ]

          when "Depends on:"
            unless field_value.empty? 
              field_value.split(",").each do |depend|
                fields << [ "depends-on", depend.strip ]
              end
            end

          when "Author:"
            unless field_value.empty? 
              fields << [ "author", field_value.gsub(/<.+>/, "").strip ]
              if link
                fields << [ "author-email", link.content.gsub(" at ", "@").gsub(" dot ", ".") ]
              end
            end

          else
            field_name = field_name.downcase.delete(":").strip.squeeze(" ").gsub(/[^A-Za-z]/, "-")
            if link
              fields << [ "#{ field_name }-url", link.content ]
            else
              fields << [ field_name, field_value ]
            end
        end
      end

      fields
    else
      nil
    end
  rescue
    puts "#{app_id} #{$!.inspect}"
    nil
  end
end

sw = SourceWell.new
last_complete_app_id = ScraperWiki.get_var("last-complete-app-id", 0).to_i
app_id = last_complete_app_id
requested = 0
while requested < 3000
  app_id += 1
  if fields = sw.get_app(app_id)
    fields << [ "downloaded-on", Time.now.utc.xmlschema ]
    ScraperWiki.save_sqlite(["application-id"], Hash[fields])
  else
    ScraperWiki.save_sqlite(["application-id"], { "application-id"=>app_id.to_s })
  end
  ScraperWiki.save_var("last-complete-app-id", app_id)
  app_id = 0 if app_id >= 5800
  requested += 1
end
ScraperWiki.save_var("last-complete-app-id", app_id)


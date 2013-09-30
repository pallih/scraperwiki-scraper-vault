require 'nokogiri'

commons_url = "http://www.parliament.uk/about/faqs/house-of-commons-faqs/business-faq-page/recess-dates/recess/"
lords_url = "http://www.parliament.uk/about/faqs/house-of-lords-faqs/lords-recess-dates/"

def scrape_data(url, house)
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  parent = doc.xpath("//div[@id='ctl00_ctl00_SiteSpecificPlaceholder_PageContent_ctlMainBody_wrapperDiv']")


  prev_label = ""

  session = {}

  parent.children.each do |node|
    case node.name
      when "h2"
        if house == "Commons"
          puts "Session: " + node.text.gsub("Recess dates ", "")
          unless session.empty? 
            #write out previous data
            if session["prorogation"]
              record = {'house' => house, 'name' => session["name"], 'begin' => session["state_opening"], 'end' => session["prorogation"]}
            else
              record = {'house' => house, 'name' => session["name"], 'begin' => session["state_opening"], 'end' => session["dissolution"]}
            end
            ScraperWiki.save(['name', 'house'], record)
            session = {}
          end
          session["name"] = node.text.gsub("Recess dates ", "").gsub("\r","").gsub("\n","")
        end
      when "h3"
        puts "Session: " + node.text.gsub("Recess dates ", "")
        unless session.empty? 
          #write out previous data
          if session["prorogation"]
            record = {'house' => house, 'name' => session["name"], 'begin' => session["state_opening"], 'end' => session["prorogation"]}
          elsif session["dissolution"]
            record = {'house' => house, 'name' => session["name"], 'begin' => session["state_opening"], 'end' => session["dissolution"]}
          else
            session = {}
          end
          ScraperWiki.save(['name', 'house'], record) unless session.empty? 
          session = {}
        end
        session["name"] = node.text.gsub("Recess dates ", "").gsub("\r","").gsub("\n","")
      when "p"
        node.children.each do |sub|
          if sub.name == "a"
            case sub.text.strip
              when /State Opening/
                prev_label = "state_opening"
              when /Prorogation/
                prev_label = "prorogation"
              when /Dissolution/
                prev_label = "dissolution"
            end
          else
            unless prev_label == ""
              break if sub.text.strip == "." or sub.text =~ /Further information/
              puts prev_label + " - " + sub.text.gsub(":","").strip
              session[prev_label] = sub.text.gsub(":","").gsub("\xC2\xA0", " ").strip
              prev_label = ""
            end
          end
        end
    end
  end
end

scrape_data(commons_url, 'Commons')
scrape_data(lords_url, 'Lords')
require 'nokogiri'

commons_url = "http://www.parliament.uk/about/faqs/house-of-commons-faqs/business-faq-page/recess-dates/recess/"
lords_url = "http://www.parliament.uk/about/faqs/house-of-lords-faqs/lords-recess-dates/"

def scrape_data(url, house)
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  parent = doc.xpath("//div[@id='ctl00_ctl00_SiteSpecificPlaceholder_PageContent_ctlMainBody_wrapperDiv']")


  prev_label = ""

  session = {}

  parent.children.each do |node|
    case node.name
      when "h2"
        if house == "Commons"
          puts "Session: " + node.text.gsub("Recess dates ", "")
          unless session.empty? 
            #write out previous data
            if session["prorogation"]
              record = {'house' => house, 'name' => session["name"], 'begin' => session["state_opening"], 'end' => session["prorogation"]}
            else
              record = {'house' => house, 'name' => session["name"], 'begin' => session["state_opening"], 'end' => session["dissolution"]}
            end
            ScraperWiki.save(['name', 'house'], record)
            session = {}
          end
          session["name"] = node.text.gsub("Recess dates ", "").gsub("\r","").gsub("\n","")
        end
      when "h3"
        puts "Session: " + node.text.gsub("Recess dates ", "")
        unless session.empty? 
          #write out previous data
          if session["prorogation"]
            record = {'house' => house, 'name' => session["name"], 'begin' => session["state_opening"], 'end' => session["prorogation"]}
          elsif session["dissolution"]
            record = {'house' => house, 'name' => session["name"], 'begin' => session["state_opening"], 'end' => session["dissolution"]}
          else
            session = {}
          end
          ScraperWiki.save(['name', 'house'], record) unless session.empty? 
          session = {}
        end
        session["name"] = node.text.gsub("Recess dates ", "").gsub("\r","").gsub("\n","")
      when "p"
        node.children.each do |sub|
          if sub.name == "a"
            case sub.text.strip
              when /State Opening/
                prev_label = "state_opening"
              when /Prorogation/
                prev_label = "prorogation"
              when /Dissolution/
                prev_label = "dissolution"
            end
          else
            unless prev_label == ""
              break if sub.text.strip == "." or sub.text =~ /Further information/
              puts prev_label + " - " + sub.text.gsub(":","").strip
              session[prev_label] = sub.text.gsub(":","").gsub("\xC2\xA0", " ").strip
              prev_label = ""
            end
          end
        end
    end
  end
end

scrape_data(commons_url, 'Commons')
scrape_data(lords_url, 'Lords')

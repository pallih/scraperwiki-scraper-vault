require 'mechanize'
require 'nokogiri'

def initial_page

begin
    
    agent = Mechanize.new
    agent.get("http://www.secureaustralia.org.au/index.php/search/index#")
    @page = agent.page
    

    rescue Timeout::Error
    retry
    rescue => e
    puts e.class
    retry
    end

end






def send_form
    begin

    @response = @page.forms.last.submit
    
    rescue Timeout::Error
    retry
    rescue => e
    puts e.class
    retry
    end
end


def get_links
    @links_list = @response.links.map {|link| link.href}
    puts @links_list.length
end






def scrape_page

    @links_list.each do |link|
          begin

        @record = {}


        agent = Mechanize.new
        agent.get(link.to_s)
        @contact_name = ''
        @contact_name = Nokogiri::HTML(agent.page.body).xpath("//div[@id='main']/div[@class='person']/h1").inner_text.strip
      puts @contact_name
      names = @contact_name.split(' ').collect {|n| n.to_s}
      puts names

      @record['contact_title']  =  names.first.strip
      @record['contact_lastname']  =  names.last.strip
      @record['contact_firstname']  =  names[1].strip
      @record['contact_middlename']  =  names[2..(names.length-2)].join(' ').strip
      @record['contact_type']  =  "National Security Researcher"

      


      @record['contact_activity']  =  Nokogiri::HTML(agent.page.body).xpath("//div[@id='main']/div[@class='person']//li").map {|i| i.inner_text.strip}
      @record['contact_activity'] = @record['contact_activity'].join("\n")


        #@record['Link'] = link.strip
        #@record['Research_Areas'] = Nokogiri::HTML(agent.page.body).xpath("//div[@id='main']/div[@class='person']/ul").inner_text.strip
        
        
        data_table = Nokogiri::HTML(agent.page.body).css('tr').collect do |row|
            text = ''
            text = row.css('td[1]').inner_text.strip.gsub(/[(-,?!\'":.)]/, '').gsub(/\s/,'_')
            #puts text
            result = ''
            result =  row.css('td[2]').inner_text.strip




case text

when "City"
@record['contact_city']  =  result

when "Personal_Webpage"
@record['contact_website']  =  result

when "Phone"
@record['contact_phone']  =  result

when "State"
@record['contact_state']  =  result

when "Link"
@record['contact_comments']  =  result


when "Postcode"
@record['contact_zip_code']  =  result


when "Address"
@record['contact_address']  =  result


when "Position"
@record['contact_job_title']  =  result


when "Email"
@record['contact_email']  =  result

when "Organisation"
@record['contact_company']  = result

when "Sub-organisation"
@record['contact_department']  =  result

when "Mobile"
@record['contact_phone_mobile']  =  result



end


            #puts @record.keys     #["'#{text}'"].key

        end
        
        
        puts @record
        ScraperWiki.save(['contact_email'], @record)



            rescue Timeout::Error
            retry
            rescue => e
            puts e.class
            puts e
             retry
            end
     end
        
end
    
    
    
    initial_page
    send_form
    get_links
    scrape_page
    
    
    
    
    
    require 'mechanize'
require 'nokogiri'

def initial_page

begin
    
    agent = Mechanize.new
    agent.get("http://www.secureaustralia.org.au/index.php/search/index#")
    @page = agent.page
    

    rescue Timeout::Error
    retry
    rescue => e
    puts e.class
    retry
    end

end






def send_form
    begin

    @response = @page.forms.last.submit
    
    rescue Timeout::Error
    retry
    rescue => e
    puts e.class
    retry
    end
end


def get_links
    @links_list = @response.links.map {|link| link.href}
    puts @links_list.length
end






def scrape_page

    @links_list.each do |link|
          begin

        @record = {}


        agent = Mechanize.new
        agent.get(link.to_s)
        @contact_name = ''
        @contact_name = Nokogiri::HTML(agent.page.body).xpath("//div[@id='main']/div[@class='person']/h1").inner_text.strip
      puts @contact_name
      names = @contact_name.split(' ').collect {|n| n.to_s}
      puts names

      @record['contact_title']  =  names.first.strip
      @record['contact_lastname']  =  names.last.strip
      @record['contact_firstname']  =  names[1].strip
      @record['contact_middlename']  =  names[2..(names.length-2)].join(' ').strip
      @record['contact_type']  =  "National Security Researcher"

      


      @record['contact_activity']  =  Nokogiri::HTML(agent.page.body).xpath("//div[@id='main']/div[@class='person']//li").map {|i| i.inner_text.strip}
      @record['contact_activity'] = @record['contact_activity'].join("\n")


        #@record['Link'] = link.strip
        #@record['Research_Areas'] = Nokogiri::HTML(agent.page.body).xpath("//div[@id='main']/div[@class='person']/ul").inner_text.strip
        
        
        data_table = Nokogiri::HTML(agent.page.body).css('tr').collect do |row|
            text = ''
            text = row.css('td[1]').inner_text.strip.gsub(/[(-,?!\'":.)]/, '').gsub(/\s/,'_')
            #puts text
            result = ''
            result =  row.css('td[2]').inner_text.strip




case text

when "City"
@record['contact_city']  =  result

when "Personal_Webpage"
@record['contact_website']  =  result

when "Phone"
@record['contact_phone']  =  result

when "State"
@record['contact_state']  =  result

when "Link"
@record['contact_comments']  =  result


when "Postcode"
@record['contact_zip_code']  =  result


when "Address"
@record['contact_address']  =  result


when "Position"
@record['contact_job_title']  =  result


when "Email"
@record['contact_email']  =  result

when "Organisation"
@record['contact_company']  = result

when "Sub-organisation"
@record['contact_department']  =  result

when "Mobile"
@record['contact_phone_mobile']  =  result



end


            #puts @record.keys     #["'#{text}'"].key

        end
        
        
        puts @record
        ScraperWiki.save(['contact_email'], @record)



            rescue Timeout::Error
            retry
            rescue => e
            puts e.class
            puts e
             retry
            end
     end
        
end
    
    
    
    initial_page
    send_form
    get_links
    scrape_page
    
    
    
    
    
    
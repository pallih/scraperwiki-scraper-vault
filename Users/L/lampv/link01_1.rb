require 'scraper'

class ACTScraper < Scraper
  def applications(date)
    url = "http://www.actpla.act.gov.au/topics/your_say/comment/pubnote"
    page = agent.get(url)
    # The way that Mechanize is invoking Nokogiri for parsing the html is for some reason not working with this html which
    # is malformed: See http://validator.w3.org/check?uri=http://apps.actpla.act.gov.au/pubnote/index.asp&charset=(detect+automatically)&doctype=Inline&group=0
    # It's chopping out the content that we're interested in. So, doing the parsing explicitly so we can control how it's done.
    page = Nokogiri::HTML(page.body)
    
    # Walking through the lines. Every 7 lines is a new application
    applications = []
    page.search('table')[1].search('tr').each_slice(7) do |lines|
      # First double check that each line has the correct form
      labels = lines.map do |line|
        if line.at('strong')
          line.at('strong').inner_text
        elsif line.at('b')
          line.at('b').inner_text
        end
      end
      
      raise "Unexpected form for suburb line" unless lines[0].at('a').has_attribute?('name')
      raise "Unexpected form application_id line" unless labels[1] == "Development Application:"
      raise "Unexpected form address line" unless labels[2] == "Address:"
      raise "Unexpected form block line" unless labels[3] == "Block: "
      raise "Unexpected form description line" unless labels[4] == "Proposal:"
      raise "Unexpected form on notice to line" unless labels[5] == "Period for representations closes:"
      raise "Unexpected form info url line" unless lines[6].at('a').inner_text == "Click here to view the plans"
      
      lines[1].at('strong').remove
      lines[2].at('strong').remove
      lines[4].at('strong').remove
      lines[5].at('strong').remove
      stripped = lines.map{|l| l.inner_text.strip}

      applications << DevelopmentApplication.new(
        :application_id => stripped[1],
        :address => stripped[2] + ", " + stripped[0] + ", " + state,
        :description => stripped[4],
        :on_notice_to => (stripped[5] if stripped[5] != ""),
        :info_url => extract_relative_url(lines[6]),
        :comment_url => url)
    end
    applications
  end
end
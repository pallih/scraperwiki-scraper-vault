require 'nokogiri'
require 'scraperwiki'
require 'scrapers/gasp_helper_rb'

class Scraper
  include GASP::Helper
  include GASP::Utils

  @@base_url = 'http://www.roberts.senate.gov/public/index.cfm'

  def scrape_biography
    html = ScraperWiki.scrape("#{@@base_url}?p=Biography")
    doc = Nokogiri::HTML(html)
    bio_paras = doc.css('#copy p').collect {|p| p.text }
    bio_pic = doc.css('#copy img').first.attr('src').to_s rescue nil
    bio = bio_paras.join "\n\n"

    add_biography bio, {:image => bio_pic}
  end

  def scrape_issues
    html = ScraperWiki.scrape("#{@@base_url}?p=IssueStatements")
    doc = Nokogiri::HTML(html)
    issues = {}
    doc.css('.actionsList h4 a').each {|issue| issues[issue.text.to_sym] = issue.attr('href') }
    issues.each do |issue, url|
      url = "#{@@base_url}#{url}" if !(url =~ /https?\:\/\//)
        issue_page = ScraperWiki.scrape(url)
        issue_doc = Nokogiri::HTML(issue_page)
        content = issue_doc.css('.textList').inner_html.gsub(/<br ?\/?>/, "\n\n")
        content = Nokogiri::HTML(content).text.strip
        if content.empty? 
          content = issue_doc.css('.textList p').collect {|p| p.text.strip }
          content = content.join "\n\n"
        end
        if content.empty?
          content = issue_doc.css('#copy div').collect {|p| p.text.strip }
          content = content.join "\n\n"
        end
        if content.empty?
          raise 'issue scraper failed!'
        end

        add_issue issue.to_s, content
      end
    end

    def scrape_offices
      html = ScraperWiki.scrape("#{@@base_url}?p=OfficeLocations")
      doc = Nokogiri::HTML(html).css('#copy').inner_html.split(/<iframe[^<]*<\/iframe>/)[1]
      offices = doc.split(/<h3[^<]*<\/h3>/).collect{|office| (office = office.strip.sub(/^<br ?\/?>/, '')).empty? ? nil : office}.compact
      offices.each do |office|
        address, phone, fax, staff = office.split(/(?:phone\:|fax\:|staff\:)/i)
        extra = {}
        address_lines = (address.strip.split(/<br ?\/?>/).collect {|line| line.empty? ? nil : line}).compact
        address_lines.collect! do |line|
          line = Nokogiri::HTML(line)
          img = line.css('img')
          if img.any?
            extra['image'] = img.first.attr('src')
            nil
          elsif line.text.strip.empty?
            nil
          else
            line.text.strip
          end
        end.compact
        phone = format_phone_for Nokogiri::HTML(phone).text
        fax = format_phone_for Nokogiri::HTML(fax).text

        add_office address_lines.join("\n"), phone, fax, extra
      end
    end

    def scrape_press_releases
      urls = parse_linklist "#{@@base_url}?p=PressReleases", ".recordListTitle a.ContentGrid"
      urls.each do |url|
        title, date, content = scrape_bloggy_content url
        add_press_release title, date, content
      end
    end

    def scrape_speeches
      urls = parse_linklist "#{@@base_url}?p=Speeches", ".recordListTitle a.ContentGrid"
      urls.each do |url|
        title, date, content = scrape_bloggy_content url
        add_other_post title, date, content, {:type => 'speech'}
      end
    end

    def scrape_columns
      urls = parse_linklist "#{@@base_url}?p=MonthlyColumns", ".recordListTitle a.ContentGrid"
      urls.each do |url|
        title, date, content = scrape_bloggy_content url, :title => '.contentrecord h2'
        add_other_post title, date, content, {:type => 'column'}
      end
    end

    def scrape_audio
      
    end

    def scrape_video

    end

    def scrape_photos
      
    end

    def scrape_newsletters
      urls = parse_linklist "#{@@base_url}?p=NewsletterArchive", ".recordListTitle a.ContentGrid"
      urls.each do |url|
        title, date, content = scrape_bloggy_content url
        add_news_update title, date, content
      end
    end

    def scrape_journal
    end

    def scrape_social_media
    end

    def run
      #scrape_biography
      #scrape_issues
      #scrape_offices
      scrape_press_releases
      scrape_columns
      scrape_newsletters
      # finish
    end

    private

    def scrape_bloggy_content(url, params={})
      html = ScraperWiki.scrape(url)
      doc = Nokogiri::HTML(html)
      title = doc.css(params[:title] || 'h1 a').first.text
      date = Time.parse(doc.css(params[:date] || '.contentrecord .date').first.text)
      # content_paras = doc.css(params[:content] || '.content').collect {|para| para.inner_html }
      # content = content_paras.join("\n\n")
      content = doc.css('.content').inner_html

      [title, date, content]
    end

  end

  Scraper.new('b673f984f7884d40a85c587a19fa1be9', 'R000307').run
require 'nokogiri'
require 'scraperwiki'
require 'scrapers/gasp_helper_rb'

class Scraper
  include GASP::Helper
  include GASP::Utils

  @@base_url = 'http://www.roberts.senate.gov/public/index.cfm'

  def scrape_biography
    html = ScraperWiki.scrape("#{@@base_url}?p=Biography")
    doc = Nokogiri::HTML(html)
    bio_paras = doc.css('#copy p').collect {|p| p.text }
    bio_pic = doc.css('#copy img').first.attr('src').to_s rescue nil
    bio = bio_paras.join "\n\n"

    add_biography bio, {:image => bio_pic}
  end

  def scrape_issues
    html = ScraperWiki.scrape("#{@@base_url}?p=IssueStatements")
    doc = Nokogiri::HTML(html)
    issues = {}
    doc.css('.actionsList h4 a').each {|issue| issues[issue.text.to_sym] = issue.attr('href') }
    issues.each do |issue, url|
      url = "#{@@base_url}#{url}" if !(url =~ /https?\:\/\//)
        issue_page = ScraperWiki.scrape(url)
        issue_doc = Nokogiri::HTML(issue_page)
        content = issue_doc.css('.textList').inner_html.gsub(/<br ?\/?>/, "\n\n")
        content = Nokogiri::HTML(content).text.strip
        if content.empty? 
          content = issue_doc.css('.textList p').collect {|p| p.text.strip }
          content = content.join "\n\n"
        end
        if content.empty?
          content = issue_doc.css('#copy div').collect {|p| p.text.strip }
          content = content.join "\n\n"
        end
        if content.empty?
          raise 'issue scraper failed!'
        end

        add_issue issue.to_s, content
      end
    end

    def scrape_offices
      html = ScraperWiki.scrape("#{@@base_url}?p=OfficeLocations")
      doc = Nokogiri::HTML(html).css('#copy').inner_html.split(/<iframe[^<]*<\/iframe>/)[1]
      offices = doc.split(/<h3[^<]*<\/h3>/).collect{|office| (office = office.strip.sub(/^<br ?\/?>/, '')).empty? ? nil : office}.compact
      offices.each do |office|
        address, phone, fax, staff = office.split(/(?:phone\:|fax\:|staff\:)/i)
        extra = {}
        address_lines = (address.strip.split(/<br ?\/?>/).collect {|line| line.empty? ? nil : line}).compact
        address_lines.collect! do |line|
          line = Nokogiri::HTML(line)
          img = line.css('img')
          if img.any?
            extra['image'] = img.first.attr('src')
            nil
          elsif line.text.strip.empty?
            nil
          else
            line.text.strip
          end
        end.compact
        phone = format_phone_for Nokogiri::HTML(phone).text
        fax = format_phone_for Nokogiri::HTML(fax).text

        add_office address_lines.join("\n"), phone, fax, extra
      end
    end

    def scrape_press_releases
      urls = parse_linklist "#{@@base_url}?p=PressReleases", ".recordListTitle a.ContentGrid"
      urls.each do |url|
        title, date, content = scrape_bloggy_content url
        add_press_release title, date, content
      end
    end

    def scrape_speeches
      urls = parse_linklist "#{@@base_url}?p=Speeches", ".recordListTitle a.ContentGrid"
      urls.each do |url|
        title, date, content = scrape_bloggy_content url
        add_other_post title, date, content, {:type => 'speech'}
      end
    end

    def scrape_columns
      urls = parse_linklist "#{@@base_url}?p=MonthlyColumns", ".recordListTitle a.ContentGrid"
      urls.each do |url|
        title, date, content = scrape_bloggy_content url, :title => '.contentrecord h2'
        add_other_post title, date, content, {:type => 'column'}
      end
    end

    def scrape_audio
      
    end

    def scrape_video

    end

    def scrape_photos
      
    end

    def scrape_newsletters
      urls = parse_linklist "#{@@base_url}?p=NewsletterArchive", ".recordListTitle a.ContentGrid"
      urls.each do |url|
        title, date, content = scrape_bloggy_content url
        add_news_update title, date, content
      end
    end

    def scrape_journal
    end

    def scrape_social_media
    end

    def run
      #scrape_biography
      #scrape_issues
      #scrape_offices
      scrape_press_releases
      scrape_columns
      scrape_newsletters
      # finish
    end

    private

    def scrape_bloggy_content(url, params={})
      html = ScraperWiki.scrape(url)
      doc = Nokogiri::HTML(html)
      title = doc.css(params[:title] || 'h1 a').first.text
      date = Time.parse(doc.css(params[:date] || '.contentrecord .date').first.text)
      # content_paras = doc.css(params[:content] || '.content').collect {|para| para.inner_html }
      # content = content_paras.join("\n\n")
      content = doc.css('.content').inner_html

      [title, date, content]
    end

  end

  Scraper.new('b673f984f7884d40a85c587a19fa1be9', 'R000307').run

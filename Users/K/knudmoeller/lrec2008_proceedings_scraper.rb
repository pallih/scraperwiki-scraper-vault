require 'rubygems'
require 'nokogiri'
require 'pp'
require 'open-uri'
require 'uri'
require 'cgi'


class LREC2008Scraper
  
  attr_reader :base, :papers, :authors
  
  def initialize(base)
    @base = base
  end
  
  def run
    
    html_base = "http://www.lrec-conf.org/proceedings/lrec2008/"
    
    pages = []
    overview = Nokogiri::HTML(open("#{@base}/papers.html"))
    
    puts "collecting paper links..."

    # iterate the list of papers
    overview.search("td[@class='paper_papers']").each do |paper_element|
      paper_element.search('a').each do |paper_link|
        pages << "summaries/#{paper_link['href'].match(/[0-9]+?\.html$/)[0]}"
      end
    end
    
    puts "scraping papers..."

    counter = 0
    @papers = []
    # testing with just a few papers:
    pages = pages[0..10]
    pages.each do |page|
      page_code = Nokogiri::HTML(open("#{@base}/#{page}"))
      
      table = page_code.search("table[@class='main_summaries']").first
      
      cell_counter = 0
      keys = []
      values = []
      table.search("td").each do |cell|
        if (cell_counter%2 == 0) 
          keys << cell.inner_text
        else
          values << cell
        end
        cell_counter += 1
      end
      
      cells = Hash[keys.zip(values)]
      
      paper = LRECPaper.new
      
      paper.id = page.match(/([0-9]+?)\.html$/)[1]
      paper.source = "#{html_base}#{page}"
      title = table.search("th[@class='second_summaries']").first.inner_text
      paper.title = title
      paper.abstract = cells["Abstract"].inner_text
      paper.pdf_link = cells["Full paper"].child['href']
      paper.slide_link = cells["Slides"].child['href']
      paper.authors = []
      cells["Authors"].search("a").each do |author|
        paper.authors << author.inner_text
      end
      paper.topics = []
      cells["Topics"].search("a").each do |topic|
        paper.topics << topic.inner_text
      end

      @papers << paper

      if counter.modulo(100) == 0
        print counter.to_s.rjust(8, "_")
        $stdout.flush
      elsif counter.modulo(10) == 0
        print "."
        $stdout.flush
      end

      counter += 1
      
    end
    
    puts
    puts "#{counter} papers scraped"

    # scrape author-affiliation mapping:

    puts "scraping authors ..."
    
    author_doc = Nokogiri::HTML(open("#{@base}/authors.html"))
    author_names = []
    author_affiliations = []
    
    author_doc.search("td[@class='author_authors']").each do |author|
      name = author.inner_text.gsub(/(.*), (.*)/, '\2 \1')
      author_names << name
    end
    
    author_doc.search("td[@class='affiliation_authors']").each do |affiliation|
      affiliation = affiliation.inner_text
      author_affiliations << affiliation
    end
    
    @authors = Hash[author_names.zip(author_affiliations)]

    puts "scraping authors done ..."
  
  end # run()
  
  def export_main_csv
    
    csv = ""
    
    @papers.each do |paper|
      counter = 1
      paper.authors.each do |author|
        csv << "#{paper.id},\"#{paper.title}\",#{counter},\"#{author}\",\"#{@authors[author]}\",#{paper.pdf_link},#{paper.slide_link},#{paper.source}\n"
        counter += 1
      end
    end
    
    return csv
  end # export_csv()
  
  def export_topic_csv
    csv = ""
    
    @papers.each do |paper|
      paper.topics.each do |topic|
        csv << "#{paper.id},\"#{topic}\"\n"
      end
    end
    
    return csv
    
  end # export_topic_csv
  
end # class LREC2008Scraper

class LRECPaper
  
  attr_accessor :id, :title, :authors, :topics, :abstract, :pdf_link, :slide_link, :source
  
end


scraper = LREC2008Scraper.new("http://www.lrec-conf.org/proceedings/lrec2008/")
scraper.run
scraper.papers.each do |paper|
  data = {
    'id' => paper.id,
    'title' => paper.title,
    'abstract' => paper.abstract,
    'pdf_link' => paper.pdf_link,
    'slide_link' => paper.slide_link,
    'source' => paper.source,
    'authors' => paper.authors.join(", "),
    'topics' => paper.topics.join("; "),
  }
  ScraperWiki.save(unique_keys=['id'], data=data)
end


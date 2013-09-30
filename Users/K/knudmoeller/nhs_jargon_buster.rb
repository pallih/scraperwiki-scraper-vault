require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'uri'
require 'cgi'


class NHSJargonScraper
  
  attr_reader :jargon_entries
  
  def run
  
    pages = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "xyz"]
    # pages = ["a", "b"]
  
    @jargon_entries = []

    pages.each do |page|
      
      puts "scraping #{page}"

      # html = ScraperWiki.scrape("http://www.ic.nhs.uk/jargon-buster/#{page}")           

      doc = Nokogiri::HTML(open("http://www.ic.nhs.uk/jargon-buster/#{page}"))
      for v in doc.search("div[@class='wysiwyg']")

        # get acronyms (all <strong> elements)
        acronyms = []
        v.search('strong').each do |acronym|
          acronyms << acronym.inner_html.strip
        end

        # get full labels (all <p> elements that do not contain '<strong>')
        # these labels might still contain comments for this particular entry
        labels = []
        label_candidates = v.search('p')
        label_candidates.each do |candidate|
          unless candidate.inner_html.match(/<strong>/)
            labels << candidate.inner_html.strip
          end
        end

        # iterate the acronyms to build our jargon entry objects
        # we assume that the labels[] and acronyms[] arrays are aligned 1:1
        count = 0
        acronyms.each do |acronym|
          label = labels[count]
          comment = nil
          # separate labels and comment with a regex.
          # this only works for about 90% of the cases
          if (match = label.match(/(.*?) - (.*?)$/))
            label = match[1].strip
            comment = match[2].strip
          end
          jargon_entry = JargonEntry.new(label, acronym, comment)
          @jargon_entries << jargon_entry

          count += 1
        end

      end
  
    end # iterate pages
  
  end # run()
  
  # return a string of turtle code containing all jargon definitions
  # namespace is the document URI to which each jargon definition will be appended as a fragment
  def export_ttl(namespace)
    
    turtle = ""

    
    turtle << "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
    turtle << "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n"
    turtle << "@prefix swc: <http://data.semanticweb.org/ns/swc/ontology#> .\n\n"
    
    @jargon_entries.each do |jargon_entry|
      turtle << jargon_entry.to_ttl(namespace)
    end
    
    return turtle
  end # export_ttl()
  
end # class NHSJargonScraper

class JargonEntry
  attr_reader :label, :acronym, :comment

  def initialize(label, acronym, comment)
    @label = label
    @acronym = acronym
    @comment = comment
  end

  def to_ttl(namespace)
    uri = "#{namespace}\##{JargonEntry.urise(@acronym)}"
    ttl = ""
    ttl << "<#{uri}> a skos:Concept ;\n"
    ttl << "  skos:prefLabel \"#{@label}\" ;\n"
    ttl << "  swc:hasAcronym \"#{@acronym}\" ;\n"
    ttl << "  rdfs:comment \"#{@comment}\" ;\n" if @comment
    ttl << ".\n\n"
  end
  
  def JargonEntry.urise(string)
    URI.escape(string.gsub(/&(.*?);/, "-").downcase)
  end

end

scraper = NHSJargonScraper.new
scraper.run
scraper.jargon_entries.each do |entry|
  data = {
    'label' => entry.label,
    'acronym' => entry.acronym,
    'comment' => entry.comment
  }
  ScraperWiki.save(unique_keys=['acronym'], data=data)
end


# this is the data we want to scrape (16/05/2011):
# it should only occur once per page
#        </ul><div class="wysiwyg"><p><strong>GBT</strong></p><p>Group business team </p><p><strong>GDS</strong></p><p>General Dental Services </p><p><strong>GFS</strong></p><p>Grant funded services - new collection measuring vulnerable people receiving services outside of a formal care plan </p><p><strong>GHS</strong></p><p>General Household survey </p><p><strong>GIS</strong></p><p>Graphical information system </p><p><strong>GMC</strong></p><p>General Medical Council </p><p><strong>GMS</strong></p><p>General medical services </p><p><strong>GOC</strong></p><p>General Ophthalmic Council </p><p><strong>GOR</strong></p><p>Government office region </p><p><strong>GOS</strong></p><p>General ophthalmic services </p><p><strong>GP</strong></p><p>General practitioner </p><p><strong>GPHS</strong></p><p>General practice health services </p><p><strong>GRN</strong></p><p>Goods received note </p><p><strong>GSS</strong></p><p>Government Statistical Service </p></div></div>
require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'uri'
require 'cgi'


class NHSJargonScraper
  
  attr_reader :jargon_entries
  
  def run
  
    pages = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "xyz"]
    # pages = ["a", "b"]
  
    @jargon_entries = []

    pages.each do |page|
      
      puts "scraping #{page}"

      # html = ScraperWiki.scrape("http://www.ic.nhs.uk/jargon-buster/#{page}")           

      doc = Nokogiri::HTML(open("http://www.ic.nhs.uk/jargon-buster/#{page}"))
      for v in doc.search("div[@class='wysiwyg']")

        # get acronyms (all <strong> elements)
        acronyms = []
        v.search('strong').each do |acronym|
          acronyms << acronym.inner_html.strip
        end

        # get full labels (all <p> elements that do not contain '<strong>')
        # these labels might still contain comments for this particular entry
        labels = []
        label_candidates = v.search('p')
        label_candidates.each do |candidate|
          unless candidate.inner_html.match(/<strong>/)
            labels << candidate.inner_html.strip
          end
        end

        # iterate the acronyms to build our jargon entry objects
        # we assume that the labels[] and acronyms[] arrays are aligned 1:1
        count = 0
        acronyms.each do |acronym|
          label = labels[count]
          comment = nil
          # separate labels and comment with a regex.
          # this only works for about 90% of the cases
          if (match = label.match(/(.*?) - (.*?)$/))
            label = match[1].strip
            comment = match[2].strip
          end
          jargon_entry = JargonEntry.new(label, acronym, comment)
          @jargon_entries << jargon_entry

          count += 1
        end

      end
  
    end # iterate pages
  
  end # run()
  
  # return a string of turtle code containing all jargon definitions
  # namespace is the document URI to which each jargon definition will be appended as a fragment
  def export_ttl(namespace)
    
    turtle = ""

    
    turtle << "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
    turtle << "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n"
    turtle << "@prefix swc: <http://data.semanticweb.org/ns/swc/ontology#> .\n\n"
    
    @jargon_entries.each do |jargon_entry|
      turtle << jargon_entry.to_ttl(namespace)
    end
    
    return turtle
  end # export_ttl()
  
end # class NHSJargonScraper

class JargonEntry
  attr_reader :label, :acronym, :comment

  def initialize(label, acronym, comment)
    @label = label
    @acronym = acronym
    @comment = comment
  end

  def to_ttl(namespace)
    uri = "#{namespace}\##{JargonEntry.urise(@acronym)}"
    ttl = ""
    ttl << "<#{uri}> a skos:Concept ;\n"
    ttl << "  skos:prefLabel \"#{@label}\" ;\n"
    ttl << "  swc:hasAcronym \"#{@acronym}\" ;\n"
    ttl << "  rdfs:comment \"#{@comment}\" ;\n" if @comment
    ttl << ".\n\n"
  end
  
  def JargonEntry.urise(string)
    URI.escape(string.gsub(/&(.*?);/, "-").downcase)
  end

end

scraper = NHSJargonScraper.new
scraper.run
scraper.jargon_entries.each do |entry|
  data = {
    'label' => entry.label,
    'acronym' => entry.acronym,
    'comment' => entry.comment
  }
  ScraperWiki.save(unique_keys=['acronym'], data=data)
end


# this is the data we want to scrape (16/05/2011):
# it should only occur once per page
#        </ul><div class="wysiwyg"><p><strong>GBT</strong></p><p>Group business team </p><p><strong>GDS</strong></p><p>General Dental Services </p><p><strong>GFS</strong></p><p>Grant funded services - new collection measuring vulnerable people receiving services outside of a formal care plan </p><p><strong>GHS</strong></p><p>General Household survey </p><p><strong>GIS</strong></p><p>Graphical information system </p><p><strong>GMC</strong></p><p>General Medical Council </p><p><strong>GMS</strong></p><p>General medical services </p><p><strong>GOC</strong></p><p>General Ophthalmic Council </p><p><strong>GOR</strong></p><p>Government office region </p><p><strong>GOS</strong></p><p>General ophthalmic services </p><p><strong>GP</strong></p><p>General practitioner </p><p><strong>GPHS</strong></p><p>General practice health services </p><p><strong>GRN</strong></p><p>Goods received note </p><p><strong>GSS</strong></p><p>Government Statistical Service </p></div></div>

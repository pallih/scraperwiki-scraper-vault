require 'nokogiri'
require 'uri'
require 'cgi'
require 'open-uri'

class BMTerm
    def initialize(label)
        @label = label
    end
    
    attr_reader :label
    attr_accessor :uri, :finds
    
    def getURIfromlabel
        sparql = "http://collection.britishmuseum.org/Sparql?Syntax=SparqlResults%2FXML&Query=SELECT+%3Fs+WHERE+%0D%0A%7B+%0D%0A%09%3Fs++%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23prefLabel%3E+%22" + URI.escape(@label) + "%22%0D%0A%7D+LIMIT+1"

      #
      # Then extract thesaurus URI from results set - in binding (name=s) element, in uri element
      begin
        xmldoc = Nokogiri::XML(open(sparql))
        # puts xmldoc.inspect
        @uri = xmldoc.xpath('///sparql:result[1]/sparql:binding[@name="s"]/sparql:uri[1]', 'sparql' => 'http://www.w3.org/2005/sparql-results#').inner_text
      rescue
        puts "Error while getting " + sparql
      end
    end

    def checkFinds
      finds_label = CGI.escape(@label.gsub(/[-\/]/,' '))
      finds_url = "http://finds.org.uk/database/terminology/object/term/" + finds_label + "/format/xml"
      begin
        findsxml = Nokogiri::XML(open(finds_url))
        finds_use = findsxml.xpath('//indexTerm').inner_text
        if (finds_use.to_s == "Y")
          @finds = "http://finds.org.uk/database/terminology/object/term/" + finds_label
        end
      rescue
        puts "Error while getting " + finds_url
      end
  end
end

base_url = "http://www.collectionslink.org.uk/assets/thesaurus_bmon/"
index_page = "Objintro.htm"
index_doc = Nokogiri::HTML(open(base_url + index_page))
puts index_doc.to_s
thes_urls = []

index_doc.xpath('//@href').each do |pages|
  thes_url = pages.inner_text
  if (thes_url.slice(0..4) === "index")
    puts base_url + thes_url
    thes_urls.push(base_url + thes_url)
  end

end
 
thes_urls.each do |url|
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  doc.xpath("//b[not(*)]").each do |terms|
      term = BMTerm.new(terms.inner_text.downcase)
      term.getURIfromlabel
      term.checkFinds
      begin
        ScraperWiki.save(unique_keys=['term'], data={'term' => term.label,'uri' => term.uri, 'finds_uri' => term.finds})
        sleep 1
      rescue
        puts "Unable to save record for " + term.label
      end
  end
end


require 'open-uri'
require 'nokogiri'
require 'benchmark'

# Returns an array of Australian Postcodes: https://gist.github.com/1504308
def australian_postcodes
  # Postcodes that look like integers
  nsw = (1000..1999).to_a +
        (2000..2599).to_a +
        (2619..2898).to_a +
        (2921..2999).to_a
  act = (2600..2618).to_a +
        (2900..2920).to_a
  vic = (3000..3999).to_a +
        (8000..8999).to_a
  qld = (4000..4999).to_a +
        (9000..9999).to_a
  tas = (7000..7799).to_a +
        (7800..7999).to_a
  sa = (5000..5799).to_a +
       (5800..5999).to_a
  wa = (6000..6797).to_a +
       (6800..6999).to_a

  # Convert integers to strings (postcodes are *not* integers)
  postcodes = (nsw + act + vic + qld + tas + sa + wa).map { |p| p.to_s }

  # Postcodes from NT (and one range in the ACT don't look like integers)
  nt_and_act_range = (800..899).to_a + (900..999).to_a + (200..299).to_a

  postcodes + (nt_and_act_range.map { |p| "0#{p.to_s}" })
end

# Create a custom subclass of Nokogiri::XML::SAX::Document to parse ABN Search results
class ABNSearchDoc < Nokogiri::XML::SAX::Document
   attr_accessor :isInABNTag,:isInPostcodeTag,:postcode,:records

   def initialize()
      @isInABNTag =false
      @isInPostcodeTag = false
      @postcode = ""
      @records = []
   end

   # set different states for the parser
   def start_element name, attrs = []
      @isInABNTag = (name == "abn")
      @isInPostcodeTag = (name == "postcode")
   end

   #store the text that is inside XML tags based on current tag name
   def characters chardata
      # remove nonprintable characters and spaces
      chardata = chardata.gsub(/[^\x20-\x7e]+/, '').gsub(/ /, '')
      if chardata != ""
         if @isInPostcodeTag
            @postcode = chardata
         end
         if @isInABNTag
            @records << {'abn' => chardata, 'postcode' => @postcode}
            # try saving small batches of records as parsed
            if @records.length > 5000
              puts "Large number of records for this postcode, saving batch of #{@records.length} records..."
              time = Benchmark.realtime do
                ScraperWiki.save_sqlite ['abn'], @records
              end
              puts "Saved in #{(time*1000).ceil} ms."
              @records = []
            end
         end
      end
   end

end

# eliminate already parsed postcodes from search
parsed_postcodes = ScraperWiki.select('* from parsed_postcodes').map { |r| r['postcode'] }
postcodes = australian_postcodes - parsed_postcodes

# make index to reduce insert cost of each abn record
#ScraperWiki.sqliteexecute('''           
#    CREATE INDEX IF NOT EXISTS abn_manual_index 
#    ON swdata (abn)''')

# Create our parser
myABNSearchDoc = ABNSearchDoc.new
parser = Nokogiri::XML::SAX::Parser.new(myABNSearchDoc)

postcodes.each do |postcode|
  puts "Getting postcode: #{postcode}"

  html = nil

  time = Benchmark.realtime do
    html = open("http://abr.business.gov.au/abrxmlsearch/AbrXmlSearch.asmx/SearchByABNStatus?postcode=#{postcode}&activeABNsOnly=N&currentGSTRegistrationOnly=N&entityTypeCode=&authenticationGuid=082f1497-93ff-4fc3-9c85-030022b11840")
  end

  puts "Downloaded in #{(time*1000).ceil} ms"

  time = Benchmark.realtime do
    parser.parse(html)
  end

  puts "Finished parsing in #{(time*1000).ceil} ms, saving #{myABNSearchDoc.records.length} records for postcode: #{postcode}"
  
  ScraperWiki.save_sqlite ['abn'], myABNSearchDoc.records, verbose=0
  ScraperWiki.save_sqlite ["postcode"], {"postcode" => postcode}, "parsed_postcodes"
end

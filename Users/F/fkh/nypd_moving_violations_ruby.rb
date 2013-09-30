# many thanks to Alex (Maxious) Sadleir for providing the basis for this code.
# more:
# http://groups.google.com/group/scraperwiki/browse_thread/thread/7aff305c7f1e7cf7

require 'rubygems'   
require 'pdf-reader'
require 'open-uri'   

##########  This section contains the callback code that processes the PDF file contents  ######
class PageTextReceiver
  attr_accessor :content, :page_counter
  def initialize
    @content = []
    @page_counter = 0
  end
  # Called when page parsing starts
  def begin_page(arg = nil)
    @page_counter += 1
    @content << ""
  end
  # record text that is drawn on the page
  def show_text(string, *params)
    if string != ""
      @content.last << " #{string}"
    end
  end

  def end_text_object(*params)
    @content << ""
  end

  # there's a few text callbacks, so make sure we process them all
  alias :super_show_text :show_text
  alias :move_to_next_line_and_show_text :show_text
  alias :set_spacing_next_line_show_text :show_text
  # this final text callback takes slightly different arguments
  def show_text_with_positioning(*params)
    params = params.first
    params.each { |str| show_text(str) if str.kind_of?(String)}
  end
end
################  End of TextReceiver #############################

#######  Instantiate the receiver and the reader
    receiver = PageTextReceiver.new
    pdf_reader = PDF::Reader.new 
    pdf = open("http://www.nyc.gov/html/nypd/downloads/pdf/traffic_data/001sum.pdf")
    pdf_reader.parse(pdf, receiver)
    lineno = 0

   heading = ''
   is_heading_set = false
   saved_first_value = 0

    
    # go through each line
    receiver.content.each do |line|    
       line = line.strip
       lineno = lineno +1
  
      # skip header lines
      if lineno < 3 
         line = ""
      end

      # clean out the junk
      if line =~ /\*/i
         print "Removed bad line (#{line})"
         line = ""
      end 


      if line =~ /[:alpha:]/ # then it's a heading
        print "Heading line: #{line} \n"
        heading = line
        heading.gsub(/[0-9]/, '') #strip out numbers 
        is_heading_set = true
        saved_first_value = 0
        print "heading: #{heading} \n"
      end

      if is_heading_set
        if line =~ /\d/ 
           print "found a value... #{line} \n"
 
          # remove any characters from the number
          line.gsub!(/[:alpha:]/, '')

          if saved_first_value == 1 # then this is the second value
            print "#{lineno} | #{heading} | YTD: #{line} \n"
            period = 'YTD'
          end 

          if saved_first_value == 0  # this is the first value
            saved_first_value = 1
            print "#{lineno} | #{heading} | MTD: #{line} \n"
            period = 'MTD'       
          end
         
        uniq_value = period + " " + heading
        uniq_value.tr("", "_")

        ScraperWiki.save_sqlite(unique_keys=['uniq'], data={'uniq'=>uniq_value, 'Violation'=>heading, 'Period'=>period,'Value'=>line})

        else
          # not a number

        end 

      end

    end# many thanks to Alex (Maxious) Sadleir for providing the basis for this code.
# more:
# http://groups.google.com/group/scraperwiki/browse_thread/thread/7aff305c7f1e7cf7

require 'rubygems'   
require 'pdf-reader'
require 'open-uri'   

##########  This section contains the callback code that processes the PDF file contents  ######
class PageTextReceiver
  attr_accessor :content, :page_counter
  def initialize
    @content = []
    @page_counter = 0
  end
  # Called when page parsing starts
  def begin_page(arg = nil)
    @page_counter += 1
    @content << ""
  end
  # record text that is drawn on the page
  def show_text(string, *params)
    if string != ""
      @content.last << " #{string}"
    end
  end

  def end_text_object(*params)
    @content << ""
  end

  # there's a few text callbacks, so make sure we process them all
  alias :super_show_text :show_text
  alias :move_to_next_line_and_show_text :show_text
  alias :set_spacing_next_line_show_text :show_text
  # this final text callback takes slightly different arguments
  def show_text_with_positioning(*params)
    params = params.first
    params.each { |str| show_text(str) if str.kind_of?(String)}
  end
end
################  End of TextReceiver #############################

#######  Instantiate the receiver and the reader
    receiver = PageTextReceiver.new
    pdf_reader = PDF::Reader.new 
    pdf = open("http://www.nyc.gov/html/nypd/downloads/pdf/traffic_data/001sum.pdf")
    pdf_reader.parse(pdf, receiver)
    lineno = 0

   heading = ''
   is_heading_set = false
   saved_first_value = 0

    
    # go through each line
    receiver.content.each do |line|    
       line = line.strip
       lineno = lineno +1
  
      # skip header lines
      if lineno < 3 
         line = ""
      end

      # clean out the junk
      if line =~ /\*/i
         print "Removed bad line (#{line})"
         line = ""
      end 


      if line =~ /[:alpha:]/ # then it's a heading
        print "Heading line: #{line} \n"
        heading = line
        heading.gsub(/[0-9]/, '') #strip out numbers 
        is_heading_set = true
        saved_first_value = 0
        print "heading: #{heading} \n"
      end

      if is_heading_set
        if line =~ /\d/ 
           print "found a value... #{line} \n"
 
          # remove any characters from the number
          line.gsub!(/[:alpha:]/, '')

          if saved_first_value == 1 # then this is the second value
            print "#{lineno} | #{heading} | YTD: #{line} \n"
            period = 'YTD'
          end 

          if saved_first_value == 0  # this is the first value
            saved_first_value = 1
            print "#{lineno} | #{heading} | MTD: #{line} \n"
            period = 'MTD'       
          end
         
        uniq_value = period + " " + heading
        uniq_value.tr("", "_")

        ScraperWiki.save_sqlite(unique_keys=['uniq'], data={'uniq'=>uniq_value, 'Violation'=>heading, 'Period'=>period,'Value'=>line})

        else
          # not a number

        end 

      end

    end
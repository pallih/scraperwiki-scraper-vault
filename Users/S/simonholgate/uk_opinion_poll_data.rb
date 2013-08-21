# encoding: utf-8
require 'rubygems'
require 'open-uri'
require 'nokogiri'
require 'scraperwiki'

class UkOpinion
  def initialize
    # Read the main page of UK Polling Report
    html = ScraperWiki.scrape("http://ukpollingreport.co.uk/voting-intention")
    # Get around any problems with page encoding
    html.force_encoding('utf-8')
    
    @doc = Nokogiri::HTML(html)
  end

  def getdata
    # Get the data from the table
    rowcount=0
    @data=Array.new
    rows = @doc.css('.polltable tr')
    rows.each do |row|
      if(rowcount>1) # Skip 2 header lines
        columns = row.css('td') # Split into td elements
        tdata = columns.map{|t| t.text} # Convert the contents of the elements to text
        # Set the first element of the array to a unique ID which is the rowcount number
        @data[rowcount-2] = [(rowcount-2).to_s, tdata[0].strip, tdata[1].strip, 
                tdata[2].to_i, tdata[3].to_i, tdata[4].to_i, tdata[5].to_i]
      end
      rowcount += 1
    end
  end

  def asData
    @data
  end
 
  def asDoc
    @doc
  end

  def savedata
    for v in (0..@data.length)
      # save data using the rowcount as key
      polls = {
        'id' => @data[v][0],
        'pollster' => @data[v][1],
        'date' => @data[v][2],
        'con' => @data[v][3],
        'lab' => @data[v][4],
        'libdem' => @data[v][5],
        'conlead' => @data[v][6]
      }
      ScraperWiki.save_sqlite(unique_keys=['id'], data=polls, 
        table_name="UK_opinion_poll_data")
    end
  end


end

## Run the job
poll = UkOpinion.new
poll.getdata
poll.savedata



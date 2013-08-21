# Cook County Assessor - Hyde Park Properties

require 'mechanize'
require 'nokogiri'
require 'date'

BASE_URL = "http://www.cookcountyassessor.com/Property_Search/Property_Search.aspx"
UNIT_NUMS = { "Two" => 2, "Three" => 3, "Four" => 4, "Five" => 5, "Six" => 6 }
TARGET_REGEXP = /ctl00\$BodyContent\$DisplayGrid\$ctl44\$ctl../

chunks = [
  { :hnum1=>"800",  :hnum2=>"2000", :dir=>"E", :street=>"47th" },
  { :hnum1=>"800",  :hnum2=>"2000", :dir=>"E", :street=>"48th" },
  { :hnum1=>"800",  :hnum2=>"2000", :dir=>"E", :street=>"49th" },
  { :hnum1=>"800",  :hnum2=>"2000", :dir=>"E", :street=>"50th" },
  { :hnum1=>"800",  :hnum2=>"2000", :dir=>"E", :street=>"51st" },
  { :hnum1=>"800",  :hnum2=>"2000", :dir=>"E", :street=>"52nd" },
  { :hnum1=>"800",  :hnum2=>"2000", :dir=>"E", :street=>"53rd" },
  { :hnum1=>"800",  :hnum2=>"2000", :dir=>"E", :street=>"54th" },
  { :hnum1=>"800",  :hnum2=>"2000", :dir=>"E", :street=>"55th" },
  { :hnum1=>"800",  :hnum2=>"2000", :dir=>"E", :street=>"56th" },
  { :hnum1=>"800",  :hnum2=>"2000", :dir=>"E", :street=>"57th" },
  { :hnum1=>"800",  :hnum2=>"2000", :dir=>"E", :street=>"58th" },
  { :hnum1=>"800",  :hnum2=>"2000", :dir=>"E", :street=>"59th" },
  { :hnum1=>"800",  :hnum2=>"2000", :dir=>"E", :street=>"60th" },
  { :hnum1=>"800",  :hnum2=>"6000", :dir=>"",  :street=>"Hyde Park" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Cottage Grove" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Maryland" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Drexel" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Ingleside" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Ellis" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Berkeley" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Greenwood" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"University" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Woodlawn" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Kimbark" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Kenwood" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Ridgewood" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Dorchester" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Blackstone" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Harper" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Lake Park" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Stony Island" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Cornell" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Everett" },
  { :hnum1=>"800",  :hnum2=>"1000", :dir=>"E", :street=>"Drexel" },  # Drexel Square
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"East View" },
  { :hnum1=>"800",  :hnum2=>"2000", :dir=>"E", :street=>"Madison Park", },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"South Shore" },
  { :hnum1=>"0",    :hnum2=>"6000", :dir=>"S", :street=>"East End" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Chicago Beach" },
  { :hnum1=>"4700", :hnum2=>"6000", :dir=>"S", :street=>"Lake Shore" }
]

agent = Mechanize.new

page = agent.get(BASE_URL)

thisrun = (ScraperWiki.get_var("lastrun", 33)+1)%chunks.length
npage = (ScraperWiki.get_var("lastpage") +1)
chunk = chunks[thisrun]

def findpage(pageno, frag, doc)
  linkpages = frag.css("a")
  if (linkpages.empty?)
    page = nil
  else
    linkpage = linkpages.find { |link| link.content.eql?(pageno.to_s) }
    linkpage = linkpages.last if (linkpage.nil? && linkpages.last.content.eql?("..."))
    if (! linkpage.nil? )
      target = linkpage.attribute("href").value.match(TARGET_REGEXP)
      linkform = doc.form("aspnetForm")
      linkform['__EVENTTARGET'] = target
      page = linkform.submit
    else
      page = nil
    end
  end
  return page
end

propform = page.form("aspnetForm")
propform['ctl00$BodyContent$Street1'] = chunk[:street]
propform['ctl00$BodyContent$FAddress'] = chunk[:hnum1]
propform['ctl00$BodyContent$Dir1'] = chunk[:dir]
propform['ctl00$BodyContent$TAddress1'] = chunk[:hnum2]
propform['ctl00$BodyContent$City1'] = "Chicago"
sbutton = propform.button_with(:name => 'ctl00$BodyContent$btn_Search_Address')
puts propform['ctl00$BodyContent$Street1']
doc = propform.submit(sbutton)
if (npage > 1)
  cell = doc.search("table.propertyresultsgrid tr").last
  doc = findpage(npage, cell, doc)
end

while (! doc.nil? ) 
#  puts "Displaying page " + npage.to_s
  doc.search("table.propertyresultsgrid tr").each do |row|
    cells = row.css("td")
    if (cells.length == 7 && ! cells[0].content.eql?("PIN"))
      pin = cells[0].css("a").inner_html.strip
      pclass = cells[5].content.strip
      if (pclass.eql?("0-00"))
        age = ""
        units = ""
        lsf = ""
        bsf = ""
        pvalue = ""
      else
        begin
          details = doc.link_with(:text => pin).click
        rescue EOFError
          exit
        end
        age = details.search("span#ctl00_BodyContent_lbl_age").inner_html.strip
        units = details.search("span#ctl00_BodyContent_lbl_units").inner_html.strip
        if (units.eql?(""))
          units = UNIT_NUMS[details.search("span#ctl00_BodyContent_lbl_apts").inner_html.strip].to_s
        end
        lsf = details.search("span#ctl00_BodyContent_lbl_lsf").inner_html.strip.delete(",")
        bsf = details.search("span#ctl00_BodyContent_lbl_bsf1").inner_html.strip.delete(",").gsub(/[ \t]+/, ' ')
        if bsf.eql?("")
          bsf = details.search("span#ctl00_BodyContent_lbl_bsf").inner_html.strip.delete(",").gsub(/[ \t]+/, ' ')
        end
        pvalue = details.search("span#ctl00_BodyContent_lbl_priortot").inner_html.strip.delete(",")
      end
      data = { 
        :pin     => pin,
        :address => cells[1].content.gsub(/[ \t]+/, ' ').strip,
        :unit    => cells[2].content.strip,
        :city    => cells[3].content.strip,
        :nhood   => cells[4].content.strip,
        :class   => pclass,
        :avalue  => cells[6].content.strip.delete(","),
        :priorvalue => pvalue,
        :age     => age,
        :units   => units,
        :lsf     => lsf,
        :bsf     => bsf,
        :updated_at => Time.new
      }
#      puts data[:pin] + ',"' + data[:address] + '","' + data[:unit] + '",' +
#        data[:nhood] + ',' +data[:class]+ ',' + data[:avalue] + ',' +
#        data[:priorvalue] + ',' +
#        data[:age] + ',' + data[:units] + ',' + data[:lsf] + ',' + data[:bsf]
      ScraperWiki.save_sqlite([:pin], data, table_name="properties")
    elsif ( cells.length == 1 )
      ScraperWiki.save_var("lastpage", npage)
      npage = npage + 1
      doc = findpage(npage, cells[0], doc)
    end
  end
end

ScraperWiki.save_var("lastrun", thisrun)
ScraperWiki.save_var("lastpage", 0)


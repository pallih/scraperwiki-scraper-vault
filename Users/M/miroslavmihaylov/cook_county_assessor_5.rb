# Cook County Assessor - Hyde Park Properties

require 'mechanize'
require 'nokogiri'
require 'date'

BASE_URL = "http://www.cookcountyassessor.com/Property_Search/Property_Search.aspx"
UNIT_NUMS = { "Two" => 2, "Three" => 3, "Four" => 4, "Five" => 5, "Six" => 6 }
TARGET_REGEXP = /ctl00\$BodyContent\$DisplayGrid\$ctl44\$ctl../
CITY_NAME = "CHICAGO"
ScraperWiki.save_var("lastrun", -1)
chunks = [
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"a"},
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"b" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"c" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"e" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"d" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"7" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"8" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"1" },
  { :hnum1=>"3500",  :hnum2=>"20000", :dir=>"", :street=>"1" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"d" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"e" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"f" },
  { :hnum1=>"9020",  :hnum2=>"20000", :dir=>"", :street=>"f" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"g" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"2" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"3" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"5" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"h" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"i" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"j" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"k" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"l" },
  { :hnum1=>"7575",  :hnum2=>"20000", :dir=>"", :street=>"l" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"m" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"n" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"o" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"p" },
  { :hnum1=>"16100",  :hnum2=>"30000", :dir=>"", :street=>"p" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"q" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"r" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"s" },
  { :hnum1=>"14039",  :hnum2=>"20000", :dir=>"", :street=>"s" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"t" },


  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"u" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"v" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"w" },
  { :hnum1=>"14120",  :hnum2=>"20000", :dir=>"", :street=>"w" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"z" },
  { :hnum1=>"8207",  :hnum2=>"20000", :dir=>"", :street=>"indian" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"indian" },
  { :hnum1=>"4900",  :hnum2=>"20000", :dir=>"", :street=>"austin" },
  { :hnum1=>"4560",  :hnum2=>"20000", :dir=>"", :street=>"elston" },
  { :hnum1=>"4520",  :hnum2=>"20000", :dir=>"", :street=>"menard" },
  { :hnum1=>"10000",  :hnum2=>"20000", :dir=>"", :street=>"major" },
  { :hnum1=>"4455",  :hnum2=>"20000", :dir=>"", :street=>"parkside" },
  { :hnum1=>"5000",  :hnum2=>"20000", :dir=>"", :street=>"MCVICKER" },
 # { :hnum1=>"5800",  :hnum2=>"20000", :dir=>"", :street=>"mobile" },
  { :hnum1=>"6563",  :hnum2=>"20000", :dir=>"", :street=>"northwest" },
  { :hnum1=>"5126",  :hnum2=>"20000", :dir=>"", :street=>"monitor" },
  { :hnum1=>"4339",  :hnum2=>"20000", :dir=>"", :street=>"mason" },
  { :hnum1=>"4919",  :hnum2=>"20000", :dir=>"", :street=>"austin" },

  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"kimbal" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"CHRISTIANA" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"Victoria" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"spaulding" },

  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"Ardmore" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"JERSEY" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"KEDZIE" }


]

agent = Mechanize.new

page = agent.get(BASE_URL)

thisrun = (ScraperWiki.get_var("lastrun", 160)+1)%chunks.length
#npage = (ScraperWiki.get_var("lastpage") +1)
npage = (0)
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
propform['ctl00$BodyContent$City1'] = "Park Dorest"
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
      #    details = doc.link_with(:text => pin).click
        rescue EOFError
          exit
        end
       #  taxcode=  details.search("ctl00_BodyContent_lbl_taxcode").inner_html.strip
#Assessed Valuation
        #lasval12=  details.search("ctl00_BodyContent_lbl_currland").inner_html.strip 
        #lassval11=  details.search("ctl00_BodyContent_lbl_priorland").inner_html.strip
        #basval12=  details.search("ctl00_BodyContent_lbl_currbldg").inner_html.strip 
        #basval11=  details.search("ctl00_BodyContent_lbl_Priorbldg").inner_html.strip
        #tassval12=  details.search("ctl00_BodyContent_lbl_currtot").inner_html.strip 
        #tassval11=  details.search("span#ctl00_BodyContent_lbl_priortot").inner_html.strip
#property characteistics
        #val12=  details.search("span#ctl00_BodyContent_lbl_currmkt1").inner_html.strip 
        #val11=  details.search("span#ctl00_BodyContent_lbl_priormkt1").inner_html.strip 
        #desc=  details.search("span#ctl00_BodyContent_lbl_classdesc").inner_html 
        #age = details.search("span#ctl00_BodyContent_lbl_age").inner_html.strip
        #units = details.search("span#ctl00_BodyContent_lbl_units").inner_html.strip
        if (units.eql?(""))
        #  units = UNIT_NUMS[details.search("span#ctl00_BodyContent_lbl_apts").inner_html.strip].to_s
        end
        #lsf = details.search("span#ctl00_BodyContent_lbl_lsf").inner_html.strip.delete(",")
        #bsf = details.search("span#ctl00_BodyContent_lbl_bsf1").inner_html.strip.delete(",").gsub(/[ \t]+/, ' ')
        if bsf.eql?("")
         # bsf = details.search("span#ctl00_BodyContent_lbl_bsf").inner_html.strip.delete(",").gsub(/[ \t]+/, ' ')
        end
        #asspass = details.search("ctl00_BodyContent_lbl_pass1").inner_html.strip
       # pvalue = details.search("span#ctl00_BodyContent_lbl_priortot").inner_html.strip.delete(",")
      end
      data = { 
        :pin     => pin,
        :address => cells[1].content.gsub(/[ \t]+/, ' ').strip,
        :unit    => cells[2].content.strip,
        :city    => cells[3].content.strip,
        :nhood   => cells[4].content.strip,
        #:taxcode => taxcode,
        #:class   => pclass.delete("-"),
        #:currland  => lasval12,
        #:priorvalue => pvalue,
        #:tassval11 =>  tassval11,
        #:val12 => val12,
        #:val11 => val11,
        #:desc => desc,
        #:age     => age,
        #:units   => units,
        #:lsf     => lsf,
        #:bsf     => bsf,
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
# Cook County Assessor - Hyde Park Properties

require 'mechanize'
require 'nokogiri'
require 'date'

BASE_URL = "http://www.cookcountyassessor.com/Property_Search/Property_Search.aspx"
UNIT_NUMS = { "Two" => 2, "Three" => 3, "Four" => 4, "Five" => 5, "Six" => 6 }
TARGET_REGEXP = /ctl00\$BodyContent\$DisplayGrid\$ctl44\$ctl../
CITY_NAME = "CHICAGO"
ScraperWiki.save_var("lastrun", -1)
chunks = [
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"a"},
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"b" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"c" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"e" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"d" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"7" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"8" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"1" },
  { :hnum1=>"3500",  :hnum2=>"20000", :dir=>"", :street=>"1" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"d" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"e" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"f" },
  { :hnum1=>"9020",  :hnum2=>"20000", :dir=>"", :street=>"f" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"g" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"2" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"3" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"5" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"h" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"i" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"j" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"k" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"l" },
  { :hnum1=>"7575",  :hnum2=>"20000", :dir=>"", :street=>"l" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"m" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"n" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"o" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"p" },
  { :hnum1=>"16100",  :hnum2=>"30000", :dir=>"", :street=>"p" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"q" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"r" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"s" },
  { :hnum1=>"14039",  :hnum2=>"20000", :dir=>"", :street=>"s" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"t" },


  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"u" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"v" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"w" },
  { :hnum1=>"14120",  :hnum2=>"20000", :dir=>"", :street=>"w" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"z" },
  { :hnum1=>"8207",  :hnum2=>"20000", :dir=>"", :street=>"indian" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"indian" },
  { :hnum1=>"4900",  :hnum2=>"20000", :dir=>"", :street=>"austin" },
  { :hnum1=>"4560",  :hnum2=>"20000", :dir=>"", :street=>"elston" },
  { :hnum1=>"4520",  :hnum2=>"20000", :dir=>"", :street=>"menard" },
  { :hnum1=>"10000",  :hnum2=>"20000", :dir=>"", :street=>"major" },
  { :hnum1=>"4455",  :hnum2=>"20000", :dir=>"", :street=>"parkside" },
  { :hnum1=>"5000",  :hnum2=>"20000", :dir=>"", :street=>"MCVICKER" },
 # { :hnum1=>"5800",  :hnum2=>"20000", :dir=>"", :street=>"mobile" },
  { :hnum1=>"6563",  :hnum2=>"20000", :dir=>"", :street=>"northwest" },
  { :hnum1=>"5126",  :hnum2=>"20000", :dir=>"", :street=>"monitor" },
  { :hnum1=>"4339",  :hnum2=>"20000", :dir=>"", :street=>"mason" },
  { :hnum1=>"4919",  :hnum2=>"20000", :dir=>"", :street=>"austin" },

  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"kimbal" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"CHRISTIANA" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"Victoria" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"spaulding" },

  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"Ardmore" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"JERSEY" },
  { :hnum1=>"0",  :hnum2=>"20000", :dir=>"", :street=>"KEDZIE" }


]

agent = Mechanize.new

page = agent.get(BASE_URL)

thisrun = (ScraperWiki.get_var("lastrun", 160)+1)%chunks.length
#npage = (ScraperWiki.get_var("lastpage") +1)
npage = (0)
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
propform['ctl00$BodyContent$City1'] = "Park Dorest"
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
      #    details = doc.link_with(:text => pin).click
        rescue EOFError
          exit
        end
       #  taxcode=  details.search("ctl00_BodyContent_lbl_taxcode").inner_html.strip
#Assessed Valuation
        #lasval12=  details.search("ctl00_BodyContent_lbl_currland").inner_html.strip 
        #lassval11=  details.search("ctl00_BodyContent_lbl_priorland").inner_html.strip
        #basval12=  details.search("ctl00_BodyContent_lbl_currbldg").inner_html.strip 
        #basval11=  details.search("ctl00_BodyContent_lbl_Priorbldg").inner_html.strip
        #tassval12=  details.search("ctl00_BodyContent_lbl_currtot").inner_html.strip 
        #tassval11=  details.search("span#ctl00_BodyContent_lbl_priortot").inner_html.strip
#property characteistics
        #val12=  details.search("span#ctl00_BodyContent_lbl_currmkt1").inner_html.strip 
        #val11=  details.search("span#ctl00_BodyContent_lbl_priormkt1").inner_html.strip 
        #desc=  details.search("span#ctl00_BodyContent_lbl_classdesc").inner_html 
        #age = details.search("span#ctl00_BodyContent_lbl_age").inner_html.strip
        #units = details.search("span#ctl00_BodyContent_lbl_units").inner_html.strip
        if (units.eql?(""))
        #  units = UNIT_NUMS[details.search("span#ctl00_BodyContent_lbl_apts").inner_html.strip].to_s
        end
        #lsf = details.search("span#ctl00_BodyContent_lbl_lsf").inner_html.strip.delete(",")
        #bsf = details.search("span#ctl00_BodyContent_lbl_bsf1").inner_html.strip.delete(",").gsub(/[ \t]+/, ' ')
        if bsf.eql?("")
         # bsf = details.search("span#ctl00_BodyContent_lbl_bsf").inner_html.strip.delete(",").gsub(/[ \t]+/, ' ')
        end
        #asspass = details.search("ctl00_BodyContent_lbl_pass1").inner_html.strip
       # pvalue = details.search("span#ctl00_BodyContent_lbl_priortot").inner_html.strip.delete(",")
      end
      data = { 
        :pin     => pin,
        :address => cells[1].content.gsub(/[ \t]+/, ' ').strip,
        :unit    => cells[2].content.strip,
        :city    => cells[3].content.strip,
        :nhood   => cells[4].content.strip,
        #:taxcode => taxcode,
        #:class   => pclass.delete("-"),
        #:currland  => lasval12,
        #:priorvalue => pvalue,
        #:tassval11 =>  tassval11,
        #:val12 => val12,
        #:val11 => val11,
        #:desc => desc,
        #:age     => age,
        #:units   => units,
        #:lsf     => lsf,
        #:bsf     => bsf,
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

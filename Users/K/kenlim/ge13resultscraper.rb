# Blank Ruby
require 'nokogiri'    
require 'pp'           
       

class Constituency
  attr_reader :candidates, :registeredVoters, :rejectedBallots, :countedBallots, 
    :issuedBallots, :name, :state, :code, :results

  def initialize(resultPage)
    @page = Nokogiri::HTML(resultPage)
    @state, @code, @name = grabConstituencyData()
    @registeredVoters = grabCommaNumber("//tr[td[text() ='JUMLAH PEMILIH BERDAFTAR ']]//td[position() = 4]")
    @rejectedBallots = grabCommaNumber("//tr[td[text() ='JUMLAH KERTAS UNDI DITOLAK ']]//td[position() = 4]")
    @countedBallots = grabCommaNumber("//tr[td[text() ='JUMLAH KERTAS UNDI DALAM PETI UNDI ']]//td[position() = 4]")
    @issuedBallots = grabCommaNumber("//tr[td[text() ='JUMLAH KERTAS UNDI DIKELUARKAN ']]//td[position() = 4]")
    @results = grabResults()
  end

  def grabCommaNumber(xpath)
    @page.at_xpath(xpath).inner_text().tr(",","").to_i
  end

  def grabConstituencyData()
    wholeCell = @page.at_xpath("//td[@width='79%']/b").inner_html
    first, blanko, last = wholeCell.split("<br>")
    state = first.split(":").last
    code, name = last.split(":").last.split("-")
    [state, code, name].map {|word| cleanup(word)} 
  end

  def cleanup(word)
    word.strip.split(" ").map{|x| x.capitalize}.join(" ")
  end

  def grabResultColumn(row, x)
    row.xpath("td[position() =" + x.to_s + "]")
  end    

  def grabResults()  
    @page.xpath("//tr[@valign='center']").map{ |row| 
      name = cleanup(grabResultColumn(row, 1).inner_text.split(".").last())
      party = cleanup(grabResultColumn(row, 2).inner_text.strip).upcase
      votes = grabResultColumn(row, 3).inner_text.tr(",", "").to_i
      Result.new(name, party, votes)
    }
  end

  def to_hash
    hash = {}
      instance_variables.each {|var| hash[var.to_s.delete("@")] = instance_variable_get(var) }
      @results.each {|result|
        hash[result.party + " Candidate"] = result.name
        hash[result.party + " Votes"] = result.votes
      }
      hash.delete("page")
      hash.delete("results")
      hash
  end

end

class Result 
  attr_reader :name, :party, :votes

  def initialize(name, party, votes)
    @name = name
    @party = party
    @votes = votes
  end

  def to_s
    "%s (%s): %s votes"%[name, party, votes] 
  end

end    

(1..222).each{|i| 
  url = "http://resultpru13.spr.gov.my/module/keputusan/paparan/5_KeputusanDR.php?kod=%05d" % (i * 100) 
  cons = Constituency.new(ScraperWiki::scrape(url))

  ScraperWiki::save_sqlite(["code"], cons.to_hash)           
}
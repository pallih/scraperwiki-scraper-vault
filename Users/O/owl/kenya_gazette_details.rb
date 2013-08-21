#<Encoding:UTF-8>
require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.gsub(/\r|\n|\t|\s+/,' ').strip
  end
end
class Array
  def pretty
    self.collect{|a|a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    gazs = data.select{|a| a =~ /GAZETTE NOTICE NO\./}
    puts gazs.inspect
    tmp = data.select{|a| a=~ /^Vol./}.first
    tm = tmp.scan(/Vol. (.*)\u2014/).flatten.first
    puts [tmp,tm].inspect
    t = RomanNumerals.to_decimal(tm).to_s
    gz_no = tmp.split(",").first.gsub(/\./,' ').gsub(/\s+/,' ').gsub(/\u2014|\s/,'_').gsub(tm,t).split("_")
    raise "invalid gazette_no #{tmp}" if gz_no.nil? or gz_no.empty? or gz_no.length < 5
    idx = 0
    records = []
    begin
      tmp = data[data.index(gazs[idx])..data.index(gazs[idx+1])-1].pretty rescue nil
      begin
        da = data[data.index(gazs[idx])..-1] rescue nil
        tmp = da[0..da.index{|a| a=~ /^NOW ON SALE|^PRINTED AND PUBLISHED BY THE GOVERNMENT PRINTER/}-1] unless da.nil? 
        puts [da,tmp].inspect
      end if tmp.nil? 
      #puts tmp.inspect
      break if tmp.nil? or tmp.empty? 

      r = {"notice"=>tmp.join("\n").strip,"notice_no" => tmp[0].gsub("GAZETTE NOTICE NO.","").strip.to_i}
      r["volume_no"] = gz_no[1]
      r["edition_no"] = gz_no[3]
      r["published_location"] = gz_no[4]

      tmp = tmp.delete_if{|a| a=~ /^THE KENYA GAZETTE/}.pretty
      begin
        if tmp.index{|a| a == "APPOINTMENT"}
          r["type"] = "APPOINTMENT"
        elsif tmp.index{|a| a == "REVOCATION OF APPOINTMENT"}
          r["type"] = "REVOCATION OF APPOINTMENT"
        elsif tmp.index{|a| a == "COLLECTION OF TRADE UNION DUES"}
          r["type"] = "COLLECTION OF TRADE UNION DUES"
        elsif tmp.index{|a| a == "DEDUCTION OF AGENCY FEES"}
          r["type"] = "DEDUCTION OF AGENCY FEES"
        elsif tmp.index{|a| a == "REVOCATION OF LAND TITLES"}
          r["type"] = "REVOCATION OF LAND TITLES"
        elsif tmp.index{|a| a == "ISSUE OF A PROVISIONAL CERTIFICATE"}
          r["type"] = "ISSUE OF A PROVISIONAL CERTIFICATE"
        elsif tmp.index{|a| a == "ISSUE OF A NEW CERTIFICATE OF LEASE"}
          r["type"] = "ISSUE OF A NEW CERTIFICATE OF LEASE"
        elsif tmp.index{|a| a == "ISSUE OF A NEW LAND TITLE DEED"}
          r["type"] = "ISSUE OF A NEW LAND TITLE DEED"
        elsif tmp.index{|a| a == "REGISTRATION OF INSTRUMENT"}
          r["type"] = "REGISTRATION OF INSTRUMENT"
        elsif tmp.index{|a| a == "APPLICATION FOR LICENCES"}
          r["type"] = "APPLICATION FOR LICENCES"
        elsif tmp.index{|a| a == "COMPLETION OF PART DEVELOPMENT PLAN"}
          r["type"] = "COMPLETION OF PART DEVELOPMENT PLAN"
        elsif tmp.index{|a| a == "COMPLETION OF PART DEVELOPMENT PLANS"}
          r["type"] = "COMPLETION OF PART DEVELOPMENT PLANS"
        elsif tmp.index{|a| a == "COMPLETION OF DEVELOPMENT PLANS"}
          r["type"] = "COMPLETION OF DEVELOPMENT PLANS"
        elsif tmp.index{|a| a == "CHANGE OF NAME"}
          r["type"] = "CHANGE OF NAME"
        elsif tmp.index{|a| a == "DISPOSAL OF UNCOLLECTED GOODS"}
          r["type"] = "DISPOSAL OF UNCOLLECTED GOODS"
        elsif tmp.index{|a| a == "LOSS OF POLICY"}
          r["type"] = "LOSS OF POLICY"
        elsif tmp.index{|a| a == "CLOSURE OF PRIVATE ROADS AND FOOTPATHS"}
          r["type"] = "CLOSURE OF PRIVATE ROADS AND FOOTPATHS"
        elsif tmp.index{|a| a == "DISPOSAL OF UNCOLLECTED GOODS"}
          r["type"] = "DISPOSAL OF UNCOLLECTED GOODS"
        elsif tmp.index{|a| a== "THE COMPANIES ACT"}
          r["type"] = "THE COMPANIES ACT"
        elsif tmp.index{|a| a == "THE LAND REGISTRATION ACT"}
          r["type"] = "THE LAND REGISTRATION ACT"
        elsif tmp.index{|a| a == "THE MINING ACT"}
          r["type"] = "THE MINING ACT"
        elsif tmp.index{|a| a == "THE LOCAL GOVERNMENT ACT"}
          r["type"] = "THE LOCAL GOVERNMENT ACT"
        elsif tmp.index{|a| a == "THE POLITICAL PARTIES ACT"}
          r["type"] = "THE POLITICAL PARTIES ACT"
        elsif tmp.index{|a| a == "THE LABOUR RELATIONS ACT"}
          r["type"] = "THE LABOUR RELATIONS ACT"
        elsif tmp.index{|a| a == "THE COMMISSIONS OF INQUIRY ACT"}
          r["type"] = "THE COMMISSIONS OF INQUIRY ACT"
        elsif tmp.index{|a| a == "THE KENYATTA UNIVERSITY ACT"}
          r["type"] = "THE KENYATTA UNIVERSITY ACT"
        elsif tmp.index{|a| a == "THE PHYSICAL PLANNING ACT"}
          r["type"] = "THE PHYSICAL PLANNING ACT"
        elsif tmp.index{|a| a == "THE JUDICIAL SERVICE ACT"}
          r["type"] = "THE JUDICIAL SERVICE ACT"
        elsif tmp.index{|a| a == "THE MICROFINANCE ACT"}
          r["type"] = "THE MICROFINANCE ACT"
        elsif tmp.index{|a| a == "THE REGISTRATION OF TITLES ACT"}
          r["type"] = "THE REGISTRATION OF TITLES ACT"
        elsif tmp.index{|a| a == "THE INCOME TAX ACT"}
          r["type"] = "THE INCOME TAX ACT"
        elsif tmp.index{|a| a == "THE TRUST LAND ACT"}
          r["type"] = "THE TRUST LAND ACT"
        elsif tmp.index{|a| a == "THE TRANSFER OF BUSINESSES ACT"}
          r["type"] = "THE TRANSFER OF BUSINESSES ACT"
        elsif tmp.index{|a| a == "THE TRANSPORT LICENSING ACT"}
          r["type"] = "THE TRANSPORT LICENSING ACT"
        elsif tmp.index{|a| a == "THE PRISONS ACT"}
          r["type"] = "THE PRISONS ACT"
        elsif tmp.index{|a| a == "THE NATIONAL MUSEUMS AND HERITAGE ACT"}
          r["type"] = "THE NATIONAL MUSEUMS AND HERITAGE ACT"
        elsif tmp.index{|a| a == "THE TEACHERS SERVICE COMMISSION ACT"}
          r["type"] = "THE TEACHERS SERVICE COMMISSION ACT"
        elsif tmp.index{|a| a == "THE TASK FORCE ON RESETTLEMENT OF BENEFICIARIES"}
          r["type"] = "THE TASK FORCE ON RESETTLEMENT OF BENEFICIARIES"
        elsif tmp.index{|a| a == "THE ENVIRONMENT AND LAND COURT ACT"}
          r["type"] = "THE ENVIRONMENT AND LAND COURT ACT"
        elsif tmp.index{|a| a == "THE RATING ACT"}
          r["type"] = "THE RATING ACT"
        elsif tmp.index{|a| a == "THE CIVIL PROCEDURE ACT"}
          r["type"] = "THE CIVIL PROCEDURE ACT"
        elsif tmp.index{|a| a == "THE CAPITAL MARKETS ACT"}
          r["type"] = "THE CAPITAL MARKETS ACT"
        elsif tmp.index{|a| a == "THE RETIREMENT BENEFITS ACT"}
          r["type"] = "THE RETIREMENT BENEFITS ACT"
        elsif tmp.index{|a| a == "CLOSURE OF ROADS"}
          r["type"] = "CLOSURE OF ROADS"
        elsif tmp.index{|a| a == "IN THE CHIEF MAGISTRATE'S COURT NANYUKI"}
          r["type"] = "IN THE CHIEF MAGISTRATE'S COURT NANYUKI"
        elsif tmp.index{|a| a == "LOSS OF SHARE CERTIFICATE"}
          r["type"] = "LOSS OF SHARE CERTIFICATE"
        elsif tmp.index{|a| a == "THE DISTRICTS AND PROVINCES ACT"}
          r["type"] = "THE DISTRICTS AND PROVINCES ACT"
        elsif tmp.index{|a| a == "THE CENTRAL BANK OF KENYA ACT"}
          r["type"] = "THE CENTRAL BANK OF KENYA ACT"
        elsif tmp.index{|a| a == "NOTIFICATION OF PRACTICE DIRECTION"}
          r["type"] = "NOTIFICATION OF PRACTICE DIRECTION"
        elsif tmp.index{|a| a == "THE AFRICAN CHRISTIAN MARRIAGE AND DIVORCE ACT"}
          r["type"] = "THE AFRICAN CHRISTIAN MARRIAGE AND DIVORCE ACT"
        elsif tmp.index{|a| a == "LOSS OF LIFE POLICY"}
          r["type"] = "LOSS OF LIFE POLICY"
        elsif tmp.index{|a| a == "THE POLICE ACT"}
          r["type"] = "THE POLICE ACT"
        elsif tmp.index{|a| a == "THE ALCOHOLIC DRINKS CONTROL ACT"}
          r["type"] = "THE ALCOHOLIC DRINKS CONTROL ACT"
        elsif tmp.index{|a| a == "AMENDMENT"}
          r["type"] = "AMENDMENT"
        elsif tmp.index{|a| a == "TRANSFER OF BUSINESS ACT"}
          r["type"] = "TRANSFER OF BUSINESS ACT"
        elsif tmp.index{|a| a == "THE NATIONAL CRIME RESEARCH CENTRE ACT"}
          r["type"] = "THE NATIONAL CRIME RESEARCH CENTRE ACT"
        elsif tmp.index{|a| a == "THE GOVERNMENT LANDS ACT"}
          r["type"] = "THE GOVERNMENT LANDS ACT"
        elsif tmp.index{|a| a == "SACCO SOCIETIES REGULATORY AUTHORITY"}
          r["type"] = "SACCO SOCIETIES REGULATORY AUTHORITY"
        elsif tmp.index{|a| a == "THE INDUSTRIAL TRAINING ACT"}
          r["type"] = "THE INDUSTRIAL TRAINING ACT"
        elsif tmp.index{|a| a == "THE INSURANCE ACT"}
          r["type"] = "THE INSURANCE ACT"
        elsif tmp.index{|a| a == "DISPOSAL OF UNCOLLECTD GOODS"}
          r["type"] = "DISPOSAL OF UNCOLLECTD GOODS"
        elsif tmp.index{|a| a == "COMMISSION ACT, 2011"}
          r["type"] = "COMMISSION ACT, 2011"
        elsif tmp.index{|a| a == "THE COMMISSION ON ADMINISTRATIVE JUSTICE ACT, 2011"}
          r["type"] = "THE COMMISSION ON ADMINISTRATIVE JUSTICE ACT, 2011"
        elsif tmp.index{|a| a == "THE MAGISTRATE'S COURT ACT"}
          r["type"] = "THE MAGISTRATE'S COURT ACT"
        elsif tmp.index{|a| a == "THE RATING ACT"}
          r["type"] = "THE RATING ACT"
        elsif tmp.index{|a| a == "THE RATING ACT"}
          r["type"] = "THE RATING ACT"
        elsif tmp.index{|a| a == "THE RATING  ACT"}
          r["type"] = "THE RATING  ACT"
        elsif tmp.index{|a| a == "THE CO-OPERATIVES SOCIETIES ACT"}
          r["type"] = "THE CO-OPERATIVES SOCIETIES ACT"
        elsif tmp.index{|a| a == "THE OATHS AND STATUTORY DECLARATIONS ACT"}
          r["type"] = "THE OATHS AND STATUTORY DECLARATIONS ACT"
        elsif tmp.index{|a| a == "THE CUSTOMS AND EXCISE ACT"}
          r["type"] = "THE CUSTOMS AND EXCISE ACT"
        elsif tmp.index{|a| a == "THE INTERPRETATION AND GENERAL PROVISIONS ACT"}
          r["type"] = "THE INTERPRETATION AND GENERAL PROVISIONS ACT"
        elsif tmp.index{|a| a == "NOTICE OF LOSS OF SEAL"}
          r["type"] = "NOTICE OF LOSS OF SEAL"
        elsif tmp.index{|a| a == "THE VETERINARY SURGEONS ACT"}
          r["type"] = "THE VETERINARY SURGEONS ACT"
        elsif tmp.index{|a| a == "IRREVOCABLE SPECIAL POWER OF ATTORNEY"}
          r["type"] = "IRREVOCABLE SPECIAL POWER OF ATTORNEY"
        elsif tmp.index{|a| a == "PRICE CONTROL ACT"}
          r["type"] = "PRICE CONTROL ACT"
        elsif tmp.index{|a| a ==  "CLOSURE OF PRIVATE ROADS"}
          r["type"] =  "CLOSURE OF PRIVATE ROADS"
        elsif tmp.index{|a| a ==  "THE NATIONAL ACCORD AND RECONCILIATION ACT"}
          r["type"] =  "THE NATIONAL ACCORD AND RECONCILIATION ACT"
        elsif tmp.index{|a| a== "THE POWER OF MERCY ACT" or a == "THE CHILDREN ACT" or a == "THE STATE CORPORATIONS ACT" or a== "LOSS OF POLICIES" or a== "IN THE SENIOR RESIDENT MAGISTRATE'S COURT" or a== "THE ENVIRONMENTAL MANAGEMENT AND" or a== "THE CO-OPERATIVE SOCIETIES ACT" or a== "THE ADVOCATES ACT" or a== "THE ANTI-CORRUPTION AND ECONOMIC CRIMES ACT" or a== "THE COFFEE ACT" or a== "THE REGISTERED LAND ACT" or a== "THE LAND ACQUISITION ACT" or a== "FUEL COST CHARGE" or a== "FOREIGN EXCHANGE RATE FLUCTUATION ADJUSTMENT" or a == "CUSTOMS SERVICES DEPARTMENT" or a == "PUBLIC SERVICE COMMISSION OF KENYA" or a == "FEES AND CHARGES" or a == "INVITATION OF PUBLIC COMMENTS" or a == "THE MOI UNIVERSITY ACT" or a == "THE PUBLIC SERVICE COMMISSION ACT" or a == "THE NATIONAL POLICE SERVICE COMMISSION ACT" or a == "THE VALUATION FOR RATING ACT" or a == "THE SCIENCE AND TECHNOLOGY ACT" or a == "THE MEDICAL PRACTITIONERS AND DENTISTS ACT" or a == "PUPILAGE AND PASSING OF EXAMINATIONS" or a =~ /THE EAST AFRICAN COMMUNITY CUSTOMS MANAGEMENT ACT/ or a == "THE WATER ACT" or a == "THE CIVIL AVIATION ACT" or a=~ /REPORT AND FINANCIAL STATEMENTS FOR THE YEAR ENDED/ or a == "THE LAW OF SUCCESSION ACT" or a =~ /STATEMENT OF ACTUAL REVENUE & NET EXCHEQUER ISSUES AS/ or a =~ /THE LAND ACT/ or a == "THE PHARMACY AND POISONS ACT" or a == "VACATION NOTICE" or a == "THE SURVEY ACT" or a =~ /IN THE MATTER OF ARBITRATION ACT/ or a == "INTENDED DESTRUCTION OF COURT RECORDS" or a =~ /IN THE PRINCIPAL MAGISTRATE'S COURT AT/ or a == "PUPILLAGE AND PASSING OF EXAMINATIONS" or a == "THE STANDARDS ACT" or a == "THE KENYA INFORMATION AND COMMUNICATIONS ACT" or a =~ /APPOINTMENT OF CHAIRPERSON AND MEMBERS/ or a == "RULES OF PROCEDURE" or a == "THE NATIONAL ASSEMBLY AND PRESIDENTIAL ELECTIONS ACT" or a == "ESTABLISHMENT OF A NATIONAL STEERING COMMITTEE" or a == "PROBATE AND ADMINISTRATION" or a == "PROBATE AND ADMIN ISTRATION" or a == "FOREIGN EXCHANGE FLUCTUATION ADJUSTMENT" or a == "INFLATION ADJUSTMENT" or a == "DIRECTORS AND STATUTORY INFORMATION" or a =~ /MONETARY POLICY STATEMENT/ or a == "NOTIFICATION OF EXAMINATION DATES" or a =~ /REPORT AND FINANCIAL STATEMENTS AT/ or a == "THE GOVERNMENT FINANCIAL MANAGEMENT ACT" or a =~ /STATEMENT OF ACTUAL REVENUE AND NET EXCHEQUER ISSUES AS AT/ or a =~ /REVISED FEES AND CHARGES/ or a =~ /THE NATIONAL GENDER AND EQUALITY COMMISSION ACT/ or a == "THE ETHICS AND ANTI-CORRUPTION COMMISSION ACT" or a =~ /INCOME AND EXPENDITURE YEAR ENDED/ or a == "THE OFFICE OF DEPUTY PRIME MINISTER AND MINISTRY" or a == "VACANCY IN THE OFFICE OF JUDGE OF THE COURT OF APPEAL" or a =~ /ENVIRONMENT AND LAND CASE/ or a == "ESTABLISHMENT OF THE TASK FORCE ON THE REALIGNMENT OF THE" or a == "THE TASK FORCE ON THE RESETTLEMENT OF" or a == "ORDER" or a == "THE ENVIRONMENTAL MANAGEMENT AND CO-" or a ==  "THE COUNCIL OF LEGAL EDUCATION (KENYA SCHOOL OF" or a ==  "IN THE PRINCIPAL MAGISTRATE'S COURT" or a =~ /IN THE MATTER OF THE ESTATE OF/ or a == "CHRISTMAS VACATION 2011" or a == "THE MAGISTRATE'S COURTS ACT" or a =~ /^LAND REFERENCE NO/ or a == "REPORT OF THE AUDITOR-GENERAL ON THE FINANCIAL STATEMENTS OF KENYA REVENUE AUTHORITY FOR THE" or a =~ /L\.R\. NO\./ or a == "AWARD OF ORDERS, DECORATIONS AND MEDALS" or a == "THE PHYSICAL PLANNERS REGISTRATION ACT" or a == "PURSUANT to the provisions of section 185 (1) of the Local" or a == "THE NATIONAL ASSEMBLY AND PRESIDENTIAL" or a == "CONSTITUTIONAL AFFAIRS"}
          #Ignore
        else
          #Ignore
          #raise "new section added #{tmp}"
        end
        begin
          t_i = tmp.index{|a| a=~ /Dated the/}
          t_i = tmp.index{|a| a=~ /Dated [0-9]/} if t_i.nil? or t_i == 0
          t_i = tmp.index{|a| a=~ /^[A-Z &,.’?-]+,$/} - 1 if t_i.nil? or t_i == 0 rescue nil
          t_i = tmp.index{|a| a=~ /^[A-Z &,.’?-]+.$/} - 1 if t_i.nil? or t_i == 0
        
          r["description"] = tmp[tmp.index{|a| a==r['type']}+1..t_i-1].join("\n")
          r["type"] = r["type"].strip
          begin
            r["published_dt"] = Date.parse(tmp[t_i].gsub(/Dated the|\./,'').strip).to_s rescue nil
            tm = tmp[t_i+1..-1]
            r["published_by"] = tm[0].gsub(/,$/,'').strip
            if tm.join(" ") =~ /MR|SSF/
            t = tm[1].split(" ")
              r["reference_no"] = t.select{|a| a =~ /^MR|^SSF/}.first
              r["department"] = t.delete_if{|a| a=~ /^MR|^SSF/}.join("\n").gsub(/\.$/,'').strip
            else
              r["reference_no"] = nil
              r["department"] = tm[1..-1].join("\n").gsub(/\.$/,'').strip
            end
          end unless r["description"].nil? 
          #r["section"] = tmp.join("\n").strip
          if r["department"] =~ /NOTE/
            da = r["department"].split("NOTE")
            r["department"] = da[0].strip
            r["note"] = da[1].strip
          end
        rescue Exception => e
          puts r.inspect
          raise e
        end unless r["type"].nil? 
      end if tmp[0].scan(/GAZETTE NOTICE NO/).count == 1 unless tmp.nil? or tmp[0] =~ /[a-z]/
      idx = idx + 1

      records << r.merge(rec).delete_if{|k,v| k=~ /^tmp_/}
    end while(true)
    return records
  elsif act == "filelist"
    records = data.force_encoding("UTF-8").split("\n")
  end
end

def action()
  list = scrape(@br.get("https://s3.amazonaws.com/kenyagazettes/list.txt"),"filelist",{})
  lstart = get_metadata("list",0)
  list[lstart..-1].each{|lfn|
    next if get_metadata(lfn,"nopes") == "complete"
    begin
      pg = @br.get("https://s3.amazonaws.com/kenyagazettes/#{lfn}") rescue nil
      next if pg.nil? 
      fn = pg.filename
      pg.save_as(fn)
      %x[java -Xms256m -Xmx1024m -jar /usr/share/java/pdfbox-app-1.7.0.jar ExtractText "#{fn}" -encoding UTF-8]
      tmp = IO.read("#{fn.gsub('.pdf','.txt')}").force_encoding("UTF-8")
      records = scrape(tmp.split("\n").pretty,"list",{"filename"=>fn})
      ScraperWiki.save_sqlite(unique_keys=['notice_no','volume_no','edition_no','published_location'],records)
      save_metadata(lfn,"complete")
      sleep(60)
    end
    lstart = lstart + 1
    save_metadata("list",lstart)
  }
  #delete_metadata("list")
end

def single(lnk)
  begin
    pg = @br.get(lnk)
    fn = pg.filename
    pg.save_as(fn)
    %x[java -Xms256m -Xmx1024m -jar /usr/share/java/pdfbox-app-1.7.0.jar ExtractText "#{fn}" -encoding UTF-8]
    tmp = IO.read("#{fn.gsub('.pdf','.txt')}").force_encoding("UTF-8")
    records = scrape(tmp.split("\n").pretty,"list",{"filename"=>fn})
    puts records.inspect
  end
end

action()

#single("https://s3.amazonaws.com/kenyagazettes/2011%20Kenya%20Gazette/Gazette%20Vol.%20101-12%E2%80%9310%E2%80%932012%20Special.pdf")#<Encoding:UTF-8>
require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.gsub(/\r|\n|\t|\s+/,' ').strip
  end
end
class Array
  def pretty
    self.collect{|a|a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    gazs = data.select{|a| a =~ /GAZETTE NOTICE NO\./}
    puts gazs.inspect
    tmp = data.select{|a| a=~ /^Vol./}.first
    tm = tmp.scan(/Vol. (.*)\u2014/).flatten.first
    puts [tmp,tm].inspect
    t = RomanNumerals.to_decimal(tm).to_s
    gz_no = tmp.split(",").first.gsub(/\./,' ').gsub(/\s+/,' ').gsub(/\u2014|\s/,'_').gsub(tm,t).split("_")
    raise "invalid gazette_no #{tmp}" if gz_no.nil? or gz_no.empty? or gz_no.length < 5
    idx = 0
    records = []
    begin
      tmp = data[data.index(gazs[idx])..data.index(gazs[idx+1])-1].pretty rescue nil
      begin
        da = data[data.index(gazs[idx])..-1] rescue nil
        tmp = da[0..da.index{|a| a=~ /^NOW ON SALE|^PRINTED AND PUBLISHED BY THE GOVERNMENT PRINTER/}-1] unless da.nil? 
        puts [da,tmp].inspect
      end if tmp.nil? 
      #puts tmp.inspect
      break if tmp.nil? or tmp.empty? 

      r = {"notice"=>tmp.join("\n").strip,"notice_no" => tmp[0].gsub("GAZETTE NOTICE NO.","").strip.to_i}
      r["volume_no"] = gz_no[1]
      r["edition_no"] = gz_no[3]
      r["published_location"] = gz_no[4]

      tmp = tmp.delete_if{|a| a=~ /^THE KENYA GAZETTE/}.pretty
      begin
        if tmp.index{|a| a == "APPOINTMENT"}
          r["type"] = "APPOINTMENT"
        elsif tmp.index{|a| a == "REVOCATION OF APPOINTMENT"}
          r["type"] = "REVOCATION OF APPOINTMENT"
        elsif tmp.index{|a| a == "COLLECTION OF TRADE UNION DUES"}
          r["type"] = "COLLECTION OF TRADE UNION DUES"
        elsif tmp.index{|a| a == "DEDUCTION OF AGENCY FEES"}
          r["type"] = "DEDUCTION OF AGENCY FEES"
        elsif tmp.index{|a| a == "REVOCATION OF LAND TITLES"}
          r["type"] = "REVOCATION OF LAND TITLES"
        elsif tmp.index{|a| a == "ISSUE OF A PROVISIONAL CERTIFICATE"}
          r["type"] = "ISSUE OF A PROVISIONAL CERTIFICATE"
        elsif tmp.index{|a| a == "ISSUE OF A NEW CERTIFICATE OF LEASE"}
          r["type"] = "ISSUE OF A NEW CERTIFICATE OF LEASE"
        elsif tmp.index{|a| a == "ISSUE OF A NEW LAND TITLE DEED"}
          r["type"] = "ISSUE OF A NEW LAND TITLE DEED"
        elsif tmp.index{|a| a == "REGISTRATION OF INSTRUMENT"}
          r["type"] = "REGISTRATION OF INSTRUMENT"
        elsif tmp.index{|a| a == "APPLICATION FOR LICENCES"}
          r["type"] = "APPLICATION FOR LICENCES"
        elsif tmp.index{|a| a == "COMPLETION OF PART DEVELOPMENT PLAN"}
          r["type"] = "COMPLETION OF PART DEVELOPMENT PLAN"
        elsif tmp.index{|a| a == "COMPLETION OF PART DEVELOPMENT PLANS"}
          r["type"] = "COMPLETION OF PART DEVELOPMENT PLANS"
        elsif tmp.index{|a| a == "COMPLETION OF DEVELOPMENT PLANS"}
          r["type"] = "COMPLETION OF DEVELOPMENT PLANS"
        elsif tmp.index{|a| a == "CHANGE OF NAME"}
          r["type"] = "CHANGE OF NAME"
        elsif tmp.index{|a| a == "DISPOSAL OF UNCOLLECTED GOODS"}
          r["type"] = "DISPOSAL OF UNCOLLECTED GOODS"
        elsif tmp.index{|a| a == "LOSS OF POLICY"}
          r["type"] = "LOSS OF POLICY"
        elsif tmp.index{|a| a == "CLOSURE OF PRIVATE ROADS AND FOOTPATHS"}
          r["type"] = "CLOSURE OF PRIVATE ROADS AND FOOTPATHS"
        elsif tmp.index{|a| a == "DISPOSAL OF UNCOLLECTED GOODS"}
          r["type"] = "DISPOSAL OF UNCOLLECTED GOODS"
        elsif tmp.index{|a| a== "THE COMPANIES ACT"}
          r["type"] = "THE COMPANIES ACT"
        elsif tmp.index{|a| a == "THE LAND REGISTRATION ACT"}
          r["type"] = "THE LAND REGISTRATION ACT"
        elsif tmp.index{|a| a == "THE MINING ACT"}
          r["type"] = "THE MINING ACT"
        elsif tmp.index{|a| a == "THE LOCAL GOVERNMENT ACT"}
          r["type"] = "THE LOCAL GOVERNMENT ACT"
        elsif tmp.index{|a| a == "THE POLITICAL PARTIES ACT"}
          r["type"] = "THE POLITICAL PARTIES ACT"
        elsif tmp.index{|a| a == "THE LABOUR RELATIONS ACT"}
          r["type"] = "THE LABOUR RELATIONS ACT"
        elsif tmp.index{|a| a == "THE COMMISSIONS OF INQUIRY ACT"}
          r["type"] = "THE COMMISSIONS OF INQUIRY ACT"
        elsif tmp.index{|a| a == "THE KENYATTA UNIVERSITY ACT"}
          r["type"] = "THE KENYATTA UNIVERSITY ACT"
        elsif tmp.index{|a| a == "THE PHYSICAL PLANNING ACT"}
          r["type"] = "THE PHYSICAL PLANNING ACT"
        elsif tmp.index{|a| a == "THE JUDICIAL SERVICE ACT"}
          r["type"] = "THE JUDICIAL SERVICE ACT"
        elsif tmp.index{|a| a == "THE MICROFINANCE ACT"}
          r["type"] = "THE MICROFINANCE ACT"
        elsif tmp.index{|a| a == "THE REGISTRATION OF TITLES ACT"}
          r["type"] = "THE REGISTRATION OF TITLES ACT"
        elsif tmp.index{|a| a == "THE INCOME TAX ACT"}
          r["type"] = "THE INCOME TAX ACT"
        elsif tmp.index{|a| a == "THE TRUST LAND ACT"}
          r["type"] = "THE TRUST LAND ACT"
        elsif tmp.index{|a| a == "THE TRANSFER OF BUSINESSES ACT"}
          r["type"] = "THE TRANSFER OF BUSINESSES ACT"
        elsif tmp.index{|a| a == "THE TRANSPORT LICENSING ACT"}
          r["type"] = "THE TRANSPORT LICENSING ACT"
        elsif tmp.index{|a| a == "THE PRISONS ACT"}
          r["type"] = "THE PRISONS ACT"
        elsif tmp.index{|a| a == "THE NATIONAL MUSEUMS AND HERITAGE ACT"}
          r["type"] = "THE NATIONAL MUSEUMS AND HERITAGE ACT"
        elsif tmp.index{|a| a == "THE TEACHERS SERVICE COMMISSION ACT"}
          r["type"] = "THE TEACHERS SERVICE COMMISSION ACT"
        elsif tmp.index{|a| a == "THE TASK FORCE ON RESETTLEMENT OF BENEFICIARIES"}
          r["type"] = "THE TASK FORCE ON RESETTLEMENT OF BENEFICIARIES"
        elsif tmp.index{|a| a == "THE ENVIRONMENT AND LAND COURT ACT"}
          r["type"] = "THE ENVIRONMENT AND LAND COURT ACT"
        elsif tmp.index{|a| a == "THE RATING ACT"}
          r["type"] = "THE RATING ACT"
        elsif tmp.index{|a| a == "THE CIVIL PROCEDURE ACT"}
          r["type"] = "THE CIVIL PROCEDURE ACT"
        elsif tmp.index{|a| a == "THE CAPITAL MARKETS ACT"}
          r["type"] = "THE CAPITAL MARKETS ACT"
        elsif tmp.index{|a| a == "THE RETIREMENT BENEFITS ACT"}
          r["type"] = "THE RETIREMENT BENEFITS ACT"
        elsif tmp.index{|a| a == "CLOSURE OF ROADS"}
          r["type"] = "CLOSURE OF ROADS"
        elsif tmp.index{|a| a == "IN THE CHIEF MAGISTRATE'S COURT NANYUKI"}
          r["type"] = "IN THE CHIEF MAGISTRATE'S COURT NANYUKI"
        elsif tmp.index{|a| a == "LOSS OF SHARE CERTIFICATE"}
          r["type"] = "LOSS OF SHARE CERTIFICATE"
        elsif tmp.index{|a| a == "THE DISTRICTS AND PROVINCES ACT"}
          r["type"] = "THE DISTRICTS AND PROVINCES ACT"
        elsif tmp.index{|a| a == "THE CENTRAL BANK OF KENYA ACT"}
          r["type"] = "THE CENTRAL BANK OF KENYA ACT"
        elsif tmp.index{|a| a == "NOTIFICATION OF PRACTICE DIRECTION"}
          r["type"] = "NOTIFICATION OF PRACTICE DIRECTION"
        elsif tmp.index{|a| a == "THE AFRICAN CHRISTIAN MARRIAGE AND DIVORCE ACT"}
          r["type"] = "THE AFRICAN CHRISTIAN MARRIAGE AND DIVORCE ACT"
        elsif tmp.index{|a| a == "LOSS OF LIFE POLICY"}
          r["type"] = "LOSS OF LIFE POLICY"
        elsif tmp.index{|a| a == "THE POLICE ACT"}
          r["type"] = "THE POLICE ACT"
        elsif tmp.index{|a| a == "THE ALCOHOLIC DRINKS CONTROL ACT"}
          r["type"] = "THE ALCOHOLIC DRINKS CONTROL ACT"
        elsif tmp.index{|a| a == "AMENDMENT"}
          r["type"] = "AMENDMENT"
        elsif tmp.index{|a| a == "TRANSFER OF BUSINESS ACT"}
          r["type"] = "TRANSFER OF BUSINESS ACT"
        elsif tmp.index{|a| a == "THE NATIONAL CRIME RESEARCH CENTRE ACT"}
          r["type"] = "THE NATIONAL CRIME RESEARCH CENTRE ACT"
        elsif tmp.index{|a| a == "THE GOVERNMENT LANDS ACT"}
          r["type"] = "THE GOVERNMENT LANDS ACT"
        elsif tmp.index{|a| a == "SACCO SOCIETIES REGULATORY AUTHORITY"}
          r["type"] = "SACCO SOCIETIES REGULATORY AUTHORITY"
        elsif tmp.index{|a| a == "THE INDUSTRIAL TRAINING ACT"}
          r["type"] = "THE INDUSTRIAL TRAINING ACT"
        elsif tmp.index{|a| a == "THE INSURANCE ACT"}
          r["type"] = "THE INSURANCE ACT"
        elsif tmp.index{|a| a == "DISPOSAL OF UNCOLLECTD GOODS"}
          r["type"] = "DISPOSAL OF UNCOLLECTD GOODS"
        elsif tmp.index{|a| a == "COMMISSION ACT, 2011"}
          r["type"] = "COMMISSION ACT, 2011"
        elsif tmp.index{|a| a == "THE COMMISSION ON ADMINISTRATIVE JUSTICE ACT, 2011"}
          r["type"] = "THE COMMISSION ON ADMINISTRATIVE JUSTICE ACT, 2011"
        elsif tmp.index{|a| a == "THE MAGISTRATE'S COURT ACT"}
          r["type"] = "THE MAGISTRATE'S COURT ACT"
        elsif tmp.index{|a| a == "THE RATING ACT"}
          r["type"] = "THE RATING ACT"
        elsif tmp.index{|a| a == "THE RATING ACT"}
          r["type"] = "THE RATING ACT"
        elsif tmp.index{|a| a == "THE RATING  ACT"}
          r["type"] = "THE RATING  ACT"
        elsif tmp.index{|a| a == "THE CO-OPERATIVES SOCIETIES ACT"}
          r["type"] = "THE CO-OPERATIVES SOCIETIES ACT"
        elsif tmp.index{|a| a == "THE OATHS AND STATUTORY DECLARATIONS ACT"}
          r["type"] = "THE OATHS AND STATUTORY DECLARATIONS ACT"
        elsif tmp.index{|a| a == "THE CUSTOMS AND EXCISE ACT"}
          r["type"] = "THE CUSTOMS AND EXCISE ACT"
        elsif tmp.index{|a| a == "THE INTERPRETATION AND GENERAL PROVISIONS ACT"}
          r["type"] = "THE INTERPRETATION AND GENERAL PROVISIONS ACT"
        elsif tmp.index{|a| a == "NOTICE OF LOSS OF SEAL"}
          r["type"] = "NOTICE OF LOSS OF SEAL"
        elsif tmp.index{|a| a == "THE VETERINARY SURGEONS ACT"}
          r["type"] = "THE VETERINARY SURGEONS ACT"
        elsif tmp.index{|a| a == "IRREVOCABLE SPECIAL POWER OF ATTORNEY"}
          r["type"] = "IRREVOCABLE SPECIAL POWER OF ATTORNEY"
        elsif tmp.index{|a| a == "PRICE CONTROL ACT"}
          r["type"] = "PRICE CONTROL ACT"
        elsif tmp.index{|a| a ==  "CLOSURE OF PRIVATE ROADS"}
          r["type"] =  "CLOSURE OF PRIVATE ROADS"
        elsif tmp.index{|a| a ==  "THE NATIONAL ACCORD AND RECONCILIATION ACT"}
          r["type"] =  "THE NATIONAL ACCORD AND RECONCILIATION ACT"
        elsif tmp.index{|a| a== "THE POWER OF MERCY ACT" or a == "THE CHILDREN ACT" or a == "THE STATE CORPORATIONS ACT" or a== "LOSS OF POLICIES" or a== "IN THE SENIOR RESIDENT MAGISTRATE'S COURT" or a== "THE ENVIRONMENTAL MANAGEMENT AND" or a== "THE CO-OPERATIVE SOCIETIES ACT" or a== "THE ADVOCATES ACT" or a== "THE ANTI-CORRUPTION AND ECONOMIC CRIMES ACT" or a== "THE COFFEE ACT" or a== "THE REGISTERED LAND ACT" or a== "THE LAND ACQUISITION ACT" or a== "FUEL COST CHARGE" or a== "FOREIGN EXCHANGE RATE FLUCTUATION ADJUSTMENT" or a == "CUSTOMS SERVICES DEPARTMENT" or a == "PUBLIC SERVICE COMMISSION OF KENYA" or a == "FEES AND CHARGES" or a == "INVITATION OF PUBLIC COMMENTS" or a == "THE MOI UNIVERSITY ACT" or a == "THE PUBLIC SERVICE COMMISSION ACT" or a == "THE NATIONAL POLICE SERVICE COMMISSION ACT" or a == "THE VALUATION FOR RATING ACT" or a == "THE SCIENCE AND TECHNOLOGY ACT" or a == "THE MEDICAL PRACTITIONERS AND DENTISTS ACT" or a == "PUPILAGE AND PASSING OF EXAMINATIONS" or a =~ /THE EAST AFRICAN COMMUNITY CUSTOMS MANAGEMENT ACT/ or a == "THE WATER ACT" or a == "THE CIVIL AVIATION ACT" or a=~ /REPORT AND FINANCIAL STATEMENTS FOR THE YEAR ENDED/ or a == "THE LAW OF SUCCESSION ACT" or a =~ /STATEMENT OF ACTUAL REVENUE & NET EXCHEQUER ISSUES AS/ or a =~ /THE LAND ACT/ or a == "THE PHARMACY AND POISONS ACT" or a == "VACATION NOTICE" or a == "THE SURVEY ACT" or a =~ /IN THE MATTER OF ARBITRATION ACT/ or a == "INTENDED DESTRUCTION OF COURT RECORDS" or a =~ /IN THE PRINCIPAL MAGISTRATE'S COURT AT/ or a == "PUPILLAGE AND PASSING OF EXAMINATIONS" or a == "THE STANDARDS ACT" or a == "THE KENYA INFORMATION AND COMMUNICATIONS ACT" or a =~ /APPOINTMENT OF CHAIRPERSON AND MEMBERS/ or a == "RULES OF PROCEDURE" or a == "THE NATIONAL ASSEMBLY AND PRESIDENTIAL ELECTIONS ACT" or a == "ESTABLISHMENT OF A NATIONAL STEERING COMMITTEE" or a == "PROBATE AND ADMINISTRATION" or a == "PROBATE AND ADMIN ISTRATION" or a == "FOREIGN EXCHANGE FLUCTUATION ADJUSTMENT" or a == "INFLATION ADJUSTMENT" or a == "DIRECTORS AND STATUTORY INFORMATION" or a =~ /MONETARY POLICY STATEMENT/ or a == "NOTIFICATION OF EXAMINATION DATES" or a =~ /REPORT AND FINANCIAL STATEMENTS AT/ or a == "THE GOVERNMENT FINANCIAL MANAGEMENT ACT" or a =~ /STATEMENT OF ACTUAL REVENUE AND NET EXCHEQUER ISSUES AS AT/ or a =~ /REVISED FEES AND CHARGES/ or a =~ /THE NATIONAL GENDER AND EQUALITY COMMISSION ACT/ or a == "THE ETHICS AND ANTI-CORRUPTION COMMISSION ACT" or a =~ /INCOME AND EXPENDITURE YEAR ENDED/ or a == "THE OFFICE OF DEPUTY PRIME MINISTER AND MINISTRY" or a == "VACANCY IN THE OFFICE OF JUDGE OF THE COURT OF APPEAL" or a =~ /ENVIRONMENT AND LAND CASE/ or a == "ESTABLISHMENT OF THE TASK FORCE ON THE REALIGNMENT OF THE" or a == "THE TASK FORCE ON THE RESETTLEMENT OF" or a == "ORDER" or a == "THE ENVIRONMENTAL MANAGEMENT AND CO-" or a ==  "THE COUNCIL OF LEGAL EDUCATION (KENYA SCHOOL OF" or a ==  "IN THE PRINCIPAL MAGISTRATE'S COURT" or a =~ /IN THE MATTER OF THE ESTATE OF/ or a == "CHRISTMAS VACATION 2011" or a == "THE MAGISTRATE'S COURTS ACT" or a =~ /^LAND REFERENCE NO/ or a == "REPORT OF THE AUDITOR-GENERAL ON THE FINANCIAL STATEMENTS OF KENYA REVENUE AUTHORITY FOR THE" or a =~ /L\.R\. NO\./ or a == "AWARD OF ORDERS, DECORATIONS AND MEDALS" or a == "THE PHYSICAL PLANNERS REGISTRATION ACT" or a == "PURSUANT to the provisions of section 185 (1) of the Local" or a == "THE NATIONAL ASSEMBLY AND PRESIDENTIAL" or a == "CONSTITUTIONAL AFFAIRS"}
          #Ignore
        else
          #Ignore
          #raise "new section added #{tmp}"
        end
        begin
          t_i = tmp.index{|a| a=~ /Dated the/}
          t_i = tmp.index{|a| a=~ /Dated [0-9]/} if t_i.nil? or t_i == 0
          t_i = tmp.index{|a| a=~ /^[A-Z &,.’?-]+,$/} - 1 if t_i.nil? or t_i == 0 rescue nil
          t_i = tmp.index{|a| a=~ /^[A-Z &,.’?-]+.$/} - 1 if t_i.nil? or t_i == 0
        
          r["description"] = tmp[tmp.index{|a| a==r['type']}+1..t_i-1].join("\n")
          r["type"] = r["type"].strip
          begin
            r["published_dt"] = Date.parse(tmp[t_i].gsub(/Dated the|\./,'').strip).to_s rescue nil
            tm = tmp[t_i+1..-1]
            r["published_by"] = tm[0].gsub(/,$/,'').strip
            if tm.join(" ") =~ /MR|SSF/
            t = tm[1].split(" ")
              r["reference_no"] = t.select{|a| a =~ /^MR|^SSF/}.first
              r["department"] = t.delete_if{|a| a=~ /^MR|^SSF/}.join("\n").gsub(/\.$/,'').strip
            else
              r["reference_no"] = nil
              r["department"] = tm[1..-1].join("\n").gsub(/\.$/,'').strip
            end
          end unless r["description"].nil? 
          #r["section"] = tmp.join("\n").strip
          if r["department"] =~ /NOTE/
            da = r["department"].split("NOTE")
            r["department"] = da[0].strip
            r["note"] = da[1].strip
          end
        rescue Exception => e
          puts r.inspect
          raise e
        end unless r["type"].nil? 
      end if tmp[0].scan(/GAZETTE NOTICE NO/).count == 1 unless tmp.nil? or tmp[0] =~ /[a-z]/
      idx = idx + 1

      records << r.merge(rec).delete_if{|k,v| k=~ /^tmp_/}
    end while(true)
    return records
  elsif act == "filelist"
    records = data.force_encoding("UTF-8").split("\n")
  end
end

def action()
  list = scrape(@br.get("https://s3.amazonaws.com/kenyagazettes/list.txt"),"filelist",{})
  lstart = get_metadata("list",0)
  list[lstart..-1].each{|lfn|
    next if get_metadata(lfn,"nopes") == "complete"
    begin
      pg = @br.get("https://s3.amazonaws.com/kenyagazettes/#{lfn}") rescue nil
      next if pg.nil? 
      fn = pg.filename
      pg.save_as(fn)
      %x[java -Xms256m -Xmx1024m -jar /usr/share/java/pdfbox-app-1.7.0.jar ExtractText "#{fn}" -encoding UTF-8]
      tmp = IO.read("#{fn.gsub('.pdf','.txt')}").force_encoding("UTF-8")
      records = scrape(tmp.split("\n").pretty,"list",{"filename"=>fn})
      ScraperWiki.save_sqlite(unique_keys=['notice_no','volume_no','edition_no','published_location'],records)
      save_metadata(lfn,"complete")
      sleep(60)
    end
    lstart = lstart + 1
    save_metadata("list",lstart)
  }
  #delete_metadata("list")
end

def single(lnk)
  begin
    pg = @br.get(lnk)
    fn = pg.filename
    pg.save_as(fn)
    %x[java -Xms256m -Xmx1024m -jar /usr/share/java/pdfbox-app-1.7.0.jar ExtractText "#{fn}" -encoding UTF-8]
    tmp = IO.read("#{fn.gsub('.pdf','.txt')}").force_encoding("UTF-8")
    records = scrape(tmp.split("\n").pretty,"list",{"filename"=>fn})
    puts records.inspect
  end
end

action()

#single("https://s3.amazonaws.com/kenyagazettes/2011%20Kenya%20Gazette/Gazette%20Vol.%20101-12%E2%80%9310%E2%80%932012%20Special.pdf")
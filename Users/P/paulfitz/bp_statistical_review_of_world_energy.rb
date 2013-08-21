require 'open-uri'           
require 'spreadsheet'           

def apply_test(x,y,z)
  print "[#{z}]: [#{y.inspect}]\n"
end

def apply(x,y,z)
  ScraperWiki.save_sqlite(x,y,z)
end

# url = "statistical_review_of_world_energy_full_report_2011.xls"
url = "http://www.bp.com/assets/bp_internet/globalbp/globalbp_uk_english/reports_and_publications/statistical_energy_review_2011/STAGING/local_assets/spreadsheets/statistical_review_of_world_energy_full_report_2011.xls"

book = nil
open url do |f|
  book = Spreadsheet.open f
  for sheet in book.worksheets
    name = sheet.name
    w = sheet.column_count
    h = sheet.row_count
    rbase = -1
    r2002 = -1
    r2003 = -1
    catch (:done) do
      for r in 0...h
        for c in 0...w
          v = sheet[r,c].to_s.to_i
          if v == 2002
            r2002 = r
          end
          if v == 2003
            r2003 = r
            throw :done  
          end
        end
      end
    end
    rbase = r2002 if r2002 == r2003
    if rbase<0 or rbase>3
      print "Skipping #{sheet.name} (2002 row #{r2002}, 2003 row #{r2003})\n"
      next
    else
      print "Working on #{sheet.name}, header row #{rbase}\n"
    end
    unit = sheet[rbase,0]
    unit.gsub!(/ [^a-z0-9]{1,3} /i," ")
    unit.gsub!(/ [^a-z0-9]{1,3}/i,"")
    unit.gsub!(/[^a-z0-9]{1,3}$/i,"")
    ctags = {}
    for c in 1...w
      ctag = ""
      for r in 0...(rbase+1)
        ctag << " " if ctag!=""
        ctag << sheet[r,c].to_s
      end
      ctag.gsub!(".0","")
      if ctag.include? "Change" or ctag.include? "share of total" or ctag.include? "over"
        ctag = nil
      end
      if ctag == ""
        ctag = nil
      end
      ctags[c] = ctag.to_i if ctag
    end

    title = sheet.name
    title.gsub!(/ [^a-z0-9]{0,3} /i," ")
    for r in (rbase+1)...h
        has_data = false
        for c in 1...w
          if sheet[r,c]
            has_data = true
            break
          end
        end
        next unless has_data
        for c in 1...w
          rtag = sheet[r,0]
          rtag.strip! unless rtag.nil?
          ctag = ctags[c]
          val = sheet[r,c]
          if rtag and ctag
            apply(["country","year"],
                  {
                    :country => rtag,
                    :year => ctag,
                    unit => val
                  },
                  title)
          end
        end
    end
  end
end



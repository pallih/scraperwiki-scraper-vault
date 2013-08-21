require 'pdf-reader'
require 'open-uri'

ScraperWiki.attach("sec_dodd-frank_meetings_v1")
joined2 = ScraperWiki.sqliteexecute("SELECT 'SECMeetings'.'link', 'SECMeetings'.'date' from 'SECMeetings'")
# save the joined data table into a scraperwiki table, format floats, get rid of percent signs
whomet = "Unknown"
joined2['data'].each do |d| 
  io     = open(d[0])
  whenwho = ""
  whenmet = ""
  reader = PDF::Reader.new(io)
  text = reader.pages.first.text
  if text.include? "Re: "
    whomets = text.partition('Re: ')[2]
  elsif text.include? "RE: "
    whomets = text.partition('RE: ')[2]
  else
    whomets = nil
  end
  # This checks and see if there is an RE field
  unless whomets.nil? 
    if whomets.include? "On"
      whowintro = whomets.partition('On')[0]
      if whowintro.include? "Meeting with"
          whomet = whowintro.partition("Meeting with")[2]
      elsif whowintro.include? "Conference call with" or "Conference Call with"
          whomet = whowintro[20..-1]
      elsif whowintro.include? "consultation with"
          whomet = whowintro.partition("consultation with")[2]
      elsif whowintro.include? "Dodd-Frank Wall Street Reform and Consumer Protection Act"
          # then who was met with is somewhere else in the PDF
          whomet = "Elsewhere"
      end
      ScraperWiki.save_sqlite(unique_keys=['link', 'who', 'when'], data={'link' => d[0], 'who' => whomet, 'when' => d[1]} , table_name="SECDoddFrankMeetings")
      else # whomets does not have an on field
        whomet = whomets
        ScraperWiki.save_sqlite(unique_keys=['link', 'who', 'when'], data={'link' => d[0], 'who' => whomet, 'when' => d[1]} , table_name="SECDoddFrankMeetings")
      end
    end
    if whomet.nil? 
      ScraperWiki.save_sqlite(unique_keys=['link', 'who', 'when'], data={"link" => d[0], "who" => "No Re field", "when" => d[1]} , table_name="SECDoddFrankMeetings")
    end
end


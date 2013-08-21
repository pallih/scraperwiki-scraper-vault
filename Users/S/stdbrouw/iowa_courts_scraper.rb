require 'json'
require 'mechanize'
require 'json'
require 'date'
require 'net/http'
require 'net/https'
require 'csv'

module IowaCourts
    IOWA_COURTS_SPREADSHEET = '/spreadsheet/pub?key=0Ao6S2MATTJSMdE1iTE1lc1hDNk9mdndHWWVOczl0b3c&single=true&gid=0&output=csv'

    def IowaCourts.get_cases()
        https = Net::HTTP.new('docs.google.com', 443)
        req = Net::HTTP::Get.new(IOWA_COURTS_SPREADSHEET)
        https.use_ssl = true
        https.verify_mode = OpenSSL::SSL::VERIFY_NONE
        response = https.request(req)

        return CSV.parse(response.body)[1..-1].collect do |row|
            case_id = row[1]
            county = row[2]
            last, first = row[3].split(', ')
            [last, first, county, case_id]            
        end
    end

    def IowaCourts.scrape(last, first, county, match_case_id)
        agent = Mechanize.new
        agent.verify_mode = OpenSSL::SSL::VERIFY_NONE
        agent.history_added = Proc.new {sleep 0.1}
        # get started by visiting the login page, so the server thinks we're human
        # and will serve us HTML (*evil grin*)
        page = agent.get('https://www.iowacourts.state.ia.us/ESAWebApp/ESALogin.jsp')
        # go to the search form
        page = agent.get('https://www.iowacourts.state.ia.us/ESAWebApp/TrialCourtStateWide')

        # enter our query: county and name
        namesearch = page.form('TrailCourtStateWide')
        namesearch.field('county').option_with(:text => county.upcase).select
        namesearch.last = (last or '').downcase
        namesearch.first = (first or '').downcase

        # submit search form
        page = agent.submit(namesearch, namesearch.buttons.first)

        caselist = {}
        page.search('table')[0].search('tr').each do |row|
            cells = row.search('td')
            # make sure we have the kind of row we need
            next if cells.length < 2
            link = cells[0].search('a')
            next unless link.length > 0
            # matches links for a URL like javascript:mySubmit('02121++EQCV020477','BT1117135')
            case_id, person_id = link[0].attribute('href').to_s.scan(/.+\('(.+)','(.+)'/)[0]

            unless case_id.empty? 
                next unless case_id.include?(match_case_id)
            end

            caselist[person_id] ||= {}
            caselist[person_id][case_id] = {
                :type => case_id[7,9],
                :person_id => person_id,
                :person => cells[2].text,
                :county => county,
                :title => cells[1].text,
                :role => cells[4].text,
                :initiated => nil,
                :disposition => nil,
                :charges => [],
                :checked => Date.today.to_s,
                :filings => []
            }
        end

        trialform = page.form('TrialForm')
        caselist.each do |person_id, cases|
            active_case = nil
            cases.each do |case_id, courtcase|
                active_case = courtcase
                # at this point we get zero or more cases in a table as well as
                # citation number; subtype (murder etc.); name; role; initiated date; disposition
                # find the case ID's of each of those cases
                trialform.field_with(:name => 'caseid').value = case_id
                # click through on case and the "banner" frame
                # (the banner frame is where we want to click on "filings" in the navigation bar)
                trial = agent.submit(trialform)
                trial = trial.frame_with(:name => 'banner').click()
                filings = trial.link_with(:text => 'Filings').click()
                rows = filings.search('table')[0].search('tr')

                rows = filings.search('table')[0].search('tr')
                rows[2..-1].each do |row|
                    cells = row.search('td')
                    if cells.length > 2
                        active_case[:filings].push({
                            :event => cells[0].text.strip,
                            :filed_by => cells[1].text.strip,
                            :filed => cells[2].text.strip,
                            :created => cells[3].text.strip,
                            :updated => cells[4].text.strip,
                            :comments => []
                        })
                    else
                        comment = cells[0].text or ''
                        last_filing = active_case[:filings][-1]
                        if last_filing
                            last_filing[:comments].push comment.strip
                        end
                    end
                end

                # find out about charges and adjudication
=begin
                charges = trial.link_with(:text => 'Criminal Charges/Disposition').click()
                cells = charges.search('table')[0].search('td')
                cells.each_with_index do |cell, i|
                    if cell.text.include? 'Count 0'
                        active_charge = {}
                        active_case[:charges].push active_charge
                    end

                    text = cell.text.gsub(/\s+/, '')
                    value = cell.next().text.strip

                    puts "`#{text}` - `#{value}`"

                    case text
                    when 'Description:'
                        active_charge[:charge] = value if value
                    when 'Adj.:'
                        active_charge[:adjudication] = value
                    when 'SentenceDate:'
                        active_charge[:sentence_date] = value
                    when 'Sentence:'
                        active_charge[:sentence] = value
                    when 'Appeal:'
                        active_charge[:appeal] = value
                    end
                end
=end
            end
        end

        return caselist
    end

    def IowaCourts.scrape_all()
        errors = []
        cases = IowaCourts::get_cases.collect do |last, first, county, case_id|
            begin
                IowaCourts::scrape(last, first, county, case_id)
            rescue => error
                errors.push({:description => "Scraping error for #{last}, #{first}, #{county}"})
                nil
            end
        end
        return [cases.compact(), errors]
    end

    def IowaCourts.clear()
        ScraperWiki.sqliteexecute("DROP TABLE IF EXISTS filings")
        ScraperWiki.sqliteexecute("DROP TABLE IF EXISTS errors")
    end

    def IowaCourts.save(data)
        data.each do |caselist|
            caselist.each do |person_id, cases|
                cases.each do |case_id, courtcase|
                    courtcase[:filings].each do |filing|
                        data = {
                            :id => rand(36**8),
                            :case_id => case_id,
                            :person_id => courtcase[:person_id],
                            :case => courtcase[:title],
                            :person => courtcase[:person],
                            :filing => filing[:event], 
                            :filed_by => filing[:filed_by],
                            :date => Date.strptime(filing[:filed], '%m/%d/%Y'),
                            :comments => ''
                        }
                        while filing[:comments].length > 0
                            data[:comments] += filing[:comments].shift()
                        end

                        if (Date.today - data[:date]).to_i < 8
                            ScraperWiki.save_sqlite(unique_keys=['id'], data, table_name="filings")
                        end
                    end
                end
            end
        end
    end

    def IowaCourts.log(errors)
        ScraperWiki.save_sqlite(unique_keys=['description'], errors, table_name="errors")
    end
end

cases, errors = IowaCourts::scrape_all()

if defined? ScraperWiki
    IowaCourts::clear()
    IowaCourts::save(cases)
    IowaCourts::log(errors)    
else
    puts JSON.pretty_generate cases
end
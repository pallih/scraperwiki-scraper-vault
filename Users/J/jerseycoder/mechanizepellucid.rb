# Blank Ruby
require 'mechanize'
require 'net/http'
require 'open-uri'
require 'csv' 

ag = Mechanize.new
ag.keep_alive = false
# Need to set this or you get OpenSSL errors:
ag.agent.http.verify_mode = OpenSSL::SSL::VERIFY_NONE
page = ag.get("https://pellucid.ipro.org/dba/")
# The second form is the login form
form = page.forms[1]
form['pma_username'] = "public"
form['pma_password'] = "tryloyw"
page2 = ag.submit(form)
page3 = ag.get('https://pellucid.ipro.org/dba/db_sql.php?db=public&server=1&db_query_force=1')
form = page3.forms[0]
form['sql_query'] = "SELECT b.name_friendly, a.measure_id, c.name, c.city, c.state, a.entity_id, a.value, a.unit, a.numerator, a.denominator, a.date_start, a.date_end, c.mpn_id
FROM entity_values AS a, measures AS b, entity_hospitals AS c
WHERE a.entity_id = c.entity_id
AND a.measure_id = b.measure_id
AND a.measure_id IN ( 10489, 10492 )
AND c.state = 'NY'
AND c.city IN ('New York', 'Far Rockaway', 'Bronx', 'Jamaica', 'Brooklyn', 'Staten Island', 'Flushing', 'Long Island City')"
page4 = ag.submit(form)
page5 = ag.click(page4.link_with(:text => 'Export'))
form = page5.form_with(:action => 'export.php')
# check off the CSV extract button
form['what'] = 'csv'
#form.field_with(:id => "radio_plugin_csv").check
# Set the delimiter to be a comma
form['csv_separator'] = ","
# We need to reinclude this sql_query variable in the form since the script fails without it
form['sql_query'] = "SELECT b.name_friendly, a.measure_id, c.name, c.city, c.state, a.entity_id, a.value, a.unit, a.numerator, a.denominator, a.date_start, a.date_end, c.mpn_id
FROM entity_values AS a, measures AS b, entity_hospitals AS c
WHERE a.entity_id = c.entity_id
AND a.measure_id = b.measure_id
AND a.measure_id IN ( 10489, 10492 )
AND c.state = 'NY'
AND c.city IN ('New York', 'Far Rockaway', 'Bronx', 'Jamaica', 'Brooklyn', 'Staten Island', 'Flushing', 'Long Island City')"
#puts form['sql_query']
# once we click submit, we will be getting a file back
csvextract = ag.submit(form)
f = csvextract.content

f.each_line {|line|
      # line has the CSV data for one row so now we parse with CSV::parse
      CSV::parse(line) do |r|
      # r now has the column data for each row. Time to save into the scraperwiki dictionary
      # Save recent data only (this filtering should be done on the CSV extract side though)  
      if r[11].include? '2010'
        ScraperWiki.save_sqlite(unique_keys=['Reimbursement Label', 'Hospital' , 'Address' , 'Amount in US Dollars','Date begun','Date End', 'hosid'], data = {'Reimbursement Label' => r[0], 'Hospital' => r[2].upcase, 'Address' => r[3] +', '+ r[4], 'Amount in US Dollars' => r[6].to_i, 'Date begun' => r[10], 'Date End' => r[11], 'hosid' => r[12]}, table_name="nonconsol")
       end  
      end
    }

# The data as it is, will now have double rows for the two different treatment types. This next section will consolodate the data into one row per hospital
#ScraperWiki.attach("mechanizepellucid")
hostids =  ScraperWiki.sqliteexecute("SELECT DISTINCT hosid FROM nonconsol")
hostids['data'].each do |hospid|
  acutemyoval = ScraperWiki.sqliteexecute('SELECT "Amount in US Dollars" FROM nonconsol WHERE hosid="' + hospid[0] + '" AND "Reimbursement Label"= "Median Reimbursement: Acute myocardial infarction, discharged alive without complications or comorbidities"')
  heartfailureval = ScraperWiki.sqliteexecute('SELECT "Amount in US Dollars" FROM nonconsol WHERE hosid="' + hospid[0] + '" AND "Reimbursement Label"= "Median Reimbursement: Heart failure & shock without complications or comorbidities"')
  restofinfo = ScraperWiki.sqliteexecute('SELECT hosid, Hospital, "Date End"  FROM nonconsol WHERE hosid="' + hospid[0] + '"')
  if acutemyoval['data'][0] == nil
    acm = "Not In Dataset"
  else acm = acutemyoval['data'][0][0]
  end
  if heartfailureval['data'][0] == nil
    hf = "Not In Dataset"
  else hf = heartfailureval['data'][0][0]
  end
 ScraperWiki.save_sqlite(unique_keys=['hosid', 'hosname','Cost of Acute Myocardial', 'Cost of Heart Failure and Shock', 'Date End'], data={'hosid' => ("'" + restofinfo['data'][0][0] + "'"), 'hosname' => restofinfo['data'][0][1], 'Cost of Acute Myocardial' => acm, 'Cost of Heart Failure and Shock' => hf, 'Date End' => restofinfo['data'][0][2]} , table_name='consolcosts')
end



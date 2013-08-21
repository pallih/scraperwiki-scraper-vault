# Blank Ruby

ScraperWiki.attach("unziphospitalcomparecsv")
joined = ScraperWiki.sqliteexecute("SELECT 'address'.hosid, 'address'.hosname, 'address'.address, 'address'.city, 'address'.phone, 'address'.ownership,  'POCdata'.measure, 'POCdata'.value from 'POCdata','address' WHERE 'POCdata'.hosid = 'address'.hosid")

joined['data'].each do |d|
   
   ScraperWiki.save_sqlite(unique_keys=['hosid', 'City', 'Phone', 'ownership', 'Address', 'hosname', 'measure', 'value'], data={"hosid" => d[0], "City" => d[1], "Phone" => d[2], "ownership" => d[3], "Address" => d[4], "hosname" => d[5], "measure" => d[6], "value" => d[7]} , table_name="POChosp")
end

# Now we want to consolodate the multiple rows for each hospital into one row for each

ScraperWiki.attach("joinscrapers")
hostids =  ScraperWiki.sqliteexecute("SELECT DISTINCT hosid FROM POChosp")
#puts hostids['data'].count
hostids['data'].each do |hospid|
  ami1 = ScraperWiki.sqliteexecute('SELECT value FROM POChosp WHERE hosid="' + hospid[0] + '" AND measure = "AMI_1"')
  ami10 = ScraperWiki.sqliteexecute('SELECT value FROM POChosp WHERE hosid="' + hospid[0] + '" AND measure = "AMI_10"')
  ami8a = ScraperWiki.sqliteexecute('SELECT hosid, City, Phone, ownership, Address, hosname, measure, value FROM POChosp WHERE hosid="' + hospid[0] + '" AND measure = "AMI_8a"')
  if ami8a['data'][0] == nil 
    a8a = "Not In Dataset" 
  else a8a = ami8a['data'][0][7] 
  end
  if ami10['data'][0] == nil 
    a10 = "Not In Dataset" 
  else a10 = ami10['data'][0][0] 
  end
  if ami1['data'][0] == nil 
    a1 = "Not In Dataset" 
  else a1 = ami1['data'][0][0] 
  end
 ScraperWiki.save_sqlite(unique_keys=['hosid', 'hosname', 'Address', 'City', 'Phone', 'ownership', 'PCI within 90 min', 'Aspirin at arrival', 'Statin at discharge'], data={"hosid" => ami8a['data'][0][0], "City" => ami8a['data'][0][3], "Phone" => ami8a['data'][0][4], "ownership" => ami8a['data'][0][5], "Address" => ami8a['data'][0][2], "hosname" => ami8a['data'][0][1], "PCI within 90 min" => a8a, "Aspirin at arrival" => a1, "Statin at discharge" => a10} , table_name="POChospConsol")
end

#Now join with the MechanizePelucid cost data
# MMK modified the MechanizePeludid scraper to include the mpn_id field on pellucid which == the provider id on the  medicare databases. The consolcosts table has the consolodated data
ScraperWiki.attach("mechanizepellucid")
joined2 = ScraperWiki.sqliteexecute("SELECT 'consolcosts'.hosid, 'consolcosts'.hosname, 'POChospConsol'.address, 'POChospConsol'.city, 'POChospConsol'.phone, 'POChospConsol'.ownership,  'POChospConsol'.'PCI within 90 min', 'POChospConsol'.'Aspirin at arrival', 'POChospConsol'.'Statin at discharge', 'consolcosts'.'Cost of Heart Failure and Shock', 'consolcosts'.'Cost of Acute Myocardial' from 'POChospConsol','consolcosts' WHERE 'POChospConsol'.hosid = 'consolcosts'.hosid")

joined2['data'].each do |d|
   
   ScraperWiki.save_sqlite(unique_keys=['Hospital ID', 'Hospital Name', 'Address', 'City', 'Phone', 'Ownership', 'PCI within 90 min',  'Aspirin at arrival', 'Statin at discharge', 'Cost of Heart Failure and Shock', 'Cost of Acute Myocardial'], data={'Hospital ID' => d[0], 'Hospital Name' => d[1], 'Address' => d[2], 'City' => d[3], 'Phone' => d[4], 'Ownership' => d[5], 'PCI within 90 min' => d[6], 'Aspirin at arrival' => d[7], 'Statin at discharge' => d[8], 'Cost of Heart Failure and Shock' => d[9],  'Cost of Acute Myocardial' => d[10]} , table_name="TotalCostsQualityTable")
end

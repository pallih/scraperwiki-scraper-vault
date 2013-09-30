# Blank Ruby
require 'zip/zip'
require 'mechanize'
require 'net/http'
require 'open-uri'
require 'csv'
require 'set'

zipfile = open('http://www.medicare.gov/download/Hospital_flatfiles.zip')

zipfileobj = Zip::ZipFile.open(zipfile.path, Zip::ZipFile::CREATE)

# This gives us the hospital quality data:
pocdata = zipfileobj.read("HQI_HOSP_MSR_XWLK.csv")
#This data set is actually bad, it has wierd HTML tags in it that are causing the CSV parser to choak at line 5426
# This give us the address data: 
addresses = zipfileobj.read("HQI_HOSP.csv")


# We just want addresses in NYC. According to this website http://nyc.everyblock.com/locations/zipcodes/, NYC zipcodes are present in certain ranges
# Brooklyn:
zips = [11201]+ (11203..11226).to_a + (11228..11239).to_a
# Manhattan
zips = zips + (10001..10007).to_a + (10009..10014).to_a + (10016..10041).to_a + [10044, 10048, 10069, 10103] + (10111...10112).to_a + [10115, 10119, 10128] + (10152..10154).to_a + [10162, 10165, 10167] + (10169..10173).to_a + [10177, 10271, 10278, 10279, 10280, 10282]
# New York
zips = zips + [10043, 10045, 10065, 10075, 10080] + (10105..10107).to_a + [10110, 10120, 10123, 10155, 10158, 10168] + (10174..10176).to_a + [10199, 10265, 10270, 10311, 10550, 10704, 10705, 10803, 11001, 11003, 11005] + (11020..11021).to_a + [11040, 11042, 11096, 11109, 11243, 11252, 11359, 11381, 11405, 11425, 11439, 11451, 11559, 11580, 11581]
# Queens
zips = zips + [11004] + (11101..11106).to_a + (11354..11358).to_a + (11360..11369).to_a + (11371..11375).to_a + (11377..11379).to_a + [11385] + (11411..11423).to_a + (11426..11430).to_a + (11432..11436).to_a + (11691..11694).to_a + [11697]
# Staten Island
zips = zips + (10301..10310).to_a + [10312, 10314]
# The Bronx
zips = zips + (10451..10475).to_a + [11370]

#puts pocdata
# We are going to have to make two scraper datastores and then join them to associate the hospital address data with the quality data
# First, we get the quality data
i = 0
j = 0
baddata = Array.new
pocdata.each_line {|line|
      # line has the CSV data for one row so now we parse with CSV::parse
      i = i + 1
      if ((line.include? 'NY') && ((line.include? 'AMI_8a') || (line.include? 'AMI_10') || (line.include? 'AMI_1'))) then
        # the next line checks for bad data and puts it into a special array
        if line.include? '<img alt="new"'
          # This is a malformed row of data so we cant use the CSV parser. 
          # split the row by comma 
          linespl = line.split(',')
          # There is a quirk with the bad data - occasionally the row will not parse even with the split
          if linespl[4].include?  'Heart' 
            measure = linespl[5][1..6]
            value = linespl[7][1..-1].chop
          else
            measure = linespl[4][1..6]
            value = linespl[6][1..-1].chop
          end 
          ScraperWiki.save_sqlite(unique_keys=['hosid', 'measure', 'value'], data = {'hosid' => linespl[0][1..8], 'measure' => measure, 'value' => value}, table_name="POCdata")
        else
          CSV::parse(line) { |r|
            if r[2] == 'NY'
              if ((r[4] == 'AMI_8a') || (r[4] =='AMI_10') || (r[4] =='AMI_1')) 
                # puts r[1] + " line no: " + i.to_s
                ScraperWiki.save_sqlite(unique_keys=['hosid', 'measure', 'value'], data = {'hosid' => r[0], 'measure' => r[4], 'value' => r[6]}, table_name="POCdata")
              end
            end
          }
        end
      end
    }


#Next we get the adddress data:
addresses.each_line {|line|
      # line has the CSV data for one row so now we parse with CSV::parse
  if line.include? 'NY'      
      CSV::parse(line) do |r|
        #puts r[7]
        if zips.include? r[7].to_i
            #puts r[1] + ", " + r[5]
           ScraperWiki.save_sqlite(unique_keys=['hosid', 'hosname', 'Address', 'City', 'Phone', 'ownership'], data = {'hosid' => r[0], 'hosname' => r[1], 'Address' => r[2], 'City' => r[5], 'Phone' => r[9], 'ownership' => r[11] }, table_name="address")
        end
      end
    end
    }

#joined = ScraperWiki.sqliteexecute("SELECT 'address'.*, 'POCdata'.measure, 'POCdata'.value from 'POCdata','address' WHERE 'POCdata'.hosid = 'address'.hosid")

#puts joined
#ScraperWiki.save_sqlite(unique_keys= joined['keys'], data= joined['data'])

# Now we join and save the joined set
#ScraperWiki.save_sqlite(unique_keys=['Hospital', 'Address', 'Phone', 'Aspirin on Arrival', 'PCI within 90 min', 'Statin at discharge'], data = {'Hospital' => hospital, #'Address' => address, 'Phone' => phone, 'Aspirin on Arrival' => percentnum.to_i, 'PCI within 90 min' => pci.to_i, 'Statin at discharge' => statin.to_i }, #table_name="quality")
# Blank Ruby
require 'zip/zip'
require 'mechanize'
require 'net/http'
require 'open-uri'
require 'csv'
require 'set'

zipfile = open('http://www.medicare.gov/download/Hospital_flatfiles.zip')

zipfileobj = Zip::ZipFile.open(zipfile.path, Zip::ZipFile::CREATE)

# This gives us the hospital quality data:
pocdata = zipfileobj.read("HQI_HOSP_MSR_XWLK.csv")
#This data set is actually bad, it has wierd HTML tags in it that are causing the CSV parser to choak at line 5426
# This give us the address data: 
addresses = zipfileobj.read("HQI_HOSP.csv")


# We just want addresses in NYC. According to this website http://nyc.everyblock.com/locations/zipcodes/, NYC zipcodes are present in certain ranges
# Brooklyn:
zips = [11201]+ (11203..11226).to_a + (11228..11239).to_a
# Manhattan
zips = zips + (10001..10007).to_a + (10009..10014).to_a + (10016..10041).to_a + [10044, 10048, 10069, 10103] + (10111...10112).to_a + [10115, 10119, 10128] + (10152..10154).to_a + [10162, 10165, 10167] + (10169..10173).to_a + [10177, 10271, 10278, 10279, 10280, 10282]
# New York
zips = zips + [10043, 10045, 10065, 10075, 10080] + (10105..10107).to_a + [10110, 10120, 10123, 10155, 10158, 10168] + (10174..10176).to_a + [10199, 10265, 10270, 10311, 10550, 10704, 10705, 10803, 11001, 11003, 11005] + (11020..11021).to_a + [11040, 11042, 11096, 11109, 11243, 11252, 11359, 11381, 11405, 11425, 11439, 11451, 11559, 11580, 11581]
# Queens
zips = zips + [11004] + (11101..11106).to_a + (11354..11358).to_a + (11360..11369).to_a + (11371..11375).to_a + (11377..11379).to_a + [11385] + (11411..11423).to_a + (11426..11430).to_a + (11432..11436).to_a + (11691..11694).to_a + [11697]
# Staten Island
zips = zips + (10301..10310).to_a + [10312, 10314]
# The Bronx
zips = zips + (10451..10475).to_a + [11370]

#puts pocdata
# We are going to have to make two scraper datastores and then join them to associate the hospital address data with the quality data
# First, we get the quality data
i = 0
j = 0
baddata = Array.new
pocdata.each_line {|line|
      # line has the CSV data for one row so now we parse with CSV::parse
      i = i + 1
      if ((line.include? 'NY') && ((line.include? 'AMI_8a') || (line.include? 'AMI_10') || (line.include? 'AMI_1'))) then
        # the next line checks for bad data and puts it into a special array
        if line.include? '<img alt="new"'
          # This is a malformed row of data so we cant use the CSV parser. 
          # split the row by comma 
          linespl = line.split(',')
          # There is a quirk with the bad data - occasionally the row will not parse even with the split
          if linespl[4].include?  'Heart' 
            measure = linespl[5][1..6]
            value = linespl[7][1..-1].chop
          else
            measure = linespl[4][1..6]
            value = linespl[6][1..-1].chop
          end 
          ScraperWiki.save_sqlite(unique_keys=['hosid', 'measure', 'value'], data = {'hosid' => linespl[0][1..8], 'measure' => measure, 'value' => value}, table_name="POCdata")
        else
          CSV::parse(line) { |r|
            if r[2] == 'NY'
              if ((r[4] == 'AMI_8a') || (r[4] =='AMI_10') || (r[4] =='AMI_1')) 
                # puts r[1] + " line no: " + i.to_s
                ScraperWiki.save_sqlite(unique_keys=['hosid', 'measure', 'value'], data = {'hosid' => r[0], 'measure' => r[4], 'value' => r[6]}, table_name="POCdata")
              end
            end
          }
        end
      end
    }


#Next we get the adddress data:
addresses.each_line {|line|
      # line has the CSV data for one row so now we parse with CSV::parse
  if line.include? 'NY'      
      CSV::parse(line) do |r|
        #puts r[7]
        if zips.include? r[7].to_i
            #puts r[1] + ", " + r[5]
           ScraperWiki.save_sqlite(unique_keys=['hosid', 'hosname', 'Address', 'City', 'Phone', 'ownership'], data = {'hosid' => r[0], 'hosname' => r[1], 'Address' => r[2], 'City' => r[5], 'Phone' => r[9], 'ownership' => r[11] }, table_name="address")
        end
      end
    end
    }

#joined = ScraperWiki.sqliteexecute("SELECT 'address'.*, 'POCdata'.measure, 'POCdata'.value from 'POCdata','address' WHERE 'POCdata'.hosid = 'address'.hosid")

#puts joined
#ScraperWiki.save_sqlite(unique_keys= joined['keys'], data= joined['data'])

# Now we join and save the joined set
#ScraperWiki.save_sqlite(unique_keys=['Hospital', 'Address', 'Phone', 'Aspirin on Arrival', 'PCI within 90 min', 'Statin at discharge'], data = {'Hospital' => hospital, #'Address' => address, 'Phone' => phone, 'Aspirin on Arrival' => percentnum.to_i, 'PCI within 90 min' => pci.to_i, 'Statin at discharge' => statin.to_i }, #table_name="quality")

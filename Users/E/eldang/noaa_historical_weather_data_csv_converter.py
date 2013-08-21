#! /usr/bin/env python

# Downloader for NOAA historical weather data
# Written by Eldan Goldenberg, Sep-Oct 2012
# http://eldan.co.uk/ ~ @eldang ~ eldang@gmail.com

# This program is free software; you can redistribute it and/or
#        modify it under the terms of the GNU General Public License
#        as published by the Free Software Foundation; either version 2
#        of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful,
#        but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#        GNU General Public License for more details.
# The licence text is available online at:
#        http://www.gnu.org/licenses/gpl-2.0.html

# Background:
# NOAA publishes an amazing trove of historical weather data from stations all
#        over the world - http://www.ncdc.noaa.gov/cgi-bin/res40.pl - but in a rather
#        awkward format: each year is a separate folder, in which each station
#        is one file, identified by two arbitrary ref numbers. Each file is gzipped
#        text in a rather non-standard format with some inconvenient features like
#        NULL tokens varying per field, and numbers being concatenated together
#        with flags that give interpretation information:
#        ftp://ftp.ncdc.noaa.gov/pub/data/gsod/readme.txt
# This script lets the user specify a station and a number of years to download.
#        It then iterates through, downloading enough years, parsing them into a much
#        more standard CSV format read for use in (e.g.) Excel or Tableau, and
#        concatenating them into one continuous file per station.

# USE:
# Simply call this script, with the optional argument --verbose if you want
# debug output. It will prompt you for everything else it needs interactively.

# TODO short term: make it take a list of stations at the beginning, so it can
#        be left running unattended after that.
# TODO long term: replace manual USAF & WBAN code input with a lookup that lets
#        users just enter a station name, and gets the two codes from that file.
# TODO total pipedream: let user give a location, and automagically find the
#        nearest station based on lat & long.
# TODO for scraperwiki: have it load in the whole list of stations and just
#        iterate over them.

import datetime
import urllib
import os
import gzip
import time
import csv
import sys

# Check for --verbose argument. You'll get more feedback if you use this.
if len(sys.argv) == 1:
    # then default to non-verbose
    verbose = False
elif sys.argv[1] == "--verbose":
    verbose = True
else:
    verbose = False

# I've assumed you'll want the same number of years for every station you
#        download in one session, so we ask this before going into the main loop.
maxyears = int(raw_input("How many years of data would you like to download " \
    "for each station?\n"))

# This function goes through each downloaded file line by line, and translates
#        it from NOAA's idiosyncratic format to CSV with all the fields separated
#        out rationally.
def parsefile(f_in, f_out, stationname):
    # Set up connections to input and output files. The CSV library also helps
    #        with reading the input file, because we can treat it as space separated
    #        with consecutive spaces being collapsed together
    reader = csv.reader(f_in, delimiter=' ', quoting=csv.QUOTE_NONE, skipinitialspace=True)
    writer = csv.writer(f_out, dialect=csv.excel)
    for row in reader:
        if (row[0] != 'STN---'):
            # If it's the header row, just skip; otherwise process
            outrow = [stationname] # the station name is not in the input file

            # skipping first 2 cols of the input file as they are the USAF & WBAN codes
            #        which we're replacing with the actual station name.

            # expanding col 3 into separate Y, M & D fields makes them easier to work
            #        with in Tableau
            outrow.append((row[2])[:4]) # first 4 digits are the year
            outrow.append((row[2])[4:6]) # next 2 are the month
            outrow.append((row[2])[-2:]) # final 2 are the day

            # now we can use a loop to get through a bunch of field pairs that all
            #        work the same:
            # MeanTemp, NTempObs, DewPoint, NDewPointObs, SeaLevelPressure,
            #        NSeaLevPressObs, StationPressure, NStatPressObs
            for i in range(3, 11, 2):
                # for each of these, 9999.9 means NULL, and the number of observations
                #        follows the value
                if (row[i+1] == "0") or (row[i] == "9999.9"):
                    outrow.append("NULL")
                    outrow.append(0)
                else:
                    outrow.append(row[i])
                    outrow.append(row[i+1])

            # Now the same principle for Visibility, which uses a different NULL token
            # Visibility, NVisibilityObs
            if (row[12] == "0") or (row[11] == "999.9"):
                outrow.append("NULL")
                outrow.append(0)
            else:
                outrow.append(row[11])
                outrow.append(row[12])

            # Now for wind data, which is 4 fields of which the second is the number
            #        of observations from which the other 3 values were determined
            # MeanWindSpeed, NWindObs, MaxSustWindSpeed, MaxWindGust
            if row[14] == "0":
                # if there are 0 observations, then set a bunch of nulls
                outrow.append("NULL")
                outrow.append("0")
                outrow.append("NULL")
                outrow.append("NULL")
            else:
                for i in range(13, 17, 1):
                    if row[i] == "999.9": outrow.append("NULL")
                    else: outrow.append(row[i])

            # Temp fields may or may not have a "*" appended after the number, so we
            #        handle these by first checking what the last character is:
            # "MaxTemp", "MaxTempSource", "MinTemp", "MinTempSource"
            for i in range(17, 19, 1):
                if (row[i])[-1] == "*":
                    # then the flag is present, indicating the source was derived
                    #        indirectly from hourly data
                    outrow.append((row[i])[:-1])
                    outrow.append("hourly")
                else:
                    # if it's not present then this was an explicit max/min reading
                    outrow.append(row[i])
                    outrow.append("explicit")

            # Precipitation has its own extra special flag source and NULL placeholder
            # PrecipAmount, NPrecipReportHours, PrecipFlag
            if row[19] == "99.99":
                # then it's null, so:
                outrow.append("NULL")
                outrow.append("NULL")
                outrow.append("NULL")
            else:
                outrow.append((row[19])[:-1])
                # translations of the flag, as per
                #        ftp://ftp.ncdc.noaa.gov/pub/data/gsod/readme.txt
                if (row[19])[-1] == "A": outrow.append("6")
                elif (row[19])[-1] == "B": outrow.append("12")
                elif (row[19])[-1] == "C": outrow.append("18")
                elif (row[19])[-1] == "D": outrow.append("24")
                elif (row[19])[-1] == "E": outrow.append("12")
                elif (row[19])[-1] == "F": outrow.append("24")
                elif (row[19])[-1] == "G": outrow.append("24")
                elif (row[19])[-1] == "H": outrow.append("0")
                elif (row[19])[-1] == "I": outrow.append("0")
                else: outrow.append("ERR")
                outrow.append((row[19])[-1])

            # SnowDepth is relatively straightforward
            if row[20] == "999.9":
                outrow.append("NULL")
            else:
                outrow.append(row[20])

            # Fog, Rain, Snow, Hail, Thunder, Tornado
            # these are stored as one six-bit binary string, so we unpack it here
            for i in range(0, 6, 1):
                outrow.append((row[21])[i])

            # And we're done!  Now write the row to the output file
            writer.writerow(outrow)
    if verbose:
        sys.stdout.write("parsed.\n")
    else:
        # even if not verbose, we say something so the user can see it's working
        sys.stdout.write(".")
    sys.stdout.flush() # need to flush the output buffer to show progress live


# This is the main control function. Each pass gets the user's input to pick a
#        station, and then loops over years to download the relevant files, calling
#        parsefile() to parse each one into standard CSV
def downloadfiles(maxyears):
    # get parameters for and start constructing filenames
    URLroot = "ftp://ftp.ncdc.noaa.gov/pub/data/gsod/" # base URL for all files
    filesuffix = ".op.gz" # suffix for all the raw files
    firstyear = 1928 # this is the first year available for any station
    USAFcode = raw_input("Please enter the USAF code for the station you want " \
        "data for (first column of  " \
        "ftp://ftp.ncdc.noaa.gov/pub/data/inventories/ISH-HISTORY.TXT )\n")
    WBANcode = raw_input("Please enter the WBAN code for the station you want " \
        "data for (second column of " \
        "ftp://ftp.ncdc.noaa.gov/pub/data/inventories/ISH-HISTORY.TXT )\n")
    # e.g. Seattle (SEA) is USAF 727930 WBAN 24233
    # Portland, OR is USAF 726980 WBAN 24229
    # LHR is USAF 037720 WBAN 99999
    stationname = raw_input("What would you like to call this station?\n")
    stationcode = str(USAFcode) + '-' + str(WBANcode)

    yearsdownloaded = 0

    for year in range(datetime.datetime.now().year-1, firstyear, -1):
        # stopping before the current year because it's necessarily incomplete, and
        #        looping back from last year, on the assumption that more recent years
        #        are of greater interest and have higher quality data.
        # First we assemble the URL for the year of interest
        fullURL = (URLroot + str(year) + '/' + stationcode + '-' +
            str(year) + filesuffix)
        if verbose:
            sys.stdout.write("Trying " + fullURL + " ... ")
            sys.stdout.flush()

        # Now we try to download the file, with very basic error handling if verbose
        try:
            urllib.urlretrieve(fullURL,str(year)+filesuffix)
            if verbose: sys.stdout.write("retrieved ... ")
            yearsdownloaded += 1
        except IOError as e:
            if verbose: print(" ")
            print(e)
        else: # if we got the file without any errors, then
            # uncompress the file
            f_in = gzip.open(str(year)+filesuffix)
            if verbose: sys.stdout.write("decompressed ... ")
            # and start writing the output
            if yearsdownloaded == 1:
                # since it's the first year, open the file and write the header row
                firstyear = year
                f_out = open(stationname+'.csv','w')
                csv.writer(f_out).writerow(["Station", "Year", "Month", "Day", \
                    "MeanTemp", "NTempObs", "DewPoint", "NDewPointObs", \
                    "SeaLevelPressure", "NSeaLevPressObs", "StationPressure", \
                    "NStatPressObs", "Visibility", "NVisibilityObs", "MeanWindSpeed", \
                    "NWindObs", "MaxSustWindSpeed", "MaxWindGust", "MaxTemp",  \
                    "MaxTempSource", "MinTemp", "MinTempSource", "PrecipAmount", \
                    "NPrecipReportHours", "PrecipFlag", "SnowDepth", "Fog", "Rain", \
                    "Snow", "Hail", "Thunder", "Tornado"])
            # This function does the actual ETL
            parsefile(f_in, f_out, stationname)
            # clean up after ourselves
            f_in.close()
            os.remove(str(year)+filesuffix)
        urllib.urlcleanup()
        if yearsdownloaded == maxyears:
            break # if we have enough years, then end this loop
        else:
            time.sleep(5) # slow down here to stop the server locking us out
        time.sleep(1)
    print("Successfully downloaded " + str(yearsdownloaded) + " years between " +
        str(year) + " and " + str(firstyear) + " for station " + stationname)
    if yearsdownloaded < maxyears:
        # If we didn't get as many years as requested, alert the user
        print("No more years are available at the NOAA website for this station.")
    f_out.close()


# This is the main control loop. It repeatedly asks the user for station codes
#        and calls downloadfiles() to download the requested data, until it's told
#        to stop.
goagain = "Y"
while not (goagain.startswith('N') or goagain.startswith('n')):
    downloadfiles(maxyears)
    goagain = raw_input("Would you like to download another station (Y/N)?\n")
    while not (goagain.startswith('N') or goagain.startswith('n') or
        goagain.startswith('y') or goagain.startswith('Y')):
        goagain = raw_input("Please help me, I am but a stupid computer. " \
            "I can only understand Y or N as responses to this prompt. "
            "Would you like to download another station (Y/N)?\n")

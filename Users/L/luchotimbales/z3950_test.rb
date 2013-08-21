# ZOOM's equivalent of the  ``Hello World'' program: a tiny Z39.50 client that fetches and displays
#  the MARC record for Farlow & Brett Surman's The Complete Dinosaur from the Library of Congress.
# Taken from :http://ruby-zoom.rubyforge.org/

require 'zoom'

ZOOM::Connection.open('z3950.loc.gov', 7090) do |conn|
      conn.database_name = 'Voyager'
      conn.preferred_record_syntax = 'USMARC'
      rset = conn.search('@attr 1=7 0253333490')
      p rset[0]
end



# ZOOM's equivalent of the  ``Hello World'' program: a tiny Z39.50 client that fetches and displays
#  the MARC record for Farlow & Brett Surman's The Complete Dinosaur from the Library of Congress.
# Taken from :http://ruby-zoom.rubyforge.org/

require 'zoom'

ZOOM::Connection.open('z3950.loc.gov', 7090) do |conn|
      conn.database_name = 'Voyager'
      conn.preferred_record_syntax = 'USMARC'
      rset = conn.search('@attr 1=7 0253333490')
      p rset[0]
end




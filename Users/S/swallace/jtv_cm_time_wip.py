"""
The goal of this project is to gather date to compare the time movies are shown on TV with the official running time of the film.
Any difference should be explained by commercial times and editing of films.
Inspiration comes form a reddit thread I saw the other day where the guy did this for Spike TV movies.
"""


#part 1: scrape data from this page: http://timetable.yanbe.net

BASE_SITE = "http://timetable.yanbe.net"
PREF_CODE_TOKYO = 13
PREF_CODE_OSAKA = 27
YEAR = 2013
MONTH = 06
DAY = 19
BROADCAST_TYPE = 1


"""
site uses a GET for URLS

URL interface:

the default base page is the same for http://timetable.yanbe.net/?p=13

http://timetable.yanbe.net/html/13/2013/01/01_1.html
shows the page for Jan 1, 2013 for Tokyo. Tokyo is the 13 part

URL breakdown: http://timetable.yanbe.net/html/<prefecture code>/<4 digit year>/<two digit month>/<two digit day>_<broadcast type>.html
broadcast type: just keep it at 1
example: April 2nd, 2013 for Osaka: http://timetable.yanbe.net/html/27/2013/04/02_1.html

other ?xx codes:

?1 = Hokkaido
?13 = Tokyo
?27 = Osaka
?47 = Okinawa

"""

#the cells with the target data are all in the class program_td
"""
The goal of this project is to gather date to compare the time movies are shown on TV with the official running time of the film.
Any difference should be explained by commercial times and editing of films.
Inspiration comes form a reddit thread I saw the other day where the guy did this for Spike TV movies.
"""


#part 1: scrape data from this page: http://timetable.yanbe.net

BASE_SITE = "http://timetable.yanbe.net"
PREF_CODE_TOKYO = 13
PREF_CODE_OSAKA = 27
YEAR = 2013
MONTH = 06
DAY = 19
BROADCAST_TYPE = 1


"""
site uses a GET for URLS

URL interface:

the default base page is the same for http://timetable.yanbe.net/?p=13

http://timetable.yanbe.net/html/13/2013/01/01_1.html
shows the page for Jan 1, 2013 for Tokyo. Tokyo is the 13 part

URL breakdown: http://timetable.yanbe.net/html/<prefecture code>/<4 digit year>/<two digit month>/<two digit day>_<broadcast type>.html
broadcast type: just keep it at 1
example: April 2nd, 2013 for Osaka: http://timetable.yanbe.net/html/27/2013/04/02_1.html

other ?xx codes:

?1 = Hokkaido
?13 = Tokyo
?27 = Osaka
?47 = Okinawa

"""

#the cells with the target data are all in the class program_td

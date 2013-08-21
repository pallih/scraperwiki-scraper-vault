# Hi. Welcome to the Ruby editor window on ScraperWiki.


# Did it work? 10 lines should have been printed in the console window below.
# If not, try using Google Chrome or the latest version of Firefox.

# The first job of any scraper is to download the text of a web-page:  

html = ScraperWiki.scrape 'http://www.leg.state.nv.us/AppCF/Lobbyist/reports/ListLobbyists.cfm?Paid=1'
puts html

# The text will appear in the console, and the URL that it downloaded from
# should appear under "Sources".
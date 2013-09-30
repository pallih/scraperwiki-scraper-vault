# Author: Michael Sobotka
# Purpose: Automatically fills out the search-form on www.laut.de
#   with a given artist and displays all albums by this artist.

require 'mechanize'

ARTIST_NAME = 'Metallica'
BASE_URL = "http://www.laut.de/"
SEARCH_FORM_ID = 'suche'

def find_albums_by(artist_name)

  # Initialize a Mechanize agent
  agent = Mechanize.new
  
  agent.get(BASE_URL) do |page|
    
    # Fill out the form. The only field is called 'suchbegriff'
    search_form = page.form_with(:id => SEARCH_FORM_ID)
    search_form.suchbegriff = artist_name
    search_results = agent.submit(search_form, search_form.buttons.first)

    # Parse the result page with Nokogiri
    search_results_page = Nokogiri::HTML(search_results.body)
    
    # Find the albums for the given artist
    albums = search_results_page.css('li.album.cf')

    # Display the results like: Artist - Album
    for album in albums
      title = album.css('.title .title').inner_text
      artist = album.css('.title .artist').inner_text
      p (artist + ' - ' +  title)
    end

  end
end

# Start the search...
find_albums_by(ARTIST_NAME)
# Author: Michael Sobotka
# Purpose: Automatically fills out the search-form on www.laut.de
#   with a given artist and displays all albums by this artist.

require 'mechanize'

ARTIST_NAME = 'Metallica'
BASE_URL = "http://www.laut.de/"
SEARCH_FORM_ID = 'suche'

def find_albums_by(artist_name)

  # Initialize a Mechanize agent
  agent = Mechanize.new
  
  agent.get(BASE_URL) do |page|
    
    # Fill out the form. The only field is called 'suchbegriff'
    search_form = page.form_with(:id => SEARCH_FORM_ID)
    search_form.suchbegriff = artist_name
    search_results = agent.submit(search_form, search_form.buttons.first)

    # Parse the result page with Nokogiri
    search_results_page = Nokogiri::HTML(search_results.body)
    
    # Find the albums for the given artist
    albums = search_results_page.css('li.album.cf')

    # Display the results like: Artist - Album
    for album in albums
      title = album.css('.title .title').inner_text
      artist = album.css('.title .artist').inner_text
      p (artist + ' - ' +  title)
    end

  end
end

# Start the search...
find_albums_by(ARTIST_NAME)

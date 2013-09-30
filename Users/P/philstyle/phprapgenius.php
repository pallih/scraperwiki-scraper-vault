<?php
######################################
# Basic PHP scraper for RapGenius
#
# a) extract lyrics from a RapGenius URL
# a') extract metadata about the page - MINIMUM of Artist, Track
# b) save those lyrics in some structure (probably blob) by artist, track, and any other metadata available
# c) track the URL used, last time retrieved, and last time the page was updated (if that info is available)

##CRAZY - make a spider - start with an artist- go to  http://rapgenius.com/artists/Atmosphere
/*
1) Grab all a.song_name and follow links - GET META AND LYRICS - meta = artist, supporting artists
2) Get album list - ul.album_list - <li><a href=link>Album Name</a></li> - THAT"S HOW WE SAVE THE ALBUM NAME
3) Follow each album link and 
4) get song list - ul.song_list - iterate through the <a> or <li><a> list inside ul
5) follow each track link (ends in -lyrics) - GET META AND LYRICS
6) break up the lyrics by artist in [] blocks, and give each block and ID so that you can put the track back together again
7) save that data


*/
## get all the album links and get those
## 
######################################

require  'scraperwiki/simple_html_dom.php';


##CREATE AND DELETE SCRIPTS
/*
scraperwiki::sqliteexecute("DROP TABLE if exists 'Track'");
scraperwiki::sqliteexecute("CREATE TABLE 'Track' ('UniqURL' text, 'Album' text, 'Artist' text, 'Track' text, 'Featuring' integer)");

scraperwiki::sqliteexecute("DROP TABLE if exists 'Lyrics'");
scraperwiki::sqliteexecute("CREATE TABLE 'Lyrics' ('UniqURI' text, 'TrackURL' text, 'TrackSegment' integer, 'Artist' text, 'Lyrics' text)");

scraperwiki::sqliteexecute("DROP TABLE if exists 'Featured_Artist'");
scraperwiki::sqliteexecute("CREATE TABLE 'Featured_Artist' ('UniqURI' text, 'TrackURL' text, 'Artist' text)");
*/

##WEB PAGE FUNCTIONS##

function STOREArtistAlbumTracks($ArtistURL) {
  $dom = new simple_html_dom();
  $BASE_URL = "http://rapgenius.com";
  $artistStartPage = scraperwiki::scrape($BASE_URL . $ArtistURL);
  $dom->load($artistStartPage);
  $albumArray = getAlbums($dom);
  $albumURLArray = $albumArray['urls'];
  $albumNameArray = $albumArray['names'];
  #print_r($albumArray);
  foreach ($albumURLArray as $i => $album) {

    $albumDom = new simple_html_dom();
 # print $album . "\n";

 
    $albumPage = scraperwiki::scrape($BASE_URL . $album);
    $albumDom->load($albumPage);
 
  #print $albumDom ."\n\n";
  #$albumA = $albumDom->find('ul.album_list',0);
    print "album => " . $albumNameArray[$i] . "\n";

    $trackArray = getSongList($albumDom);
    $albumName = $albumNameArray[$i];

  #print_r($trackArray);

    foreach ($trackArray as $j => $track) {
      $trackPage = scraperwiki::scrape($BASE_URL . $track);
      $trackDom = new simple_html_dom();
    #print $track . "\n";
      $trackDom->load($trackPage);
      //use trackDom to get lyrics and metadata?
      $trackMeta = getTrackMetaData($trackDom);
    #print_r($trackMeta);
      $trackMeta['album'] = $albumName;
      addTrack($track, $trackMeta);
    }
  }
}

function getPageDom($URL) {
  $dom = new simple_html_dom();
  $page = scraperwiki::scrape($URL);
  $dom->load($page);
  return $dom;
}

## PRINTS the lyrics DIV from a track page in plaintext
## $dom - simplesomethingDOM
function getLyrics($dom) {
  $lyrics = "";
  foreach($dom->find('div.lyrics ') as $data){
    #print $data->plaintext;
    $lyrics = $lyrics . $data->plaintext;
  }   
  return $lyrics;
}

## Gets the Track, Artist, and <TODO> Featured Artists
## $dom - simplesomethingDOM
function getTrackMetaData($dom) {
  $output = getArtistAndTrackname($dom);
  ##TODO - need to get supporting artists (array)
  $output['featuring'] = getFeaturedArtists($dom);
  return $output;
}

## Gets the Track, Artist
## $dom - simplesomethingDOM
function getArtistAndTrackName($dom) {
  $artistTrack = $dom->find('h1.song_title',0);
  $artist = $artistTrack->find('a',0)->plaintext;
  $startBuffer = 8;
  $endBuffer = -11;
  $track = substr($artistTrack->plaintext, ($startBuffer + strlen($artist)) , $endBuffer);
  $output['track'] = $track;
  $output['artist'] = $artist;

  return $output;
}

## Gets the list of <a> featured artists 
## ASSUMING THAT ALL ARTISTS HAVE HYPERLINKS!
## returns an array of artists from the <a> hyperlinks inside the featured_artists div
function getFeaturedArtists($dom) {
  $feat = $dom->find('div.featured_artists',0);
  $artists = array();
  if ($feat != NULL && sizeof($feat) > 0) {
    foreach($feat->find('a') as $artist) {
      $artists[] = $artist->plaintext;
    }
  }
  return $artists;
}


## Expects the DOM of an artist page
## Returns an array of album URLs and album names (same keys)
function getAlbums($dom) {
  $albumURLs = array();
  $albumNames = array();
  $albums = $dom->find('ul.album_list',0);
  foreach($albums->find('li a') as $data){
    #print $data->href. "\n";
    $albumURLs[] = $data->href;
    $albumNames[] = $data->plaintext;
  }
  return array("urls"=>$albumURLs, "names"=>$albumNames);
}

## Expects the DOM of an album page
## Returns an array of track URLs
function getSongList($dom) {
  $trackURLs = array();
  $songs = $dom->find('ul.song_list  ',0);
  #print $songs; 
  #print_r($songs);
  foreach($songs->find('li a') as $track) {
    #print $track->href . "\n";
    $trackURLs[] = $track->href;
    #print $track->href. "\n";
  }
  return $trackURLs;
}

##addLyrics expects the $URL and $dom for the track

###NOTE### - UNIQ URI should be the song URL plus '#', and a unique identifier (within the table)

##DATABASE FUNCTIONS##
function insertIntoTrack($URL, $album, $artist, $track, $featuring) {
  scraperwiki::save_sqlite(array("UniqURL"), array("UniqURL"=>$URL, "Album"=>$album, "Artist"=>$artist, "Track"=>$track, "Featuring"=>$featuring), $table_name="Track");
}

##Expects Track URL, artist, and lyrics
##For now attribute all lyrics to the main artist (segment 0)
function insertIntoLyrics($URL, $artist, $lyrics) {
  $URI = $URL . "#" . str_replace(" ", "_", $artist);
  scraperwiki::save_sqlite(array("UniqURI"), array("UniqURI"=>$URI, "TrackURL"=>$URL, "TrackSegment"=>0, "Artist"=>$artist, "Lyrics"=>$lyrics), $table_name="Lyrics");
}

function insertIntoFeaturedArtist($URL, $artist) {
  $URI = $URL . "#" . str_replace(" ", "_", $artist);
  scraperwiki::save_sqlite(array("UniqURI"), array("UniqURI"=>$URI, "TrackURL"=>$URL, "Artist"=>$artist), $table_name="Featured_Artist");
}

## Expects track URL, and trackMeta (album, artist, track, and featuring count)
function addTrack($URL, $trackMeta) {
  insertIntoTrack($URL, $trackMeta['album'], $trackMeta['artist'], $trackMeta['track'], count($trackMeta['featuring']));
  if (count($trackMeta['featuring']) > 0) {
    foreach ($trackMeta['featuring'] as $i => $artist) {
      insertIntoFeaturedArtist($URL, $artist);
    }
  }
}

##DATABASE QUERIES##
function printTrackTable() {
  print "\nselect * from Track\n\n";
  $retVal = scraperwiki::select("* from Track");
  foreach($retVal as $i => $value){
    print $i . " -> " . $value . "\n";
    print_r($value);
  } 
}

function printFeaturedArtistTable() {
  print "\nselect * from Featured_Artist\n\n";
  $retVal = scraperwiki::select("* from Featured_Artist");
  foreach($retVal as $i => $value){
    print $i . " -> " . $value . "\n";
    print_r($value);
  }
}


#random URL...
#$TylerURL = "http://rapgenius.com/lyrics/Earl-sweatshirt-ft-tyler-the-creator/Couch";
##$TylerURL = "http://rapgenius.com/Jennifer-lopez-aint-it-funny-remix-lyrics";


/*
$BASE_URL = "http://rapgenius.com";
$dom = getPageDom($BASE_URL . "/Big-l-games-lyrics");

getLyrics($dom);
*/

##TESTS##
###THIS WORKS FOR RAPGENIUS but you don't get album - http://rapgenius.com/songs?page=300

## 2-song test to get lyrics and/or metadata

/*
$dom = new simple_html_dom();
$html[0] = scraperwiki::scrape($TylerURL);
$html[1] = scraperwiki::scrape("http://rapgenius.com/Ugk-one-day-lyrics");
$dom->load($html[0]);

#getLyrics($dom);

$trackMeta = getTrackMetaData($dom);
print_r($trackMeta);

insertIntoTrack($TylerURL, "AlbumName", $trackMeta['artist'], $trackMeta['track'], count($trackMeta['featuring']));
if (count($trackMeta['featuring']) > 0) {
  foreach ($trackMeta['featuring'] as $i => $artist) {
    insertIntoFeaturedArtist($TylerURL, $artist);
  }
}

printTrackTable();
printFeaturedArtistTable();

*/

#$dom->load($html[1]);
#getMetaData($dom);



/* get all albums from Atmosphere Artist page
$dom = new simple_html_dom();
$artistStartPage = scraperwiki::scrape("http://rapgenius.com/artists/Atmosphere");
$dom->load($artistStartPage);
getAlbums($dom);
*/



/* get all songs from an album
$dom = new simple_html_dom();
$album = scraperwiki::scrape("http://rapgenius.com/albums/Atmosphere/Lucy-ford");
$dom->load($album);

getSongList($dom);
*/




/*
- Experiment - 
Start with atmosphere artist page - http://rapgenius.com/artists/Atmosphere
Use getAlbums to get a list of all albums (in the form of an array of '/albums/blahblah')
For each album, use getSongList to get a list of all songs (in the form of an array of 'Atmosphere-.....-lyrics')
for each song, use getLyrics, getMetaData, and THE NAME OF THE ALBUM to store all the information

-SAVING-
key - URL??

*/



##LOADED All of Big-L so far - /artists/Big-l 
##Atmosphere

$BASE_URL = "http://rapgenius.com";
$artistURL = "/artists/Jay-z";
$dom = getPageDom($BASE_URL . $artistURL);
$albumArray = getAlbums($dom);
$albumURLArray = $albumArray['urls'];
$albumNameArray = $albumArray['names'];
#print_r($albumArray);
foreach ($albumURLArray as $i => $albumURL) {

  $albumDom = new simple_html_dom();
 # print $album . "\n";

  
  $albumPage = scraperwiki::scrape($BASE_URL . $albumURL);
  $albumDom->load($albumPage);
  
  #print $albumDom ."\n\n";
  #$albumA = $albumDom->find('ul.album_list',0);
  print "album => " . $albumNameArray[$i] . "\n";

  $trackArray = getSongList($albumDom);
  $albumName = $albumNameArray[$i];

  #print_r($trackArray);

  foreach ($trackArray as $j => $trackURL) {
    $trackPage = scraperwiki::scrape($BASE_URL . $trackURL);
    $trackDom = new simple_html_dom();
    #print $track . "\n";
    $trackDom->load($trackPage);
    //use trackDom to get lyrics and metadata?
    $trackMeta = getTrackMetaData($trackDom);
    #print_r($trackMeta);
    $trackMeta['album'] = $albumName;
    addTrack($track, $trackMeta);
    $trackLyrics = getLyrics($trackDom);
    insertIntoLyrics($trackURL, $trackMeta['artist'], $trackLyrics);
  }
}

/*"/artists/Big-l"*/

/*
$message = scraperwiki::save_sqlite(array("URL"), array("URL"=>"blablabla-lyrics", "Album"=>"My pants", "Artist"=>"Tyler", "Track"=>"Couch",)); print_r($message); 
#scraperwiki::save_sqlite(array("a"),array("a"=>1, "bbb"=>"Hi there")); 
scraperwiki::save_sqlite(array("a"), array("a"=>1, "bbb"=>"Bye there")); 
*/

##See what's in swdata
/*
$retVal = scraperwiki::select("* from swdata");
foreach($retVal as $i => $value){
  print $i . " -> " . $value . "\n";
  print_r($value);
}  
*/

/* ONE OFF database interactions*/
#scraperwiki::sqliteexecute("delete FROM swdata");

##CREATE AND DELETE SCRIPTS

#scraperwiki::sqliteexecute("DROP TABLE if exists 'Track'");
#scraperwiki::sqliteexecute("CREATE TABLE 'Track' ('UniqURL' text, 'Album' text, 'Artist' text, 'Track' text, 'Featuring' integer)");

#scraperwiki::sqliteexecute("DROP TABLE if exists 'Lyrics'");
#scraperwiki::sqliteexecute("CREATE TABLE 'Lyrics' ('UniqURI' text, 'TrackURL' text, 'TrackSegment' integer, 'Artist' text, 'Lyrics' text)");

#scraperwiki::sqliteexecute("DROP TABLE if exists 'Featured_Artist'");
#scraperwiki::sqliteexecute("CREATE TABLE 'Featured_Artist' ('UniqURI' text, 'TrackURL' text, 'Artist' text)");




##Show all tables in the database##
# print_r(scraperwiki::show_tables());
?>


<?php
######################################
# Basic PHP scraper for RapGenius
#
# a) extract lyrics from a RapGenius URL
# a') extract metadata about the page - MINIMUM of Artist, Track
# b) save those lyrics in some structure (probably blob) by artist, track, and any other metadata available
# c) track the URL used, last time retrieved, and last time the page was updated (if that info is available)

##CRAZY - make a spider - start with an artist- go to  http://rapgenius.com/artists/Atmosphere
/*
1) Grab all a.song_name and follow links - GET META AND LYRICS - meta = artist, supporting artists
2) Get album list - ul.album_list - <li><a href=link>Album Name</a></li> - THAT"S HOW WE SAVE THE ALBUM NAME
3) Follow each album link and 
4) get song list - ul.song_list - iterate through the <a> or <li><a> list inside ul
5) follow each track link (ends in -lyrics) - GET META AND LYRICS
6) break up the lyrics by artist in [] blocks, and give each block and ID so that you can put the track back together again
7) save that data


*/
## get all the album links and get those
## 
######################################

require  'scraperwiki/simple_html_dom.php';


##CREATE AND DELETE SCRIPTS
/*
scraperwiki::sqliteexecute("DROP TABLE if exists 'Track'");
scraperwiki::sqliteexecute("CREATE TABLE 'Track' ('UniqURL' text, 'Album' text, 'Artist' text, 'Track' text, 'Featuring' integer)");

scraperwiki::sqliteexecute("DROP TABLE if exists 'Lyrics'");
scraperwiki::sqliteexecute("CREATE TABLE 'Lyrics' ('UniqURI' text, 'TrackURL' text, 'TrackSegment' integer, 'Artist' text, 'Lyrics' text)");

scraperwiki::sqliteexecute("DROP TABLE if exists 'Featured_Artist'");
scraperwiki::sqliteexecute("CREATE TABLE 'Featured_Artist' ('UniqURI' text, 'TrackURL' text, 'Artist' text)");
*/

##WEB PAGE FUNCTIONS##

function STOREArtistAlbumTracks($ArtistURL) {
  $dom = new simple_html_dom();
  $BASE_URL = "http://rapgenius.com";
  $artistStartPage = scraperwiki::scrape($BASE_URL . $ArtistURL);
  $dom->load($artistStartPage);
  $albumArray = getAlbums($dom);
  $albumURLArray = $albumArray['urls'];
  $albumNameArray = $albumArray['names'];
  #print_r($albumArray);
  foreach ($albumURLArray as $i => $album) {

    $albumDom = new simple_html_dom();
 # print $album . "\n";

 
    $albumPage = scraperwiki::scrape($BASE_URL . $album);
    $albumDom->load($albumPage);
 
  #print $albumDom ."\n\n";
  #$albumA = $albumDom->find('ul.album_list',0);
    print "album => " . $albumNameArray[$i] . "\n";

    $trackArray = getSongList($albumDom);
    $albumName = $albumNameArray[$i];

  #print_r($trackArray);

    foreach ($trackArray as $j => $track) {
      $trackPage = scraperwiki::scrape($BASE_URL . $track);
      $trackDom = new simple_html_dom();
    #print $track . "\n";
      $trackDom->load($trackPage);
      //use trackDom to get lyrics and metadata?
      $trackMeta = getTrackMetaData($trackDom);
    #print_r($trackMeta);
      $trackMeta['album'] = $albumName;
      addTrack($track, $trackMeta);
    }
  }
}

function getPageDom($URL) {
  $dom = new simple_html_dom();
  $page = scraperwiki::scrape($URL);
  $dom->load($page);
  return $dom;
}

## PRINTS the lyrics DIV from a track page in plaintext
## $dom - simplesomethingDOM
function getLyrics($dom) {
  $lyrics = "";
  foreach($dom->find('div.lyrics ') as $data){
    #print $data->plaintext;
    $lyrics = $lyrics . $data->plaintext;
  }   
  return $lyrics;
}

## Gets the Track, Artist, and <TODO> Featured Artists
## $dom - simplesomethingDOM
function getTrackMetaData($dom) {
  $output = getArtistAndTrackname($dom);
  ##TODO - need to get supporting artists (array)
  $output['featuring'] = getFeaturedArtists($dom);
  return $output;
}

## Gets the Track, Artist
## $dom - simplesomethingDOM
function getArtistAndTrackName($dom) {
  $artistTrack = $dom->find('h1.song_title',0);
  $artist = $artistTrack->find('a',0)->plaintext;
  $startBuffer = 8;
  $endBuffer = -11;
  $track = substr($artistTrack->plaintext, ($startBuffer + strlen($artist)) , $endBuffer);
  $output['track'] = $track;
  $output['artist'] = $artist;

  return $output;
}

## Gets the list of <a> featured artists 
## ASSUMING THAT ALL ARTISTS HAVE HYPERLINKS!
## returns an array of artists from the <a> hyperlinks inside the featured_artists div
function getFeaturedArtists($dom) {
  $feat = $dom->find('div.featured_artists',0);
  $artists = array();
  if ($feat != NULL && sizeof($feat) > 0) {
    foreach($feat->find('a') as $artist) {
      $artists[] = $artist->plaintext;
    }
  }
  return $artists;
}


## Expects the DOM of an artist page
## Returns an array of album URLs and album names (same keys)
function getAlbums($dom) {
  $albumURLs = array();
  $albumNames = array();
  $albums = $dom->find('ul.album_list',0);
  foreach($albums->find('li a') as $data){
    #print $data->href. "\n";
    $albumURLs[] = $data->href;
    $albumNames[] = $data->plaintext;
  }
  return array("urls"=>$albumURLs, "names"=>$albumNames);
}

## Expects the DOM of an album page
## Returns an array of track URLs
function getSongList($dom) {
  $trackURLs = array();
  $songs = $dom->find('ul.song_list  ',0);
  #print $songs; 
  #print_r($songs);
  foreach($songs->find('li a') as $track) {
    #print $track->href . "\n";
    $trackURLs[] = $track->href;
    #print $track->href. "\n";
  }
  return $trackURLs;
}

##addLyrics expects the $URL and $dom for the track

###NOTE### - UNIQ URI should be the song URL plus '#', and a unique identifier (within the table)

##DATABASE FUNCTIONS##
function insertIntoTrack($URL, $album, $artist, $track, $featuring) {
  scraperwiki::save_sqlite(array("UniqURL"), array("UniqURL"=>$URL, "Album"=>$album, "Artist"=>$artist, "Track"=>$track, "Featuring"=>$featuring), $table_name="Track");
}

##Expects Track URL, artist, and lyrics
##For now attribute all lyrics to the main artist (segment 0)
function insertIntoLyrics($URL, $artist, $lyrics) {
  $URI = $URL . "#" . str_replace(" ", "_", $artist);
  scraperwiki::save_sqlite(array("UniqURI"), array("UniqURI"=>$URI, "TrackURL"=>$URL, "TrackSegment"=>0, "Artist"=>$artist, "Lyrics"=>$lyrics), $table_name="Lyrics");
}

function insertIntoFeaturedArtist($URL, $artist) {
  $URI = $URL . "#" . str_replace(" ", "_", $artist);
  scraperwiki::save_sqlite(array("UniqURI"), array("UniqURI"=>$URI, "TrackURL"=>$URL, "Artist"=>$artist), $table_name="Featured_Artist");
}

## Expects track URL, and trackMeta (album, artist, track, and featuring count)
function addTrack($URL, $trackMeta) {
  insertIntoTrack($URL, $trackMeta['album'], $trackMeta['artist'], $trackMeta['track'], count($trackMeta['featuring']));
  if (count($trackMeta['featuring']) > 0) {
    foreach ($trackMeta['featuring'] as $i => $artist) {
      insertIntoFeaturedArtist($URL, $artist);
    }
  }
}

##DATABASE QUERIES##
function printTrackTable() {
  print "\nselect * from Track\n\n";
  $retVal = scraperwiki::select("* from Track");
  foreach($retVal as $i => $value){
    print $i . " -> " . $value . "\n";
    print_r($value);
  } 
}

function printFeaturedArtistTable() {
  print "\nselect * from Featured_Artist\n\n";
  $retVal = scraperwiki::select("* from Featured_Artist");
  foreach($retVal as $i => $value){
    print $i . " -> " . $value . "\n";
    print_r($value);
  }
}


#random URL...
#$TylerURL = "http://rapgenius.com/lyrics/Earl-sweatshirt-ft-tyler-the-creator/Couch";
##$TylerURL = "http://rapgenius.com/Jennifer-lopez-aint-it-funny-remix-lyrics";


/*
$BASE_URL = "http://rapgenius.com";
$dom = getPageDom($BASE_URL . "/Big-l-games-lyrics");

getLyrics($dom);
*/

##TESTS##
###THIS WORKS FOR RAPGENIUS but you don't get album - http://rapgenius.com/songs?page=300

## 2-song test to get lyrics and/or metadata

/*
$dom = new simple_html_dom();
$html[0] = scraperwiki::scrape($TylerURL);
$html[1] = scraperwiki::scrape("http://rapgenius.com/Ugk-one-day-lyrics");
$dom->load($html[0]);

#getLyrics($dom);

$trackMeta = getTrackMetaData($dom);
print_r($trackMeta);

insertIntoTrack($TylerURL, "AlbumName", $trackMeta['artist'], $trackMeta['track'], count($trackMeta['featuring']));
if (count($trackMeta['featuring']) > 0) {
  foreach ($trackMeta['featuring'] as $i => $artist) {
    insertIntoFeaturedArtist($TylerURL, $artist);
  }
}

printTrackTable();
printFeaturedArtistTable();

*/

#$dom->load($html[1]);
#getMetaData($dom);



/* get all albums from Atmosphere Artist page
$dom = new simple_html_dom();
$artistStartPage = scraperwiki::scrape("http://rapgenius.com/artists/Atmosphere");
$dom->load($artistStartPage);
getAlbums($dom);
*/



/* get all songs from an album
$dom = new simple_html_dom();
$album = scraperwiki::scrape("http://rapgenius.com/albums/Atmosphere/Lucy-ford");
$dom->load($album);

getSongList($dom);
*/




/*
- Experiment - 
Start with atmosphere artist page - http://rapgenius.com/artists/Atmosphere
Use getAlbums to get a list of all albums (in the form of an array of '/albums/blahblah')
For each album, use getSongList to get a list of all songs (in the form of an array of 'Atmosphere-.....-lyrics')
for each song, use getLyrics, getMetaData, and THE NAME OF THE ALBUM to store all the information

-SAVING-
key - URL??

*/



##LOADED All of Big-L so far - /artists/Big-l 
##Atmosphere

$BASE_URL = "http://rapgenius.com";
$artistURL = "/artists/Jay-z";
$dom = getPageDom($BASE_URL . $artistURL);
$albumArray = getAlbums($dom);
$albumURLArray = $albumArray['urls'];
$albumNameArray = $albumArray['names'];
#print_r($albumArray);
foreach ($albumURLArray as $i => $albumURL) {

  $albumDom = new simple_html_dom();
 # print $album . "\n";

  
  $albumPage = scraperwiki::scrape($BASE_URL . $albumURL);
  $albumDom->load($albumPage);
  
  #print $albumDom ."\n\n";
  #$albumA = $albumDom->find('ul.album_list',0);
  print "album => " . $albumNameArray[$i] . "\n";

  $trackArray = getSongList($albumDom);
  $albumName = $albumNameArray[$i];

  #print_r($trackArray);

  foreach ($trackArray as $j => $trackURL) {
    $trackPage = scraperwiki::scrape($BASE_URL . $trackURL);
    $trackDom = new simple_html_dom();
    #print $track . "\n";
    $trackDom->load($trackPage);
    //use trackDom to get lyrics and metadata?
    $trackMeta = getTrackMetaData($trackDom);
    #print_r($trackMeta);
    $trackMeta['album'] = $albumName;
    addTrack($track, $trackMeta);
    $trackLyrics = getLyrics($trackDom);
    insertIntoLyrics($trackURL, $trackMeta['artist'], $trackLyrics);
  }
}

/*"/artists/Big-l"*/

/*
$message = scraperwiki::save_sqlite(array("URL"), array("URL"=>"blablabla-lyrics", "Album"=>"My pants", "Artist"=>"Tyler", "Track"=>"Couch",)); print_r($message); 
#scraperwiki::save_sqlite(array("a"),array("a"=>1, "bbb"=>"Hi there")); 
scraperwiki::save_sqlite(array("a"), array("a"=>1, "bbb"=>"Bye there")); 
*/

##See what's in swdata
/*
$retVal = scraperwiki::select("* from swdata");
foreach($retVal as $i => $value){
  print $i . " -> " . $value . "\n";
  print_r($value);
}  
*/

/* ONE OFF database interactions*/
#scraperwiki::sqliteexecute("delete FROM swdata");

##CREATE AND DELETE SCRIPTS

#scraperwiki::sqliteexecute("DROP TABLE if exists 'Track'");
#scraperwiki::sqliteexecute("CREATE TABLE 'Track' ('UniqURL' text, 'Album' text, 'Artist' text, 'Track' text, 'Featuring' integer)");

#scraperwiki::sqliteexecute("DROP TABLE if exists 'Lyrics'");
#scraperwiki::sqliteexecute("CREATE TABLE 'Lyrics' ('UniqURI' text, 'TrackURL' text, 'TrackSegment' integer, 'Artist' text, 'Lyrics' text)");

#scraperwiki::sqliteexecute("DROP TABLE if exists 'Featured_Artist'");
#scraperwiki::sqliteexecute("CREATE TABLE 'Featured_Artist' ('UniqURI' text, 'TrackURL' text, 'Artist' text)");




##Show all tables in the database##
# print_r(scraperwiki::show_tables());
?>



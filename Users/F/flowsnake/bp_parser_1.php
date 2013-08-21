<?php
//echo date("YmdHis") ;
scraperwiki::sqliteexecute( " DROP TABLE date_20121027 " );



$table_name = "date_" . date("Ymd") ;
$page_ID = "page_ID_" . date("Ymd") ;


//////////////////////////////////////////////////////////////////////////////////////////////
//                                       create table                                       //
//////////////////////////////////////////////////////////////////////////////////////////////
if (scraperwiki::sqliteexecute( " CREATE TABLE $table_name ( pageID int, name plaintext, html blob)" ) )
{
echo "table created: " . $table_name . "\n" ;
}
else echo "failed to create table: " . $table_name . "\n" ;
//create index for the table//////////////////////////////////////////////////////////////////
if (scraperwiki::sqliteexecute( " CREATE UNIQUE INDEX $page_ID ON $table_name ( pageID ) " ) ) echo "index created\n" ;
else echo "failed to create index\n" ;
//////////////////////////////////////////////////////////////////////////////////////////////









//////////////////////////////////////////////////////////////////////////////////////////////
//                                       scrape pages                                       //
//////////////////////////////////////////////////////////////////////////////////////////////
$url_list = array
(
"http://www.beatport.com",
"http://www.beatport.com/top-100",
"http://www.beatport.com/top-100-releases",
"http://www.beatport.com/charts",
"http://www.beatport.com/genre/breaks/9",
"http://www.beatport.com/genre/chill-out/10",
"http://www.beatport.com/genre/deep-house/12",
"http://www.beatport.com/genre/dj-tools/16",
"http://www.beatport.com/genre/drum-and-bass/1",
"http://www.beatport.com/genre/dubstep/18",
"http://www.beatport.com/genre/electro-house/17",
"http://www.beatport.com/genre/electronica/3",
"http://www.beatport.com/genre/funk-r-and-b/40",
"http://www.beatport.com/genre/glitch-hop/49",
"http://www.beatport.com/genre/hard-dance/8",
"http://www.beatport.com/genre/hardcore-hard-techno/2",
"http://www.beatport.com/genre/hip-hop/38",
"http://www.beatport.com/genre/house/5",
"http://www.beatport.com/genre/indie-dance-nu-disco/37",
"http://www.beatport.com/genre/minimal/14",
"http://www.beatport.com/genre/pop-rock/39",
"http://www.beatport.com/genre/progressive-house/15",
"http://www.beatport.com/genre/psy-trance/13",
"http://www.beatport.com/genre/reggae-dub/41",
"http://www.beatport.com/genre/tech-house/11",
"http://www.beatport.com/genre/techno/6",
"http://www.beatport.com/genre/trance/7",
"http://www.beatport.com/genre/breaks/9/top-100",
"http://www.beatport.com/genre/chill-out/10/top-100",
"http://www.beatport.com/genre/deep-house/12/top-100",
"http://www.beatport.com/genre/dj-tools/16/top-100",
"http://www.beatport.com/genre/drum-and-bass/1/top-100",
"http://www.beatport.com/genre/dubstep/18/top-100",
"http://www.beatport.com/genre/electro-house/17/top-100",
"http://www.beatport.com/genre/electronica/3/top-100",
"http://www.beatport.com/genre/funk-r-and-b/40/top-100",
"http://www.beatport.com/genre/glitch-hop/49/top-100",
"http://www.beatport.com/genre/hard-dance/8/top-100",
"http://www.beatport.com/genre/hardcore-hard-techno/2/top-100",
"http://www.beatport.com/genre/hip-hop/38/top-100",
"http://www.beatport.com/genre/house/5/top-100",
"http://www.beatport.com/genre/indie-dance-nu-disco/37/top-100",
"http://www.beatport.com/genre/minimal/14/top-100",
"http://www.beatport.com/genre/pop-rock/39/top-100",
"http://www.beatport.com/genre/progressive-house/15/top-100",
"http://www.beatport.com/genre/psy-trance/13/top-100",
"http://www.beatport.com/genre/reggae-dub/41/top-100",
"http://www.beatport.com/genre/tech-house/11/top-100",
"http://www.beatport.com/genre/techno/6/top-100",
"http://www.beatport.com/genre/trance/7/top-100",
"http://www.beatport.com/genre/breaks/9/top-100-releases",
"http://www.beatport.com/genre/chill-out/10/top-100-releases",
"http://www.beatport.com/genre/deep-house/12/top-100-releases",
"http://www.beatport.com/genre/dj-tools/16/top-100-releases",
"http://www.beatport.com/genre/drum-and-bass/1/top-100-releases",
"http://www.beatport.com/genre/dubstep/18/top-100-releases",
"http://www.beatport.com/genre/electro-house/17/top-100-releases",
"http://www.beatport.com/genre/electronica/3/top-100-releases",
"http://www.beatport.com/genre/funk-r-and-b/40/top-100-releases",
"http://www.beatport.com/genre/glitch-hop/49/top-100-releases",
"http://www.beatport.com/genre/hard-dance/8/top-100-releases",
"http://www.beatport.com/genre/hardcore-hard-techno/2/top-100-releases",
"http://www.beatport.com/genre/hip-hop/38/top-100-releases",
"http://www.beatport.com/genre/house/5/top-100-releases",
"http://www.beatport.com/genre/indie-dance-nu-disco/37/top-100-releases",
"http://www.beatport.com/genre/minimal/14/top-100-releases",
"http://www.beatport.com/genre/pop-rock/39/top-100-releases",
"http://www.beatport.com/genre/progressive-house/15/top-100-releases",
"http://www.beatport.com/genre/psy-trance/13/top-100-releases",
"http://www.beatport.com/genre/reggae-dub/41/top-100-releases",
"http://www.beatport.com/genre/tech-house/11/top-100-releases",
"http://www.beatport.com/genre/techno/6/top-100-releases",
"http://www.beatport.com/genre/trance/7/top-100-release"
) ;
////////////////////////
$i = 0;
foreach ($url_list as $URL)
  {
        $i++ ;
        $name = preg_replace('#(http://|www\.|\.|\/)#','-',$URL); 
        $name = trim($name,"-") ;
        echo $name . "\n" ;
        $html = scraperWiki::scrape($URL);
//  save data into table
$message = scraperwiki::save_sqlite(array($page_ID), array($page_ID=>$i, "name"=>$name, "html"=>$html),$table_name);           
print_r($message); 
        //if (scraperwiki::sqliteexecute( " INSERT INTO $table_name VALUES ( $i, $name, ' $html ' ) " ) ) echo "Saved name and html successfully: [" . $index . "] " . $name . "\n" ;
        //else echo "Save name and html failed: [" . $index . "] " . $name . "\n" ;
   }
//////////////////////////////////////////////////////////////////////////////////////////////




?>
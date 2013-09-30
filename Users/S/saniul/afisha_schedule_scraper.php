<?php
require 'scraperwiki/simple_html_dom.php';           
error_reporting(E_ALL);

function createMovieFromDiv($div){
        $a = $div->find("h3 a",0);
        $p = $div->find("p",0);
        $title = $a->plaintext;
        $url = $a->href;
        $components = explode("/",$url);
        $afisha_id = $components[sizeof($components)-2];
        $description = $p->plaintext;

        $movie = array(
            'afisha_id'=>$afisha_id,
            'title'=>$title,
            'description'=>$description
        );
        return $movie;
}

function createCinemaFromTd($td){
            $a = $td->children(0);
            if(empty($a)){
                $a=$td->parent()->prev_sibling()->children(0)->children(0);
            }
            $name = $a->plaintext;
            $url = $a->href;
            $components = explode("/",$url);
            $afisha_id = $components[sizeof($components)-2];
        
          $cinema = array(
            'afisha_id'=>$afisha_id,
            'name'=>$name
          );
            return $cinema;
}
/*
$date = "29-12-2011";

$html = scraperWiki::scrape("http://www.afisha.ru/msk/schedule_cinema/$date/");           
$dom = new simple_html_dom();
$dom->load($html);

$foundMovies = array();
$foundCinemas = array();
$foundShowtimes = array();

foreach($dom->find("div.m-disp-table") as $data){
        $movie = createMovieFromDiv($data);
        //$foundMovies[]=$movie;
        scraperwiki::save_sqlite(array('afisha_id'), $movie, 'movies', 2); 
        print_r("Start:".$movie['title']."\n");

        $scheduleTable = $data->next_sibling();
        $showtimes=array();
        foreach($scheduleTable->children(0)->children() as $tr){
            $cinemaTd = $tr->children(0);
            $cinema = createCinemaFromTd($cinemaTd);
            $foundCinemas[$cinema['afisha_id']]=$cinema;
            //print_r($cinema['name']."\n");

            foreach($tr->children(1)->children(0)->children() as $span){
                $time = $span->plaintext;
                $datetime = strtotime($date."T".$time);
                $afisha_id = $span->id;

                $showtime['afisha_id'] = $afisha_id;
                $showtime['movie'] = $movie['afisha_id'];
                $showtime['cinema'] = $cinema['afisha_id'];
                $showtime['datetime'] = $datetime;
                //TODO:!!! If earlier than 03:00 - add 1 day
                $showtimes[]=$showtime;
            }
        }
        scraperwiki::save_sqlite(array('afisha_id'), $showtimes, 'showtimes', 0);
        //$foundShowtimes[]=$showtimes;
        print_r("Done:".$movie['title']."\n");
}
$dom->clear();
unset($dom);
*/
$foundCinemas=array(
    "2836"=>array(
        "afisha_id"=>2836,
        "name"=>"Пионер"
    )
);
print_r("START PROCESSING CINEMAS");
$cinemas=array();
foreach($foundCinemas as $afisha_id=>$cinema)
{
    $html = scraperWiki::scrape("http://www.afisha.ru/msk/cinema/$afisha_id/");           
    $dom = new simple_html_dom();
    $dom->load($html);
    $lat=$dom->find("meta[property=og:latitude]",0)->content;
    $long=$dom->find("meta[property=og:longitude]",0)->content;
    $address=$dom->find("meta[property=og:street-address]",0)->content;
    $rating=doubleval(str_replace(',','.',$dom->find("div.rating",0)->children(0)->children(0)->plaintext));
    $cinema['lat']=$lat;
    $cinema['long']=$long;
    $cinema['address']=$address;
    $cinema['rating']=$rating;
    $cinemas[]=$cinema;
}
scraperwiki::save_sqlite(array("afisha_id"), $cinemas, "cinemas", 2);
print_r("DONE PROCESSING CINEMAS");
?>
<?php
require 'scraperwiki/simple_html_dom.php';           
error_reporting(E_ALL);

function createMovieFromDiv($div){
        $a = $div->find("h3 a",0);
        $p = $div->find("p",0);
        $title = $a->plaintext;
        $url = $a->href;
        $components = explode("/",$url);
        $afisha_id = $components[sizeof($components)-2];
        $description = $p->plaintext;

        $movie = array(
            'afisha_id'=>$afisha_id,
            'title'=>$title,
            'description'=>$description
        );
        return $movie;
}

function createCinemaFromTd($td){
            $a = $td->children(0);
            if(empty($a)){
                $a=$td->parent()->prev_sibling()->children(0)->children(0);
            }
            $name = $a->plaintext;
            $url = $a->href;
            $components = explode("/",$url);
            $afisha_id = $components[sizeof($components)-2];
        
          $cinema = array(
            'afisha_id'=>$afisha_id,
            'name'=>$name
          );
            return $cinema;
}
/*
$date = "29-12-2011";

$html = scraperWiki::scrape("http://www.afisha.ru/msk/schedule_cinema/$date/");           
$dom = new simple_html_dom();
$dom->load($html);

$foundMovies = array();
$foundCinemas = array();
$foundShowtimes = array();

foreach($dom->find("div.m-disp-table") as $data){
        $movie = createMovieFromDiv($data);
        //$foundMovies[]=$movie;
        scraperwiki::save_sqlite(array('afisha_id'), $movie, 'movies', 2); 
        print_r("Start:".$movie['title']."\n");

        $scheduleTable = $data->next_sibling();
        $showtimes=array();
        foreach($scheduleTable->children(0)->children() as $tr){
            $cinemaTd = $tr->children(0);
            $cinema = createCinemaFromTd($cinemaTd);
            $foundCinemas[$cinema['afisha_id']]=$cinema;
            //print_r($cinema['name']."\n");

            foreach($tr->children(1)->children(0)->children() as $span){
                $time = $span->plaintext;
                $datetime = strtotime($date."T".$time);
                $afisha_id = $span->id;

                $showtime['afisha_id'] = $afisha_id;
                $showtime['movie'] = $movie['afisha_id'];
                $showtime['cinema'] = $cinema['afisha_id'];
                $showtime['datetime'] = $datetime;
                //TODO:!!! If earlier than 03:00 - add 1 day
                $showtimes[]=$showtime;
            }
        }
        scraperwiki::save_sqlite(array('afisha_id'), $showtimes, 'showtimes', 0);
        //$foundShowtimes[]=$showtimes;
        print_r("Done:".$movie['title']."\n");
}
$dom->clear();
unset($dom);
*/
$foundCinemas=array(
    "2836"=>array(
        "afisha_id"=>2836,
        "name"=>"Пионер"
    )
);
print_r("START PROCESSING CINEMAS");
$cinemas=array();
foreach($foundCinemas as $afisha_id=>$cinema)
{
    $html = scraperWiki::scrape("http://www.afisha.ru/msk/cinema/$afisha_id/");           
    $dom = new simple_html_dom();
    $dom->load($html);
    $lat=$dom->find("meta[property=og:latitude]",0)->content;
    $long=$dom->find("meta[property=og:longitude]",0)->content;
    $address=$dom->find("meta[property=og:street-address]",0)->content;
    $rating=doubleval(str_replace(',','.',$dom->find("div.rating",0)->children(0)->children(0)->plaintext));
    $cinema['lat']=$lat;
    $cinema['long']=$long;
    $cinema['address']=$address;
    $cinema['rating']=$rating;
    $cinemas[]=$cinema;
}
scraperwiki::save_sqlite(array("afisha_id"), $cinemas, "cinemas", 2);
print_r("DONE PROCESSING CINEMAS");
?>

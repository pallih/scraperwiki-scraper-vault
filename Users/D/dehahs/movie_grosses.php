<?php

//Year to get data
$currentyear = date("Y");
$year = $currentyear-1;  //2012

$numyears = 11;
$url = "http://www.boxofficemojo.com";
require 'scraperwiki/simple_html_dom.php';

for($j=$year; $j>($year-$numyears); $j--){ 
    $html = scraperWiki::scrape($url."/yearly/chart/?view=releasedate&view2=domestic&yr=".$j."&sort=gross&order=DESC&p=.htm");
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $movielinks=array();
    $genres=array();
    $ratings=array();
    $budgets=array();
    $i=0;
    
    foreach($dom->find("tr") as $data){
            $tds = $data->find("td");
            if(count($tds)==9){
                //Get links for each movie (to get the genre)
                foreach ($data->find("td a") as $el) {
                    
                    /*Check 3D in title and increase offset if 3D
                    $check3D = $tds[1]->plaintext;
                    $d="3D";
                    $pos3D = strpos($check3D, $d);
                    if($pos3D !== false){ 
                        $offset=5;                
                    }else{
                        $offset=4;
                    }*/
        
                    $link = $el->getAttribute('href');
                    $movieurl = "/movies";            
                    $pos = strpos($link, $movieurl);  //Only get links that go to the movie details page
                    if($pos !== false){  //Get Genres
                        $genrelink = $url.$link;
                        $genrehtml = scraperWiki::scrape($genrelink);
                        $gendom = new simple_html_dom();
                        $gendom->load($genrehtml);
                        
                        $offset=0;
                        //Increment offset by 1 if there is a 'Domestic Lifetime Gross' data
                        foreach($gendom->find("td[@align='center'] a" ) as $gendata){
                            $lgrosstag = $gendata->find("b");
                            if(count($lgrosstag)>0){
                                $lgross = $lgrosstag[0]->plaintext;
                                if(count($lgross)>0){
                                    $offset=1;
                                    break;
                                }
                            }
                        }
                        foreach($gendom->find("td[@valign='top']" ) as $gendata){
                            $btag = $gendata->find("b");
                            $genre = $btag[4+$offset]->plaintext;
                            $rating = $btag[6+$offset]->plaintext;
                            $budget = $btag[7+$offset]->plaintext;
                            array_push($genres, $genre);
                            array_push($ratings, $rating);
                            array_push($budgets, $budget);
                            if(count($genre)>0){
                                break;
                            }
                        }
                        //array_push($movielinks, $link);
                       
                    }        
                }
        
                $record = array(
                    'movie' => $tds[1]->plaintext,
                    'studio' => $tds[2]->plaintext,
                    'total_gross' => $tds[3]->plaintext,
                    'total_theaters' => $tds[4]->plaintext,
                    'genre' => $genres[$i],
                    'rating' => $ratings[$i],
                    'budget' => $budgets[$i],
                    'year' => $j
                );
                scraperwiki::save(array('movie'), $record);
        
                $i++;    
            }
       }
}
?>
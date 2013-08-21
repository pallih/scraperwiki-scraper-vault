<?php
/* This Scrapper will extract data about shows from IMDB. I use this in conjunction with awk to rename digital recordings of some series I watch and to provide additional data */
/* A fair warning: my regexps are a lot more specific than I'd like. Small changes to the IMDB site will result in badass failure of everything. I mean it: the universe will fold, time will stop, milk will turn sour, coke will turn into pepsi. You get the idea */
/* For a Bash Skript doing exactly the same thing better, check out the end of this page. */


/* Add new shows here */
$series_string["BBT"]    = "tt0898266"; //Big Bang Theory
$series_string["Cali"]   = "tt0904208"; //Californication
$series_string["30R"]    = "tt0496424"; //30 Rock
$series_string["HIMYM"]  = "tt0460649"; //How I Met Your Mother
$series_string["Scrubs"] = "tt0285403"; //Scrubs
$series_string["Fringe"] = "tt1119644"; //Fringe  
$series_string["Lost"]   = "tt0411008"; //Lost
//$series_string[""] = ""; // Dummy

/* Specify a show to process. If none is specified, will process all shows. */
//$show = "Cali";


/* actual code begins here */
if (isset($show)){
        $scrape_url = "http://www.imdb.com/title/".$series_string[$show]."/episodes";
        processShow($scrape_url);
}
else{
    foreach ($series_string as $show => $temp){
    
        $scrape_url = "http://www.imdb.com/title/".$series_string[$show]."/episodes";
        processShow($scrape_url);
    
    }
}
$keys = array('series_title', 'nr', 'season', 'episode', 'airdate', 'link', 'airdate', 'episode_title', 'description');
scraperwiki::save_metadata('data_columns',$keys);



/* function declarations */

    /* this function will do all of the scrapping, string-matching and saving */
    function processShow($url){
         
        $html = scraperwiki::scrape($url);
        
        $regexp_show = '|<h1><small>Episode list for<br></small><a [^>]*>&#x22;([^&]*)&#x22;</a>|';
        
        preg_match($regexp_show,$html,$arr);
        $series_title = $arr[1];
        
        $regexp = "|<div class=\"filter-all filter-year-([0-9]{4,4})\"><hr /><table cellspacing=\"0\" cellpadding=\"0\"><tr> <td valign=\"top\"><div class=\"episode_slate_container\"><div class=[^>]*></div></div></td> <td valign=\"top\"><h3>Season ([[:digit:]]*), Episode ([[:digit:]]*): <a href=\"(/title/[[:alnum:]]*/)\">([^<]*)</a></h3><span class=\"less-emphasis\">Original Air Date&mdash;<strong>([^<]*)</strong></span><br>([^<]*)[^\n]*</td></tr></table></div>|";
        
        preg_match_all($regexp,$html,$arr, PREG_SET_ORDER);
        
        
        $keys = array('series_title', 'nr', 'season', 'episode', 'airdate', 'link', 'airdate', 'episode_title', 'description');
        $i=0;
        foreach ($arr as $val) {
            $i++;
            $data = array('series_title' => clean($series_title),
                                'nr' => $i,
                                'season' => clean($val[2]),
                                'episode' => clean($val[3]),
                                'airdate' => clean(date('d.m.Y',strtotime($val[6]))),
                                'link' => clean('http://www.imdb.com'.$val[4]),
                                'episode_title' => clean($val[5]),
                                'description' => clean($val[7]));
            
            scraperwiki::save($keys, $data);
                
        }
    }   
        
    /* I took this one from the IMDB-top-250 scrapper, does some string cleaning I guess. Will check this later. */
    function clean($val) {
        $val = str_replace('&nbsp;',' ',$val);
        $val = str_replace('&amp;','&',$val);
        $val = html_entity_decode($val);
        $val = strip_tags($val);
        $val = trim($val);
        $val = utf8_decode($val);
        return($val);
    }

    
/* Here's the Bash Script. */

#!/bin/bash

#url='http://www.imdb.com/title/tt0904208/episodes'
#pattern='<div class="filter-all filter-year-([0-9]{4,4})"><hr /><table cellspacing="0" cellpadding="0"><tr> <td valign="top"><div class="episode_slate_container"><div class=[^>]*></div></div></td> <td valign="top"><h3>Season ([[:digit:]]*), Episode ([[:digit:]]*): <a href="(/title/[[:alnum:]]*/)">([^<]*)</a></h3><span class="less-emphasis">Original Air Date&mdash;<strong>([^<]*)</strong></span><br>#([^<]*)[^\n]*'
#
#curl -s $url | 
#    grep -E '<div class="filter-all filter-year-([0-9]{4,4})"><hr /><table cellspacing="0" cellpadding="0">' | 
#    sed -r -e 's|'"$pattern"'|\2\t\3\t\6\t\4\t\5\t\7|g' -e 's/&#x[[:digit:]]*;//g' | 
#    awk -F'\t' '{printf("Californication S%2dE%2s - %s\n",$1,$2,$5)}' | 
#    sed -r -e 's/S ([0-9])/S0\1/g' -e 's/E ([0-9])/E0\1/g' | 
#    less

/* end of Bash script. Just remove comment symbols and run it in your bash (or whatever commandline you have at your disposal) */
?>
<?php
//year can start at 1997
require 'scraperwiki/simple_html_dom.php';
/*
for($year = 2012; $year <= 2012; $year++)
{
    for($month = 11; $month <= 12; $month++)
    {
        for($day = 1; $day <= 31; $day++)
        {
            $html = scraperWiki::scrape("http://api.wunderground.com/api/16000cc04ab1fb20/history_".$year.$month.$day."/q/PH/Manila.json");
            print $html . "\n";

            // load html into dom
            $dom = new simple_html_dom();
            $dom->load($html);
        
            //turn dom into a string
            $json = $dom;    

            //make the json string an array which i confusingly call an object
            $obj = json_decode($json);

            //Test:
            //print_r($obj);

            $rows = '';

            //create results table
            $results = array(
                'index' => strval($obj->history->pretty)
                'first_name' => strval($obj->first_name),
                'last_name' => strval($obj->web_name),
                'position' => strval($obj->type_name),
                'team_name' => strval($obj->team_name), 
                'total_points' => strval($obj->total_points),     
                'now_cost' => strval($obj->now_cost)
            );

            //check results
            print_r($results);
            
            //save
            scraperwiki::save(array('index'),$results);
        }
    }
}
*/

$html = scraperWiki::scrape("http://api.wunderground.com/api/16000cc04ab1fb20/history_20121118/q/PH/Manila.json");
            print $html . "\n";

            // load html into dom
            $dom = new simple_html_dom();
            $dom->load($html);
        
            //turn dom into a string
            $json = $dom;    

            //make the json string an array which i confusingly call an object
            $obj = json_decode($json);

            //Test:
            print_r($obj);

            $rows = '';

            //create results table
            $results = array(
                'index' => strval("1"));

            //check results
            print_r($results);
            
            //save
            scraperwiki::save(array('index'),$results);

?><?php
//year can start at 1997
require 'scraperwiki/simple_html_dom.php';
/*
for($year = 2012; $year <= 2012; $year++)
{
    for($month = 11; $month <= 12; $month++)
    {
        for($day = 1; $day <= 31; $day++)
        {
            $html = scraperWiki::scrape("http://api.wunderground.com/api/16000cc04ab1fb20/history_".$year.$month.$day."/q/PH/Manila.json");
            print $html . "\n";

            // load html into dom
            $dom = new simple_html_dom();
            $dom->load($html);
        
            //turn dom into a string
            $json = $dom;    

            //make the json string an array which i confusingly call an object
            $obj = json_decode($json);

            //Test:
            //print_r($obj);

            $rows = '';

            //create results table
            $results = array(
                'index' => strval($obj->history->pretty)
                'first_name' => strval($obj->first_name),
                'last_name' => strval($obj->web_name),
                'position' => strval($obj->type_name),
                'team_name' => strval($obj->team_name), 
                'total_points' => strval($obj->total_points),     
                'now_cost' => strval($obj->now_cost)
            );

            //check results
            print_r($results);
            
            //save
            scraperwiki::save(array('index'),$results);
        }
    }
}
*/

$html = scraperWiki::scrape("http://api.wunderground.com/api/16000cc04ab1fb20/history_20121118/q/PH/Manila.json");
            print $html . "\n";

            // load html into dom
            $dom = new simple_html_dom();
            $dom->load($html);
        
            //turn dom into a string
            $json = $dom;    

            //make the json string an array which i confusingly call an object
            $obj = json_decode($json);

            //Test:
            print_r($obj);

            $rows = '';

            //create results table
            $results = array(
                'index' => strval("1"));

            //check results
            print_r($results);
            
            //save
            scraperwiki::save(array('index'),$results);

?>
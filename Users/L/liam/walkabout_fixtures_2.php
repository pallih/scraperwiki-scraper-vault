<?php
   ob_start();
$html = scraperWiki::scrape("http://walkabout.eu.com/sport/");  
require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("div[class=sportsrow]") as $data){
    $team1 = $data->find("div[class=sport_teams] strong");
    $team2 = $data->find("div[class=sport_teams] strong", 1);
    $comp = $data->find("div[class=competition_name] strong");
    $date = $data->find("div[class=start_time]");
    $time = $data->find("div[class=start_time] strong");
    $chan = $data->find("div[class=channel_name]");
    $sport = $data;   
       echo $team1[0]->innertext . ' vs ' . $team2->innertext.PHP_EOL;
       // competition
       echo $comp[0]->innertext.PHP_EOL; 
       // time
       echo $time[0]->innertext.PHP_EOL;
       // date
       echo substr($date[0]->innertext, -37, 10).PHP_EOL; 

       // channel - need to convert numbers to channels. 62=sky, 52=bbc, 
       $chan1 = $chan[0];
       preg_match_all('!\d+!', $chan1, $matches);
           // convert to channel from no
           if (($matches[0][0]) == '52')  echo 'BBC'.PHP_EOL;
           if (($matches[0][0]) == '62')  echo 'Sky'.PHP_EOL;

       $sportfilt = substr($sport, 30, 5); // $chan[0]->innertext; 
           if ($sportfilt == 'Crick')  echo 'Cricket'.PHP_EOL;
           if ($sportfilt == 'Rugby')  echo 'Rugby' .PHP_EOL;
           if ($sportfilt == 'Footb')  echo 'Football'.PHP_EOL;  
}
       // teams
       echo $team1[0]->innertext . ' vs ' . $team2->innertext.PHP_EOL;
       // competition
       echo $comp[0]->innertext.PHP_EOL; 
       // time
       echo $time[0]->innertext.PHP_EOL;
       // date
       echo substr($date[0]->innertext, -37, 10).PHP_EOL; 

       // channel - need to convert numbers to channels. 62=sky, 52=bbc, 
       $chan1 = $chan[0];
       preg_match_all('!\d+!', $chan1, $matches);
           // convert to channel from no
           if ($matches[0][0] == '52')  echo 'BBC'.PHP_EOL;
           if ($matches[0][0] == '62')  echo 'Sky'.PHP_EOL;

       $sportfilt = substr($sport, 30, 5); // $chan[0]->innertext; 
           if ($sportfilt == 'Crick')  echo 'Cricket'.PHP_EOL;
           if ($sportfilt == 'Rugby')  echo 'Rugby' .PHP_EOL;
           if ($sportfilt == 'Footb')  echo 'Football'.PHP_EOL;

       //echo $chan[0]->innertext; 
       //echo $sport;
       //echo substr($sport->innertext, 30, 45); 



$content = ob_get_contents();

echo $content;

?>
<?php
   ob_start();
$html = scraperWiki::scrape("http://walkabout.eu.com/sport/");  
require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("div[class=sportsrow]") as $data){
    $team1 = $data->find("div[class=sport_teams] strong");
    $team2 = $data->find("div[class=sport_teams] strong", 1);
    $comp = $data->find("div[class=competition_name] strong");
    $date = $data->find("div[class=start_time]");
    $time = $data->find("div[class=start_time] strong");
    $chan = $data->find("div[class=channel_name]");
    $sport = $data;   
       echo $team1[0]->innertext . ' vs ' . $team2->innertext.PHP_EOL;
       // competition
       echo $comp[0]->innertext.PHP_EOL; 
       // time
       echo $time[0]->innertext.PHP_EOL;
       // date
       echo substr($date[0]->innertext, -37, 10).PHP_EOL; 

       // channel - need to convert numbers to channels. 62=sky, 52=bbc, 
       $chan1 = $chan[0];
       preg_match_all('!\d+!', $chan1, $matches);
           // convert to channel from no
           if (($matches[0][0]) == '52')  echo 'BBC'.PHP_EOL;
           if (($matches[0][0]) == '62')  echo 'Sky'.PHP_EOL;

       $sportfilt = substr($sport, 30, 5); // $chan[0]->innertext; 
           if ($sportfilt == 'Crick')  echo 'Cricket'.PHP_EOL;
           if ($sportfilt == 'Rugby')  echo 'Rugby' .PHP_EOL;
           if ($sportfilt == 'Footb')  echo 'Football'.PHP_EOL;  
}
       // teams
       echo $team1[0]->innertext . ' vs ' . $team2->innertext.PHP_EOL;
       // competition
       echo $comp[0]->innertext.PHP_EOL; 
       // time
       echo $time[0]->innertext.PHP_EOL;
       // date
       echo substr($date[0]->innertext, -37, 10).PHP_EOL; 

       // channel - need to convert numbers to channels. 62=sky, 52=bbc, 
       $chan1 = $chan[0];
       preg_match_all('!\d+!', $chan1, $matches);
           // convert to channel from no
           if ($matches[0][0] == '52')  echo 'BBC'.PHP_EOL;
           if ($matches[0][0] == '62')  echo 'Sky'.PHP_EOL;

       $sportfilt = substr($sport, 30, 5); // $chan[0]->innertext; 
           if ($sportfilt == 'Crick')  echo 'Cricket'.PHP_EOL;
           if ($sportfilt == 'Rugby')  echo 'Rugby' .PHP_EOL;
           if ($sportfilt == 'Footb')  echo 'Football'.PHP_EOL;

       //echo $chan[0]->innertext; 
       //echo $sport;
       //echo substr($sport->innertext, 30, 45); 



$content = ob_get_contents();

echo $content;

?>
<?php
   ob_start();
$html = scraperWiki::scrape("http://walkabout.eu.com/sport/");  
require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("div[class=sportsrow]") as $data){
    $team1 = $data->find("div[class=sport_teams] strong");
    $team2 = $data->find("div[class=sport_teams] strong", 1);
    $comp = $data->find("div[class=competition_name] strong");
    $date = $data->find("div[class=start_time]");
    $time = $data->find("div[class=start_time] strong");
    $chan = $data->find("div[class=channel_name]");
    $sport = $data;   
       echo $team1[0]->innertext . ' vs ' . $team2->innertext.PHP_EOL;
       // competition
       echo $comp[0]->innertext.PHP_EOL; 
       // time
       echo $time[0]->innertext.PHP_EOL;
       // date
       echo substr($date[0]->innertext, -37, 10).PHP_EOL; 

       // channel - need to convert numbers to channels. 62=sky, 52=bbc, 
       $chan1 = $chan[0];
       preg_match_all('!\d+!', $chan1, $matches);
           // convert to channel from no
           if (($matches[0][0]) == '52')  echo 'BBC'.PHP_EOL;
           if (($matches[0][0]) == '62')  echo 'Sky'.PHP_EOL;

       $sportfilt = substr($sport, 30, 5); // $chan[0]->innertext; 
           if ($sportfilt == 'Crick')  echo 'Cricket'.PHP_EOL;
           if ($sportfilt == 'Rugby')  echo 'Rugby' .PHP_EOL;
           if ($sportfilt == 'Footb')  echo 'Football'.PHP_EOL;  
}
       // teams
       echo $team1[0]->innertext . ' vs ' . $team2->innertext.PHP_EOL;
       // competition
       echo $comp[0]->innertext.PHP_EOL; 
       // time
       echo $time[0]->innertext.PHP_EOL;
       // date
       echo substr($date[0]->innertext, -37, 10).PHP_EOL; 

       // channel - need to convert numbers to channels. 62=sky, 52=bbc, 
       $chan1 = $chan[0];
       preg_match_all('!\d+!', $chan1, $matches);
           // convert to channel from no
           if ($matches[0][0] == '52')  echo 'BBC'.PHP_EOL;
           if ($matches[0][0] == '62')  echo 'Sky'.PHP_EOL;

       $sportfilt = substr($sport, 30, 5); // $chan[0]->innertext; 
           if ($sportfilt == 'Crick')  echo 'Cricket'.PHP_EOL;
           if ($sportfilt == 'Rugby')  echo 'Rugby' .PHP_EOL;
           if ($sportfilt == 'Footb')  echo 'Football'.PHP_EOL;

       //echo $chan[0]->innertext; 
       //echo $sport;
       //echo substr($sport->innertext, 30, 45); 



$content = ob_get_contents();

echo $content;

?>
<?php
   ob_start();
$html = scraperWiki::scrape("http://walkabout.eu.com/sport/");  
require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("div[class=sportsrow]") as $data){
    $team1 = $data->find("div[class=sport_teams] strong");
    $team2 = $data->find("div[class=sport_teams] strong", 1);
    $comp = $data->find("div[class=competition_name] strong");
    $date = $data->find("div[class=start_time]");
    $time = $data->find("div[class=start_time] strong");
    $chan = $data->find("div[class=channel_name]");
    $sport = $data;   
       echo $team1[0]->innertext . ' vs ' . $team2->innertext.PHP_EOL;
       // competition
       echo $comp[0]->innertext.PHP_EOL; 
       // time
       echo $time[0]->innertext.PHP_EOL;
       // date
       echo substr($date[0]->innertext, -37, 10).PHP_EOL; 

       // channel - need to convert numbers to channels. 62=sky, 52=bbc, 
       $chan1 = $chan[0];
       preg_match_all('!\d+!', $chan1, $matches);
           // convert to channel from no
           if (($matches[0][0]) == '52')  echo 'BBC'.PHP_EOL;
           if (($matches[0][0]) == '62')  echo 'Sky'.PHP_EOL;

       $sportfilt = substr($sport, 30, 5); // $chan[0]->innertext; 
           if ($sportfilt == 'Crick')  echo 'Cricket'.PHP_EOL;
           if ($sportfilt == 'Rugby')  echo 'Rugby' .PHP_EOL;
           if ($sportfilt == 'Footb')  echo 'Football'.PHP_EOL;  
}
       // teams
       echo $team1[0]->innertext . ' vs ' . $team2->innertext.PHP_EOL;
       // competition
       echo $comp[0]->innertext.PHP_EOL; 
       // time
       echo $time[0]->innertext.PHP_EOL;
       // date
       echo substr($date[0]->innertext, -37, 10).PHP_EOL; 

       // channel - need to convert numbers to channels. 62=sky, 52=bbc, 
       $chan1 = $chan[0];
       preg_match_all('!\d+!', $chan1, $matches);
           // convert to channel from no
           if ($matches[0][0] == '52')  echo 'BBC'.PHP_EOL;
           if ($matches[0][0] == '62')  echo 'Sky'.PHP_EOL;

       $sportfilt = substr($sport, 30, 5); // $chan[0]->innertext; 
           if ($sportfilt == 'Crick')  echo 'Cricket'.PHP_EOL;
           if ($sportfilt == 'Rugby')  echo 'Rugby' .PHP_EOL;
           if ($sportfilt == 'Footb')  echo 'Football'.PHP_EOL;

       //echo $chan[0]->innertext; 
       //echo $sport;
       //echo substr($sport->innertext, 30, 45); 



$content = ob_get_contents();

echo $content;

?>

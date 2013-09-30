<?php

$sourceurl="http://vhre.ru/agentstva-spb.shtml"; //page url containing links
$linkscontainer="div[id='table'] "; //links container

require 'scraperwiki/simple_html_dom.php'; 
$dom = new simple_html_dom();

//Getting all links in container $linkscontainer
$html = scraperWiki::scrape($sourceurl);
$dom->load($html);
foreach($dom->find($linkscontainer."a") as $url){
    
    $link = $url->href;    
    $title = $url->innertext;

    //run thruogh all links
        $response_html  = scraperWiki::scrape("http://vhre.ru/".$link);                
        $response = str_get_html($response_html);

        foreach($response->find("div[id='p_info'] table") as $pagedata){
              
           $record = array(
                'title' => $title, 
                'city' => $pagedata->find('tr',4)->find('td',1)->plaintext,
                'services' => "",
                'phone' => $pagedata->find('tr',0)->find('td',1)->plaintext,
                'site' => $pagedata->find('tr',3)->find('td',1)->plaintext
            );
            

            //print_r($city);
        
            //print_r($record);
            scraperwiki::save(array('title'), $record);
        
        }

}


?>
<?php

$sourceurl="http://vhre.ru/agentstva-spb.shtml"; //page url containing links
$linkscontainer="div[id='table'] "; //links container

require 'scraperwiki/simple_html_dom.php'; 
$dom = new simple_html_dom();

//Getting all links in container $linkscontainer
$html = scraperWiki::scrape($sourceurl);
$dom->load($html);
foreach($dom->find($linkscontainer."a") as $url){
    
    $link = $url->href;    
    $title = $url->innertext;

    //run thruogh all links
        $response_html  = scraperWiki::scrape("http://vhre.ru/".$link);                
        $response = str_get_html($response_html);

        foreach($response->find("div[id='p_info'] table") as $pagedata){
              
           $record = array(
                'title' => $title, 
                'city' => $pagedata->find('tr',4)->find('td',1)->plaintext,
                'services' => "",
                'phone' => $pagedata->find('tr',0)->find('td',1)->plaintext,
                'site' => $pagedata->find('tr',3)->find('td',1)->plaintext
            );
            

            //print_r($city);
        
            //print_r($record);
            scraperwiki::save(array('title'), $record);
        
        }

}


?>

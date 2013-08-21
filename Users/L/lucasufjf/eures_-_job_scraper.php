<?php
######################################
# PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$page = array("/ShowJvServlet?lg=EN&serviceUri=http://ec.europa.eu/eures/eures-localpes/services/ServiceProvider&uniqueJvId=4828871");

for ($i=0; $i < sizeof($page); $i++){
    $url = "http://ec.europa.eu/eures/eures-searchengine/servlet".$page[$i];
    
    $html = scraperwiki::scrape($url);
    print $html;
    
    $dom = new simple_html_dom();
    $dom->load($html);
    
      foreach($dom->find('th') as $data)
         {  
                $text = trim($data->plaintext);
                
                $value = trim($data->next_sibling()->plaintext);
    
                echo $text.$value."\n";    

                scraperwiki::save(array('text'), array($text => $value));   
        }
}
?>
<?php

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://www.herold.at/telefonbuch/%C3%A4rzte/");
$html = str_get_html($html_content);
foreach ($html->find("div.result-wrap h2 a") as $el) { 
      $record = array(
            'name' => "Doctor:".$el->innertext , 
            'link' => "Link:".$el->href );
                
    print $el->innertext." ";
    print $el->href."\n";
    scraperwiki::save(array('link'), $record); 
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://www.herold.at/telefonbuch/%C3%A4rzte/");
$html = str_get_html($html_content);
foreach ($html->find("div.result-wrap h2 a") as $el) { 
      $record = array(
            'name' => "Doctor:".$el->innertext , 
            'link' => "Link:".$el->href );
                
    print $el->innertext." ";
    print $el->href."\n";
    scraperwiki::save(array('link'), $record); 
}

?>

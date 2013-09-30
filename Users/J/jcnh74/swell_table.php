<?php


$html = scraperWiki::scrape("http://www.surfline.com/surfdata/forecast_buoy_summary.cfm?id=2957");           

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[id='forecastDiv'] tr") as $data){
    $tds = $data->find("td");
        $record = array(
            'bouy name' => $tds[0]->plaintext, 
            'station id' => $tds[1]->plaintext, 
            'swells' => $tds[2]->plaintext,
        );
        scraperwiki::save(array('swells'), $record);  
}

?>
<?php


$html = scraperWiki::scrape("http://www.surfline.com/surfdata/forecast_buoy_summary.cfm?id=2957");           

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[id='forecastDiv'] tr") as $data){
    $tds = $data->find("td");
        $record = array(
            'bouy name' => $tds[0]->plaintext, 
            'station id' => $tds[1]->plaintext, 
            'swells' => $tds[2]->plaintext,
        );
        scraperwiki::save(array('swells'), $record);  
}

?>

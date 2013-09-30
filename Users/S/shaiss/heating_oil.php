<?php

$oilSuppliers = array(
    'AmericanFulesPA' => "http://www.americanfuelspa.com/", 
    'PlottsOil' => "http://www.plottsenergy.com/"
);

$html = scraperWiki::scrape("http://www.americanfuelspa.com/");           
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("span[@id='ctl00_lblPrice']") as $data){
    $record = array(
        '_dbkey' => mktime(),
        'price' => $data->plaintext, 
        'date' => date('m.d.y'),
        'time' => date("H:i:s"),
        'company' => "AmericanFuels"
    );
    $message = scraperwiki::save(array('_dbkey'),$record);
    print_r($message);
    //print_r($record);
}
/* Commented out as this needs more work
//parse plotts oil
$html = scraperWiki::scrape("http://www.plottsenergy.com/");           
//print $html . "\n";

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("div[@id='highlights']") as $data){
    //echo $data;
    $arr = array(); 
    foreach ($dom->find('td') as $td)
        //array_push($arr, $td->plaintext);
        $record = array(
        'country' => $td[6]->plaintext
    );
    print_r($record);
   //print_r($arr);
}
*/
?>
<?php

$oilSuppliers = array(
    'AmericanFulesPA' => "http://www.americanfuelspa.com/", 
    'PlottsOil' => "http://www.plottsenergy.com/"
);

$html = scraperWiki::scrape("http://www.americanfuelspa.com/");           
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("span[@id='ctl00_lblPrice']") as $data){
    $record = array(
        '_dbkey' => mktime(),
        'price' => $data->plaintext, 
        'date' => date('m.d.y'),
        'time' => date("H:i:s"),
        'company' => "AmericanFuels"
    );
    $message = scraperwiki::save(array('_dbkey'),$record);
    print_r($message);
    //print_r($record);
}
/* Commented out as this needs more work
//parse plotts oil
$html = scraperWiki::scrape("http://www.plottsenergy.com/");           
//print $html . "\n";

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("div[@id='highlights']") as $data){
    //echo $data;
    $arr = array(); 
    foreach ($dom->find('td') as $td)
        //array_push($arr, $td->plaintext);
        $record = array(
        'country' => $td[6]->plaintext
    );
    print_r($record);
   //print_r($arr);
}
*/
?>

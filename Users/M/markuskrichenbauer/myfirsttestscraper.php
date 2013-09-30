<?php
$json = scraperWiki::scrape("https://graph.facebook.com/search?q=n%C3%BCrtingen&type=page&limit=5000");
$mJsonResult=json_decode($json);

//print_r($mJsonResult);
//print $mJsonResult->data[0]->id;

foreach ($mJsonResult->data as $item)
{
    $aModel = array (
        'id'=>$item->id,
        'name'=>$item->name,
        'category'=>$item->category
    );
    scraperwiki::save(array('id','name','category'),$aModel);
}

/*
$html = scraperWiki::scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm");
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@align='left'] tr.tcont") as $data){
    $tds = $data->find("td");
    $record = array(
        'country' => $tds[0]->plaintext, 
        'years_in_school' => intval($tds[5]->plaintext)
    );
       scraperwiki::save(array('years_in_school','country'), $record);
}*/
?>
<?php
$json = scraperWiki::scrape("https://graph.facebook.com/search?q=n%C3%BCrtingen&type=page&limit=5000");
$mJsonResult=json_decode($json);

//print_r($mJsonResult);
//print $mJsonResult->data[0]->id;

foreach ($mJsonResult->data as $item)
{
    $aModel = array (
        'id'=>$item->id,
        'name'=>$item->name,
        'category'=>$item->category
    );
    scraperwiki::save(array('id','name','category'),$aModel);
}

/*
$html = scraperWiki::scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm");
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@align='left'] tr.tcont") as $data){
    $tds = $data->find("td");
    $record = array(
        'country' => $tds[0]->plaintext, 
        'years_in_school' => intval($tds[5]->plaintext)
    );
       scraperwiki::save(array('years_in_school','country'), $record);
}*/
?>

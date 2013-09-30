<?php

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.flipkart.com/mobiles/samsung~brand/pr?sid=tyy%2C4io");

$html = str_get_html($html_content);
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("//*[@id=\"products\"]/div/div/div") as $data){
    $name = $data->find("//h2",0);
    print $name;

    //$name = $name->plaintext;

    /*$rating= $html->find("//*[@id=\"products\"]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div",0);
    $rating= $rating->plaintext;

    $el = $html->find("//*[@id=\"products\"]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[1]/div/b",0);
    $strPrice = $el->plaintext;
    $price = str_replace("Rs.","", $strPrice);
    $price = trim($price);

    $offer= $html->find("//*[@id=\"products\"]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[2]",0);
    $offer= $offer->plaintext;*/

    //scraperwiki::save_sqlite(array("name", "price"),array("name"=>$name, "price"=>$name));

}
?>
<?php

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.flipkart.com/mobiles/samsung~brand/pr?sid=tyy%2C4io");

$html = str_get_html($html_content);
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("//*[@id=\"products\"]/div/div/div") as $data){
    $name = $data->find("//h2",0);
    print $name;

    //$name = $name->plaintext;

    /*$rating= $html->find("//*[@id=\"products\"]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div",0);
    $rating= $rating->plaintext;

    $el = $html->find("//*[@id=\"products\"]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[1]/div/b",0);
    $strPrice = $el->plaintext;
    $price = str_replace("Rs.","", $strPrice);
    $price = trim($price);

    $offer= $html->find("//*[@id=\"products\"]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[2]",0);
    $offer= $offer->plaintext;*/

    //scraperwiki::save_sqlite(array("name", "price"),array("name"=>$name, "price"=>$name));

}
?>

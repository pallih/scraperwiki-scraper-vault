<?php
require 'scraperwiki/simple_html_dom.php';   

//Delete existing data
$info = scraperwiki::table_info($name="swdata");
if(!empty($info)){
    scraperwiki::sqliteexecute("DELETE FROM swdata"); //Truncate the table before adding new results
}

$html = scraperWiki::scrape("http://www.guitarcenter.com/Keyboard-Synthesizers-Keyboards---MIDI,Show-All-Brands.gc");           
//print $html . "\n";
$depth = 150; //Set the link depth (mostly for testing)
$sub_depth = 500;
$counter = 0; //To check the depth
$sub_counter = 0;
$testing = true; //Test variable activates the depth search
        
$dom = new simple_html_dom();
$dom->load($html); //Load the HTML
echo $dom;

$synths = array();
$counter = 0;
foreach($dom->find("div[id=ctl00_ContentLeftNav_divLeftNav] ul[name=Brand] li a[id=categoryMenuItem]") as $data){
    echo $data."\n";
    $synthManufacturer = trim($data->plaintext);
    $synthManufacturer = preg_replace("/\([0-9]+\)/",'',$synthManufacturer);
    $synthManufacturer = trim($synthManufacturer);
    echo $synthManufacturer."\n";
    if(!empty($synthManufacturer)){
        $synthManufacturerLink = $data->href;
        $synthManufacturerLink = "http://www.guitarcenter.com".$synthManufacturerLink."&ipp=100";
        $html2 = scraperWiki::scrape($synthManufacturerLink);
        //echo "Scraping: ".$synthManufacturerLink."\n";
        $dom2 = new simple_html_dom();
        $dom2->load($html2); //Load the HTML
        
        /*foreach($dom2->find("div[id=search_nav] table tbody tr") as $data2){
            //
            foreach($data2->find('td div[class=itemfv-box]') as $data3){
                $itemContainer = $data3->find('div[class=itemfv-content] table tbody tr td',0);
                if(!empty($itemContainer)){
                    //echo $itemContainer;
                    $synthItemImg = $itemContainer->find('div[class=itemfv-photo] a img',0)->src;
                    $synthItemName = $itemContainer->find('div[class=itemfv-link] a',0)->plaintext;
                    $synthItemLink = $itemContainer->find('div[class=itemfv-link] a',0)->href;
                    $synthItemLink = "http://www.guitarcenter.com".$synthItemLink;
                    $priceContainer = $itemContainer->find('div[class=itemfv-info] div[class=itemfv-pricing] p[class=itemfv-price] a',0);
                    if(!empty($priceContainer)){
                        $synthItemPrice = $priceContainer->plaintext;
                        $synthItemPrice = trim(str_replace('GBP','',$synthItemPrice));
                    }else{
                        $synthItemPrice = "";
                    }
                    
                    echo "ImgPath: ".$synthItemImg."\n";
                    echo "Name: ".$synthItemName."\n";
                    echo "URL: ".$synthItemLink."\n";
                    echo "Price: ".$synthItemPrice."\n";
                    $synths[$counter]['manufacturer'] = $synthManufacturer;
                    $synths[$counter]['name'] = $synthItemName;
                    $synths[$counter]['url'] = $synthItemLink;
                    $synths[$counter]['price'] = $synthItemPrice;
                    $synths[$counter]['images'] = $synthItemImg;
                    $counter++;
                }else{
                   //
                }
            }
        }*/
        
    }
}

/*echo "<pre>";
print_r($synths);
echo "</pre>";*/

$saveMessage = scraperWiki::save_sqlite(array('manufacturer','name','url','images'), $synths);
print strval($saveMessage);

scraperwiki::save_var('total_results', count($synths));           
print scraperWiki::get_var('total_results');

?>

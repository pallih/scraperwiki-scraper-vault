<?php
require 'scraperwiki/simple_html_dom.php';   

//Delete existing data
$info = scraperwiki::table_info($name="swdata");
if(!empty($info)){
    scraperwiki::sqliteexecute("DELETE FROM swdata"); //Truncate the table before adding new results
}

$html = scraperWiki::scrape("http://www.bhphotovideo.com/c/search?ipp=25&srtclk=itemspp&ci=12265&N=4294550187");           
//print $html . "\n";
$depth = 150; //Set the link depth (mostly for testing)
$sub_depth = 500;
$counter = 0; //To check the depth
$sub_counter = 0;
$testing = true; //Test variable activates the depth search
        
$dom = new simple_html_dom();
$dom->load($html); //Load the HTML

$synths = array();
$counter = 0;
foreach($dom->find("div[id=attributes] div[class=attGroup brands] ul li a") as $data){
    $synthManufacturer = trim($data->plaintext);
    $synthManufacturer = preg_replace("/\([0-9]+\)/",'',$synthManufacturer);
    $synthManufacturer = trim($synthManufacturer);
    echo $synthManufacturer."\n";
    if(!empty($synthManufacturer)){
        $synthManufacturerLink = $data->href;
        $synthManufacturerLink = $synthManufacturerLink;
        $html2 = scraperWiki::scrape($synthManufacturerLink);
        //echo "Scraping: ".$synthManufacturerLink."\n";
        $dom2 = new simple_html_dom();
        $dom2->load($html2); //Load the HTML
        echo $dom2;
        foreach($dom2->find("div[class=tMain] div[class=tBlock] div[class=productBlock]") as $data2){
            //
            echo $data2;
            if(!empty($data2)){
                $synthItemImg = $itemContainer->find('div[class=productBlockLeft] a img',0)->src;
                $synthItemName = $itemContainer->find('div[class=productBlockCenter] div[id=productTitle] h2 a',0)->plaintext;
                $synthItemLink = $itemContainer->find('div[class=productBlockCenter] a',0)->href;
                $synthItemLink = $synthItemLink."&ipp=100";
                $priceContainer = $itemContainer->find('div[id=productRight] ul[class=priceContainer] li[class=price] span[class=value]',0);
                if(!empty($priceContainer)){
                    $synthItemPrice = $priceContainer->plaintext;
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
<?php
require 'scraperwiki/simple_html_dom.php';   

//Delete existing data
$info = scraperwiki::table_info($name="swdata");
if(!empty($info)){
    scraperwiki::sqliteexecute("DELETE FROM swdata"); //Truncate the table before adding new results
}

$html = scraperWiki::scrape("http://www.bhphotovideo.com/c/search?ipp=25&srtclk=itemspp&ci=12265&N=4294550187");           
//print $html . "\n";
$depth = 150; //Set the link depth (mostly for testing)
$sub_depth = 500;
$counter = 0; //To check the depth
$sub_counter = 0;
$testing = true; //Test variable activates the depth search
        
$dom = new simple_html_dom();
$dom->load($html); //Load the HTML

$synths = array();
$counter = 0;
foreach($dom->find("div[id=attributes] div[class=attGroup brands] ul li a") as $data){
    $synthManufacturer = trim($data->plaintext);
    $synthManufacturer = preg_replace("/\([0-9]+\)/",'',$synthManufacturer);
    $synthManufacturer = trim($synthManufacturer);
    echo $synthManufacturer."\n";
    if(!empty($synthManufacturer)){
        $synthManufacturerLink = $data->href;
        $synthManufacturerLink = $synthManufacturerLink;
        $html2 = scraperWiki::scrape($synthManufacturerLink);
        //echo "Scraping: ".$synthManufacturerLink."\n";
        $dom2 = new simple_html_dom();
        $dom2->load($html2); //Load the HTML
        echo $dom2;
        foreach($dom2->find("div[class=tMain] div[class=tBlock] div[class=productBlock]") as $data2){
            //
            echo $data2;
            if(!empty($data2)){
                $synthItemImg = $itemContainer->find('div[class=productBlockLeft] a img',0)->src;
                $synthItemName = $itemContainer->find('div[class=productBlockCenter] div[id=productTitle] h2 a',0)->plaintext;
                $synthItemLink = $itemContainer->find('div[class=productBlockCenter] a',0)->href;
                $synthItemLink = $synthItemLink."&ipp=100";
                $priceContainer = $itemContainer->find('div[id=productRight] ul[class=priceContainer] li[class=price] span[class=value]',0);
                if(!empty($priceContainer)){
                    $synthItemPrice = $priceContainer->plaintext;
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

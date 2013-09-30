<?php
require 'scraperwiki/simple_html_dom.php';   

//Delete existing data
$info = scraperwiki::table_info($name="swdata");
if(!empty($info)){
    scraperwiki::sqliteexecute("DELETE FROM swdata"); //Truncate the table before adding new results
}

$html = scraperWiki::scrape("http://www.vintagesynth.com/menu.htm");           
//print $html . "\n";
$depth = 150; //Set the link depth (mostly for testing)
$sub_depth = 500;
$counter = 0; //To check the depth
$sub_counter = 0;
$testing = true; //Test variable activates the depth search
        
$dom = new simple_html_dom();
$dom->load($html); //Load the HTML

foreach($dom->find("ul li") as $data){
    $navLink = $data->find("a");

    if(isset($navLink[0]->href)){
        $navLinkURL = $navLink[0]->href;
    }else{
        $navLinkURL = "";
    }
    if($navLinkURL != "" && isset($navLinkURL)){
        echo "Scraping: http://www.vintagesynth.com".$navLinkURL."\n";
        if($testing == true) $counter++;
        if($counter <= $depth){
            $sub_html = scraperWiki::scrape("http://www.vintagesynth.com".$navLinkURL);
            echo "-> Scraping sub page: "."http://www.vintagesynth.com".$navLinkURL."\n";
            $sub_dom = new simple_html_dom();
            $sub_dom->load($sub_html); //Load the HTML
            foreach($sub_dom->find("ul li") as $sub_data){
                if($sub_counter <= $sub_depth){
                    $subNavLink = $sub_data->find("a");
                    $cleanSynthName = trim(str_replace("&bull;","",$subNavLink[0]->plaintext));
                    if(isset($subNavLink[0]->href)){
                        $subNavLinkURL = $subNavLink[0]->href;
                    }else{
                        $subNavLinkURL = "";
                    }
                    
                    $checkExtension = preg_replace('/^.*\.([^.]+)$/D', '$1', $subNavLinkURL);
                    //echo $checkExtension."\n";
                    if($checkExtension == "php"){
                        if($testing == true) $sub_counter++;
                        //Navigate to the url ("http://www.vintagesynth.com".$subNavLinkURL) and pull the data from the view page.
                        $view_html = scraperWiki::scrape("http://www.vintagesynth.com".$subNavLinkURL);
                        echo "--> Scraping view page: "."http://www.vintagesynth.com".$subNavLinkURL."\n";
                        $view_dom = new simple_html_dom();
                        $view_dom->load($view_html); //Load the HTML
                        $subDir = explode("/",$subNavLinkURL);
                        $subDir = "/".$subDir[1]."/";
                        $synthImages = "";
                        foreach($view_dom->find('div[id=left_col] img[class=imgcenter]') as $element){
                            $synthImages .= "http://www.vintagesynth.com".$subDir.$element->src.",";
                        }
                        $synthDescription = "";
                        foreach($view_dom->find("div[class=grid_11] div[id=left_col] p") as $view_data){
                            $synthDescription .= $view_data->plaintext."<br/>";
                        }
                        $synths[] = array(
                            'name' => $cleanSynthName,
                            'manufacturer' => $navLink[0]->plaintext,
                            'url' => "http://www.vintagesynth.com".$subNavLinkURL,
                            'description' => $synthDescription,
                            'images' => $synthImages
                        );
                        /*echo "<pre>";
                        print_r($synths);
                        echo "</pre>";*/
                    }
                }else{
                    break;
                }
            }
        }else{
            print "The scrape has completed at a depth level of $depth.\n";
            break;
        }
    }
}

/*echo "<pre>";
print_r($synths);
echo "</pre>";*/

//$dbName = "vintagesynth-scrape-".$today = date("m-d-Y");
//$saveMessage = scraperWiki::save_sqlite(array('manufacturer','name','url','description','images'), $synths,$table_name=$dbName);
$saveMessage = scraperWiki::save_sqlite(array('manufacturer','name','url','description','images'), $synths);
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

$html = scraperWiki::scrape("http://www.vintagesynth.com/menu.htm");           
//print $html . "\n";
$depth = 150; //Set the link depth (mostly for testing)
$sub_depth = 500;
$counter = 0; //To check the depth
$sub_counter = 0;
$testing = true; //Test variable activates the depth search
        
$dom = new simple_html_dom();
$dom->load($html); //Load the HTML

foreach($dom->find("ul li") as $data){
    $navLink = $data->find("a");

    if(isset($navLink[0]->href)){
        $navLinkURL = $navLink[0]->href;
    }else{
        $navLinkURL = "";
    }
    if($navLinkURL != "" && isset($navLinkURL)){
        echo "Scraping: http://www.vintagesynth.com".$navLinkURL."\n";
        if($testing == true) $counter++;
        if($counter <= $depth){
            $sub_html = scraperWiki::scrape("http://www.vintagesynth.com".$navLinkURL);
            echo "-> Scraping sub page: "."http://www.vintagesynth.com".$navLinkURL."\n";
            $sub_dom = new simple_html_dom();
            $sub_dom->load($sub_html); //Load the HTML
            foreach($sub_dom->find("ul li") as $sub_data){
                if($sub_counter <= $sub_depth){
                    $subNavLink = $sub_data->find("a");
                    $cleanSynthName = trim(str_replace("&bull;","",$subNavLink[0]->plaintext));
                    if(isset($subNavLink[0]->href)){
                        $subNavLinkURL = $subNavLink[0]->href;
                    }else{
                        $subNavLinkURL = "";
                    }
                    
                    $checkExtension = preg_replace('/^.*\.([^.]+)$/D', '$1', $subNavLinkURL);
                    //echo $checkExtension."\n";
                    if($checkExtension == "php"){
                        if($testing == true) $sub_counter++;
                        //Navigate to the url ("http://www.vintagesynth.com".$subNavLinkURL) and pull the data from the view page.
                        $view_html = scraperWiki::scrape("http://www.vintagesynth.com".$subNavLinkURL);
                        echo "--> Scraping view page: "."http://www.vintagesynth.com".$subNavLinkURL."\n";
                        $view_dom = new simple_html_dom();
                        $view_dom->load($view_html); //Load the HTML
                        $subDir = explode("/",$subNavLinkURL);
                        $subDir = "/".$subDir[1]."/";
                        $synthImages = "";
                        foreach($view_dom->find('div[id=left_col] img[class=imgcenter]') as $element){
                            $synthImages .= "http://www.vintagesynth.com".$subDir.$element->src.",";
                        }
                        $synthDescription = "";
                        foreach($view_dom->find("div[class=grid_11] div[id=left_col] p") as $view_data){
                            $synthDescription .= $view_data->plaintext."<br/>";
                        }
                        $synths[] = array(
                            'name' => $cleanSynthName,
                            'manufacturer' => $navLink[0]->plaintext,
                            'url' => "http://www.vintagesynth.com".$subNavLinkURL,
                            'description' => $synthDescription,
                            'images' => $synthImages
                        );
                        /*echo "<pre>";
                        print_r($synths);
                        echo "</pre>";*/
                    }
                }else{
                    break;
                }
            }
        }else{
            print "The scrape has completed at a depth level of $depth.\n";
            break;
        }
    }
}

/*echo "<pre>";
print_r($synths);
echo "</pre>";*/

//$dbName = "vintagesynth-scrape-".$today = date("m-d-Y");
//$saveMessage = scraperWiki::save_sqlite(array('manufacturer','name','url','description','images'), $synths,$table_name=$dbName);
$saveMessage = scraperWiki::save_sqlite(array('manufacturer','name','url','description','images'), $synths);
print strval($saveMessage);

scraperwiki::save_var('total_results', count($synths));           
print scraperWiki::get_var('total_results');

?>

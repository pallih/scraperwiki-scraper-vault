<?php
######################################
# Basic PHP scraper
######################################
date_default_timezone_set("Europe/London");
require  'scraperwiki/simple_html_dom.php';
$node=114; // Manchester page

//Manchester, UK pages of Fillthathole - a pot hole reporting site by the CTC
//Forked to scrape all pages
//Get number of pages
$html = scraperwiki::scrape("http://www.fillthathole.org.uk/node/" . $node . "/hazards");
#print $html;

# Use the PHP Simple HTML DOM Parser to extract pager tags
$dom = new simple_html_dom();
$dom->load($html);

//There are 2 pagers on the page
//Finds the links to the last page
$last = $dom->find("li.pager-last a");
//We only need the first link
$link = $last[0]->href;
$exploded_link = explode("=",$link);
$no_pages = $exploded_link[1];
//Debug
//echo $link . "<br/>";
//echo $no_pages;
//die;

//grab one page at a time starting at the last back to the first
for ($i=0;$i<=$no_pages;$i++) { 
    $page_number = $no_pages - $i;
    $html = scraperwiki::scrape("http://www.fillthathole.org.uk/node/" . $node ."/hazards?page=". $page_number);
    if ($page_number == 0) {
        $html = scraperwiki::scrape("http://www.fillthathole.org.uk/node/" . $node . "/hazards");
    }
    #echo $html;
    #print $html;
    
    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);
    
    //data is held in a simple table
    foreach($dom->find("tr") as $data) {
    
        $tds = $data->find("td");
        if (!empty($tds)) { //hack to ignore table header (th) row
            //Grab all fields
            $record = array("id" => $tds[0]->plaintext,
                            "dateadded" => date("Y-m-d",strtotime($tds[1]->plaintext)),
                            "haref" => $tds[2]->plaintext,
                            "road" => $tds[3]->plaintext,
                            "description" => $tds[4]->plaintext,
                            "status" => $tds[5]->plaintext);     
            //Output
            #print_r($record);
            //Save data with id as the unique key
            scraperwiki::save(array("id"), $record);  
        }
    }
}
?>
<?php
######################################
# Basic PHP scraper
######################################
date_default_timezone_set("Europe/London");
require  'scraperwiki/simple_html_dom.php';
$node=114; // Manchester page

//Manchester, UK pages of Fillthathole - a pot hole reporting site by the CTC
//Forked to scrape all pages
//Get number of pages
$html = scraperwiki::scrape("http://www.fillthathole.org.uk/node/" . $node . "/hazards");
#print $html;

# Use the PHP Simple HTML DOM Parser to extract pager tags
$dom = new simple_html_dom();
$dom->load($html);

//There are 2 pagers on the page
//Finds the links to the last page
$last = $dom->find("li.pager-last a");
//We only need the first link
$link = $last[0]->href;
$exploded_link = explode("=",$link);
$no_pages = $exploded_link[1];
//Debug
//echo $link . "<br/>";
//echo $no_pages;
//die;

//grab one page at a time starting at the last back to the first
for ($i=0;$i<=$no_pages;$i++) { 
    $page_number = $no_pages - $i;
    $html = scraperwiki::scrape("http://www.fillthathole.org.uk/node/" . $node ."/hazards?page=". $page_number);
    if ($page_number == 0) {
        $html = scraperwiki::scrape("http://www.fillthathole.org.uk/node/" . $node . "/hazards");
    }
    #echo $html;
    #print $html;
    
    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);
    
    //data is held in a simple table
    foreach($dom->find("tr") as $data) {
    
        $tds = $data->find("td");
        if (!empty($tds)) { //hack to ignore table header (th) row
            //Grab all fields
            $record = array("id" => $tds[0]->plaintext,
                            "dateadded" => date("Y-m-d",strtotime($tds[1]->plaintext)),
                            "haref" => $tds[2]->plaintext,
                            "road" => $tds[3]->plaintext,
                            "description" => $tds[4]->plaintext,
                            "status" => $tds[5]->plaintext);     
            //Output
            #print_r($record);
            //Save data with id as the unique key
            scraperwiki::save(array("id"), $record);  
        }
    }
}
?>

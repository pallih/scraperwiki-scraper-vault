<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

//Bradford, UK page of Fillthathole - a pot hole reporting site by the CTC
$html = scraperwiki::scrape("http://www.fillthathole.org.uk/node/51/hazards");
#print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

//data is held in a simple table
foreach($dom->find("tr") as $data)
{

    $tds = $data->find("td");
    if (!empty($tds)) { //hack to ignore table header (th) row
        //Grab all fields
        $record = array("id" => $tds[0]->plaintext,
                        "dateadded" => $tds[1]->plaintext,
                        "haref" => $tds[2]->plaintext,
                        "road" => $tds[3]->plaintext,
                        "description" => $tds[4]->plaintext,
                        "status" => $tds[5]->plaintext);     
        //Output
        #print_r($record);
        //Save
        scraperwiki::save(array("id"), $record);  
    }
}
?>
<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

//Bradford, UK page of Fillthathole - a pot hole reporting site by the CTC
$html = scraperwiki::scrape("http://www.fillthathole.org.uk/node/51/hazards");
#print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

//data is held in a simple table
foreach($dom->find("tr") as $data)
{

    $tds = $data->find("td");
    if (!empty($tds)) { //hack to ignore table header (th) row
        //Grab all fields
        $record = array("id" => $tds[0]->plaintext,
                        "dateadded" => $tds[1]->plaintext,
                        "haref" => $tds[2]->plaintext,
                        "road" => $tds[3]->plaintext,
                        "description" => $tds[4]->plaintext,
                        "status" => $tds[5]->plaintext);     
        //Output
        #print_r($record);
        //Save
        scraperwiki::save(array("id"), $record);  
    }
}
?>
<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

//Bradford, UK page of Fillthathole - a pot hole reporting site by the CTC
$html = scraperwiki::scrape("http://www.fillthathole.org.uk/node/51/hazards");
#print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

//data is held in a simple table
foreach($dom->find("tr") as $data)
{

    $tds = $data->find("td");
    if (!empty($tds)) { //hack to ignore table header (th) row
        //Grab all fields
        $record = array("id" => $tds[0]->plaintext,
                        "dateadded" => $tds[1]->plaintext,
                        "haref" => $tds[2]->plaintext,
                        "road" => $tds[3]->plaintext,
                        "description" => $tds[4]->plaintext,
                        "status" => $tds[5]->plaintext);     
        //Output
        #print_r($record);
        //Save
        scraperwiki::save(array("id"), $record);  
    }
}
?>

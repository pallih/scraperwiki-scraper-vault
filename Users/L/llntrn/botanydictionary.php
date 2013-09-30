<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';


//print $html;


$base_url = "http://www.botany.com/";

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$html = scraperwiki::scrape($base_url."index.16.htm");
$dom = new simple_html_dom();
$dom->load($html);


$pages_to_scrape = array();
foreach($dom->find('p[class=lettersIndex] a') as $label){
    print $label->href ."\n";
    array_push($pages_to_scrape,$label->href);
}

    print_r($pages_to_scrape);

foreach($pages_to_scrape as $page){

    $html = scraperwiki::scrape($base_url.$page);
    $sections_dom = new simple_html_dom();
    $sections_dom->load($html);




    
    foreach($sections_dom->find('div[class=content] p') as $data)
    {
        $parts = explode(':',$data,2);
    
       // if(count($parts)>1){
            print_r($parts);
            $entry['term'] = strip_tags($parts[0]);
            $entry['defintion'] = strip_tags($parts[1]);
            scraperwiki::save(array('term'), $entry);
       // }
    }

}
?>
<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';


//print $html;


$base_url = "http://www.botany.com/";

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$html = scraperwiki::scrape($base_url."index.16.htm");
$dom = new simple_html_dom();
$dom->load($html);


$pages_to_scrape = array();
foreach($dom->find('p[class=lettersIndex] a') as $label){
    print $label->href ."\n";
    array_push($pages_to_scrape,$label->href);
}

    print_r($pages_to_scrape);

foreach($pages_to_scrape as $page){

    $html = scraperwiki::scrape($base_url.$page);
    $sections_dom = new simple_html_dom();
    $sections_dom->load($html);




    
    foreach($sections_dom->find('div[class=content] p') as $data)
    {
        $parts = explode(':',$data,2);
    
       // if(count($parts)>1){
            print_r($parts);
            $entry['term'] = strip_tags($parts[0]);
            $entry['defintion'] = strip_tags($parts[1]);
            scraperwiki::save(array('term'), $entry);
       // }
    }

}
?>

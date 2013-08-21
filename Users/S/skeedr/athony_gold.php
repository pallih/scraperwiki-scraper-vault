<?php
$baseurl = "www.anthonygold.co.uk";

$data = array();
$people = array();
$items = array("name" => "div[class=title] h1", "job" => "div[class=job_title]", "phone" => "020 7940 4000", "email" => "div[class=contactEmail]");
$i = 0;

$html = scraperWiki::scrape("http://www.anthonygold.co.uk/site/people/clinicalnegligencedept/");
require 'scraperwiki/simple_html_dom.php';
$html_dom = new simple_html_dom();
$html_dom->load($html);

foreach($html_dom->find("td[class=icon]") as $link){
    //$data['name'] = $link->plaintext;
    print_r($link->href."\r\n");
    foreach($link->find("a") as $href){
        $phtml = scraperWiki::scrape($baseurl.$href->href);
        $phtml_dom = new simple_html_dom();
        $phtml_dom->load($phtml);
        foreach($items as $key => $search){
print_r($search."\r\n");
            foreach($phtml_dom->find($search) as $item){
//print_r($item->plaintext);
                switch($key){
                    case "name":
                        $data[$key] = $item->plaintext;
print_r("Name: ");
                        break;
                    case "job":
                        $data[$key] = $item->plaintext;
print_r("Job: ");
                        break;
                    case "email":
                        print_r("Email: ".$item->href);
                        foreach($item->find("span") as $span){
print_r("Found Span: ".$span->href);
                            foreach($span->find("a") as $alink){
print_r("Found a tag: ");
                                print_r($alink->href);
                                $data[$key] = $alink->href;
                            }
                        }
                        break;
                    case "phone":
                        $data[$key] = $item;
print_r("Phone: ");
                        break;
                }
print_r($item->plaintext."\r\n");
            }
        }
print_r("\r\n");
    }
    $pkey = str_replace(" ", "", $data['name']);
    $people[$pkey] = $data;
}

foreach($people as $person){
    foreach($person as $item){
        print_r($item."\r\n");
    }
    scraperwiki::save_sqlite(array("name"), $person);
}

?>

<?php
$baseurl = "http://www.dacbeachcroft.com";

$data = array();
$people = array();
$items = array("name" => "h1[itemprop=name]", "job" => "h2[itemprop=jobTitle]", "phone" => "div[class=phone]", "email" => "div[class=email]");
$i = 0;

$html = scraperWiki::scrape("http://www.dacbeachcroft.com/people/people-by-expertise/?id=21cbc717d65e4c7daf9a2e851ec69d9a");
require 'scraperwiki/simple_html_dom.php';
$html_dom = new simple_html_dom();
$html_dom->load($html);

foreach($html_dom->find("td[class=person]") as $link){
    $fullname = explode(", ", $link->plaintext);
    $name = $fullname[0]." ".$fullname[1];
    $data['name'] = $name;
    //print_r($link->plaintext."-".$link->first_child->href."\r\n");
    foreach($link->find("a") as $href){
        $phtml = scraperWiki::scrape($baseurl.$href->href);
        $phtml_dom = new simple_html_dom();
        $phtml_dom->load($phtml);
        foreach($items as $key => $search){
            foreach($phtml_dom->find($search) as $item){
                switch($key){
                    case "name":
print_r("Name: ");
                        break;
                    case "job":
                        $data[$key] = $item->plaintext;
print_r("Job: ");
                        break;
                    case "email":
                        $data[$key] = $item->plaintext;
print_r("Email: ");
                        break;
                    case "phone":
                        $data[$key] = $item->plaintext;
print_r("Phone: ");
                        break;
                }
print_r($item->plaintext."\r\n");
            }
        }
print_r($href->href."\r\n");
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
<?php
$baseurl = "http://www.dacbeachcroft.com";

$data = array();
$people = array();
$items = array("name" => "h1[itemprop=name]", "job" => "h2[itemprop=jobTitle]", "phone" => "div[class=phone]", "email" => "div[class=email]");
$i = 0;

$html = scraperWiki::scrape("http://www.dacbeachcroft.com/people/people-by-expertise/?id=21cbc717d65e4c7daf9a2e851ec69d9a");
require 'scraperwiki/simple_html_dom.php';
$html_dom = new simple_html_dom();
$html_dom->load($html);

foreach($html_dom->find("td[class=person]") as $link){
    $fullname = explode(", ", $link->plaintext);
    $name = $fullname[0]." ".$fullname[1];
    $data['name'] = $name;
    //print_r($link->plaintext."-".$link->first_child->href."\r\n");
    foreach($link->find("a") as $href){
        $phtml = scraperWiki::scrape($baseurl.$href->href);
        $phtml_dom = new simple_html_dom();
        $phtml_dom->load($phtml);
        foreach($items as $key => $search){
            foreach($phtml_dom->find($search) as $item){
                switch($key){
                    case "name":
print_r("Name: ");
                        break;
                    case "job":
                        $data[$key] = $item->plaintext;
print_r("Job: ");
                        break;
                    case "email":
                        $data[$key] = $item->plaintext;
print_r("Email: ");
                        break;
                    case "phone":
                        $data[$key] = $item->plaintext;
print_r("Phone: ");
                        break;
                }
print_r($item->plaintext."\r\n");
            }
        }
print_r($href->href."\r\n");
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

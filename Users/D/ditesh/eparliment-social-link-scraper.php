<?php

require 'scraperwiki/simple_html_dom.php';

scraperwiki::sqliteexecute("DELETE FROM eparlimen_social_links");
scraperwiki::attach("eparlimen-constituencies", "urls");
$urls = scraperwiki::select("* FROM urls.eparlimen_constituencies_links");

foreach ($urls as $url) {

    $url = str_replace(",%20", "", $url["url"]);  // A hack for a known bad link. This should be in the link scraper, but it's xmas and I have better things to do :)

    $html = scraperwiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    $node = $dom->find("ul.wrap_senarai li", 2);

    if (is_object($node)) $code = $node->children(1)->plaintext;
    else {

        echo "Unable to parse $url\n";
        continue;

    }
        
    $results = array("id"=>$code);

    foreach($dom->find("div.detail div a") as $data){

        $url = strtolower($data->href);

        # Not the most correct approach, but it should work on most usecases
        if (stristr($url, "facebook")) $results["facebook_url"] = $url;
        else if (stristr($url, "twitter")) $results["twitter_url"] = $url;
        else $results["website_url"] = $url;

        // There are max 3 urls we are interested in
        if (sizeof($results) === 4) break;

    }

    scraperwiki::save_sqlite(array("id"), $results, "eparlimen_social_links");

}

?>
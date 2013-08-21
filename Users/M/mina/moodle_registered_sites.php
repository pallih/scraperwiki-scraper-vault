<?php

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("https://moodle.org/sites/?lang=en");
$html = str_get_html($html_content);

// Get all country codes
$country_codes = array();
foreach ($html->find("p.countrytagcloud a") as $el) {
    $query = parse_str(end(explode("?", $el->href)));
    $country_codes[] = $country;
}
$html->__destruct();

// Visit each country page and get the number of registered sites
foreach ( $country_codes as $code ) {
    //print("https://moodle.org/sites/index.php?lang=en&country=" . $code);
    $html_content = scraperwiki::scrape("https://moodle.org/sites/index.php?lang=en&country=" . $code);
    $html = str_get_html($html_content);
    $country_text = preg_split("/ <img| <span/", $html->find("h3.headingblock", 0)->innertext);
    $country_name = $country_text[0];
    $sites_text = explode(" ",$html->find("h3.headingblock span", 0)->plaintext);
    $registered_sites = $sites_text[0] + 0;
    scraperwiki::save_sqlite(array("Country code"), array("Country code" => $code, "Country name" => $country_name, "Number of sites" => $registered_sites));
    // if ($code == "AR") { break; }
    $html->__destruct();
}

?>
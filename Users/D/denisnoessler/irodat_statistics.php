<?php

require 'scraperwiki/simple_html_dom.php';

$url_base = 'http://www.irodat.org/';
$url_start = $url_base . 'irodat_health_en.php';

$html_content_start = scraperwiki::scrape($url_start);
$html_start = str_get_html($html_content_start);

foreach ($html_start->find('map area') as $country) {           
    if (trim($country->href) == '') continue;
    
    $r_country = array(
        'country' => $country->alt,
        'link' => $url_base . $country->href);

    $html_content_country = scraperwiki::scrape($r_country['link']);
    $html_country = str_get_html($html_content_country);
    
    foreach ($html_country->find('table[width=250] span.IRODaTcontent a[href]') as $year) {
        if (!isset($year->href)) continue;

        $year_num = $year->children(0)->plaintext;
        $url_year = $url_base . $year->href;
                
        $html_content_year = scraperwiki::scrape($url_year);
        $html_year = str_get_html($html_content_year);
        
        $pmp = $html_year->find('tr[height=400] td p[align=center] table[width=910] > tr', 8)->find('table[@width=900]', 2)->find('tr', 1)->find('td', 6)->plaintext;
        $r_country[$year_num] = floatval(str_replace(',', '.', $pmp));
    }
    
    scraperwiki::save(array('country'), $r_country);
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';

$url_base = 'http://www.irodat.org/';
$url_start = $url_base . 'irodat_health_en.php';

$html_content_start = scraperwiki::scrape($url_start);
$html_start = str_get_html($html_content_start);

foreach ($html_start->find('map area') as $country) {           
    if (trim($country->href) == '') continue;
    
    $r_country = array(
        'country' => $country->alt,
        'link' => $url_base . $country->href);

    $html_content_country = scraperwiki::scrape($r_country['link']);
    $html_country = str_get_html($html_content_country);
    
    foreach ($html_country->find('table[width=250] span.IRODaTcontent a[href]') as $year) {
        if (!isset($year->href)) continue;

        $year_num = $year->children(0)->plaintext;
        $url_year = $url_base . $year->href;
                
        $html_content_year = scraperwiki::scrape($url_year);
        $html_year = str_get_html($html_content_year);
        
        $pmp = $html_year->find('tr[height=400] td p[align=center] table[width=910] > tr', 8)->find('table[@width=900]', 2)->find('tr', 1)->find('td', 6)->plaintext;
        $r_country[$year_num] = floatval(str_replace(',', '.', $pmp));
    }
    
    scraperwiki::save(array('country'), $r_country);
}

?>

<?php

# SCRAPE bugmenot.com LOGIN DATA
###########################################

$domain = "nypost.com";
$html = scraperWiki::scrape("http://bugmenot.com/view/" . $domain); 

preg_match_all('|<div class="account"(.*?)</div>|is', $html, $all);
$accs = array();

foreach($all[1] as $item) {
    if(preg_match('|<tr><th>Username </th><td>([-_a-z0-9@]+)</td></tr>|i', $item, $u)
        && preg_match('|<tr><th>Password </th><td>([-_a-z0-9@]+)</td></tr>|i', $item, $p)
        && preg_match('|<tr><th>Other</th><td>([-_a-z0-9@]+)</td></tr>|i', $item, $o)) {
    
        $acc = array(
            'login' => html_entity_decode($u[1]),
            'password' => html_entity_decode($p[1]),
            'other' => html_entity_decode($o[1]),
            'domain' => $domain,
            );    
        scraperwiki::save(array('domain'), $acc); 
    }
}

// done

?>

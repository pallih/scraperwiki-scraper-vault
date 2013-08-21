<?php

//scraperwiki::save_var('last', 0);

scraperwiki::attach("find_4n_profiles");

$links = scraperwiki::select("profile from find_4n_profiles.swdata");

require 'scraperwiki/simple_html_dom.php';
$profile = new simple_html_dom();

foreach( $links as $link ){

    set_time_limit(0);

    $profile_no = intval(str_replace('http://www.4networking.biz/Members/Details/','',$link['profile']));

    if( $profile_no > scraperwiki::get_var('last') ){

        $html = scraperWiki::scrape($link['profile']);
        $profile->load($html);
    
        if( !$company = $profile->find("//*[@id='main']/div[1]/div/div[1]/div[2]/div[1]/div[1]/span/span", 0)->title ){
            $company = $profile->find("//*[@id='main']/div[1]/div/div[1]/div[2]/div[1]/div[1]/span/span", 0)->plaintext;
        }
    
        $website = $profile->find("span.orange-text a",0) ? $profile->find("span.orange-text a",0)->href : '';
    
        if( $profile->find("div.blue3-empty-box div.content div.word-wrap",0) ){
            $info = $profile->find("div.blue3-empty-box div.content div.word-wrap",0)->plaintext;
        } else {
            $info = '';
        }
    
        $record = array(
            'name' => $profile->find("//div/a/span",1)->plaintext,
            'company' => $company,
            'phone' => $profile->find("strong.big-blue3-text span",0)->plaintext,
            'website' => $website
        );
    
        scraperwiki::save(array('company'), $record);
        //print json_encode($record) . "\n";

        scraperwiki::save_var('last', $profile_no);

    }
}

?>

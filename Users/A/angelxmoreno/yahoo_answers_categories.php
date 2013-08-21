<?php
$url_base = 'http://answers.yahoo.com';
$url = $url_base . '/dir/index';
$p_xpath = '//div[@id="yan-categories"]/div[2]/ul/li/a';
$c_xpath = '//*[@id="yan-categories"]/div[2]/ul/li/a';

$p_dom = new DOMDocument;
@$p_dom->loadHTML(scraperwiki::scrape($url));

$p_domxpath = new DOMXPath($p_dom);
foreach (($p_domxpath->query($p_xpath)) as $p_anchor_tag) {
    $p_category = array(
        'id' => str_replace('/dir/index?sid=', '', $p_anchor_tag->getAttribute('href')),
        'name' => $p_anchor_tag->nodeValue,
        'parent_id' => 0,
    );
    $c_url = $url_base . $p_anchor_tag->getAttribute('href');
    $categories[] = $p_category;
    $c_dom = new DOMDocument;
    @$c_dom->loadHTML(scraperwiki::scrape($c_url));
    $c_domxpath = new DOMXPath($c_dom);
    
    foreach (($c_domxpath->query($c_xpath)) as $c_anchor_tag) {
        $c_category = array(
            'id' => str_replace('/dir/index?sid=', '', $c_anchor_tag->getAttribute('href')),
            'name' => $c_anchor_tag->nodeValue,
            'parent_id' => $p_category['id'],
        );
        $categories[] = $c_category;
    }
    
}
scraperwiki::save_sqlite(array('id'), $categories, 'yahoo_answers_categories');
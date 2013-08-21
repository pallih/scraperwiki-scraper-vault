<?php

$html = scraperWiki::scrape("http://ark.intel.com/products/family/1125/Intel-Desktop-Boards");           
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

function GetList( $dom ) {
    foreach ( $dom->find('tr.product-row') as $row )
    {
        $tds = $row->find('td');
        
        $pattern = '/[A-Z]+[0-9]+[A-Z]+([-][0-9]+[A-Z]+)?/';
        $input = $tds[1]->plaintext;
        preg_match( $pattern, $input, $matches );
    
        $uri = $tds[1]->find('a');
    
        #print_r($uri);
    
        $record = array(
            'Name' => $matches[0],
            'URI' => 'http://ark.intel.com' . $uri[0]->href
        );
        
        $output[] = $record;
    }
    return $output;
}

$motherboards = GetList( $dom );
//print_r($motherboards);

function ProductInfo( $motherboards )
{
    foreach ( $motherboards as $mobo )
    {
        $html = scraperWiki::scrape($mobo['URI']);
        $dom = new simple_html_dom();
        $dom->load($html);
        $specs = $dom->find('div#specifications',0);
        $details = array();
        $details['Name'] = $mobo['Name'];
        foreach ( $specs->find('tbody tr') as $row )
        {
            $tds = $row->find('td');
            if ( count($tds) == 2 )
            {
                $details[$tds[0]->plaintext] = $tds[1]->plaintext;
            }
        }
        scraperwiki::save_sqlite( array('Name'), $details);

        $output[] = $details;
    }
    return $output;
}

$info = ProductInfo($motherboards);

?>
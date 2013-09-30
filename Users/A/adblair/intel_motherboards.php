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
        $specs = $dom->find('div#specifications');

        $video = $specs[0]->find('tr#GraphicsOutput td',1)->plaintext;
        $hdmi = preg_match( '/hdmi/', strtolower($video) );
        $vga = preg_match( '/vga/', strtolower($video) );
        $dp = preg_match( '/dp|displayport|display[ ]port/', strtolower($video) );
        
        $details = array(
            'Name' => $mobo['Name'],
            'URI' => $mobo['URI'],
            'Status' => $specs[0]->find('div#infosectionessentials tr',1)->find('td',1)->plaintext,
            'Form factor' => $specs[0]->find('tr#FormFactor td',1)->plaintext,
            'Socket' => $specs[0]->find('tr#SupportedCPUSocket td',1)->plaintext,
            'HDMI' => $hdmi,
            'VGA' => $vga,
            'DP' => $dp
        );
        //print_r($details);
        scraperwiki::save_sqlite( array('Name'), $details);

        $output[] = $details;
    }
    return $output;
}

$info = ProductInfo($motherboards);

?><?php

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
        $specs = $dom->find('div#specifications');

        $video = $specs[0]->find('tr#GraphicsOutput td',1)->plaintext;
        $hdmi = preg_match( '/hdmi/', strtolower($video) );
        $vga = preg_match( '/vga/', strtolower($video) );
        $dp = preg_match( '/dp|displayport|display[ ]port/', strtolower($video) );
        
        $details = array(
            'Name' => $mobo['Name'],
            'URI' => $mobo['URI'],
            'Status' => $specs[0]->find('div#infosectionessentials tr',1)->find('td',1)->plaintext,
            'Form factor' => $specs[0]->find('tr#FormFactor td',1)->plaintext,
            'Socket' => $specs[0]->find('tr#SupportedCPUSocket td',1)->plaintext,
            'HDMI' => $hdmi,
            'VGA' => $vga,
            'DP' => $dp
        );
        //print_r($details);
        scraperwiki::save_sqlite( array('Name'), $details);

        $output[] = $details;
    }
    return $output;
}

$info = ProductInfo($motherboards);

?>
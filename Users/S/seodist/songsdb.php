<?php
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape('http://www.raaga.com/channels/tamil/movies.asp');
$dom = new DOMDocument(); 
@$dom->loadHtml($html);
$xpath = new DOMXPath($dom);
$articleList = $xpath->query("//a[@class='blackNoLine']"); 
$count = 0;
foreach ($articleList as $item)
{
    if ($count > 1993)
   {
    // echo $item->nodeValue;
    $url = "http://www.raaga.com".$item->getAttribute('href');
    $movie = $item->nodeValue;
    echo $movie;
    // echo $url;
    print "\n";
    $html2 = scraperwiki::scrape($url);
    $dom2 = new simple_html_dom();
    $dom2->load($html2);
        foreach($dom2->find('div[style="margin-bottom:10px;height:75px;"]') as $data2)
        {
        $songdata = $data2->plaintext;
        //$songname = $data2->find('div(class="lftFlt1")');
        //echo $songname;
        //echo $songname[1];
        $record = array('movie'=>$movie, 'songdata' => $songdata);
        scraperwiki::save_sqlite(array("movie","songdata"),$record,"songsdb");
        print "\n";
        } 
    }  
    $count = $count + 1;    
}

?>
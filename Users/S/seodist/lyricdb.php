<?php
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape('http://www.paadalvarigal.com/songfilmindex.php');
$dom = new DOMDocument(); 
@$dom->loadHtml($html);
$xpath = new DOMXPath($dom);
$articleList = $xpath->query("//*[@id='content-wrap']//a"); 
//print 'before';
foreach ($articleList as $item)
{
    //echo 'inside';
    //echo $item->nodeValue;
    $url1 = "http://www.paadalvarigal.com".$item->getAttribute('href');
    //$movie = $item->nodeValue;
    //echo $movie;
    echo $url1;
    print "\n";
    $html2 = scraperwiki::scrape($url1);
    $dom2 = new simple_html_dom();
    $dom2->load($html2);
        //echo 'before2';
        foreach($dom2->find('div[itemtype="http://schema.org/Movie"] a') as $data2)
        {
            //echo 'iside 2';
            $url2 =  $data2->getAttribute('href');
            $songtitle = $data2->plaintext;
            echo $url2;
            print "\n";

            $html3 = scraperwiki::scrape($url2);
            $dom3 = new simple_html_dom();
            $dom3->load($html3);
            $lyricscontent = $dom3->find('//*[@id="lyricscontent"]/');
            $lyricsdetail = $dom3->find('//*[@id="main"]/ul/li');
            $lyricsmovie = $dom3->find('//*[@id="lyricscontent"]/h4');

            foreach ($lyricsmovie as $item4)
                {
               $lyricmovie1 =  $item4->plaintext;
                }

            foreach ($lyricscontent as $item3)
                {
                $lyriccontent1 =  $item3->plaintext;
                //echo $lyriccontent1;
                }

               $record = array('movie'=>$lyricmovie1 ,'content' => $lyriccontent1 ,'detail' => $songtitle );
               scraperwiki::save_sqlite(array("movie","content","detail"),$record,"lyricdb");
                print "\n";

        }
  
}


?><?php
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape('http://www.paadalvarigal.com/songfilmindex.php');
$dom = new DOMDocument(); 
@$dom->loadHtml($html);
$xpath = new DOMXPath($dom);
$articleList = $xpath->query("//*[@id='content-wrap']//a"); 
//print 'before';
foreach ($articleList as $item)
{
    //echo 'inside';
    //echo $item->nodeValue;
    $url1 = "http://www.paadalvarigal.com".$item->getAttribute('href');
    //$movie = $item->nodeValue;
    //echo $movie;
    echo $url1;
    print "\n";
    $html2 = scraperwiki::scrape($url1);
    $dom2 = new simple_html_dom();
    $dom2->load($html2);
        //echo 'before2';
        foreach($dom2->find('div[itemtype="http://schema.org/Movie"] a') as $data2)
        {
            //echo 'iside 2';
            $url2 =  $data2->getAttribute('href');
            $songtitle = $data2->plaintext;
            echo $url2;
            print "\n";

            $html3 = scraperwiki::scrape($url2);
            $dom3 = new simple_html_dom();
            $dom3->load($html3);
            $lyricscontent = $dom3->find('//*[@id="lyricscontent"]/');
            $lyricsdetail = $dom3->find('//*[@id="main"]/ul/li');
            $lyricsmovie = $dom3->find('//*[@id="lyricscontent"]/h4');

            foreach ($lyricsmovie as $item4)
                {
               $lyricmovie1 =  $item4->plaintext;
                }

            foreach ($lyricscontent as $item3)
                {
                $lyriccontent1 =  $item3->plaintext;
                //echo $lyriccontent1;
                }

               $record = array('movie'=>$lyricmovie1 ,'content' => $lyriccontent1 ,'detail' => $songtitle );
               scraperwiki::save_sqlite(array("movie","content","detail"),$record,"lyricdb");
                print "\n";

        }
  
}


?>
<?php

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.canthoinfo.com/ttraovat.asp?kind=dienthoai");
$html = str_get_html($html_content);
$data = array();
foreach($html->find('table#AutoNumber29') as $tb)
{
   foreach($tb->find('tr') as $tr)
    {
        $i=0;
        foreach($tr->find('td a') as $a)
         {
              $html_content = scraperwiki::scrape("http://www.canthoinfo.com/".$a->href);
              $html2 = str_get_html($html_content);
              foreach($html2->find('table#AutoNumber27') as $tb2)
                {
                    $title = $tb2->find('tr',0)->find('td',0)->plaintext;
                    $content = $tb2->find('tr',1)->find('td',0)->innertext;
                }
              foreach($html2->find('table#AutoNumber28') as $tb3)
                {
                    $ten = $tb3->find('tr',0)->find('td',2)->plaintext;
                    $dt = $tb3->find('tr',2)->find('td',2)->plaintext;
                    $dc = $tb3->find('tr',3)->find('td',2)->plaintext;
                }
                $i++;
                @scraperwiki::save_sqlite(array('title'),array('title'=>$title,'content'=>$content,'ten'=>$ten,'dt'=>$dt,'dc'=>$dc)); 
            $html2->clear(); 
            unset($html2);
         }
    }
}

?>

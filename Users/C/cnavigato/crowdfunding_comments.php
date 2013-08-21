<?php
// Gets basic data and links for invasive species from the MN DNR

         
require 'scraperwiki/simple_html_dom.php';

    $html = scraperWiki::scrape("http://www.sec.gov/comments/jobs-title-iii/jobs-title-iii.shtml");
    $dom = new simple_html_dom();
    $dom->load($html);
    $count = 0;
    $base_url = "http://www.sec.gov";

    foreach($dom->find("tr[onMouseOver]") as $rows) {
        $count++;
        $data = $rows->find("td");
        $comment_date = $data[0]->plaintext;
        $comment_date = date_create($comment_date);
        $name = $data[1]->plaintext;
        $link_url = $data[1]->find("a");
        if (!empty($data[0]->plaintext)) {
            $record = array(
                'id' => $count,
                'comment_date' => $comment_date,
                'name' => $name,
                'link' => $base_url . $link_url[0]->href
            );
    
            scraperwiki::save(array('id'), $record);

        }
    }


?>
<?php
         
require 'scraperwiki/simple_html_dom.php';

    $html = scraperWiki::scrape("http://www.scrapmonster.com/moreprice/usa-westcost/7/1");
    $dom = new simple_html_dom();
    $dom->load($html);
    $count = 0;
    //$base_url = "http://www.scrapmonster.com/moreprice";

    //foreach($dom->find("tr[onMouseOver]") as $rows) {
    $data = $dom->find("div[@class=down-area]");
    //$lists = $data->find("ul");
    //$header = $lists[0];
    //$values = $lists[1];
    
    print json_encode($data);
   // print json_encode($values);



        //$count++;
        //$data = $rows->find("td");
        //$comment_date = $data[0]->plaintext;
        //$comment_date = date_create($comment_date);
        //$name = $data[1]->plaintext;
        //$link_url = $data[1]->find("a");
        //if (!empty($data[0]->plaintext)) {
            //$record = array(
                //'id' => $count,
               // 'comment_date' => $comment_date,
               // 'name' => $name,
                //'link' => $base_url . $link_url[0]->href
           // );
    
           // scraperwiki::save(array('id'), $record);
           //print json_encode($rows);

?>
<?php
         
require 'scraperwiki/simple_html_dom.php';

    $html = scraperWiki::scrape("http://www.scrapmonster.com/moreprice/usa-westcost/7/1");
    $dom = new simple_html_dom();
    $dom->load($html);
    $count = 0;
    //$base_url = "http://www.scrapmonster.com/moreprice";

    //foreach($dom->find("tr[onMouseOver]") as $rows) {
    $data = $dom->find("div[@class=down-area]");
    //$lists = $data->find("ul");
    //$header = $lists[0];
    //$values = $lists[1];
    
    print json_encode($data);
   // print json_encode($values);



        //$count++;
        //$data = $rows->find("td");
        //$comment_date = $data[0]->plaintext;
        //$comment_date = date_create($comment_date);
        //$name = $data[1]->plaintext;
        //$link_url = $data[1]->find("a");
        //if (!empty($data[0]->plaintext)) {
            //$record = array(
                //'id' => $count,
               // 'comment_date' => $comment_date,
               // 'name' => $name,
                //'link' => $base_url . $link_url[0]->href
           // );
    
           // scraperwiki::save(array('id'), $record);
           //print json_encode($rows);

?>

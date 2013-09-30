<?php

# Blank PHP

$html = scraperWiki::scrape("http://www.google.co.in/#q=Easy+loans&hl=en&prmd=imvns&ei=2I9UUMCVM4TorQfcqoDwCw&start=20&sa=N&bav=on.3,or.r_gc.r_pw.r_qf.&fp=fffd88ca7a51950&biw=1309&bih=704");           
#print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("div[@id='content']/div/ul/li/a") as $data){
   # $tds = $data->find("td");
    $record = array(
        'name' => $data->plaintext
   #     'country' => $tds[0]->plaintext, 
   #     'years_in_school' => intval($tds[4]->plaintext)
    );
    print_r($record);
}

?>
<?php

# Blank PHP

$html = scraperWiki::scrape("http://www.google.co.in/#q=Easy+loans&hl=en&prmd=imvns&ei=2I9UUMCVM4TorQfcqoDwCw&start=20&sa=N&bav=on.3,or.r_gc.r_pw.r_qf.&fp=fffd88ca7a51950&biw=1309&bih=704");           
#print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("div[@id='content']/div/ul/li/a") as $data){
   # $tds = $data->find("td");
    $record = array(
        'name' => $data->plaintext
   #     'country' => $tds[0]->plaintext, 
   #     'years_in_school' => intval($tds[4]->plaintext)
    );
    print_r($record);
}

?>

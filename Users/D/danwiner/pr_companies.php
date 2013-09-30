<?php
require 'scraperwiki/simple_html_dom.php';           
    $n=1;
while ($n<=999):
    if (strlen($n)==1){
        $n="00".$n;}
    elseif (strlen($n)==2){
        $n="0".$n;}
    else{
        $n=$n;}
    $url="http://www.prca.org.uk/prcaMembers.asp?ltr=all&mbd=".$n;
    $html = scraperWiki::scrape($url);
    $n++;
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table.rosterTable") as $data){
    $tds = $data->find("td");
    $record = array(
        '1' => urlencode($tds[0]->plaintext),
        '2' => urlencode($tds[1]->plaintext),
'3' => urlencode($tds[2]->plaintext),
'4' => urlencode($tds[3]->plaintext),
'5' => urlencode($tds[4]->plaintext),
'6' => urlencode($tds[5]->plaintext),
'7' => urlencode($tds[6]->plaintext),
'8' => urlencode($tds[7]->plaintext),
'9' => urlencode($tds[8]->plaintext),
'10' => urlencode($tds[9]->plaintext)
    );
    print_r($record);
    };
scraperwiki::save(array('1','2','3','4','5','6','7','8','9','10'), $record); 
endwhile;
?>
<?php
require 'scraperwiki/simple_html_dom.php';           
    $n=1;
while ($n<=999):
    if (strlen($n)==1){
        $n="00".$n;}
    elseif (strlen($n)==2){
        $n="0".$n;}
    else{
        $n=$n;}
    $url="http://www.prca.org.uk/prcaMembers.asp?ltr=all&mbd=".$n;
    $html = scraperWiki::scrape($url);
    $n++;
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table.rosterTable") as $data){
    $tds = $data->find("td");
    $record = array(
        '1' => urlencode($tds[0]->plaintext),
        '2' => urlencode($tds[1]->plaintext),
'3' => urlencode($tds[2]->plaintext),
'4' => urlencode($tds[3]->plaintext),
'5' => urlencode($tds[4]->plaintext),
'6' => urlencode($tds[5]->plaintext),
'7' => urlencode($tds[6]->plaintext),
'8' => urlencode($tds[7]->plaintext),
'9' => urlencode($tds[8]->plaintext),
'10' => urlencode($tds[9]->plaintext)
    );
    print_r($record);
    };
scraperwiki::save(array('1','2','3','4','5','6','7','8','9','10'), $record); 
endwhile;
?>

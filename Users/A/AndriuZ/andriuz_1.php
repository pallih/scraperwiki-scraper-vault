<?php
# Blank PHP
print "Hello, coding in the cloud!";
$html = scraperwiki::scrape("http://www.vrk.lt/rinkimai/99_lt/Ikainiai/zpIkainiai_Alytaus%20regionin%C4%97%20televizija_2011.html");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table[@align='left'] tr.tcont") as $data){
    $tds = $data->find("td");
    $record = array(
        'Įkainio pavadinimas' => $tds[0]->plaintext, 
        #'Pateikta' => intval($tds[4]->plaintext)
        'Pateikta' => $tds[0]->plaintext, 
        'Mato vnt.'=> $tds[0]->plaintext, 
        'Įkainis su PVM, Lt nuo' => $tds[0]->plaintext, 
        'Įkainis su PVM, Lt iki' => $tds[0]->plaintext, 
        'Sąlygos' => $tds[0]->plaintext,

    );
        scraperwiki::save(array('Įkainio pavadinimas','Pateikta'), $record);

}
?>
<?php
# Blank PHP
print "Hello, coding in the cloud!";
$html = scraperwiki::scrape("http://www.vrk.lt/rinkimai/99_lt/Ikainiai/zpIkainiai_Alytaus%20regionin%C4%97%20televizija_2011.html");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table[@align='left'] tr.tcont") as $data){
    $tds = $data->find("td");
    $record = array(
        'Įkainio pavadinimas' => $tds[0]->plaintext, 
        #'Pateikta' => intval($tds[4]->plaintext)
        'Pateikta' => $tds[0]->plaintext, 
        'Mato vnt.'=> $tds[0]->plaintext, 
        'Įkainis su PVM, Lt nuo' => $tds[0]->plaintext, 
        'Įkainis su PVM, Lt iki' => $tds[0]->plaintext, 
        'Sąlygos' => $tds[0]->plaintext,

    );
        scraperwiki::save(array('Įkainio pavadinimas','Pateikta'), $record);

}
?>

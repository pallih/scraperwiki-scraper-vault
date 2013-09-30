<?php

require 'scraperwiki/simple_html_dom.php';

$html = file_get_html("http://comdinheiro.com.br/Fundamentalista1-02020-20100331-AP-ABYA3%20-consolidado-SOCIETARIO-comdinheiro-1");

$dom = new simple_html_dom();
$dom->load($html);
$ret = $html->find('div[id=RENTA1] td');

/**
foreach ($ret as $i => $value) {
    print($ret[$i]);
    print "\n";
    print $ret[$i]->plaintext;
    print "\n";
}
**/


print "ROE P/L \n";
print $ret[2]->plaintext;
print " ";
print $ret[14]->plaintext;





?><?php

require 'scraperwiki/simple_html_dom.php';

$html = file_get_html("http://comdinheiro.com.br/Fundamentalista1-02020-20100331-AP-ABYA3%20-consolidado-SOCIETARIO-comdinheiro-1");

$dom = new simple_html_dom();
$dom->load($html);
$ret = $html->find('div[id=RENTA1] td');

/**
foreach ($ret as $i => $value) {
    print($ret[$i]);
    print "\n";
    print $ret[$i]->plaintext;
    print "\n";
}
**/


print "ROE P/L \n";
print $ret[2]->plaintext;
print " ";
print $ret[14]->plaintext;





?>
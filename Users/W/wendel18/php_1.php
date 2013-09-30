<?php    
require 'scraperwiki/simple_html_dom.php';

// Create DOM from URL or file
$html = file_get_html('http://nadaguides.com/Cars/1996/Lincoln/Continental-V8/Sedan-4D/Values');

// Find table that contains prices
$table= $html->find('table[class]');
//Find price last cell
$td = $table[0]->find('td');
$data = $td[19]->plaintext; 

// Find table that contains prices
$h1 = $html->find('h1');
//Find price last cell
$h1clean = $h1[0]->plaintext; 

//Remove special characters
$data2 = str_replace("$", "", $data);
$data2 = str_replace(",", "", $data2);
 
$message = scraperwiki::save_sqlite(array("price"), array("price"=>$data2, "title"=>$h1clean));

?>
<?php    
require 'scraperwiki/simple_html_dom.php';

// Create DOM from URL or file
$html = file_get_html('http://nadaguides.com/Cars/1996/Lincoln/Continental-V8/Sedan-4D/Values');

// Find table that contains prices
$table= $html->find('table[class]');
//Find price last cell
$td = $table[0]->find('td');
$data = $td[19]->plaintext; 

// Find table that contains prices
$h1 = $html->find('h1');
//Find price last cell
$h1clean = $h1[0]->plaintext; 

//Remove special characters
$data2 = str_replace("$", "", $data);
$data2 = str_replace(",", "", $data2);
 
$message = scraperwiki::save_sqlite(array("price"), array("price"=>$data2, "title"=>$h1clean));

?>

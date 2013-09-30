<?php

# Blank PHP

$url="http://thonegger.com/dir/JournalFinal.txt";
$journaux=scraperwiki::scrape($url);

$csvNumColumns = 3; 
$csvDelim = ","; 
$data = array_chunk(str_getcsv($journaux, $csvDelim), $csvNumColumns);
print scraperwiki::get_var('data');



?>

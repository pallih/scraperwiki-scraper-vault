<?php
   
$file='http://www.fingalcoco.public-i.tv/core/data/2691/agenda/1.xml';
$xml = simplexml_load_file($file);
$f = fopen('fingalmeetings.csv', 'w');

foreach ($xml->item as $item)
{   
    fputcsv($f, get_object_vars($item),'|','"');
}
fclose($f);

?>
<?php
   
$file='http://www.fingalcoco.public-i.tv/core/data/2691/agenda/1.xml';
$xml = simplexml_load_file($file);
$f = fopen('fingalmeetings.csv', 'w');

foreach ($xml->item as $item)
{   
    fputcsv($f, get_object_vars($item),'|','"');
}
fclose($f);

?>
<?php
   
$file='http://www.fingalcoco.public-i.tv/core/data/2691/agenda/1.xml';
$xml = simplexml_load_file($file);
$f = fopen('fingalmeetings.csv', 'w');

foreach ($xml->item as $item)
{   
    fputcsv($f, get_object_vars($item),'|','"');
}
fclose($f);

?>
<?php
   
$file='http://www.fingalcoco.public-i.tv/core/data/2691/agenda/1.xml';
$xml = simplexml_load_file($file);
$f = fopen('fingalmeetings.csv', 'w');

foreach ($xml->item as $item)
{   
    fputcsv($f, get_object_vars($item),'|','"');
}
fclose($f);

?>

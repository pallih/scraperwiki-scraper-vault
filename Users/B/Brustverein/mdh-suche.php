<?php

require 'scraperwiki/simple_html_dom.php'; 

$seite = 3;
$offset = 15;

$html_content = scraperwiki::scrape("http://www.mydirtyhobby.com/?ac=search&ac2=umgebung&plz=2#type|1|ac|search|anf|".$seite*$offset."|ac2|umgebung|plz|2|gender|F|module|get"); 
$html = str_get_html($html_content); 

foreach ($html->find("div.amateurs_block .am_name_block a") as $el) { 


preg_match ('/"(.*?)"/',$el,$el);
$URL = $el[1];
print $URL."\n";
}
?>
<?php

require 'scraperwiki/simple_html_dom.php'; 

$seite = 3;
$offset = 15;

$html_content = scraperwiki::scrape("http://www.mydirtyhobby.com/?ac=search&ac2=umgebung&plz=2#type|1|ac|search|anf|".$seite*$offset."|ac2|umgebung|plz|2|gender|F|module|get"); 
$html = str_get_html($html_content); 

foreach ($html->find("div.amateurs_block .am_name_block a") as $el) { 


preg_match ('/"(.*?)"/',$el,$el);
$URL = $el[1];
print $URL."\n";
}
?>

<?php
require 'scraperwiki/simple_html_dom.php';

$url = 'http://www.cs.virginia.edu/~robins/quotes.html';

$html = file_get_html($url);

foreach($html->find('dt') as $e)
{
echo $e;
}
?>
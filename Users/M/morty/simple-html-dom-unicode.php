<?php
require  'scraperwiki/simple_html_dom.php';

$htmlParser = new simple_html_dom();
$htmlParser->load('<html><body><a href="default.asp?housetype=0&amp;HouseNum=1&amp;MemberID=38&amp;ConstID=110"><b>Mr. Piaras Béaslaí</b></a></body></html>');
$images = $htmlParser->find('a');
print $images[0]->plaintext;
?>
<?php
require  'scraperwiki/simple_html_dom.php';

$htmlParser = new simple_html_dom();
$htmlParser->load('<html><body><a href="default.asp?housetype=0&amp;HouseNum=1&amp;MemberID=38&amp;ConstID=110"><b>Mr. Piaras Béaslaí</b></a></body></html>');
$images = $htmlParser->find('a');
print $images[0]->plaintext;
?>

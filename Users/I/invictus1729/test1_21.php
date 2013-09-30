<?php
require 'scraperwiki/simple_html_dom.php';
$html=file_get_html("http://www.flipkart.com/art-arts-photography-and-design-books-3");

//$image=array();
//$linka=array();

foreach($html->find('a') as $element){
$data=array(
'image'=>$element->href
);
scraperwiki::save(array('image'),$data);
}

?>

<?php
require 'scraperwiki/simple_html_dom.php';
$html=file_get_html("http://www.flipkart.com/art-arts-photography-and-design-books-3");

//$image=array();
//$linka=array();

foreach($html->find('a') as $element){
$data=array(
'image'=>$element->href
);
scraperwiki::save(array('image'),$data);
}

?>


 <?php
    require 'scraperwiki/simple_html_dom.php';
$html=file_get_html('http://www.flipkart.com/arts-photography-and-design-books-2#scrollTo=1;');
foreach($html->find('div[id=search_results]') as $cha)
{
$count=0;
    foreach($cha->find('img') as $cha1){
        if($cha1->title!=null)
$count=$count+1;
            echo $cha1->title;
}
echo $count;
}




?>

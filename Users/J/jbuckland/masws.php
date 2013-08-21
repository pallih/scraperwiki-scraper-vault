<?php
require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://www.jamesbuckland.com/masws/liv.html");
$html = str_get_html($html_content);
$result = "";
$result .= "@base <http://www.jamesbuckland.com/masws/liv.html#>" . "\n";     
$result .= "@prefix address: <http://schemas.talis.com/2005/address/schema#> ." . "\n";
$result .= "@prefix db: <http://dbpedia.org/ontology/> ." . "\n";

 
     
foreach ($html->find("table.datatable") as $el) {   
       
    

    $ref = $el->find("td.ref a",0);
    $ref = $ref->innertext;
    $ref = trim(str_replace(' ', '', $ref));
    $result .= '<'.$ref.'> db:id "'.$ref.'" .' ."\n";

    $name = $el->find("td.name",0);
    $name = trim($name->innertext);
    $propname = str_replace(' ', '_', $name);
    $result .= '<'.$ref.'> db:company "'.$name.'" .' ."\n";

    $type = $el->find("td.type",0);
    $type = $type->innertext;
    $result .= '<'.$ref.'> db:type "'.$type.'" .' ."\n";

    $wiki = $el->find("td.wiki a",0);  
    if (isset($wiki)) {
        $wiki = $wiki->href;
        $result .= '<'.$ref.'> db:wikiPageExternalLink <'.$wiki.'> .' ."\n";    }
    else {
        $result .= '<'.$ref.'> db:wikiPageExternalLink "None" .' ."\n";
    }

    $trade = $el->find("td.trade",0);
    $trade = $trade->innertext;
    $result .= '<'.$ref.'> db:profession "'.$type.'" .' ."\n";

    $exp = $el->find("td.exp",0);
    $exp = $exp->innertext;
    $result .= '<'.$ref.'> db:desc "'.$exp.'" .' ."\n";

    $char = $el->find("td.char",0);
    $char = $char->innertext;
    $result .= '<'.$ref.'> db:date "'.$char.'" .' ."\n";

    $db = $el->find("td.db a",0);
    if (isset($db)) {
        $db = $db->href;
        $result .= '<'.$ref.'> db:source <'.$db.'> .' ."\n";
    }
    else {
        $result .= '<'.$ref.'> db:source "None" .' ."\n";
    }
    

    $ico = $el->find("td.ico a",0);
    if (isset($ico)) {
        $ico = $ico->href;
        $result .= '<'.$ref.'> db:source <'.$ico.'> .' ."\n";
    }
    else {
        $result .= '<'.$ref.'> db:source "None" .' ."\n";
    }

    $add = $el->find("td.add",0);
    $add = trim($add->innertext);
    $result .= '<'.$ref.'> address:streetAddress "'.$add.'" .' ."\n";

    $post = $el->find("td.post",0);
    $post = trim($post->innertext);
    $result .= '<'.$ref.'> address:postalCode "'.$post.'" .' ."\n";
    
    $phone = $el->find("td.phone",0);
    $phone = trim($phone->innertext);
    $result .= '<'.$ref.'> address:tel "'.$phone.'" . ' ."\n";

    $web = $el->find("td.web a",0);
    $web = $web->href;
    $result .= '<'.$ref.'> db:homepage <'.$web.'> .' ."\n";

    //$linked = $el->find("td.linked a",0);
    //if(isset($linked)) {
    //    $result .= $linked->href ."\n";
    //}
    //else {
    //    $result .= "No Profile. \n";
    //}

    //$hall = $el->find("td.hall a",0);
    //$result .= $hall->href ."\n";

    $colour = $el->find("td.colour",0);
    $colour = $colour->innertext;
    $result .= '<'.$ref.'> db:colour "'.$colour.'" .' ."\n";
    
    //foreach ($el->find("td.links ul li") as $links) {
    //    $link = $links->find("a",0);        
    //    if(isset($link)) {
    //        $result .= $link->href ."\n";
    //    }
    //    else {
    //        $result .= $links->innertext ."\n";
    //    }        
  // }
    //
  //  foreach ($el->find("td.res a") as $res) {
    //    $result .= $res->href ."\n";      
    //}
}
$arr = array ('one' => $result);
scraperwiki::save(array('one'), $arr);   
?>

<?php
$html = scraperWiki::scrape("http://oxfordshire.b4-business.com/business-directory-navigation?term_node_tid_depth=Any");
require 'scraperwiki/simple_html_dom.php';
$directory = new simple_html_dom();
$directory->load($html);

foreach($directory->find(".view-business-directory-navigation .view-content .views-row .views-field-title a") as $link){

    $company_page_html = scraperWiki::scrape("http://oxfordshire.b4-business.com" . $link->href);
    $company_dom = new simple_html_dom();
    $company_dom->load($company_page_html);

    if(  $company_dom->find("#pagetop-chessboard-bottom-right .field-field-contact .field-item", 0) ){
        $name = trim(str_replace("Contact:&nbsp;", "", $company_dom->find("#pagetop-chessboard-bottom-right .field-field-contact .field-item", 0)->plaintext));
    } else {
        $name = '';
    }

    // Get Phone
    if( $company_dom->find("#pagetop-chessboard-bottom-right .field-field-telephone .field-item", 0)){
        $phone = trim(str_replace("Telephone:&nbsp;", "", $company_dom->find("#pagetop-chessboard-bottom-right .field-field-telephone .field-item", 0)->plaintext));
    } else {
        $phone = '';
    }

    if( $company_dom->find("#pagetop-chessboard-bottom-right .field-field-email a", 0) ){
        $email = $company_dom->find("#pagetop-chessboard-bottom-right .field-field-email a", 0)->plaintext;
    } else {
        $email = '';
    }

    if( $company_dom->find("#pagetop-chessboard-bottom-right .field-field-address .field-item", 0) ){
        $address = trim(str_replace("Address:&nbsp;", "", $company_dom->find("#pagetop-chessboard-bottom-right .field-field-address .field-item", 0)->plaintext));
    } else {
        $address = '';
    }

    if( $company_dom->find("#pagetop-chessboard-bottom-right .field-field-web .field-item", 0) ){
        $web = trim(str_replace("Web:&nbsp;", "", $company_dom->find("#pagetop-chessboard-bottom-right .field-field-web .field-item", 0)->plaintext));
    } else {
        $web = '';
    }
    //$value = mb_check_encoding($value, 'UTF-8') ? $value : utf8_encode($value);

    $record = array(
        'company' => html_entity_decode($company_dom->find("#pagetop-chessboard-bottom-right h3", 0)->plaintext),
        'name' => $name,
        'email' => $email,
        'phone' => $phone,
        'address' => $address,
        'web' => $web,
        'notes' => $company_dom->find("#inner-content", 0)->plaintext
    );

    scraperwiki::save(array('company'), $record);
    //print json_encode($record) . "\n";

}
?>
<?php
$html = scraperWiki::scrape("http://oxfordshire.b4-business.com/business-directory-navigation?term_node_tid_depth=Any");
require 'scraperwiki/simple_html_dom.php';
$directory = new simple_html_dom();
$directory->load($html);

foreach($directory->find(".view-business-directory-navigation .view-content .views-row .views-field-title a") as $link){

    $company_page_html = scraperWiki::scrape("http://oxfordshire.b4-business.com" . $link->href);
    $company_dom = new simple_html_dom();
    $company_dom->load($company_page_html);

    if(  $company_dom->find("#pagetop-chessboard-bottom-right .field-field-contact .field-item", 0) ){
        $name = trim(str_replace("Contact:&nbsp;", "", $company_dom->find("#pagetop-chessboard-bottom-right .field-field-contact .field-item", 0)->plaintext));
    } else {
        $name = '';
    }

    // Get Phone
    if( $company_dom->find("#pagetop-chessboard-bottom-right .field-field-telephone .field-item", 0)){
        $phone = trim(str_replace("Telephone:&nbsp;", "", $company_dom->find("#pagetop-chessboard-bottom-right .field-field-telephone .field-item", 0)->plaintext));
    } else {
        $phone = '';
    }

    if( $company_dom->find("#pagetop-chessboard-bottom-right .field-field-email a", 0) ){
        $email = $company_dom->find("#pagetop-chessboard-bottom-right .field-field-email a", 0)->plaintext;
    } else {
        $email = '';
    }

    if( $company_dom->find("#pagetop-chessboard-bottom-right .field-field-address .field-item", 0) ){
        $address = trim(str_replace("Address:&nbsp;", "", $company_dom->find("#pagetop-chessboard-bottom-right .field-field-address .field-item", 0)->plaintext));
    } else {
        $address = '';
    }

    if( $company_dom->find("#pagetop-chessboard-bottom-right .field-field-web .field-item", 0) ){
        $web = trim(str_replace("Web:&nbsp;", "", $company_dom->find("#pagetop-chessboard-bottom-right .field-field-web .field-item", 0)->plaintext));
    } else {
        $web = '';
    }
    //$value = mb_check_encoding($value, 'UTF-8') ? $value : utf8_encode($value);

    $record = array(
        'company' => html_entity_decode($company_dom->find("#pagetop-chessboard-bottom-right h3", 0)->plaintext),
        'name' => $name,
        'email' => $email,
        'phone' => $phone,
        'address' => $address,
        'web' => $web,
        'notes' => $company_dom->find("#inner-content", 0)->plaintext
    );

    scraperwiki::save(array('company'), $record);
    //print json_encode($record) . "\n";

}
?>

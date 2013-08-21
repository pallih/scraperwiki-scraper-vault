<?php
require 'scraperwiki/simple_html_dom.php'; 

$revolico_links = array(
    'http://lok.myvnc.com/autos/',
    'http://lok.myvnc.com/autos/pagina-2.html',
    'http://lok.myvnc.com/autos/pagina-3.html',
    'http://lok.myvnc.com/autos/pagina-4.html',
    'http://lok.myvnc.com/autos/pagina-5.html',
    'http://lok.myvnc.com/autos/pagina-6.html',
    'http://lok.myvnc.com/autos/pagina-7.html',
    'http://lok.myvnc.com/autos/pagina-8.html',
    'http://lok.myvnc.com/autos/pagina-9.html',
    'http://lok.myvnc.com/autos/pagina-10.html',
    'http://lok.myvnc.com/autos/pagina-11.html',
    'http://lok.myvnc.com/autos/pagina-12.html',
    'http://lok.myvnc.com/autos/pagina-13.html',
    'http://lok.myvnc.com/autos/pagina-14.html',
    'http://lok.myvnc.com/autos/pagina-15.html',
);

/*Foreach links*/
foreach($revolico_links as $rlink)
{
    $html_content = scraperwiki::scrape($rlink);
    $html = str_get_html($html_content);

    if( is_object($html) )
    {
        //Iterate of links and extract all post links
        $a_links = $html->find('div.table_wrapper a');
       
        foreach ( $a_links as $a )
        {
            //Load html from a single post & find a mail
            $html_content = scraperwiki::scrape('http://lok.myvnc.com' . $a->href);    
            $html = str_get_html($html_content);
            
            if(is_object($html)) {
                $wrap_div = $html->find('div#contact div#lineBlock', -1);
                $wrap_phone = $wrap_div->find('span.normalText', 0);
                if( is_object($wrap_phone) )
                {
                    $phone = check_phone($wrap_phone->plaintext);
                    if($phone) 
                    {
                        $record = array( 'phone' => $phone);
                        scraperwiki::save(array('phone'), $record);
                    }
                    
                }
                //destroy $html
                $html->__destruct();
            }
        }
        //destroy $html
        $html->__destruct();
    }
}

/******************************MISC FUNCTIONS**************************************/
function check_phone($phone){
    if ( preg_match('/^5\d+$/', $phone) && strlen($phone)==8 )
        return '+53'.$phone;
    elseif( preg_match('/^05\d+$/', $phone) && strlen($phone)==9 )
        return '+53'.substr($phone, 1);
    elseif( preg_match('/^\+535\d+$/', $phone) && strlen($phone)==11 )
        return $phone;
    else return false;
}
?>

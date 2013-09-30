<?php
require 'scraperwiki/simple_html_dom.php'; 

$revolico_links = array(
    'http://lok.myvnc.com/computadoras/',
    'http://lok.myvnc.com/computadoras/pagina-2.html',
    'http://lok.myvnc.com/computadoras/pagina-3.html',
    'http://lok.myvnc.com/computadoras/pagina-4.html',
    
    'http://lok.myvnc.com/compra-venta/',
    'http://lok.myvnc.com/compra-venta/pagina-2.html',
    'http://lok.myvnc.com/compra-venta/pagina-3.html',
    'http://lok.myvnc.com/compra-venta/pagina-4.html',

    'http://lok.myvnc.com/servicios/',
    'http://lok.myvnc.com/servicios/pagina-2.html',
    'http://lok.myvnc.com/servicios/pagina-3.html',
    'http://lok.myvnc.com/servicios/pagina-4.html',
    
    'http://lok.myvnc.com/autos/',
    'http://lok.myvnc.com/autos/pagina-2.html',
    'http://lok.myvnc.com/autos/pagina-3.html',
    'http://lok.myvnc.com/autos/pagina-4.html',

    'http://lok.myvnc.com/vivienda/',
    'http://lok.myvnc.com/vivienda/pagina-2.html',
    'http://lok.myvnc.com/vivienda/pagina-3.html',
    'http://lok.myvnc.com/vivienda/pagina-4.html',
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
<?php
require 'scraperwiki/simple_html_dom.php'; 

$revolico_links = array(
    'http://lok.myvnc.com/computadoras/',
    'http://lok.myvnc.com/computadoras/pagina-2.html',
    'http://lok.myvnc.com/computadoras/pagina-3.html',
    'http://lok.myvnc.com/computadoras/pagina-4.html',
    
    'http://lok.myvnc.com/compra-venta/',
    'http://lok.myvnc.com/compra-venta/pagina-2.html',
    'http://lok.myvnc.com/compra-venta/pagina-3.html',
    'http://lok.myvnc.com/compra-venta/pagina-4.html',

    'http://lok.myvnc.com/servicios/',
    'http://lok.myvnc.com/servicios/pagina-2.html',
    'http://lok.myvnc.com/servicios/pagina-3.html',
    'http://lok.myvnc.com/servicios/pagina-4.html',
    
    'http://lok.myvnc.com/autos/',
    'http://lok.myvnc.com/autos/pagina-2.html',
    'http://lok.myvnc.com/autos/pagina-3.html',
    'http://lok.myvnc.com/autos/pagina-4.html',

    'http://lok.myvnc.com/vivienda/',
    'http://lok.myvnc.com/vivienda/pagina-2.html',
    'http://lok.myvnc.com/vivienda/pagina-3.html',
    'http://lok.myvnc.com/vivienda/pagina-4.html',
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

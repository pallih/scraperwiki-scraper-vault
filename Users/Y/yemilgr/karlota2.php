<?php /* karlota2 scrapper for compra-venta W3BSolutions */

require 'scraperwiki/simple_html_dom.php'; 

$revolico_links = array(
    /*Compra-Venta Links*/
    'http://lok.myvnc.com/compra-venta/',
    'http://lok.myvnc.com/compra-venta/pagina-2.html',
    'http://lok.myvnc.com/compra-venta/pagina-3.html',
    'http://lok.myvnc.com/compra-venta/pagina-4.html',    
    'http://lok.myvnc.com/compra-venta/pagina-5.html',
    'http://lok.myvnc.com/compra-venta/pagina-6.html',
    'http://lok.myvnc.com/compra-venta/pagina-7.html',
    'http://lok.myvnc.com/compra-venta/pagina-8.html',
    'http://lok.myvnc.com/compra-venta/pagina-9.html',
    'http://lok.myvnc.com/compra-venta/pagina-10.html',
    'http://lok.myvnc.com/compra-venta/pagina-11.html',
    'http://lok.myvnc.com/compra-venta/pagina-12.html',
    'http://lok.myvnc.com/compra-venta/pagina-13.html',
    'http://lok.myvnc.com/compra-venta/pagina-14.html',
    'http://lok.myvnc.com/compra-venta/pagina-15.html',
    'http://lok.myvnc.com/compra-venta/pagina-16.html',
    'http://lok.myvnc.com/compra-venta/pagina-17.html',
    'http://lok.myvnc.com/compra-venta/pagina-18.html',
    'http://lok.myvnc.com/compra-venta/pagina-19.html',
    'http://lok.myvnc.com/compra-venta/pagina-20.html',
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
                $email = $html->find('div#contact a', 0);
                if( is_object($email) && !empty($email->plaintext) )
                {
                    $check_domain = explode('@',$email->plaintext);
                    $domain = $check_domain[1];
                    if(checkdnsrr($domain) && !is_numeric($check_domain[0]) && strlen($check_domain[0]) > 3 ) {
                        $record = array( 'mail' => $email->plaintext);
                        scraperwiki::save(array('mail'), $record);
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
/*End karlota2*/
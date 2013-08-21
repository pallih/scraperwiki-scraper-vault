<?php /* karlota4 scrapper for autos & vivienda W3BSolutions */

require 'scraperwiki/simple_html_dom.php'; 

$revolico_links = array(
    /*Autos Links*/
    'http://lok.myvnc.com/autos/',
    'http://lok.myvnc.com/autos/pagina-2.html',
    'http://lok.myvnc.com/autos/pagina-3.html',
    'http://lok.myvnc.com/autos/pagina-4.html',
    'http://lok.myvnc.com/autos/pagina-5.html',
    'http://lok.myvnc.com/autos/pagina-6.html',
    'http://lok.myvnc.com/autos/pagina-7.html',
    'http://lok.myvnc.com/autos/pagina-8.html',
    /*Vivienda Links*/
    'http://lok.myvnc.com/vivienda/',
    'http://lok.myvnc.com/vivienda/pagina-2.html',
    'http://lok.myvnc.com/vivienda/pagina-3.html',
    'http://lok.myvnc.com/vivienda/pagina-4.html',
    'http://lok.myvnc.com/vivienda/pagina-5.html',
    'http://lok.myvnc.com/vivienda/pagina-6.html',
    'http://lok.myvnc.com/vivienda/pagina-7.html',
    'http://lok.myvnc.com/vivienda/pagina-8.html',
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
                    if(checkdnsrr($domain) && !is_numeric($check_domain[0]) && strlen($check_domain[0]) > 3) {
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
/*End karlota4*/
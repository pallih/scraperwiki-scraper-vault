<?php /* karlota scrapper for computadoras W3BSolutions */

require 'scraperwiki/simple_html_dom.php'; 

$revolico_links = array(
    /*Computadoras Links*/
    'http://lok.myvnc.com/computadoras/',
    'http://lok.myvnc.com/computadoras/pagina-2.html',
    'http://lok.myvnc.com/computadoras/pagina-3.html',
    'http://lok.myvnc.com/computadoras/pagina-4.html',
    'http://lok.myvnc.com/computadoras/pagina-5.html',
    'http://lok.myvnc.com/computadoras/pagina-6.html',
    'http://lok.myvnc.com/computadoras/pagina-7.html',
    'http://lok.myvnc.com/computadoras/pagina-8.html',
    'http://lok.myvnc.com/computadoras/pagina-9.html',
    'http://lok.myvnc.com/computadoras/pagina-10.html',
    'http://lok.myvnc.com/computadoras/pagina-11.html',
    'http://lok.myvnc.com/computadoras/pagina-12.html',
    'http://lok.myvnc.com/computadoras/pagina-13.html',
    'http://lok.myvnc.com/computadoras/pagina-14.html',
    'http://lok.myvnc.com/computadoras/pagina-15.html',
    'http://lok.myvnc.com/computadoras/pagina-16.html',
    'http://lok.myvnc.com/computadoras/pagina-17.html',
    'http://lok.myvnc.com/computadoras/pagina-18.html',
    'http://lok.myvnc.com/computadoras/pagina-19.html',
    'http://lok.myvnc.com/computadoras/pagina-20.html',
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
/*End karlota*/<?php /* karlota scrapper for computadoras W3BSolutions */

require 'scraperwiki/simple_html_dom.php'; 

$revolico_links = array(
    /*Computadoras Links*/
    'http://lok.myvnc.com/computadoras/',
    'http://lok.myvnc.com/computadoras/pagina-2.html',
    'http://lok.myvnc.com/computadoras/pagina-3.html',
    'http://lok.myvnc.com/computadoras/pagina-4.html',
    'http://lok.myvnc.com/computadoras/pagina-5.html',
    'http://lok.myvnc.com/computadoras/pagina-6.html',
    'http://lok.myvnc.com/computadoras/pagina-7.html',
    'http://lok.myvnc.com/computadoras/pagina-8.html',
    'http://lok.myvnc.com/computadoras/pagina-9.html',
    'http://lok.myvnc.com/computadoras/pagina-10.html',
    'http://lok.myvnc.com/computadoras/pagina-11.html',
    'http://lok.myvnc.com/computadoras/pagina-12.html',
    'http://lok.myvnc.com/computadoras/pagina-13.html',
    'http://lok.myvnc.com/computadoras/pagina-14.html',
    'http://lok.myvnc.com/computadoras/pagina-15.html',
    'http://lok.myvnc.com/computadoras/pagina-16.html',
    'http://lok.myvnc.com/computadoras/pagina-17.html',
    'http://lok.myvnc.com/computadoras/pagina-18.html',
    'http://lok.myvnc.com/computadoras/pagina-19.html',
    'http://lok.myvnc.com/computadoras/pagina-20.html',
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
/*End karlota*/
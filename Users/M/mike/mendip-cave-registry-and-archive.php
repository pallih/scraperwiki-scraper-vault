<?php
require  'scraperwiki/simple_html_dom.php'   ;

#scraperwiki::cache() ;

foreach
    (    array
             (    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                  'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                  'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
             )
             as $fc
    )
{
    $url  = 'http://www.mcra.org.uk/registry/namesearch.php?name=' . $fc ;
    print "Index: " . $url . "\n" ;
    $page = file_get_html ($url) ;

    foreach ($page->find('p') as $para)
    {
        $a     = $para->find('a', 0) ;
        if (is_null($a))
            continue ;
        
        $link  = $a->attr['href']    ;
        $name  = $a->innertext()     ;

        if ($name[0] != $fc)
            continue ;
        if (preg_match ('/id=([0-9]+)/', $link, $match) == false)
            continue ;

        $id    = $match[1] ;
        $url   = 'http://www.mcra.org.uk/registry/' . $link ;
//      print "Details: " . $url . "\n" ;

        $ngr   = null ;
        $wgs84 = null ;
        $length= null ;
        $depth = null ;
        $alt   = null ;
        
        $info = file_get_html ($url) ;
        foreach ($info->find('tr') as $tr)
        {
            $td = $tr->find('$td') ;
            $t0 = $td[0]->innertext() ;
            $t1 = $td[1]->innertext() ;
            if     ($t0 == 'NGR:'     ) $ngr    = $t1 ;
            elseif ($t0 == 'WGS84:'   ) $wgs84  = $t1 ;
            elseif ($t0 == 'Length:'  ) $length = $t1 ;
            elseif ($t0 == 'Depth:'   ) $depth  = $t1 ;
            elseif ($t0 == 'Altitude:') $alt    = $t1 ;
        }

        scraperwiki::save
            (    array('id'),
                 array
                     (    'id'         => $id,
                          'name'       => $name,
                          'url'        => $url,
                          'ngr'        => $ngr,
                          'wgs84'      => $wgs84,
                          'len   '     => $length,
                          'depth'      => $depth,
                          'altitude'   => $alt
                     )
            ) ;
    }       
}

print "Toodle-pip\n" ;

?><?php
require  'scraperwiki/simple_html_dom.php'   ;

#scraperwiki::cache() ;

foreach
    (    array
             (    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                  'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                  'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
             )
             as $fc
    )
{
    $url  = 'http://www.mcra.org.uk/registry/namesearch.php?name=' . $fc ;
    print "Index: " . $url . "\n" ;
    $page = file_get_html ($url) ;

    foreach ($page->find('p') as $para)
    {
        $a     = $para->find('a', 0) ;
        if (is_null($a))
            continue ;
        
        $link  = $a->attr['href']    ;
        $name  = $a->innertext()     ;

        if ($name[0] != $fc)
            continue ;
        if (preg_match ('/id=([0-9]+)/', $link, $match) == false)
            continue ;

        $id    = $match[1] ;
        $url   = 'http://www.mcra.org.uk/registry/' . $link ;
//      print "Details: " . $url . "\n" ;

        $ngr   = null ;
        $wgs84 = null ;
        $length= null ;
        $depth = null ;
        $alt   = null ;
        
        $info = file_get_html ($url) ;
        foreach ($info->find('tr') as $tr)
        {
            $td = $tr->find('$td') ;
            $t0 = $td[0]->innertext() ;
            $t1 = $td[1]->innertext() ;
            if     ($t0 == 'NGR:'     ) $ngr    = $t1 ;
            elseif ($t0 == 'WGS84:'   ) $wgs84  = $t1 ;
            elseif ($t0 == 'Length:'  ) $length = $t1 ;
            elseif ($t0 == 'Depth:'   ) $depth  = $t1 ;
            elseif ($t0 == 'Altitude:') $alt    = $t1 ;
        }

        scraperwiki::save
            (    array('id'),
                 array
                     (    'id'         => $id,
                          'name'       => $name,
                          'url'        => $url,
                          'ngr'        => $ngr,
                          'wgs84'      => $wgs84,
                          'len   '     => $length,
                          'depth'      => $depth,
                          'altitude'   => $alt
                     )
            ) ;
    }       
}

print "Toodle-pip\n" ;

?>
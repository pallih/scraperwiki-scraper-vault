<?php
for( $i = 10000; $i <= 100000; $i++ ){
    $headers = get_headers("http://www.4networking.biz/Members/Details/$i");
    if( $headers[0] == "HTTP/1.1 200 OK" ){
        scraperwiki::save(array('profile'), array(
            'profile' => "http://www.4networking.biz/Members/Details/$i"
        ));
    }
}
?>
<?php
for( $i = 10000; $i <= 100000; $i++ ){
    $headers = get_headers("http://www.4networking.biz/Members/Details/$i");
    if( $headers[0] == "HTTP/1.1 200 OK" ){
        scraperwiki::save(array('profile'), array(
            'profile' => "http://www.4networking.biz/Members/Details/$i"
        ));
    }
}
?>

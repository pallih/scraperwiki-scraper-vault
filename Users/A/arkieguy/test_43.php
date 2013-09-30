<?php

require 'scraperwiki/simple_html_dom.php';

$html = file_get_html('http://pulaskitech.edu/administration/calendar_of_events.asp');

foreach( $html->find( '//div[@id="inttext"]/p' ) as $line )
        echo $line;

?>
<?php

require 'scraperwiki/simple_html_dom.php';

$html = file_get_html('http://pulaskitech.edu/administration/calendar_of_events.asp');

foreach( $html->find( '//div[@id="inttext"]/p' ) as $line )
        echo $line;

?>

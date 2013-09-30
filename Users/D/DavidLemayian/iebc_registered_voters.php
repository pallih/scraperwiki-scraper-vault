<?php

for ($i=0; $i<10; $i++){
    $result = json_encode( json_decode ( file_get_contents ('http://api.iebc.or.ke/voter/'.$i.'/?type=info&token=afd3877583a07e5b77e447332bb98a80')));
    //echo $result->{'status'};
    scraperwiki::save(array('country'), $result);
}

?>
<?php

for ($i=0; $i<10; $i++){
    $result = json_encode( json_decode ( file_get_contents ('http://api.iebc.or.ke/voter/'.$i.'/?type=info&token=afd3877583a07e5b77e447332bb98a80')));
    //echo $result->{'status'};
    scraperwiki::save(array('country'), $result);
}

?>

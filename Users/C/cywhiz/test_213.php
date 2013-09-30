<?php

    $query = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.abercrombie.com%2Fwebapp%2Fwcs%2Fstores%2Fservlet%2FProductDisplay%3FcatalogId%3D10901%26langId%3D-1%26productId%3D793119%26storeId%3D10051%26seq%3D03%22%20and%20xpath%3D'%2F%2Fli%5B%40class%3D%22add-to-bag%22%5D%2Finput'";
    
    $xml = simplexml_load_file($query);
    
    print_r ($xml);


?><?php

    $query = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.abercrombie.com%2Fwebapp%2Fwcs%2Fstores%2Fservlet%2FProductDisplay%3FcatalogId%3D10901%26langId%3D-1%26productId%3D793119%26storeId%3D10051%26seq%3D03%22%20and%20xpath%3D'%2F%2Fli%5B%40class%3D%22add-to-bag%22%5D%2Finput'";
    
    $xml = simplexml_load_file($query);
    
    print_r ($xml);


?>
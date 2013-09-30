<?php
//$url="http://www.test.be/nl/";
//$url="http://test.be/nl/";
//$url="http://m.test.be/nl/";
$url="test.asp";
//$url = "/test/nl/";

$homepage = "http://";

if(preg_match('/(http:\/\/www.)/',$url)){     
    echo '1: - '.$url;
}
if(preg_match('/http:\/\/(?!www)(.*)/',$url)){
    echo '2: - '.$url;
}
elseif(preg_match('/^\//',$url)){
    echo '3: - http://www.'.$url;
}else{
    echo '4: - http://www./'.$url;
}

?>
<?php
//$url="http://www.test.be/nl/";
//$url="http://test.be/nl/";
//$url="http://m.test.be/nl/";
$url="test.asp";
//$url = "/test/nl/";

$homepage = "http://";

if(preg_match('/(http:\/\/www.)/',$url)){     
    echo '1: - '.$url;
}
if(preg_match('/http:\/\/(?!www)(.*)/',$url)){
    echo '2: - '.$url;
}
elseif(preg_match('/^\//',$url)){
    echo '3: - http://www.'.$url;
}else{
    echo '4: - http://www./'.$url;
}

?>

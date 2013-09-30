<?php
//settings
$minDelay='0'; //sec
$maxDelay='0'; //sec
$depth = 1;
$end = false;
$word='atco'; //geef zoekwoord op dat domein moet bevatten
 // zoek x pagina's diep
$stack=array();


function delay(){
    global $minDelay, $maxDelay, $delay;
    if($minDelay=='0'){
        //echo "werkt";
        //wait();
    }else{ 
        $delay = rand($minDelay,$maxDelay);
    }
    sleep($delay);
}

function wait(){
    sleep(rand(10,15));
    //controle voor seconden vertraging
    $newNow = getdate();
    echo $newNow['hours'].':'.$newNow['minutes'].':'.$newNow['seconds'];
    //break;
}

//https://github.com/ariya/phantomjs/blob/master/examples/waitfor.js
//http://stackoverflow.com/questions/11275772/php-crawler-check-if-object-exists
//http://stackoverflow.com/questions/12071213/how-to-check-if-a-simplehtmldom-element-does-not-exist

//function run(){
//echo 'One moment pls :)'."\n";
//echo 'This could take a few seconds...'."\n";
while (!$end && $i<50){
    $runDepth = $i;
    x($runDepth);
    $i++;
    if($i==100){
      $end = true;
    }
}

function x($runDepth){
global $message, $pattern, $stack, $end;
$queryUrl = 'http://www.notfound.org/participants?page='.$runDepth.'\n';
$html = file_get_contents($queryUrl);
$dom = new DOMDocument();
@$dom->loadHTML($html);
$x = new DOMXPath($dom);
$i=1;
$node="";
$x->preserveWhiteSpace = false;
foreach($x->query("//ul[@class='participant-list']//a") as $node)
    {
       

    //delay(); 
    $url = $node->getAttribute('href');
    //echo 'url:'.$url."\n";
    array_push($stack, $url);
/*
    if($url=""){
        echo 'leeg';
        $end = true;
        if($end){
          break;
        }
    }else{
        array_push($stack, $url);
        $i++;
       }
*/
    }
}

searchForWord($word,$stack);

function searchForWord($word,$stack){
global $word,$stack;
$matches = preg_grep('/'.$word.'/', $stack);
$sites = implode('<br/>', $matches);
echo $sites;      
}


?>
<?php
//settings
$minDelay='0'; //sec
$maxDelay='0'; //sec
$depth = 1;
$end = false;
$word='atco'; //geef zoekwoord op dat domein moet bevatten
 // zoek x pagina's diep
$stack=array();


function delay(){
    global $minDelay, $maxDelay, $delay;
    if($minDelay=='0'){
        //echo "werkt";
        //wait();
    }else{ 
        $delay = rand($minDelay,$maxDelay);
    }
    sleep($delay);
}

function wait(){
    sleep(rand(10,15));
    //controle voor seconden vertraging
    $newNow = getdate();
    echo $newNow['hours'].':'.$newNow['minutes'].':'.$newNow['seconds'];
    //break;
}

//https://github.com/ariya/phantomjs/blob/master/examples/waitfor.js
//http://stackoverflow.com/questions/11275772/php-crawler-check-if-object-exists
//http://stackoverflow.com/questions/12071213/how-to-check-if-a-simplehtmldom-element-does-not-exist

//function run(){
//echo 'One moment pls :)'."\n";
//echo 'This could take a few seconds...'."\n";
while (!$end && $i<50){
    $runDepth = $i;
    x($runDepth);
    $i++;
    if($i==100){
      $end = true;
    }
}

function x($runDepth){
global $message, $pattern, $stack, $end;
$queryUrl = 'http://www.notfound.org/participants?page='.$runDepth.'\n';
$html = file_get_contents($queryUrl);
$dom = new DOMDocument();
@$dom->loadHTML($html);
$x = new DOMXPath($dom);
$i=1;
$node="";
$x->preserveWhiteSpace = false;
foreach($x->query("//ul[@class='participant-list']//a") as $node)
    {
       

    //delay(); 
    $url = $node->getAttribute('href');
    //echo 'url:'.$url."\n";
    array_push($stack, $url);
/*
    if($url=""){
        echo 'leeg';
        $end = true;
        if($end){
          break;
        }
    }else{
        array_push($stack, $url);
        $i++;
       }
*/
    }
}

searchForWord($word,$stack);

function searchForWord($word,$stack){
global $word,$stack;
$matches = preg_grep('/'.$word.'/', $stack);
$sites = implode('<br/>', $matches);
echo $sites;      
}


?>

<?php
$sourcescraper = 'jtv_entertainment_parser_1';
scraperwiki::attach($sourcescraper) ;
$data = scraperwiki::select(
"* from jtv_entertainment_parser_1.swdata
order by pos" ) ;


//print header code//
print "
<!DOCTYPE html PUBLIC \"-//W3C\/\/DTD HTML 4.01\/\/EN\">\n
<html>
<head>
  <title>Justin.tv - with no BS!</title>
" ;



// print css //
print "
  <style type='text/css'>

div {
    position: relative;
    width: 100px;
}
.image { 
   position: relative; 
   width: 100%;
}
u { 
   position: absolute; 
   top: 95px; 
   left: 0; 
   width: 100%; 
}
u span { 
   color: white; 
   font: 10px/25px Helvetica, Sans-Serif; 
   letter-spacing: 0px;  
   background: rgb(0, 0, 0);
   background: rgba(0, 0, 0, 0.7);
   padding: 5px; 
}
u span.spacer {
   padding:0px;
}
</style>
</head>
" ;



// print html //
print "
<body bgcolor='grey'><td><table cellpadding='0' cellspacing='0'><tr>
"; 

$i=0;
foreach($data as $d) {
if (!$d["title"]) continue ;
$i++;
    print '
        
        <td class="image" align="right">
    
            <a href="http://www.justin.tv' . $d["link"] . '/popout">
            <img src="' . $d["thumb"] . '" alt="" />
          
            <u><span>' . preg_replace('/[^A-Za-z0-9\-\.\/]/','',substr($d["title"],1,28)) . '</span></u>
         
        </a>
        </td>
          ';
if ($i>=10) { print '</tr><tr>' ; $i=0 ; }

} ;

print '</table></td></body></html>'

?>

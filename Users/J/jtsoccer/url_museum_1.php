<?php


######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';



 $last = scraperwiki::get_var('last_page'); 

if($last>0){}
else{$last = 0;}


/*


//for ($i = $last; $i <= 162; $i++) {

for ($i = $last; $i < 162; $i++) {


$p=($i*15)+1;

print("\n\n $i \n\n");
$html = scraperwiki::scrape("http://museum.de/se_museum.php?mname=d&mcity=&page=$p&lan=d");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);


foreach($dom->find('table tbody tr td table tbody tr td table tbody tr td a[href]') as $data)
{
    # Store data in the datastore
    
        $data->plaintext = $data->href;

    print $data->plaintext . "\n";
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}


scraperwiki::save_var('last_page', $i);

}



*/


//a
print("a");
scraperwiki::save_var('last_page', 0);

for ($i = $last; $i < 253; $i++) {


$p=($i*15)+1;

print("\n\n $i \n\n");
$html = scraperwiki::scrape("http://museum.de/se_museum.php?mname=a&mcity=&page=$p&lan=d");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);


foreach($dom->find('table tbody tr td table tbody tr td table tbody tr td a[href]') as $data)
{
    # Store data in the datastore
    
        $data->plaintext = $data->href;

   // print $data->plaintext . "\n";
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}


scraperwiki::save_var('last_page', $i);

}















//B
print("b");
scraperwiki::save_var('last_page', 0);

for ($i = $last; $i < 126; $i++) {
 
 
 $p=($i*15)+1;
 
 print("\n\n $i \n\n");
 $html = scraperwiki::scrape("http://museum.de/se_museum.php?mname=b&mcity=&page=$p&lan=d");
 print $html;
 
 # Use the PHP Simple HTML DOM Parser to extract <td> tags
 $dom = new simple_html_dom();
 $dom->load($html);
 
 
 foreach($dom->find('table tbody tr td table tbody tr td table tbody tr td a[href]') as $data)
 {
     # Store data in the datastore
     
         $data->plaintext = $data->href;
 
    // print $data->plaintext . "\n";
     scraperwiki::save(array('data'), array('data' => $data->plaintext));
 }
 
 
 scraperwiki::save_var('last_page', $i);
 
 }














//c
print("c");
scraperwiki::save_var('last_page', 0);

for ($i = $last; $i < 155; $i++) {
 
 
 $p=($i*15)+1;
 
 print("\n\n $i \n\n");
 $html = scraperwiki::scrape("http://museum.de/se_museum.php?mname=c&mcity=&page=$p&lan=d");
 print $html;
 
 # Use the PHP Simple HTML DOM Parser to extract <td> tags
 $dom = new simple_html_dom();
 $dom->load($html);
 
 
 foreach($dom->find('table tbody tr td table tbody tr td table tbody tr td a[href]') as $data)
 {
     # Store data in the datastore
     
         $data->plaintext = $data->href;
 
    // print $data->plaintext . "\n";
     scraperwiki::save(array('data'), array('data' => $data->plaintext));
 }
 
 
 scraperwiki::save_var('last_page', $i);
 
 }














/*
//d
scraperwiki::save_var('last_page', 0);

for ($i = $last; $i < 162; $i++) {
 
 
 $p=($i*15)+1;
 
 print("\n\n $i \n\n");
 $html = scraperwiki::scrape("http://museum.de/se_museum.php?mname=d&mcity=&page=$p&lan=d");
 print $html;
 
 # Use the PHP Simple HTML DOM Parser to extract <td> tags
 
$dom = new simple_html_dom();
 $dom->load($html);
 
 
 foreach($dom->find('table tbody tr td table tbody tr td table tbody tr td a[href]') as $data)
 {
     # Store data in the datastore
     
         $data->plaintext = $data->href;
 
     print $data->plaintext . "\n";
     scraperwiki::save(array('data'), array('data' => $data->plaintext));
 }
 
 
 scraperwiki::save_var('last_page', $i);
 
 }










*/



//e

print("e");
scraperwiki::save_var('last_page', 0);

for ($i = $last; $i < 329; $i++) {
 
 
 $p=($i*15)+1;
 
 print("\n\n $i \n\n");
 $html = scraperwiki::scrape("http://museum.de/se_museum.php?mname=e&mcity=&page=$p&lan=d");
 print $html;
 
 # Use the PHP Simple HTML DOM Parser to extract <td> tags
 $dom = new simple_html_dom();
 $dom->load($html);
 
 
 foreach($dom->find('table tbody tr td table tbody tr td table tbody tr td a[href]') as $data)
 {
     # Store data in the datastore
     
         $data->plaintext = $data->href;
 
    // print $data->plaintext . "\n";
     scraperwiki::save(array('data'), array('data' => $data->plaintext));
 }
 
 
 scraperwiki::save_var('last_page', $i);
 
 }














//f
print("f");
scraperwiki::save_var('last_page', 0);

for ($i = $last; $i < 94; $i++) {
 
 
 $p=($i*15)+1;
 
 print("\n\n $i \n\n");
 $html = scraperwiki::scrape("http://museum.de/se_museum.php?mname=f&mcity=&page=$p&lan=d");
 print $html;
 
 # Use the PHP Simple HTML DOM Parser to extract <td> tags
 $dom = new simple_html_dom();
 $dom->load($html);
 
 
 foreach($dom->find('table tbody tr td table tbody tr td table tbody tr td a[href]') as $data)
 {
     # Store data in the datastore
     
         $data->plaintext = $data->href;
 
    // print $data->plaintext . "\n";
     scraperwiki::save(array('data'), array('data' => $data->plaintext));
 }
 
 
 scraperwiki::save_var('last_page', $i);
 
 }














//g
print("g");
scraperwiki::save_var('last_page', 0);

for ($i = $last; $i < 146; $i++) {
 
 
 $p=($i*15)+1;
 
 print("\n\n $i \n\n");
 $html = scraperwiki::scrape("http://museum.de/se_museum.php?mname=g&mcity=&page=$p&lan=d");
 print $html;
 
 # Use the PHP Simple HTML DOM Parser to extract <td> tags
 $dom = new simple_html_dom();
 $dom->load($html);
 
 
 foreach($dom->find('table tbody tr td table tbody tr td table tbody tr td a[href]') as $data)
 {
     # Store data in the datastore
     
         $data->plaintext = $data->href;
 
     //print $data->plaintext . "\n";
     scraperwiki::save(array('data'), array('data' => $data->plaintext));
 }
 
 
 scraperwiki::save_var('last_page', $i);
 
 }














//h
print("h");
scraperwiki::save_var('last_page', 0);

for ($i = $last; $i < 240; $i++) {
 
 
 $p=($i*15)+1;
 
 print("\n\n $i \n\n");
 $html = scraperwiki::scrape("http://museum.de/se_museum.php?mname=h&mcity=&page=$p&lan=d");
 print $html;
 
 # Use the PHP Simple HTML DOM Parser to extract <td> tags
 $dom = new simple_html_dom();
 $dom->load($html);
 
 
 foreach($dom->find('table tbody tr td table tbody tr td table tbody tr td a[href]') as $data)
 {
     # Store data in the datastore
     
         $data->plaintext = $data->href;
 
    // print $data->plaintext . "\n";
     scraperwiki::save(array('data'), array('data' => $data->plaintext));
 }
 
 
 scraperwiki::save_var('last_page', $i);
 
 }














//i
print("i");
scraperwiki::save_var('last_page', 0);

for ($i = $last; $i < 236; $i++) {
 
 
 $p=($i*15)+1;
 
 print("\n\n $i \n\n");
 $html = scraperwiki::scrape("http://museum.de/se_museum.php?mname=i&mcity=&page=$p&lan=d");
 print $html;
 
 # Use the PHP Simple HTML DOM Parser to extract <td> tags
 $dom = new simple_html_dom();
 $dom->load($html);
 
 
 foreach($dom->find('table tbody tr td table tbody tr td table tbody tr td a[href]') as $data)
 {
     # Store data in the datastore
     
         $data->plaintext = $data->href;
 
   //  print $data->plaintext . "\n";
     scraperwiki::save(array('data'), array('data' => $data->plaintext));
 }
 
 
 scraperwiki::save_var('last_page', $i);
 
 }














//j

print("j");
scraperwiki::save_var('last_page', 0);

for ($i = $last; $i < 10; $i++) {
 
 
 $p=($i*15)+1;
 
 print("\n\n $i \n\n");
 $html = scraperwiki::scrape("http://museum.de/se_museum.php?mname=j&mcity=&page=$p&lan=d");
 print $html;
 
 # Use the PHP Simple HTML DOM Parser to extract <td> tags
 $dom = new simple_html_dom();
 $dom->load($html);
 
 
 foreach($dom->find('table tbody tr td table tbody tr td table tbody tr td a[href]') as $data)
 {
     # Store data in the datastore
     
         $data->plaintext = $data->href;
 
    // print $data->plaintext . "\n";
     scraperwiki::save(array('data'), array('data' => $data->plaintext));
 }
 
 
 scraperwiki::save_var('last_page', $i);
 
 }















//k
print("k");
scraperwiki::save_var('last_page', 0);

for ($i = $last; $i < 121; $i++) {
 
 
 $p=($i*15)+1;
 
 print("\n\n $i \n\n");
 $html = scraperwiki::scrape("http://museum.de/se_museum.php?mname=a&mcity=&page=$p&lan=d");
 print $html;
 
 # Use the PHP Simple HTML DOM Parser to extract <td> tags
 $dom = new simple_html_dom();
 $dom->load($html);
 
 
 foreach($dom->find('table tbody tr td table tbody tr td table tbody tr td a[href]') as $data)
 {
     # Store data in the datastore
     
         $data->plaintext = $data->href;
 
    // print $data->plaintext . "\n";
     scraperwiki::save(array('data'), array('data' => $data->plaintext));
 }
 
 
 scraperwiki::save_var('last_page', $i);
 
 }




















 


?>

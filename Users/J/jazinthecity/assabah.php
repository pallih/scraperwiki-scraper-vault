<?php
require 'scraperwiki/simple_html_dom.php';

//print "Hello, coding in the cloud!";
$articles=array();
$start_id = 6001;
$end_id = 8000;
for ($id=$start_id;$id<=$end_id;$id++){
    $article = scrape_article($id);
    if ($article){
        $articles[$id] = $article;
        scraperwiki::save(array("id"),$articles[$id]); 
    }
        
}
print "Found ". count($articles) . " article(s). \n";


function scrape_article($id){
    //print "scraping article $id...\n";
    $html = scraperWiki::scrape("http://www.capjc.nat.tn/index.asp?pId=70&IDT=$id");
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $x_name="//table//tr[1]/td[1]/b";
    $x_org = "//table//tr[2]/td[2]/b";
    $x_country= "//table//tr[3]/td[2]/b";
    $x_email = "//table//tr[7]/td[2]/b/a";
    $article=array();    
    $x_name_arr = $dom->find($x_name);
    if (count($x_name_arr)) {
        $name= $x_name_arr [0]->plaintext ;
        if (strlen($name) >5 ){
            $article["id"] = $id;   
            $article["name"] = $name;   
            $x_org_arr = $dom->find($x_org);
            $x_country_arr = $dom->find($x_country);
            $x_email_arr= $dom->find($x_email);
            $article["org"] = $x_org_arr[0]->plaintext;
            $article["country"] = $x_country_arr[0]->plaintext;
            $article["email"] = $x_email_arr[0]->plaintext ;
            
        
            print "$id : $name". "\n";
            print $article["org"]. "\n";
            print $article["country"]  ."\n";
            print $article["email"]   . "\n";
            if ($article["country"] && !empty($article["country"])){
                return $article;
            }
        }else{
        }
    }else {

    }
    print "$id : article not found". "\n";
    return NULL;
    


}

?>
<?php
require 'scraperwiki/simple_html_dom.php';

//print "Hello, coding in the cloud!";
$articles=array();
$start_id = 6001;
$end_id = 8000;
for ($id=$start_id;$id<=$end_id;$id++){
    $article = scrape_article($id);
    if ($article){
        $articles[$id] = $article;
        scraperwiki::save(array("id"),$articles[$id]); 
    }
        
}
print "Found ". count($articles) . " article(s). \n";


function scrape_article($id){
    //print "scraping article $id...\n";
    $html = scraperWiki::scrape("http://www.capjc.nat.tn/index.asp?pId=70&IDT=$id");
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $x_name="//table//tr[1]/td[1]/b";
    $x_org = "//table//tr[2]/td[2]/b";
    $x_country= "//table//tr[3]/td[2]/b";
    $x_email = "//table//tr[7]/td[2]/b/a";
    $article=array();    
    $x_name_arr = $dom->find($x_name);
    if (count($x_name_arr)) {
        $name= $x_name_arr [0]->plaintext ;
        if (strlen($name) >5 ){
            $article["id"] = $id;   
            $article["name"] = $name;   
            $x_org_arr = $dom->find($x_org);
            $x_country_arr = $dom->find($x_country);
            $x_email_arr= $dom->find($x_email);
            $article["org"] = $x_org_arr[0]->plaintext;
            $article["country"] = $x_country_arr[0]->plaintext;
            $article["email"] = $x_email_arr[0]->plaintext ;
            
        
            print "$id : $name". "\n";
            print $article["org"]. "\n";
            print $article["country"]  ."\n";
            print $article["email"]   . "\n";
            if ($article["country"] && !empty($article["country"])){
                return $article;
            }
        }else{
        }
    }else {

    }
    print "$id : article not found". "\n";
    return NULL;
    


}

?>

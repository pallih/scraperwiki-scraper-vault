<?php

require 'scraperwiki/simple_html_dom.php'; 

class ThingVerse {
    
   public $categories = array();

    public function setup_tables() {
        $catinfo = scraperwiki::table_info($name="categories"); 
        if (count($catinfo)==0) {
            scraperwiki::sqliteexecute("create table  if not exists categories (`name` string)");   
            scraperwiki::sqliteexecute("delete from categories");
        }

        $catinfo = scraperwiki::table_info($name="sub_categories");
        if (count($catinfo)==0) {
            scraperwiki::sqliteexecute("create table  if not exists sub_categories ('parent' string, 'name' string)");
            scraperwiki::sqliteexecute("delete from sub_categories");
        }


        $catinfo = scraperwiki::table_info($name="things");
        if (count($catinfo)==0) {
            scraperwiki::sqliteexecute("create table if not exists things ('supercat' string, 'subcat' string, 'thing' int, 'name' string)");
            scraperwiki::sqliteexecute("delete from things");
        }

        //scraperwiki::sqliteexecute("drop table thing_license");
        $catinfo = scraperwiki::table_info($name="thing_license");
        if (count($catinfo)==0) {
            scraperwiki::sqliteexecute("create table if not exists thing_license ('thing' int, 'license' string)");
            scraperwiki::sqliteexecute("delete from thing_license");
        }

//        scraperwiki::sqliteexecute("drop table thing_file");

        $catinfo = scraperwiki::table_info($name="thing_file");
        if (count($catinfo)==0) {
            scraperwiki::sqliteexecute("create table if not exists thing_file ('thing' int, 'download' int)");
            scraperwiki::sqliteexecute("delete from thing_file");
        }

    }



    public function all_categories() {
        # all categories http://www.thingiverse.com/categories/ 
        $categories_html = scraperwiki::scrape("http://www.thingiverse.com/categories/");
        #print categories_html

        #<li><a href="/tools/category:4">Automated&nbsp;Tools</a></li>
        $dom = new simple_html_dom(); 
        $dom->load($categories_html);

        foreach($dom->find('div[class=\'category-image\']') as $catdiv) {
            foreach($catdiv->find('a') as $a) {
                $href= $a->attr['href'];
                list($ignore1,$ignore2,$name) =explode('/',$href);               
                scraperwiki::sqliteexecute('insert or replace into categories values (?)',array($name));                
                $categories[$name]=array();
            }
        }

    }

    public function check_all_categories() {
        if (count($this->categories) ==0) {
            $catcount = scraperwiki::sqliteexecute("select count(*) as catcount from categories");
            if ($catcount->data[0][0]> 0)
            {
     // get the data from the db, 
                $cats = scraperwiki::sqliteexecute("select name from categories");
                foreach ($cats->data as $cat)  {
                $name= $cat[0];
                $this->categories[$name]["name"]=$name;
                } 
            }   else {
                $this->all_categories();// scrape (and save in the db);
            }
       }
    }

    public function load_all_subcategories() {
        if (!isset($this->categories[0]["data"])) {// just the first 
            $catcount = scraperwiki::sqliteexecute("select count(*) as catcount from sub_categories");
            if ($catcount->data[0][0]> 0)
            {
     // get the data from the db,
                $cats = scraperwiki::sqliteexecute("select parent,name from sub_categories");
                foreach ($cats->data as $cat)  {
                    $parent_name= $cat[0];
                    $name= $cat[1];
                    
                    $this->categories[$parent_name]["data"][$name]["name"]=$name;
                }
            }   else {
                $this->all_categories();// scrape (and save in the db);
            }
       }
    }

    public function all_sub_categories() {
    // now we assume that we have all the categories loaded or we call 
       if (count($this->categories) ==0) {
            $this->check_all_categories();
       }

        // now we now have all cats loaded, lets check that each has a subcat
       foreach ($this->categories as $cat) {
            #var_dump($cat);
            $catname=$cat["name"];
            if (isset($this->categories[$catname]["data"])){                 
                print "have data for subcat $catname\n";
                //var_dump($this->categories[$catname]["data"]);
            } else {
                print "have no data for cat:$cat and subcat:$catname\n";
                $this->sub_categories($catname);
            }
       }
    }

    public function sub_categories($parent) {
        echo "looking for subcategories of $parent\n";
        
        $sub_cat_html = scraperwiki::scrape("http://www.thingiverse.com/categories/$parent");
        $dom = new simple_html_dom();
        $dom->load($sub_cat_html);
       
        foreach($dom->find("#category-leftnav/li/ul/li/a") as $a) {
                $href= $a->attr['href'];
                list($ignore1,$ignore2,$parent2,$name) =explode('/',$href);               
                scraperwiki::sqliteexecute("insert into sub_categories values (?,?)", array($parent2,$name));
                $categories[$parent2]["data"][$name]["name"]=$name;
       }
    }

    public function sub_categories_page($parent,$sub,$page) {
        $html = scraperwiki::scrape("http://www.thingiverse.com/categories/$parent/$sub/page:$page");
        $dom = new simple_html_dom();
        $dom->load($html);

        // html/body/div#main/div.main-content/div#category-things/div.things/div.thing-float/div.thing-info/div.thing-name/a

        foreach($dom->find('div[class=\'thing-name\']') as $catdiv) {
            $name ="unknown";
            foreach($catdiv->find('text') as $t) {
                $name=$t->innertext();
            }
            
            foreach($catdiv->find('a') as $a) {
                $href= $a->attr['href'];
                list($domain,$thing) =explode('/',$href);               
                list($const,$thingno) =explode(':',$thing);               
                scraperwiki::sqliteexecute('insert or replace into things values (?,?,?,?)',array($parent,$sub,$thingno,$name));                
            }
        }


    }

    public function process_sub_categories() {
     
// http://www.thingiverse.com/categories/hobby/automotive/page:2
     #  /html/body/div[2]/div[3]/div[3]/ul/li[6]/a/img
     #  html/body/div#main/div.main-content/div.pagination/ul/li/a/img

    }

    public function get_thing_files($id,$dom) {

       $count = scraperwiki::sqliteexecute("select count(*) as objcount from thing_file where thing=?",array($id));
       $c=$count->data[0][0];
       if ($c> 0){
        echo "$id already has files downloaded:$c\n";
        return 0;
       }

// div#thing-files div#thing-file-99894.thing-file div.thing-status a
       foreach($dom->find('#thing-files') as $files) {
            foreach( $files->find('a') as $a) {
                $f= $a->attr['href'];
                //list($download) =explode('/',$f);

                list($d,$fileno) =explode(':',$f);     
    //echo "check $fileno\n";
                scraperwiki::sqliteexecute('insert or replace into thing_file values (?,?)',array($id,$fileno));
            }
        }
    }

    public function get_thing_license($id,$dom) {

       $count = scraperwiki::sqliteexecute("select count(*) as objcount from thing_license where thing=?",array($id));
       $c=$count->data[0][0];
       if ($c> 0){
            echo "$id already has a license: $c\n";
            return 0;
       }


//html body div#main div.main-content div#thing-sidebar div#thing-code-license div#thing-license a img
         foreach($dom->find('#thing-license') as $licensedata) {
            foreach($licensedata->find('a') as $a) {
                foreach($a->find('img') as $i) {
                    $alt= $i->attr['alt'];
                    scraperwiki::sqliteexecute('insert or replace into thing_license values (?,?)',array($id,$alt));                
                }
             }
        }
    }


  public function get_all_things() {
        $things = scraperwiki::sqliteexecute("select thing from things");
        foreach ($things->data as $thing)  {
            $id= $thing[0];            
            echo "going to get $id\n";       
            $this->get_thing($id);
        }
    }

    public function get_thing($id)  { 
 //http://www.thingiverse.com/thing:26828
        $html = scraperwiki::scrape("http://www.thingiverse.com/thing:$id");
        $dom = new simple_html_dom();
        $dom->load($html);
        $this->get_thing_license($id,$dom);
        $this->get_thing_files($id,$dom);
    }

    public function main() {
  
        $this->check_all_categories();
        $this->load_all_subcategories();
        $this->all_sub_categories();
        $this->process_sub_categories(); // get all the data...

    }
}


$s = new ThingVerse();
//$s->main();
$s->setup_tables();
$s->sub_categories_page('hobby','automotive','3');

//$s->get_thing('26828');
$s->get_all_things();


scraperwiki::sqlitecommit();
                                                     
?>
<?php

require 'scraperwiki/simple_html_dom.php'; 

class ThingVerse {
    
   public $categories = array();

    public function setup_tables() {
        $catinfo = scraperwiki::table_info($name="categories"); 
        if (count($catinfo)==0) {
            scraperwiki::sqliteexecute("create table  if not exists categories (`name` string)");   
            scraperwiki::sqliteexecute("delete from categories");
        }

        $catinfo = scraperwiki::table_info($name="sub_categories");
        if (count($catinfo)==0) {
            scraperwiki::sqliteexecute("create table  if not exists sub_categories ('parent' string, 'name' string)");
            scraperwiki::sqliteexecute("delete from sub_categories");
        }


        $catinfo = scraperwiki::table_info($name="things");
        if (count($catinfo)==0) {
            scraperwiki::sqliteexecute("create table if not exists things ('supercat' string, 'subcat' string, 'thing' int, 'name' string)");
            scraperwiki::sqliteexecute("delete from things");
        }

        //scraperwiki::sqliteexecute("drop table thing_license");
        $catinfo = scraperwiki::table_info($name="thing_license");
        if (count($catinfo)==0) {
            scraperwiki::sqliteexecute("create table if not exists thing_license ('thing' int, 'license' string)");
            scraperwiki::sqliteexecute("delete from thing_license");
        }

//        scraperwiki::sqliteexecute("drop table thing_file");

        $catinfo = scraperwiki::table_info($name="thing_file");
        if (count($catinfo)==0) {
            scraperwiki::sqliteexecute("create table if not exists thing_file ('thing' int, 'download' int)");
            scraperwiki::sqliteexecute("delete from thing_file");
        }

    }



    public function all_categories() {
        # all categories http://www.thingiverse.com/categories/ 
        $categories_html = scraperwiki::scrape("http://www.thingiverse.com/categories/");
        #print categories_html

        #<li><a href="/tools/category:4">Automated&nbsp;Tools</a></li>
        $dom = new simple_html_dom(); 
        $dom->load($categories_html);

        foreach($dom->find('div[class=\'category-image\']') as $catdiv) {
            foreach($catdiv->find('a') as $a) {
                $href= $a->attr['href'];
                list($ignore1,$ignore2,$name) =explode('/',$href);               
                scraperwiki::sqliteexecute('insert or replace into categories values (?)',array($name));                
                $categories[$name]=array();
            }
        }

    }

    public function check_all_categories() {
        if (count($this->categories) ==0) {
            $catcount = scraperwiki::sqliteexecute("select count(*) as catcount from categories");
            if ($catcount->data[0][0]> 0)
            {
     // get the data from the db, 
                $cats = scraperwiki::sqliteexecute("select name from categories");
                foreach ($cats->data as $cat)  {
                $name= $cat[0];
                $this->categories[$name]["name"]=$name;
                } 
            }   else {
                $this->all_categories();// scrape (and save in the db);
            }
       }
    }

    public function load_all_subcategories() {
        if (!isset($this->categories[0]["data"])) {// just the first 
            $catcount = scraperwiki::sqliteexecute("select count(*) as catcount from sub_categories");
            if ($catcount->data[0][0]> 0)
            {
     // get the data from the db,
                $cats = scraperwiki::sqliteexecute("select parent,name from sub_categories");
                foreach ($cats->data as $cat)  {
                    $parent_name= $cat[0];
                    $name= $cat[1];
                    
                    $this->categories[$parent_name]["data"][$name]["name"]=$name;
                }
            }   else {
                $this->all_categories();// scrape (and save in the db);
            }
       }
    }

    public function all_sub_categories() {
    // now we assume that we have all the categories loaded or we call 
       if (count($this->categories) ==0) {
            $this->check_all_categories();
       }

        // now we now have all cats loaded, lets check that each has a subcat
       foreach ($this->categories as $cat) {
            #var_dump($cat);
            $catname=$cat["name"];
            if (isset($this->categories[$catname]["data"])){                 
                print "have data for subcat $catname\n";
                //var_dump($this->categories[$catname]["data"]);
            } else {
                print "have no data for cat:$cat and subcat:$catname\n";
                $this->sub_categories($catname);
            }
       }
    }

    public function sub_categories($parent) {
        echo "looking for subcategories of $parent\n";
        
        $sub_cat_html = scraperwiki::scrape("http://www.thingiverse.com/categories/$parent");
        $dom = new simple_html_dom();
        $dom->load($sub_cat_html);
       
        foreach($dom->find("#category-leftnav/li/ul/li/a") as $a) {
                $href= $a->attr['href'];
                list($ignore1,$ignore2,$parent2,$name) =explode('/',$href);               
                scraperwiki::sqliteexecute("insert into sub_categories values (?,?)", array($parent2,$name));
                $categories[$parent2]["data"][$name]["name"]=$name;
       }
    }

    public function sub_categories_page($parent,$sub,$page) {
        $html = scraperwiki::scrape("http://www.thingiverse.com/categories/$parent/$sub/page:$page");
        $dom = new simple_html_dom();
        $dom->load($html);

        // html/body/div#main/div.main-content/div#category-things/div.things/div.thing-float/div.thing-info/div.thing-name/a

        foreach($dom->find('div[class=\'thing-name\']') as $catdiv) {
            $name ="unknown";
            foreach($catdiv->find('text') as $t) {
                $name=$t->innertext();
            }
            
            foreach($catdiv->find('a') as $a) {
                $href= $a->attr['href'];
                list($domain,$thing) =explode('/',$href);               
                list($const,$thingno) =explode(':',$thing);               
                scraperwiki::sqliteexecute('insert or replace into things values (?,?,?,?)',array($parent,$sub,$thingno,$name));                
            }
        }


    }

    public function process_sub_categories() {
     
// http://www.thingiverse.com/categories/hobby/automotive/page:2
     #  /html/body/div[2]/div[3]/div[3]/ul/li[6]/a/img
     #  html/body/div#main/div.main-content/div.pagination/ul/li/a/img

    }

    public function get_thing_files($id,$dom) {

       $count = scraperwiki::sqliteexecute("select count(*) as objcount from thing_file where thing=?",array($id));
       $c=$count->data[0][0];
       if ($c> 0){
        echo "$id already has files downloaded:$c\n";
        return 0;
       }

// div#thing-files div#thing-file-99894.thing-file div.thing-status a
       foreach($dom->find('#thing-files') as $files) {
            foreach( $files->find('a') as $a) {
                $f= $a->attr['href'];
                //list($download) =explode('/',$f);

                list($d,$fileno) =explode(':',$f);     
    //echo "check $fileno\n";
                scraperwiki::sqliteexecute('insert or replace into thing_file values (?,?)',array($id,$fileno));
            }
        }
    }

    public function get_thing_license($id,$dom) {

       $count = scraperwiki::sqliteexecute("select count(*) as objcount from thing_license where thing=?",array($id));
       $c=$count->data[0][0];
       if ($c> 0){
            echo "$id already has a license: $c\n";
            return 0;
       }


//html body div#main div.main-content div#thing-sidebar div#thing-code-license div#thing-license a img
         foreach($dom->find('#thing-license') as $licensedata) {
            foreach($licensedata->find('a') as $a) {
                foreach($a->find('img') as $i) {
                    $alt= $i->attr['alt'];
                    scraperwiki::sqliteexecute('insert or replace into thing_license values (?,?)',array($id,$alt));                
                }
             }
        }
    }


  public function get_all_things() {
        $things = scraperwiki::sqliteexecute("select thing from things");
        foreach ($things->data as $thing)  {
            $id= $thing[0];            
            echo "going to get $id\n";       
            $this->get_thing($id);
        }
    }

    public function get_thing($id)  { 
 //http://www.thingiverse.com/thing:26828
        $html = scraperwiki::scrape("http://www.thingiverse.com/thing:$id");
        $dom = new simple_html_dom();
        $dom->load($html);
        $this->get_thing_license($id,$dom);
        $this->get_thing_files($id,$dom);
    }

    public function main() {
  
        $this->check_all_categories();
        $this->load_all_subcategories();
        $this->all_sub_categories();
        $this->process_sub_categories(); // get all the data...

    }
}


$s = new ThingVerse();
//$s->main();
$s->setup_tables();
$s->sub_categories_page('hobby','automotive','3');

//$s->get_thing('26828');
$s->get_all_things();


scraperwiki::sqlitecommit();
                                                     
?>

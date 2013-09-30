<?php
echo 'start';
require 'scraperwiki/simple_html_dom.php';           

class site{

    public $dom;
    public $html;
    public $url;
    public $exp;
    public $pages = array();

    function __construct(){
        
    }

    function scrape(){
        $this->html = scraperWiki::scrape($this->url);
        $this->dom = new simple_html_dom();
        $this->dom->load($this->html);
    }
    
    function parse($html){
        return $this->dom->find($html);
    }

    function loadProducts(){
        $dds = $this->dom->find($this->exp->products->holders);
        foreach($dds as $dd){
            $name = $dd->find($this->exp->products->title);
            echo ($name[0]->plaintext).'
    ';
        }
    }

    function loadPages(){
        $links = $this->parse($this->exp->pages->link);
        foreach($links as $link){
            $this->pages[] = array(/*'url'=>*/$link->href,/*'title'=>*/$link->plaintext);
        }
    }

    function save_data(){
        scraperwiki::sqliteexecute("drop table pc_garage_pages");
        //scraperwiki::sqliteexecute("create table IF NOT EXISTS pc_garage_pages (id int PRIMARY KEY AUTO_INCREMENT, url string UNIQUE, title string)");
        print_r(scraperwiki::sqliteexecute('select * from pc_garage_pages'));        
        //echo $sql = $this->createInsert('pc_garage_pages',array('url','title'),$this->pages);
        echo '
';
        //scraperwiki::sqliteexecute($sql);
    }

    function createInsert($table,$fields,$data){
        $field = implode(',',$fields);
        $values = array();
        foreach($data as $d){
            $values[] = "'".implode("','",$d)."'";
        }
        $value = "(".implode("),(",$values).")";
        return ("insert INTO $table ($field) VALUES $value");
    }

}


class pcgarage extends site{
    
    public $url = "http://www.pcgarage.ro/";

    function __construct(){
        $product;
        $product->holders = "dd.product_table_holder";
        $product->title = "dd.product_name";
        $this->exp->products = $product;

        $page;
        $page->holder = "li.second_left_category";
        $page->link = "li.second_left_category li a";
        $this->exp->pages = $page;
    }

}



echo 'a';

$x = new pcgarage();
//$x->scrape();
//$x->loadPages();
$x->save_data();
//$x->loadProducts();

?>
<?php
echo 'start';
require 'scraperwiki/simple_html_dom.php';           

class site{

    public $dom;
    public $html;
    public $url;
    public $exp;
    public $pages = array();

    function __construct(){
        
    }

    function scrape(){
        $this->html = scraperWiki::scrape($this->url);
        $this->dom = new simple_html_dom();
        $this->dom->load($this->html);
    }
    
    function parse($html){
        return $this->dom->find($html);
    }

    function loadProducts(){
        $dds = $this->dom->find($this->exp->products->holders);
        foreach($dds as $dd){
            $name = $dd->find($this->exp->products->title);
            echo ($name[0]->plaintext).'
    ';
        }
    }

    function loadPages(){
        $links = $this->parse($this->exp->pages->link);
        foreach($links as $link){
            $this->pages[] = array(/*'url'=>*/$link->href,/*'title'=>*/$link->plaintext);
        }
    }

    function save_data(){
        scraperwiki::sqliteexecute("drop table pc_garage_pages");
        //scraperwiki::sqliteexecute("create table IF NOT EXISTS pc_garage_pages (id int PRIMARY KEY AUTO_INCREMENT, url string UNIQUE, title string)");
        print_r(scraperwiki::sqliteexecute('select * from pc_garage_pages'));        
        //echo $sql = $this->createInsert('pc_garage_pages',array('url','title'),$this->pages);
        echo '
';
        //scraperwiki::sqliteexecute($sql);
    }

    function createInsert($table,$fields,$data){
        $field = implode(',',$fields);
        $values = array();
        foreach($data as $d){
            $values[] = "'".implode("','",$d)."'";
        }
        $value = "(".implode("),(",$values).")";
        return ("insert INTO $table ($field) VALUES $value");
    }

}


class pcgarage extends site{
    
    public $url = "http://www.pcgarage.ro/";

    function __construct(){
        $product;
        $product->holders = "dd.product_table_holder";
        $product->title = "dd.product_name";
        $this->exp->products = $product;

        $page;
        $page->holder = "li.second_left_category";
        $page->link = "li.second_left_category li a";
        $this->exp->pages = $page;
    }

}



echo 'a';

$x = new pcgarage();
//$x->scrape();
//$x->loadPages();
$x->save_data();
//$x->loadProducts();

?>

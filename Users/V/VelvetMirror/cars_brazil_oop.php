<?php
require 'scraperwiki/simple_html_dom.php';           

class Car
{
    private $_brand;

    public function __construct($brand) {
        $this->_brand = $brand;
    }
    
    public function getBrand() {
        return $this->_brand;
    }

    public function setBrand($brand) {
        $this->_brand = $brand;
    }    
}

class Dom
{
    private $_dom;
    
    public function __construct($html) {       
        $this->_dom = new simple_html_dom();
        $this->_dom->load($html);
    }

    public function getDom() {
        return $this->_dom;
    }
    
    public function setDom($dom) {
        $this->_dom = $dom;
    }
    
}

class Brands {
    private $_uls;
    public function __construct($dom) {
        foreach($dom->getDom()->find("div.lista") as $data) {
            $this->_uls = $data->find("ul[class='']");
        }
    }

    function getBrands() {
        $num_car = 0;
        $brands = array();
        foreach ($this->_uls as $ul) {
                $lis = $ul->find("li.modelo");
        
                foreach ($lis as $li) {
                    $links = $li->find("h1 a");
                    foreach ($links as $link) {
                        $model = $link->plaintext;
                        $arr = explode(' ', trim($model));
                        if(in_array($arr[0], $brands) == false) {
                            $brands[$num_car] = $arr[0];
                            $num_car++;
                        }
                        //$cars[$num_car]['model'] = $model;
                    }
                }
            }
            return $brands;
    }
}

$html = scraperWiki::scrape("http://www.icarros.com.br/catalogo/listaversoes.jsp");           

$dom = new Dom($html);

$brands = new Brands($dom);
$a_brands = $brands->getBrands();

//print_r($a_brands);

$num_cars = 0;
$a_car = array();
foreach ($a_brands as $brand) {
    
    $car = new Car($brand);    
    $a_car[$num_cars] = $car;
    $num_cars++;
}

print_r($a_car[0]);
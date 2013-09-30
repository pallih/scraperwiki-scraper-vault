<?php
    
require 'scraperwiki/simple_html_dom.php';

function notEmpty($str) {
    return !empty($str);
}

class Theater {
    protected static $data = array();

    public static function clear () {
        self::$data = array();
    }

    public static function uid ($element) {
        if (!isset(self::$data["uid"])) {
            self::$data["uid"] = substr(md5(self::$data["title"]), 0, 10);
        }

        return self::$data["uid"];
    }

    public static function getDescription () {
        return self::$data["description"];
    }

    public static function getTrailer () {
        return self::$data["trailer"];
    }
    
    public function getRating() {
        $return = "";
        $content = "";
        if (isset(self::$data["title"])) {
            
            $title = str_replace(" ", "%20", self::$data["title"]);
            //$content = json_decode(scraperWiki::scrape("http://www.imdbapi.com/?t=" . $title . "&y=" . date("Y")));

            if (is_object($content)) {
                $return = $content->Rating;
            }
        }

        return $return;
    }
}

class TheCinemas extends Theater {
    
    public static function mainData ($dom) {
        return $dom->find("ul[class='schedule'] li");
    }

    public static function getTitle ($element) {
        if (!isset(self::$data["title"])) {
            self::$data["title"] = trim($element->find("h2", 0)->plaintext);
        }

        return self::$data["title"];
    }

    public static function isNew ($element) {
        return (is_object($element->find("img[class='banner']", 0)) && (strtolower($element->find("img[class='banner']", 0)->alt) == "new this week"));
    }

    public static function getPoster ($element) {
        if (!isset(self::$data["poster"])) {
            self::$data["poster"] = $element->find("img[class='poster']", 0)->getAttribute("src");
            self::$data["poster"] = (substr(self::$data["poster"], 0,1) == "/") ? self::getUrl() . self::$data["poster"] : self::getUrl() . "/" . self::$data["poster"];
        }

        return self::$data["poster"];
    }

    public static function getUrl () {
        return "http://thecinemascuracao.com";
    }

    public static function loadDeepData($element) {
        if (!isset(self::$data["description"]) || !isset(self::$data["trailer"])) {
            $strNewTarget = $element->find("a", 0)->getAttribute("href");
            $strNewTarget = (substr($strNewTarget, 0, 1) == "/") ? $strNewTarget : "/" . $strNewTarget;
        
            $newHtml = scraperWiki::scrape(self::getUrl() . $strNewTarget);
                   
            $newDom = new simple_html_dom();
            $newDom->load($newHtml);

                self::$data["description"] = $newDom->find("div[class='story movie'] div", 8)->find("p")->innertext;
        
                // clean up
                self::$data["description"] = str_replace("<br>", "", self::$data["description"]);
                self::$data["description"] = str_replace("&nbsp;", "", self::$data["description"]);
        
            self::$data["trailer"] = (is_object($newDom->find("iframe", 0))) ? $newDom->find("iframe", 0)->getAttribute("src") : "";
        }
    }

    public static function extractTime ($data) {
        $arrNew = array();
        $strTime = $data->find("p[class='showtimes']", 0)->plaintext;
        $arrTime = explode("\n", $strTime);

        foreach ($arrTime as $strTimePart) {
            $temp = explode(": ", $strTimePart);
            $strTimePart = trim($strTimePart);
            if (!empty($strTimePart)) {
                for ($i = 0; $i < count($temp); $i++) {
                    $strKey = trim(str_replace(" ", "", str_replace(".", "", strtolower($temp[$i]))));
                    $arrNew[$strKey] = explode(" ", $temp[$i+1]);
                    $arrNew[$strKey] = array_values($arrNew[$strKey]);
                    $arrNew[$strKey] = array_filter($arrNew[$strKey], "notEmpty");
                    $arrNew[$strKey] = array_filter($arrNew[$strKey], "trim");
                    $i++;
                }
            }
        }

        return json_encode($arrNew);
    }
}

class TheMovies extends Theater {
    
    public static function mainData ($dom) {
        return $dom->find("#inside a[style='text-decoration:none;']");
    }

    public static function getTitle ($element) {
        if (!isset(self::$data["title"])) {
            self::$data["title"] = trim($element->find("h3", 0)->plaintext);
        }

        return self::$data["title"];
    }

    public static function getPoster ($element) {
        if (!isset(self::$data["poster"])) {
            self::$data["poster"] = $element->find("div p img", 0)->getAttribute("src");
            self::$data["poster"] = (substr(self::$data["poster"], 0,1) == "/") ? self::getUrl() . self::$data["poster"] : self::getUrl() . "/" . self::$data["poster"];
        }

        return self::$data["poster"];
    }

    public static function isNew ($element) {
        return (is_object($element->find("div[class=box] p img", 1)) && (strtolower($element->find("div[class=box] p img", 1)->alt) == "new this week"));
    }

    public static function getUrl () {
        return "http://themoviescuracao.com";
    }

    public static function loadDeepData($element) {
        if (!isset(self::$data["description"]) || !isset(self::$data["trailer"])) {
            $strNewTarget = $element->getAttribute("href");
            $strNewTarget = (substr($strNewTarget, 0, 1) == "/") ? $strNewTarget : "/" . $strNewTarget;
        
            $newHtml = scraperWiki::scrape(self::getUrl() . $strNewTarget);
                   
            $newDom = new simple_html_dom();
            $newDom->load($newHtml);
        
            foreach ($newDom->find("div#inside table") as $data) {
                self::$data["description"] = trim($data->find("tr", 8)->find("td", 0)->innertext);
        
                // clean up
                self::$data["description"] = str_replace("<br>", "", self::$data["description"]);
                self::$data["description"] = str_replace("&nbsp;", "", self::$data["description"]);
        
                self::$data["trailer"] = (is_object($data->find("tr", 9)->find("iframe", 0))) ? $data->find("tr", 9)->find("iframe", 0)->getAttribute("src") : "";
            }
        }
    }

    public static function extractTime ($data) {
        $arrNew = array();
        $arrParagraphs = $data->find("div.box", 0)->find("p");

        foreach ($arrParagraphs as $objParagraph) {
            $temp = explode(": ", $objParagraph->plaintext);
            $strTimePart = trim($objParagraph->plaintext);
            if (!empty($strTimePart)) {
                for ($i = 0; $i < count($temp); $i++) {
                    $strKey = trim(str_replace(" ", "", str_replace(".", "", strtolower($temp[$i]))));
                    $arrNew[$strKey] = array_filter(array_values(explode(" ", $temp[$i+1])), "notEmpty");
                    $i++;
                }
            }
        }

        return json_encode($arrNew);
    }
}

$theaters = array("TheCinemas", "TheMovies");

scraperwiki::sqliteexecute("delete from swdata");
foreach ($theaters as $theater) {
//    $theater = get_class($theater);
    $html = scraperWiki::scrape($theater::getUrl());         
    $dom = new simple_html_dom();
    $dom->load($html);
    
    
    foreach($theater::mainData($dom) as $data){
        $theater::clear();
    
        $arrMovie = array();
        $arrMovie["title"] = $theater::getTitle($data);
        $arrMovie["uid"] = $theater::uid($data);
        $arrMovie["poster"] = $theater::getPoster($data);
        $arrMovie["rating"] = $theater::getRating($theater::getTitle($data));
        $arrMovie["new"] = $theater::isNew($data);

       // $playTimes = array();
       // preg_match_all("/\d{2}\:\d{2}/i", $arrMovie["playtimes"], $playTimes);
        //sort($playTimes[0]);
       // $playTimes = implode("||", $playTimes[0]);

//echo($data->find("div.innermovie", 0)->find("p", 0)->plaintext); exit;
        
        $arrMovie["playtimes"] = $theater::extractTime($data);
    
        $theater::loadDeepData($data);
        $arrMovie["description"] = $theater::getDescription();
        $arrMovie["trailer"] = $theater::getTrailer();
        $arrMovie["theater"] = $theater;
    
        scraperWiki::save_sqlite(array("uid"), $arrMovie);
    }
}

?><?php
    
require 'scraperwiki/simple_html_dom.php';

function notEmpty($str) {
    return !empty($str);
}

class Theater {
    protected static $data = array();

    public static function clear () {
        self::$data = array();
    }

    public static function uid ($element) {
        if (!isset(self::$data["uid"])) {
            self::$data["uid"] = substr(md5(self::$data["title"]), 0, 10);
        }

        return self::$data["uid"];
    }

    public static function getDescription () {
        return self::$data["description"];
    }

    public static function getTrailer () {
        return self::$data["trailer"];
    }
    
    public function getRating() {
        $return = "";
        $content = "";
        if (isset(self::$data["title"])) {
            
            $title = str_replace(" ", "%20", self::$data["title"]);
            //$content = json_decode(scraperWiki::scrape("http://www.imdbapi.com/?t=" . $title . "&y=" . date("Y")));

            if (is_object($content)) {
                $return = $content->Rating;
            }
        }

        return $return;
    }
}

class TheCinemas extends Theater {
    
    public static function mainData ($dom) {
        return $dom->find("ul[class='schedule'] li");
    }

    public static function getTitle ($element) {
        if (!isset(self::$data["title"])) {
            self::$data["title"] = trim($element->find("h2", 0)->plaintext);
        }

        return self::$data["title"];
    }

    public static function isNew ($element) {
        return (is_object($element->find("img[class='banner']", 0)) && (strtolower($element->find("img[class='banner']", 0)->alt) == "new this week"));
    }

    public static function getPoster ($element) {
        if (!isset(self::$data["poster"])) {
            self::$data["poster"] = $element->find("img[class='poster']", 0)->getAttribute("src");
            self::$data["poster"] = (substr(self::$data["poster"], 0,1) == "/") ? self::getUrl() . self::$data["poster"] : self::getUrl() . "/" . self::$data["poster"];
        }

        return self::$data["poster"];
    }

    public static function getUrl () {
        return "http://thecinemascuracao.com";
    }

    public static function loadDeepData($element) {
        if (!isset(self::$data["description"]) || !isset(self::$data["trailer"])) {
            $strNewTarget = $element->find("a", 0)->getAttribute("href");
            $strNewTarget = (substr($strNewTarget, 0, 1) == "/") ? $strNewTarget : "/" . $strNewTarget;
        
            $newHtml = scraperWiki::scrape(self::getUrl() . $strNewTarget);
                   
            $newDom = new simple_html_dom();
            $newDom->load($newHtml);

                self::$data["description"] = $newDom->find("div[class='story movie'] div", 8)->find("p")->innertext;
        
                // clean up
                self::$data["description"] = str_replace("<br>", "", self::$data["description"]);
                self::$data["description"] = str_replace("&nbsp;", "", self::$data["description"]);
        
            self::$data["trailer"] = (is_object($newDom->find("iframe", 0))) ? $newDom->find("iframe", 0)->getAttribute("src") : "";
        }
    }

    public static function extractTime ($data) {
        $arrNew = array();
        $strTime = $data->find("p[class='showtimes']", 0)->plaintext;
        $arrTime = explode("\n", $strTime);

        foreach ($arrTime as $strTimePart) {
            $temp = explode(": ", $strTimePart);
            $strTimePart = trim($strTimePart);
            if (!empty($strTimePart)) {
                for ($i = 0; $i < count($temp); $i++) {
                    $strKey = trim(str_replace(" ", "", str_replace(".", "", strtolower($temp[$i]))));
                    $arrNew[$strKey] = explode(" ", $temp[$i+1]);
                    $arrNew[$strKey] = array_values($arrNew[$strKey]);
                    $arrNew[$strKey] = array_filter($arrNew[$strKey], "notEmpty");
                    $arrNew[$strKey] = array_filter($arrNew[$strKey], "trim");
                    $i++;
                }
            }
        }

        return json_encode($arrNew);
    }
}

class TheMovies extends Theater {
    
    public static function mainData ($dom) {
        return $dom->find("#inside a[style='text-decoration:none;']");
    }

    public static function getTitle ($element) {
        if (!isset(self::$data["title"])) {
            self::$data["title"] = trim($element->find("h3", 0)->plaintext);
        }

        return self::$data["title"];
    }

    public static function getPoster ($element) {
        if (!isset(self::$data["poster"])) {
            self::$data["poster"] = $element->find("div p img", 0)->getAttribute("src");
            self::$data["poster"] = (substr(self::$data["poster"], 0,1) == "/") ? self::getUrl() . self::$data["poster"] : self::getUrl() . "/" . self::$data["poster"];
        }

        return self::$data["poster"];
    }

    public static function isNew ($element) {
        return (is_object($element->find("div[class=box] p img", 1)) && (strtolower($element->find("div[class=box] p img", 1)->alt) == "new this week"));
    }

    public static function getUrl () {
        return "http://themoviescuracao.com";
    }

    public static function loadDeepData($element) {
        if (!isset(self::$data["description"]) || !isset(self::$data["trailer"])) {
            $strNewTarget = $element->getAttribute("href");
            $strNewTarget = (substr($strNewTarget, 0, 1) == "/") ? $strNewTarget : "/" . $strNewTarget;
        
            $newHtml = scraperWiki::scrape(self::getUrl() . $strNewTarget);
                   
            $newDom = new simple_html_dom();
            $newDom->load($newHtml);
        
            foreach ($newDom->find("div#inside table") as $data) {
                self::$data["description"] = trim($data->find("tr", 8)->find("td", 0)->innertext);
        
                // clean up
                self::$data["description"] = str_replace("<br>", "", self::$data["description"]);
                self::$data["description"] = str_replace("&nbsp;", "", self::$data["description"]);
        
                self::$data["trailer"] = (is_object($data->find("tr", 9)->find("iframe", 0))) ? $data->find("tr", 9)->find("iframe", 0)->getAttribute("src") : "";
            }
        }
    }

    public static function extractTime ($data) {
        $arrNew = array();
        $arrParagraphs = $data->find("div.box", 0)->find("p");

        foreach ($arrParagraphs as $objParagraph) {
            $temp = explode(": ", $objParagraph->plaintext);
            $strTimePart = trim($objParagraph->plaintext);
            if (!empty($strTimePart)) {
                for ($i = 0; $i < count($temp); $i++) {
                    $strKey = trim(str_replace(" ", "", str_replace(".", "", strtolower($temp[$i]))));
                    $arrNew[$strKey] = array_filter(array_values(explode(" ", $temp[$i+1])), "notEmpty");
                    $i++;
                }
            }
        }

        return json_encode($arrNew);
    }
}

$theaters = array("TheCinemas", "TheMovies");

scraperwiki::sqliteexecute("delete from swdata");
foreach ($theaters as $theater) {
//    $theater = get_class($theater);
    $html = scraperWiki::scrape($theater::getUrl());         
    $dom = new simple_html_dom();
    $dom->load($html);
    
    
    foreach($theater::mainData($dom) as $data){
        $theater::clear();
    
        $arrMovie = array();
        $arrMovie["title"] = $theater::getTitle($data);
        $arrMovie["uid"] = $theater::uid($data);
        $arrMovie["poster"] = $theater::getPoster($data);
        $arrMovie["rating"] = $theater::getRating($theater::getTitle($data));
        $arrMovie["new"] = $theater::isNew($data);

       // $playTimes = array();
       // preg_match_all("/\d{2}\:\d{2}/i", $arrMovie["playtimes"], $playTimes);
        //sort($playTimes[0]);
       // $playTimes = implode("||", $playTimes[0]);

//echo($data->find("div.innermovie", 0)->find("p", 0)->plaintext); exit;
        
        $arrMovie["playtimes"] = $theater::extractTime($data);
    
        $theater::loadDeepData($data);
        $arrMovie["description"] = $theater::getDescription();
        $arrMovie["trailer"] = $theater::getTrailer();
        $arrMovie["theater"] = $theater;
    
        scraperWiki::save_sqlite(array("uid"), $arrMovie);
    }
}

?>
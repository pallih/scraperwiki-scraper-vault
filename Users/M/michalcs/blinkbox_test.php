<?php

$html = scraperWiki::scrape("http://www.blinkbox.com/Movies/Catalogue/Free?page=1&sort=Popularity");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
    $m = new MediaInfo();

foreach($dom->find("ul[@id='contentList_lv_ul'] div[@class='summary']") as $movies){
    $title = $movies->find("span[@class='t1']");
    $link = $movies->find("a");
    $record = array('title' => $title[0]->plaintext, 'link' => $link[0]->href);
    /* print json_encode($record) . "\n"; */
    $info = $m->getMovieInfo($title[0]->plaintext);
    print_r($info);
}




    class MediaInfo
    {
        public $info;

        function __construct($str = null)
        {
            if(!is_null($str))
                $this->autodetect($str);
        }

        function autodetect($str)
        {
            // Attempt to cleanup $str in case it's a filename ;-)
            $str = pathinfo($str, PATHINFO_FILENAME);
            $str = $this->normalize($str);

            // Is it a movie or tv show?
            if(preg_match('/s[0-9][0-9]?.?e[0-9][0-9]?/i', $str) == 1)
                $this->info = $this->getEpisodeInfo($str);
            else
                $this->info = $this->getMovieInfo($str);

            return $this->info;
        }

        function getEpisodeInfo($str)
        {
            $arr = array();
            $arr['kind'] = 'tv';
            return $arr;
        }

        function getMovieInfo($str)
        {
            $str  = str_ireplace('the ', '', $str);
            $url  = "http://www.google.com/search?hl=en&q=imdb+" . urlencode($str) . "&btnI=I%27m+Feeling+Lucky";
            $html = $this->geturl($url);
            if(stripos($html, "302 Moved") !== false)
                $html = $this->geturl($this->match('/HREF="(.*?)"/ms', $html, 1));

            $arr = array();
            $arr['kind'] = 'movie';
            $arr['id'] = $this->match('/poster.*?(tt[0-9]+)/ms', $html, 1);
            $arr['title'] = $this->match('/<title>(.*?)<\/title>/ms', $html, 1);
            /*$arr['title'] = preg_replace('/\([0-9]+\)/', '', $arr['title']);
            $arr['title'] = trim($arr['title']);*/
            $arr['rating'] = $this->match('/([0-9]\.[0-9])\/10/ms', $html, 1);
            $arr['director'] = trim(strip_tags($this->match('/Director:(.*?)<\/a>/ms', $html, 1)));
            $arr['release_date'] = $this->match('/([0-9][0-9]? (January|February|March|April|May|June|July|August|September|October|November|December) (19|20)[0-9][0-9])/ms', $html, 1);
            $arr['plot'] = trim(strip_tags($this->match('/Plot:(.*?)<a/ms', $html, 1)));
            $arr['genres'] = $this->match_all('/Sections\/Genres\/(.*?)[\/">]/ms', $html, 1);
            $arr['genres'] = array_unique($arr['genres']);
            $arr['poster'] = $this->match('/<a.*?name=.poster.*?src=.(.*?)(\'|")/ms', $html, 1);

            $arr['cast'] = array();
            foreach($this->match_all('/class="nm">(.*?\.\.\..*?)<\/tr>/ms', $html, 1) as $m)
            {
                list($actor, $character) = explode('...', strip_tags($m));
                $arr['cast'][trim($actor)] = trim($character);
            }

            return $arr;
        }

        // ****************************************************************

        function normalize($str)
        {
            $str = str_replace('_', ' ', $str);
            $str = str_replace('.', ' ', $str);
            $str = preg_replace('/ +/', ' ', $str);
            return $str;
        }

        function geturl($url, $username = null, $password = null)
        {
            $ch = curl_init();
            if(!is_null($username) && !is_null($password))
                curl_setopt($ch, CURLOPT_HTTPHEADER, array('Authorization: Basic ' .  base64_encode("$username:$password")));
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
            $html = curl_exec($ch);
            curl_close($ch);
            return $html;
        }

        function match_all($regex, $str, $i = 0)
        {
            if(preg_match_all($regex, $str, $matches) === false)
                return false;
            else
                return $matches[$i];

        }

        function match($regex, $str, $i = 0)
        {
            if(preg_match($regex, $str, $match) == 1)
                return $match[$i];
            else
                return false;
        }
    }

?>
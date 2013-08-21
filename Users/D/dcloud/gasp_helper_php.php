<?php /* FWIW: ScraperWiki is running PHP v5.3.5 */

function _hash($content)
{
    $input_encoding = mb_detect_encoding($content);
    if ($input_encoding) $content = mb_convert_encoding($content, $input_encoding);
    
    return hash("sha256", utf8_encode($content));
}

/**
* GaspHelper
*/
class GaspHelper
{
    /*
        Python script pulls from scraperwiki.datastore.m_scrapername, but that isn't part of PHP scraperwiki lib, so we 
        ask for the user to input it (until we come up with a better solution)
    */
    
    function __construct($sunlight_key, $bioguide_id, $scraper_name="")
    {
        $this->sunlight_key = $sunlight_key;
        $this->bioguide_id = $bioguide_id;
        $this->scraper_name = $scraper_name;
        
        $this->updates = array();
    }
    
    private function _add_update($update_type, $title, $date, $content, $kwargs="")
    {
        $data = array(
            'update_type' => $update_type,
            'title' => $title,
            'date' => $date,
            'content' => $content,
            'content_hash' => _hash($content),
            'extra' => json_encode($kwargs)
        );
        scraperwiki::save_sqlite( array('title', 'date', 'content_hash', 'update_type'), $data, $table_name='updates' );
    }
    
    public function add_biography($content, $kwargs="")
    {
        $data = array(
            'content' => $content,
            'content_hash' => _hash($content),
            'extra' => json_encode($kwargs)
        );
        
        print $data['content'] . "\n";
        scraperwiki::save_sqlite( array('content_hash'), $data, $table_name='biography' );
    }
    
    public function add_issue($title, $content, $kwargs="")
    {
        $data = array(
            'title'=> $title,
            'content' => $content,
            'content_hash' => _hash($content),
            'extra' => json_encode($kwargs)
        );
        scraperwiki::save_sqlite( array('title', 'content_hash'), $data, $table_name='issues' );
    }
    
    public function add_office($address, $phone, $fax="", $kwargs="")
    {
        $data = array(
            'address' => $address, 
            'phone' => $phone,
            'fax' => $fax,
            'extra' => json_encode($kwargs)
        );
        $unique_keys = array('address', 'phone', 'fax');
        scraperwiki::save_sqlite( $unique_keys, $data, $table_name='offices' );
    }

    public function add_event($title, $date, $location, $kwargs="")
    {
        $data = array(
            'title' => $title,
            'date' => $date,
            'location' => $location,
            'extra' => json_encode($kwargs)
        );
        scraperwiki::save_sqlite( array('title', 'date', 'location'), $data, $table_name='events' );
    }

    public function add_social_media($service_name, $url, $kwargs="")
    {
        $data = array(
            'service' => $service_name,
            'url' => $url,
            'extra' => json_encode($kwargs)
        );
        scraperwiki::save_sqlite( array('service', 'url'), $data, $table_name='social_media' );
    }

    // type helpers
    public function add_press_release($title, $date, $content, $kwargs="")
    {
        $this->_add_update('press_release', $title, $date, $content, $kwargs);
    }
    
    public function add_news_update($title, $date, $content, $kwargs="")
    {
        $this->_add_update('news_update', $title, $date, $content, $kwargs);
    }
    
    public function add_blog_post($title, $date, $content, $kwargs="")
    {
        $this->_add_update('blog_post', $title, $date, $content, $kwargs);
    }

    public function add_other_update($title, $date, $content, $kwargs="")
    {
        $this->_add_update('other', $title, $date, $content, $kwargs);
    }
    
    public function add_facebook($url, $kwargs="")
    {
        $this->add_social_media('facebook', $url, $kwargs);
    }

    public function add_flickr($url, $kwargs="")
    {
        $this->add_social_media('flickr', $url, $kwargs);
    }

    public function add_twitter($url, $kwargs="")
    {
        $this->add_social_media('twitter', $url, $kwargs);
    }
    

    public function add_youtube($url, $kwargs="")
    {
        $this->add_social_media('youtube', $url, $kwargs);
    }

    public function finish()
    {   
        # send heartbeat
        $url = sprintf( 'http://services.sunlightlabs.com/gasp/heartbeat/?apikey=%s&bioguide_id=%s&scraper_id=%s', 
                        $this->sunlight_key, 
                        $this->bioguide_id,
                        $this->scraper_name 
                    );
        print $url;
        print scraperWiki::scrape( $url );
    }

}
?>
<?php

class BlogPost
{
    var $date;
    var $ts;
    var $link;

    var $title;
    var $text;
}

class BlogFeed
{
    var $posts = array();

    function BlogFeed($file_or_url)
    {
        if(!eregi('^http:', $file_or_url))
            $feed_uri = $_SERVER['DOCUMENT_ROOT'] .'/shared/xml/'. $file_or_url;
        else
            $feed_uri = $file_or_url;

        $xml_source = file_get_contents($feed_uri);
        $x = simplexml_load_string($xml_source);

        if(count($x) == 0)
            return;

        foreach($x->channel->item as $item)
        {
            $post = new BlogPost();
            $post->date = (string) $item->pubDate;
            $post->ts = strtotime($item->pubDate);
            $post->link = (string) $item->link;
            $post->title = (string) $item->title;
            $post->text = (string) $item->description;

            // Create summary as a shortened body and remove images, extraneous line breaks, etc.
            $summary = $post->text;
            $summary = eregi_replace("<img[^>]*>", "", $summary);
            $summary = eregi_replace("^(<br[ ]?/>)*", "", $summary);
            $summary = eregi_replace("(<br[ ]?/>)*$", "", $summary);

            // Truncate summary line to 100 characters
            $max_len = 100;
            if(strlen($summary) > $max_len)
                $summary = substr($summary, 0, $max_len) . '...';

            $post->summary = $summary;

            $this->posts[] = $post;
        }
    }
}

?>
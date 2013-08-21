 <?php
require 'scraperwiki/simple_html_dom.php';

abstract class blog
{
    public $_blog_type;
    protected $_html;
    function __construct($html)
    {
        $this->_html = $html;
    }

    abstract public function find_signature();
    abstract public function get_comments();
    abstract public function get_comment_anchor($comment);
}

class typepad extends blog
{
    function __construct($html)
    {
        parent::__construct($html);
        $this->_blog_type = 'typepad';
    }

    public function find_signature()
    {
        $result = false;
        $sig = $this->_html->find(".comments-header");
    
        if ($sig)
        {
            $result = true;
        }
        return $result;
    }

    private function get_comments1(&$output)
    {
        $result = false;
        $comments = $this->_html->find("#all-comments div");
        if ($comments)
        {
            if (is_array($comments))
            {
                $content = $comments[0]->find("p.comment-footer");
                $output = $content;
                $result = true;
            }
        } 
        return $result;
    }
    
    private function get_comments2(&$output)
    {
        $result = false;
        $comments = $this->_html->find("div.comments-content");
        if ($comments)
        {
            if (is_array($comments))
            {
                $content = $comments[0]->find("div.comment");
                $output = $content;
                $result = true;
            }
        } 
        return $result;
    }

    public function get_comments()
    {
        $result=null;
        if ($this->get_comments1($comments))
        {
            $result = $comments;
        }
        else if ($this->get_comments2($comments))
        {
            $result = $comments;
        }
        else
        {
            throw new Exception($this->_blog_type . ' comments could not be found.');
        }
    
        return $result;
    }
    
    public function get_comment_anchor($comment)
    {
        $result = null;
    
        $anchors = $comment->find("a");
    
        $result = $anchors[0];
    
        return $result;
    }
}

class wordpress extends blog
{
    function __construct($html)
    {
        parent::__construct($html);
        $this->_blog_type = 'wordpress';
    }

    public function find_signature()
    {
        $result = false;
        $sig = $this->_html->find("ol.commentlist");
    
        if ($sig)
        {
            $result = true;
        }
        return $result;
    }
    
    public function get_comments()
    {
        $result=null;
        $comments = $this->_html->find("ol.commentlist");
        $content = $comments[0]->find("li");

        $result = $content;
    
        return $result;
    }
    
    public function get_comment_anchor($comment)
    {
        $result = null;
    
        $anchors = $comment->find("cite a.url");
    
        $result = $anchors;
    
        return $result;
    }
} 

class blogger extends blog
{
    function __construct($html)
    {
        parent::__construct($html);
        $this->_blog_type = 'blogger';
    }

    public function find_signature()
    {
        $result = false;
        $sig = $this->_html->find("#comment-holder");
    
        if ($sig)
        {
            $result = true;
        }
        return $result;
    }
    
    public function get_comments()
    {
        $result=null;
        $container =  $this->_html->find("#comment-holder");
        $thread = $container[0]->find("div.comment-thread");
        $comments = $thread[0]->find("div.comment-block");

        $result = $comments;
    
        return $result;
    }
    
    public function get_comment_anchor($comment)
    {
        $result = null;
    
        $anchors = $comment->find("cite.user a");
    
        $result = $anchors;
    
        return $result;
    }
}  

function dump_anchor($anchor)
{
    if (is_null($anchor))
    {
    }
    else if (is_array($anchor))
    {
        if (isset($anchor[0]))
        {
            dump_anchor($anchor[0]);
        }
    }
    else if (is_object($anchor))
    {
        print('link = ' . $anchor->href . ', ');
        print('title = ' . $anchor->title . ', ');
        print('rel = ' . $anchor->rel . ', ');
        print('text = ' . $anchor->text() . "\n");
    }
}

function dump_node($node)
{
    if (is_null($node))
    {
        print('element is null');
        return;
    }

    if (is_array($node))
    {
        if (isset($node[0]))
        {
            foreach($node as $thisnode)
            {
                dump_node($thisnode);
            }
            return;
        }
        else if ( count($node) > 0 )
        {
            $keys = array_keys($node);
            print_r($keys);
            return;
        }
        else
        {
            print('array is empty');
            return;
        }
    }

    $tag = $node->tag;
    $id = $node->id;
    $class = (isset($node->attr['class'])) ? $node->attr['class'] : '';

    print("<{$tag} id=\"{$id}\" class=\"{$class}\"\n");
}

function is_typepad($html,&$helper)
{
    $result = false;

    $o = new typepad($html);
    if ($o->find_signature())
    {
        $helper = $o;
        $result = true;
    }

    return $result;
}

function is_blogger($html,&$helper)
{
    $result = false;

    $o = new blogger($html);
    if ($o->find_signature())
    {
        $helper = $o;
        $result = true;
    }

    return $result; 
}

function is_wordpress($html,&$helper)
{
    $result = false;

    $o = new wordpress($html);
    if ($o->find_signature())
    {
        $helper = $o;
        $result = true;
    }

    return $result;
}

function find_signature($html,&$blog)
{
    $result = false;

    $_blog;
    $sig_found = false;
    if (is_typepad($html,$_blog))
    {
        $sig_found = true;
    }
    else if(is_wordpress($html,$_blog))
    {
        $sig_found = true;
    }
    else if(is_blogger($html,$_blog))
    {
        $sig_found = true;
    }
 
    if ($sig_found)
    {
        $blog = $_blog;
        $result = true;
    }

    return $result;
}

function scrape_resource($res)
{
    $html = str_get_html($res);
    
    $blog;
    if (find_signature($html,$blog))
    {
        $comments = $blog->get_comments();
        foreach($comments as $comment)
        {
            $anchor = $blog->get_comment_anchor($comment);
            dump_anchor($anchor);
        }
    }
    else
    {
        print('blog signature not recognized.');
    }
}

$urls = array(
    'http://thestar.blogs.com/kenzie/2011/01/how-are-car-washes-like-airports.html',
    'http://stopthestorm.wordpress.com/2012/04/03/this-post-as-yogi-might-say-not-for-the-average-bear/',
    'http://mas110sem12012-lab5.blogspot.com/2012/03/so-fml.html',
    'http://daddyroblog.blogs.com/daddyroblog/2011/12/the-car-wash.html',
    'http://jonnybaker.blogs.com/jonnybaker/2011/03/hipstamatic-car-wash.html',
    'http://openchoke.blogs.com/open_choke/2010/01/urine-a-car-wash.html',
    'http://www.questiontechnology.org/blog/2009/09/michael-sandel-on-genetics-and-morality.html',
    'http://www.questiontechnology.org/blog/2009/01/arne-naess.html'
);

function process_all()
{
    global $urls;

    foreach($urls as $url)
    {
        print('processing ' . $url . "\n");
        $res = scraperWiki::scrape($url);
        try
        {
            scrape_resource($res);
        }
        catch(Exception $e)
        {
            print($e->getMessage() . "\n");
        }
    }
}

function unit_test($index)
{
    global $urls;

    print('processing ' . $urls[$index] . "\n");
    $res = scraperWiki::scrape($urls[$index]);
    try
    {
        scrape_resource($res);
    }
    catch(Exception $e)
    {
        print($e->getMessage() . "\n");
    }
}

/*unit_test(0);*/

$url = 'http://www.google.com';

$res = scraperWiki::scrape($url);
if ($res)
{
    $html = str_get_html($res);
    if ($html)
    {
        $list = $html->find('body');

        if (is_array($list))
        {
            print('list has ' . count($list) . ' element(s).');
        }
        
        dump_node($list);
    }
    else
    {
        print($res);
    }
}
else
{
    print('error retrieving url.');
}
?> 
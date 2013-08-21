<?php
/**
* Federal Data (Top Parent Class)
*/
class federal_data {

    public function __construct($data = FALSE){
    
    }
    
    /**
    * Default XML Parsing function
    * This function is run on construct if the supplied data is of the type “SimpleXMLElement”
    *
    *    PHP’s SimpleXMLElement obejct class has several functions associated to it however we
    *    only need to take advantage of retrieving information from either a child value or an
    *    attribute value. Children elements are referenced as an object variable of their parent
    *    and attributes are obtained by using the function:
    *    [SimpleXMLElement object]->attributes()->{attribute name}
    *
    *    @vars    obj        $data        SimpleXMLElement Object
    */
    public function parse_data_from_xml($data) {  }
    
    public function get_element_by_language($lang, $element, $parent){
        $all_elements = $parent->{$element};
        foreach($all_elements as $el) if($el->attributes()->language == $lang) return $el;
        return NULL;
    }
    
    public function get_government_file($external_url){
        // Using the custom header context, capture the XML file as a string and return trimmed string value
        return trim(file_get_contents($external_url, FALSE, stream_context_create(array(
            'http' => array(
                'method'    => 'GET',
                'header'    => 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30' . "\r\n"
            )
        ))));
    }

}

/**
* Federal Bill
*
*    @vars    int        $id                    Unique identifier of the specific bill
*            int        $last_updated        PHP date of the last update
*            str        $title_en            Government provided title of the bill (English)
*            str        $title_fr            Government provided title of the bill (French)
*            int        $status                Stage in which the bill is at
*            int        $sponsor_id            Unique identifier of the representative (rep_id)
*            int        $session            Parliamentary number
*            int        $session_number        Parliamentary session number
*            str        $prefix                Bill ID prefix character
*            int        $introductory_date    PHP date of the session’s start date
*            arr        $publications        Federal Publication objects associated to the bill
*            arr        $events                Federal Event objects associated to the bill
*/
class federal_bill extends federal_data {

    public    $id,
            $identifier,
            $last_updated,
            $title_en,
            $title_fr,
            $status,
            $sponsor_id,
            $session,
            $session_number,
            $prefix,
            $number,
            $introductory_date,
            $publications,
            $events;
    
    public function __construct($data){
        parent::__construct();
        if(get_class($data) === 'SimpleXMLElement') $this->parse_data_from_xml($data);
    }
    
    /**
    * Default XML Parsing function
    * This function is run on construct if the supplied data is of the type “SimpleXMLElement”
    *
    *    PHP’s SimpleXMLElement obejct class has several functions associated to it however we
    *    only need to take advantage of retrieving information from either a child value or an
    *    attribute value. Children elements are referenced as an object variable of their parent
    *    and attributes are obtained by using the function:
    *    [SimpleXMLElement object]->attributes()->{attribute name}
    *
    *    @params    (obj)    $data        SimpleXMLElement Object
    */
    public function parse_data_from_xml($data){
    
        // Root element’s id attribute
        $this->identifier            = (integer) $data->attributes()->id;
        
        // Root element’s lastUpdated attribute converted to time
        $this->last_updated            = strtotime($data->attributes()->lastUpdated);
        
        // Contents of the appropriate language’s Title element of the BillTitle element
        $this->title_en                = (string) $this->get_element_by_language('en', 'Title', $data->BillTitle);
        $this->title_fr                = (string) $this->get_element_by_language('fr', 'Title', $data->BillTitle);
        
        // id attribute of the SponsorAffiliation element
        $this->sponsor_id            = (integer) $data->SponsorAffiliation->attributes()->id;
        
        // Appropriate attributes of the ParliamentSession element
        $this->session                = (integer) $data->ParliamentSession->attributes()->parliamentNumber;
        $this->session_number        = (integer) $data->ParliamentSession->attributes()->sessionNumber;
        
        // prefix attribute of the BillNumber element
        $this->prefix                = (string) $data->BillNumber->attributes()->prefix;
        $this->number                = (integer) $data->BillNumber->attributes()->number;
        
        // Content value of the BillIntroducedDate element converted to time
        $this->introductory_date    = strtotime($data->BillIntroducedDate);

        // Array of objects created from each of the Publication elements of the Publications element
        foreach($data->Publications->Publication as $publication_data){
            $this->publications[] = new federal_publication($publication_data);
        }

        // Array of objects created from each of the Event elements of the LegislativeEvents element
        foreach($data->Events->LegislativeEvents->Event as $event_data) {
            $this->events[]    = new federal_event($event_data);
        }
        
        // The current status of the bill is equal to that of the last event status
        $this->status = $this->events[count($this->events) - 1]->status;
        
        $data = NULL;
    }
    
    public function add_to_database($identifier){
        
            $insert_data = array(
                'title_en'            => $this->title_en,
                'title_fr'            => $this->title_fr,
                'sponsor_id'        => $this->sponsor_id,
                'status'            => $this->status,
                'prefix'            => $this->prefix,
                'number'            => $this->number,
                'introductory_date'    => $this->introductory_date,
                'identifier'        => $this->identifier,
                'parliament'        => 41,
                'session'            => 1,
                'is_public'            => 1,
                'bill_type'            => 1
            );
            $keys = array_keys($insert_data);
            scraperwiki::save_sqlite($keys, $insert_data, 'federal_bills');
            
            foreach($this->publications as $publication){
                unset($publication->id);
                $publication->bill_id = $this->identifier;
                $publication = (array) $publication;
                $keys = array_keys($publication);
                scraperwiki::save_sqlite($keys, $publication, 'federal_publications');
            }
            
            foreach($this->events as $event){
                unset($event->id);
                $publication->bill_id = $this->identifier;
                $event->committees = json_encode($event->committees);
                $event = (array) $event;
                $keys = array_keys($event);
                scraperwiki::save_sqlite($keys, $event, 'federal_events');
            }

            
        }
}

/**
* Federal Event
*
*    @vars    int        $id                    Unique identifier of the specific event
*            str        $chamber            Abbreviation of the chamber associated to the event
*            int        $date                PHP date of the last update
*            int        $meeting_number        Meeting number of the event
*            arr        $committees            Unique identifier of the representative (rep_id)
*            str        $title_en            Government provided title of the bill (English)
*            str        $title_fr            Government provided title of the bill (French)
*            str        $description_en        Bill ID prefix character
*            str        $description_fr        PHP date of the session’s start date
*/
class federal_event extends federal_data {
    
    public $id,
            $identifier,
            $chamber,
            $date,
            $meeting_number,
            $committees,
            $title_en,
            $title_fr,
            $description_en,
            $description_fr,
            $status;

    public function __construct($data){
        parent::__construct();
        if(get_class($data) === 'SimpleXMLElement') $this->parse_data_from_xml($data);
    }

    /**
    * Default XML Parsing function
    * This function is run on construct if the supplied data is of the type “SimpleXMLElement”
    *
    *    PHP’s SimpleXMLElement obejct class has several functions associated to it however we
    *    only need to take advantage of retrieving information from either a child value or an
    *    attribute value. Children elements are referenced as an object variable of their parent
    *    and attributes are obtained by using the function:
    *    [SimpleXMLElement object]->attributes()->{attribute name}
    *
    *    @params    (obj)    $data        SimpleXMLElement Object
    */
    public function parse_data_from_xml($data){
        $this->identifier        = (integer) $data->attributes()->id;
        $this->chamber            = (integer) ($data->attributes()->chamber == 'SEN') ? 1 : 2;
        $this->date                = strtotime($data->attributes()->date);
        $this->meeting_number    = (integer) $data->attributes()->meetingNumber;
        $this->committees        = (array) $data->committee;
        $this->title_en            = (string) $this->get_element_by_language('en', 'Title', $data->Status);
        $this->title_fr            = (string) $this->get_element_by_language('fr', 'Title', $data->Status);
        $this->description_en    = (string) $this->get_element_by_language('en', 'Title', $data->Description);
        $this->description_fr    = (string) $this->get_element_by_language('fr', 'Title', $data->Description);
        switch(strtolower($this->title_en)){
            case 'pre-study of commons bill':
                $this->status = 1;
                break;

            // 1st Reading
            case 'introduction and first reading':
            case 'first reading':
                $this->status = 2;
                break;

            // 2nd Reading
            case 'second reading and referral to committee':
            case 'debate at second reading':
            case 'second reading':
                $this->status = 3;
                break;

            // Committee
            case 'referral to committee':
                $this->status = 4;
                break;
            
            // Report
            case 'committee report presented':
                $this->status = 5;
                break;
            case 'debate at report stage':
                $this->status = 6;
                break;
            case 'concurrence at report stage':
                $this->status = 7;
                break;

            // 3rd reading
            case 'debate at 3rd reading':
            case 'third reading':
                $this->status = 8;
                break;
            case 'placed in the order of precedence':
                $this->status = 9;
                break;
            case 'jointly seconded by':
                $this->status = 10;
                break;
            case 'bill not proceeded with':
                $this->status = 0;
                break;
            case 'royal assent':
                $this->status = 20;
                break;
            default: $this->status = $this->title_en;
        }
    }
    
}

/**
* Federal Publication
*
*    @vars    int        $id                    Unique identifier of the specific publication
*            int        $type                Various type of the publication by type ID
*/
class federal_publication extends federal_data {

    public    $id,
            $identifier,
            $type,
            $title_en,
            $title_fr,
            $header_en,
            $header_fr,
            $recommendation_en    = '',
            $recommendation_fr    = '',
            $summary_en            = '',
            $summary_fr            = '';
            
    public function __construct($create_data = FALSE){
        parent::__construct();
        if(is_integer($create_data)){
            $this->identifier = $create_data;
            $this->parse_from_website($this->identifier);
        }
        
        if(is_object($create_data)){
            $this->parse_data_from_xml($create_data);
        }
    }

    /**
    * Default XML Parsing function
    * This function is run on construct if the supplied data is of the type “SimpleXMLElement”
    *
    *    PHP’s SimpleXMLElement obejct class has several functions associated to it however we
    *    only need to take advantage of retrieving information from either a child value or an
    *    attribute value. Children elements are referenced as an object variable of their parent
    *    and attributes are obtained by using the function:
    *    [SimpleXMLElement object]->attributes()->{attribute name}
    *
    *    @params    (obj)    $data        SimpleXMLElement Object
    */
    public function parse_data_from_xml($data){
        $this->identifier = (integer) $data->attributes()->id;
        switch($data->Title[0]){
            case 'First Reading':
                $this->type = 1;
                break;
            case 'As passed by the House of Commons':
                $this->type = 2;
                break;
            case 'As amended by committee':
                $this->type = 3;
                break;
            case 'Royal Assent':
                $this->type = 9;
                break;
            default: $this->type = 0;
        }
        $this->parse_from_website($this->identifier);
        $this->title_en = (string) $data->Title[0];
        $this->title_fr = (string) $data->Title[1];

    }
    
    public function parse_from_website($publication = FALSE){
        if(is_integer($publication)) $publication_text = $this->get_government_file('http://parl.gc.ca/HousePublications/Publication.aspx?Docid=' .  $publication. '&file=4');
        $remove = array(
            '/\<(link|meta) .*?\>/i',
            '/\<base .*?\>\<\/base\>/i',
            '/ href\=\".*?\"/i'
        );
        $publication_text = preg_replace($remove, '', $publication_text);
        $doc = new DOMDocument();
        $doc->loadHTML($publication_text);
        $xPath            = new DOMXPath($doc);

        $headers        = $xPath->query('//div[@id="publicationContent"]/table[1]/tr[6]/td/center/div');
        $summary_divs    = $xPath->query('//div[@id="publicationContent"]/table[2]/tr[1]/td/div');

        foreach($headers as $header){
            if(isset($this->header_en)) $this->header_fr = utf8_decode($header->textContent);
            else $this->header_en = utf8_decode($header->textContent);
        }
        
        $current_summary_type = FALSE;
        foreach($summary_divs as $div){
            switch(strtoupper($div->nodeValue)){
                case 'RECOMMENDATION':
                    $current_summary_type = 'recommendation_en';
                break;
                case 'SUMMARY':
                    $current_summary_type = 'summary_en';
                break;
                case 'RECOMMANDATION':
                    $current_summary_type = 'recommendation_fr';
                break;
                case 'SOMMAIRE':
                    $current_summary_type = 'summary_fr';
                break;
                default:
                    switch($current_summary_type){
                        case 'recommendation_en' : 
                            $this->recommendation_en .= "\n" . utf8_decode($div->nodeValue);
                        break;
                        case 'summary_en' : 
                            $this->summary_en .= "\n" . utf8_decode($div->nodeValue);
                        break;
                        case 'recommendation_fr' : 
                            $this->recommendation_fr .= "\n" . utf8_decode($div->nodeValue);
                        break;
                        case 'summary_fr' : 
                            $this->summary_fr .= "\n" . utf8_decode($div->nodeValue);
                        break;
                    }
            }
        }
        $this->recommendation_en    = trim($this->recommendation_en);
        $this->summary_en            = trim($this->summary_en);
        $this->recommendation_fr    = trim($this->recommendation_fr);
        $this->summary_fr            = trim($this->summary_fr);
        
    }

}

class Federal_Parser {

    public    $parliament_number,
            $session_number,
            $current_bills            = array(),
            $current_reps            = array();
            
    

    public function __construct(){
        
        // Future versions of this will grab the current session and parliament numbers from a database setting or even live from the government website.
        $this->parliament_number    = 41;
        $this->session_number        = 1;
    }
    
    public function create_daily_bills(){
        // Start by capturing the bill list
        $this->federal_bill_list = $this->get_government_file('http://parl.gc.ca/LegisInfo/Home.aspx?language=E&Parl=' . $this->parliament_number . '&Ses=' . $this->session_number . '&Mode=1&download=xml');
        $this->federal_bill_list = simplexml_load_string($this->federal_bill_list);
        $this->federal_bill_list = $this->federal_bill_list[0];
        // Capture and parse each of the bills from the bill list
        $i = 1;
        foreach($this->federal_bill_list as $bill){
            $bill = new federal_bill($bill);
            $bill->add_to_database($i);
            $i++;
        }
        
    }

    public function get_government_file($external_url){
        // Using the custom header context, capture the XML file as a string and return trimmed string value
        return trim(file_get_contents($external_url, FALSE, stream_context_create(array(
            'http' => array(
                'method'    => 'GET',
                'header'    => 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30' . "\r\n"
            )
        ))));
    }
}

$federal_parser = new Federal_Parser();
$federal_parser->create_daily_bills();
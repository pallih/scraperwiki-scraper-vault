<?php
//ebayscraper5.php => ebayscraper4.php + record contendo o memberId, Link pessoal e FeedBackLink 
//e insere em uma nova tabela.

$MyString = "";
$MyStringVendedor = "";

// Salva o record na tabela allFeedBacks.
function saveData($unique, $record){
    scraperWiki::save_sqlite(array("data_autocount", "data_Feedback","data_MemberID_AND_FeedbackScore"), $record,"allFeedBacks");
}

// Salva o record na tabela memberLinks.
function saveMembersLinks($unique, $recordLinks){
    scraperWiki::save_sqlite(array("data_MemberID"), $recordLinks,"membersLinks");
}

// Pega todos os links - paginas de usuários e paginas de seus respectivos feedbacks e insere na tabela memberLinks
function getLinks($data)
{
    $cont=1;
    foreach($data->find('div.mbg') as $elementMemberIdLink)
    {
        foreach($elementMemberIdLink->find('a') as $element)
        {
            if ($cont==1)
            {
                $MyMemberLink = $element->href;
                $MyMemberLink=  htmlspecialchars_decode($MyMemberLink);
        //        print"linkPessoal = ". $MyMemberLink . " ** ";
                
                foreach($elementMemberIdLink->find('span.mbg-nw') as $elementMemberId)
                {
                    $MyMemberId = $elementMemberId->plaintext;
          //          print "myMemberId = " . $MyMemberId . " ** ";
                }
                $cont--;
            }
            else
            {
                $MyFeedbackLink = $element->href;
                $MyFeedbackLink=  htmlspecialchars_decode($MyFeedbackLink);
          //      print "myFeedbackLink = " . $MyFeedbackLink . "\n ";
                $cont+=1;
            }
        }
        $recordLinks = array(
                        'data_MemberID' => $MyMemberId,
                        'data_MemberLink' => $MyMemberLink,
                        'data_FeedbackLink' => $MyFeedbackLink
                    );
                // Salva o record na tabela.
                saveMembersLinks(array("data_MemberID"), $recordLinks);
    }
  
}

// Coloca o memberId no link pra pagina.
function avaliaVendedor($memberId)
{
    global $MyString, $MyStringVendedor;
    $MyStringVendedor = $memberId;
    $MyString ="http://feedback.ebay.com/ws/eBayISAPI.dll?ViewFeedback2&userid=". $MyStringVendedor . "&ftab=AllFeedback";
}

// Passeia por todas as paginas de feedback daquele vendedor
function proxPaginaVendedor($dom)
{
    global $MyString;
    foreach($dom->find("b.pg-rp")as $nextPage)
    {
        foreach($nextPage->find('a') as $element)
        {
          $MyString = $element->href;
          $MyString =  htmlspecialchars_decode($MyString);
  //         print "Próxima página: " . $MyString . "\n";
        }  
    }
}

//************************programa principal************************//

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();


//*Pegar os memberId dos avaliadores pelo sql e passar para a função*//
avaliaVendedor("blowitoutahere");

print "MyString = " . $MyString . "\n";

//limitando em percorrer 3 páginas
for ($pag=0; $pag<3; $pag++)
{
    $html = scraperWiki::scrape($MyString);
    $dom->load($html);
    foreach($dom->find("table.FbOuterYukon") as $data)
    {
        $tds = $data->find("td");
         for ($i=4; $i<=197; $i+= 8)
         {
            $record = array(
                    'data_autocount' =>$i,
                    'data_Feedback' => $tds[$i+1]->plaintext,
                    'data_MemberID_AND_FeedbackScore' => $tds[$i+2]->plaintext,
                    'data_Date-Time' => $tds[$i+3]->plaintext,
                    'data_Item_Weight_Price_ItemNumber' => $tds[$i+5]->plaintext,
                    'data_Price' => $tds[$i+6]->plaintext,
            );
           
            // Salva o record na tabela // Salvar o $MyStringVendedor também.
            saveData(array("Data_autocount","data_Feedback","data_MemberID_AND_FeedbackScore"), $record);
        }
        getLinks($data);
    }
    proxPaginaVendedor($dom);
}
       
print_r(scraperwiki::show_tables());
print_r(scraperwiki::sqliteexecute("select * from membersLinks"));
//print_r(scraperwiki::sqliteexecute("select * from allFeedBacks"));
?>
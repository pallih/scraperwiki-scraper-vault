ScraperWiki.httpresponseheader('Content-Type','application/javascript')

#<script src="https://views.scraperwiki.com/run/rna_2/"></script>

print <<EOF
function loadhidden(){
  $("#page_inner").append('<div style="display: block;" id="omghax"></div>');
}

function loadscraper(scrapername,callback){
//  $(".about_this_scraper a").remove();
  $.get("https://scraperwiki.com/scrapers/"+scrapername+"/",function(html){
    $("#omghax").append('<div class="'+scrapername+'"></div>');
    var descriptiontable=html.split('<table class="about" cellspacing="0" cellpadding="0">')[1].split('</tbody></table>')[0];
    $("#omghax ."+scrapername).html('<table>'+descriptiontable+'</table>');
    callback();
  });
}

function editdescription(scrapername,callback){
  $.get("https://scraperwiki.com/scrapers/"+scrapername+"/raw_about_markup/?id=divAboutScraper",function(textile){
/*
    $.post("/views/"+scrapername+"/admin",{
      id:"divAboutScraper"
    , short_name:scrapername
    , value:"<script></script>"+textile
    });
*/
    if ("<script"!=textile.slice(0,7)){
      loadscraper(scrapername,function(){
        $("#omghax .about_this_scraper a").click();
        $("#divAboutScraper textarea").text("<script></script>"+textile);
      });
    }
  });

}

function loadauth(){
  $.get("https://scraperwiki.com/admin/auth/user/",function(html){
    $("#omghax").append('<div class="admin-users"></div>')
    //$("#omghax .admin-users").html(html);
    //document.write(html);
    //alert($("#result_list", $(html)).html());
    $("#result_list", $(html)).find('tr').each(function(){
      alert(  $( $(this).find('td')[2]  ).text()  );
    });
  });
}

//Works
//loadhidden();
loadauth();

//Doesn't
//loadscraper('dbgetpy_example');
//editdescription('dr_foster_hospital_guide_mortality_ratios');
EOF
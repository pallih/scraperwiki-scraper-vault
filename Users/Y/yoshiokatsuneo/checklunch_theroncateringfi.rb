# Blank Ruby


require 'open-uri'
require 'kconv'
require 'json'

body = open('http://www.theroncatering.fi/rlahti.txt', 'r:ISO8859-1:UTF-8').read;
lines = body.split(/\r?\n/);
week_number = 0;
lines.grep(/^LOUNASLISTA VIIKOLLE (\d+)/){|line|
        week_number = $1.to_i;
}

if(! week_number) then
        print "ERROR: no week number\n";
        exit 1
end

price=0
lines.grep(/^BUFFETLOUNAS (\d+),(\d+)/){|line|
        price = "#{$1}.#{$2}".to_f
}

weekday = 0;
content=""
f_menu=false
lines.each{|line|
        line.tr!("\r","");
        line.gsub!(/\s*$/,"");
        if (line =~ /^\S+:$/) then
                weekday +=1
                content=""
                f_menu=true
        elsif (line =~ /^$/) then
                if(f_menu && content != "") then
                        date = Date.commercial(Time.now.year, week_number, weekday);
                        menutext = content.encode('UTF-8')
                        doc_item = {
                                "date" => date,
                                "title" => menutext,
                                "price" => price
                        }
                        ScraperWiki::save_sqlite(['date','title'], doc_item)

                        content=""
                        f_menu=false
                end
        else
                content += (line + "\n");
        end
}



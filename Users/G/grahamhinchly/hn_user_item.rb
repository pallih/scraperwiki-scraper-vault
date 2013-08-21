require 'nokogiri'
require 'open-uri'

#get existing_ids from existing database if it exists
begin
ScraperWiki::attach("hn_user_item")
  existing_ids = ScraperWiki::select(
      "id from hn_user_item.swdata"
  )
rescue
  existing_ids = []
end

#get array of usernames that we want 
#target_users = ['llambda', 'gnyman', 'andrewmunsell', 'travisneotyler', 'petenixey', 'irq', 'bradgessler', 'asto' , 'dag11', 'iProject']
target_users = ['iProject']
ids = []
user_names = []
data = []
existing_ids_array = []
TIME_AGO_REGEX = /(?:\w+\W+){2}(?=ago)/



#put array of id hashes into array of just ids
existing_ids.each do |id_obj| 
   existing_ids_array << id_obj["id"]
end

target_users.each do |name|   
    full_url = 'http://news.ycombinator.com/submitted?id=' + name
    # Get a Nokogiri::HTML:Document 
    doc = Nokogiri::HTML(open(full_url))
    
    #some posts have multiple titles which screws up array indexing, only take first
    titles = doc.css('td.title a:first')
    scores = doc.css('td.subtext span')
    attrs = doc.css('td.subtext a')
    posted = doc.css('td.subtext').text.scan(TIME_AGO_REGEX)

    attrs.each_with_index do |item,index|
        #td.subtext a gives both user and id, e.g. user?id=avolcano
        #Nokogiri returns as string split with newlines, so put into array
        #split into attribute type and value
        split_attr = item['href'].split("=")
        case split_attr[0]
        when "user?id"
            user_names << split_attr[1]
        when "item?id"
            ids << split_attr[1]
        end
    end
            

    titles.zip(scores, user_names, ids, posted).each do |title, score, user_name, id, posted|
        #only put in if item id doesn't currently exist
        unless existing_ids_array.include?(id) 
          #"more" link shows up as a title, just check other attributes not nil
          unless title.nil? || user_name.nil? || id.nil? || score.nil? || posted.nil? 
            data = {
                id: id,
                user_name: user_name,
                #still need to extract .content from Nokogiri
                title: title.content,
                link: title['href'],
                score: score.content,  
                posted: posted + 'ago'          
            }
            ScraperWiki::save_sqlite(['id'], data)        
          end
        end
    end
    
end



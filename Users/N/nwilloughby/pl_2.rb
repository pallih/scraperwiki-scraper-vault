#TODO
# > Speedfix - Stop team being updated on each player run
# > Look into footytube.com/openfooty/
require 'json'

PLAYER_LIMIT = 643
def self.scrape(urls)
 urls.each do |player_url|  
   begin
     json = ScraperWiki::scrape(player_url) 
 
     parsed = JSON.parse(json) 
    
     #Scrape Player Data
     ScraperWiki::save_sqlite(
      unique_keys = [:id], 
      data = {
        :id => parsed["id"],
        :first_name => parsed["first_name"],
        :second_name => parsed["second_name"],
        :start_cost => parsed["original_cost"] / 10.00,
        :min_cost => parsed["min_cost"] / 10.00,
        :max_cost =>parsed["max_cost"] / 10.00,
        :current_cost => parsed["now_cost"] / 10.00,
        :position_text => parsed["type_name"],
        :position_id => parsed["element_type_id"],
        :team_id => parsed["team_id"],
        :ppg => parsed["points_per_game"],
        :tp => parsed["total_points"],
        :form => parsed["form"],
        :status => parsed["status"],
        :news => parsed["news"],
        :news_last_updated => parsed["news_added"],
        :dream_team => parsed["in_dreamteam"],
        :player_image=> parsed["photo_mobile_url"],
        :shirt_image => parsed["shirt_image_url"],
        :last_opponent => parsed["current_fixture"],
        :next_opponent => parsed["next_fixture"],
        :selected_by => parsed["selected_by"],
        :appearances => 0,
        :goals_scored => 0,
        :assists => 0,
        :avg_playing_time => 0       
       },table_name="players", verbose=2)
  

      # Scrape History
      @appearances = parsed["fixture_history"]["all"].count
      @goals_scored = 0
      @assists = 0
      @playing_time = 0

      parsed["fixture_history"]["all"].each_with_index do |h,i|
         @goals_scored += h[4]
         @assists += h[5]
         @playing_time += h[3]

         ScraperWiki::save_sqlite(
          unique_keys = [:game_week,:player_id],
          data = {
            :game_week => h[1],
            :player_id => parsed["id"],
            :date => h[0],
            :opp => h[2],            
            :mins_played => h[3],
            :goals_scored => @goals_scored,
            :assists => @assists,
            :clean_sheets => h[6],
            :goals_conceded => h[7],
            :own_goals => h[8],
            :pens_saved => h[9],
            :pens_missed => h[10],
            :yellow_cards => h[11],
            :red_cards => h[12],
            :saves => h[13],
            :bonus => h[14],
            :ea_ppi=> h[15],
            :value=> h[17] / 10.00,
            :points=> h[18],
          },table_name="player_history")

          #Calc Current Average Point Score
          
          if i >= 3
            
            av = 0
            goals = 0 
            assists = 0
            (0..3).each do |x|
              history = parsed["fixture_history"]["all"][i-x]
              av += history[18]
              goals += history[4]
              assists += history[5]
            end            
            
            ScraperWiki::save_sqlite(
             unique_keys = [:game_week,:player_id],
             data = {
               :game_week => h[1],
               :player_id => parsed["id"],
               :last_4_form => av / 4.00,
               :last_4_goals => goals / 4.00,
               :last_4_assists => assists/ 4.00
             },table_name="player_form")
          end
      end

 
      #Player Performance
      ScraperWiki::sqliteexecute("update players SET 
        appearances = ?,
        goals_scored = ?,
        avg_playing_time = ?,
        assists = ?
              
      WHERE id = ?",[        
        @appearances,
        @goals_scored,
        @playing_time / @appearances,
        @assists,                
        parsed["id"]
      ])

      
      # Scrape Team
      ScraperWiki::save_sqlite(
      unique_keys = [:id], 
      data = {
        :id => parsed["team_id"],
        :name => parsed["team_name"]      
      },table_name="teams", verbose=2)


  rescue Exception => e  
    puts "Something borked #{player_url}"
    puts e.message  
    puts e.backtrace.inspect 
  end
 end

end

def self.scrape_urls
   @urls = []
   
   (1..PLAYER_LIMIT ).each do |id|
     url = "http://fantasy.premierleague.com/web/api/elements/#{id}/"
     @urls << url   
   end

   return @urls
end


urls = scrape_urls
scrape (urls)




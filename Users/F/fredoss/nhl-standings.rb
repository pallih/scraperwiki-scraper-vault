require 'open-uri';
require 'nokogiri';
require 'date';

class NHLScraper
  TEAMS = [
    'Chicago Blackhawks', 'Columbus Blue Jackets', 'Detroit Red Wings',
    'Nashville Predators', 'St. Louis Blues', 'Calgary Flames', 'Colorado Avalanche', 
    'Edmonton Oilers', 'Minnesota Wild', 'Vancouver Canucks', 'Anaheim Ducks', 
    'Dallas Stars', 'Los Angeles Kings', 'Phoenix Coyotes', 'San Jose Sharks', 
    'New Jersey Devils', 'New York Islanders', 'New York Rangers', 'Philadelphia Flyers', 
    'Pittsburgh Penguins', 'Boston Bruins', 'Buffalo Sabres', 'Montreal Canadiens', 
    'Ottawa Senators', 'Toronto Maple Leafs', 'Carolina Hurricanes', 'Florida Panthers', 
    'Tampa Bay Lightning', 'Washington Capitals', 'Winnipeg Jets']

  CONFERENCES_AND_DIVISIONS = {
    'ATL' => :eastern,
    'NE' => :eastern,
    'SE' => :eastern,
    'SEN' => :western,
    'PAC' => :western,
    'NW' => :western
  }

  # SCHEDULE_URL = 'http://www.nhl.com/ice/schedulebyseason.htm'
  STANDINGS_URL = 'http://www.nhl.com/ice/standings.htm?type=lea'

  def initialize(lazy = false)
    # @schedule_document = Nokogiri(open(SCHEDULE_URL).read)
    @standings_document = Nokogiri(open(STANDINGS_URL).read)

    # @schedule_document = Nokogiri(File.open('../test/11-03-2013-schedule.html'))
    @standings_document = Nokogiri(File.open('http://phsr.biz/11-03-2013-standings.html'))

    # @lazy = lazy

    unless @lazy
      @standings = scrape_standings
      @divisions = scrape_divisions
      scrape_all_games
    end
  end

  def all_games
    if @all_games.nil? 
      scrape_all_games
    end

    return @all_games
  end

  def future_games
    @future_games ||= scrape_future_games    
  end

  def completed_games
    @completed_games ||= scrape_completed_games    
  end

  def standings
    @standings ||= scrape_standings
  end

  def divisions
    @divisions || scrape_divisions
  end

  def scrape_all_games
    @future_games = scrape_future_games
    @completed_games = scrape_completed_games
    @all_games = @completed_games + @future_games
  end

  def scrape_future_games
    future_games_table = @schedule_document.search('table.data.schedTbl').first.search('tbody/tr')
    return future_games_table.map { |row| extract_date_and_teams(row)}
  end

  def scrape_completed_games
    completed_games_table = @schedule_document.search('table.data.schedTbl').last.search('tbody/tr')
    return completed_games_table.map do |row|
      result_matches = row.at('td.tvInfo').inner_text.delete("\n").match('FINAL: \w+\((\d)\) - \w+ \((\d)\)(?:(.+))?')

      home_team_score, away_team_score = result_matches[2].to_i, result_matches[1].to_i
      
      if result_matches[3].nil? 
        winning_team_points, losing_team_points = 2, 0
        game_type = :regular
      else
        winning_team_points, losing_team_points = 2, 1
        game_type = (result_matches[3] == 'OT' ? :overtime : :shootout)
      end

      if home_team_score > away_team_score
        home_team_points, away_team_points = winning_team_points, losing_team_points
      else
        home_team_points, away_team_points = losing_team_points, winning_team_points
      end

      extract_date_and_teams(row).merge({
        home_team_score: home_team_score,
        away_team_score: away_team_score,
        home_team_points: home_team_points,
        away_team_points: away_team_points,
        game_type: game_type
        })
    end
  end

  def scrape_standings
    return @standings_document.at('table.standings/tbody').search('tr').map do |row|
      columns = row.search('td')
      division_text = columns[2].inner_text.strip

      {
        team: columns[1].inner_text.strip,
        division: division_text.downcase.to_sym,
        conference: CONFERENCES_AND_DIVISIONS[division_text],
        points: columns[7].inner_text.strip.to_i
      }
    end
  end

  def scrape_divisions
    @divisions = {}
    
    @standings_document.at('table.standings/tbody').search('tr').each do |row|
      columns = row.search('td')
      team = columns[1].search('a').last.inner_text.strip
      division = columns[2].inner_text.strip.to_sym

      @divisions[team] = division
    end

    return @divisions
  end

  protected
    def extract_date_and_teams(row)
      home_team = row.search('td.team').last.at('div.teamName').inner_text
      away_team = row.search('td.team').first.at('div.teamName').inner_text

      {
          date: Date.parse(row.at('td.date/div.skedStartDateSite').inner_text),
          home_team: home_team,
          away_team: away_team,
          home_team_division: @divisions[home_team],
          away_team_division: @divisions[away_team]
      }      
    end
end
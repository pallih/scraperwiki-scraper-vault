require 'nokogiri'           
url = "http://www.bbcgoodfood.com/content/local/seasonal/table/all/"
MONTH_KEYS = %w(jan feb mar apr may jun jul aug sep oct nov dec).map(&:to_sym)

def first_month_in_season(seasonality)
  0.upto(12) do |i|
    if seasonality[MONTH_KEYS[i]] == :in_season && seasonality[MONTH_KEYS[i-1]] != :in_season
      return MONTH_KEYS[i]
    end
  end
  nil
end

def last_month_in_season(seasonality)
  0.upto(12) do |i|
    if seasonality[MONTH_KEYS[i]] == :in_season && seasonality[MONTH_KEYS[i+1]] != :in_season
      return MONTH_KEYS[i]
    end
  end
  nil
end

def first_month_out_of_season(seasonality)
  0.upto(12) do |i|
    if seasonality[MONTH_KEYS[i]] != :in_season && seasonality[MONTH_KEYS[i-1]] == :in_season
      return MONTH_KEYS[i]
    end
  end
  nil
end

def seasonality_additions(seasonality)
  {
    comes_into_season: first_month_in_season(seasonality),
    last_month_in_season: last_month_in_season(seasonality),
    out_of_season: first_month_out_of_season(seasonality)
  }
end

html = ScraperWiki::scrape(url)
doc = Nokogiri::HTML html
data = doc.search("table[@summary='Seasonal availability'] tbody tr").inject([]) do |d, row|
  thing = row.search('th a')[0]
  if thing
    name = thing.text.strip
    url = thing.attr('href')
    if name != "Jan"
      month_cells = row.search('td')
      months = MONTH_KEYS.inject({}) { |h, m| h[m] = nil; h }
      seasonality = month_cells.inject(months) do |months, cell|
        if cell.attr('headers')
          month = cell.attr('headers').split.last.to_sym
          if img = cell.search('img')[0]
            if img.attr('src') =~ /circle/
              months[month] = :coming
            else
              months[month] = :in_season
            end
          end
        end
        months
      end
      d << {name: name, url: url}.merge(seasonality).merge(seasonality_additions(seasonality))
    end
  end
  d
end

p data.to_json

ScraperWiki::save_sqlite(['name'], data)
require 'nokogiri'           
url = "http://www.bbcgoodfood.com/content/local/seasonal/table/all/"
MONTH_KEYS = %w(jan feb mar apr may jun jul aug sep oct nov dec).map(&:to_sym)

def first_month_in_season(seasonality)
  0.upto(12) do |i|
    if seasonality[MONTH_KEYS[i]] == :in_season && seasonality[MONTH_KEYS[i-1]] != :in_season
      return MONTH_KEYS[i]
    end
  end
  nil
end

def last_month_in_season(seasonality)
  0.upto(12) do |i|
    if seasonality[MONTH_KEYS[i]] == :in_season && seasonality[MONTH_KEYS[i+1]] != :in_season
      return MONTH_KEYS[i]
    end
  end
  nil
end

def first_month_out_of_season(seasonality)
  0.upto(12) do |i|
    if seasonality[MONTH_KEYS[i]] != :in_season && seasonality[MONTH_KEYS[i-1]] == :in_season
      return MONTH_KEYS[i]
    end
  end
  nil
end

def seasonality_additions(seasonality)
  {
    comes_into_season: first_month_in_season(seasonality),
    last_month_in_season: last_month_in_season(seasonality),
    out_of_season: first_month_out_of_season(seasonality)
  }
end

html = ScraperWiki::scrape(url)
doc = Nokogiri::HTML html
data = doc.search("table[@summary='Seasonal availability'] tbody tr").inject([]) do |d, row|
  thing = row.search('th a')[0]
  if thing
    name = thing.text.strip
    url = thing.attr('href')
    if name != "Jan"
      month_cells = row.search('td')
      months = MONTH_KEYS.inject({}) { |h, m| h[m] = nil; h }
      seasonality = month_cells.inject(months) do |months, cell|
        if cell.attr('headers')
          month = cell.attr('headers').split.last.to_sym
          if img = cell.search('img')[0]
            if img.attr('src') =~ /circle/
              months[month] = :coming
            else
              months[month] = :in_season
            end
          end
        end
        months
      end
      d << {name: name, url: url}.merge(seasonality).merge(seasonality_additions(seasonality))
    end
  end
  d
end

p data.to_json

ScraperWiki::save_sqlite(['name'], data)

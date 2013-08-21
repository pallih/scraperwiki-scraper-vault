require 'date'
require 'erb'
sourcescraper = 'https://scraperwiki.com/scrapers/poets_dob/'

class PopulationStats

  attr_reader :frequency, :percent, :population_size
  def initialize(population, field)
    @population = population
    @frequency = calc_frequency(field)
    @population_size = calc_population_size
    @percent = calc_percent

  end

  def calc_frequency(field)
    frequency = Hash.new(0)
    @population.each do |person|
      begin
        mob = Date::MONTHNAMES[Date.parse(person[field]).month]
        frequency[mob] += 1
      rescue
      end
    end
    frequency
  end

  def calc_percent
    percent = {}
    @frequency.each do |variable, freq|
      percent[variable] = 1.0 * freq / @population_size * 100
    end
    percent
  end

  def calc_population_size
    population_size = 0
    @frequency.each {|term, freq| population_size += freq}
    population_size
  end

end

MONTH_NAMES = Date::MONTHNAMES[1..12]

def sort_stats(stats)
  MONTH_NAMES.collect do |month|
    [month, stats[month]]    
  end
end


PAGE_TEMPLATE = "
      <!--Load the AJAX API-->
    <script type='text/javascript' src='https://www.google.com/jsapi'></script>
    <script type='text/javascript'>
    
      // Load the Visualization API and the piechart package.
      google.load('visualization', '1.0', {'packages':['corechart']});
      
      // Set a callback to run when the Google Visualization API is loaded.
      google.setOnLoadCallback(drawChart);
      
      // Callback that creates and populates a data table, 
      // instantiates the pie chart, passes in the data and
      // draws it.
      function drawChart() {

        // Create the data table.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Month');
        data.addColumn('number', 'Percentage');
        data.addRows([
% population_percent.each do |stat|
          ['<%= stat[0].capitalize %>', <%= stat[1] %>],
% end
        ]);

        // Set chart options
        var options = {'title':'Months of Birth for Poets',
                       'width':700,
                       'height':500};


        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>

    <h2>The Distribution of Months of Birth Among Notable Poets</h2>

    <div>
      This was obtained by scraping wikipedia&#039;s 
      <a href='http://en.wikipedia.org/wiki/List_of_poets'>List of poets</a>.
      Then the page of each person listed was scraped to see when they were born.
    </div>

    <!--Div that will hold the pie chart-->
    <div id='chart_div'></div>

    <table>
      <tr>
        <th style='text-align: left;'>Month of Birth</th>
        <th style='text-align: left; padding-right: 1em;'>Frequency</th>
        <th style='text-align: left; padding-right: 1em;'>Percent</th>
      </tr>
% term_index = 0
% population_freq.each do |stat|
      <tr>
        <td style='padding-right: 1em;'><%= stat[0].capitalize %></td>
        <td><%= stat[1] %></td>
        <td><%= sprintf('%.2f', population_percent[term_index][1]) %></td>
      </tr>
% term_index += 1
%end
    </table>

    <div style='padding-top: 1em;'>
      <strong>Sample Size:</strong> <%= population_size %>
    </div>
"

ScraperWiki.attach("poets_dob") 

data = ScraperWiki.select(           
  "dob from poets_dob.swdata"
)

popStats = PopulationStats.new(data, 'dob')
population_freq = sort_stats(popStats.frequency)
population_percent = sort_stats(popStats.percent)
population_size = popStats.population_size

puts ERB.new(PAGE_TEMPLATE, 0, '%').result(binding)


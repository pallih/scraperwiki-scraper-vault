require 'nokogiri'
require 'open-uri'

root = "http://fantacalcio.repubblica.it/index.php?page=calciatori&ruolo="

cats = { 'P' => 'portiere', 'D' => 'difensore', 'A' => 'attaccante', 'C' => 'centrocampista' }

str2int = proc { |i| i.to_i }
fields = [
  [:nome,              proc { |i| i.strip.split.map(&:capitalize).join(' ') }],
  [:squadra,           proc { |i| i.strip.capitalize }],
  [:valore,            str2int],
  [:presenze,          str2int],
  [:rigori_parati,     str2int],
  [:rigori_sbagliati,  str2int],
  [:gol,               str2int],
  [:ammonizioni,       str2int],
  [:espulsioni,        str2int]
]

id_inc = 0

cats.each_pair do |cat, name|
  html = Nokogiri::HTML.parse(open(root + cat))
  rows = html.css('table.red tbody tr')

  rows.each do |row|
    player = {}

    row.css('td').each_with_index.map do |child, i|
      puts child.text
      player[fields[i][0]] = fields[i][1].call(child.text)
    end

    player[:tipo] = name

    if cat == 'P'
      player[:subiti] = player[:gol]
      player.delete :gol
    end

    player[:id] = id_inc

    ScraperWiki.save(['id',], player)
    id_inc += 1
  end
end
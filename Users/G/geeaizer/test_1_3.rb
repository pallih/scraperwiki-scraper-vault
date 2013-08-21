html = ScraperWiki.scrape("http://www.amazon.com/best-sellers-movies-TV-DVD-Blu-ray/zgbs/movies-tv/ref=pd_ts_zgc_mov_movies-tv_morl?pf_rd_p=1326658342&pf_rd_s=right-4&pf_rd_t=101&pf_rd_i=2625373011&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=0FQ5NXJMNQJ0F3PJ6RAD")

puts html

require 'nokogiri' #HTML parser

doc = Nokogiri::HTML(html)
for v in doc.search("div[id='centerColInner'] div[class='zg_item_normal']")
  cells = v.search("div[class='zg_itemRightDiv_normal']")
  data = {
    'Rank' => ("span[class='zg_rankNumber']").inner_html.to_i
   # 'Title' => cells[4].inner_html,
   # 'Stars' => cells[4].inner_html,
    #'Format' => cells[4].inner_html,
    #'List Price' => cells[4].inner_html,
   # 'Price' => cells[4].inner_html

  }
  puts data.to_json
end

ScraperWiki.save_sqlite(unique_keys=['Rank'], data=data)
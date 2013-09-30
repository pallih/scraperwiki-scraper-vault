require "csv"
$ic = Iconv.new("UTF-8", "CP437")

# vestigingen PO
data = ScraperWiki.scrape("http://www.cijfers.minocw.nl/EtalageBestand.aspx?Bestandsnaam=A_VESTBO&SectorCode=PO&Bestand=CSV&Actie=download")
data = $ic.iconv(data)
csv = CSV.new(data, :headers=>true, :col_sep=>";")
ScraperWiki.save_sqlite(["BRIN-VEST NR"], csv.map(&:to_hash), "vestigingen_po")

# vestigingen VO
data = ScraperWiki.scrape("http://www.cijfers.minocw.nl/EtalageBestand.aspx?Bestandsnaam=A_VESTVO&SectorCode=VO&Bestand=CSV&Actie=download")
data = $ic.iconv(data)
csv = CSV.new(data, :headers=>true, :col_sep=>";")
ScraperWiki.save_sqlite(["BRIN-VESTNR"], csv.map(&:to_hash), "vestigingen_vo")

require "csv"
$ic = Iconv.new("UTF-8", "CP437")

# vestigingen PO
data = ScraperWiki.scrape("http://www.cijfers.minocw.nl/EtalageBestand.aspx?Bestandsnaam=A_VESTBO&SectorCode=PO&Bestand=CSV&Actie=download")
data = $ic.iconv(data)
csv = CSV.new(data, :headers=>true, :col_sep=>";")
ScraperWiki.save_sqlite(["BRIN-VEST NR"], csv.map(&:to_hash), "vestigingen_po")

# vestigingen VO
data = ScraperWiki.scrape("http://www.cijfers.minocw.nl/EtalageBestand.aspx?Bestandsnaam=A_VESTVO&SectorCode=VO&Bestand=CSV&Actie=download")
data = $ic.iconv(data)
csv = CSV.new(data, :headers=>true, :col_sep=>";")
ScraperWiki.save_sqlite(["BRIN-VESTNR"], csv.map(&:to_hash), "vestigingen_vo")


#################################################################
# Extract information from a PDF file
#################################################################
# This scraper uses the pdf-reader gem.
# Documentation is at https://github.com/yob/pdf-reader#readme
# If you have problems you can ask for help at http://groups.google.com/group/pdf-reader
require 'pdf-reader'   
require 'open-uri'

def write_data(year,idProv,id,nombre,distrito,seccion,lmesas,local,direccion,cp) 
  puts "idMuni: #{id}, nombre: #{nombre}"
  puts "distrito: #{distrito}, seccion: #{seccion}, mesas: #{lmesas}"
  puts "local: #{local}"
  puts "direccion: #{direccion}, codigo postal: #{cp}"
  mesas = lmesas.split(" ")
  mesas.each do |m|
    data = {year: year,
            idProv: idProv,
            id: id,
            nombre: nombre,
            distrito: distrito,
            seccion: seccion,
            mesa: m,
            local: local,
            direccion: direccion,
            codigo_postal: cp}
    ScraperWiki::save_sqlite(['year','id','distrito','seccion','mesa'], data,table_name="MesasElectoralesGalicia")
  end
end

#Coruña
#io = open('http://bop.dicoruna.es/bopportal/publicado/2012/09/03/2012_0000010887.pdf')
#idProv = 15
#Lugo
#io = open('http://www.deputacionlugo.org/portal_localweb_ag/RecursosWeb/DOCUMENTOS/1/0_7055_1.pdf')
#idProv = 27
#Ourense 2 columns PDF not detected correctly
#io = open('http://dl.dropbox.com/u/19188751/Mesas/MesasOurense2012.pdf')
#idProv = 32
#Pontevedra
io = open('http://www.bop.depo.es/bop.PONTEVEDRA/2012/bop.PONTEVEDRA.20120904.170.pdf')
idProv = 36

reader = PDF::Reader.new(io)

inside_info_item = false 
year = 2012
idMuni,nomMuni,distrito,seccion,mesas,local,direccion,cp = nil
reader.pages.each do |page|
    lines = page.text.lines.to_a
    lines.each do |line|
      l = line.strip
      if l.match(/^MUNICIPIO:/)
        if inside_info_item 
          puts "LOG ERROR"
        else
          inside_info_item = true
        end
        l =~ /^MUNICIPIO:\s*(\d{3})\s*(.*)$/
        idMuni = idProv*1000 + $1.to_i 
        nomMuni = $2
        next
      end
      if inside_info_item
        case
        when l.match(/^DISTRITO\.*:/)
          l =~ /^DISTRITO\.*:\s*(\d{2}).*SECCION\.*:\s*(\d{3}).*MESA\/S\.*:\s*(.*)$/
          distrito = $1.to_i
          seccion = $2.to_i
          mesas = $3
        when l.match(/^LOCAL ELECTORAL:/)
          l =~ /^LOCAL ELECTORAL:\s*(.*)$/
          local = $1
        when l.match(/^DIRECCION:/)
          l =~ /^DIRECCION:(.*)(\d{5})$/
          direccion = $1
          cp = $2
          if $1.nil? 
            l =~ /^DIRECCION:(.*)$/
            direccion = $1
          end
          if cp
            write_data(year,idProv,idMuni,nomMuni,distrito,seccion,mesas,local,direccion,cp)
            idMuni,nomMuni,distrito,seccion,mesas,local,direccion,cp = nil
            inside_info_item = false
          end
        when l.match(/^\d{5}$/)
          l =~ /^(\d{5})$/
          cp = $1
          if cp
            write_data(year,idProv,idMuni,nomMuni,distrito,seccion,mesas,local,direccion,cp)
            idMuni,nomMuni,distrito,seccion,mesas,local,direccion,cp = nil
            inside_info_item = false
          end
        end
      end
    end
end

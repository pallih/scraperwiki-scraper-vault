# Blank Ruby
require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'builder'



a1 = {:texts=>"WA6265", :dimensions=>{:A=>"245,00", :B=>"169,00", :C=>"0,00", :D=>"0,00", :E=>"0,00", :F=>"0,00", :G=>"0,00", :H=>"61,00"}, :using=>{:byPassValve=>"No", :antiDrainValve=>"No", :antiSyphonValve=>"No", :installationGuide=>"None", :applications=>"Fiat Brava, Bravo, Marea, Marengo TD75, TD100"}, :pictures=>"http://wixeurope.com/Content/images/filters/Filtron/WA6265.jpg", :brand=>" ALFA ROMEO ", :model=>"145", :engine=>{:engine_name=>"1.4i 16V Twin Spark", :cc=>"1370", :no=>"AR33503", :hp=>"103"}}

a2 = {:texts=>"WL7083", :dimensions=>{:A=>"75,00", :B=>"69,50", :C=>"61,50", :D=>"0,00", :E=>"0,00", :F=>"0,00", :G=>"M 20x1,5", :H=>"76,00"}, :using=>{:byPassValve=>"Yes", :antiDrainValve=>"Yes", :antiSyphonValve=>"No", :installationGuide=>"None", :applications=>"Alfa Romeo 145, 146, 156, 166, Coupe 1/97->;  Lancia Delta 1.8i 16V 1/96->"}, :pictures=>"http://wixeurope.com/Content/images/filters/Filtron/L14.jpg", :brand=>" ALFA ROMEO ", :model=>"145", :engine=>{:engine_name=>"1.4i 16V Twin Spark", :cc=>"1370", :no=>"AR33503", :hp=>"103"}}

a = [a1,a2]

output = ""

xml = Builder::XmlMarkup.new(:target => output, :ident => 2)

xml.instruct!
a.each do |item|
  xml.item do
    xml.texts item[:texts]
    dimensions = item[:dimensions]
    xml.dimensions do
      xml.A dimensions[:A]
      xml.B dimensions[:B]
      xml.C dimensions[:C]
      xml.D dimensions[:D]
      xml.E dimensions[:E]
      xml.F dimensions[:F]
      xml.G dimensions[:G]
      xml.H dimensions[:H]
    end
    using = item[:using]
    xml.using do
      xml.byPassValve using[:byPassValve]
      xml.antiDrainValve using[:antiDrainValve]
      xml.antiSyphonValve using[:antiSyphonValve]
      xml.installationGuide using[:installationGuide]
      xml.applications using[:applications]
    end
    xml.pictures item[:pictures]
    xml.brand item[:brand]
    xml.model item[:model]
    engine = item[:engine]
    xml.engine do
      xml.engine_name engine[:engine_name]
      xml.cc engine[:cc]
      xml.no engine[:no]
      xml.hp engine[:hp]
    end
  end
end

o = File.new("test_noko.xml", "w")
o.write(output)
o.close

puts output# Blank Ruby
require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'builder'



a1 = {:texts=>"WA6265", :dimensions=>{:A=>"245,00", :B=>"169,00", :C=>"0,00", :D=>"0,00", :E=>"0,00", :F=>"0,00", :G=>"0,00", :H=>"61,00"}, :using=>{:byPassValve=>"No", :antiDrainValve=>"No", :antiSyphonValve=>"No", :installationGuide=>"None", :applications=>"Fiat Brava, Bravo, Marea, Marengo TD75, TD100"}, :pictures=>"http://wixeurope.com/Content/images/filters/Filtron/WA6265.jpg", :brand=>" ALFA ROMEO ", :model=>"145", :engine=>{:engine_name=>"1.4i 16V Twin Spark", :cc=>"1370", :no=>"AR33503", :hp=>"103"}}

a2 = {:texts=>"WL7083", :dimensions=>{:A=>"75,00", :B=>"69,50", :C=>"61,50", :D=>"0,00", :E=>"0,00", :F=>"0,00", :G=>"M 20x1,5", :H=>"76,00"}, :using=>{:byPassValve=>"Yes", :antiDrainValve=>"Yes", :antiSyphonValve=>"No", :installationGuide=>"None", :applications=>"Alfa Romeo 145, 146, 156, 166, Coupe 1/97->;  Lancia Delta 1.8i 16V 1/96->"}, :pictures=>"http://wixeurope.com/Content/images/filters/Filtron/L14.jpg", :brand=>" ALFA ROMEO ", :model=>"145", :engine=>{:engine_name=>"1.4i 16V Twin Spark", :cc=>"1370", :no=>"AR33503", :hp=>"103"}}

a = [a1,a2]

output = ""

xml = Builder::XmlMarkup.new(:target => output, :ident => 2)

xml.instruct!
a.each do |item|
  xml.item do
    xml.texts item[:texts]
    dimensions = item[:dimensions]
    xml.dimensions do
      xml.A dimensions[:A]
      xml.B dimensions[:B]
      xml.C dimensions[:C]
      xml.D dimensions[:D]
      xml.E dimensions[:E]
      xml.F dimensions[:F]
      xml.G dimensions[:G]
      xml.H dimensions[:H]
    end
    using = item[:using]
    xml.using do
      xml.byPassValve using[:byPassValve]
      xml.antiDrainValve using[:antiDrainValve]
      xml.antiSyphonValve using[:antiSyphonValve]
      xml.installationGuide using[:installationGuide]
      xml.applications using[:applications]
    end
    xml.pictures item[:pictures]
    xml.brand item[:brand]
    xml.model item[:model]
    engine = item[:engine]
    xml.engine do
      xml.engine_name engine[:engine_name]
      xml.cc engine[:cc]
      xml.no engine[:no]
      xml.hp engine[:hp]
    end
  end
end

o = File.new("test_noko.xml", "w")
o.write(output)
o.close

puts output
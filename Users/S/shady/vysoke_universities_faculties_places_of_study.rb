#encoding: utf-8

require 'rubygems'
require 'nokogiri'
require 'open-uri'

url = 'http://www.portalvs.sk/sk/informacie-o-vysokych-skolach'
html = Nokogiri::HTML(open(url))

type = ['verejna', 'sukromna', 'statna']
t = 0
id = 1
@id_fak = 1
@id_pla = 1

class Nokogiri::XML::Element
  def parse_degrees(degrees)
    stupne = self.text.split('. stupe')
    key = '0'
    stupne.each do |stupen|
      if key != '0'
        degrees[key] = stupen.sub(/\s+\d/, "").sub(/\s$/, "").sub(/^\W\s/, "")
      end
      if stupen.include? '1'
        key = '1'
      elsif stupen.include? '2'
        key = '2'
      elsif stupen.include? '3'
        key = '3'
      else
        key = '0'
      end
    end
    return degrees
  end

=begin
  def get_students(students)
        pole = ["denni", "externi", "vsetci"]
        i = 0
        self.search('strong').each do |count|
          if /(\d)/ =~ count
            students[pole[i]] = count.content
            i+=1
          end
        end
        return students
  end
=end
end


def parse_fakulta(fakulta_url, fakulta_text, school, type)
  fakulta = Nokogiri::HTML(open(fakulta_url))
#  students = Hash.new
  degrees = Hash.new
  dekan =""
  address = ""
  fakulta.search('div.rc2').each do |rc2|

    dekan = rc2.text.split('Aktu')[0].split('Dekan: ')[1]

    if rc2.text.include? "Zobrazi"
      address = rc2.text.split('Zobra')[0]
    else
      if rc2.inner_html.include? 'img class="right"'
        right = rc2.inner_html.split('alt="">')[1]
      else
        right = rc2.inner_html
      end
      address_array = right.split('<br>')
      address = address_array[0].concat(address_array[1])
    end

#    students = rc2.get_students(students)
  end

  fakulta.search('div.rc1').each do |rc1|
    degrees = rc1.parse_degrees(degrees)
  end

      data = {
        :id => @id_fak,
        :school => school,
        :type => type,
        :fakulta => fakulta_text,
        :degree1 => degrees['1'],
        :degree2 => degrees['2'],
        :degree3 => degrees['3'],
        :dekan => dekan,
        :address => address
# according to my information, count of students is not true
#        :students_denni => students["denni"],
#        :students_extern => students["externi"],
#        :students_all => students["vsetci"]
      }
      ScraperWiki.save_sqlite(unique_keys=[:id], data=data, table_name='faculties')
      @id_fak += 1
end

def parse_place(place_url, place_text, school, type)
  place = Nokogiri::HTML(open(place_url))
  degrees = Hash.new
  address = ""
  place.search('div.rc2').each do |rc2|
    if rc2.text.include? "Zobrazi"
      address = rc2.text.split('Zobra')[0]
    else
      if rc2.inner_html.include? 'img class="right"'
        right = rc2.inner_html.split('alt="">')[1]
      else
        right = rc2.inner_html
      end
      address_array = right.split('<br>')
      address = address_array[0].concat(address_array[1])
    end
  end

  place.search('div.rc1').each do |rc1|
    degrees = rc1.parse_degrees(degrees)
  end

      data = {
        :id => @id_pla,
        :school => school,
        :type => type,
        :place => place_text,
        :degree1 => degrees['1'],
        :degree2 => degrees['2'],
        :degree3 => degrees['3'],
        :address => address
      }
      ScraperWiki.save_sqlite(unique_keys=[:id], data=data, table_name='places')
      @id_pla += 1
end

html.at('div#right-column').search('ul').each do |ul|
  ul.search('a').each do |a|
    if a.search('img').empty? 
      school = a.text
      skola_url = 'http://www.portalvs.sk/'+a.attr('href')

      skola = Nokogiri::HTML(open(skola_url))
      degrees = Hash.new
      fakulty = ""
      study_places = ""
      rektor = ""
      creation_date = ""
      address = ""
#      students = Hash.new
      content = ""
      last_change = ""

      skola.search('div.rc1').each do |rc1|
        if rc1.text.include? '. stupe'
          degrees = rc1.parse_degrees(degrees)
        end
        rc1.search('ul').each do |ul|

          if ul.inner_html.include? 'sk/fakulta'
            ul.search('li a').each do |a|
              fakulta_url = "http://www.portalvs.sk/"+a.attr('href')
              parse_fakulta(fakulta_url, a.text, school, type[t])
#              id_fak += 1
              fakulty.concat(a.text+"\n")
            end
            fakulty.strip!


            elsif ul.inner_html.include? 'sk/miesto-studia'
            ul.search('li a').each do |a|
              place_url = "http://www.portalvs.sk/"+a.attr('href')
              parse_place(place_url, a.text, school, type[t])
#              id_pla += 1
              study_places.concat(a.text+"\n") 
            end
            study_places.strip!
          end

        end
      end
      skola.search('div.rc2').each do |rc2|
        rektor = rc2.text.split('Aktu')[0].split('Rektor: ')[1]


        if rc2.text.include? "Zobrazi"
          if /(\d{2}\.\d{2}\.\d{4})/ =~ rc2.text.split('Zobra')[0].split('koly:')[1] then
            creation_date = $1
            address = rc2.text.split('Zobra')[0].split('koly:')[1].sub /(\d{2}\.\d{2}\.\d{4})/, ""
          else
            address = rc2.text.split('Zobra')[0]
          end
        else
          if /(\d{2}\.\d{2}\.\d{4})/ =~ rc2.text.split('+')[0].split('koly:')[1] then
            creation_date = $1
            address = rc2.text.split('+')[0].split('koly:')[1].sub(/(\d{2}\.\d{2}\.\d{4})/, "").split(/(\d{3}\/\d{4})/)[0].split(/(\d{4} )/)[0]
          end
        end

#        students = rc2.get_students(students)

      end

      skola.search('p').each do |p|
        if p.text.include? "Zodpovednos"
          array = p.text.split(":", 3)
          content =  array[1].split("Posledn")[0].strip.gsub(/(^\s+)/, "")
          last_change = array[2].gsub(/(^\s+)/, "")
        end
      end

      data = {
        :id => id,
        :school => school,
        :type => type[t],
        :fakulty => fakulty,
        :study_places => study_places,
        :degree1 => degrees['1'],
        :degree2 => degrees['2'],
        :degree3 => degrees['3'],
        :rektor => rektor,
        :creation_date => creation_date,
        :address => address,
# according to my information, count of students is not true
#        :students_denni => students["denni"],
#        :students_extern => students["externi"],
#        :students_all => students["vsetci"],
        :content => content,
        :last_change => last_change
      }
      ScraperWiki.save_sqlite(unique_keys=[:id], data=data, table_name='schools')
      id += 1
    end
  end
  t+=1
end

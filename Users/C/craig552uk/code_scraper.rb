# Blank Ruby

require 'open-uri'

URL="https://www.pcspecialist.co.uk/includes/promo_code.php?promo_code="

('A'..'Z').each do |a|
  ('A'..'Z').each do |b|
    ('A'..'Z').each do |c|
      (0..9).each do |d|
        (0..9).each do |e|
          puts URL+a+b+c+d.to_s+e.to_s
        end
      end
    end
  end
end
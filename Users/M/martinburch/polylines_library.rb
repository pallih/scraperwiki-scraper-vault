# https://github.com/joshuaclayton/polylines

module Polylines
  class Base
    attr_reader :current_value, :negative

    def initialize(current_value)
      @current_value = current_value
    end

    def step_2
      @negative = current_value < 0 if encoding?

      encode! { (current_value * 1e5).round }
      decode! { current_value.to_f / 1e5 }
    end

    def step_3
      return unless negative
      encode! { ~(current_value * -1) + 1 }
      decode! { ~(current_value - 1) * -1 }
    end

    def step_4
      encode! { current_value << 1 }
      decode! { current_value >> 1 }
    end

    def step_5
      return unless negative
      encode! { ~current_value }
      decode! { ~current_value }
    end

    def step_6
      encode! do
        [].tap do |numbers|
          while current_value > 0 do
            numbers.unshift(current_value & 0x1f)
            @current_value >>= 5
          end

          numbers << 0 if numbers.empty? 
        end
      end

      decode! do
        current_value.map {|chunk| "%05b" % chunk }.join.tap do |val|
          @negative = val[-1, 1] == "1"
        end.to_i(2)
      end
    end

    def step_7
      encode! { current_value.reverse }
      decode! { current_value.reverse }
    end

    def step_8
      encode! { current_value[0..-2].map {|item| item | 0x20 } << current_value.last }
      decode! { current_value[0..-2].map {|item| item ^ 0x20 } << current_value.last }
    end

    def step_10
      encode! { current_value.map {|value| value + 63 } }
      decode! { current_value.map {|value| value - 63 } }
    end

    def step_11
      encode! { current_value.map(&:chr).join }
      decode! { current_value.split(//).map {|char| char.unpack("U").first } }
    end

    def encode!
      if encoding?
        @current_value = yield
      end
    end

    def decode!
      if decoding?
        @current_value = yield
      end
    end

    def encoding?
      self.is_a?(Polylines::Encoder)
    end

    def decoding?
      self.is_a?(Polylines::Decoder)
    end

    def self.transform_to_array_of_lat_lng_and_deltas(value)
      if self == Polylines::Encoder
        delta_latitude, delta_longitude = 0, 0

        return value.inject([]) do |polyline, (latitude, longitude)|
          polyline << latitude - delta_latitude
          polyline << longitude - delta_longitude
          delta_latitude, delta_longitude = latitude, longitude
          polyline
        end
      end

      if self == Polylines::Decoder
        set = []
        return value.split(//).inject([]) do |charset, char|
          set << char

          if ((char.unpack("U").first - 63) & 0x20).zero? 
            charset << set.join
            set = []
          end

          charset
        end.map {|charset| decode(charset) }
      end
    end
  end
end

## Decoder class

module Polylines
  class Decoder < Base
    def self.decode_polyline(polyline)
      points_with_deltas = transform_to_array_of_lat_lng_and_deltas(polyline)

      [].tap do |points|
        points << [points_with_deltas.shift, points_with_deltas.shift]

        while points_with_deltas.any? 
          points << [
            points.last[0] + points_with_deltas.shift,
            points.last[1] + points_with_deltas.shift
          ]
        end
      end
    end

    def self.decode(string)
      self.new(string).tap do |decoding|
        decoding.step_11
        decoding.step_10
        decoding.step_8
        decoding.step_7
        decoding.step_6
        decoding.step_5
        decoding.step_4
        decoding.step_3
        decoding.step_2
      end.current_value
    end
  end
end

module Polylines
  class Encoder < Base
    def self.encode_points(points)
      points_with_deltas = transform_to_array_of_lat_lng_and_deltas(points)
      points_with_deltas.map {|point| encode(point) }.join
    end

    def self.encode(number)
      self.new(number).tap do |encoding|
        encoding.step_2
        encoding.step_3
        encoding.step_4
        encoding.step_5
        encoding.step_6
        encoding.step_7
        encoding.step_8
        encoding.step_10
        encoding.step_11
      end.current_value
    end
  end
end

# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

require "date"
require "open-uri"
require "stringio"


module Vcard
  # Split on \r\n or \n to get the lines, unfold continued lines (they
  # start with " " or \t), and return the array of unfolded lines.
  #
  # This also supports the (invalid) encoding convention of allowing empty
  # lines to be inserted for readability - it does this by dropping zero-length
  # lines.
  def self.unfold(card) #:nodoc:
      unfolded = []

      card.lines do |line|
        line.chomp!
        # If it's a continuation line, add it to the last.
        # If it's an empty line, drop it from the input.
        if( line =~ /^[ \t]/ )
          unfolded[-1] << line[1, line.size-1]
        elsif( line =~ /^$/ )
        else
          unfolded << line
        end
      end

      unfolded
  end

  # Convert a +sep+-seperated list of values into an array of values.
  def self.decode_list(value, sep = ",") # :nodoc:
    list = []

    value.split(sep).each do |item|
      item.chomp!(sep)
      list << yield(item)
    end
    list
  end

  # Convert a RFC 2425 date into an array of [year, month, day].
  def self.decode_date(v) # :nodoc:
    unless v =~ %r{^\s*#{Bnf::DATE}\s*$}
      raise ::Vcard::InvalidEncodingError, "date not valid (#{v})"
    end
    [$1.to_i, $2.to_i, $3.to_i]
  end

  # Convert a RFC 2425 date into a Date object.
  def self.decode_date_to_date(v)
    Date.new(*decode_date(v))
  end

  # Note in the following the RFC2425 allows yyyy-mm-ddThh:mm:ss, but RFC2445
  # does not. I choose to encode to the subset that is valid for both.

  # Encode a Date object as "yyyymmdd".
  def self.encode_date(d) # :nodoc:
     "%0.4d%0.2d%0.2d" % [ d.year, d.mon, d.day ]
  end

  # Encode a Date object as "yyyymmdd".
  def self.encode_time(d) # :nodoc:
     "%0.4d%0.2d%0.2d" % [ d.year, d.mon, d.day ]
  end

  # Encode a Time or DateTime object as "yyyymmddThhmmss"
  def self.encode_date_time(d) # :nodoc:
     "%0.4d%0.2d%0.2dT%0.2d%0.2d%0.2d" % [ d.year, d.mon, d.day, d.hour, d.min, d.sec ]
  end

  # Convert a RFC 2425 time into an array of [hour,min,sec,secfrac,timezone]
  def self.decode_time(v) # :nodoc:
    unless match = %r{^\s*#{Bnf::TIME}\s*$}.match(v)
      raise ::Vcard::InvalidEncodingError, "time '#{v}' not valid"
    end
    hour, min, sec, secfrac, tz = match.to_a[1..5]

    [hour.to_i, min.to_i, sec.to_i, secfrac ? secfrac.to_f : 0, tz]
  end

  def self.array_datetime_to_time(dtarray) #:nodoc:
    # We get [ year, month, day, hour, min, sec, usec, tz ]
    begin
      tz = (dtarray.pop == "Z") ? :gm : :local
      Time.send(tz, *dtarray)
    rescue ArgumentError => e
      raise ::Vcard::InvalidEncodingError, "#{tz} #{e} (#{dtarray.join(', ')})"
    end
  end

  # Convert a RFC 2425 time into an array of Time objects.
  def self.decode_time_to_time(v) # :nodoc:
    array_datetime_to_time(decode_date_time(v))
  end

  # Convert a RFC 2425 date-time into an array of [year,mon,day,hour,min,sec,secfrac,timezone]
  def self.decode_date_time(v) # :nodoc:
    unless match = %r{^\s*#{Bnf::DATE}T#{Bnf::TIME}\s*$}.match(v)
      raise ::Vcard::InvalidEncodingError, "date-time '#{v}' not valid"
    end
    year, month, day, hour, min, sec, secfrac, tz = match.to_a[1..8]

    [
      # date
      year.to_i, month.to_i, day.to_i,
      # time
      hour.to_i, min.to_i, sec.to_i, secfrac ? secfrac.to_f : 0, tz
    ]
  end

  def self.decode_date_time_to_datetime(v) #:nodoc:
    year, month, day, hour, min, sec = decode_date_time(v)
    # TODO - DateTime understands timezones, so we could decode tz and use it.
    DateTime.civil(year, month, day, hour, min, sec, 0)
  end

  # decode_boolean
  #
  # float
  #
  # float_list

  # Convert an RFC2425 INTEGER value into an Integer
  def self.decode_integer(v) # :nodoc:
    unless %r{\s*#{Bnf::INTEGER}\s*}.match(v)
      raise ::Vcard::InvalidEncodingError, "integer not valid (#{v})"
    end
    v.to_i
  end

  #
  # integer_list

  # Convert a RFC2425 date-list into an array of dates.
  def self.decode_date_list(v) # :nodoc:
    decode_list(v) do |date|
      date.strip!
      if date.length > 0
        decode_date(date)
      end
    end.compact
  end

  # Convert a RFC 2425 time-list into an array of times.
  def self.decode_time_list(v) # :nodoc:
    decode_list(v) do |time|
      time.strip!
      if time.length > 0
        decode_time(time)
      end
    end.compact
  end

  # Convert a RFC 2425 date-time-list into an array of date-times.
  def self.decode_date_time_list(v) # :nodoc:
    decode_list(v) do |datetime|
      datetime.strip!
      if datetime.length > 0
        decode_date_time(datetime)
      end
    end.compact
  end

  # Convert RFC 2425 text into a String.
  # \\ -> \
  # \n -> NL
  # \N -> NL
  # \, -> ,
  # \; -> ;
  #
  # I've seen double-quote escaped by iCal.app. Hmm. Ok, if you aren't supposed
  # to escape anything but the above, everything else is ambiguous, so I'll
  # just support it.
  def self.decode_text(v) # :nodoc:
    # FIXME - I think this should trim leading and trailing space
    v.gsub(/\\(.)/) do
      case $1
      when "n", "N"
        "\n"
      else
        $1
      end
    end
  end

  def self.encode_text(v) #:nodoc:
    v.to_str.gsub(/([\\,;\n])/) { $1 == "\n" ? "\\n" : "\\"+$1 }
  end

  # v is an Array of String, or just a single String
  def self.encode_text_list(v, sep = ",") #:nodoc:
    begin
      v.to_ary.map{ |t| encode_text(t) }.join(sep)
    rescue
      encode_text(v)
    end
  end

  # Convert a +sep+-seperated list of TEXT values into an array of values.
  def self.decode_text_list(value, sep = ",") # :nodoc:
    # Need to do in two stages, as best I can find.
    list = value.scan(/([^#{sep}\\]*(?:\\.[^#{sep}\\]*)*)#{sep}/).map do |v|
      decode_text(v.first)
    end
    if value.match(/([^#{sep}\\]*(?:\\.[^#{sep}\\]*)*)$/)
      list << $1
    end
    list
  end

  # param-value = paramtext / quoted-string
  # paramtext  = *SAFE-CHAR
  # quoted-string      = DQUOTE *QSAFE-CHAR DQUOTE
  def self.encode_paramtext(value)
    case value
    when %r{\A#{Bnf::SAFECHAR}*\z}
      value
    else
      raise ::Vcard::Unencodable, "paramtext #{value.inspect}"
    end
  end

  def self.encode_paramvalue(value)
    case value
    when %r{\A#{Bnf::SAFECHAR}*\z}
      value
    when %r{\A#{Bnf::QSAFECHAR}*\z}
      '"' + value + '"'
    else
      raise ::Vcard::Unencodable, "param-value #{value.inspect}"
    end
  end


  # Unfold the lines in +card+, then return an array of one Field object per
  # line.
  def self.decode(card) #:nodoc:
    unfold(card).collect { |line| DirectoryInfo::Field.decode(line) }
  end


  # Expand an array of fields into its syntactic entities. Each entity is a sequence
  # of fields where the sequences is delimited by a BEGIN/END field. Since
  # BEGIN/END delimited entities can be nested, we build a tree. Each entry in
  # the array is either a Field or an array of entries (where each entry is
  # either a Field, or an array of entries...).
  def self.expand(src) #:nodoc:
    # output array to expand the src to
    dst = []
    # stack used to track our nesting level, as we see begin/end we start a
    # new/finish the current entity, and push/pop that entity from the stack
    current = [ dst ]

    for f in src
      if f.name? "BEGIN"
        e = [ f ]

        current.last.push(e)
        current.push(e)

      elsif f.name? "END"
        current.last.push(f)

        unless current.last.first.value? current.last.last.value
          raise "BEGIN/END mismatch (#{current.last.first.value} != #{current.last.last.value})"
        end

        current.pop

      else
        current.last.push(f)
      end
    end

    dst
  end

  # Split an array into an array of all the fields at the outer level, and
  # an array of all the inner arrays of fields. Return the array [outer,
  # inner].
  def self.outer_inner(fields) #:nodoc:
    # TODO - use Enumerable#partition
    # seperate into the outer-level fields, and the arrays of component
    # fields
    outer = []
    inner = []
    fields.each do |line|
      case line
      when Array; inner << line
      else;       outer << line
      end
    end
    return outer, inner
  end
end


# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

module Vcard

  # Attachments are used by both iCalendar and vCard. They are either a URI or
  # inline data, and their decoded value will be either a Uri or a Inline, as
  # appropriate.
  #
  # Besides the methods specific to their class, both kinds of object implement
  # a set of common methods, allowing them to be treated uniformly:
  # - Uri#to_io, Inline#to_io: return an IO from which the value can be read.
  # - Uri#to_s, Inline#to_s: return the value as a String.
  # - Uri#format, Inline#format: the format of the value. This is supposed to
  #   be an "iana defined" identifier (like "image/jpeg"), but could be almost
  #   anything (or nothing) in practice.  Since the parameter is optional, it may
  #   be "".
  #
  # The objects can also be distinguished by their class, if necessary.
  module Attachment

    # TODO - It might be possible to autodetect the format from the first few
    # bytes of the value, and return the appropriate MIME type when format
    # isn't defined.
    #
    # iCalendar and vCard put the format in different parameters, and the
    # default kind of value is different.
    def Attachment.decode(field, defkind, fmtparam) #:nodoc:
      format = field.pvalue(fmtparam) || ""
      kind = field.kind || defkind
      case kind
      when "text"
        Inline.new(::Vcard.decode_text(field.value), format)
      when "uri"
        Uri.new(field.value_raw, format)
      when "binary"
        Inline.new(field.value, format)
      else
        raise InvalidEncodingError, "Attachment of type #{kind} is not allowed"
      end
    end

    # Extends a String to support some of the same methods as Uri.
    class Inline < String
      def initialize(s, format) #:nodoc:
        @format = format
        super(s)
      end

      # Return an IO object for the inline data. See +stringio+ for more
      # information.
      def to_io
        StringIO.new(self)
      end

      # The format of the inline data.
      # See Attachment.
      attr_reader :format
    end

    # Encapsulates a URI and implements some methods of String.
    class Uri
      def initialize(uri, format) #:nodoc:
        @uri = uri
        @format = format
      end

      # The URI value.
      attr_reader :uri

      # The format of the data referred to by the URI.
      # See Attachment.
      attr_reader :format

      # Return an IO object from opening the URI.  See +open-uri+ for more
      # information.
      def to_io
        open(@uri)
      end

      # Return the String from reading the IO object to end-of-data.
      def to_s
        to_io.read(nil)
      end

      def inspect #:nodoc:
        s = "<#{self.class.to_s}: #{uri.inspect}>"
        s << ", #{@format.inspect}" if @format
        s
      end
    end

  end
end

# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

module Vcard
  # Contains regular expression strings for the EBNF of RFC 2425.
  module Bnf #:nodoc:

    # 1*(ALPHA / DIGIT / "-")
    # Note: I think I can add A-Z here, and get rid of the "i" matches elsewhere.
    # Note: added "_" to allowed because its produced by Notes  (X-LOTUS-CHILD_UID:)
    # Note: added "/" to allowed because its produced by KAddressBook (X-messaging/xmpp-All:)
    # Note: added " " to allowed because its produced by highrisehq.com (X-GOOGLE TALK:)
    NAME    = "[-a-z0-9_/][-a-z0-9_/ ]*"

    # <"> <Any character except CTLs, DQUOTE> <">
    QSTR    = '"([^"]*)"'

    # *<Any character except CTLs, DQUOTE, ";", ":", ",">
    PTEXT   = '([^";:,]+)'

    # param-value = ptext / quoted-string
    PVALUE  = "(?:#{QSTR}|#{PTEXT})"

    # param = name "=" param-value *("," param-value)
    # Note: v2.1 allows a type or encoding param-value to appear without the type=
    # or the encoding=. This is hideous, but we try and support it, if there
    # is no "=", then $2 will be "", and we will treat it as a v2.1 param.
    PARAM = ";(#{NAME})(=?)((?:#{PVALUE})?(?:,#{PVALUE})*)"

    # V3.0: contentline  =   [group "."]  name *(";" param) ":" value
    # V2.1: contentline  = *( group "." ) name *(";" param) ":" value
    #
    # We accept the V2.1 syntax for backwards compatibility.
    #LINE = "((?:#{NAME}\\.)*)?(#{NAME})([^:]*)\:(.*)"
    LINE = "^((?:#{NAME}\\.)*)?(#{NAME})((?:#{PARAM})*):(.*)$"

    # date = date-fullyear ["-"] date-month ["-"] date-mday
    # date-fullyear = 4 DIGIT
    # date-month = 2 DIGIT
    # date-mday = 2 DIGIT
    DATE = "(\d\d\d\d)-?(\d\d)-?(\d\d)"

    # time = time-hour [":"] time-minute [":"] time-second [time-secfrac] [time-zone]
    # time-hour = 2 DIGIT
    # time-minute = 2 DIGIT
    # time-second = 2 DIGIT
    # time-secfrac = "," 1*DIGIT
    # time-zone = "Z" / time-numzone
    # time-numzone = sign time-hour [":"] time-minute
    TIME = "(\d\d):?(\d\d):?(\d\d)(\.\d+)?(Z|[-+]\d\d:?\d\d)?"

    # integer = (["+"] / "-") 1*DIGIT
    INTEGER = "[-+]?\d+"

    # QSAFE-CHAR = WSP / %x21 / %x23-7E / NON-US-ASCII
    #  ; Any character except CTLs and DQUOTE
    QSAFECHAR = "[ \t\x21\x23-\x7e\x80-\xff]"

    # SAFE-CHAR  = WSP / %x21 / %x23-2B / %x2D-39 / %x3C-7E / NON-US-ASCII
    #   ; Any character except CTLs, DQUOTE, ";", ":", ","
    SAFECHAR = "[ \t\x21\x23-\x2b\x2d-\x39\x3c-\x7e\x80-\xff]"
  end
end

# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

module Vcard
  # An RFC 2425 directory info object.
  #
  # A directory information object is a sequence of fields. The basic
  # structure of the object, and the way in which it is broken into fields
  # is common to all profiles of the directory info type.
  #
  # A vCard, for example, is a specialization of a directory info object.
  #
  # - [RFC2425] the directory information framework (ftp://ftp.ietf.org/rfc/rfc2425.txt)
  #
  # Here's an example of encoding a simple vCard using the low-level APIs:
  #
  #   card = Vcard::Vcard.create
  #   card << Vcard::DirectoryInfo::Field.create("EMAIL", "user.name@example.com", "TYPE" => "INTERNET" )
  #   card << Vcard::DirectoryInfo::Field.create("URL", "http://www.example.com/user" )
  #   card << Vcard::DirectoryInfo::Field.create("FN", "User Name" )
  #   puts card.to_s
  #
  # Don't do it like that, use Vcard::Vcard::Maker.
  class DirectoryInfo
    include Enumerable

    private_class_method :new

    # Initialize a DirectoryInfo object from +fields+. If +profile+ is
    # specified, check the BEGIN/END fields.
    def initialize(fields, profile = nil) #:nodoc:
      if fields.detect { |f| ! f.kind_of? DirectoryInfo::Field }
        raise ArgumentError, "fields must be an array of DirectoryInfo::Field objects"
      end

      @string = nil # this is used as a flag to indicate that recoding will be necessary
      @fields = fields

      check_begin_end(profile) if profile
    end

    # Decode +card+ into a DirectoryInfo object.
    #
    # +card+ may either be a something that is convertible to a string using
    # #to_str or an Array of objects that can be joined into a string using
    # #join("\n"), or an IO object (which will be read to end-of-file).
    #
    # The lines in the string may be delimited using IETF (CRLF) or Unix (LF) conventions.
    #
    # A DirectoryInfo is mutable, you can add new fields to it, see
    # Vcard::DirectoryInfo::Field#create() for how to create a new Field.
    #
    # TODO: I don't believe this is ever used, maybe I can remove it.
    def DirectoryInfo.decode(card) #:nodoc:
      if card.respond_to? :to_str
        string = card.to_str
      elsif card.kind_of? Array
        string = card.join("\n")
      elsif card.kind_of? IO
        string = card.read(nil)
      else
        raise ArgumentError, "DirectoryInfo cannot be created from a #{card.type}"
      end

      fields = ::Vcard.decode(string)

      new(fields)
    end

    # Create a new DirectoryInfo object. The +fields+ are an optional array of
    # DirectoryInfo::Field objects to add to the new object, between the
    # BEGIN/END.  If the +profile+ string is not nil, then it is the name of
    # the directory info profile, and the BEGIN:+profile+/END:+profile+ fields
    # will be added.
    #
    # A DirectoryInfo is mutable, you can add new fields to it using #push(),
    # and see Field#create().
    def DirectoryInfo.create(fields = [], profile = nil)

      if profile
        p = profile.to_str
        f = [ Field.create("BEGIN", p) ]
        f.concat fields
        f.push Field.create("END", p)
        fields = f
      end

      new(fields, profile)
    end

    # The first field named +name+, or nil if no
    # match is found.
    def field(name)
      enum_by_name(name).each { |f| return f }
      nil
    end

    # The value of the first field named +name+, or nil if no
    # match is found.
    def [](name)
      enum_by_name(name).each { |f| return f.value if f.value != ""}
      enum_by_name(name).each { |f| return f.value }
      nil
    end

    # An array of all the values of fields named +name+, converted to text
    # (using Field#to_text()).
    #
    # TODO - call this #texts(), as in the plural?
    def text(name)
      accum = []
      each do |f|
        if f.name? name
          accum << f.to_text
        end
      end
      accum
    end

    # Array of all the Field#group()s.
    def groups
      @fields.collect { |f| f.group } .compact.uniq
    end

    # All fields, frozen.
    def fields #:nodoc:
      @fields.dup.freeze
    end

    # Yields for each Field for which +cond+.call(field) is true. The
    # (default) +cond+ of nil is considered true for all fields, so
    # this acts like a normal #each() when called with no arguments.
    def each(cond = nil) # :yields: Field
      @fields.each do |field|
         if(cond == nil || cond.call(field))
           yield field
         end
      end
      self
    end

    # Returns an Enumerator for each Field for which #name?(+name+) is true.
    #
    # An Enumerator supports all the methods of Enumerable, so it allows iteration,
    # collection, mapping, etc.
    #
    # Examples:
    #
    # Print all the nicknames in a card:
    #
    #   card.enum_by_name("NICKNAME") { |f| puts f.value }
    #
    # Print an Array of the preferred email addresses in the card:
    #
    #   pref_emails = card.enum_by_name("EMAIL").select { |f| f.pref? }
    def enum_by_name(name)
      Enumerator.new(self, Proc.new { |field| field.name?(name) })
    end

    # Returns an Enumerator for each Field for which #group?(+group+) is true.
    #
    # For example, to print all the fields, sorted by group, you could do:
    #
    #   card.groups.sort.each do |group|
    #     card.enum_by_group(group).each do |field|
    #       puts "#{group} -> #{field.name}"
    #     end
    #   end
    #
    # or to get an array of all the fields in group "AGROUP", you could do:
    #
    #   card.enum_by_group("AGROUP").to_a
    def enum_by_group(group)
      Enumerator.new(self, Proc.new { |field| field.group?(group) })
    end

    # Returns an Enumerator for each Field for which +cond+.call(field) is true.
    def enum_by_cond(cond)
      Enumerator.new(self, cond )
    end

    # Force card to be reencoded from the fields.
    def dirty #:nodoc:
      #string = nil
    end

    # Append +field+ to the fields. Note that it won't be literally appended
    # to the fields, it will be inserted before the closing END field.
    def push(field)
      dirty
      @fields[-1,0] = field
      self
    end

    alias << push

    # Push +field+ onto the fields, unless there is already a field
    # with this name.
    def push_unique(field)
      push(field) unless @fields.detect { |f| f.name? field.name }
      self
    end

    # Append +field+ to the end of all the fields. This isn't usually what you
    # want to do, usually a DirectoryInfo's first and last fields are a
    # BEGIN/END pair, see #push().
    def push_end(field)
      @fields << field
      self
    end

    # Delete +field+.
    #
    # Warning: You can't delete BEGIN: or END: fields, but other
    # profile-specific fields can be deleted, including mandatory ones. For
    # vCards in particular, in order to avoid destroying them, I suggest
    # creating a new Vcard, and copying over all the fields that you still
    # want, rather than using #delete. This is easy with Vcard::Maker#copy, see
    # the Vcard::Maker examples.
    def delete(field)
      case
      when field.name?("BEGIN"), field.name?("END")
        raise ArgumentError, "Cannot delete BEGIN or END fields."
      else
        @fields.delete field
      end

      self
    end

    # The string encoding of the DirectoryInfo. See Field#encode for information
    # about the width parameter.
    def encode(width=nil)
      unless @string
        @string = @fields.collect { |f| f.encode(width) } . join ""
      end
      @string
    end

    alias to_s encode

    # Check that the DirectoryInfo object is correctly delimited by a BEGIN
    # and END, that their profile values match, and if +profile+ is specified, that
    # they are the specified profile.
    def check_begin_end(profile=nil) #:nodoc:
      unless @fields.first
        raise "No fields to check"
      end
      unless @fields.first.name? "BEGIN"
        raise "Needs BEGIN, found: #{@fields.first.encode nil}"
      end
      unless @fields.last.name? "END"
        raise "Needs END, found: #{@fields.last.encode nil}"
      end
      unless @fields.last.value? @fields.first.value
        raise "BEGIN/END mismatch: (#{@fields.first.value} != #{@fields.last.value}"
      end
      if profile
        if ! @fields.first.value? profile
          raise "Mismatched profile"
        end
      end
      true
    end
  end
end

# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

module Vcard
  # This is a way for an object to have multiple ways of being enumerated via
  # argument to it's #each() method. An Enumerator mixes in Enumerable, so the
  # standard APIs such as Enumerable#map(), Enumerable#to_a(), and
  # Enumerable#find_all() can be used on it.
  #
  # TODO since 1.8, this is part of the standard library, I should rewrite vPim
  # so this can be removed.
  class Enumerator
    include Enumerable

    def initialize(obj, *args)
      @obj = obj
      @args = args
    end

    def each(&block)
      @obj.each(*@args, &block)
    end
  end
end

# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

module Vcard
  # Exception used to indicate that data being decoded is invalid, the message
  # should describe what is invalid.
  class InvalidEncodingError < StandardError; end

  # Exception used to indicate that data being decoded is unsupported, the message
  # should describe what is unsupported.
  #
  # If its unsupported, its likely because I didn't anticipate it being useful
  # to support this, and it likely it could be supported on request.
  class UnsupportedError < StandardError; end

  # Exception used to indicate that encoding failed, probably because the
  # object would not result in validly encoded data. The message should
  # describe what is unsupported.
  class Unencodeable < StandardError; end
end

# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify it
# under the same terms as the ruby language itself, see the file COPYING for
# details.

module Vcard

  class DirectoryInfo

    # A field in a directory info object.
    class Field
      # TODO
      # - Field should know which param values and field values are
      #   case-insensitive, configurably, so it can down case them
      # - perhaps should have pvalue_set/del/add, perhaps case-insensitive, or
      #   pvalue_iset/idel/iadd, where set sets them all, add adds if not present,
      #   and del deletes any that are present
      # - I really, really, need a case-insensitive string...
      # - should allow nil as a field value, its not the same as "", if there is
      #   more than one pvalue, the empty string will show up. This isn't strictly
      #   disallowed, but its odd. Should also strip empty strings on decoding, if
      #   I don't already.
      private_class_method :new

      def Field.create_array(fields)
        case fields
        when Hash
          fields.map do |name,value|
            DirectoryInfo::Field.create( name, value )
          end
        else
          fields.to_ary
        end
      end

      # Encode a field.
      def Field.encode0(group, name, params={}, value="") # :nodoc:
        line = ""

        # A reminder of the line format:
        #   [<group>.]<name>;<pname>=<pvalue>,<pvalue>:<value>

        if group
          line << group << "."
        end

        line << name

        params.each do |pname, pvalues|

          unless pvalues.respond_to? :to_ary
            pvalues = [ pvalues ]
          end

          line << ";" << pname << "="

          sep = "" # set to "," after one pvalue has been appended

          pvalues.each do |pvalue|
            # check if we need to do any encoding
            if pname.casecmp("ENCODING") == 0 && pvalue == :b64
              pvalue = "B" # the RFC definition of the base64 param value
              value = [ value.to_str ].pack("m").gsub("\n", "")
            end

            line << sep << pvalue
            sep =",";
          end
        end

        line << ":"

        line << Field.value_str(value)

        line
      end

      def Field.value_str(value) # :nodoc:
        line = ""
        case value
        when Date
          line << ::Vcard.encode_date(value)

        when Time #, DateTime
          line << ::Vcard.encode_date_time(value)

        when Array
          line << value.map { |v| Field.value_str(v) }.join(";")

        when Symbol
          line << value

        else
          # FIXME - somewhere along here, values with special chars need escaping...
          line << value.to_str
        end
        line
      end

      # Decode a field.
      def Field.decode0(atline) # :nodoc:
        unless atline =~ %r{#{Bnf::LINE}}i
          raise ::Vcard::InvalidEncodingError, atline
        end

        atgroup = $1.upcase
        atname = $2.upcase
        paramslist = $3
        atvalue = $~[-1]

        # I've seen space that shouldn't be there, as in "BEGIN:VCARD ", so
        # strip it. I'm not absolutely sure this is allowed... it certainly
        # breaks round-trip encoding.
        atvalue.strip!

        if atgroup.length > 0
          atgroup.chomp!(".")
        else
          atgroup = nil
        end

        atparams = {}

        # Collect the params, if any.
        if paramslist.size > 1

          # v3.0 and v2.1 params
          paramslist.scan( %r{#{Bnf::PARAM}}i ) do

            # param names are case-insensitive, and multi-valued
            name = $1.upcase
            params = $3

            # v2.1 params have no "=" sign, figure out what kind of param it
            # is (either its a known encoding, or we treat it as a "TYPE"
            # param).

            if $2 == ""
              params = $1
              case $1
              when /quoted-printable/i
                name = "ENCODING"

              when /base64/i
                name = "ENCODING"

              else
                name = "TYPE"
              end
            end

            # TODO - In ruby1.8 I can give an initial value to the atparams
            # hash values instead of this.
            unless atparams.key? name
              atparams[name] = []
            end

            params.scan( %r{#{Bnf::PVALUE}} ) do
              atparams[name] << ($1 || $2)
            end
          end
        end

        [ atgroup, atname, atparams, atvalue ]
      end

      def initialize(line) # :nodoc:
        @line = line.to_str
        @group, @name, @params, @value = Field.decode0(@line)

        @params.each do |pname,pvalues|
          pvalues.freeze
        end
        self
      end

      # Create a field by decoding +line+, a String which must already be
      # unfolded. Decoded fields are frozen, but see #copy().
      def Field.decode(line)
        new(line).freeze
      end

      # Create a field with name +name+ (a String), value +value+ (see below),
      # and optional parameters, +params+. +params+ is a hash of the parameter
      # name (a String) to either a single string or symbol, or an array of
      # strings and symbols (parameters can be multi-valued).
      #
      # If "ENCODING" => :b64 is specified as a parameter, the value will be
      # base-64 encoded. If it's already base-64 encoded, then use String
      # values ("ENCODING" => "B"), and no further encoding will be done by
      # this routine.
      #
      # Currently handled value types are:
      # - Time, encoded as a date-time value
      # - Date, encoded as a date value
      # - String, encoded directly
      # - Array of String, concatentated with ";" between them.
      #
      # TODO - need a way to encode String values as TEXT, at least optionally,
      # so as to escape special chars, etc.
      def Field.create(name, value="", params={})
        line = Field.encode0(nil, name, params, value)

        begin
          new(line)
        rescue ::Vcard::InvalidEncodingError => e
          raise ArgumentError, e.to_s
        end
      end

      # Create a copy of Field. If the original Field was frozen, this one
      # won't be.
      def copy
        Marshal.load(Marshal.dump(self))
      end

      # The String encoding of the Field. The String will be wrapped to a
      # maximum line width of +width+, where +0+ means no wrapping, and nil is
      # to accept the default wrapping (75, recommended by RFC2425).
      #
      # Note: AddressBook.app 3.0.3 neither understands to unwrap lines when it
      # imports vCards (it treats them as raw new-line characters), nor wraps
      # long lines on export. This is mostly a cosmetic problem, but wrapping
      # can be disabled by setting width to +0+, if desired.
      #
      # FIXME - breaks round-trip encoding, need to change this to not wrap
      # fields that are already wrapped.
      def encode(width=nil)
        width = 75 unless width
        l = @line
        # Wrap to width, unless width is zero.
        if width > 0
          l = l.gsub(/.{#{width},#{width}}/) { |m| m + "\n " }
        end
        # Make sure it's terminated with no more than a single NL.
        l.gsub(/\s*\z/, "") + "\n"
      end

      alias to_s encode

      # The name.
      def name
        @name
      end

      # The group, if present, or nil if not present.
      def group
        @group
      end

      # An Array of all the param names.
      def pnames
        @params.keys
      end

      # FIXME - remove my own uses of #params
      alias params pnames # :nodoc:

      # The first value of the param +name+,  nil if there is no such param,
      # the param has no value, or the first param value is zero-length.
      def pvalue(name)
        v = pvalues( name )
        if v
          v = v.first
        end
        if v
          v = nil unless v.length > 0
        end
        v
      end

      # The Array of all values of the param +name+,  nil if there is no such
      # param, [] if the param has no values. If the Field isn't frozen, the
      # Array is mutable.
      def pvalues(name)
        @params[name.upcase]
      end

      # FIXME - remove my own uses of #param
      alias param pvalues # :nodoc:

      alias [] pvalues

      # Yield once for each param, +name+ is the parameter name, +value+ is an
      # array of the parameter values.
      def each_param(&block) #:yield: name, value
        if @params
          @params.each(&block)
        end
      end

      # The decoded value.
      #
      # The encoding specified by the #encoding, if any, is stripped.
      #
      # Note: Both the RFC 2425 encoding param ("b", meaning base-64) and the
      # vCard 2.1 encoding params ("base64", "quoted-printable", "8bit", and
      # "7bit") are supported.
      #
      # FIXME:
      # - should use the VALUE parameter
      # - should also take a default value type, so it can be converted
      #   if VALUE parameter is not present.
      def value
        case encoding
        when nil, "8BIT", "7BIT" then @value

          # Hack - if the base64 lines started with 2 SPC chars, which is invalid,
          # there will be extra spaces in @value. Since no SPC chars show up in
          # b64 encodings, they can be safely stripped out before unpacking.
        when "B", "BASE64"       then @value.gsub(" ", "").unpack("m*").first

        when "QUOTED-PRINTABLE"  then @value.unpack("M*").first

        else
          raise ::Vcard::InvalidEncodingError, "unrecognized encoding (#{encoding})"
        end
      end

      # Is the #name of this Field +name+? Names are case insensitive.
      def name?(name)
        @name.casecmp(name) == 0
      end

      # Is the #group of this field +group+? Group names are case insensitive.
      # A +group+ of nil matches if the field has no group.
      def group?(group)
        @group.casecmp(group) == 0
      end

      # Is the value of this field of type +kind+? RFC2425 allows the type of
      # a fields value to be encoded in the VALUE parameter. Don't rely on its
      # presence, they aren't required, and usually aren't bothered with. In
      # cases where the kind of value might vary (an iCalendar DTSTART can be
      # either a date or a date-time, for example), you are more likely to see
      # the kind of value specified explicitly.
      #
      # The value types defined by RFC 2425 are:
      # - uri:
      # - text:
      # - date: a list of 1 or more dates
      # - time: a list of 1 or more times
      # - date-time: a list of 1 or more date-times
      # - integer:
      # - boolean:
      # - float:
      def kind?(kind)
        self.kind.casecmp(kind) == 0
      end

      # Is one of the values of the TYPE parameter of this field +type+? The
      # type parameter values are case insensitive. False if there is no TYPE
      # parameter.
      #
      # TYPE parameters are used for general categories, such as
      # distinguishing between an email address used at home or at work.
      def type?(type)
        type = type.to_str

        types = param("TYPE")

        if types
          types = types.detect { |t| t.casecmp(type) == 0 }
        end
      end

      # Is this field marked as preferred? A vCard field is preferred if
      # #type?("PREF"). This method is not necessarily meaningful for
      # non-vCard profiles.
      def pref?
        type? "PREF"
      end

      # Set whether a field is marked as preferred. See #pref?
      def pref=(ispref)
        if ispref
          pvalue_iadd("TYPE", "PREF")
        else
          pvalue_idel("TYPE", "PREF")
        end
      end

      # Is the value of this field +value+? The check is case insensitive.
      # FIXME - it shouldn't be insensitive, make a #casevalue? method.
      def value?(value)
        @value.casecmp(value) == 0
      end

      # The value of the ENCODING parameter, if present, or nil if not
      # present.
      def encoding
        e = param("ENCODING")

        if e
          if e.length > 1
            raise ::Vcard::InvalidEncodingError, "multi-valued param 'ENCODING' (#{e})"
          end
          e = e.first.upcase
        end
        e
      end

      # The type of the value, as specified by the VALUE parameter, nil if
      # unspecified.
      def kind
        v = param("VALUE")
        if v
          if v.size > 1
            raise InvalidEncodingError, "multi-valued param 'VALUE' (#{values})"
          end
          v = v.first.downcase
        end
        v
      end

      # The value as an array of Time objects (all times and dates in
      # RFC2425 are lists, even where it might not make sense, such as a
      # birthday). The time will be UTC if marked as so (with a timezone of
      # "Z"), and in localtime otherwise.
      #
      # TODO - support timezone offsets
      #
      # TODO - if year is before 1970, this won't work... but some people
      # are generating calendars saying Canada Day started in 1753!
      # That's just wrong! So, what to do? I add a message
      # saying what the year is that breaks, so they at least know that
      # its ridiculous! I think I need my own DateTime variant.
      def to_time
        begin
          ::Vcard.decode_date_time_list(value).collect do |d|
            # We get [ year, month, day, hour, min, sec, usec, tz ]
            begin
              if(d.pop == "Z")
                Time.gm(*d)
              else
                Time.local(*d)
              end
            rescue ArgumentError => e
              raise ::Vcard::InvalidEncodingError, "Time.gm(#{d.join(', ')}) failed with #{e.message}"
            end
          end
        rescue ::Vcard::InvalidEncodingError
          ::Vcard.decode_date_list(value).collect do |d|
            # We get [ year, month, day ]
            begin
              Time.gm(*d)
            rescue ArgumentError => e
              raise ::Vcard::InvalidEncodingError, "Time.gm(#{d.join(', ')}) failed with #{e.message}"
            end
          end
        end
      end

      # The value as an array of Date objects (all times and dates in
      # RFC2425 are lists, even where it might not make sense, such as a
      # birthday).
      #
      # The field value may be a list of either DATE or DATE-TIME values,
      # decoding is tried first as a DATE-TIME, then as a DATE, if neither
      # works an InvalidEncodingError will be raised.
      def to_date
        begin
          ::Vcard.decode_date_time_list(value).collect do |d|
            # We get [ year, month, day, hour, min, sec, usec, tz ]
            Date.new(d[0], d[1], d[2])
          end
        rescue ::Vcard::InvalidEncodingError
          ::Vcard.decode_date_list(value).collect do |d|
            # We get [ year, month, day ]
            Date.new(*d)
          end
        end
      end

      # The value as text. Text can have escaped newlines, commas, and escape
      # characters, this method will strip them, if present.
      #
      # In theory, #value could also do this, but it would need to know that
      # the value is of type "TEXT", and often for text values the "VALUE"
      # parameter is not present, so knowledge of the expected type of the
      # field is required from the decoder.
      def to_text
        ::Vcard.decode_text(value)
      end

      # The undecoded value, see +value+.
      def value_raw
        @value
      end

      # TODO def pretty_print() ...

      # Set the group of this field to +group+.
      def group=(group)
        mutate(group, @name, @params, @value)
        group
      end

      # Set the value of this field to +value+.  Valid values are as in
      # Field.create().
      def value=(value)
        mutate(@group, @name, @params, value)
        value
      end

      # Convert +value+ to text, then assign.
      #
      # TODO - unimplemented
      def text=(text)
      end

      # Set a the param +pname+'s value to +pvalue+, replacing any value it
      # currently has. See Field.create() for a description of +pvalue+.
      #
      # Example:
      #  if field["TYPE"]
      #    field["TYPE"] << "HOME"
      #  else
      #    field["TYPE"] = [ "HOME" ]
      #  end
      #
      # TODO - this could be an alias to #pvalue_set
      def []=(pname,pvalue)
        unless pvalue.respond_to?(:to_ary)
          pvalue = [ pvalue ]
        end

        h = @params.dup

        h[pname.upcase] = pvalue

        mutate(@group, @name, h, @value)
        pvalue
      end

      # Add +pvalue+ to the param +pname+'s value. The values are treated as a
      # set so duplicate values won't occur, and String values are case
      # insensitive.  See Field.create() for a description of +pvalue+.
      def pvalue_iadd(pname, pvalue)
        pname = pname.upcase

        # Get a uniq set, where strings are compared case-insensitively.
        values = [ pvalue, @params[pname] ].flatten.compact
        values = values.collect do |v|
          if v.respond_to? :to_str
            v = v.to_str.upcase
          end
          v
        end
        values.uniq!

        h = @params.dup

        h[pname] = values

        mutate(@group, @name, h, @value)
        values
      end

      # Delete +pvalue+ from the param +pname+'s value. The values are treated
      # as a set so duplicate values won't occur, and String values are case
      # insensitive.  +pvalue+ must be a single String or Symbol.
      def pvalue_idel(pname, pvalue)
        pname = pname.upcase
        if pvalue.respond_to? :to_str
          pvalue = pvalue.to_str.downcase
        end

        # Get a uniq set, where strings are compared case-insensitively.
        values = [ nil, @params[pname] ].flatten.compact
        values = values.collect do |v|
          if v.respond_to? :to_str
            v = v.to_str.downcase
          end
          v
        end
        values.uniq!
        values.delete pvalue

        h = @params.dup

        h[pname] = values

        mutate(@group, @name, h, @value)
        values
      end

      # FIXME - should change this so it doesn't assign to @line here, so @line
      # is used to preserve original encoding. That way, #encode can only wrap
      # new fields, not old fields.
      def mutate(g, n, p, v) #:nodoc:
        line = Field.encode0(g, n, p, v)

        begin
          @group, @name, @params, @value = Field.decode0(line)
          @line = line
        rescue ::Vcard::InvalidEncodingError => e
          raise ArgumentError, e.to_s
        end
        self
      end

      private :mutate
    end
  end
end


# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

module Vcard
  # A vCard, a specialization of a directory info object.
  #
  # The vCard format is specified by:
  # - RFC2426[http://www.ietf.org/rfc/rfc2426.txt]: vCard MIME Directory Profile (vCard 3.0)
  # - RFC2425[http://www.ietf.org/rfc/rfc2425.txt]: A MIME Content-Type for Directory Information
  #
  # This implements vCard 3.0, but it is also capable of working with vCard 2.1
  # if used with care.
  #
  # All line values can be accessed with Vcard#value, Vcard#values, or even by
  # iterating through Vcard#lines. Line types that don't have specific support
  # and non-standard line types ("X-MY-SPECIAL", for example) will be returned
  # as a String, with any base64 or quoted-printable encoding removed.
  #
  # Specific support exists to return more useful values for the standard vCard
  # types, where appropriate.
  #
  # The wrapper functions (#birthday, #nicknames, #emails, etc.) exist
  # partially as an API convenience, and partially as a place to document
  # the values returned for the more complex types, like PHOTO and EMAIL.
  #
  # For types that do not sensibly occur multiple times (like BDAY or GEO),
  # sometimes a wrapper exists only to return a single line, using #value.
  # However, if you find the need, you can still call #values to get all the
  # lines, and both the singular and plural forms will eventually be
  # implemented.
  #
  # For more information see:
  # - RFC2426[http://www.ietf.org/rfc/rfc2426.txt]: vCard MIME Directory Profile (vCard 3.0)
  # - RFC2425[http://www.ietf.org/rfc/rfc2425.txt]: A MIME Content-Type for Directory Information
  # - vCard2.1[http://www.imc.org/pdi/pdiproddev.html]: vCard 2.1 Specifications
  #
  # vCards are usually transmitted in files with <code>.vcf</code>
  # extensions.
  #
  # = Examples
  #
  # - link:ex_mkvcard.txt: example of creating a vCard
  # - link:ex_cpvcard.txt: example of copying and them modifying a vCard
  # - link:ex_mkv21vcard.txt: example of creating version 2.1 vCard
  # - link:mutt-aliases-to-vcf.txt: convert a mutt aliases file to vCards
  # - link:ex_get_vcard_photo.txt: pull photo data from a vCard
  # - link:ab-query.txt: query the OS X Address Book to find vCards
  # - link:vcf-to-mutt.txt: query vCards for matches, output in formats useful
  #   with Mutt (see link:README.mutt for details)
  # - link:tabbed-file-to-vcf.txt: convert a tab-delimited file to vCards, a
  #   (small but) complete application contributed by Dane G. Avilla, thanks!
  # - link:vcf-to-ics.txt: example of how to create calendars of birthdays from vCards
  # - link:vcf-dump.txt: utility for dumping contents of .vcf files
  class Vcard < DirectoryInfo

    # Represents the value of an ADR field.
    #
    # #location, #preferred, and #delivery indicate information about how the
    # address is to be used, the other attributes are parts of the address.
    #
    # Using values other than those defined for #location or #delivery is
    # unlikely to be portable, or even conformant.
    #
    # All attributes are optional. #location and #delivery can be set to arrays
    # of strings.
    class Address
      # post office box (String)
      attr_accessor :pobox
      # seldom used, its not clear what it is for (String)
      attr_accessor :extended
      # street address (String)
      attr_accessor :street
      # usually the city (String)
      attr_accessor :locality
      # usually the province or state (String)
      attr_accessor :region
      # postal code (String)
      attr_accessor :postalcode
      # country name (String)
      attr_accessor :country
      # home, work (Array of String): the location referred to by the address
      attr_accessor :location
      # true, false (boolean): where this is the preferred address (for this location)
      attr_accessor :preferred
      # postal, parcel, dom (domestic), intl (international) (Array of String): delivery
      # type of this address
      attr_accessor :delivery

      # nonstandard types, their meaning is undefined (Array of String). These
      # might be found during decoding, but shouldn't be set during encoding.
      attr_reader :nonstandard

      # Used to simplify some long and tedious code. These symbols are in the
      # order required for the ADR field structured TEXT value, the order
      # cannot be changed.
      @@adr_parts = [
        :@pobox,
        :@extended,
        :@street,
        :@locality,
        :@region,
        :@postalcode,
        :@country,
      ]

      # TODO
      # - #location?
      # - #delivery?
      def initialize #:nodoc:
        # TODO - Add #label to support LABEL. Try to find LABEL
        # in either same group, or with sam params.
        @@adr_parts.each do |part|
          instance_variable_set(part, "")
        end

        @location = []
        @preferred = false
        @delivery = []
        @nonstandard = []
      end

      def encode #:nodoc:
        parts = @@adr_parts.map do |part|
          instance_variable_get(part)
        end

        value = ::Vcard.encode_text_list(parts, ";")

        params = [ @location, @delivery, @nonstandard ]
        params << "pref" if @preferred
        params = params.flatten.compact.map { |s| s.to_str.downcase }.uniq

        paramshash = {}

        paramshash["TYPE"] = params if params.first

        ::Vcard::DirectoryInfo::Field.create( "ADR", value, paramshash)
      end

      def Address.decode(card, field) #:nodoc:
        adr = new

        parts = ::Vcard.decode_text_list(field.value_raw, ";")

        @@adr_parts.each_with_index do |part,i|
          adr.instance_variable_set(part, parts[i] || "")
        end

        params = field.pvalues("TYPE")

        if params
          params.each do |p|
            p.downcase!
            case p
            when "home", "work"
              adr.location << p
            when "postal", "parcel", "dom", "intl"
              adr.delivery << p
            when "pref"
              adr.preferred = true
            else
              adr.nonstandard << p
            end
          end
          # Strip duplicates
          [ adr.location, adr.delivery, adr.nonstandard ].each do |a|
            a.uniq!
          end
        end

        adr
      end
    end

    # Represents the value of an EMAIL field.
    class Email < String
      # true, false (boolean): whether this is the preferred email address
      attr_accessor :preferred
      # internet, x400 (String): the email address format, rarely specified
      # since the default is "internet"
      attr_accessor :format
      # home, work (Array of String): the location referred to by the address. The
      # inclusion of location parameters in a vCard seems to be non-conformant,
      # strictly speaking, but also seems to be widespread.
      attr_accessor :location
      # nonstandard types, their meaning is undefined (Array of String). These
      # might be found during decoding, but shouldn't be set during encoding.
      attr_reader :nonstandard

      def initialize(email="") #:nodoc:
        @preferred = false
        @format = "internet"
        @location = []
        @nonstandard = []
        super(email)
      end

      def inspect #:nodoc:
        s = "#<#{self.class.to_s}: #{to_str.inspect}"
        s << ", pref" if preferred
        s << ", #{format}" if format != "internet"
        s << ", " << @location.join(", ") if @location.first
        s << ", #{@nonstandard.join(", ")}" if @nonstandard.first
        s
      end

      def encode #:nodoc:
        value = to_str.strip

        if value.length < 1
          raise InvalidEncodingError, "EMAIL must have a value"
        end

        params = [ @location, @nonstandard ]
        params << @format if @format != "internet"
        params << "pref"  if @preferred

        params = params.flatten.compact.map { |s| s.to_str.downcase }.uniq

        paramshash = {}

        paramshash["TYPE"] = params if params.first

        ::Vcard::DirectoryInfo::Field.create("EMAIL", value, paramshash)
      end

      def Email.decode(field) #:nodoc:
        value = field.to_text.strip

        if value.length < 1
          raise InvalidEncodingError, "EMAIL must have a value"
        end

        eml = Email.new(value)

        params = field.pvalues("TYPE")

        if params
          params.each do |p|
            p.downcase!
            case p
            when "home", "work"
              eml.location << p
            when "pref"
              eml.preferred = true
            when "x400", "internet"
              eml.format = p
            else
              eml.nonstandard << p
            end
          end
          # Strip duplicates
          [ eml.location, eml.nonstandard ].each do |a|
            a.uniq!
          end
        end

        eml
      end
    end

    # Represents the value of a TEL field.
    #
    # The value is supposed to be a "X.500 Telephone Number" according to RFC
    # 2426, but that standard is not freely available. Otherwise, anything that
    # looks like a phone number should be OK.
    class Telephone < String
      # true, false (boolean): whether this is the preferred email address
      attr_accessor :preferred
      # home, work, cell, car, pager (Array of String): the location
      # of the device
      attr_accessor :location
      # voice, fax, video, msg, bbs, modem, isdn, pcs (Array of String): the
      # capabilities of the device
      attr_accessor :capability
      # nonstandard types, their meaning is undefined (Array of String). These
      # might be found during decoding, but shouldn't be set during encoding.
      attr_reader :nonstandard

      def initialize(telephone="") #:nodoc:
        @preferred = false
        @location = []
        @capability = []
        @nonstandard = []
        super(telephone)
      end

      def inspect #:nodoc:
        s = "#<#{self.class.to_s}: #{to_str.inspect}"
        s << ", pref" if preferred
        s << ", " << @location.join(", ") if @location.first
        s << ", " << @capability.join(", ") if @capability.first
        s << ", #{@nonstandard.join(", ")}" if @nonstandard.first
        s
      end

      def encode #:nodoc:
        value = to_str.strip

        if value.length < 1
          raise InvalidEncodingError, "TEL must have a value"
        end

        params = [ @location, @capability, @nonstandard ]
        params << "pref"  if @preferred

        params = params.flatten.compact.map { |s| s.to_str.downcase }.uniq

        paramshash = {}

        paramshash["TYPE"] = params if params.first

        ::Vcard::DirectoryInfo::Field.create( "TEL", value, paramshash)
      end

      def Telephone.decode(field) #:nodoc:
        value = field.to_text.strip

        if value.length < 1
          raise InvalidEncodingError, "TEL must have a value"
        end

        tel = Telephone.new(value)

        params = field.pvalues("TYPE")

        if params
          params.each do |p|
            p.downcase!
            case p
            when "home", "work", "cell", "car", "pager"
              tel.location << p
            when "voice", "fax", "video", "msg", "bbs", "modem", "isdn", "pcs"
              tel.capability << p
            when "pref"
              tel.preferred = true
            else
              tel.nonstandard << p
            end
          end
          # Strip duplicates
          [ tel.location, tel.capability, tel.nonstandard ].each do |a|
            a.uniq!
          end
        end

        tel
      end
    end

    # The name from a vCard, including all the components of the N: and FN:
    # fields.
    class Name
      # family name, from N
      attr_accessor :family
      # given name, from N
      attr_accessor :given
      # additional names, from N
      attr_accessor :additional
      # such as "Ms." or "Dr.", from N
      attr_accessor :prefix
      # such as "BFA", from N
      attr_accessor :suffix
      # full name, the FN field. FN is a formatted version of the N field,
      # intended to be in a form more aligned with the cultural conventions of
      # the vCard owner than +formatted+ is.
      attr_accessor :fullname
      # all the components of N formtted as "#{prefix} #{given} #{additional} #{family}, #{suffix}"
      attr_reader   :formatted

      # Override the attr reader to make it dynamic
      remove_method :formatted
      def formatted #:nodoc:
        f = [ @prefix, @given, @additional, @family ].map{|i| i == "" ? nil : i.strip}.compact.join(" ")
        if @suffix != ""
          f << ", " << @suffix
        end
        f
      end

      def initialize(n="", fn="") #:nodoc:
        n = ::Vcard.decode_text_list(n, ";") do |item|
          item.strip
        end

        @family     = n[0] || ""
        @given      = n[1] || ""
        @additional = n[2] || ""
        @prefix     = n[3] || ""
        @suffix     = n[4] || ""

        # FIXME - make calls to #fullname fail if fn is nil
        @fullname = (fn || "").strip
      end

      def encode #:nodoc:
        ::Vcard::DirectoryInfo::Field.create("N", ::Vcard.encode_text_list([ @family, @given, @additional, @prefix, @suffix ].map{|n| n.strip}, ";"))
      end

      def encode_fn #:nodoc:
        fn = @fullname.strip
        if @fullname.length == 0
          fn = formatted
        end
        ::Vcard::DirectoryInfo::Field.create("FN", fn)
      end
    end

    def decode_invisible(field) #:nodoc:
      nil
    end

    def decode_default(field) #:nodoc:
      Line.new( field.group, field.name, field.value )
    end

    def decode_version(field) #:nodoc:
      Line.new( field.group, field.name, (field.value.to_f * 10).to_i )
    end

    def decode_text(field) #:nodoc:
      Line.new( field.group, field.name, ::Vcard.decode_text(field.value_raw) )
    end

    def decode_n(field) #:nodoc:
      Line.new( field.group, field.name, Name.new(field.value, self["FN"]).freeze )
    end

    def decode_date_or_datetime(field) #:nodoc:
      date = nil
      begin
        date = ::Vcard.decode_date_to_date(field.value_raw)
      rescue ::Vcard::InvalidEncodingError
        date = ::Vcard.decode_date_time_to_datetime(field.value_raw)
      end
      Line.new( field.group, field.name, date )
    end

    def decode_bday(field) #:nodoc:
      begin
        return decode_date_or_datetime(field)

      rescue ::Vcard::InvalidEncodingError
        # Hack around BDAY dates hat are correct in the month and day, but have
        # some kind of garbage in the year.
        if field.value =~ /^\s*(\d+)-(\d+)-(\d+)\s*$/
          y = $1.to_i
          m = $2.to_i
          d = $3.to_i
          if(y < 1900)
            y = Time.now.year
          end
          Line.new( field.group, field.name, Date.new(y, m, d) )
        else
          raise
        end
      end
    end

    def decode_geo(field) #:nodoc:
      geo = ::Vcard.decode_list(field.value_raw, ";") do |item| item.to_f end
      Line.new( field.group, field.name, geo )
    end

    def decode_address(field) #:nodoc:
      Line.new( field.group, field.name, Address.decode(self, field) )
    end

    def decode_email(field) #:nodoc:
      Line.new( field.group, field.name, Email.decode(field) )
    end

    def decode_telephone(field) #:nodoc:
      Line.new( field.group, field.name, Telephone.decode(field) )
    end

    def decode_list_of_text(field) #:nodoc:
      Line.new(field.group, field.name, ::Vcard.decode_text_list(field.value_raw).select{|t| t.length > 0}.uniq)
    end

    def decode_structured_text(field) #:nodoc:
      Line.new( field.group, field.name, ::Vcard.decode_text_list(field.value_raw, ";") )
    end

    def decode_uri(field) #:nodoc:
      Line.new( field.group, field.name, Attachment::Uri.new(field.value, nil) )
    end

    def decode_agent(field) #:nodoc:
      case field.kind
      when "text"
        decode_text(field)
      when "uri"
        decode_uri(field)
      when "vcard", nil
        Line.new( field.group, field.name, ::Vcard.decode(::Vcard.decode_text(field.value_raw)).first )
      else
        raise InvalidEncodingError, "AGENT type #{field.kind} is not allowed"
      end
    end

    def decode_attachment(field) #:nodoc:
      Line.new( field.group, field.name, Attachment.decode(field, "binary", "TYPE") )
    end

    @@decode = {
      "BEGIN"      => :decode_invisible, # Don't return delimiter
      "END"        => :decode_invisible, # Don't return delimiter
      "FN"         => :decode_invisible, # Returned as part of N.

      "ADR"        => :decode_address,
      "AGENT"      => :decode_agent,
      "BDAY"       => :decode_bday,
      "CATEGORIES" => :decode_list_of_text,
      "EMAIL"      => :decode_email,
      "GEO"        => :decode_geo,
      "KEY"        => :decode_attachment,
      "LOGO"       => :decode_attachment,
      "MAILER"     => :decode_text,
      "N"          => :decode_n,
      "NAME"       => :decode_text,
      "NICKNAME"   => :decode_list_of_text,
      "NOTE"       => :decode_text,
      "ORG"        => :decode_structured_text,
      "PHOTO"      => :decode_attachment,
      "PRODID"     => :decode_text,
      "PROFILE"    => :decode_text,
      "REV"        => :decode_date_or_datetime,
      "ROLE"       => :decode_text,
      "SOUND"      => :decode_attachment,
      "SOURCE"     => :decode_text,
      "TEL"        => :decode_telephone,
      "TITLE"      => :decode_text,
      "UID"        => :decode_text,
      "URL"        => :decode_uri,
      "VERSION"    => :decode_version,
    }

    @@decode.default = :decode_default

    # Cache of decoded lines/fields, so we don't have to decode a field more than once.
    attr_reader :cache #:nodoc:

    # An entry in a vCard. The #value object's type varies with the kind of
    # line (the #name), and on how the line was encoded. The objects returned
    # for a specific kind of line are often extended so that they support a
    # common set of methods. The goal is to allow all types of objects for a
    # kind of line to be treated with some uniformity, but still allow specific
    # handling for the various value types if desired.
    #
    # See the specific methods for details.
    class Line
      attr_reader :group
      attr_reader :name
      attr_reader :value

      def initialize(group, name, value) #:nodoc:
        @group, @name, @value = (group||""), name.to_str, value
      end

      def self.decode(decode, card, field) #:nodoc:
        card.cache[field] || (card.cache[field] = card.send(decode[field.name], field))
      end
    end

    #@lines = {} FIXME - dead code

    # Return line for a field
    def f2l(field) #:nodoc:
      begin
        Line.decode(@@decode, self, field)
      rescue InvalidEncodingError
        # Skip invalidly encoded fields.
      end
    end

    # With no block, returns an Array of Line. If +name+ is specified, the
    # Array will only contain the +Line+s with that +name+. The Array may be
    # empty.
    #
    # If a block is given, each Line will be yielded instead of being returned
    # in an Array.
    def lines(name=nil) #:yield: Line
      # FIXME - this would be much easier if #lines was #each, and there was a
      # different #lines that returned an Enumerator that used #each
      unless block_given?
        map do |f|
          if( !name || f.name?(name) )
            f2l(f)
          else
            nil
          end
        end.compact
      else
        each do |f|
          if( !name || f.name?(name) )
            line = f2l(f)
            if line
              yield line
            end
          end
        end
        self
      end
    end

    private_class_method :new

    def initialize(fields, profile) #:nodoc:
      @cache = {}
      super(fields, profile)
    end

    # Create a vCard 3.0 object with the minimum required fields, plus any
    # +fields+ you want in the card (they can also be added later).
    def self.create(fields = [] )
      fields.unshift Field.create("VERSION", "3.0")
      super(fields, "VCARD")
    end

    # Decode a collection of vCards into an array of Vcard objects.
    #
    # +card+ can be either a String or an IO object.
    #
    # Since vCards are self-delimited (by a BEGIN:vCard and an END:vCard),
    # multiple vCards can be concatenated into a single directory info object.
    # They may or may not be related. For example, AddressBook.app (the OS X
    # contact manager) will export multiple selected cards in this format.
    #
    # Input data will be converted from unicode if it is detected. The heuristic
    # is based on the first bytes in the string:
    # - 0xEF 0xBB 0xBF: UTF-8 with a BOM, the BOM is stripped
    # - 0xFE 0xFF: UTF-16 with a BOM (big-endian), the BOM is stripped and string
    #   is converted to UTF-8
    # - 0xFF 0xFE: UTF-16 with a BOM (little-endian), the BOM is stripped and string
    #   is converted to UTF-8
    # - 0x00 "B" or 0x00 "b": UTF-16 (big-endian), the string is converted to UTF-8
    # - "B" 0x00 or "b" 0x00: UTF-16 (little-endian), the string is converted to UTF-8
    #
    # If you know that you have only one vCard, then you can decode that
    # single vCard by doing something like:
    #
    #   vcard = Vcard.decode(card_data).first
    #
    # Note: Should the import encoding be remembered, so that it can be reencoded in
    # the same format?
    def self.decode(card)
      if card.respond_to? :to_str
        string = card.to_str
      elsif card.respond_to? :read
        string = card.read(nil)
      else
        raise ArgumentError, "Vcard.decode cannot be called with a #{card.type}"
      end

      string.force_encoding(Encoding::UTF_8)
      entities = ::Vcard.expand(::Vcard.decode(string))

      # Since all vCards must have a begin/end, the top-level should consist
      # entirely of entities/arrays, even if its a single vCard.
      if entities.detect { |e| ! e.kind_of? Array }
        raise "Not a valid vCard"
      end

      vcards = []

      for e in entities
        vcards.push(new(e.flatten, "VCARD"))
      end

      vcards
    end

    # The value of the field named +name+, optionally limited to fields of
    # type +type+. If no match is found, nil is returned, if multiple matches
    # are found, the first match to have one of its type values be "PREF"
    # (preferred) is returned, otherwise the first match is returned.
    #
    # FIXME - this will become an alias for #value.
    def [](name, type=nil)
      fields = enum_by_name(name).find_all { |f| type == nil || f.type?(type) }

      valued = fields.select { |f| f.value != "" }
      if valued.first
        fields = valued
      end

      # limit to preferred, if possible
      pref = fields.select { |f| f.pref? }

      if pref.first
        fields = pref
      end

      fields.first ? fields.first.value : nil
    end

    # Return the Line#value for a specific +name+, and optionally for a
    # specific +type+.
    #
    # If no line with the +name+ (and, optionally, +type+) exists, nil is
    # returned.
    #
    # If multiple lines exist, the order of preference is:
    # - lines with values over lines without
    # - lines with a type of "pref" over lines without
    # If multiple lines are equally preferred, then the first line will be
    # returned.
    #
    # This is most useful when looking for a line that can not occur multiple
    # times, or when the line can occur multiple times, and you want to pick
    # the first preferred line of a specific type. See #values if you need to
    # access all the lines.
    #
    # Note that the +type+ field parameter is used for different purposes by
    # the various kinds of vCard lines, but for the addressing lines (ADR,
    # LABEL, TEL, EMAIL) it is has a reasonably consistent usage. Each
    # addressing line can occur multiple times, and a +type+ of "pref"
    # indicates that a particular line is the preferred line. Other +type+
    # values tend to indicate some information about the location ("home",
    # "work", ...) or some detail about the address ("cell", "fax", "voice",
    # ...). See the methods for the specific types of line for information
    # about supported types and their meaning.
    def value(name, type = nil)
      fields = enum_by_name(name).find_all { |f| type == nil || f.type?(type) }

      valued = fields.select { |f| f.value != "" }
      if valued.first
        fields = valued
      end

      pref = fields.select { |f| f.pref? }

      if pref.first
        fields = pref
      end

      if fields.first
        line = begin
                 Line.decode(@@decode, self, fields.first)
               rescue ::Vcard::InvalidEncodingError
               end

        if line
          return line.value
        end
      end

      nil
    end

    # A variant of #lines that only iterates over specific Line names. Since
    # the name is known, only the Line#value is returned or yielded.
    def values(name)
      unless block_given?
        lines(name).map { |line| line.value }
      else
        lines(name) { |line| yield line.value }
      end
    end

    # The first ADR value of type +type+, a Address. Any of the location or
    # delivery attributes of Address can be used as +type+. A wrapper around
    # #value("ADR", +type+).
    def address(type=nil)
      value("ADR", type)
    end

    # The ADR values, an array of Address. If a block is given, the values are
    # yielded. A wrapper around #values("ADR").
    def addresses #:yield:address
      values("ADR")
    end

    # The AGENT values. Each AGENT value is either a String, a Uri, or a Vcard.
    # If a block is given, the values are yielded. A wrapper around
    # #values("AGENT").
    def agents #:yield:agent
      values("AGENT")
    end

    # The BDAY value as either a Date or a DateTime, or nil if there is none.
    #
    # If the BDAY value is invalidly formatted, a feeble heuristic is applied
    # to find the month and year, and return a Date in the current year.
    def birthday
      value("BDAY")
    end

    # The CATEGORIES values, an array of String. A wrapper around
    # #value("CATEGORIES").
    def categories
      value("CATEGORIES")
    end

    # The first EMAIL value of type +type+, a Email. Any of the location
    # attributes of Email can be used as +type+. A wrapper around
    # #value("EMAIL", +type+).
    def email(type=nil)
      value("EMAIL", type)
    end

    # The EMAIL values, an array of Email. If a block is given, the values are
    # yielded. A wrapper around #values("EMAIL").
    def emails #:yield:email
      values("EMAIL")
    end

    # The GEO value, an Array of two Floats, +[ latitude, longitude]+.  North
    # of the equator is positive latitude, east of the meridian is positive
    # longitude.  See RFC2445 for more info, there are lots of special cases
    # and RFC2445"s description is more complete thant RFC2426.
    def geo
      value("GEO")
    end

    # Return an Array of KEY Line#value, or yield each Line#value if a block
    # is given. A wrapper around #values("KEY").
    #
    # KEY is a public key or authentication certificate associated with the
    # object that the vCard represents. It is not commonly used, but could
    # contain a X.509 or PGP certificate.
    #
    # See Attachment for a description of the value.
    def keys(&proc) #:yield: Line.value
      values("KEY", &proc)
    end

    # Return an Array of LOGO Line#value, or yield each Line#value if a block
    # is given. A wrapper around #values("LOGO").
    #
    # LOGO is a graphic image of a logo associated with the object the vCard
    # represents. Its not common, but would probably be equivalent to the logo
    # on a printed card.
    #
    # See Attachment for a description of the value.
    def logos(&proc) #:yield: Line.value
      values("LOGO", &proc)
    end

    ## MAILER

    # The N and FN as a Name object.
    #
    # N is required for a vCards, this raises InvalidEncodingError if
    # there is no N so it cannot return nil.
    def name
      value("N") || raise(::Vcard::InvalidEncodingError, "Missing mandatory N field")
    end

    # The first NICKNAME value, nil if there are none.
    def nickname
      v = value("NICKNAME")
      v = v.first if v
      v
    end

    # The NICKNAME values, an array of String. The array may be empty.
    def nicknames
      values("NICKNAME").flatten.uniq
    end

    # The NOTE value, a String. A wrapper around #value("NOTE").
    def note
      value("NOTE")
    end

    # The ORG value, an Array of String. The first string is the organization,
    # subsequent strings are departments within the organization. A wrapper
    # around #value("ORG").
    def org
      value("ORG")
    end

    # Return an Array of PHOTO Line#value, or yield each Line#value if a block
    # is given. A wrapper around #values("PHOTO").
    #
    # PHOTO is an image or photograph information that annotates some aspect of
    # the object the vCard represents. Commonly there is one PHOTO, and it is a
    # photo of the person identified by the vCard.
    #
    # See Attachment for a description of the value.
    def photos(&proc) #:yield: Line.value
      values("PHOTO", &proc)
    end

    ## PRODID

    ## PROFILE

    ## REV

    ## ROLE

    # Return an Array of SOUND Line#value, or yield each Line#value if a block
    # is given. A wrapper around #values("SOUND").
    #
    # SOUND is digital sound content information that annotates some aspect of
    # the vCard. By default this type is used to specify the proper
    # pronunciation of the name associated with the vCard. It is not commonly
    # used. Also, note that there is no mechanism available to specify that the
    # SOUND is being used for anything other than the default.
    #
    # See Attachment for a description of the value.
    def sounds(&proc) #:yield: Line.value
      values("SOUND", &proc)
    end

    ## SOURCE

    # The first TEL value of type +type+, a Telephone. Any of the location or
    # capability attributes of Telephone can be used as +type+. A wrapper around
    # #value("TEL", +type+).
    def telephone(type=nil)
      value("TEL", type)
    end

    # The TEL values, an array of Telephone. If a block is given, the values are
    # yielded. A wrapper around #values("TEL").
    def telephones #:yield:tel
      values("TEL")
    end

    # The TITLE value, a text string specifying the job title, functional
    # position, or function of the object the card represents. A wrapper around
    # #value("TITLE").
    def title
      value("TITLE")
    end

    ## UID

    # The URL value, a Attachment::Uri. A wrapper around #value("URL").
    def url
      value("URL")
    end

    # The URL values, an Attachment::Uri. A wrapper around #values("URL").
    def urls
      values("URL")
    end

    # The VERSION multiplied by 10 as an Integer.  For example, a VERSION:2.1
    # vCard would have a version of 21, and a VERSION:3.0 vCard would have a
    # version of 30.
    #
    # VERSION is required for a vCard, this raises InvalidEncodingError if
    # there is no VERSION so it cannot return nil.
    def version
      v = value("VERSION")
      unless v
        raise ::Vcard::InvalidEncodingError, "Invalid vCard - it has no version field!"
      end
      v
    end

    # Make changes to a vCard.
    #
    # Yields a Vcard::Vcard::Maker that can be used to modify this vCard.
    def make #:yield: maker
      ::Vcard::Vcard::Maker.make2(self) do |maker|
        yield maker
      end
    end

    # Delete +line+ if block yields true.
    def delete_if #:nodoc: :yield: line
      # Do in two steps to not mess up progress through the enumerator.
      rm = []

      each do |f|
        line = f2l(f)
        if line && yield(line)
          rm << f

          # Hack - because we treat N and FN as one field
          if f.name? "N"
            rm << field("FN")
          end
        end
      end

      rm.each do |f|
        @fields.delete( f )
        @cache.delete( f )
      end

    end

    # A class to make and make changes to vCards.
    #
    # It can be used to create completely new vCards using Vcard#make2.
    #
    # Its is also yielded from Vcard::Vcard#make, in which case it allows a kind
    # of transactional approach to changing vCards, so their values can be
    # validated after any changes have been made.
    #
    # Examples:
    # - link:ex_mkvcard.txt: example of creating a vCard
    # - link:ex_cpvcard.txt: example of copying and them modifying a vCard
    # - link:ex_mkv21vcard.txt: example of creating version 2.1 vCard
    # - link:ex_mkyourown.txt: example of adding support for new fields to Vcard::Maker
    class Maker
      # Make a vCard.
      #
      # Yields +maker+, a Vcard::Vcard::Maker which allows fields to be added to
      # +card+, and returns +card+, a Vcard::Vcard.
      #
      # If +card+ is nil or not provided a new Vcard::Vcard is created and the
      # fields are added to it.
      #
      # Defaults:
      # - vCards must have both an N and an FN field, #make2 will fail if there
      #   is no N field in the +card+ when your block is finished adding fields.
      # - If there is an N field, but no FN field, FN will be set from the
      #   information in N, see Vcard::Name#preformatted for more information.
      # - vCards must have a VERSION field. If one does not exist when your block is
      #   is finished it will be set to 3.0.
      def self.make2(card = ::Vcard::Vcard.create, &block) # :yields: maker
        new(nil, card).make(&block)
      end

      # Deprecated, use #make2.
      #
      # If set, the FN field will be set to +full_name+. Otherwise, FN will
      # be set from the values in #name.
      def self.make(full_name = nil, &block) # :yields: maker
        new(full_name, ::Vcard::Vcard.create).make(&block)
      end

      def make # :nodoc:
        yield self
        unless @card["N"]
          raise Unencodeable, "N field is mandatory"
        end
        fn = @card.field("FN")
        if fn && fn.value.strip.length == 0
          @card.delete(fn)
          fn = nil
        end
        unless fn
          @card << ::Vcard::DirectoryInfo::Field.create("FN", ::Vcard::Vcard::Name.new(@card["N"], "").formatted)
        end
        unless @card["VERSION"]
          @card << ::Vcard::DirectoryInfo::Field.create("VERSION", "3.0")
        end
        @card
      end

      private

      def initialize(full_name, card) # :nodoc:
        @card = card || ::Vcard::Vcard::create
        if full_name
          @card << ::Vcard::DirectoryInfo::Field.create("FN", full_name.strip )
        end
      end

      public

      # Deprecated, see #name.
      #
      # Use
      #   maker.name do |n| n.fullname = "foo" end
      # to set just fullname, or set the other fields to set fullname and the
      # name.
      def fullname=(fullname) #:nodoc: bacwards compat
        if @card.field("FN")
          raise ::Vcard::InvalidEncodingError, "Not allowed to add more than one FN field to a vCard."
        end
        @card << ::Vcard::DirectoryInfo::Field.create( "FN", fullname );
      end

      # Set the name fields, N and FN.
      #
      # Attributes of +name+ are:
      # - family: family name
      # - given: given name
      # - additional: additional names
      # - prefix: such as "Ms." or "Dr."
      # - suffix: such as "BFA", or "Sensei"
      #
      # +name+ is a Vcard::Name.
      #
      # All attributes are optional, though have all names be zero-length
      # strings isn't really in the spirit of  things. FN's value will be set
      # to Vcard::Name#formatted if Vcard::Name#fullname isn't given a specific
      # value.
      #
      # Warning: This is the only mandatory field.
      def name #:yield:name
        x = begin
              @card.name.dup
            rescue
              ::Vcard::Vcard::Name.new
            end

        yield x

        x.fullname.strip!

        delete_if do |line|
          line.name == "N"
        end

        @card << x.encode
        @card << x.encode_fn

        self
      end

      alias :add_name :name #:nodoc: backwards compatibility

      # Add an address field, ADR. +address+ is a Vcard::Vcard::Address.
      def add_addr # :yield: address
        x = ::Vcard::Vcard::Address.new
        yield x
        @card << x.encode
        self
      end

      # Add a telephone field, TEL. +tel+ is a Vcard::Vcard::Telephone.
      #
      # The block is optional, its only necessary if you want to specify
      # the optional attributes.
      def add_tel(number) # :yield: tel
        x = ::Vcard::Vcard::Telephone.new(number)
        if block_given?
          yield x
        end
        @card << x.encode
        self
      end

      # Add an email field, EMAIL. +email+ is a Vcard::Vcard::Email.
      #
      # The block is optional, its only necessary if you want to specify
      # the optional attributes.
      def add_email(email) # :yield: email
        x = ::Vcard::Vcard::Email.new(email)
        if block_given?
          yield x
        end
        @card << x.encode
        self
      end

      # Set the nickname field, NICKNAME.
      #
      # It can be set to a single String or an Array of String.
      def nickname=(nickname)
        delete_if { |l| l.name == "NICKNAME" }

        @card << ::Vcard::DirectoryInfo::Field.create( "NICKNAME", nickname );
      end

      # Add a birthday field, BDAY.
      #
      # +birthday+ must be a time or date object.
      #
      # Warning: It may confuse both humans and software if you add multiple
      # birthdays.
      def birthday=(birthday)
        if !birthday.respond_to? :month
          raise ArgumentError, "birthday must be a date or time object."
        end
        delete_if { |l| l.name == "BDAY" }
        @card << ::Vcard::DirectoryInfo::Field.create( "BDAY", birthday );
      end

      # Add a note field, NOTE. The +note+ String can contain newlines, they
      # will be escaped.
      def add_note(note)
        @card << ::Vcard::DirectoryInfo::Field.create( "NOTE", ::Vcard.encode_text(note) );
      end

      # Add an instant-messaging/point of presence address field, IMPP. The address
      # is a URL, with the syntax depending on the protocol.
      #
      # Attributes of IMPP are:
      # - preferred: true - set if this is the preferred address
      # - location: home, work, mobile - location of address
      # - purpose: personal,business - purpose of communications
      #
      # All attributes are optional, and so is the block.
      #
      # The URL syntaxes for the messaging schemes is fairly complicated, so I
      # don't try and build the URLs here, maybe in the future. This forces
      # the user to know the URL for their own address, hopefully not too much
      # of a burden.
      #
      # IMPP is defined in draft-jennings-impp-vcard-04.txt. It refers to the
      # URI scheme of a number of messaging protocols, but doesn't give
      # references to all of them:
      # - "xmpp" indicates to use XMPP, draft-saintandre-xmpp-uri-06.txt
      # - "irc" or "ircs" indicates to use IRC, draft-butcher-irc-url-04.txt
      # - "sip" indicates to use SIP/SIMPLE, RFC 3261
      # - "im" or "pres" indicates to use a CPIM or CPP gateway, RFC 3860 and RFC 3859
      # - "ymsgr" indicates to use yahoo
      # - "msn" might indicate to use Microsoft messenger
      # - "aim" indicates to use AOL
      #
      def add_impp(url) # :yield: impp
        params = {}

        if block_given?
          x = Struct.new( :location, :preferred, :purpose ).new

          yield x

          x[:preferred] = "PREF" if x[:preferred]

          types = x.to_a.flatten.compact.map { |s| s.downcase }.uniq

          params["TYPE"] = types if types.first
        end

        @card << ::Vcard::DirectoryInfo::Field.create( "IMPP", url, params)
        self
      end

      # Add an X-AIM account name where +xaim+ is an AIM screen name.
      #
      # I don't know if this is conventional, or supported by anything other
      # than AddressBook.app, but an example is:
      #   X-AIM;type=HOME;type=pref:exampleaccount
      #
      # Attributes of X-AIM are:
      # - preferred: true - set if this is the preferred address
      # - location: home, work, mobile - location of address
      #
      # All attributes are optional, and so is the block.
      def add_x_aim(xaim) # :yield: xaim
        params = {}

        if block_given?
          x = Struct.new( :location, :preferred ).new

          yield x

          x[:preferred] = "PREF" if x[:preferred]

          types = x.to_a.flatten.compact.map { |s| s.downcase }.uniq

          params["TYPE"] = types if types.first
        end

        @card << ::Vcard::DirectoryInfo::Field.create( "X-AIM", xaim, params)
        self
      end


      # Add a photo field, PHOTO.
      #
      # Attributes of PHOTO are:
      # - image: set to image data to include inline
      # - link: set to the URL of the image data
      # - type: string identifying the image type, supposed to be an "IANA registered image format",
      #     or a non-registered image format (usually these start with an x-)
      #
      # An error will be raised if neither image or link is set, or if both image
      # and link is set.
      #
      # Setting type is optional for a link image, because either the URL, the
      # image file extension, or a HTTP Content-Type may specify the type. If
      # it's not a link, setting type is mandatory, though it can be set to an
      # empty string, <code>''</code>, if the type is unknown.
      #
      # TODO - I'm not sure about this API. I'm thinking maybe it should be
      # #add_photo(image, type), and that I should detect when the image is a
      # URL, and make type mandatory if it wasn't a URL.
      def add_photo # :yield: photo
        x = Struct.new(:image, :link, :type).new
        yield x
        if x[:image] && x[:link]
          raise ::Vcard::InvalidEncodingError, "Image is not allowed to be both inline and a link."
        end

        value = x[:image] || x[:link]

        if !value
          raise ::Vcard::InvalidEncodingError, "A image link or inline data must be provided."
        end

        params = {}

        # Don't set type to the empty string.
        params["TYPE"] = x[:type] if( x[:type] && x[:type].length > 0 )

        if x[:link]
          params["VALUE"] = "URI"
        else # it's inline, base-64 encode it
          params["ENCODING"] = :b64
          if !x[:type]
            raise ::Vcard::InvalidEncodingError, "Inline image data must have it's type set."
          end
        end

        @card << ::Vcard::DirectoryInfo::Field.create( "PHOTO", value, params )
        self
      end

      # Set the title field, TITLE.
      #
      # It can be set to a single String.
      def title=(title)
        delete_if { |l| l.name == "TITLE" }

        @card << ::Vcard::DirectoryInfo::Field.create( "TITLE", title );
      end

      # Set the org field, ORG.
      #
      # It can be set to a single String or an Array of String.
      def org=(org)
        delete_if { |l| l.name == "ORG" }

        @card << ::Vcard::DirectoryInfo::Field.create( "ORG", org );
      end


      # Add a URL field, URL.
      def add_url(url)
        @card << ::Vcard::DirectoryInfo::Field.create( "URL", url.to_str );
      end

      # Add a Field, +field+.
      def add_field(field)
        fieldname = field.name.upcase
        case
        when [ "BEGIN", "END" ].include?(fieldname)
          raise ::Vcard::InvalidEncodingError, "Not allowed to manually add #{field.name} to a vCard."

        when [ "VERSION", "N", "FN" ].include?(fieldname)
          if @card.field(fieldname)
            raise ::Vcard::InvalidEncodingError, "Not allowed to add more than one #{fieldname} to a vCard."
          end
          @card << field

        else
          @card << field
        end
      end

      # Copy the fields from +card+ into self using #add_field. If a block is
      # provided, each Field from +card+ is yielded. The block should return a
      # Field to add, or nil.  The Field doesn't have to be the one yielded,
      # allowing the field to be copied and modified (see Field#copy) before adding, or
      # not added at all if the block yields nil.
      #
      # The vCard fields BEGIN and END aren't copied, and VERSION, N, and FN are copied
      # only if the card doesn't have them already.
      def copy(card) # :yields: Field
        card.each do |field|
          fieldname = field.name.upcase
          case
          when [ "BEGIN", "END" ].include?(fieldname)
            # Never copy these

          when [ "VERSION", "N", "FN" ].include?(fieldname) && @card.field(fieldname)
            # Copy these only if they don't already exist.

          else
            if block_given?
              field = yield field
            end

            if field
              add_field(field)
            end
          end
        end
      end

      # Delete +line+ if block yields true.
      def delete_if #:yield: line
        begin
          @card.delete_if do |line|
            yield line
          end
        rescue NoMethodError
          # FIXME - this is a hideous hack, allowing a DirectoryInfo to
          # be passed instead of a Vcard, and for it to almost work. Yuck.
        end
      end

    end
  end
end


module Vcard
  VERSION = "0.2.0"
end

# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

require "date"
require "open-uri"
require "stringio"


module Vcard
  # Split on \r\n or \n to get the lines, unfold continued lines (they
  # start with " " or \t), and return the array of unfolded lines.
  #
  # This also supports the (invalid) encoding convention of allowing empty
  # lines to be inserted for readability - it does this by dropping zero-length
  # lines.
  def self.unfold(card) #:nodoc:
      unfolded = []

      card.lines do |line|
        line.chomp!
        # If it's a continuation line, add it to the last.
        # If it's an empty line, drop it from the input.
        if( line =~ /^[ \t]/ )
          unfolded[-1] << line[1, line.size-1]
        elsif( line =~ /^$/ )
        else
          unfolded << line
        end
      end

      unfolded
  end

  # Convert a +sep+-seperated list of values into an array of values.
  def self.decode_list(value, sep = ",") # :nodoc:
    list = []

    value.split(sep).each do |item|
      item.chomp!(sep)
      list << yield(item)
    end
    list
  end

  # Convert a RFC 2425 date into an array of [year, month, day].
  def self.decode_date(v) # :nodoc:
    unless v =~ %r{^\s*#{Bnf::DATE}\s*$}
      raise ::Vcard::InvalidEncodingError, "date not valid (#{v})"
    end
    [$1.to_i, $2.to_i, $3.to_i]
  end

  # Convert a RFC 2425 date into a Date object.
  def self.decode_date_to_date(v)
    Date.new(*decode_date(v))
  end

  # Note in the following the RFC2425 allows yyyy-mm-ddThh:mm:ss, but RFC2445
  # does not. I choose to encode to the subset that is valid for both.

  # Encode a Date object as "yyyymmdd".
  def self.encode_date(d) # :nodoc:
     "%0.4d%0.2d%0.2d" % [ d.year, d.mon, d.day ]
  end

  # Encode a Date object as "yyyymmdd".
  def self.encode_time(d) # :nodoc:
     "%0.4d%0.2d%0.2d" % [ d.year, d.mon, d.day ]
  end

  # Encode a Time or DateTime object as "yyyymmddThhmmss"
  def self.encode_date_time(d) # :nodoc:
     "%0.4d%0.2d%0.2dT%0.2d%0.2d%0.2d" % [ d.year, d.mon, d.day, d.hour, d.min, d.sec ]
  end

  # Convert a RFC 2425 time into an array of [hour,min,sec,secfrac,timezone]
  def self.decode_time(v) # :nodoc:
    unless match = %r{^\s*#{Bnf::TIME}\s*$}.match(v)
      raise ::Vcard::InvalidEncodingError, "time '#{v}' not valid"
    end
    hour, min, sec, secfrac, tz = match.to_a[1..5]

    [hour.to_i, min.to_i, sec.to_i, secfrac ? secfrac.to_f : 0, tz]
  end

  def self.array_datetime_to_time(dtarray) #:nodoc:
    # We get [ year, month, day, hour, min, sec, usec, tz ]
    begin
      tz = (dtarray.pop == "Z") ? :gm : :local
      Time.send(tz, *dtarray)
    rescue ArgumentError => e
      raise ::Vcard::InvalidEncodingError, "#{tz} #{e} (#{dtarray.join(', ')})"
    end
  end

  # Convert a RFC 2425 time into an array of Time objects.
  def self.decode_time_to_time(v) # :nodoc:
    array_datetime_to_time(decode_date_time(v))
  end

  # Convert a RFC 2425 date-time into an array of [year,mon,day,hour,min,sec,secfrac,timezone]
  def self.decode_date_time(v) # :nodoc:
    unless match = %r{^\s*#{Bnf::DATE}T#{Bnf::TIME}\s*$}.match(v)
      raise ::Vcard::InvalidEncodingError, "date-time '#{v}' not valid"
    end
    year, month, day, hour, min, sec, secfrac, tz = match.to_a[1..8]

    [
      # date
      year.to_i, month.to_i, day.to_i,
      # time
      hour.to_i, min.to_i, sec.to_i, secfrac ? secfrac.to_f : 0, tz
    ]
  end

  def self.decode_date_time_to_datetime(v) #:nodoc:
    year, month, day, hour, min, sec = decode_date_time(v)
    # TODO - DateTime understands timezones, so we could decode tz and use it.
    DateTime.civil(year, month, day, hour, min, sec, 0)
  end

  # decode_boolean
  #
  # float
  #
  # float_list

  # Convert an RFC2425 INTEGER value into an Integer
  def self.decode_integer(v) # :nodoc:
    unless %r{\s*#{Bnf::INTEGER}\s*}.match(v)
      raise ::Vcard::InvalidEncodingError, "integer not valid (#{v})"
    end
    v.to_i
  end

  #
  # integer_list

  # Convert a RFC2425 date-list into an array of dates.
  def self.decode_date_list(v) # :nodoc:
    decode_list(v) do |date|
      date.strip!
      if date.length > 0
        decode_date(date)
      end
    end.compact
  end

  # Convert a RFC 2425 time-list into an array of times.
  def self.decode_time_list(v) # :nodoc:
    decode_list(v) do |time|
      time.strip!
      if time.length > 0
        decode_time(time)
      end
    end.compact
  end

  # Convert a RFC 2425 date-time-list into an array of date-times.
  def self.decode_date_time_list(v) # :nodoc:
    decode_list(v) do |datetime|
      datetime.strip!
      if datetime.length > 0
        decode_date_time(datetime)
      end
    end.compact
  end

  # Convert RFC 2425 text into a String.
  # \\ -> \
  # \n -> NL
  # \N -> NL
  # \, -> ,
  # \; -> ;
  #
  # I've seen double-quote escaped by iCal.app. Hmm. Ok, if you aren't supposed
  # to escape anything but the above, everything else is ambiguous, so I'll
  # just support it.
  def self.decode_text(v) # :nodoc:
    # FIXME - I think this should trim leading and trailing space
    v.gsub(/\\(.)/) do
      case $1
      when "n", "N"
        "\n"
      else
        $1
      end
    end
  end

  def self.encode_text(v) #:nodoc:
    v.to_str.gsub(/([\\,;\n])/) { $1 == "\n" ? "\\n" : "\\"+$1 }
  end

  # v is an Array of String, or just a single String
  def self.encode_text_list(v, sep = ",") #:nodoc:
    begin
      v.to_ary.map{ |t| encode_text(t) }.join(sep)
    rescue
      encode_text(v)
    end
  end

  # Convert a +sep+-seperated list of TEXT values into an array of values.
  def self.decode_text_list(value, sep = ",") # :nodoc:
    # Need to do in two stages, as best I can find.
    list = value.scan(/([^#{sep}\\]*(?:\\.[^#{sep}\\]*)*)#{sep}/).map do |v|
      decode_text(v.first)
    end
    if value.match(/([^#{sep}\\]*(?:\\.[^#{sep}\\]*)*)$/)
      list << $1
    end
    list
  end

  # param-value = paramtext / quoted-string
  # paramtext  = *SAFE-CHAR
  # quoted-string      = DQUOTE *QSAFE-CHAR DQUOTE
  def self.encode_paramtext(value)
    case value
    when %r{\A#{Bnf::SAFECHAR}*\z}
      value
    else
      raise ::Vcard::Unencodable, "paramtext #{value.inspect}"
    end
  end

  def self.encode_paramvalue(value)
    case value
    when %r{\A#{Bnf::SAFECHAR}*\z}
      value
    when %r{\A#{Bnf::QSAFECHAR}*\z}
      '"' + value + '"'
    else
      raise ::Vcard::Unencodable, "param-value #{value.inspect}"
    end
  end


  # Unfold the lines in +card+, then return an array of one Field object per
  # line.
  def self.decode(card) #:nodoc:
    unfold(card).collect { |line| DirectoryInfo::Field.decode(line) }
  end


  # Expand an array of fields into its syntactic entities. Each entity is a sequence
  # of fields where the sequences is delimited by a BEGIN/END field. Since
  # BEGIN/END delimited entities can be nested, we build a tree. Each entry in
  # the array is either a Field or an array of entries (where each entry is
  # either a Field, or an array of entries...).
  def self.expand(src) #:nodoc:
    # output array to expand the src to
    dst = []
    # stack used to track our nesting level, as we see begin/end we start a
    # new/finish the current entity, and push/pop that entity from the stack
    current = [ dst ]

    for f in src
      if f.name? "BEGIN"
        e = [ f ]

        current.last.push(e)
        current.push(e)

      elsif f.name? "END"
        current.last.push(f)

        unless current.last.first.value? current.last.last.value
          raise "BEGIN/END mismatch (#{current.last.first.value} != #{current.last.last.value})"
        end

        current.pop

      else
        current.last.push(f)
      end
    end

    dst
  end

  # Split an array into an array of all the fields at the outer level, and
  # an array of all the inner arrays of fields. Return the array [outer,
  # inner].
  def self.outer_inner(fields) #:nodoc:
    # TODO - use Enumerable#partition
    # seperate into the outer-level fields, and the arrays of component
    # fields
    outer = []
    inner = []
    fields.each do |line|
      case line
      when Array; inner << line
      else;       outer << line
      end
    end
    return outer, inner
  end
end


# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

module Vcard

  # Attachments are used by both iCalendar and vCard. They are either a URI or
  # inline data, and their decoded value will be either a Uri or a Inline, as
  # appropriate.
  #
  # Besides the methods specific to their class, both kinds of object implement
  # a set of common methods, allowing them to be treated uniformly:
  # - Uri#to_io, Inline#to_io: return an IO from which the value can be read.
  # - Uri#to_s, Inline#to_s: return the value as a String.
  # - Uri#format, Inline#format: the format of the value. This is supposed to
  #   be an "iana defined" identifier (like "image/jpeg"), but could be almost
  #   anything (or nothing) in practice.  Since the parameter is optional, it may
  #   be "".
  #
  # The objects can also be distinguished by their class, if necessary.
  module Attachment

    # TODO - It might be possible to autodetect the format from the first few
    # bytes of the value, and return the appropriate MIME type when format
    # isn't defined.
    #
    # iCalendar and vCard put the format in different parameters, and the
    # default kind of value is different.
    def Attachment.decode(field, defkind, fmtparam) #:nodoc:
      format = field.pvalue(fmtparam) || ""
      kind = field.kind || defkind
      case kind
      when "text"
        Inline.new(::Vcard.decode_text(field.value), format)
      when "uri"
        Uri.new(field.value_raw, format)
      when "binary"
        Inline.new(field.value, format)
      else
        raise InvalidEncodingError, "Attachment of type #{kind} is not allowed"
      end
    end

    # Extends a String to support some of the same methods as Uri.
    class Inline < String
      def initialize(s, format) #:nodoc:
        @format = format
        super(s)
      end

      # Return an IO object for the inline data. See +stringio+ for more
      # information.
      def to_io
        StringIO.new(self)
      end

      # The format of the inline data.
      # See Attachment.
      attr_reader :format
    end

    # Encapsulates a URI and implements some methods of String.
    class Uri
      def initialize(uri, format) #:nodoc:
        @uri = uri
        @format = format
      end

      # The URI value.
      attr_reader :uri

      # The format of the data referred to by the URI.
      # See Attachment.
      attr_reader :format

      # Return an IO object from opening the URI.  See +open-uri+ for more
      # information.
      def to_io
        open(@uri)
      end

      # Return the String from reading the IO object to end-of-data.
      def to_s
        to_io.read(nil)
      end

      def inspect #:nodoc:
        s = "<#{self.class.to_s}: #{uri.inspect}>"
        s << ", #{@format.inspect}" if @format
        s
      end
    end

  end
end

# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

module Vcard
  # Contains regular expression strings for the EBNF of RFC 2425.
  module Bnf #:nodoc:

    # 1*(ALPHA / DIGIT / "-")
    # Note: I think I can add A-Z here, and get rid of the "i" matches elsewhere.
    # Note: added "_" to allowed because its produced by Notes  (X-LOTUS-CHILD_UID:)
    # Note: added "/" to allowed because its produced by KAddressBook (X-messaging/xmpp-All:)
    # Note: added " " to allowed because its produced by highrisehq.com (X-GOOGLE TALK:)
    NAME    = "[-a-z0-9_/][-a-z0-9_/ ]*"

    # <"> <Any character except CTLs, DQUOTE> <">
    QSTR    = '"([^"]*)"'

    # *<Any character except CTLs, DQUOTE, ";", ":", ",">
    PTEXT   = '([^";:,]+)'

    # param-value = ptext / quoted-string
    PVALUE  = "(?:#{QSTR}|#{PTEXT})"

    # param = name "=" param-value *("," param-value)
    # Note: v2.1 allows a type or encoding param-value to appear without the type=
    # or the encoding=. This is hideous, but we try and support it, if there
    # is no "=", then $2 will be "", and we will treat it as a v2.1 param.
    PARAM = ";(#{NAME})(=?)((?:#{PVALUE})?(?:,#{PVALUE})*)"

    # V3.0: contentline  =   [group "."]  name *(";" param) ":" value
    # V2.1: contentline  = *( group "." ) name *(";" param) ":" value
    #
    # We accept the V2.1 syntax for backwards compatibility.
    #LINE = "((?:#{NAME}\\.)*)?(#{NAME})([^:]*)\:(.*)"
    LINE = "^((?:#{NAME}\\.)*)?(#{NAME})((?:#{PARAM})*):(.*)$"

    # date = date-fullyear ["-"] date-month ["-"] date-mday
    # date-fullyear = 4 DIGIT
    # date-month = 2 DIGIT
    # date-mday = 2 DIGIT
    DATE = "(\d\d\d\d)-?(\d\d)-?(\d\d)"

    # time = time-hour [":"] time-minute [":"] time-second [time-secfrac] [time-zone]
    # time-hour = 2 DIGIT
    # time-minute = 2 DIGIT
    # time-second = 2 DIGIT
    # time-secfrac = "," 1*DIGIT
    # time-zone = "Z" / time-numzone
    # time-numzone = sign time-hour [":"] time-minute
    TIME = "(\d\d):?(\d\d):?(\d\d)(\.\d+)?(Z|[-+]\d\d:?\d\d)?"

    # integer = (["+"] / "-") 1*DIGIT
    INTEGER = "[-+]?\d+"

    # QSAFE-CHAR = WSP / %x21 / %x23-7E / NON-US-ASCII
    #  ; Any character except CTLs and DQUOTE
    QSAFECHAR = "[ \t\x21\x23-\x7e\x80-\xff]"

    # SAFE-CHAR  = WSP / %x21 / %x23-2B / %x2D-39 / %x3C-7E / NON-US-ASCII
    #   ; Any character except CTLs, DQUOTE, ";", ":", ","
    SAFECHAR = "[ \t\x21\x23-\x2b\x2d-\x39\x3c-\x7e\x80-\xff]"
  end
end

# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

module Vcard
  # An RFC 2425 directory info object.
  #
  # A directory information object is a sequence of fields. The basic
  # structure of the object, and the way in which it is broken into fields
  # is common to all profiles of the directory info type.
  #
  # A vCard, for example, is a specialization of a directory info object.
  #
  # - [RFC2425] the directory information framework (ftp://ftp.ietf.org/rfc/rfc2425.txt)
  #
  # Here's an example of encoding a simple vCard using the low-level APIs:
  #
  #   card = Vcard::Vcard.create
  #   card << Vcard::DirectoryInfo::Field.create("EMAIL", "user.name@example.com", "TYPE" => "INTERNET" )
  #   card << Vcard::DirectoryInfo::Field.create("URL", "http://www.example.com/user" )
  #   card << Vcard::DirectoryInfo::Field.create("FN", "User Name" )
  #   puts card.to_s
  #
  # Don't do it like that, use Vcard::Vcard::Maker.
  class DirectoryInfo
    include Enumerable

    private_class_method :new

    # Initialize a DirectoryInfo object from +fields+. If +profile+ is
    # specified, check the BEGIN/END fields.
    def initialize(fields, profile = nil) #:nodoc:
      if fields.detect { |f| ! f.kind_of? DirectoryInfo::Field }
        raise ArgumentError, "fields must be an array of DirectoryInfo::Field objects"
      end

      @string = nil # this is used as a flag to indicate that recoding will be necessary
      @fields = fields

      check_begin_end(profile) if profile
    end

    # Decode +card+ into a DirectoryInfo object.
    #
    # +card+ may either be a something that is convertible to a string using
    # #to_str or an Array of objects that can be joined into a string using
    # #join("\n"), or an IO object (which will be read to end-of-file).
    #
    # The lines in the string may be delimited using IETF (CRLF) or Unix (LF) conventions.
    #
    # A DirectoryInfo is mutable, you can add new fields to it, see
    # Vcard::DirectoryInfo::Field#create() for how to create a new Field.
    #
    # TODO: I don't believe this is ever used, maybe I can remove it.
    def DirectoryInfo.decode(card) #:nodoc:
      if card.respond_to? :to_str
        string = card.to_str
      elsif card.kind_of? Array
        string = card.join("\n")
      elsif card.kind_of? IO
        string = card.read(nil)
      else
        raise ArgumentError, "DirectoryInfo cannot be created from a #{card.type}"
      end

      fields = ::Vcard.decode(string)

      new(fields)
    end

    # Create a new DirectoryInfo object. The +fields+ are an optional array of
    # DirectoryInfo::Field objects to add to the new object, between the
    # BEGIN/END.  If the +profile+ string is not nil, then it is the name of
    # the directory info profile, and the BEGIN:+profile+/END:+profile+ fields
    # will be added.
    #
    # A DirectoryInfo is mutable, you can add new fields to it using #push(),
    # and see Field#create().
    def DirectoryInfo.create(fields = [], profile = nil)

      if profile
        p = profile.to_str
        f = [ Field.create("BEGIN", p) ]
        f.concat fields
        f.push Field.create("END", p)
        fields = f
      end

      new(fields, profile)
    end

    # The first field named +name+, or nil if no
    # match is found.
    def field(name)
      enum_by_name(name).each { |f| return f }
      nil
    end

    # The value of the first field named +name+, or nil if no
    # match is found.
    def [](name)
      enum_by_name(name).each { |f| return f.value if f.value != ""}
      enum_by_name(name).each { |f| return f.value }
      nil
    end

    # An array of all the values of fields named +name+, converted to text
    # (using Field#to_text()).
    #
    # TODO - call this #texts(), as in the plural?
    def text(name)
      accum = []
      each do |f|
        if f.name? name
          accum << f.to_text
        end
      end
      accum
    end

    # Array of all the Field#group()s.
    def groups
      @fields.collect { |f| f.group } .compact.uniq
    end

    # All fields, frozen.
    def fields #:nodoc:
      @fields.dup.freeze
    end

    # Yields for each Field for which +cond+.call(field) is true. The
    # (default) +cond+ of nil is considered true for all fields, so
    # this acts like a normal #each() when called with no arguments.
    def each(cond = nil) # :yields: Field
      @fields.each do |field|
         if(cond == nil || cond.call(field))
           yield field
         end
      end
      self
    end

    # Returns an Enumerator for each Field for which #name?(+name+) is true.
    #
    # An Enumerator supports all the methods of Enumerable, so it allows iteration,
    # collection, mapping, etc.
    #
    # Examples:
    #
    # Print all the nicknames in a card:
    #
    #   card.enum_by_name("NICKNAME") { |f| puts f.value }
    #
    # Print an Array of the preferred email addresses in the card:
    #
    #   pref_emails = card.enum_by_name("EMAIL").select { |f| f.pref? }
    def enum_by_name(name)
      Enumerator.new(self, Proc.new { |field| field.name?(name) })
    end

    # Returns an Enumerator for each Field for which #group?(+group+) is true.
    #
    # For example, to print all the fields, sorted by group, you could do:
    #
    #   card.groups.sort.each do |group|
    #     card.enum_by_group(group).each do |field|
    #       puts "#{group} -> #{field.name}"
    #     end
    #   end
    #
    # or to get an array of all the fields in group "AGROUP", you could do:
    #
    #   card.enum_by_group("AGROUP").to_a
    def enum_by_group(group)
      Enumerator.new(self, Proc.new { |field| field.group?(group) })
    end

    # Returns an Enumerator for each Field for which +cond+.call(field) is true.
    def enum_by_cond(cond)
      Enumerator.new(self, cond )
    end

    # Force card to be reencoded from the fields.
    def dirty #:nodoc:
      #string = nil
    end

    # Append +field+ to the fields. Note that it won't be literally appended
    # to the fields, it will be inserted before the closing END field.
    def push(field)
      dirty
      @fields[-1,0] = field
      self
    end

    alias << push

    # Push +field+ onto the fields, unless there is already a field
    # with this name.
    def push_unique(field)
      push(field) unless @fields.detect { |f| f.name? field.name }
      self
    end

    # Append +field+ to the end of all the fields. This isn't usually what you
    # want to do, usually a DirectoryInfo's first and last fields are a
    # BEGIN/END pair, see #push().
    def push_end(field)
      @fields << field
      self
    end

    # Delete +field+.
    #
    # Warning: You can't delete BEGIN: or END: fields, but other
    # profile-specific fields can be deleted, including mandatory ones. For
    # vCards in particular, in order to avoid destroying them, I suggest
    # creating a new Vcard, and copying over all the fields that you still
    # want, rather than using #delete. This is easy with Vcard::Maker#copy, see
    # the Vcard::Maker examples.
    def delete(field)
      case
      when field.name?("BEGIN"), field.name?("END")
        raise ArgumentError, "Cannot delete BEGIN or END fields."
      else
        @fields.delete field
      end

      self
    end

    # The string encoding of the DirectoryInfo. See Field#encode for information
    # about the width parameter.
    def encode(width=nil)
      unless @string
        @string = @fields.collect { |f| f.encode(width) } . join ""
      end
      @string
    end

    alias to_s encode

    # Check that the DirectoryInfo object is correctly delimited by a BEGIN
    # and END, that their profile values match, and if +profile+ is specified, that
    # they are the specified profile.
    def check_begin_end(profile=nil) #:nodoc:
      unless @fields.first
        raise "No fields to check"
      end
      unless @fields.first.name? "BEGIN"
        raise "Needs BEGIN, found: #{@fields.first.encode nil}"
      end
      unless @fields.last.name? "END"
        raise "Needs END, found: #{@fields.last.encode nil}"
      end
      unless @fields.last.value? @fields.first.value
        raise "BEGIN/END mismatch: (#{@fields.first.value} != #{@fields.last.value}"
      end
      if profile
        if ! @fields.first.value? profile
          raise "Mismatched profile"
        end
      end
      true
    end
  end
end

# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

module Vcard
  # This is a way for an object to have multiple ways of being enumerated via
  # argument to it's #each() method. An Enumerator mixes in Enumerable, so the
  # standard APIs such as Enumerable#map(), Enumerable#to_a(), and
  # Enumerable#find_all() can be used on it.
  #
  # TODO since 1.8, this is part of the standard library, I should rewrite vPim
  # so this can be removed.
  class Enumerator
    include Enumerable

    def initialize(obj, *args)
      @obj = obj
      @args = args
    end

    def each(&block)
      @obj.each(*@args, &block)
    end
  end
end

# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

module Vcard
  # Exception used to indicate that data being decoded is invalid, the message
  # should describe what is invalid.
  class InvalidEncodingError < StandardError; end

  # Exception used to indicate that data being decoded is unsupported, the message
  # should describe what is unsupported.
  #
  # If its unsupported, its likely because I didn't anticipate it being useful
  # to support this, and it likely it could be supported on request.
  class UnsupportedError < StandardError; end

  # Exception used to indicate that encoding failed, probably because the
  # object would not result in validly encoded data. The message should
  # describe what is unsupported.
  class Unencodeable < StandardError; end
end

# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify it
# under the same terms as the ruby language itself, see the file COPYING for
# details.

module Vcard

  class DirectoryInfo

    # A field in a directory info object.
    class Field
      # TODO
      # - Field should know which param values and field values are
      #   case-insensitive, configurably, so it can down case them
      # - perhaps should have pvalue_set/del/add, perhaps case-insensitive, or
      #   pvalue_iset/idel/iadd, where set sets them all, add adds if not present,
      #   and del deletes any that are present
      # - I really, really, need a case-insensitive string...
      # - should allow nil as a field value, its not the same as "", if there is
      #   more than one pvalue, the empty string will show up. This isn't strictly
      #   disallowed, but its odd. Should also strip empty strings on decoding, if
      #   I don't already.
      private_class_method :new

      def Field.create_array(fields)
        case fields
        when Hash
          fields.map do |name,value|
            DirectoryInfo::Field.create( name, value )
          end
        else
          fields.to_ary
        end
      end

      # Encode a field.
      def Field.encode0(group, name, params={}, value="") # :nodoc:
        line = ""

        # A reminder of the line format:
        #   [<group>.]<name>;<pname>=<pvalue>,<pvalue>:<value>

        if group
          line << group << "."
        end

        line << name

        params.each do |pname, pvalues|

          unless pvalues.respond_to? :to_ary
            pvalues = [ pvalues ]
          end

          line << ";" << pname << "="

          sep = "" # set to "," after one pvalue has been appended

          pvalues.each do |pvalue|
            # check if we need to do any encoding
            if pname.casecmp("ENCODING") == 0 && pvalue == :b64
              pvalue = "B" # the RFC definition of the base64 param value
              value = [ value.to_str ].pack("m").gsub("\n", "")
            end

            line << sep << pvalue
            sep =",";
          end
        end

        line << ":"

        line << Field.value_str(value)

        line
      end

      def Field.value_str(value) # :nodoc:
        line = ""
        case value
        when Date
          line << ::Vcard.encode_date(value)

        when Time #, DateTime
          line << ::Vcard.encode_date_time(value)

        when Array
          line << value.map { |v| Field.value_str(v) }.join(";")

        when Symbol
          line << value

        else
          # FIXME - somewhere along here, values with special chars need escaping...
          line << value.to_str
        end
        line
      end

      # Decode a field.
      def Field.decode0(atline) # :nodoc:
        unless atline =~ %r{#{Bnf::LINE}}i
          raise ::Vcard::InvalidEncodingError, atline
        end

        atgroup = $1.upcase
        atname = $2.upcase
        paramslist = $3
        atvalue = $~[-1]

        # I've seen space that shouldn't be there, as in "BEGIN:VCARD ", so
        # strip it. I'm not absolutely sure this is allowed... it certainly
        # breaks round-trip encoding.
        atvalue.strip!

        if atgroup.length > 0
          atgroup.chomp!(".")
        else
          atgroup = nil
        end

        atparams = {}

        # Collect the params, if any.
        if paramslist.size > 1

          # v3.0 and v2.1 params
          paramslist.scan( %r{#{Bnf::PARAM}}i ) do

            # param names are case-insensitive, and multi-valued
            name = $1.upcase
            params = $3

            # v2.1 params have no "=" sign, figure out what kind of param it
            # is (either its a known encoding, or we treat it as a "TYPE"
            # param).

            if $2 == ""
              params = $1
              case $1
              when /quoted-printable/i
                name = "ENCODING"

              when /base64/i
                name = "ENCODING"

              else
                name = "TYPE"
              end
            end

            # TODO - In ruby1.8 I can give an initial value to the atparams
            # hash values instead of this.
            unless atparams.key? name
              atparams[name] = []
            end

            params.scan( %r{#{Bnf::PVALUE}} ) do
              atparams[name] << ($1 || $2)
            end
          end
        end

        [ atgroup, atname, atparams, atvalue ]
      end

      def initialize(line) # :nodoc:
        @line = line.to_str
        @group, @name, @params, @value = Field.decode0(@line)

        @params.each do |pname,pvalues|
          pvalues.freeze
        end
        self
      end

      # Create a field by decoding +line+, a String which must already be
      # unfolded. Decoded fields are frozen, but see #copy().
      def Field.decode(line)
        new(line).freeze
      end

      # Create a field with name +name+ (a String), value +value+ (see below),
      # and optional parameters, +params+. +params+ is a hash of the parameter
      # name (a String) to either a single string or symbol, or an array of
      # strings and symbols (parameters can be multi-valued).
      #
      # If "ENCODING" => :b64 is specified as a parameter, the value will be
      # base-64 encoded. If it's already base-64 encoded, then use String
      # values ("ENCODING" => "B"), and no further encoding will be done by
      # this routine.
      #
      # Currently handled value types are:
      # - Time, encoded as a date-time value
      # - Date, encoded as a date value
      # - String, encoded directly
      # - Array of String, concatentated with ";" between them.
      #
      # TODO - need a way to encode String values as TEXT, at least optionally,
      # so as to escape special chars, etc.
      def Field.create(name, value="", params={})
        line = Field.encode0(nil, name, params, value)

        begin
          new(line)
        rescue ::Vcard::InvalidEncodingError => e
          raise ArgumentError, e.to_s
        end
      end

      # Create a copy of Field. If the original Field was frozen, this one
      # won't be.
      def copy
        Marshal.load(Marshal.dump(self))
      end

      # The String encoding of the Field. The String will be wrapped to a
      # maximum line width of +width+, where +0+ means no wrapping, and nil is
      # to accept the default wrapping (75, recommended by RFC2425).
      #
      # Note: AddressBook.app 3.0.3 neither understands to unwrap lines when it
      # imports vCards (it treats them as raw new-line characters), nor wraps
      # long lines on export. This is mostly a cosmetic problem, but wrapping
      # can be disabled by setting width to +0+, if desired.
      #
      # FIXME - breaks round-trip encoding, need to change this to not wrap
      # fields that are already wrapped.
      def encode(width=nil)
        width = 75 unless width
        l = @line
        # Wrap to width, unless width is zero.
        if width > 0
          l = l.gsub(/.{#{width},#{width}}/) { |m| m + "\n " }
        end
        # Make sure it's terminated with no more than a single NL.
        l.gsub(/\s*\z/, "") + "\n"
      end

      alias to_s encode

      # The name.
      def name
        @name
      end

      # The group, if present, or nil if not present.
      def group
        @group
      end

      # An Array of all the param names.
      def pnames
        @params.keys
      end

      # FIXME - remove my own uses of #params
      alias params pnames # :nodoc:

      # The first value of the param +name+,  nil if there is no such param,
      # the param has no value, or the first param value is zero-length.
      def pvalue(name)
        v = pvalues( name )
        if v
          v = v.first
        end
        if v
          v = nil unless v.length > 0
        end
        v
      end

      # The Array of all values of the param +name+,  nil if there is no such
      # param, [] if the param has no values. If the Field isn't frozen, the
      # Array is mutable.
      def pvalues(name)
        @params[name.upcase]
      end

      # FIXME - remove my own uses of #param
      alias param pvalues # :nodoc:

      alias [] pvalues

      # Yield once for each param, +name+ is the parameter name, +value+ is an
      # array of the parameter values.
      def each_param(&block) #:yield: name, value
        if @params
          @params.each(&block)
        end
      end

      # The decoded value.
      #
      # The encoding specified by the #encoding, if any, is stripped.
      #
      # Note: Both the RFC 2425 encoding param ("b", meaning base-64) and the
      # vCard 2.1 encoding params ("base64", "quoted-printable", "8bit", and
      # "7bit") are supported.
      #
      # FIXME:
      # - should use the VALUE parameter
      # - should also take a default value type, so it can be converted
      #   if VALUE parameter is not present.
      def value
        case encoding
        when nil, "8BIT", "7BIT" then @value

          # Hack - if the base64 lines started with 2 SPC chars, which is invalid,
          # there will be extra spaces in @value. Since no SPC chars show up in
          # b64 encodings, they can be safely stripped out before unpacking.
        when "B", "BASE64"       then @value.gsub(" ", "").unpack("m*").first

        when "QUOTED-PRINTABLE"  then @value.unpack("M*").first

        else
          raise ::Vcard::InvalidEncodingError, "unrecognized encoding (#{encoding})"
        end
      end

      # Is the #name of this Field +name+? Names are case insensitive.
      def name?(name)
        @name.casecmp(name) == 0
      end

      # Is the #group of this field +group+? Group names are case insensitive.
      # A +group+ of nil matches if the field has no group.
      def group?(group)
        @group.casecmp(group) == 0
      end

      # Is the value of this field of type +kind+? RFC2425 allows the type of
      # a fields value to be encoded in the VALUE parameter. Don't rely on its
      # presence, they aren't required, and usually aren't bothered with. In
      # cases where the kind of value might vary (an iCalendar DTSTART can be
      # either a date or a date-time, for example), you are more likely to see
      # the kind of value specified explicitly.
      #
      # The value types defined by RFC 2425 are:
      # - uri:
      # - text:
      # - date: a list of 1 or more dates
      # - time: a list of 1 or more times
      # - date-time: a list of 1 or more date-times
      # - integer:
      # - boolean:
      # - float:
      def kind?(kind)
        self.kind.casecmp(kind) == 0
      end

      # Is one of the values of the TYPE parameter of this field +type+? The
      # type parameter values are case insensitive. False if there is no TYPE
      # parameter.
      #
      # TYPE parameters are used for general categories, such as
      # distinguishing between an email address used at home or at work.
      def type?(type)
        type = type.to_str

        types = param("TYPE")

        if types
          types = types.detect { |t| t.casecmp(type) == 0 }
        end
      end

      # Is this field marked as preferred? A vCard field is preferred if
      # #type?("PREF"). This method is not necessarily meaningful for
      # non-vCard profiles.
      def pref?
        type? "PREF"
      end

      # Set whether a field is marked as preferred. See #pref?
      def pref=(ispref)
        if ispref
          pvalue_iadd("TYPE", "PREF")
        else
          pvalue_idel("TYPE", "PREF")
        end
      end

      # Is the value of this field +value+? The check is case insensitive.
      # FIXME - it shouldn't be insensitive, make a #casevalue? method.
      def value?(value)
        @value.casecmp(value) == 0
      end

      # The value of the ENCODING parameter, if present, or nil if not
      # present.
      def encoding
        e = param("ENCODING")

        if e
          if e.length > 1
            raise ::Vcard::InvalidEncodingError, "multi-valued param 'ENCODING' (#{e})"
          end
          e = e.first.upcase
        end
        e
      end

      # The type of the value, as specified by the VALUE parameter, nil if
      # unspecified.
      def kind
        v = param("VALUE")
        if v
          if v.size > 1
            raise InvalidEncodingError, "multi-valued param 'VALUE' (#{values})"
          end
          v = v.first.downcase
        end
        v
      end

      # The value as an array of Time objects (all times and dates in
      # RFC2425 are lists, even where it might not make sense, such as a
      # birthday). The time will be UTC if marked as so (with a timezone of
      # "Z"), and in localtime otherwise.
      #
      # TODO - support timezone offsets
      #
      # TODO - if year is before 1970, this won't work... but some people
      # are generating calendars saying Canada Day started in 1753!
      # That's just wrong! So, what to do? I add a message
      # saying what the year is that breaks, so they at least know that
      # its ridiculous! I think I need my own DateTime variant.
      def to_time
        begin
          ::Vcard.decode_date_time_list(value).collect do |d|
            # We get [ year, month, day, hour, min, sec, usec, tz ]
            begin
              if(d.pop == "Z")
                Time.gm(*d)
              else
                Time.local(*d)
              end
            rescue ArgumentError => e
              raise ::Vcard::InvalidEncodingError, "Time.gm(#{d.join(', ')}) failed with #{e.message}"
            end
          end
        rescue ::Vcard::InvalidEncodingError
          ::Vcard.decode_date_list(value).collect do |d|
            # We get [ year, month, day ]
            begin
              Time.gm(*d)
            rescue ArgumentError => e
              raise ::Vcard::InvalidEncodingError, "Time.gm(#{d.join(', ')}) failed with #{e.message}"
            end
          end
        end
      end

      # The value as an array of Date objects (all times and dates in
      # RFC2425 are lists, even where it might not make sense, such as a
      # birthday).
      #
      # The field value may be a list of either DATE or DATE-TIME values,
      # decoding is tried first as a DATE-TIME, then as a DATE, if neither
      # works an InvalidEncodingError will be raised.
      def to_date
        begin
          ::Vcard.decode_date_time_list(value).collect do |d|
            # We get [ year, month, day, hour, min, sec, usec, tz ]
            Date.new(d[0], d[1], d[2])
          end
        rescue ::Vcard::InvalidEncodingError
          ::Vcard.decode_date_list(value).collect do |d|
            # We get [ year, month, day ]
            Date.new(*d)
          end
        end
      end

      # The value as text. Text can have escaped newlines, commas, and escape
      # characters, this method will strip them, if present.
      #
      # In theory, #value could also do this, but it would need to know that
      # the value is of type "TEXT", and often for text values the "VALUE"
      # parameter is not present, so knowledge of the expected type of the
      # field is required from the decoder.
      def to_text
        ::Vcard.decode_text(value)
      end

      # The undecoded value, see +value+.
      def value_raw
        @value
      end

      # TODO def pretty_print() ...

      # Set the group of this field to +group+.
      def group=(group)
        mutate(group, @name, @params, @value)
        group
      end

      # Set the value of this field to +value+.  Valid values are as in
      # Field.create().
      def value=(value)
        mutate(@group, @name, @params, value)
        value
      end

      # Convert +value+ to text, then assign.
      #
      # TODO - unimplemented
      def text=(text)
      end

      # Set a the param +pname+'s value to +pvalue+, replacing any value it
      # currently has. See Field.create() for a description of +pvalue+.
      #
      # Example:
      #  if field["TYPE"]
      #    field["TYPE"] << "HOME"
      #  else
      #    field["TYPE"] = [ "HOME" ]
      #  end
      #
      # TODO - this could be an alias to #pvalue_set
      def []=(pname,pvalue)
        unless pvalue.respond_to?(:to_ary)
          pvalue = [ pvalue ]
        end

        h = @params.dup

        h[pname.upcase] = pvalue

        mutate(@group, @name, h, @value)
        pvalue
      end

      # Add +pvalue+ to the param +pname+'s value. The values are treated as a
      # set so duplicate values won't occur, and String values are case
      # insensitive.  See Field.create() for a description of +pvalue+.
      def pvalue_iadd(pname, pvalue)
        pname = pname.upcase

        # Get a uniq set, where strings are compared case-insensitively.
        values = [ pvalue, @params[pname] ].flatten.compact
        values = values.collect do |v|
          if v.respond_to? :to_str
            v = v.to_str.upcase
          end
          v
        end
        values.uniq!

        h = @params.dup

        h[pname] = values

        mutate(@group, @name, h, @value)
        values
      end

      # Delete +pvalue+ from the param +pname+'s value. The values are treated
      # as a set so duplicate values won't occur, and String values are case
      # insensitive.  +pvalue+ must be a single String or Symbol.
      def pvalue_idel(pname, pvalue)
        pname = pname.upcase
        if pvalue.respond_to? :to_str
          pvalue = pvalue.to_str.downcase
        end

        # Get a uniq set, where strings are compared case-insensitively.
        values = [ nil, @params[pname] ].flatten.compact
        values = values.collect do |v|
          if v.respond_to? :to_str
            v = v.to_str.downcase
          end
          v
        end
        values.uniq!
        values.delete pvalue

        h = @params.dup

        h[pname] = values

        mutate(@group, @name, h, @value)
        values
      end

      # FIXME - should change this so it doesn't assign to @line here, so @line
      # is used to preserve original encoding. That way, #encode can only wrap
      # new fields, not old fields.
      def mutate(g, n, p, v) #:nodoc:
        line = Field.encode0(g, n, p, v)

        begin
          @group, @name, @params, @value = Field.decode0(line)
          @line = line
        rescue ::Vcard::InvalidEncodingError => e
          raise ArgumentError, e.to_s
        end
        self
      end

      private :mutate
    end
  end
end


# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

module Vcard
  # A vCard, a specialization of a directory info object.
  #
  # The vCard format is specified by:
  # - RFC2426[http://www.ietf.org/rfc/rfc2426.txt]: vCard MIME Directory Profile (vCard 3.0)
  # - RFC2425[http://www.ietf.org/rfc/rfc2425.txt]: A MIME Content-Type for Directory Information
  #
  # This implements vCard 3.0, but it is also capable of working with vCard 2.1
  # if used with care.
  #
  # All line values can be accessed with Vcard#value, Vcard#values, or even by
  # iterating through Vcard#lines. Line types that don't have specific support
  # and non-standard line types ("X-MY-SPECIAL", for example) will be returned
  # as a String, with any base64 or quoted-printable encoding removed.
  #
  # Specific support exists to return more useful values for the standard vCard
  # types, where appropriate.
  #
  # The wrapper functions (#birthday, #nicknames, #emails, etc.) exist
  # partially as an API convenience, and partially as a place to document
  # the values returned for the more complex types, like PHOTO and EMAIL.
  #
  # For types that do not sensibly occur multiple times (like BDAY or GEO),
  # sometimes a wrapper exists only to return a single line, using #value.
  # However, if you find the need, you can still call #values to get all the
  # lines, and both the singular and plural forms will eventually be
  # implemented.
  #
  # For more information see:
  # - RFC2426[http://www.ietf.org/rfc/rfc2426.txt]: vCard MIME Directory Profile (vCard 3.0)
  # - RFC2425[http://www.ietf.org/rfc/rfc2425.txt]: A MIME Content-Type for Directory Information
  # - vCard2.1[http://www.imc.org/pdi/pdiproddev.html]: vCard 2.1 Specifications
  #
  # vCards are usually transmitted in files with <code>.vcf</code>
  # extensions.
  #
  # = Examples
  #
  # - link:ex_mkvcard.txt: example of creating a vCard
  # - link:ex_cpvcard.txt: example of copying and them modifying a vCard
  # - link:ex_mkv21vcard.txt: example of creating version 2.1 vCard
  # - link:mutt-aliases-to-vcf.txt: convert a mutt aliases file to vCards
  # - link:ex_get_vcard_photo.txt: pull photo data from a vCard
  # - link:ab-query.txt: query the OS X Address Book to find vCards
  # - link:vcf-to-mutt.txt: query vCards for matches, output in formats useful
  #   with Mutt (see link:README.mutt for details)
  # - link:tabbed-file-to-vcf.txt: convert a tab-delimited file to vCards, a
  #   (small but) complete application contributed by Dane G. Avilla, thanks!
  # - link:vcf-to-ics.txt: example of how to create calendars of birthdays from vCards
  # - link:vcf-dump.txt: utility for dumping contents of .vcf files
  class Vcard < DirectoryInfo

    # Represents the value of an ADR field.
    #
    # #location, #preferred, and #delivery indicate information about how the
    # address is to be used, the other attributes are parts of the address.
    #
    # Using values other than those defined for #location or #delivery is
    # unlikely to be portable, or even conformant.
    #
    # All attributes are optional. #location and #delivery can be set to arrays
    # of strings.
    class Address
      # post office box (String)
      attr_accessor :pobox
      # seldom used, its not clear what it is for (String)
      attr_accessor :extended
      # street address (String)
      attr_accessor :street
      # usually the city (String)
      attr_accessor :locality
      # usually the province or state (String)
      attr_accessor :region
      # postal code (String)
      attr_accessor :postalcode
      # country name (String)
      attr_accessor :country
      # home, work (Array of String): the location referred to by the address
      attr_accessor :location
      # true, false (boolean): where this is the preferred address (for this location)
      attr_accessor :preferred
      # postal, parcel, dom (domestic), intl (international) (Array of String): delivery
      # type of this address
      attr_accessor :delivery

      # nonstandard types, their meaning is undefined (Array of String). These
      # might be found during decoding, but shouldn't be set during encoding.
      attr_reader :nonstandard

      # Used to simplify some long and tedious code. These symbols are in the
      # order required for the ADR field structured TEXT value, the order
      # cannot be changed.
      @@adr_parts = [
        :@pobox,
        :@extended,
        :@street,
        :@locality,
        :@region,
        :@postalcode,
        :@country,
      ]

      # TODO
      # - #location?
      # - #delivery?
      def initialize #:nodoc:
        # TODO - Add #label to support LABEL. Try to find LABEL
        # in either same group, or with sam params.
        @@adr_parts.each do |part|
          instance_variable_set(part, "")
        end

        @location = []
        @preferred = false
        @delivery = []
        @nonstandard = []
      end

      def encode #:nodoc:
        parts = @@adr_parts.map do |part|
          instance_variable_get(part)
        end

        value = ::Vcard.encode_text_list(parts, ";")

        params = [ @location, @delivery, @nonstandard ]
        params << "pref" if @preferred
        params = params.flatten.compact.map { |s| s.to_str.downcase }.uniq

        paramshash = {}

        paramshash["TYPE"] = params if params.first

        ::Vcard::DirectoryInfo::Field.create( "ADR", value, paramshash)
      end

      def Address.decode(card, field) #:nodoc:
        adr = new

        parts = ::Vcard.decode_text_list(field.value_raw, ";")

        @@adr_parts.each_with_index do |part,i|
          adr.instance_variable_set(part, parts[i] || "")
        end

        params = field.pvalues("TYPE")

        if params
          params.each do |p|
            p.downcase!
            case p
            when "home", "work"
              adr.location << p
            when "postal", "parcel", "dom", "intl"
              adr.delivery << p
            when "pref"
              adr.preferred = true
            else
              adr.nonstandard << p
            end
          end
          # Strip duplicates
          [ adr.location, adr.delivery, adr.nonstandard ].each do |a|
            a.uniq!
          end
        end

        adr
      end
    end

    # Represents the value of an EMAIL field.
    class Email < String
      # true, false (boolean): whether this is the preferred email address
      attr_accessor :preferred
      # internet, x400 (String): the email address format, rarely specified
      # since the default is "internet"
      attr_accessor :format
      # home, work (Array of String): the location referred to by the address. The
      # inclusion of location parameters in a vCard seems to be non-conformant,
      # strictly speaking, but also seems to be widespread.
      attr_accessor :location
      # nonstandard types, their meaning is undefined (Array of String). These
      # might be found during decoding, but shouldn't be set during encoding.
      attr_reader :nonstandard

      def initialize(email="") #:nodoc:
        @preferred = false
        @format = "internet"
        @location = []
        @nonstandard = []
        super(email)
      end

      def inspect #:nodoc:
        s = "#<#{self.class.to_s}: #{to_str.inspect}"
        s << ", pref" if preferred
        s << ", #{format}" if format != "internet"
        s << ", " << @location.join(", ") if @location.first
        s << ", #{@nonstandard.join(", ")}" if @nonstandard.first
        s
      end

      def encode #:nodoc:
        value = to_str.strip

        if value.length < 1
          raise InvalidEncodingError, "EMAIL must have a value"
        end

        params = [ @location, @nonstandard ]
        params << @format if @format != "internet"
        params << "pref"  if @preferred

        params = params.flatten.compact.map { |s| s.to_str.downcase }.uniq

        paramshash = {}

        paramshash["TYPE"] = params if params.first

        ::Vcard::DirectoryInfo::Field.create("EMAIL", value, paramshash)
      end

      def Email.decode(field) #:nodoc:
        value = field.to_text.strip

        if value.length < 1
          raise InvalidEncodingError, "EMAIL must have a value"
        end

        eml = Email.new(value)

        params = field.pvalues("TYPE")

        if params
          params.each do |p|
            p.downcase!
            case p
            when "home", "work"
              eml.location << p
            when "pref"
              eml.preferred = true
            when "x400", "internet"
              eml.format = p
            else
              eml.nonstandard << p
            end
          end
          # Strip duplicates
          [ eml.location, eml.nonstandard ].each do |a|
            a.uniq!
          end
        end

        eml
      end
    end

    # Represents the value of a TEL field.
    #
    # The value is supposed to be a "X.500 Telephone Number" according to RFC
    # 2426, but that standard is not freely available. Otherwise, anything that
    # looks like a phone number should be OK.
    class Telephone < String
      # true, false (boolean): whether this is the preferred email address
      attr_accessor :preferred
      # home, work, cell, car, pager (Array of String): the location
      # of the device
      attr_accessor :location
      # voice, fax, video, msg, bbs, modem, isdn, pcs (Array of String): the
      # capabilities of the device
      attr_accessor :capability
      # nonstandard types, their meaning is undefined (Array of String). These
      # might be found during decoding, but shouldn't be set during encoding.
      attr_reader :nonstandard

      def initialize(telephone="") #:nodoc:
        @preferred = false
        @location = []
        @capability = []
        @nonstandard = []
        super(telephone)
      end

      def inspect #:nodoc:
        s = "#<#{self.class.to_s}: #{to_str.inspect}"
        s << ", pref" if preferred
        s << ", " << @location.join(", ") if @location.first
        s << ", " << @capability.join(", ") if @capability.first
        s << ", #{@nonstandard.join(", ")}" if @nonstandard.first
        s
      end

      def encode #:nodoc:
        value = to_str.strip

        if value.length < 1
          raise InvalidEncodingError, "TEL must have a value"
        end

        params = [ @location, @capability, @nonstandard ]
        params << "pref"  if @preferred

        params = params.flatten.compact.map { |s| s.to_str.downcase }.uniq

        paramshash = {}

        paramshash["TYPE"] = params if params.first

        ::Vcard::DirectoryInfo::Field.create( "TEL", value, paramshash)
      end

      def Telephone.decode(field) #:nodoc:
        value = field.to_text.strip

        if value.length < 1
          raise InvalidEncodingError, "TEL must have a value"
        end

        tel = Telephone.new(value)

        params = field.pvalues("TYPE")

        if params
          params.each do |p|
            p.downcase!
            case p
            when "home", "work", "cell", "car", "pager"
              tel.location << p
            when "voice", "fax", "video", "msg", "bbs", "modem", "isdn", "pcs"
              tel.capability << p
            when "pref"
              tel.preferred = true
            else
              tel.nonstandard << p
            end
          end
          # Strip duplicates
          [ tel.location, tel.capability, tel.nonstandard ].each do |a|
            a.uniq!
          end
        end

        tel
      end
    end

    # The name from a vCard, including all the components of the N: and FN:
    # fields.
    class Name
      # family name, from N
      attr_accessor :family
      # given name, from N
      attr_accessor :given
      # additional names, from N
      attr_accessor :additional
      # such as "Ms." or "Dr.", from N
      attr_accessor :prefix
      # such as "BFA", from N
      attr_accessor :suffix
      # full name, the FN field. FN is a formatted version of the N field,
      # intended to be in a form more aligned with the cultural conventions of
      # the vCard owner than +formatted+ is.
      attr_accessor :fullname
      # all the components of N formtted as "#{prefix} #{given} #{additional} #{family}, #{suffix}"
      attr_reader   :formatted

      # Override the attr reader to make it dynamic
      remove_method :formatted
      def formatted #:nodoc:
        f = [ @prefix, @given, @additional, @family ].map{|i| i == "" ? nil : i.strip}.compact.join(" ")
        if @suffix != ""
          f << ", " << @suffix
        end
        f
      end

      def initialize(n="", fn="") #:nodoc:
        n = ::Vcard.decode_text_list(n, ";") do |item|
          item.strip
        end

        @family     = n[0] || ""
        @given      = n[1] || ""
        @additional = n[2] || ""
        @prefix     = n[3] || ""
        @suffix     = n[4] || ""

        # FIXME - make calls to #fullname fail if fn is nil
        @fullname = (fn || "").strip
      end

      def encode #:nodoc:
        ::Vcard::DirectoryInfo::Field.create("N", ::Vcard.encode_text_list([ @family, @given, @additional, @prefix, @suffix ].map{|n| n.strip}, ";"))
      end

      def encode_fn #:nodoc:
        fn = @fullname.strip
        if @fullname.length == 0
          fn = formatted
        end
        ::Vcard::DirectoryInfo::Field.create("FN", fn)
      end
    end

    def decode_invisible(field) #:nodoc:
      nil
    end

    def decode_default(field) #:nodoc:
      Line.new( field.group, field.name, field.value )
    end

    def decode_version(field) #:nodoc:
      Line.new( field.group, field.name, (field.value.to_f * 10).to_i )
    end

    def decode_text(field) #:nodoc:
      Line.new( field.group, field.name, ::Vcard.decode_text(field.value_raw) )
    end

    def decode_n(field) #:nodoc:
      Line.new( field.group, field.name, Name.new(field.value, self["FN"]).freeze )
    end

    def decode_date_or_datetime(field) #:nodoc:
      date = nil
      begin
        date = ::Vcard.decode_date_to_date(field.value_raw)
      rescue ::Vcard::InvalidEncodingError
        date = ::Vcard.decode_date_time_to_datetime(field.value_raw)
      end
      Line.new( field.group, field.name, date )
    end

    def decode_bday(field) #:nodoc:
      begin
        return decode_date_or_datetime(field)

      rescue ::Vcard::InvalidEncodingError
        # Hack around BDAY dates hat are correct in the month and day, but have
        # some kind of garbage in the year.
        if field.value =~ /^\s*(\d+)-(\d+)-(\d+)\s*$/
          y = $1.to_i
          m = $2.to_i
          d = $3.to_i
          if(y < 1900)
            y = Time.now.year
          end
          Line.new( field.group, field.name, Date.new(y, m, d) )
        else
          raise
        end
      end
    end

    def decode_geo(field) #:nodoc:
      geo = ::Vcard.decode_list(field.value_raw, ";") do |item| item.to_f end
      Line.new( field.group, field.name, geo )
    end

    def decode_address(field) #:nodoc:
      Line.new( field.group, field.name, Address.decode(self, field) )
    end

    def decode_email(field) #:nodoc:
      Line.new( field.group, field.name, Email.decode(field) )
    end

    def decode_telephone(field) #:nodoc:
      Line.new( field.group, field.name, Telephone.decode(field) )
    end

    def decode_list_of_text(field) #:nodoc:
      Line.new(field.group, field.name, ::Vcard.decode_text_list(field.value_raw).select{|t| t.length > 0}.uniq)
    end

    def decode_structured_text(field) #:nodoc:
      Line.new( field.group, field.name, ::Vcard.decode_text_list(field.value_raw, ";") )
    end

    def decode_uri(field) #:nodoc:
      Line.new( field.group, field.name, Attachment::Uri.new(field.value, nil) )
    end

    def decode_agent(field) #:nodoc:
      case field.kind
      when "text"
        decode_text(field)
      when "uri"
        decode_uri(field)
      when "vcard", nil
        Line.new( field.group, field.name, ::Vcard.decode(::Vcard.decode_text(field.value_raw)).first )
      else
        raise InvalidEncodingError, "AGENT type #{field.kind} is not allowed"
      end
    end

    def decode_attachment(field) #:nodoc:
      Line.new( field.group, field.name, Attachment.decode(field, "binary", "TYPE") )
    end

    @@decode = {
      "BEGIN"      => :decode_invisible, # Don't return delimiter
      "END"        => :decode_invisible, # Don't return delimiter
      "FN"         => :decode_invisible, # Returned as part of N.

      "ADR"        => :decode_address,
      "AGENT"      => :decode_agent,
      "BDAY"       => :decode_bday,
      "CATEGORIES" => :decode_list_of_text,
      "EMAIL"      => :decode_email,
      "GEO"        => :decode_geo,
      "KEY"        => :decode_attachment,
      "LOGO"       => :decode_attachment,
      "MAILER"     => :decode_text,
      "N"          => :decode_n,
      "NAME"       => :decode_text,
      "NICKNAME"   => :decode_list_of_text,
      "NOTE"       => :decode_text,
      "ORG"        => :decode_structured_text,
      "PHOTO"      => :decode_attachment,
      "PRODID"     => :decode_text,
      "PROFILE"    => :decode_text,
      "REV"        => :decode_date_or_datetime,
      "ROLE"       => :decode_text,
      "SOUND"      => :decode_attachment,
      "SOURCE"     => :decode_text,
      "TEL"        => :decode_telephone,
      "TITLE"      => :decode_text,
      "UID"        => :decode_text,
      "URL"        => :decode_uri,
      "VERSION"    => :decode_version,
    }

    @@decode.default = :decode_default

    # Cache of decoded lines/fields, so we don't have to decode a field more than once.
    attr_reader :cache #:nodoc:

    # An entry in a vCard. The #value object's type varies with the kind of
    # line (the #name), and on how the line was encoded. The objects returned
    # for a specific kind of line are often extended so that they support a
    # common set of methods. The goal is to allow all types of objects for a
    # kind of line to be treated with some uniformity, but still allow specific
    # handling for the various value types if desired.
    #
    # See the specific methods for details.
    class Line
      attr_reader :group
      attr_reader :name
      attr_reader :value

      def initialize(group, name, value) #:nodoc:
        @group, @name, @value = (group||""), name.to_str, value
      end

      def self.decode(decode, card, field) #:nodoc:
        card.cache[field] || (card.cache[field] = card.send(decode[field.name], field))
      end
    end

    #@lines = {} FIXME - dead code

    # Return line for a field
    def f2l(field) #:nodoc:
      begin
        Line.decode(@@decode, self, field)
      rescue InvalidEncodingError
        # Skip invalidly encoded fields.
      end
    end

    # With no block, returns an Array of Line. If +name+ is specified, the
    # Array will only contain the +Line+s with that +name+. The Array may be
    # empty.
    #
    # If a block is given, each Line will be yielded instead of being returned
    # in an Array.
    def lines(name=nil) #:yield: Line
      # FIXME - this would be much easier if #lines was #each, and there was a
      # different #lines that returned an Enumerator that used #each
      unless block_given?
        map do |f|
          if( !name || f.name?(name) )
            f2l(f)
          else
            nil
          end
        end.compact
      else
        each do |f|
          if( !name || f.name?(name) )
            line = f2l(f)
            if line
              yield line
            end
          end
        end
        self
      end
    end

    private_class_method :new

    def initialize(fields, profile) #:nodoc:
      @cache = {}
      super(fields, profile)
    end

    # Create a vCard 3.0 object with the minimum required fields, plus any
    # +fields+ you want in the card (they can also be added later).
    def self.create(fields = [] )
      fields.unshift Field.create("VERSION", "3.0")
      super(fields, "VCARD")
    end

    # Decode a collection of vCards into an array of Vcard objects.
    #
    # +card+ can be either a String or an IO object.
    #
    # Since vCards are self-delimited (by a BEGIN:vCard and an END:vCard),
    # multiple vCards can be concatenated into a single directory info object.
    # They may or may not be related. For example, AddressBook.app (the OS X
    # contact manager) will export multiple selected cards in this format.
    #
    # Input data will be converted from unicode if it is detected. The heuristic
    # is based on the first bytes in the string:
    # - 0xEF 0xBB 0xBF: UTF-8 with a BOM, the BOM is stripped
    # - 0xFE 0xFF: UTF-16 with a BOM (big-endian), the BOM is stripped and string
    #   is converted to UTF-8
    # - 0xFF 0xFE: UTF-16 with a BOM (little-endian), the BOM is stripped and string
    #   is converted to UTF-8
    # - 0x00 "B" or 0x00 "b": UTF-16 (big-endian), the string is converted to UTF-8
    # - "B" 0x00 or "b" 0x00: UTF-16 (little-endian), the string is converted to UTF-8
    #
    # If you know that you have only one vCard, then you can decode that
    # single vCard by doing something like:
    #
    #   vcard = Vcard.decode(card_data).first
    #
    # Note: Should the import encoding be remembered, so that it can be reencoded in
    # the same format?
    def self.decode(card)
      if card.respond_to? :to_str
        string = card.to_str
      elsif card.respond_to? :read
        string = card.read(nil)
      else
        raise ArgumentError, "Vcard.decode cannot be called with a #{card.type}"
      end

      string.force_encoding(Encoding::UTF_8)
      entities = ::Vcard.expand(::Vcard.decode(string))

      # Since all vCards must have a begin/end, the top-level should consist
      # entirely of entities/arrays, even if its a single vCard.
      if entities.detect { |e| ! e.kind_of? Array }
        raise "Not a valid vCard"
      end

      vcards = []

      for e in entities
        vcards.push(new(e.flatten, "VCARD"))
      end

      vcards
    end

    # The value of the field named +name+, optionally limited to fields of
    # type +type+. If no match is found, nil is returned, if multiple matches
    # are found, the first match to have one of its type values be "PREF"
    # (preferred) is returned, otherwise the first match is returned.
    #
    # FIXME - this will become an alias for #value.
    def [](name, type=nil)
      fields = enum_by_name(name).find_all { |f| type == nil || f.type?(type) }

      valued = fields.select { |f| f.value != "" }
      if valued.first
        fields = valued
      end

      # limit to preferred, if possible
      pref = fields.select { |f| f.pref? }

      if pref.first
        fields = pref
      end

      fields.first ? fields.first.value : nil
    end

    # Return the Line#value for a specific +name+, and optionally for a
    # specific +type+.
    #
    # If no line with the +name+ (and, optionally, +type+) exists, nil is
    # returned.
    #
    # If multiple lines exist, the order of preference is:
    # - lines with values over lines without
    # - lines with a type of "pref" over lines without
    # If multiple lines are equally preferred, then the first line will be
    # returned.
    #
    # This is most useful when looking for a line that can not occur multiple
    # times, or when the line can occur multiple times, and you want to pick
    # the first preferred line of a specific type. See #values if you need to
    # access all the lines.
    #
    # Note that the +type+ field parameter is used for different purposes by
    # the various kinds of vCard lines, but for the addressing lines (ADR,
    # LABEL, TEL, EMAIL) it is has a reasonably consistent usage. Each
    # addressing line can occur multiple times, and a +type+ of "pref"
    # indicates that a particular line is the preferred line. Other +type+
    # values tend to indicate some information about the location ("home",
    # "work", ...) or some detail about the address ("cell", "fax", "voice",
    # ...). See the methods for the specific types of line for information
    # about supported types and their meaning.
    def value(name, type = nil)
      fields = enum_by_name(name).find_all { |f| type == nil || f.type?(type) }

      valued = fields.select { |f| f.value != "" }
      if valued.first
        fields = valued
      end

      pref = fields.select { |f| f.pref? }

      if pref.first
        fields = pref
      end

      if fields.first
        line = begin
                 Line.decode(@@decode, self, fields.first)
               rescue ::Vcard::InvalidEncodingError
               end

        if line
          return line.value
        end
      end

      nil
    end

    # A variant of #lines that only iterates over specific Line names. Since
    # the name is known, only the Line#value is returned or yielded.
    def values(name)
      unless block_given?
        lines(name).map { |line| line.value }
      else
        lines(name) { |line| yield line.value }
      end
    end

    # The first ADR value of type +type+, a Address. Any of the location or
    # delivery attributes of Address can be used as +type+. A wrapper around
    # #value("ADR", +type+).
    def address(type=nil)
      value("ADR", type)
    end

    # The ADR values, an array of Address. If a block is given, the values are
    # yielded. A wrapper around #values("ADR").
    def addresses #:yield:address
      values("ADR")
    end

    # The AGENT values. Each AGENT value is either a String, a Uri, or a Vcard.
    # If a block is given, the values are yielded. A wrapper around
    # #values("AGENT").
    def agents #:yield:agent
      values("AGENT")
    end

    # The BDAY value as either a Date or a DateTime, or nil if there is none.
    #
    # If the BDAY value is invalidly formatted, a feeble heuristic is applied
    # to find the month and year, and return a Date in the current year.
    def birthday
      value("BDAY")
    end

    # The CATEGORIES values, an array of String. A wrapper around
    # #value("CATEGORIES").
    def categories
      value("CATEGORIES")
    end

    # The first EMAIL value of type +type+, a Email. Any of the location
    # attributes of Email can be used as +type+. A wrapper around
    # #value("EMAIL", +type+).
    def email(type=nil)
      value("EMAIL", type)
    end

    # The EMAIL values, an array of Email. If a block is given, the values are
    # yielded. A wrapper around #values("EMAIL").
    def emails #:yield:email
      values("EMAIL")
    end

    # The GEO value, an Array of two Floats, +[ latitude, longitude]+.  North
    # of the equator is positive latitude, east of the meridian is positive
    # longitude.  See RFC2445 for more info, there are lots of special cases
    # and RFC2445"s description is more complete thant RFC2426.
    def geo
      value("GEO")
    end

    # Return an Array of KEY Line#value, or yield each Line#value if a block
    # is given. A wrapper around #values("KEY").
    #
    # KEY is a public key or authentication certificate associated with the
    # object that the vCard represents. It is not commonly used, but could
    # contain a X.509 or PGP certificate.
    #
    # See Attachment for a description of the value.
    def keys(&proc) #:yield: Line.value
      values("KEY", &proc)
    end

    # Return an Array of LOGO Line#value, or yield each Line#value if a block
    # is given. A wrapper around #values("LOGO").
    #
    # LOGO is a graphic image of a logo associated with the object the vCard
    # represents. Its not common, but would probably be equivalent to the logo
    # on a printed card.
    #
    # See Attachment for a description of the value.
    def logos(&proc) #:yield: Line.value
      values("LOGO", &proc)
    end

    ## MAILER

    # The N and FN as a Name object.
    #
    # N is required for a vCards, this raises InvalidEncodingError if
    # there is no N so it cannot return nil.
    def name
      value("N") || raise(::Vcard::InvalidEncodingError, "Missing mandatory N field")
    end

    # The first NICKNAME value, nil if there are none.
    def nickname
      v = value("NICKNAME")
      v = v.first if v
      v
    end

    # The NICKNAME values, an array of String. The array may be empty.
    def nicknames
      values("NICKNAME").flatten.uniq
    end

    # The NOTE value, a String. A wrapper around #value("NOTE").
    def note
      value("NOTE")
    end

    # The ORG value, an Array of String. The first string is the organization,
    # subsequent strings are departments within the organization. A wrapper
    # around #value("ORG").
    def org
      value("ORG")
    end

    # Return an Array of PHOTO Line#value, or yield each Line#value if a block
    # is given. A wrapper around #values("PHOTO").
    #
    # PHOTO is an image or photograph information that annotates some aspect of
    # the object the vCard represents. Commonly there is one PHOTO, and it is a
    # photo of the person identified by the vCard.
    #
    # See Attachment for a description of the value.
    def photos(&proc) #:yield: Line.value
      values("PHOTO", &proc)
    end

    ## PRODID

    ## PROFILE

    ## REV

    ## ROLE

    # Return an Array of SOUND Line#value, or yield each Line#value if a block
    # is given. A wrapper around #values("SOUND").
    #
    # SOUND is digital sound content information that annotates some aspect of
    # the vCard. By default this type is used to specify the proper
    # pronunciation of the name associated with the vCard. It is not commonly
    # used. Also, note that there is no mechanism available to specify that the
    # SOUND is being used for anything other than the default.
    #
    # See Attachment for a description of the value.
    def sounds(&proc) #:yield: Line.value
      values("SOUND", &proc)
    end

    ## SOURCE

    # The first TEL value of type +type+, a Telephone. Any of the location or
    # capability attributes of Telephone can be used as +type+. A wrapper around
    # #value("TEL", +type+).
    def telephone(type=nil)
      value("TEL", type)
    end

    # The TEL values, an array of Telephone. If a block is given, the values are
    # yielded. A wrapper around #values("TEL").
    def telephones #:yield:tel
      values("TEL")
    end

    # The TITLE value, a text string specifying the job title, functional
    # position, or function of the object the card represents. A wrapper around
    # #value("TITLE").
    def title
      value("TITLE")
    end

    ## UID

    # The URL value, a Attachment::Uri. A wrapper around #value("URL").
    def url
      value("URL")
    end

    # The URL values, an Attachment::Uri. A wrapper around #values("URL").
    def urls
      values("URL")
    end

    # The VERSION multiplied by 10 as an Integer.  For example, a VERSION:2.1
    # vCard would have a version of 21, and a VERSION:3.0 vCard would have a
    # version of 30.
    #
    # VERSION is required for a vCard, this raises InvalidEncodingError if
    # there is no VERSION so it cannot return nil.
    def version
      v = value("VERSION")
      unless v
        raise ::Vcard::InvalidEncodingError, "Invalid vCard - it has no version field!"
      end
      v
    end

    # Make changes to a vCard.
    #
    # Yields a Vcard::Vcard::Maker that can be used to modify this vCard.
    def make #:yield: maker
      ::Vcard::Vcard::Maker.make2(self) do |maker|
        yield maker
      end
    end

    # Delete +line+ if block yields true.
    def delete_if #:nodoc: :yield: line
      # Do in two steps to not mess up progress through the enumerator.
      rm = []

      each do |f|
        line = f2l(f)
        if line && yield(line)
          rm << f

          # Hack - because we treat N and FN as one field
          if f.name? "N"
            rm << field("FN")
          end
        end
      end

      rm.each do |f|
        @fields.delete( f )
        @cache.delete( f )
      end

    end

    # A class to make and make changes to vCards.
    #
    # It can be used to create completely new vCards using Vcard#make2.
    #
    # Its is also yielded from Vcard::Vcard#make, in which case it allows a kind
    # of transactional approach to changing vCards, so their values can be
    # validated after any changes have been made.
    #
    # Examples:
    # - link:ex_mkvcard.txt: example of creating a vCard
    # - link:ex_cpvcard.txt: example of copying and them modifying a vCard
    # - link:ex_mkv21vcard.txt: example of creating version 2.1 vCard
    # - link:ex_mkyourown.txt: example of adding support for new fields to Vcard::Maker
    class Maker
      # Make a vCard.
      #
      # Yields +maker+, a Vcard::Vcard::Maker which allows fields to be added to
      # +card+, and returns +card+, a Vcard::Vcard.
      #
      # If +card+ is nil or not provided a new Vcard::Vcard is created and the
      # fields are added to it.
      #
      # Defaults:
      # - vCards must have both an N and an FN field, #make2 will fail if there
      #   is no N field in the +card+ when your block is finished adding fields.
      # - If there is an N field, but no FN field, FN will be set from the
      #   information in N, see Vcard::Name#preformatted for more information.
      # - vCards must have a VERSION field. If one does not exist when your block is
      #   is finished it will be set to 3.0.
      def self.make2(card = ::Vcard::Vcard.create, &block) # :yields: maker
        new(nil, card).make(&block)
      end

      # Deprecated, use #make2.
      #
      # If set, the FN field will be set to +full_name+. Otherwise, FN will
      # be set from the values in #name.
      def self.make(full_name = nil, &block) # :yields: maker
        new(full_name, ::Vcard::Vcard.create).make(&block)
      end

      def make # :nodoc:
        yield self
        unless @card["N"]
          raise Unencodeable, "N field is mandatory"
        end
        fn = @card.field("FN")
        if fn && fn.value.strip.length == 0
          @card.delete(fn)
          fn = nil
        end
        unless fn
          @card << ::Vcard::DirectoryInfo::Field.create("FN", ::Vcard::Vcard::Name.new(@card["N"], "").formatted)
        end
        unless @card["VERSION"]
          @card << ::Vcard::DirectoryInfo::Field.create("VERSION", "3.0")
        end
        @card
      end

      private

      def initialize(full_name, card) # :nodoc:
        @card = card || ::Vcard::Vcard::create
        if full_name
          @card << ::Vcard::DirectoryInfo::Field.create("FN", full_name.strip )
        end
      end

      public

      # Deprecated, see #name.
      #
      # Use
      #   maker.name do |n| n.fullname = "foo" end
      # to set just fullname, or set the other fields to set fullname and the
      # name.
      def fullname=(fullname) #:nodoc: bacwards compat
        if @card.field("FN")
          raise ::Vcard::InvalidEncodingError, "Not allowed to add more than one FN field to a vCard."
        end
        @card << ::Vcard::DirectoryInfo::Field.create( "FN", fullname );
      end

      # Set the name fields, N and FN.
      #
      # Attributes of +name+ are:
      # - family: family name
      # - given: given name
      # - additional: additional names
      # - prefix: such as "Ms." or "Dr."
      # - suffix: such as "BFA", or "Sensei"
      #
      # +name+ is a Vcard::Name.
      #
      # All attributes are optional, though have all names be zero-length
      # strings isn't really in the spirit of  things. FN's value will be set
      # to Vcard::Name#formatted if Vcard::Name#fullname isn't given a specific
      # value.
      #
      # Warning: This is the only mandatory field.
      def name #:yield:name
        x = begin
              @card.name.dup
            rescue
              ::Vcard::Vcard::Name.new
            end

        yield x

        x.fullname.strip!

        delete_if do |line|
          line.name == "N"
        end

        @card << x.encode
        @card << x.encode_fn

        self
      end

      alias :add_name :name #:nodoc: backwards compatibility

      # Add an address field, ADR. +address+ is a Vcard::Vcard::Address.
      def add_addr # :yield: address
        x = ::Vcard::Vcard::Address.new
        yield x
        @card << x.encode
        self
      end

      # Add a telephone field, TEL. +tel+ is a Vcard::Vcard::Telephone.
      #
      # The block is optional, its only necessary if you want to specify
      # the optional attributes.
      def add_tel(number) # :yield: tel
        x = ::Vcard::Vcard::Telephone.new(number)
        if block_given?
          yield x
        end
        @card << x.encode
        self
      end

      # Add an email field, EMAIL. +email+ is a Vcard::Vcard::Email.
      #
      # The block is optional, its only necessary if you want to specify
      # the optional attributes.
      def add_email(email) # :yield: email
        x = ::Vcard::Vcard::Email.new(email)
        if block_given?
          yield x
        end
        @card << x.encode
        self
      end

      # Set the nickname field, NICKNAME.
      #
      # It can be set to a single String or an Array of String.
      def nickname=(nickname)
        delete_if { |l| l.name == "NICKNAME" }

        @card << ::Vcard::DirectoryInfo::Field.create( "NICKNAME", nickname );
      end

      # Add a birthday field, BDAY.
      #
      # +birthday+ must be a time or date object.
      #
      # Warning: It may confuse both humans and software if you add multiple
      # birthdays.
      def birthday=(birthday)
        if !birthday.respond_to? :month
          raise ArgumentError, "birthday must be a date or time object."
        end
        delete_if { |l| l.name == "BDAY" }
        @card << ::Vcard::DirectoryInfo::Field.create( "BDAY", birthday );
      end

      # Add a note field, NOTE. The +note+ String can contain newlines, they
      # will be escaped.
      def add_note(note)
        @card << ::Vcard::DirectoryInfo::Field.create( "NOTE", ::Vcard.encode_text(note) );
      end

      # Add an instant-messaging/point of presence address field, IMPP. The address
      # is a URL, with the syntax depending on the protocol.
      #
      # Attributes of IMPP are:
      # - preferred: true - set if this is the preferred address
      # - location: home, work, mobile - location of address
      # - purpose: personal,business - purpose of communications
      #
      # All attributes are optional, and so is the block.
      #
      # The URL syntaxes for the messaging schemes is fairly complicated, so I
      # don't try and build the URLs here, maybe in the future. This forces
      # the user to know the URL for their own address, hopefully not too much
      # of a burden.
      #
      # IMPP is defined in draft-jennings-impp-vcard-04.txt. It refers to the
      # URI scheme of a number of messaging protocols, but doesn't give
      # references to all of them:
      # - "xmpp" indicates to use XMPP, draft-saintandre-xmpp-uri-06.txt
      # - "irc" or "ircs" indicates to use IRC, draft-butcher-irc-url-04.txt
      # - "sip" indicates to use SIP/SIMPLE, RFC 3261
      # - "im" or "pres" indicates to use a CPIM or CPP gateway, RFC 3860 and RFC 3859
      # - "ymsgr" indicates to use yahoo
      # - "msn" might indicate to use Microsoft messenger
      # - "aim" indicates to use AOL
      #
      def add_impp(url) # :yield: impp
        params = {}

        if block_given?
          x = Struct.new( :location, :preferred, :purpose ).new

          yield x

          x[:preferred] = "PREF" if x[:preferred]

          types = x.to_a.flatten.compact.map { |s| s.downcase }.uniq

          params["TYPE"] = types if types.first
        end

        @card << ::Vcard::DirectoryInfo::Field.create( "IMPP", url, params)
        self
      end

      # Add an X-AIM account name where +xaim+ is an AIM screen name.
      #
      # I don't know if this is conventional, or supported by anything other
      # than AddressBook.app, but an example is:
      #   X-AIM;type=HOME;type=pref:exampleaccount
      #
      # Attributes of X-AIM are:
      # - preferred: true - set if this is the preferred address
      # - location: home, work, mobile - location of address
      #
      # All attributes are optional, and so is the block.
      def add_x_aim(xaim) # :yield: xaim
        params = {}

        if block_given?
          x = Struct.new( :location, :preferred ).new

          yield x

          x[:preferred] = "PREF" if x[:preferred]

          types = x.to_a.flatten.compact.map { |s| s.downcase }.uniq

          params["TYPE"] = types if types.first
        end

        @card << ::Vcard::DirectoryInfo::Field.create( "X-AIM", xaim, params)
        self
      end


      # Add a photo field, PHOTO.
      #
      # Attributes of PHOTO are:
      # - image: set to image data to include inline
      # - link: set to the URL of the image data
      # - type: string identifying the image type, supposed to be an "IANA registered image format",
      #     or a non-registered image format (usually these start with an x-)
      #
      # An error will be raised if neither image or link is set, or if both image
      # and link is set.
      #
      # Setting type is optional for a link image, because either the URL, the
      # image file extension, or a HTTP Content-Type may specify the type. If
      # it's not a link, setting type is mandatory, though it can be set to an
      # empty string, <code>''</code>, if the type is unknown.
      #
      # TODO - I'm not sure about this API. I'm thinking maybe it should be
      # #add_photo(image, type), and that I should detect when the image is a
      # URL, and make type mandatory if it wasn't a URL.
      def add_photo # :yield: photo
        x = Struct.new(:image, :link, :type).new
        yield x
        if x[:image] && x[:link]
          raise ::Vcard::InvalidEncodingError, "Image is not allowed to be both inline and a link."
        end

        value = x[:image] || x[:link]

        if !value
          raise ::Vcard::InvalidEncodingError, "A image link or inline data must be provided."
        end

        params = {}

        # Don't set type to the empty string.
        params["TYPE"] = x[:type] if( x[:type] && x[:type].length > 0 )

        if x[:link]
          params["VALUE"] = "URI"
        else # it's inline, base-64 encode it
          params["ENCODING"] = :b64
          if !x[:type]
            raise ::Vcard::InvalidEncodingError, "Inline image data must have it's type set."
          end
        end

        @card << ::Vcard::DirectoryInfo::Field.create( "PHOTO", value, params )
        self
      end

      # Set the title field, TITLE.
      #
      # It can be set to a single String.
      def title=(title)
        delete_if { |l| l.name == "TITLE" }

        @card << ::Vcard::DirectoryInfo::Field.create( "TITLE", title );
      end

      # Set the org field, ORG.
      #
      # It can be set to a single String or an Array of String.
      def org=(org)
        delete_if { |l| l.name == "ORG" }

        @card << ::Vcard::DirectoryInfo::Field.create( "ORG", org );
      end


      # Add a URL field, URL.
      def add_url(url)
        @card << ::Vcard::DirectoryInfo::Field.create( "URL", url.to_str );
      end

      # Add a Field, +field+.
      def add_field(field)
        fieldname = field.name.upcase
        case
        when [ "BEGIN", "END" ].include?(fieldname)
          raise ::Vcard::InvalidEncodingError, "Not allowed to manually add #{field.name} to a vCard."

        when [ "VERSION", "N", "FN" ].include?(fieldname)
          if @card.field(fieldname)
            raise ::Vcard::InvalidEncodingError, "Not allowed to add more than one #{fieldname} to a vCard."
          end
          @card << field

        else
          @card << field
        end
      end

      # Copy the fields from +card+ into self using #add_field. If a block is
      # provided, each Field from +card+ is yielded. The block should return a
      # Field to add, or nil.  The Field doesn't have to be the one yielded,
      # allowing the field to be copied and modified (see Field#copy) before adding, or
      # not added at all if the block yields nil.
      #
      # The vCard fields BEGIN and END aren't copied, and VERSION, N, and FN are copied
      # only if the card doesn't have them already.
      def copy(card) # :yields: Field
        card.each do |field|
          fieldname = field.name.upcase
          case
          when [ "BEGIN", "END" ].include?(fieldname)
            # Never copy these

          when [ "VERSION", "N", "FN" ].include?(fieldname) && @card.field(fieldname)
            # Copy these only if they don't already exist.

          else
            if block_given?
              field = yield field
            end

            if field
              add_field(field)
            end
          end
        end
      end

      # Delete +line+ if block yields true.
      def delete_if #:yield: line
        begin
          @card.delete_if do |line|
            yield line
          end
        rescue NoMethodError
          # FIXME - this is a hideous hack, allowing a DirectoryInfo to
          # be passed instead of a Vcard, and for it to almost work. Yuck.
        end
      end

    end
  end
end


module Vcard
  VERSION = "0.2.0"
end

# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

require "date"
require "open-uri"
require "stringio"


module Vcard
  # Split on \r\n or \n to get the lines, unfold continued lines (they
  # start with " " or \t), and return the array of unfolded lines.
  #
  # This also supports the (invalid) encoding convention of allowing empty
  # lines to be inserted for readability - it does this by dropping zero-length
  # lines.
  def self.unfold(card) #:nodoc:
      unfolded = []

      card.lines do |line|
        line.chomp!
        # If it's a continuation line, add it to the last.
        # If it's an empty line, drop it from the input.
        if( line =~ /^[ \t]/ )
          unfolded[-1] << line[1, line.size-1]
        elsif( line =~ /^$/ )
        else
          unfolded << line
        end
      end

      unfolded
  end

  # Convert a +sep+-seperated list of values into an array of values.
  def self.decode_list(value, sep = ",") # :nodoc:
    list = []

    value.split(sep).each do |item|
      item.chomp!(sep)
      list << yield(item)
    end
    list
  end

  # Convert a RFC 2425 date into an array of [year, month, day].
  def self.decode_date(v) # :nodoc:
    unless v =~ %r{^\s*#{Bnf::DATE}\s*$}
      raise ::Vcard::InvalidEncodingError, "date not valid (#{v})"
    end
    [$1.to_i, $2.to_i, $3.to_i]
  end

  # Convert a RFC 2425 date into a Date object.
  def self.decode_date_to_date(v)
    Date.new(*decode_date(v))
  end

  # Note in the following the RFC2425 allows yyyy-mm-ddThh:mm:ss, but RFC2445
  # does not. I choose to encode to the subset that is valid for both.

  # Encode a Date object as "yyyymmdd".
  def self.encode_date(d) # :nodoc:
     "%0.4d%0.2d%0.2d" % [ d.year, d.mon, d.day ]
  end

  # Encode a Date object as "yyyymmdd".
  def self.encode_time(d) # :nodoc:
     "%0.4d%0.2d%0.2d" % [ d.year, d.mon, d.day ]
  end

  # Encode a Time or DateTime object as "yyyymmddThhmmss"
  def self.encode_date_time(d) # :nodoc:
     "%0.4d%0.2d%0.2dT%0.2d%0.2d%0.2d" % [ d.year, d.mon, d.day, d.hour, d.min, d.sec ]
  end

  # Convert a RFC 2425 time into an array of [hour,min,sec,secfrac,timezone]
  def self.decode_time(v) # :nodoc:
    unless match = %r{^\s*#{Bnf::TIME}\s*$}.match(v)
      raise ::Vcard::InvalidEncodingError, "time '#{v}' not valid"
    end
    hour, min, sec, secfrac, tz = match.to_a[1..5]

    [hour.to_i, min.to_i, sec.to_i, secfrac ? secfrac.to_f : 0, tz]
  end

  def self.array_datetime_to_time(dtarray) #:nodoc:
    # We get [ year, month, day, hour, min, sec, usec, tz ]
    begin
      tz = (dtarray.pop == "Z") ? :gm : :local
      Time.send(tz, *dtarray)
    rescue ArgumentError => e
      raise ::Vcard::InvalidEncodingError, "#{tz} #{e} (#{dtarray.join(', ')})"
    end
  end

  # Convert a RFC 2425 time into an array of Time objects.
  def self.decode_time_to_time(v) # :nodoc:
    array_datetime_to_time(decode_date_time(v))
  end

  # Convert a RFC 2425 date-time into an array of [year,mon,day,hour,min,sec,secfrac,timezone]
  def self.decode_date_time(v) # :nodoc:
    unless match = %r{^\s*#{Bnf::DATE}T#{Bnf::TIME}\s*$}.match(v)
      raise ::Vcard::InvalidEncodingError, "date-time '#{v}' not valid"
    end
    year, month, day, hour, min, sec, secfrac, tz = match.to_a[1..8]

    [
      # date
      year.to_i, month.to_i, day.to_i,
      # time
      hour.to_i, min.to_i, sec.to_i, secfrac ? secfrac.to_f : 0, tz
    ]
  end

  def self.decode_date_time_to_datetime(v) #:nodoc:
    year, month, day, hour, min, sec = decode_date_time(v)
    # TODO - DateTime understands timezones, so we could decode tz and use it.
    DateTime.civil(year, month, day, hour, min, sec, 0)
  end

  # decode_boolean
  #
  # float
  #
  # float_list

  # Convert an RFC2425 INTEGER value into an Integer
  def self.decode_integer(v) # :nodoc:
    unless %r{\s*#{Bnf::INTEGER}\s*}.match(v)
      raise ::Vcard::InvalidEncodingError, "integer not valid (#{v})"
    end
    v.to_i
  end

  #
  # integer_list

  # Convert a RFC2425 date-list into an array of dates.
  def self.decode_date_list(v) # :nodoc:
    decode_list(v) do |date|
      date.strip!
      if date.length > 0
        decode_date(date)
      end
    end.compact
  end

  # Convert a RFC 2425 time-list into an array of times.
  def self.decode_time_list(v) # :nodoc:
    decode_list(v) do |time|
      time.strip!
      if time.length > 0
        decode_time(time)
      end
    end.compact
  end

  # Convert a RFC 2425 date-time-list into an array of date-times.
  def self.decode_date_time_list(v) # :nodoc:
    decode_list(v) do |datetime|
      datetime.strip!
      if datetime.length > 0
        decode_date_time(datetime)
      end
    end.compact
  end

  # Convert RFC 2425 text into a String.
  # \\ -> \
  # \n -> NL
  # \N -> NL
  # \, -> ,
  # \; -> ;
  #
  # I've seen double-quote escaped by iCal.app. Hmm. Ok, if you aren't supposed
  # to escape anything but the above, everything else is ambiguous, so I'll
  # just support it.
  def self.decode_text(v) # :nodoc:
    # FIXME - I think this should trim leading and trailing space
    v.gsub(/\\(.)/) do
      case $1
      when "n", "N"
        "\n"
      else
        $1
      end
    end
  end

  def self.encode_text(v) #:nodoc:
    v.to_str.gsub(/([\\,;\n])/) { $1 == "\n" ? "\\n" : "\\"+$1 }
  end

  # v is an Array of String, or just a single String
  def self.encode_text_list(v, sep = ",") #:nodoc:
    begin
      v.to_ary.map{ |t| encode_text(t) }.join(sep)
    rescue
      encode_text(v)
    end
  end

  # Convert a +sep+-seperated list of TEXT values into an array of values.
  def self.decode_text_list(value, sep = ",") # :nodoc:
    # Need to do in two stages, as best I can find.
    list = value.scan(/([^#{sep}\\]*(?:\\.[^#{sep}\\]*)*)#{sep}/).map do |v|
      decode_text(v.first)
    end
    if value.match(/([^#{sep}\\]*(?:\\.[^#{sep}\\]*)*)$/)
      list << $1
    end
    list
  end

  # param-value = paramtext / quoted-string
  # paramtext  = *SAFE-CHAR
  # quoted-string      = DQUOTE *QSAFE-CHAR DQUOTE
  def self.encode_paramtext(value)
    case value
    when %r{\A#{Bnf::SAFECHAR}*\z}
      value
    else
      raise ::Vcard::Unencodable, "paramtext #{value.inspect}"
    end
  end

  def self.encode_paramvalue(value)
    case value
    when %r{\A#{Bnf::SAFECHAR}*\z}
      value
    when %r{\A#{Bnf::QSAFECHAR}*\z}
      '"' + value + '"'
    else
      raise ::Vcard::Unencodable, "param-value #{value.inspect}"
    end
  end


  # Unfold the lines in +card+, then return an array of one Field object per
  # line.
  def self.decode(card) #:nodoc:
    unfold(card).collect { |line| DirectoryInfo::Field.decode(line) }
  end


  # Expand an array of fields into its syntactic entities. Each entity is a sequence
  # of fields where the sequences is delimited by a BEGIN/END field. Since
  # BEGIN/END delimited entities can be nested, we build a tree. Each entry in
  # the array is either a Field or an array of entries (where each entry is
  # either a Field, or an array of entries...).
  def self.expand(src) #:nodoc:
    # output array to expand the src to
    dst = []
    # stack used to track our nesting level, as we see begin/end we start a
    # new/finish the current entity, and push/pop that entity from the stack
    current = [ dst ]

    for f in src
      if f.name? "BEGIN"
        e = [ f ]

        current.last.push(e)
        current.push(e)

      elsif f.name? "END"
        current.last.push(f)

        unless current.last.first.value? current.last.last.value
          raise "BEGIN/END mismatch (#{current.last.first.value} != #{current.last.last.value})"
        end

        current.pop

      else
        current.last.push(f)
      end
    end

    dst
  end

  # Split an array into an array of all the fields at the outer level, and
  # an array of all the inner arrays of fields. Return the array [outer,
  # inner].
  def self.outer_inner(fields) #:nodoc:
    # TODO - use Enumerable#partition
    # seperate into the outer-level fields, and the arrays of component
    # fields
    outer = []
    inner = []
    fields.each do |line|
      case line
      when Array; inner << line
      else;       outer << line
      end
    end
    return outer, inner
  end
end


# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

module Vcard

  # Attachments are used by both iCalendar and vCard. They are either a URI or
  # inline data, and their decoded value will be either a Uri or a Inline, as
  # appropriate.
  #
  # Besides the methods specific to their class, both kinds of object implement
  # a set of common methods, allowing them to be treated uniformly:
  # - Uri#to_io, Inline#to_io: return an IO from which the value can be read.
  # - Uri#to_s, Inline#to_s: return the value as a String.
  # - Uri#format, Inline#format: the format of the value. This is supposed to
  #   be an "iana defined" identifier (like "image/jpeg"), but could be almost
  #   anything (or nothing) in practice.  Since the parameter is optional, it may
  #   be "".
  #
  # The objects can also be distinguished by their class, if necessary.
  module Attachment

    # TODO - It might be possible to autodetect the format from the first few
    # bytes of the value, and return the appropriate MIME type when format
    # isn't defined.
    #
    # iCalendar and vCard put the format in different parameters, and the
    # default kind of value is different.
    def Attachment.decode(field, defkind, fmtparam) #:nodoc:
      format = field.pvalue(fmtparam) || ""
      kind = field.kind || defkind
      case kind
      when "text"
        Inline.new(::Vcard.decode_text(field.value), format)
      when "uri"
        Uri.new(field.value_raw, format)
      when "binary"
        Inline.new(field.value, format)
      else
        raise InvalidEncodingError, "Attachment of type #{kind} is not allowed"
      end
    end

    # Extends a String to support some of the same methods as Uri.
    class Inline < String
      def initialize(s, format) #:nodoc:
        @format = format
        super(s)
      end

      # Return an IO object for the inline data. See +stringio+ for more
      # information.
      def to_io
        StringIO.new(self)
      end

      # The format of the inline data.
      # See Attachment.
      attr_reader :format
    end

    # Encapsulates a URI and implements some methods of String.
    class Uri
      def initialize(uri, format) #:nodoc:
        @uri = uri
        @format = format
      end

      # The URI value.
      attr_reader :uri

      # The format of the data referred to by the URI.
      # See Attachment.
      attr_reader :format

      # Return an IO object from opening the URI.  See +open-uri+ for more
      # information.
      def to_io
        open(@uri)
      end

      # Return the String from reading the IO object to end-of-data.
      def to_s
        to_io.read(nil)
      end

      def inspect #:nodoc:
        s = "<#{self.class.to_s}: #{uri.inspect}>"
        s << ", #{@format.inspect}" if @format
        s
      end
    end

  end
end

# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

module Vcard
  # Contains regular expression strings for the EBNF of RFC 2425.
  module Bnf #:nodoc:

    # 1*(ALPHA / DIGIT / "-")
    # Note: I think I can add A-Z here, and get rid of the "i" matches elsewhere.
    # Note: added "_" to allowed because its produced by Notes  (X-LOTUS-CHILD_UID:)
    # Note: added "/" to allowed because its produced by KAddressBook (X-messaging/xmpp-All:)
    # Note: added " " to allowed because its produced by highrisehq.com (X-GOOGLE TALK:)
    NAME    = "[-a-z0-9_/][-a-z0-9_/ ]*"

    # <"> <Any character except CTLs, DQUOTE> <">
    QSTR    = '"([^"]*)"'

    # *<Any character except CTLs, DQUOTE, ";", ":", ",">
    PTEXT   = '([^";:,]+)'

    # param-value = ptext / quoted-string
    PVALUE  = "(?:#{QSTR}|#{PTEXT})"

    # param = name "=" param-value *("," param-value)
    # Note: v2.1 allows a type or encoding param-value to appear without the type=
    # or the encoding=. This is hideous, but we try and support it, if there
    # is no "=", then $2 will be "", and we will treat it as a v2.1 param.
    PARAM = ";(#{NAME})(=?)((?:#{PVALUE})?(?:,#{PVALUE})*)"

    # V3.0: contentline  =   [group "."]  name *(";" param) ":" value
    # V2.1: contentline  = *( group "." ) name *(";" param) ":" value
    #
    # We accept the V2.1 syntax for backwards compatibility.
    #LINE = "((?:#{NAME}\\.)*)?(#{NAME})([^:]*)\:(.*)"
    LINE = "^((?:#{NAME}\\.)*)?(#{NAME})((?:#{PARAM})*):(.*)$"

    # date = date-fullyear ["-"] date-month ["-"] date-mday
    # date-fullyear = 4 DIGIT
    # date-month = 2 DIGIT
    # date-mday = 2 DIGIT
    DATE = "(\d\d\d\d)-?(\d\d)-?(\d\d)"

    # time = time-hour [":"] time-minute [":"] time-second [time-secfrac] [time-zone]
    # time-hour = 2 DIGIT
    # time-minute = 2 DIGIT
    # time-second = 2 DIGIT
    # time-secfrac = "," 1*DIGIT
    # time-zone = "Z" / time-numzone
    # time-numzone = sign time-hour [":"] time-minute
    TIME = "(\d\d):?(\d\d):?(\d\d)(\.\d+)?(Z|[-+]\d\d:?\d\d)?"

    # integer = (["+"] / "-") 1*DIGIT
    INTEGER = "[-+]?\d+"

    # QSAFE-CHAR = WSP / %x21 / %x23-7E / NON-US-ASCII
    #  ; Any character except CTLs and DQUOTE
    QSAFECHAR = "[ \t\x21\x23-\x7e\x80-\xff]"

    # SAFE-CHAR  = WSP / %x21 / %x23-2B / %x2D-39 / %x3C-7E / NON-US-ASCII
    #   ; Any character except CTLs, DQUOTE, ";", ":", ","
    SAFECHAR = "[ \t\x21\x23-\x2b\x2d-\x39\x3c-\x7e\x80-\xff]"
  end
end

# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

module Vcard
  # An RFC 2425 directory info object.
  #
  # A directory information object is a sequence of fields. The basic
  # structure of the object, and the way in which it is broken into fields
  # is common to all profiles of the directory info type.
  #
  # A vCard, for example, is a specialization of a directory info object.
  #
  # - [RFC2425] the directory information framework (ftp://ftp.ietf.org/rfc/rfc2425.txt)
  #
  # Here's an example of encoding a simple vCard using the low-level APIs:
  #
  #   card = Vcard::Vcard.create
  #   card << Vcard::DirectoryInfo::Field.create("EMAIL", "user.name@example.com", "TYPE" => "INTERNET" )
  #   card << Vcard::DirectoryInfo::Field.create("URL", "http://www.example.com/user" )
  #   card << Vcard::DirectoryInfo::Field.create("FN", "User Name" )
  #   puts card.to_s
  #
  # Don't do it like that, use Vcard::Vcard::Maker.
  class DirectoryInfo
    include Enumerable

    private_class_method :new

    # Initialize a DirectoryInfo object from +fields+. If +profile+ is
    # specified, check the BEGIN/END fields.
    def initialize(fields, profile = nil) #:nodoc:
      if fields.detect { |f| ! f.kind_of? DirectoryInfo::Field }
        raise ArgumentError, "fields must be an array of DirectoryInfo::Field objects"
      end

      @string = nil # this is used as a flag to indicate that recoding will be necessary
      @fields = fields

      check_begin_end(profile) if profile
    end

    # Decode +card+ into a DirectoryInfo object.
    #
    # +card+ may either be a something that is convertible to a string using
    # #to_str or an Array of objects that can be joined into a string using
    # #join("\n"), or an IO object (which will be read to end-of-file).
    #
    # The lines in the string may be delimited using IETF (CRLF) or Unix (LF) conventions.
    #
    # A DirectoryInfo is mutable, you can add new fields to it, see
    # Vcard::DirectoryInfo::Field#create() for how to create a new Field.
    #
    # TODO: I don't believe this is ever used, maybe I can remove it.
    def DirectoryInfo.decode(card) #:nodoc:
      if card.respond_to? :to_str
        string = card.to_str
      elsif card.kind_of? Array
        string = card.join("\n")
      elsif card.kind_of? IO
        string = card.read(nil)
      else
        raise ArgumentError, "DirectoryInfo cannot be created from a #{card.type}"
      end

      fields = ::Vcard.decode(string)

      new(fields)
    end

    # Create a new DirectoryInfo object. The +fields+ are an optional array of
    # DirectoryInfo::Field objects to add to the new object, between the
    # BEGIN/END.  If the +profile+ string is not nil, then it is the name of
    # the directory info profile, and the BEGIN:+profile+/END:+profile+ fields
    # will be added.
    #
    # A DirectoryInfo is mutable, you can add new fields to it using #push(),
    # and see Field#create().
    def DirectoryInfo.create(fields = [], profile = nil)

      if profile
        p = profile.to_str
        f = [ Field.create("BEGIN", p) ]
        f.concat fields
        f.push Field.create("END", p)
        fields = f
      end

      new(fields, profile)
    end

    # The first field named +name+, or nil if no
    # match is found.
    def field(name)
      enum_by_name(name).each { |f| return f }
      nil
    end

    # The value of the first field named +name+, or nil if no
    # match is found.
    def [](name)
      enum_by_name(name).each { |f| return f.value if f.value != ""}
      enum_by_name(name).each { |f| return f.value }
      nil
    end

    # An array of all the values of fields named +name+, converted to text
    # (using Field#to_text()).
    #
    # TODO - call this #texts(), as in the plural?
    def text(name)
      accum = []
      each do |f|
        if f.name? name
          accum << f.to_text
        end
      end
      accum
    end

    # Array of all the Field#group()s.
    def groups
      @fields.collect { |f| f.group } .compact.uniq
    end

    # All fields, frozen.
    def fields #:nodoc:
      @fields.dup.freeze
    end

    # Yields for each Field for which +cond+.call(field) is true. The
    # (default) +cond+ of nil is considered true for all fields, so
    # this acts like a normal #each() when called with no arguments.
    def each(cond = nil) # :yields: Field
      @fields.each do |field|
         if(cond == nil || cond.call(field))
           yield field
         end
      end
      self
    end

    # Returns an Enumerator for each Field for which #name?(+name+) is true.
    #
    # An Enumerator supports all the methods of Enumerable, so it allows iteration,
    # collection, mapping, etc.
    #
    # Examples:
    #
    # Print all the nicknames in a card:
    #
    #   card.enum_by_name("NICKNAME") { |f| puts f.value }
    #
    # Print an Array of the preferred email addresses in the card:
    #
    #   pref_emails = card.enum_by_name("EMAIL").select { |f| f.pref? }
    def enum_by_name(name)
      Enumerator.new(self, Proc.new { |field| field.name?(name) })
    end

    # Returns an Enumerator for each Field for which #group?(+group+) is true.
    #
    # For example, to print all the fields, sorted by group, you could do:
    #
    #   card.groups.sort.each do |group|
    #     card.enum_by_group(group).each do |field|
    #       puts "#{group} -> #{field.name}"
    #     end
    #   end
    #
    # or to get an array of all the fields in group "AGROUP", you could do:
    #
    #   card.enum_by_group("AGROUP").to_a
    def enum_by_group(group)
      Enumerator.new(self, Proc.new { |field| field.group?(group) })
    end

    # Returns an Enumerator for each Field for which +cond+.call(field) is true.
    def enum_by_cond(cond)
      Enumerator.new(self, cond )
    end

    # Force card to be reencoded from the fields.
    def dirty #:nodoc:
      #string = nil
    end

    # Append +field+ to the fields. Note that it won't be literally appended
    # to the fields, it will be inserted before the closing END field.
    def push(field)
      dirty
      @fields[-1,0] = field
      self
    end

    alias << push

    # Push +field+ onto the fields, unless there is already a field
    # with this name.
    def push_unique(field)
      push(field) unless @fields.detect { |f| f.name? field.name }
      self
    end

    # Append +field+ to the end of all the fields. This isn't usually what you
    # want to do, usually a DirectoryInfo's first and last fields are a
    # BEGIN/END pair, see #push().
    def push_end(field)
      @fields << field
      self
    end

    # Delete +field+.
    #
    # Warning: You can't delete BEGIN: or END: fields, but other
    # profile-specific fields can be deleted, including mandatory ones. For
    # vCards in particular, in order to avoid destroying them, I suggest
    # creating a new Vcard, and copying over all the fields that you still
    # want, rather than using #delete. This is easy with Vcard::Maker#copy, see
    # the Vcard::Maker examples.
    def delete(field)
      case
      when field.name?("BEGIN"), field.name?("END")
        raise ArgumentError, "Cannot delete BEGIN or END fields."
      else
        @fields.delete field
      end

      self
    end

    # The string encoding of the DirectoryInfo. See Field#encode for information
    # about the width parameter.
    def encode(width=nil)
      unless @string
        @string = @fields.collect { |f| f.encode(width) } . join ""
      end
      @string
    end

    alias to_s encode

    # Check that the DirectoryInfo object is correctly delimited by a BEGIN
    # and END, that their profile values match, and if +profile+ is specified, that
    # they are the specified profile.
    def check_begin_end(profile=nil) #:nodoc:
      unless @fields.first
        raise "No fields to check"
      end
      unless @fields.first.name? "BEGIN"
        raise "Needs BEGIN, found: #{@fields.first.encode nil}"
      end
      unless @fields.last.name? "END"
        raise "Needs END, found: #{@fields.last.encode nil}"
      end
      unless @fields.last.value? @fields.first.value
        raise "BEGIN/END mismatch: (#{@fields.first.value} != #{@fields.last.value}"
      end
      if profile
        if ! @fields.first.value? profile
          raise "Mismatched profile"
        end
      end
      true
    end
  end
end

# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

module Vcard
  # This is a way for an object to have multiple ways of being enumerated via
  # argument to it's #each() method. An Enumerator mixes in Enumerable, so the
  # standard APIs such as Enumerable#map(), Enumerable#to_a(), and
  # Enumerable#find_all() can be used on it.
  #
  # TODO since 1.8, this is part of the standard library, I should rewrite vPim
  # so this can be removed.
  class Enumerator
    include Enumerable

    def initialize(obj, *args)
      @obj = obj
      @args = args
    end

    def each(&block)
      @obj.each(*@args, &block)
    end
  end
end

# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

module Vcard
  # Exception used to indicate that data being decoded is invalid, the message
  # should describe what is invalid.
  class InvalidEncodingError < StandardError; end

  # Exception used to indicate that data being decoded is unsupported, the message
  # should describe what is unsupported.
  #
  # If its unsupported, its likely because I didn't anticipate it being useful
  # to support this, and it likely it could be supported on request.
  class UnsupportedError < StandardError; end

  # Exception used to indicate that encoding failed, probably because the
  # object would not result in validly encoded data. The message should
  # describe what is unsupported.
  class Unencodeable < StandardError; end
end

# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify it
# under the same terms as the ruby language itself, see the file COPYING for
# details.

module Vcard

  class DirectoryInfo

    # A field in a directory info object.
    class Field
      # TODO
      # - Field should know which param values and field values are
      #   case-insensitive, configurably, so it can down case them
      # - perhaps should have pvalue_set/del/add, perhaps case-insensitive, or
      #   pvalue_iset/idel/iadd, where set sets them all, add adds if not present,
      #   and del deletes any that are present
      # - I really, really, need a case-insensitive string...
      # - should allow nil as a field value, its not the same as "", if there is
      #   more than one pvalue, the empty string will show up. This isn't strictly
      #   disallowed, but its odd. Should also strip empty strings on decoding, if
      #   I don't already.
      private_class_method :new

      def Field.create_array(fields)
        case fields
        when Hash
          fields.map do |name,value|
            DirectoryInfo::Field.create( name, value )
          end
        else
          fields.to_ary
        end
      end

      # Encode a field.
      def Field.encode0(group, name, params={}, value="") # :nodoc:
        line = ""

        # A reminder of the line format:
        #   [<group>.]<name>;<pname>=<pvalue>,<pvalue>:<value>

        if group
          line << group << "."
        end

        line << name

        params.each do |pname, pvalues|

          unless pvalues.respond_to? :to_ary
            pvalues = [ pvalues ]
          end

          line << ";" << pname << "="

          sep = "" # set to "," after one pvalue has been appended

          pvalues.each do |pvalue|
            # check if we need to do any encoding
            if pname.casecmp("ENCODING") == 0 && pvalue == :b64
              pvalue = "B" # the RFC definition of the base64 param value
              value = [ value.to_str ].pack("m").gsub("\n", "")
            end

            line << sep << pvalue
            sep =",";
          end
        end

        line << ":"

        line << Field.value_str(value)

        line
      end

      def Field.value_str(value) # :nodoc:
        line = ""
        case value
        when Date
          line << ::Vcard.encode_date(value)

        when Time #, DateTime
          line << ::Vcard.encode_date_time(value)

        when Array
          line << value.map { |v| Field.value_str(v) }.join(";")

        when Symbol
          line << value

        else
          # FIXME - somewhere along here, values with special chars need escaping...
          line << value.to_str
        end
        line
      end

      # Decode a field.
      def Field.decode0(atline) # :nodoc:
        unless atline =~ %r{#{Bnf::LINE}}i
          raise ::Vcard::InvalidEncodingError, atline
        end

        atgroup = $1.upcase
        atname = $2.upcase
        paramslist = $3
        atvalue = $~[-1]

        # I've seen space that shouldn't be there, as in "BEGIN:VCARD ", so
        # strip it. I'm not absolutely sure this is allowed... it certainly
        # breaks round-trip encoding.
        atvalue.strip!

        if atgroup.length > 0
          atgroup.chomp!(".")
        else
          atgroup = nil
        end

        atparams = {}

        # Collect the params, if any.
        if paramslist.size > 1

          # v3.0 and v2.1 params
          paramslist.scan( %r{#{Bnf::PARAM}}i ) do

            # param names are case-insensitive, and multi-valued
            name = $1.upcase
            params = $3

            # v2.1 params have no "=" sign, figure out what kind of param it
            # is (either its a known encoding, or we treat it as a "TYPE"
            # param).

            if $2 == ""
              params = $1
              case $1
              when /quoted-printable/i
                name = "ENCODING"

              when /base64/i
                name = "ENCODING"

              else
                name = "TYPE"
              end
            end

            # TODO - In ruby1.8 I can give an initial value to the atparams
            # hash values instead of this.
            unless atparams.key? name
              atparams[name] = []
            end

            params.scan( %r{#{Bnf::PVALUE}} ) do
              atparams[name] << ($1 || $2)
            end
          end
        end

        [ atgroup, atname, atparams, atvalue ]
      end

      def initialize(line) # :nodoc:
        @line = line.to_str
        @group, @name, @params, @value = Field.decode0(@line)

        @params.each do |pname,pvalues|
          pvalues.freeze
        end
        self
      end

      # Create a field by decoding +line+, a String which must already be
      # unfolded. Decoded fields are frozen, but see #copy().
      def Field.decode(line)
        new(line).freeze
      end

      # Create a field with name +name+ (a String), value +value+ (see below),
      # and optional parameters, +params+. +params+ is a hash of the parameter
      # name (a String) to either a single string or symbol, or an array of
      # strings and symbols (parameters can be multi-valued).
      #
      # If "ENCODING" => :b64 is specified as a parameter, the value will be
      # base-64 encoded. If it's already base-64 encoded, then use String
      # values ("ENCODING" => "B"), and no further encoding will be done by
      # this routine.
      #
      # Currently handled value types are:
      # - Time, encoded as a date-time value
      # - Date, encoded as a date value
      # - String, encoded directly
      # - Array of String, concatentated with ";" between them.
      #
      # TODO - need a way to encode String values as TEXT, at least optionally,
      # so as to escape special chars, etc.
      def Field.create(name, value="", params={})
        line = Field.encode0(nil, name, params, value)

        begin
          new(line)
        rescue ::Vcard::InvalidEncodingError => e
          raise ArgumentError, e.to_s
        end
      end

      # Create a copy of Field. If the original Field was frozen, this one
      # won't be.
      def copy
        Marshal.load(Marshal.dump(self))
      end

      # The String encoding of the Field. The String will be wrapped to a
      # maximum line width of +width+, where +0+ means no wrapping, and nil is
      # to accept the default wrapping (75, recommended by RFC2425).
      #
      # Note: AddressBook.app 3.0.3 neither understands to unwrap lines when it
      # imports vCards (it treats them as raw new-line characters), nor wraps
      # long lines on export. This is mostly a cosmetic problem, but wrapping
      # can be disabled by setting width to +0+, if desired.
      #
      # FIXME - breaks round-trip encoding, need to change this to not wrap
      # fields that are already wrapped.
      def encode(width=nil)
        width = 75 unless width
        l = @line
        # Wrap to width, unless width is zero.
        if width > 0
          l = l.gsub(/.{#{width},#{width}}/) { |m| m + "\n " }
        end
        # Make sure it's terminated with no more than a single NL.
        l.gsub(/\s*\z/, "") + "\n"
      end

      alias to_s encode

      # The name.
      def name
        @name
      end

      # The group, if present, or nil if not present.
      def group
        @group
      end

      # An Array of all the param names.
      def pnames
        @params.keys
      end

      # FIXME - remove my own uses of #params
      alias params pnames # :nodoc:

      # The first value of the param +name+,  nil if there is no such param,
      # the param has no value, or the first param value is zero-length.
      def pvalue(name)
        v = pvalues( name )
        if v
          v = v.first
        end
        if v
          v = nil unless v.length > 0
        end
        v
      end

      # The Array of all values of the param +name+,  nil if there is no such
      # param, [] if the param has no values. If the Field isn't frozen, the
      # Array is mutable.
      def pvalues(name)
        @params[name.upcase]
      end

      # FIXME - remove my own uses of #param
      alias param pvalues # :nodoc:

      alias [] pvalues

      # Yield once for each param, +name+ is the parameter name, +value+ is an
      # array of the parameter values.
      def each_param(&block) #:yield: name, value
        if @params
          @params.each(&block)
        end
      end

      # The decoded value.
      #
      # The encoding specified by the #encoding, if any, is stripped.
      #
      # Note: Both the RFC 2425 encoding param ("b", meaning base-64) and the
      # vCard 2.1 encoding params ("base64", "quoted-printable", "8bit", and
      # "7bit") are supported.
      #
      # FIXME:
      # - should use the VALUE parameter
      # - should also take a default value type, so it can be converted
      #   if VALUE parameter is not present.
      def value
        case encoding
        when nil, "8BIT", "7BIT" then @value

          # Hack - if the base64 lines started with 2 SPC chars, which is invalid,
          # there will be extra spaces in @value. Since no SPC chars show up in
          # b64 encodings, they can be safely stripped out before unpacking.
        when "B", "BASE64"       then @value.gsub(" ", "").unpack("m*").first

        when "QUOTED-PRINTABLE"  then @value.unpack("M*").first

        else
          raise ::Vcard::InvalidEncodingError, "unrecognized encoding (#{encoding})"
        end
      end

      # Is the #name of this Field +name+? Names are case insensitive.
      def name?(name)
        @name.casecmp(name) == 0
      end

      # Is the #group of this field +group+? Group names are case insensitive.
      # A +group+ of nil matches if the field has no group.
      def group?(group)
        @group.casecmp(group) == 0
      end

      # Is the value of this field of type +kind+? RFC2425 allows the type of
      # a fields value to be encoded in the VALUE parameter. Don't rely on its
      # presence, they aren't required, and usually aren't bothered with. In
      # cases where the kind of value might vary (an iCalendar DTSTART can be
      # either a date or a date-time, for example), you are more likely to see
      # the kind of value specified explicitly.
      #
      # The value types defined by RFC 2425 are:
      # - uri:
      # - text:
      # - date: a list of 1 or more dates
      # - time: a list of 1 or more times
      # - date-time: a list of 1 or more date-times
      # - integer:
      # - boolean:
      # - float:
      def kind?(kind)
        self.kind.casecmp(kind) == 0
      end

      # Is one of the values of the TYPE parameter of this field +type+? The
      # type parameter values are case insensitive. False if there is no TYPE
      # parameter.
      #
      # TYPE parameters are used for general categories, such as
      # distinguishing between an email address used at home or at work.
      def type?(type)
        type = type.to_str

        types = param("TYPE")

        if types
          types = types.detect { |t| t.casecmp(type) == 0 }
        end
      end

      # Is this field marked as preferred? A vCard field is preferred if
      # #type?("PREF"). This method is not necessarily meaningful for
      # non-vCard profiles.
      def pref?
        type? "PREF"
      end

      # Set whether a field is marked as preferred. See #pref?
      def pref=(ispref)
        if ispref
          pvalue_iadd("TYPE", "PREF")
        else
          pvalue_idel("TYPE", "PREF")
        end
      end

      # Is the value of this field +value+? The check is case insensitive.
      # FIXME - it shouldn't be insensitive, make a #casevalue? method.
      def value?(value)
        @value.casecmp(value) == 0
      end

      # The value of the ENCODING parameter, if present, or nil if not
      # present.
      def encoding
        e = param("ENCODING")

        if e
          if e.length > 1
            raise ::Vcard::InvalidEncodingError, "multi-valued param 'ENCODING' (#{e})"
          end
          e = e.first.upcase
        end
        e
      end

      # The type of the value, as specified by the VALUE parameter, nil if
      # unspecified.
      def kind
        v = param("VALUE")
        if v
          if v.size > 1
            raise InvalidEncodingError, "multi-valued param 'VALUE' (#{values})"
          end
          v = v.first.downcase
        end
        v
      end

      # The value as an array of Time objects (all times and dates in
      # RFC2425 are lists, even where it might not make sense, such as a
      # birthday). The time will be UTC if marked as so (with a timezone of
      # "Z"), and in localtime otherwise.
      #
      # TODO - support timezone offsets
      #
      # TODO - if year is before 1970, this won't work... but some people
      # are generating calendars saying Canada Day started in 1753!
      # That's just wrong! So, what to do? I add a message
      # saying what the year is that breaks, so they at least know that
      # its ridiculous! I think I need my own DateTime variant.
      def to_time
        begin
          ::Vcard.decode_date_time_list(value).collect do |d|
            # We get [ year, month, day, hour, min, sec, usec, tz ]
            begin
              if(d.pop == "Z")
                Time.gm(*d)
              else
                Time.local(*d)
              end
            rescue ArgumentError => e
              raise ::Vcard::InvalidEncodingError, "Time.gm(#{d.join(', ')}) failed with #{e.message}"
            end
          end
        rescue ::Vcard::InvalidEncodingError
          ::Vcard.decode_date_list(value).collect do |d|
            # We get [ year, month, day ]
            begin
              Time.gm(*d)
            rescue ArgumentError => e
              raise ::Vcard::InvalidEncodingError, "Time.gm(#{d.join(', ')}) failed with #{e.message}"
            end
          end
        end
      end

      # The value as an array of Date objects (all times and dates in
      # RFC2425 are lists, even where it might not make sense, such as a
      # birthday).
      #
      # The field value may be a list of either DATE or DATE-TIME values,
      # decoding is tried first as a DATE-TIME, then as a DATE, if neither
      # works an InvalidEncodingError will be raised.
      def to_date
        begin
          ::Vcard.decode_date_time_list(value).collect do |d|
            # We get [ year, month, day, hour, min, sec, usec, tz ]
            Date.new(d[0], d[1], d[2])
          end
        rescue ::Vcard::InvalidEncodingError
          ::Vcard.decode_date_list(value).collect do |d|
            # We get [ year, month, day ]
            Date.new(*d)
          end
        end
      end

      # The value as text. Text can have escaped newlines, commas, and escape
      # characters, this method will strip them, if present.
      #
      # In theory, #value could also do this, but it would need to know that
      # the value is of type "TEXT", and often for text values the "VALUE"
      # parameter is not present, so knowledge of the expected type of the
      # field is required from the decoder.
      def to_text
        ::Vcard.decode_text(value)
      end

      # The undecoded value, see +value+.
      def value_raw
        @value
      end

      # TODO def pretty_print() ...

      # Set the group of this field to +group+.
      def group=(group)
        mutate(group, @name, @params, @value)
        group
      end

      # Set the value of this field to +value+.  Valid values are as in
      # Field.create().
      def value=(value)
        mutate(@group, @name, @params, value)
        value
      end

      # Convert +value+ to text, then assign.
      #
      # TODO - unimplemented
      def text=(text)
      end

      # Set a the param +pname+'s value to +pvalue+, replacing any value it
      # currently has. See Field.create() for a description of +pvalue+.
      #
      # Example:
      #  if field["TYPE"]
      #    field["TYPE"] << "HOME"
      #  else
      #    field["TYPE"] = [ "HOME" ]
      #  end
      #
      # TODO - this could be an alias to #pvalue_set
      def []=(pname,pvalue)
        unless pvalue.respond_to?(:to_ary)
          pvalue = [ pvalue ]
        end

        h = @params.dup

        h[pname.upcase] = pvalue

        mutate(@group, @name, h, @value)
        pvalue
      end

      # Add +pvalue+ to the param +pname+'s value. The values are treated as a
      # set so duplicate values won't occur, and String values are case
      # insensitive.  See Field.create() for a description of +pvalue+.
      def pvalue_iadd(pname, pvalue)
        pname = pname.upcase

        # Get a uniq set, where strings are compared case-insensitively.
        values = [ pvalue, @params[pname] ].flatten.compact
        values = values.collect do |v|
          if v.respond_to? :to_str
            v = v.to_str.upcase
          end
          v
        end
        values.uniq!

        h = @params.dup

        h[pname] = values

        mutate(@group, @name, h, @value)
        values
      end

      # Delete +pvalue+ from the param +pname+'s value. The values are treated
      # as a set so duplicate values won't occur, and String values are case
      # insensitive.  +pvalue+ must be a single String or Symbol.
      def pvalue_idel(pname, pvalue)
        pname = pname.upcase
        if pvalue.respond_to? :to_str
          pvalue = pvalue.to_str.downcase
        end

        # Get a uniq set, where strings are compared case-insensitively.
        values = [ nil, @params[pname] ].flatten.compact
        values = values.collect do |v|
          if v.respond_to? :to_str
            v = v.to_str.downcase
          end
          v
        end
        values.uniq!
        values.delete pvalue

        h = @params.dup

        h[pname] = values

        mutate(@group, @name, h, @value)
        values
      end

      # FIXME - should change this so it doesn't assign to @line here, so @line
      # is used to preserve original encoding. That way, #encode can only wrap
      # new fields, not old fields.
      def mutate(g, n, p, v) #:nodoc:
        line = Field.encode0(g, n, p, v)

        begin
          @group, @name, @params, @value = Field.decode0(line)
          @line = line
        rescue ::Vcard::InvalidEncodingError => e
          raise ArgumentError, e.to_s
        end
        self
      end

      private :mutate
    end
  end
end


# Copyright (C) 2008 Sam Roberts

# This library is free software; you can redistribute it and/or modify
# it under the same terms as the ruby language itself, see the file
# VPIM-LICENSE.txt for details.

module Vcard
  # A vCard, a specialization of a directory info object.
  #
  # The vCard format is specified by:
  # - RFC2426[http://www.ietf.org/rfc/rfc2426.txt]: vCard MIME Directory Profile (vCard 3.0)
  # - RFC2425[http://www.ietf.org/rfc/rfc2425.txt]: A MIME Content-Type for Directory Information
  #
  # This implements vCard 3.0, but it is also capable of working with vCard 2.1
  # if used with care.
  #
  # All line values can be accessed with Vcard#value, Vcard#values, or even by
  # iterating through Vcard#lines. Line types that don't have specific support
  # and non-standard line types ("X-MY-SPECIAL", for example) will be returned
  # as a String, with any base64 or quoted-printable encoding removed.
  #
  # Specific support exists to return more useful values for the standard vCard
  # types, where appropriate.
  #
  # The wrapper functions (#birthday, #nicknames, #emails, etc.) exist
  # partially as an API convenience, and partially as a place to document
  # the values returned for the more complex types, like PHOTO and EMAIL.
  #
  # For types that do not sensibly occur multiple times (like BDAY or GEO),
  # sometimes a wrapper exists only to return a single line, using #value.
  # However, if you find the need, you can still call #values to get all the
  # lines, and both the singular and plural forms will eventually be
  # implemented.
  #
  # For more information see:
  # - RFC2426[http://www.ietf.org/rfc/rfc2426.txt]: vCard MIME Directory Profile (vCard 3.0)
  # - RFC2425[http://www.ietf.org/rfc/rfc2425.txt]: A MIME Content-Type for Directory Information
  # - vCard2.1[http://www.imc.org/pdi/pdiproddev.html]: vCard 2.1 Specifications
  #
  # vCards are usually transmitted in files with <code>.vcf</code>
  # extensions.
  #
  # = Examples
  #
  # - link:ex_mkvcard.txt: example of creating a vCard
  # - link:ex_cpvcard.txt: example of copying and them modifying a vCard
  # - link:ex_mkv21vcard.txt: example of creating version 2.1 vCard
  # - link:mutt-aliases-to-vcf.txt: convert a mutt aliases file to vCards
  # - link:ex_get_vcard_photo.txt: pull photo data from a vCard
  # - link:ab-query.txt: query the OS X Address Book to find vCards
  # - link:vcf-to-mutt.txt: query vCards for matches, output in formats useful
  #   with Mutt (see link:README.mutt for details)
  # - link:tabbed-file-to-vcf.txt: convert a tab-delimited file to vCards, a
  #   (small but) complete application contributed by Dane G. Avilla, thanks!
  # - link:vcf-to-ics.txt: example of how to create calendars of birthdays from vCards
  # - link:vcf-dump.txt: utility for dumping contents of .vcf files
  class Vcard < DirectoryInfo

    # Represents the value of an ADR field.
    #
    # #location, #preferred, and #delivery indicate information about how the
    # address is to be used, the other attributes are parts of the address.
    #
    # Using values other than those defined for #location or #delivery is
    # unlikely to be portable, or even conformant.
    #
    # All attributes are optional. #location and #delivery can be set to arrays
    # of strings.
    class Address
      # post office box (String)
      attr_accessor :pobox
      # seldom used, its not clear what it is for (String)
      attr_accessor :extended
      # street address (String)
      attr_accessor :street
      # usually the city (String)
      attr_accessor :locality
      # usually the province or state (String)
      attr_accessor :region
      # postal code (String)
      attr_accessor :postalcode
      # country name (String)
      attr_accessor :country
      # home, work (Array of String): the location referred to by the address
      attr_accessor :location
      # true, false (boolean): where this is the preferred address (for this location)
      attr_accessor :preferred
      # postal, parcel, dom (domestic), intl (international) (Array of String): delivery
      # type of this address
      attr_accessor :delivery

      # nonstandard types, their meaning is undefined (Array of String). These
      # might be found during decoding, but shouldn't be set during encoding.
      attr_reader :nonstandard

      # Used to simplify some long and tedious code. These symbols are in the
      # order required for the ADR field structured TEXT value, the order
      # cannot be changed.
      @@adr_parts = [
        :@pobox,
        :@extended,
        :@street,
        :@locality,
        :@region,
        :@postalcode,
        :@country,
      ]

      # TODO
      # - #location?
      # - #delivery?
      def initialize #:nodoc:
        # TODO - Add #label to support LABEL. Try to find LABEL
        # in either same group, or with sam params.
        @@adr_parts.each do |part|
          instance_variable_set(part, "")
        end

        @location = []
        @preferred = false
        @delivery = []
        @nonstandard = []
      end

      def encode #:nodoc:
        parts = @@adr_parts.map do |part|
          instance_variable_get(part)
        end

        value = ::Vcard.encode_text_list(parts, ";")

        params = [ @location, @delivery, @nonstandard ]
        params << "pref" if @preferred
        params = params.flatten.compact.map { |s| s.to_str.downcase }.uniq

        paramshash = {}

        paramshash["TYPE"] = params if params.first

        ::Vcard::DirectoryInfo::Field.create( "ADR", value, paramshash)
      end

      def Address.decode(card, field) #:nodoc:
        adr = new

        parts = ::Vcard.decode_text_list(field.value_raw, ";")

        @@adr_parts.each_with_index do |part,i|
          adr.instance_variable_set(part, parts[i] || "")
        end

        params = field.pvalues("TYPE")

        if params
          params.each do |p|
            p.downcase!
            case p
            when "home", "work"
              adr.location << p
            when "postal", "parcel", "dom", "intl"
              adr.delivery << p
            when "pref"
              adr.preferred = true
            else
              adr.nonstandard << p
            end
          end
          # Strip duplicates
          [ adr.location, adr.delivery, adr.nonstandard ].each do |a|
            a.uniq!
          end
        end

        adr
      end
    end

    # Represents the value of an EMAIL field.
    class Email < String
      # true, false (boolean): whether this is the preferred email address
      attr_accessor :preferred
      # internet, x400 (String): the email address format, rarely specified
      # since the default is "internet"
      attr_accessor :format
      # home, work (Array of String): the location referred to by the address. The
      # inclusion of location parameters in a vCard seems to be non-conformant,
      # strictly speaking, but also seems to be widespread.
      attr_accessor :location
      # nonstandard types, their meaning is undefined (Array of String). These
      # might be found during decoding, but shouldn't be set during encoding.
      attr_reader :nonstandard

      def initialize(email="") #:nodoc:
        @preferred = false
        @format = "internet"
        @location = []
        @nonstandard = []
        super(email)
      end

      def inspect #:nodoc:
        s = "#<#{self.class.to_s}: #{to_str.inspect}"
        s << ", pref" if preferred
        s << ", #{format}" if format != "internet"
        s << ", " << @location.join(", ") if @location.first
        s << ", #{@nonstandard.join(", ")}" if @nonstandard.first
        s
      end

      def encode #:nodoc:
        value = to_str.strip

        if value.length < 1
          raise InvalidEncodingError, "EMAIL must have a value"
        end

        params = [ @location, @nonstandard ]
        params << @format if @format != "internet"
        params << "pref"  if @preferred

        params = params.flatten.compact.map { |s| s.to_str.downcase }.uniq

        paramshash = {}

        paramshash["TYPE"] = params if params.first

        ::Vcard::DirectoryInfo::Field.create("EMAIL", value, paramshash)
      end

      def Email.decode(field) #:nodoc:
        value = field.to_text.strip

        if value.length < 1
          raise InvalidEncodingError, "EMAIL must have a value"
        end

        eml = Email.new(value)

        params = field.pvalues("TYPE")

        if params
          params.each do |p|
            p.downcase!
            case p
            when "home", "work"
              eml.location << p
            when "pref"
              eml.preferred = true
            when "x400", "internet"
              eml.format = p
            else
              eml.nonstandard << p
            end
          end
          # Strip duplicates
          [ eml.location, eml.nonstandard ].each do |a|
            a.uniq!
          end
        end

        eml
      end
    end

    # Represents the value of a TEL field.
    #
    # The value is supposed to be a "X.500 Telephone Number" according to RFC
    # 2426, but that standard is not freely available. Otherwise, anything that
    # looks like a phone number should be OK.
    class Telephone < String
      # true, false (boolean): whether this is the preferred email address
      attr_accessor :preferred
      # home, work, cell, car, pager (Array of String): the location
      # of the device
      attr_accessor :location
      # voice, fax, video, msg, bbs, modem, isdn, pcs (Array of String): the
      # capabilities of the device
      attr_accessor :capability
      # nonstandard types, their meaning is undefined (Array of String). These
      # might be found during decoding, but shouldn't be set during encoding.
      attr_reader :nonstandard

      def initialize(telephone="") #:nodoc:
        @preferred = false
        @location = []
        @capability = []
        @nonstandard = []
        super(telephone)
      end

      def inspect #:nodoc:
        s = "#<#{self.class.to_s}: #{to_str.inspect}"
        s << ", pref" if preferred
        s << ", " << @location.join(", ") if @location.first
        s << ", " << @capability.join(", ") if @capability.first
        s << ", #{@nonstandard.join(", ")}" if @nonstandard.first
        s
      end

      def encode #:nodoc:
        value = to_str.strip

        if value.length < 1
          raise InvalidEncodingError, "TEL must have a value"
        end

        params = [ @location, @capability, @nonstandard ]
        params << "pref"  if @preferred

        params = params.flatten.compact.map { |s| s.to_str.downcase }.uniq

        paramshash = {}

        paramshash["TYPE"] = params if params.first

        ::Vcard::DirectoryInfo::Field.create( "TEL", value, paramshash)
      end

      def Telephone.decode(field) #:nodoc:
        value = field.to_text.strip

        if value.length < 1
          raise InvalidEncodingError, "TEL must have a value"
        end

        tel = Telephone.new(value)

        params = field.pvalues("TYPE")

        if params
          params.each do |p|
            p.downcase!
            case p
            when "home", "work", "cell", "car", "pager"
              tel.location << p
            when "voice", "fax", "video", "msg", "bbs", "modem", "isdn", "pcs"
              tel.capability << p
            when "pref"
              tel.preferred = true
            else
              tel.nonstandard << p
            end
          end
          # Strip duplicates
          [ tel.location, tel.capability, tel.nonstandard ].each do |a|
            a.uniq!
          end
        end

        tel
      end
    end

    # The name from a vCard, including all the components of the N: and FN:
    # fields.
    class Name
      # family name, from N
      attr_accessor :family
      # given name, from N
      attr_accessor :given
      # additional names, from N
      attr_accessor :additional
      # such as "Ms." or "Dr.", from N
      attr_accessor :prefix
      # such as "BFA", from N
      attr_accessor :suffix
      # full name, the FN field. FN is a formatted version of the N field,
      # intended to be in a form more aligned with the cultural conventions of
      # the vCard owner than +formatted+ is.
      attr_accessor :fullname
      # all the components of N formtted as "#{prefix} #{given} #{additional} #{family}, #{suffix}"
      attr_reader   :formatted

      # Override the attr reader to make it dynamic
      remove_method :formatted
      def formatted #:nodoc:
        f = [ @prefix, @given, @additional, @family ].map{|i| i == "" ? nil : i.strip}.compact.join(" ")
        if @suffix != ""
          f << ", " << @suffix
        end
        f
      end

      def initialize(n="", fn="") #:nodoc:
        n = ::Vcard.decode_text_list(n, ";") do |item|
          item.strip
        end

        @family     = n[0] || ""
        @given      = n[1] || ""
        @additional = n[2] || ""
        @prefix     = n[3] || ""
        @suffix     = n[4] || ""

        # FIXME - make calls to #fullname fail if fn is nil
        @fullname = (fn || "").strip
      end

      def encode #:nodoc:
        ::Vcard::DirectoryInfo::Field.create("N", ::Vcard.encode_text_list([ @family, @given, @additional, @prefix, @suffix ].map{|n| n.strip}, ";"))
      end

      def encode_fn #:nodoc:
        fn = @fullname.strip
        if @fullname.length == 0
          fn = formatted
        end
        ::Vcard::DirectoryInfo::Field.create("FN", fn)
      end
    end

    def decode_invisible(field) #:nodoc:
      nil
    end

    def decode_default(field) #:nodoc:
      Line.new( field.group, field.name, field.value )
    end

    def decode_version(field) #:nodoc:
      Line.new( field.group, field.name, (field.value.to_f * 10).to_i )
    end

    def decode_text(field) #:nodoc:
      Line.new( field.group, field.name, ::Vcard.decode_text(field.value_raw) )
    end

    def decode_n(field) #:nodoc:
      Line.new( field.group, field.name, Name.new(field.value, self["FN"]).freeze )
    end

    def decode_date_or_datetime(field) #:nodoc:
      date = nil
      begin
        date = ::Vcard.decode_date_to_date(field.value_raw)
      rescue ::Vcard::InvalidEncodingError
        date = ::Vcard.decode_date_time_to_datetime(field.value_raw)
      end
      Line.new( field.group, field.name, date )
    end

    def decode_bday(field) #:nodoc:
      begin
        return decode_date_or_datetime(field)

      rescue ::Vcard::InvalidEncodingError
        # Hack around BDAY dates hat are correct in the month and day, but have
        # some kind of garbage in the year.
        if field.value =~ /^\s*(\d+)-(\d+)-(\d+)\s*$/
          y = $1.to_i
          m = $2.to_i
          d = $3.to_i
          if(y < 1900)
            y = Time.now.year
          end
          Line.new( field.group, field.name, Date.new(y, m, d) )
        else
          raise
        end
      end
    end

    def decode_geo(field) #:nodoc:
      geo = ::Vcard.decode_list(field.value_raw, ";") do |item| item.to_f end
      Line.new( field.group, field.name, geo )
    end

    def decode_address(field) #:nodoc:
      Line.new( field.group, field.name, Address.decode(self, field) )
    end

    def decode_email(field) #:nodoc:
      Line.new( field.group, field.name, Email.decode(field) )
    end

    def decode_telephone(field) #:nodoc:
      Line.new( field.group, field.name, Telephone.decode(field) )
    end

    def decode_list_of_text(field) #:nodoc:
      Line.new(field.group, field.name, ::Vcard.decode_text_list(field.value_raw).select{|t| t.length > 0}.uniq)
    end

    def decode_structured_text(field) #:nodoc:
      Line.new( field.group, field.name, ::Vcard.decode_text_list(field.value_raw, ";") )
    end

    def decode_uri(field) #:nodoc:
      Line.new( field.group, field.name, Attachment::Uri.new(field.value, nil) )
    end

    def decode_agent(field) #:nodoc:
      case field.kind
      when "text"
        decode_text(field)
      when "uri"
        decode_uri(field)
      when "vcard", nil
        Line.new( field.group, field.name, ::Vcard.decode(::Vcard.decode_text(field.value_raw)).first )
      else
        raise InvalidEncodingError, "AGENT type #{field.kind} is not allowed"
      end
    end

    def decode_attachment(field) #:nodoc:
      Line.new( field.group, field.name, Attachment.decode(field, "binary", "TYPE") )
    end

    @@decode = {
      "BEGIN"      => :decode_invisible, # Don't return delimiter
      "END"        => :decode_invisible, # Don't return delimiter
      "FN"         => :decode_invisible, # Returned as part of N.

      "ADR"        => :decode_address,
      "AGENT"      => :decode_agent,
      "BDAY"       => :decode_bday,
      "CATEGORIES" => :decode_list_of_text,
      "EMAIL"      => :decode_email,
      "GEO"        => :decode_geo,
      "KEY"        => :decode_attachment,
      "LOGO"       => :decode_attachment,
      "MAILER"     => :decode_text,
      "N"          => :decode_n,
      "NAME"       => :decode_text,
      "NICKNAME"   => :decode_list_of_text,
      "NOTE"       => :decode_text,
      "ORG"        => :decode_structured_text,
      "PHOTO"      => :decode_attachment,
      "PRODID"     => :decode_text,
      "PROFILE"    => :decode_text,
      "REV"        => :decode_date_or_datetime,
      "ROLE"       => :decode_text,
      "SOUND"      => :decode_attachment,
      "SOURCE"     => :decode_text,
      "TEL"        => :decode_telephone,
      "TITLE"      => :decode_text,
      "UID"        => :decode_text,
      "URL"        => :decode_uri,
      "VERSION"    => :decode_version,
    }

    @@decode.default = :decode_default

    # Cache of decoded lines/fields, so we don't have to decode a field more than once.
    attr_reader :cache #:nodoc:

    # An entry in a vCard. The #value object's type varies with the kind of
    # line (the #name), and on how the line was encoded. The objects returned
    # for a specific kind of line are often extended so that they support a
    # common set of methods. The goal is to allow all types of objects for a
    # kind of line to be treated with some uniformity, but still allow specific
    # handling for the various value types if desired.
    #
    # See the specific methods for details.
    class Line
      attr_reader :group
      attr_reader :name
      attr_reader :value

      def initialize(group, name, value) #:nodoc:
        @group, @name, @value = (group||""), name.to_str, value
      end

      def self.decode(decode, card, field) #:nodoc:
        card.cache[field] || (card.cache[field] = card.send(decode[field.name], field))
      end
    end

    #@lines = {} FIXME - dead code

    # Return line for a field
    def f2l(field) #:nodoc:
      begin
        Line.decode(@@decode, self, field)
      rescue InvalidEncodingError
        # Skip invalidly encoded fields.
      end
    end

    # With no block, returns an Array of Line. If +name+ is specified, the
    # Array will only contain the +Line+s with that +name+. The Array may be
    # empty.
    #
    # If a block is given, each Line will be yielded instead of being returned
    # in an Array.
    def lines(name=nil) #:yield: Line
      # FIXME - this would be much easier if #lines was #each, and there was a
      # different #lines that returned an Enumerator that used #each
      unless block_given?
        map do |f|
          if( !name || f.name?(name) )
            f2l(f)
          else
            nil
          end
        end.compact
      else
        each do |f|
          if( !name || f.name?(name) )
            line = f2l(f)
            if line
              yield line
            end
          end
        end
        self
      end
    end

    private_class_method :new

    def initialize(fields, profile) #:nodoc:
      @cache = {}
      super(fields, profile)
    end

    # Create a vCard 3.0 object with the minimum required fields, plus any
    # +fields+ you want in the card (they can also be added later).
    def self.create(fields = [] )
      fields.unshift Field.create("VERSION", "3.0")
      super(fields, "VCARD")
    end

    # Decode a collection of vCards into an array of Vcard objects.
    #
    # +card+ can be either a String or an IO object.
    #
    # Since vCards are self-delimited (by a BEGIN:vCard and an END:vCard),
    # multiple vCards can be concatenated into a single directory info object.
    # They may or may not be related. For example, AddressBook.app (the OS X
    # contact manager) will export multiple selected cards in this format.
    #
    # Input data will be converted from unicode if it is detected. The heuristic
    # is based on the first bytes in the string:
    # - 0xEF 0xBB 0xBF: UTF-8 with a BOM, the BOM is stripped
    # - 0xFE 0xFF: UTF-16 with a BOM (big-endian), the BOM is stripped and string
    #   is converted to UTF-8
    # - 0xFF 0xFE: UTF-16 with a BOM (little-endian), the BOM is stripped and string
    #   is converted to UTF-8
    # - 0x00 "B" or 0x00 "b": UTF-16 (big-endian), the string is converted to UTF-8
    # - "B" 0x00 or "b" 0x00: UTF-16 (little-endian), the string is converted to UTF-8
    #
    # If you know that you have only one vCard, then you can decode that
    # single vCard by doing something like:
    #
    #   vcard = Vcard.decode(card_data).first
    #
    # Note: Should the import encoding be remembered, so that it can be reencoded in
    # the same format?
    def self.decode(card)
      if card.respond_to? :to_str
        string = card.to_str
      elsif card.respond_to? :read
        string = card.read(nil)
      else
        raise ArgumentError, "Vcard.decode cannot be called with a #{card.type}"
      end

      string.force_encoding(Encoding::UTF_8)
      entities = ::Vcard.expand(::Vcard.decode(string))

      # Since all vCards must have a begin/end, the top-level should consist
      # entirely of entities/arrays, even if its a single vCard.
      if entities.detect { |e| ! e.kind_of? Array }
        raise "Not a valid vCard"
      end

      vcards = []

      for e in entities
        vcards.push(new(e.flatten, "VCARD"))
      end

      vcards
    end

    # The value of the field named +name+, optionally limited to fields of
    # type +type+. If no match is found, nil is returned, if multiple matches
    # are found, the first match to have one of its type values be "PREF"
    # (preferred) is returned, otherwise the first match is returned.
    #
    # FIXME - this will become an alias for #value.
    def [](name, type=nil)
      fields = enum_by_name(name).find_all { |f| type == nil || f.type?(type) }

      valued = fields.select { |f| f.value != "" }
      if valued.first
        fields = valued
      end

      # limit to preferred, if possible
      pref = fields.select { |f| f.pref? }

      if pref.first
        fields = pref
      end

      fields.first ? fields.first.value : nil
    end

    # Return the Line#value for a specific +name+, and optionally for a
    # specific +type+.
    #
    # If no line with the +name+ (and, optionally, +type+) exists, nil is
    # returned.
    #
    # If multiple lines exist, the order of preference is:
    # - lines with values over lines without
    # - lines with a type of "pref" over lines without
    # If multiple lines are equally preferred, then the first line will be
    # returned.
    #
    # This is most useful when looking for a line that can not occur multiple
    # times, or when the line can occur multiple times, and you want to pick
    # the first preferred line of a specific type. See #values if you need to
    # access all the lines.
    #
    # Note that the +type+ field parameter is used for different purposes by
    # the various kinds of vCard lines, but for the addressing lines (ADR,
    # LABEL, TEL, EMAIL) it is has a reasonably consistent usage. Each
    # addressing line can occur multiple times, and a +type+ of "pref"
    # indicates that a particular line is the preferred line. Other +type+
    # values tend to indicate some information about the location ("home",
    # "work", ...) or some detail about the address ("cell", "fax", "voice",
    # ...). See the methods for the specific types of line for information
    # about supported types and their meaning.
    def value(name, type = nil)
      fields = enum_by_name(name).find_all { |f| type == nil || f.type?(type) }

      valued = fields.select { |f| f.value != "" }
      if valued.first
        fields = valued
      end

      pref = fields.select { |f| f.pref? }

      if pref.first
        fields = pref
      end

      if fields.first
        line = begin
                 Line.decode(@@decode, self, fields.first)
               rescue ::Vcard::InvalidEncodingError
               end

        if line
          return line.value
        end
      end

      nil
    end

    # A variant of #lines that only iterates over specific Line names. Since
    # the name is known, only the Line#value is returned or yielded.
    def values(name)
      unless block_given?
        lines(name).map { |line| line.value }
      else
        lines(name) { |line| yield line.value }
      end
    end

    # The first ADR value of type +type+, a Address. Any of the location or
    # delivery attributes of Address can be used as +type+. A wrapper around
    # #value("ADR", +type+).
    def address(type=nil)
      value("ADR", type)
    end

    # The ADR values, an array of Address. If a block is given, the values are
    # yielded. A wrapper around #values("ADR").
    def addresses #:yield:address
      values("ADR")
    end

    # The AGENT values. Each AGENT value is either a String, a Uri, or a Vcard.
    # If a block is given, the values are yielded. A wrapper around
    # #values("AGENT").
    def agents #:yield:agent
      values("AGENT")
    end

    # The BDAY value as either a Date or a DateTime, or nil if there is none.
    #
    # If the BDAY value is invalidly formatted, a feeble heuristic is applied
    # to find the month and year, and return a Date in the current year.
    def birthday
      value("BDAY")
    end

    # The CATEGORIES values, an array of String. A wrapper around
    # #value("CATEGORIES").
    def categories
      value("CATEGORIES")
    end

    # The first EMAIL value of type +type+, a Email. Any of the location
    # attributes of Email can be used as +type+. A wrapper around
    # #value("EMAIL", +type+).
    def email(type=nil)
      value("EMAIL", type)
    end

    # The EMAIL values, an array of Email. If a block is given, the values are
    # yielded. A wrapper around #values("EMAIL").
    def emails #:yield:email
      values("EMAIL")
    end

    # The GEO value, an Array of two Floats, +[ latitude, longitude]+.  North
    # of the equator is positive latitude, east of the meridian is positive
    # longitude.  See RFC2445 for more info, there are lots of special cases
    # and RFC2445"s description is more complete thant RFC2426.
    def geo
      value("GEO")
    end

    # Return an Array of KEY Line#value, or yield each Line#value if a block
    # is given. A wrapper around #values("KEY").
    #
    # KEY is a public key or authentication certificate associated with the
    # object that the vCard represents. It is not commonly used, but could
    # contain a X.509 or PGP certificate.
    #
    # See Attachment for a description of the value.
    def keys(&proc) #:yield: Line.value
      values("KEY", &proc)
    end

    # Return an Array of LOGO Line#value, or yield each Line#value if a block
    # is given. A wrapper around #values("LOGO").
    #
    # LOGO is a graphic image of a logo associated with the object the vCard
    # represents. Its not common, but would probably be equivalent to the logo
    # on a printed card.
    #
    # See Attachment for a description of the value.
    def logos(&proc) #:yield: Line.value
      values("LOGO", &proc)
    end

    ## MAILER

    # The N and FN as a Name object.
    #
    # N is required for a vCards, this raises InvalidEncodingError if
    # there is no N so it cannot return nil.
    def name
      value("N") || raise(::Vcard::InvalidEncodingError, "Missing mandatory N field")
    end

    # The first NICKNAME value, nil if there are none.
    def nickname
      v = value("NICKNAME")
      v = v.first if v
      v
    end

    # The NICKNAME values, an array of String. The array may be empty.
    def nicknames
      values("NICKNAME").flatten.uniq
    end

    # The NOTE value, a String. A wrapper around #value("NOTE").
    def note
      value("NOTE")
    end

    # The ORG value, an Array of String. The first string is the organization,
    # subsequent strings are departments within the organization. A wrapper
    # around #value("ORG").
    def org
      value("ORG")
    end

    # Return an Array of PHOTO Line#value, or yield each Line#value if a block
    # is given. A wrapper around #values("PHOTO").
    #
    # PHOTO is an image or photograph information that annotates some aspect of
    # the object the vCard represents. Commonly there is one PHOTO, and it is a
    # photo of the person identified by the vCard.
    #
    # See Attachment for a description of the value.
    def photos(&proc) #:yield: Line.value
      values("PHOTO", &proc)
    end

    ## PRODID

    ## PROFILE

    ## REV

    ## ROLE

    # Return an Array of SOUND Line#value, or yield each Line#value if a block
    # is given. A wrapper around #values("SOUND").
    #
    # SOUND is digital sound content information that annotates some aspect of
    # the vCard. By default this type is used to specify the proper
    # pronunciation of the name associated with the vCard. It is not commonly
    # used. Also, note that there is no mechanism available to specify that the
    # SOUND is being used for anything other than the default.
    #
    # See Attachment for a description of the value.
    def sounds(&proc) #:yield: Line.value
      values("SOUND", &proc)
    end

    ## SOURCE

    # The first TEL value of type +type+, a Telephone. Any of the location or
    # capability attributes of Telephone can be used as +type+. A wrapper around
    # #value("TEL", +type+).
    def telephone(type=nil)
      value("TEL", type)
    end

    # The TEL values, an array of Telephone. If a block is given, the values are
    # yielded. A wrapper around #values("TEL").
    def telephones #:yield:tel
      values("TEL")
    end

    # The TITLE value, a text string specifying the job title, functional
    # position, or function of the object the card represents. A wrapper around
    # #value("TITLE").
    def title
      value("TITLE")
    end

    ## UID

    # The URL value, a Attachment::Uri. A wrapper around #value("URL").
    def url
      value("URL")
    end

    # The URL values, an Attachment::Uri. A wrapper around #values("URL").
    def urls
      values("URL")
    end

    # The VERSION multiplied by 10 as an Integer.  For example, a VERSION:2.1
    # vCard would have a version of 21, and a VERSION:3.0 vCard would have a
    # version of 30.
    #
    # VERSION is required for a vCard, this raises InvalidEncodingError if
    # there is no VERSION so it cannot return nil.
    def version
      v = value("VERSION")
      unless v
        raise ::Vcard::InvalidEncodingError, "Invalid vCard - it has no version field!"
      end
      v
    end

    # Make changes to a vCard.
    #
    # Yields a Vcard::Vcard::Maker that can be used to modify this vCard.
    def make #:yield: maker
      ::Vcard::Vcard::Maker.make2(self) do |maker|
        yield maker
      end
    end

    # Delete +line+ if block yields true.
    def delete_if #:nodoc: :yield: line
      # Do in two steps to not mess up progress through the enumerator.
      rm = []

      each do |f|
        line = f2l(f)
        if line && yield(line)
          rm << f

          # Hack - because we treat N and FN as one field
          if f.name? "N"
            rm << field("FN")
          end
        end
      end

      rm.each do |f|
        @fields.delete( f )
        @cache.delete( f )
      end

    end

    # A class to make and make changes to vCards.
    #
    # It can be used to create completely new vCards using Vcard#make2.
    #
    # Its is also yielded from Vcard::Vcard#make, in which case it allows a kind
    # of transactional approach to changing vCards, so their values can be
    # validated after any changes have been made.
    #
    # Examples:
    # - link:ex_mkvcard.txt: example of creating a vCard
    # - link:ex_cpvcard.txt: example of copying and them modifying a vCard
    # - link:ex_mkv21vcard.txt: example of creating version 2.1 vCard
    # - link:ex_mkyourown.txt: example of adding support for new fields to Vcard::Maker
    class Maker
      # Make a vCard.
      #
      # Yields +maker+, a Vcard::Vcard::Maker which allows fields to be added to
      # +card+, and returns +card+, a Vcard::Vcard.
      #
      # If +card+ is nil or not provided a new Vcard::Vcard is created and the
      # fields are added to it.
      #
      # Defaults:
      # - vCards must have both an N and an FN field, #make2 will fail if there
      #   is no N field in the +card+ when your block is finished adding fields.
      # - If there is an N field, but no FN field, FN will be set from the
      #   information in N, see Vcard::Name#preformatted for more information.
      # - vCards must have a VERSION field. If one does not exist when your block is
      #   is finished it will be set to 3.0.
      def self.make2(card = ::Vcard::Vcard.create, &block) # :yields: maker
        new(nil, card).make(&block)
      end

      # Deprecated, use #make2.
      #
      # If set, the FN field will be set to +full_name+. Otherwise, FN will
      # be set from the values in #name.
      def self.make(full_name = nil, &block) # :yields: maker
        new(full_name, ::Vcard::Vcard.create).make(&block)
      end

      def make # :nodoc:
        yield self
        unless @card["N"]
          raise Unencodeable, "N field is mandatory"
        end
        fn = @card.field("FN")
        if fn && fn.value.strip.length == 0
          @card.delete(fn)
          fn = nil
        end
        unless fn
          @card << ::Vcard::DirectoryInfo::Field.create("FN", ::Vcard::Vcard::Name.new(@card["N"], "").formatted)
        end
        unless @card["VERSION"]
          @card << ::Vcard::DirectoryInfo::Field.create("VERSION", "3.0")
        end
        @card
      end

      private

      def initialize(full_name, card) # :nodoc:
        @card = card || ::Vcard::Vcard::create
        if full_name
          @card << ::Vcard::DirectoryInfo::Field.create("FN", full_name.strip )
        end
      end

      public

      # Deprecated, see #name.
      #
      # Use
      #   maker.name do |n| n.fullname = "foo" end
      # to set just fullname, or set the other fields to set fullname and the
      # name.
      def fullname=(fullname) #:nodoc: bacwards compat
        if @card.field("FN")
          raise ::Vcard::InvalidEncodingError, "Not allowed to add more than one FN field to a vCard."
        end
        @card << ::Vcard::DirectoryInfo::Field.create( "FN", fullname );
      end

      # Set the name fields, N and FN.
      #
      # Attributes of +name+ are:
      # - family: family name
      # - given: given name
      # - additional: additional names
      # - prefix: such as "Ms." or "Dr."
      # - suffix: such as "BFA", or "Sensei"
      #
      # +name+ is a Vcard::Name.
      #
      # All attributes are optional, though have all names be zero-length
      # strings isn't really in the spirit of  things. FN's value will be set
      # to Vcard::Name#formatted if Vcard::Name#fullname isn't given a specific
      # value.
      #
      # Warning: This is the only mandatory field.
      def name #:yield:name
        x = begin
              @card.name.dup
            rescue
              ::Vcard::Vcard::Name.new
            end

        yield x

        x.fullname.strip!

        delete_if do |line|
          line.name == "N"
        end

        @card << x.encode
        @card << x.encode_fn

        self
      end

      alias :add_name :name #:nodoc: backwards compatibility

      # Add an address field, ADR. +address+ is a Vcard::Vcard::Address.
      def add_addr # :yield: address
        x = ::Vcard::Vcard::Address.new
        yield x
        @card << x.encode
        self
      end

      # Add a telephone field, TEL. +tel+ is a Vcard::Vcard::Telephone.
      #
      # The block is optional, its only necessary if you want to specify
      # the optional attributes.
      def add_tel(number) # :yield: tel
        x = ::Vcard::Vcard::Telephone.new(number)
        if block_given?
          yield x
        end
        @card << x.encode
        self
      end

      # Add an email field, EMAIL. +email+ is a Vcard::Vcard::Email.
      #
      # The block is optional, its only necessary if you want to specify
      # the optional attributes.
      def add_email(email) # :yield: email
        x = ::Vcard::Vcard::Email.new(email)
        if block_given?
          yield x
        end
        @card << x.encode
        self
      end

      # Set the nickname field, NICKNAME.
      #
      # It can be set to a single String or an Array of String.
      def nickname=(nickname)
        delete_if { |l| l.name == "NICKNAME" }

        @card << ::Vcard::DirectoryInfo::Field.create( "NICKNAME", nickname );
      end

      # Add a birthday field, BDAY.
      #
      # +birthday+ must be a time or date object.
      #
      # Warning: It may confuse both humans and software if you add multiple
      # birthdays.
      def birthday=(birthday)
        if !birthday.respond_to? :month
          raise ArgumentError, "birthday must be a date or time object."
        end
        delete_if { |l| l.name == "BDAY" }
        @card << ::Vcard::DirectoryInfo::Field.create( "BDAY", birthday );
      end

      # Add a note field, NOTE. The +note+ String can contain newlines, they
      # will be escaped.
      def add_note(note)
        @card << ::Vcard::DirectoryInfo::Field.create( "NOTE", ::Vcard.encode_text(note) );
      end

      # Add an instant-messaging/point of presence address field, IMPP. The address
      # is a URL, with the syntax depending on the protocol.
      #
      # Attributes of IMPP are:
      # - preferred: true - set if this is the preferred address
      # - location: home, work, mobile - location of address
      # - purpose: personal,business - purpose of communications
      #
      # All attributes are optional, and so is the block.
      #
      # The URL syntaxes for the messaging schemes is fairly complicated, so I
      # don't try and build the URLs here, maybe in the future. This forces
      # the user to know the URL for their own address, hopefully not too much
      # of a burden.
      #
      # IMPP is defined in draft-jennings-impp-vcard-04.txt. It refers to the
      # URI scheme of a number of messaging protocols, but doesn't give
      # references to all of them:
      # - "xmpp" indicates to use XMPP, draft-saintandre-xmpp-uri-06.txt
      # - "irc" or "ircs" indicates to use IRC, draft-butcher-irc-url-04.txt
      # - "sip" indicates to use SIP/SIMPLE, RFC 3261
      # - "im" or "pres" indicates to use a CPIM or CPP gateway, RFC 3860 and RFC 3859
      # - "ymsgr" indicates to use yahoo
      # - "msn" might indicate to use Microsoft messenger
      # - "aim" indicates to use AOL
      #
      def add_impp(url) # :yield: impp
        params = {}

        if block_given?
          x = Struct.new( :location, :preferred, :purpose ).new

          yield x

          x[:preferred] = "PREF" if x[:preferred]

          types = x.to_a.flatten.compact.map { |s| s.downcase }.uniq

          params["TYPE"] = types if types.first
        end

        @card << ::Vcard::DirectoryInfo::Field.create( "IMPP", url, params)
        self
      end

      # Add an X-AIM account name where +xaim+ is an AIM screen name.
      #
      # I don't know if this is conventional, or supported by anything other
      # than AddressBook.app, but an example is:
      #   X-AIM;type=HOME;type=pref:exampleaccount
      #
      # Attributes of X-AIM are:
      # - preferred: true - set if this is the preferred address
      # - location: home, work, mobile - location of address
      #
      # All attributes are optional, and so is the block.
      def add_x_aim(xaim) # :yield: xaim
        params = {}

        if block_given?
          x = Struct.new( :location, :preferred ).new

          yield x

          x[:preferred] = "PREF" if x[:preferred]

          types = x.to_a.flatten.compact.map { |s| s.downcase }.uniq

          params["TYPE"] = types if types.first
        end

        @card << ::Vcard::DirectoryInfo::Field.create( "X-AIM", xaim, params)
        self
      end


      # Add a photo field, PHOTO.
      #
      # Attributes of PHOTO are:
      # - image: set to image data to include inline
      # - link: set to the URL of the image data
      # - type: string identifying the image type, supposed to be an "IANA registered image format",
      #     or a non-registered image format (usually these start with an x-)
      #
      # An error will be raised if neither image or link is set, or if both image
      # and link is set.
      #
      # Setting type is optional for a link image, because either the URL, the
      # image file extension, or a HTTP Content-Type may specify the type. If
      # it's not a link, setting type is mandatory, though it can be set to an
      # empty string, <code>''</code>, if the type is unknown.
      #
      # TODO - I'm not sure about this API. I'm thinking maybe it should be
      # #add_photo(image, type), and that I should detect when the image is a
      # URL, and make type mandatory if it wasn't a URL.
      def add_photo # :yield: photo
        x = Struct.new(:image, :link, :type).new
        yield x
        if x[:image] && x[:link]
          raise ::Vcard::InvalidEncodingError, "Image is not allowed to be both inline and a link."
        end

        value = x[:image] || x[:link]

        if !value
          raise ::Vcard::InvalidEncodingError, "A image link or inline data must be provided."
        end

        params = {}

        # Don't set type to the empty string.
        params["TYPE"] = x[:type] if( x[:type] && x[:type].length > 0 )

        if x[:link]
          params["VALUE"] = "URI"
        else # it's inline, base-64 encode it
          params["ENCODING"] = :b64
          if !x[:type]
            raise ::Vcard::InvalidEncodingError, "Inline image data must have it's type set."
          end
        end

        @card << ::Vcard::DirectoryInfo::Field.create( "PHOTO", value, params )
        self
      end

      # Set the title field, TITLE.
      #
      # It can be set to a single String.
      def title=(title)
        delete_if { |l| l.name == "TITLE" }

        @card << ::Vcard::DirectoryInfo::Field.create( "TITLE", title );
      end

      # Set the org field, ORG.
      #
      # It can be set to a single String or an Array of String.
      def org=(org)
        delete_if { |l| l.name == "ORG" }

        @card << ::Vcard::DirectoryInfo::Field.create( "ORG", org );
      end


      # Add a URL field, URL.
      def add_url(url)
        @card << ::Vcard::DirectoryInfo::Field.create( "URL", url.to_str );
      end

      # Add a Field, +field+.
      def add_field(field)
        fieldname = field.name.upcase
        case
        when [ "BEGIN", "END" ].include?(fieldname)
          raise ::Vcard::InvalidEncodingError, "Not allowed to manually add #{field.name} to a vCard."

        when [ "VERSION", "N", "FN" ].include?(fieldname)
          if @card.field(fieldname)
            raise ::Vcard::InvalidEncodingError, "Not allowed to add more than one #{fieldname} to a vCard."
          end
          @card << field

        else
          @card << field
        end
      end

      # Copy the fields from +card+ into self using #add_field. If a block is
      # provided, each Field from +card+ is yielded. The block should return a
      # Field to add, or nil.  The Field doesn't have to be the one yielded,
      # allowing the field to be copied and modified (see Field#copy) before adding, or
      # not added at all if the block yields nil.
      #
      # The vCard fields BEGIN and END aren't copied, and VERSION, N, and FN are copied
      # only if the card doesn't have them already.
      def copy(card) # :yields: Field
        card.each do |field|
          fieldname = field.name.upcase
          case
          when [ "BEGIN", "END" ].include?(fieldname)
            # Never copy these

          when [ "VERSION", "N", "FN" ].include?(fieldname) && @card.field(fieldname)
            # Copy these only if they don't already exist.

          else
            if block_given?
              field = yield field
            end

            if field
              add_field(field)
            end
          end
        end
      end

      # Delete +line+ if block yields true.
      def delete_if #:yield: line
        begin
          @card.delete_if do |line|
            yield line
          end
        rescue NoMethodError
          # FIXME - this is a hideous hack, allowing a DirectoryInfo to
          # be passed instead of a Vcard, and for it to almost work. Yuck.
        end
      end

    end
  end
end


module Vcard
  VERSION = "0.2.0"
end


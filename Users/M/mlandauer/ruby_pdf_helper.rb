require "tempfile"

# Make a pdftoxml method just like in Python
module PdfHelper
  def self.pdftoxml(data, options = "")
    # Write data to a temporary file (with a pdf extension)
    src = Tempfile.new(['pdftohtml_src.', '.pdf'])
    dst = Tempfile.new(['pdftohtml_dst.', '.xml'])

    src.write(data)
    src.close

    command = "/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes #{options} #{src.path} #{dst.path}"
    # Would be good to turn off output here
    system(command)

    result = dst.read

    # Cleanup
    src.unlink
    dst.unlink

    result
  end

  def self.find_column_no(columns, left, right)
    columns.find_index do |c|
      (left >= c[0] && left <= c[1]) || (right >= c[0] && right <= c[1]) || (left <= c[0] && right >= c[1])
    end
  end

  def self.extract_columns_from_pdf_text(texts)
    columns = []
    texts.each do |t|
      # See if there is any overlap between the current bit of text and any of the
      # preexisting columns
      left = t["left"].to_i
      right = t["left"].to_i + t["width"].to_i
      i = find_column_no(columns, left, right)
      if i
        puts "#{t.inner_text} is in column #{i}"
        # Update the boundary of the column based on the current text position
        columns[i] = [[left, columns[i][0]].min, [right, columns[i][1]].max]
      else
        puts "#{t.inner_text} is in new column"
        columns << [left, right]
      end
    end
    # And make sure the results are in order
    columns.sort{|a,b| a[0] <=> b[0]}
  end

  def self.extract_indices_from_pdf_text(texts, columns = nil)
    columns = extract_columns_from_pdf_text(texts) if columns.nil? 
    top, left, width = nil, nil, nil
    x, y = 0, 0
    texts = texts.map do |t|
      left = t["left"].to_i
      right = left + t["width"].to_i
      new_x = find_column_no(columns, left, right)
      # If we're back at the beginning of a row this is a new row
      y += 1 if new_x == 0 && x > 0
      x = new_x
      [x, y, t.inner_text]
    end
  end

  # Can pass in the optional columns if the automated finding of columns
  # doesn't work properly for some reason
  def self.extract_table_from_pdf_text(texts, columns = nil)
    texts = extract_indices_from_pdf_text(texts, columns)
    # Find the the range of indices
    max_x, max_y = texts.first
    texts.each do |t|
      max_x = [max_x, t[0]].max
      max_y = [max_y, t[1]].max
    end
    # Create an empty 2d array
    result = Array.new(max_y + 1) { |i| Array.new(max_x + 1) }
    texts.each do |t|
      x, y, text = t
      if result[y][x].nil? 
        result[y][x] = text
      else
        result[y][x] += "\n" + text
      end
    end
    result
  end
end

require "tempfile"

# Make a pdftoxml method just like in Python
module PdfHelper
  def self.pdftoxml(data, options = "")
    # Write data to a temporary file (with a pdf extension)
    src = Tempfile.new(['pdftohtml_src.', '.pdf'])
    dst = Tempfile.new(['pdftohtml_dst.', '.xml'])

    src.write(data)
    src.close

    command = "/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes #{options} #{src.path} #{dst.path}"
    # Would be good to turn off output here
    system(command)

    result = dst.read

    # Cleanup
    src.unlink
    dst.unlink

    result
  end

  def self.find_column_no(columns, left, right)
    columns.find_index do |c|
      (left >= c[0] && left <= c[1]) || (right >= c[0] && right <= c[1]) || (left <= c[0] && right >= c[1])
    end
  end

  def self.extract_columns_from_pdf_text(texts)
    columns = []
    texts.each do |t|
      # See if there is any overlap between the current bit of text and any of the
      # preexisting columns
      left = t["left"].to_i
      right = t["left"].to_i + t["width"].to_i
      i = find_column_no(columns, left, right)
      if i
        puts "#{t.inner_text} is in column #{i}"
        # Update the boundary of the column based on the current text position
        columns[i] = [[left, columns[i][0]].min, [right, columns[i][1]].max]
      else
        puts "#{t.inner_text} is in new column"
        columns << [left, right]
      end
    end
    # And make sure the results are in order
    columns.sort{|a,b| a[0] <=> b[0]}
  end

  def self.extract_indices_from_pdf_text(texts, columns = nil)
    columns = extract_columns_from_pdf_text(texts) if columns.nil? 
    top, left, width = nil, nil, nil
    x, y = 0, 0
    texts = texts.map do |t|
      left = t["left"].to_i
      right = left + t["width"].to_i
      new_x = find_column_no(columns, left, right)
      # If we're back at the beginning of a row this is a new row
      y += 1 if new_x == 0 && x > 0
      x = new_x
      [x, y, t.inner_text]
    end
  end

  # Can pass in the optional columns if the automated finding of columns
  # doesn't work properly for some reason
  def self.extract_table_from_pdf_text(texts, columns = nil)
    texts = extract_indices_from_pdf_text(texts, columns)
    # Find the the range of indices
    max_x, max_y = texts.first
    texts.each do |t|
      max_x = [max_x, t[0]].max
      max_y = [max_y, t[1]].max
    end
    # Create an empty 2d array
    result = Array.new(max_y + 1) { |i| Array.new(max_x + 1) }
    texts.each do |t|
      x, y, text = t
      if result[y][x].nil? 
        result[y][x] = text
      else
        result[y][x] += "\n" + text
      end
    end
    result
  end
end


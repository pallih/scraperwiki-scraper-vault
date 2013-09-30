# SOURCE: https://github.com/paulfitz/coopy/tree/master/src/ruby
# EXAMPLE USE:
# see https://scraperwiki.com/views/paulfitzplaygroundview/
# show difference between paulfitzplayground.broken_bridge and paulfitzplayground.bridge
#   ScraperWiki.attach("paulfitzplayground")
#   sql = ScraperwikiSqlWrapper.new(ScraperWiki)
#   sql.set_primary_key(["bridge"])
#   cmp = SqlCompare.new(sql,"paulfitzplayground.broken_bridge","paulfitzplayground.bridge")
#   render = DiffRenderHtml.new
#   cmp.set_output(render)
#   cmp.apply
#   print render.to_string




# diff_columns.rb

class DiffColumns
  attr_accessor :change_row
  attr_accessor :title_row

  # general
  attr_accessor :column_name   # *after* any column changes
  attr_accessor :column_offset # *after* any column changes
  attr_accessor :column_by_name
  attr_accessor :column_by_offset

  def update(prefix=1)
    return if @title_row.nil?
    @column_name = {}
    @column_offset = {}
    @column_by_name = {}
    @column_by_offset = []
    offset = -prefix
    @title_row.each_with_index do |title,idx|
      @column_name[idx] = title
      if offset>=0
        # assuming no column changes for the moment
        @column_offset[idx] = offset
        @column_by_name[title] = {
          :title => title,
          :in_offset => offset,
          :diff_offset => idx
        }
        @column_by_offset << @column_by_name[title]
      end
      offset = offset+1
    end
  end
end


# row_change.rb

class RowChange
  attr_accessor :row_mode
  attr_accessor :cells
  attr_accessor :columns
  attr_accessor :key

  def initialize(row_mode,cells)
    @row_mode = row_mode
    @cells = cells
    @key = nil
  end

  def active_columns
    return [] if @columns.nil?
    @columns.column_by_offset
  end

  def value_at(column)
    @cells[column[:diff_offset]][:value]
  end

  def new_value_at(column)
    @cells[column[:diff_offset]][:new_value]
  end

  def has_new_value_at(column)
    @cells[column[:diff_offset]].key? :new_value
  end
end


# sql_wrapper.rb

class SqlWrapper
  def insert(tbl,cols,vals)
  end

  def delete(tbl,cols,vals)
  end

  def update(tbl,set_cols,set_vals,cond_cols,cond_vals)
  end

  def column_names(tbl)
    []
  end

  def primary_key(tbl)
    []
  end

  def except_primary_key(tbl)
    column_names(tbl)-primary_key(tbl)
  end

  def fetch(sql)
    []
  end

  def quote_column(c)
    c.to_s
  end

  def quote_table(t)
    t.to_s
  end
end


# sql_compare.rb


class SqlCompare
  def initialize(db1,db2)
    @db1 = db
    @db2 = db2
    @table1 = nil
    @table2 = nil
    @single_db = false
    raise "not implemented yet"
  end

  def initialize(db,table1,table2)
    @db1 = db
    @db2 = db.clone
    @table1 = table1
    @table2 = table2
    @single_db = true
  end

  def set_output(patch)
    @patch = patch
  end

  def apply
    apply_single
  end

  # We are not implementing full comparison, just an adequate subset
  # for easy cases (a table with a trustworthy primary key, and constant
  # columns).  Make sure we are not trying to do something we're not ready 
  # for.
  def validate_schema
    all_cols1 = @db1.column_names(@table1)
    all_cols2 = @db2.column_names(@table2)
    if all_cols1 != all_cols2
      raise "Columns do not match, please use full coopy toolbox"
    end

    key_cols1 = @db1.primary_key(@table1)
    key_cols2 = @db2.primary_key(@table2)
    if key_cols1 != key_cols2
      raise "Primary keys do not match, please use full coopy toolbox"
    end
  end

  def keyify(lst)
    lst.map{|x| x.to_s}.join("___")
  end

  # When working within a single database, we can delegate more work to SQL.
  # So we specialize this case.
  def apply_single
    validate_schema

    # Prepare some lists of columns.
    key_cols = @db1.primary_key(@table1)
    data_cols = @db1.except_primary_key(@table1)
    all_cols = @db1.column_names(@table1)

    # Let our public know we are beginning.
    @patch.begin_diff

    # Advertise column names.
    @rc_columns = DiffColumns.new
    @rc_columns.title_row = all_cols
    @rc_columns.update(0)
    cells = all_cols.map{|v| { :txt => v, :value => v, :cell_mode => "" }}
    rc = RowChange.new("@@",cells)
    @patch.apply_row(rc)

    # If requested, we will be providing context rows around changed rows.
    # This is not a natural thing to do with SQL, so we do it only on request.
    # When requested, we need to buffer row changes.
    @pending_rcs = []

    # Prepare some useful SQL fragments to assemble later.
    sql_table1 = @db1.quote_table(@table1)
    sql_table2 = @db1.quote_table(@table2)
    sql_key_cols = key_cols.map{|c| @db1.quote_column(c)}.join(",")
    sql_all_cols = all_cols.map{|c| @db1.quote_column(c)}.join(",")
    sql_key_match = key_cols.map{|c| @db1.quote_column(c)}.map{|c| "#{sql_table1}.#{c} IS #{sql_table2}.#{c}"}.join(" AND ")
    sql_data_mismatch = data_cols.map{|c| @db1.quote_column(c)}.map{|c| "#{sql_table1}.#{c} IS NOT #{sql_table2}.#{c}"}.join(" OR ")

    # For one query we will need to interleave columns from two tables.  For
    # portability we need to give these columns distinct names.
    weave = all_cols.map{|c| [[sql_table1,@db1.quote_column(c)],
                              [sql_table2,@db2.quote_column(c)]]}.flatten(1)
    dbl_cols = weave.map{|c| "#{c[0]}.#{c[1]}"}
    sql_dbl_cols = weave.map{|c| "#{c[0]}.#{c[1]} AS #{c[0].gsub(/[^a-zA-Z0-9]/,'_')}_#{c[1].gsub(/[^a-zA-Z0-9]/,'_')}"}.join(",")

    # Prepare a map of primary key offsets.
    keys_in_all_cols = key_cols.each.map{|c| all_cols.index(c)}
    keys_in_dbl_cols = keys_in_all_cols.map{|x| 2*x}

    # Find rows in table2 that are not in table1.
    sql = "SELECT #{sql_all_cols} FROM #{sql_table2} WHERE NOT EXISTS (SELECT 1 FROM #{sql_table1} WHERE #{sql_key_match})"
    apply_inserts(sql,all_cols,keys_in_all_cols)

    # Find rows in table1 and table2 that differ while having the same primary
    # key.
    sql = "SELECT #{sql_dbl_cols} FROM #{sql_table1} INNER JOIN #{sql_table2} ON #{sql_key_match} WHERE #{sql_data_mismatch}"
    apply_updates(sql,dbl_cols,keys_in_dbl_cols)

    # Find rows that are in table1 but not table2
    sql = "SELECT #{sql_all_cols} FROM #{sql_table1} WHERE NOT EXISTS (SELECT 1 FROM #{sql_table2} WHERE #{sql_key_match})"
    apply_deletes(sql,all_cols,keys_in_all_cols)

    # If we are supposed to provide context, we need to deal with row order.
    if @patch.want_context
      sql = "SELECT #{sql_all_cols}, 0 AS __coopy_tag__ FROM #{sql_table1} UNION SELECT #{sql_all_cols}, 1 AS __coopy_tag__ FROM #{sql_table2} ORDER BY #{sql_key_cols}, __coopy_tag__"
      apply_with_context(sql,all_cols,keys_in_all_cols)
    end

    # Done!
    @patch.end_diff
  end


  def apply_inserts(sql,all_cols,keys_in_all_cols)
    @db1.fetch(sql,all_cols) do |row|
      cells = row.map{|v| { :txt => v, :value => v, :cell_mode => "" }}
      rc = RowChange.new("+++",cells)
      apply_rc(rc,row,keys_in_all_cols)
    end
  end


  def apply_updates(sql,dbl_cols,keys_in_dbl_cols)
    @db1.fetch(sql,dbl_cols) do |row|
      pairs = row.enum_for(:each_slice,2).to_a
      cells = pairs.map do |v| 
        if v[0]==v[1] 
          { :txt => v[0], :value => v[0], :cell_mode => "" }
        else
          { :txt => v[0], :value => v[0], :new_value => v[1], :cell_mode => "->" }
        end
      end
      rc = RowChange.new("->",cells)
      apply_rc(rc,row,keys_in_dbl_cols)
    end
  end


  def apply_deletes(sql,all_cols,keys_in_all_cols)
    @db1.fetch(sql,all_cols) do |row|
      cells = row.map{|v| { :txt => v, :value => v, :cell_mode => "" }}
      rc = RowChange.new("---",cells)
      apply_rc(rc,row,keys_in_all_cols)
    end
  end

  def apply_rc(rc,row,keys_in_cols)
    rc.columns = @rc_columns
    if @patch.want_context
      rc.key = keyify(row.values_at(*keys_in_cols))
      @pending_rcs << rc
    else
      @patch.apply_row(rc)
    end
  end

  def emit_skip(row)
    cells = row.map{|v| { :txt => "...", :value => "...", :cell_mode => "" }}
    rc = RowChange.new("...",cells)
    rc.columns = @rc_columns
    @patch.apply_row(rc)
  end

  # Do the context dance.
  def apply_with_context(sql,all_cols,keys_in_all_cols)
    hits = {}
    @pending_rcs.each do |rc|
      hits[rc.key] = rc
    end 
    hist = []
    n = 2
    pending = 0
    skipped = false
    noted = false
    last_row = nil
    @db1.fetch(sql,all_cols + ["__coopy_tag__"]) do |row|
      tag = row.pop.to_i
      k = keyify(row.values_at(*keys_in_all_cols))
      if hits[k]
        emit_skip(row) if skipped
        hist.each do |row0|
          cells = row0.map{|v| { :txt => v, :value => v, :cell_mode => "" }}
          rc = RowChange.new("",cells)
          rc.columns = @rc_columns
          @patch.apply_row(rc)
        end
        hist.clear
        pending = n
        @patch.apply_row(hits[k])
        hits.delete(k)
        skipped = false
        noted =  true
      elsif tag == 1
        # ignore redundant row
      elsif pending>0
        emit_skip(row) if skipped
        cells = row.map{|v| { :txt => v, :value => v, :cell_mode => "" }}
        rc = RowChange.new("",cells)
        rc.columns = @rc_columns
        @patch.apply_row(rc)
        pending = pending-1
        skipped = false
      else
        hist << row
        if hist.length>n
          skipped = true
          last_row = row
          hist.shift
        end
      end
    end
    emit_skip(last_row) if skipped and noted
  end
end



# diff_output.rb


class DiffOutput
  def begin_diff
  end

  def end_diff
  end

  def apply_row(rc)
  end

  def to_string
    ""
  end

  def want_context
    true
  end
end


# diff_output_table.rb


class DiffOutputTable < DiffOutput
  def begin_table
  end

  def end_table
  end

  def begin_row(mode)
  end

  def insert_cell(txt,mode,separator)
  end

  def end_row
  end

  def quote(x)
    return "" if x.nil?
    x
  end

  def apply_row(rc)
    self.begin_row(rc.row_mode)
    self.insert_cell(rc.row_mode,
                     (rc.row_mode=="->") ? rc.row_mode : "",
                     (rc.row_mode=="->") ? rc.row_mode : "")
    rc.cells.each do |cell|
      if cell.key? :new_value
        self.insert_cell(quote(cell[:value]) + "->" + quote(cell[:new_value]),
                         cell[:cell_mode],
                         "->")
      else
        self.insert_cell(cell[:txt],cell[:cell_mode],cell[:separator])
      end
    end
    self.end_row
  end

  def begin_diff
    self.begin_table
  end

  def end_diff
    self.end_table
  end
end



# diff_render_html.rb


class DiffRenderHtml < DiffOutputTable
  def initialize
    @text_to_insert = []
  end

  def insert(str)
    @text_to_insert << str
  end

  def begin_table
    self.insert "<table class='csv_sheet'>\n"
  end

  def begin_row(mode)
    @td_open = '<td';
    @td_close = '</td>';
    @row_color = "";
    @open = false;
    case mode
    when "@@"
      @td_open = "<th"
      @td_close = "</th>"
    when "!"
      @row_color = "#aaaaaa"
    when "+++"
      @row_color = "#7fff7f";
    when "---"
      @row_color = "#ff7f7f";
    else
      @open = true
    end
    tr = "<tr>";
    row_decorate = ""
    if @row_color!=""
      row_decorate = " bgcolor=\"" + @row_color + "\" style=\"background-color: " + @row_color + ";\""
      tr = "<tr" + row_decorate + ">"
    end
    self.insert(tr)
  end

  def insert_cell(txt,mode,separator)
    cell_decorate = ""
    case mode
    when "+++"
      cell_decorate = " bgcolor=\"#7fff7f\" style=\"background-color: #7fff7f;\""
    when "---"
      cell_decorate = " bgcolor=\"#ff7f7f\" style=\"background-color: #ff7f7f;\""
    when "->"
      cell_decorate = " bgcolor=\"#7f7fff\" style=\"background-color: #7f7fff;\""
    end
    self.insert @td_open+cell_decorate+">"
    self.insert txt
    self.insert @td_close
  end

  def end_row
    self.insert "</tr>\n"
  end

  def end_table
    self.insert "</table>\n"
  end

  def html
    @text_to_insert.join ''
  end

  def to_string
    html
  end
end



# diff_output_action.rb


class DiffOutputAction < DiffOutput
  def row_insert(rc)
  end

  def row_delete(rc)
  end

  def row_update(rc)
  end

  def row_skip(rc)
  end

  def row_context(rc)
  end

  def apply_row(rc)
    mode = rc.row_mode
    case mode
    when "+++"
      row_insert(rc)
    when "---"
      row_delete(rc)
    when "->"
      row_update(rc)
    when "..."
      row_skip(rc)
    when ""
      row_context(rc)
    end
  end
end


# diff_output_group.rb


class DiffOutputGroup
  def initialize(*sinks)
    @sinks = sinks
  end

  def <<(x)
    @sinks = [] if @sinks.nil?
    @sinks << x
  end

  def begin_diff
    @sinks.each { |s| s.begin_diff }
  end

  def end_diff
    @sinks.each { |s| s.end_diff }
  end

  def apply_row(rc)
    @sinks.each { |s| s.apply_row(rc) }
  end

  def to_string
    @sinks.each do |s|
      result = s.to_string
      return result if result!=""
    end
    ""
  end

  def want_context
    return @want_context0 unless @want_context0.nil?
    @want_context0 = false
    @want_context0 = @sinks.each { |s| @want_context0 ||= s.want_context }
    @want_context0
  end
end


# diff_apply_sql.rb


# for now, assume no schema changes, and a single table
class DiffApplySql < DiffOutputAction
  def initialize(db, name = nil)
    @name = name
    @db = db
  end

  def row_insert(rc)
    cols = rc.active_columns
    @db.insert(@name,
               cols.map{|c| c[:title]},
               cols.map{|c| rc.value_at(c)})
  end

  def row_delete(rc)
    cols = rc.active_columns
    @db.delete(@name,
               cols.map{|c| c[:title]},
               cols.map{|c| rc.value_at(c)})
  end

  def row_update(rc)
    cols = rc.active_columns
    touched_cols = cols.select{|c| rc.has_new_value_at(c)}
    @db.update(@name,
               touched_cols.map{|c| c[:title]},
               touched_cols.map{|c| rc.new_value_at(c)},
               cols.map{|c| c[:title]},
               cols.map{|c| rc.value_at(c)})
  end
end



# sqlite_sql_wrapper.rb


class SqliteSqlWrapper < SqlWrapper
  def initialize(db)
    @db = db
    @t = nil
    @qt = nil
    @pk = nil
    @info = {}
  end

  def set_primary_key(lst)
    @pk = lst
  end

  def sqlite_execute(template,vals)
    return @db.execute(template,*vals)
  end

  def get_table_names
    return sqlite_execute("SELECT name FROM sqlite_master WHERE type='table'",[]).flatten
  end

  def complete_table(tbl)
    @t = tbl unless tbl.nil?
    @t
  end

  def quote_with_dots(x)
    return x if x.match(/^[a-zA-Z0-9_]+$/)
    x.split('.').map{|p| "`#{p}`"}.join('.')
  end

  def quote_table(tbl)
    complete_table(tbl)
    return @t if @t.match(/^[a-zA-Z0-9_]+$/)
    quote_with_dots(@t)
  end

  def quote_column(col)
    return col if col.match(/^[a-zA-Z0-9_]+$/)
    quote_with_dots(col)
  end

  def insert(tbl,cols,vals)
    tbl = quote_table(tbl)
    template = cols.map{|x| '?'}.join(",")
    template = "INSERT INTO #{tbl} VALUES(#{template})"
    sqlite_execute(template,vals)
  end

  def delete(tbl,cols,vals)
    tbl = quote_table(tbl)
    template = cols.map{|c| quote_column(c) + ' IS ?'}.join(" AND ")
    template = "DELETE FROM #{tbl} WHERE #{template}"
    sqlite_execute(template,vals)
  end
  
  def update(tbl,set_cols,set_vals,cond_cols,cond_vals)
    tbl = quote_table(tbl)
    conds = cond_cols.map{|c| quote_column(c) + ' IS ?'}.join(" AND ")
    sets = set_cols.map{|c| quote_column(c) + ' = ?'}.join(", ")
    template = "UPDATE #{tbl} SET #{sets} WHERE #{conds}"
    v = set_vals + cond_vals
    sqlite_execute(template,v)
  end

  def transaction(&block)
    # not yet mapped, not yet used
    block.call
  end

  def pragma(tbl,info)
    if tbl.include? '.'
      dbname, tbname, *ignore = tbl.split('.')
      dbname = quote_with_dots(dbname)
      tbname = quote_with_dots(tbname)
      query = "PRAGMA #{dbname}.#{info}(#{tbname})"
    else
      tbl = quote_with_dots(tbl)
      query = "PRAGMA #{info}(#{tbl})"
    end
    result = sqlite_execute(query,[])
    result
  end

  def part(row,n,name)
    row[n]
  end

  def columns(tbl)
    tbl = complete_table(tbl)
    @info[tbl] = pragma(tbl,"table_info") unless @info.has_key? tbl
    @info[tbl]
  end

  def column_names(tbl)
    columns(tbl).map{|c| part(c,1,"name")}
  end

  def fetch(sql,names)
    sqlite_execute(sql,[]).each do |row|
      yield row
    end
  end

  def primary_key(tbl)
    return @pk unless @pk.nil?
    cols = columns(tbl)
    cols = cols.select{|c| part(c,5,"pk").to_s=="1"}.map{|c| part(c,1,"name")}
    if cols.length == 0
      cols = pk_from_unique_index(tbl)
    end
    @pk = cols if cols.length>0
    cols
  end

  def pk_from_unique_index(tbl)
    pragma(tbl,"index_list").each do |row|
      if part(row,2,"unique").to_s == "1"
        idx = part(row,1,"name")
        return pragma(idx,"index_info").map{|r| part(r,2,"name")}
      end
    end
    nil
  end

  # copy the structure of an attached table, along with any indexes
  def copy_table_structure(rdb,tbl)
    template = "SELECT sql, type from X.sqlite_master WHERE tbl_name = ? ORDER BY type DESC"
    lsql = template.gsub('X',"main")
    rsql = template.gsub('X',quote_with_dots(rdb))
    args = [quote_with_dots(tbl)]
    lschema = sqlite_execute(lsql,args)
    rschema = sqlite_execute(rsql,args)
    if lschema.length>0
      return false
    end
    rschema.each{ |row| sqlite_execute(row[0],[]) }
    true
  end
end


# scraperwiki_sql_wrapper.rb


# Tweak sqlite wrapper slightly to match ScraperWiki's API
class ScraperwikiSqlWrapper < SqliteSqlWrapper
  def sqlite_execute(template,vals)
    @db.sqliteexecute(template,vals)["data"]
  end
end


# scraperwiki_utils.rb

def link_tables(watch_scraper,watch_tables)
  sql = ScraperwikiSqlWrapper.new(ScraperWiki)
  watch_tables.each { |tbl| sql.copy_table_structure(watch_scraper,tbl) }
end

class CoopyResult
  attr_accessor :html
end

def sync_table(watch_scraper,tbl,keys)
  sql = ScraperwikiSqlWrapper.new(ScraperWiki)
  sql.set_primary_key(keys) unless keys.nil? 
  cmp = SqlCompare.new(sql,"main.#{tbl}","#{watch_scraper}.#{tbl}")
  sinks = DiffOutputGroup.new
  render = DiffRenderHtml.new
  sinks << render
  sinks << DiffApplySql.new(sql,"main.#{tbl}")
  cmp.set_output(sinks)
  cmp.apply
  result = CoopyResult.new
  result.html = render.to_string
  result
end# SOURCE: https://github.com/paulfitz/coopy/tree/master/src/ruby
# EXAMPLE USE:
# see https://scraperwiki.com/views/paulfitzplaygroundview/
# show difference between paulfitzplayground.broken_bridge and paulfitzplayground.bridge
#   ScraperWiki.attach("paulfitzplayground")
#   sql = ScraperwikiSqlWrapper.new(ScraperWiki)
#   sql.set_primary_key(["bridge"])
#   cmp = SqlCompare.new(sql,"paulfitzplayground.broken_bridge","paulfitzplayground.bridge")
#   render = DiffRenderHtml.new
#   cmp.set_output(render)
#   cmp.apply
#   print render.to_string




# diff_columns.rb

class DiffColumns
  attr_accessor :change_row
  attr_accessor :title_row

  # general
  attr_accessor :column_name   # *after* any column changes
  attr_accessor :column_offset # *after* any column changes
  attr_accessor :column_by_name
  attr_accessor :column_by_offset

  def update(prefix=1)
    return if @title_row.nil?
    @column_name = {}
    @column_offset = {}
    @column_by_name = {}
    @column_by_offset = []
    offset = -prefix
    @title_row.each_with_index do |title,idx|
      @column_name[idx] = title
      if offset>=0
        # assuming no column changes for the moment
        @column_offset[idx] = offset
        @column_by_name[title] = {
          :title => title,
          :in_offset => offset,
          :diff_offset => idx
        }
        @column_by_offset << @column_by_name[title]
      end
      offset = offset+1
    end
  end
end


# row_change.rb

class RowChange
  attr_accessor :row_mode
  attr_accessor :cells
  attr_accessor :columns
  attr_accessor :key

  def initialize(row_mode,cells)
    @row_mode = row_mode
    @cells = cells
    @key = nil
  end

  def active_columns
    return [] if @columns.nil?
    @columns.column_by_offset
  end

  def value_at(column)
    @cells[column[:diff_offset]][:value]
  end

  def new_value_at(column)
    @cells[column[:diff_offset]][:new_value]
  end

  def has_new_value_at(column)
    @cells[column[:diff_offset]].key? :new_value
  end
end


# sql_wrapper.rb

class SqlWrapper
  def insert(tbl,cols,vals)
  end

  def delete(tbl,cols,vals)
  end

  def update(tbl,set_cols,set_vals,cond_cols,cond_vals)
  end

  def column_names(tbl)
    []
  end

  def primary_key(tbl)
    []
  end

  def except_primary_key(tbl)
    column_names(tbl)-primary_key(tbl)
  end

  def fetch(sql)
    []
  end

  def quote_column(c)
    c.to_s
  end

  def quote_table(t)
    t.to_s
  end
end


# sql_compare.rb


class SqlCompare
  def initialize(db1,db2)
    @db1 = db
    @db2 = db2
    @table1 = nil
    @table2 = nil
    @single_db = false
    raise "not implemented yet"
  end

  def initialize(db,table1,table2)
    @db1 = db
    @db2 = db.clone
    @table1 = table1
    @table2 = table2
    @single_db = true
  end

  def set_output(patch)
    @patch = patch
  end

  def apply
    apply_single
  end

  # We are not implementing full comparison, just an adequate subset
  # for easy cases (a table with a trustworthy primary key, and constant
  # columns).  Make sure we are not trying to do something we're not ready 
  # for.
  def validate_schema
    all_cols1 = @db1.column_names(@table1)
    all_cols2 = @db2.column_names(@table2)
    if all_cols1 != all_cols2
      raise "Columns do not match, please use full coopy toolbox"
    end

    key_cols1 = @db1.primary_key(@table1)
    key_cols2 = @db2.primary_key(@table2)
    if key_cols1 != key_cols2
      raise "Primary keys do not match, please use full coopy toolbox"
    end
  end

  def keyify(lst)
    lst.map{|x| x.to_s}.join("___")
  end

  # When working within a single database, we can delegate more work to SQL.
  # So we specialize this case.
  def apply_single
    validate_schema

    # Prepare some lists of columns.
    key_cols = @db1.primary_key(@table1)
    data_cols = @db1.except_primary_key(@table1)
    all_cols = @db1.column_names(@table1)

    # Let our public know we are beginning.
    @patch.begin_diff

    # Advertise column names.
    @rc_columns = DiffColumns.new
    @rc_columns.title_row = all_cols
    @rc_columns.update(0)
    cells = all_cols.map{|v| { :txt => v, :value => v, :cell_mode => "" }}
    rc = RowChange.new("@@",cells)
    @patch.apply_row(rc)

    # If requested, we will be providing context rows around changed rows.
    # This is not a natural thing to do with SQL, so we do it only on request.
    # When requested, we need to buffer row changes.
    @pending_rcs = []

    # Prepare some useful SQL fragments to assemble later.
    sql_table1 = @db1.quote_table(@table1)
    sql_table2 = @db1.quote_table(@table2)
    sql_key_cols = key_cols.map{|c| @db1.quote_column(c)}.join(",")
    sql_all_cols = all_cols.map{|c| @db1.quote_column(c)}.join(",")
    sql_key_match = key_cols.map{|c| @db1.quote_column(c)}.map{|c| "#{sql_table1}.#{c} IS #{sql_table2}.#{c}"}.join(" AND ")
    sql_data_mismatch = data_cols.map{|c| @db1.quote_column(c)}.map{|c| "#{sql_table1}.#{c} IS NOT #{sql_table2}.#{c}"}.join(" OR ")

    # For one query we will need to interleave columns from two tables.  For
    # portability we need to give these columns distinct names.
    weave = all_cols.map{|c| [[sql_table1,@db1.quote_column(c)],
                              [sql_table2,@db2.quote_column(c)]]}.flatten(1)
    dbl_cols = weave.map{|c| "#{c[0]}.#{c[1]}"}
    sql_dbl_cols = weave.map{|c| "#{c[0]}.#{c[1]} AS #{c[0].gsub(/[^a-zA-Z0-9]/,'_')}_#{c[1].gsub(/[^a-zA-Z0-9]/,'_')}"}.join(",")

    # Prepare a map of primary key offsets.
    keys_in_all_cols = key_cols.each.map{|c| all_cols.index(c)}
    keys_in_dbl_cols = keys_in_all_cols.map{|x| 2*x}

    # Find rows in table2 that are not in table1.
    sql = "SELECT #{sql_all_cols} FROM #{sql_table2} WHERE NOT EXISTS (SELECT 1 FROM #{sql_table1} WHERE #{sql_key_match})"
    apply_inserts(sql,all_cols,keys_in_all_cols)

    # Find rows in table1 and table2 that differ while having the same primary
    # key.
    sql = "SELECT #{sql_dbl_cols} FROM #{sql_table1} INNER JOIN #{sql_table2} ON #{sql_key_match} WHERE #{sql_data_mismatch}"
    apply_updates(sql,dbl_cols,keys_in_dbl_cols)

    # Find rows that are in table1 but not table2
    sql = "SELECT #{sql_all_cols} FROM #{sql_table1} WHERE NOT EXISTS (SELECT 1 FROM #{sql_table2} WHERE #{sql_key_match})"
    apply_deletes(sql,all_cols,keys_in_all_cols)

    # If we are supposed to provide context, we need to deal with row order.
    if @patch.want_context
      sql = "SELECT #{sql_all_cols}, 0 AS __coopy_tag__ FROM #{sql_table1} UNION SELECT #{sql_all_cols}, 1 AS __coopy_tag__ FROM #{sql_table2} ORDER BY #{sql_key_cols}, __coopy_tag__"
      apply_with_context(sql,all_cols,keys_in_all_cols)
    end

    # Done!
    @patch.end_diff
  end


  def apply_inserts(sql,all_cols,keys_in_all_cols)
    @db1.fetch(sql,all_cols) do |row|
      cells = row.map{|v| { :txt => v, :value => v, :cell_mode => "" }}
      rc = RowChange.new("+++",cells)
      apply_rc(rc,row,keys_in_all_cols)
    end
  end


  def apply_updates(sql,dbl_cols,keys_in_dbl_cols)
    @db1.fetch(sql,dbl_cols) do |row|
      pairs = row.enum_for(:each_slice,2).to_a
      cells = pairs.map do |v| 
        if v[0]==v[1] 
          { :txt => v[0], :value => v[0], :cell_mode => "" }
        else
          { :txt => v[0], :value => v[0], :new_value => v[1], :cell_mode => "->" }
        end
      end
      rc = RowChange.new("->",cells)
      apply_rc(rc,row,keys_in_dbl_cols)
    end
  end


  def apply_deletes(sql,all_cols,keys_in_all_cols)
    @db1.fetch(sql,all_cols) do |row|
      cells = row.map{|v| { :txt => v, :value => v, :cell_mode => "" }}
      rc = RowChange.new("---",cells)
      apply_rc(rc,row,keys_in_all_cols)
    end
  end

  def apply_rc(rc,row,keys_in_cols)
    rc.columns = @rc_columns
    if @patch.want_context
      rc.key = keyify(row.values_at(*keys_in_cols))
      @pending_rcs << rc
    else
      @patch.apply_row(rc)
    end
  end

  def emit_skip(row)
    cells = row.map{|v| { :txt => "...", :value => "...", :cell_mode => "" }}
    rc = RowChange.new("...",cells)
    rc.columns = @rc_columns
    @patch.apply_row(rc)
  end

  # Do the context dance.
  def apply_with_context(sql,all_cols,keys_in_all_cols)
    hits = {}
    @pending_rcs.each do |rc|
      hits[rc.key] = rc
    end 
    hist = []
    n = 2
    pending = 0
    skipped = false
    noted = false
    last_row = nil
    @db1.fetch(sql,all_cols + ["__coopy_tag__"]) do |row|
      tag = row.pop.to_i
      k = keyify(row.values_at(*keys_in_all_cols))
      if hits[k]
        emit_skip(row) if skipped
        hist.each do |row0|
          cells = row0.map{|v| { :txt => v, :value => v, :cell_mode => "" }}
          rc = RowChange.new("",cells)
          rc.columns = @rc_columns
          @patch.apply_row(rc)
        end
        hist.clear
        pending = n
        @patch.apply_row(hits[k])
        hits.delete(k)
        skipped = false
        noted =  true
      elsif tag == 1
        # ignore redundant row
      elsif pending>0
        emit_skip(row) if skipped
        cells = row.map{|v| { :txt => v, :value => v, :cell_mode => "" }}
        rc = RowChange.new("",cells)
        rc.columns = @rc_columns
        @patch.apply_row(rc)
        pending = pending-1
        skipped = false
      else
        hist << row
        if hist.length>n
          skipped = true
          last_row = row
          hist.shift
        end
      end
    end
    emit_skip(last_row) if skipped and noted
  end
end



# diff_output.rb


class DiffOutput
  def begin_diff
  end

  def end_diff
  end

  def apply_row(rc)
  end

  def to_string
    ""
  end

  def want_context
    true
  end
end


# diff_output_table.rb


class DiffOutputTable < DiffOutput
  def begin_table
  end

  def end_table
  end

  def begin_row(mode)
  end

  def insert_cell(txt,mode,separator)
  end

  def end_row
  end

  def quote(x)
    return "" if x.nil?
    x
  end

  def apply_row(rc)
    self.begin_row(rc.row_mode)
    self.insert_cell(rc.row_mode,
                     (rc.row_mode=="->") ? rc.row_mode : "",
                     (rc.row_mode=="->") ? rc.row_mode : "")
    rc.cells.each do |cell|
      if cell.key? :new_value
        self.insert_cell(quote(cell[:value]) + "->" + quote(cell[:new_value]),
                         cell[:cell_mode],
                         "->")
      else
        self.insert_cell(cell[:txt],cell[:cell_mode],cell[:separator])
      end
    end
    self.end_row
  end

  def begin_diff
    self.begin_table
  end

  def end_diff
    self.end_table
  end
end



# diff_render_html.rb


class DiffRenderHtml < DiffOutputTable
  def initialize
    @text_to_insert = []
  end

  def insert(str)
    @text_to_insert << str
  end

  def begin_table
    self.insert "<table class='csv_sheet'>\n"
  end

  def begin_row(mode)
    @td_open = '<td';
    @td_close = '</td>';
    @row_color = "";
    @open = false;
    case mode
    when "@@"
      @td_open = "<th"
      @td_close = "</th>"
    when "!"
      @row_color = "#aaaaaa"
    when "+++"
      @row_color = "#7fff7f";
    when "---"
      @row_color = "#ff7f7f";
    else
      @open = true
    end
    tr = "<tr>";
    row_decorate = ""
    if @row_color!=""
      row_decorate = " bgcolor=\"" + @row_color + "\" style=\"background-color: " + @row_color + ";\""
      tr = "<tr" + row_decorate + ">"
    end
    self.insert(tr)
  end

  def insert_cell(txt,mode,separator)
    cell_decorate = ""
    case mode
    when "+++"
      cell_decorate = " bgcolor=\"#7fff7f\" style=\"background-color: #7fff7f;\""
    when "---"
      cell_decorate = " bgcolor=\"#ff7f7f\" style=\"background-color: #ff7f7f;\""
    when "->"
      cell_decorate = " bgcolor=\"#7f7fff\" style=\"background-color: #7f7fff;\""
    end
    self.insert @td_open+cell_decorate+">"
    self.insert txt
    self.insert @td_close
  end

  def end_row
    self.insert "</tr>\n"
  end

  def end_table
    self.insert "</table>\n"
  end

  def html
    @text_to_insert.join ''
  end

  def to_string
    html
  end
end



# diff_output_action.rb


class DiffOutputAction < DiffOutput
  def row_insert(rc)
  end

  def row_delete(rc)
  end

  def row_update(rc)
  end

  def row_skip(rc)
  end

  def row_context(rc)
  end

  def apply_row(rc)
    mode = rc.row_mode
    case mode
    when "+++"
      row_insert(rc)
    when "---"
      row_delete(rc)
    when "->"
      row_update(rc)
    when "..."
      row_skip(rc)
    when ""
      row_context(rc)
    end
  end
end


# diff_output_group.rb


class DiffOutputGroup
  def initialize(*sinks)
    @sinks = sinks
  end

  def <<(x)
    @sinks = [] if @sinks.nil?
    @sinks << x
  end

  def begin_diff
    @sinks.each { |s| s.begin_diff }
  end

  def end_diff
    @sinks.each { |s| s.end_diff }
  end

  def apply_row(rc)
    @sinks.each { |s| s.apply_row(rc) }
  end

  def to_string
    @sinks.each do |s|
      result = s.to_string
      return result if result!=""
    end
    ""
  end

  def want_context
    return @want_context0 unless @want_context0.nil?
    @want_context0 = false
    @want_context0 = @sinks.each { |s| @want_context0 ||= s.want_context }
    @want_context0
  end
end


# diff_apply_sql.rb


# for now, assume no schema changes, and a single table
class DiffApplySql < DiffOutputAction
  def initialize(db, name = nil)
    @name = name
    @db = db
  end

  def row_insert(rc)
    cols = rc.active_columns
    @db.insert(@name,
               cols.map{|c| c[:title]},
               cols.map{|c| rc.value_at(c)})
  end

  def row_delete(rc)
    cols = rc.active_columns
    @db.delete(@name,
               cols.map{|c| c[:title]},
               cols.map{|c| rc.value_at(c)})
  end

  def row_update(rc)
    cols = rc.active_columns
    touched_cols = cols.select{|c| rc.has_new_value_at(c)}
    @db.update(@name,
               touched_cols.map{|c| c[:title]},
               touched_cols.map{|c| rc.new_value_at(c)},
               cols.map{|c| c[:title]},
               cols.map{|c| rc.value_at(c)})
  end
end



# sqlite_sql_wrapper.rb


class SqliteSqlWrapper < SqlWrapper
  def initialize(db)
    @db = db
    @t = nil
    @qt = nil
    @pk = nil
    @info = {}
  end

  def set_primary_key(lst)
    @pk = lst
  end

  def sqlite_execute(template,vals)
    return @db.execute(template,*vals)
  end

  def get_table_names
    return sqlite_execute("SELECT name FROM sqlite_master WHERE type='table'",[]).flatten
  end

  def complete_table(tbl)
    @t = tbl unless tbl.nil?
    @t
  end

  def quote_with_dots(x)
    return x if x.match(/^[a-zA-Z0-9_]+$/)
    x.split('.').map{|p| "`#{p}`"}.join('.')
  end

  def quote_table(tbl)
    complete_table(tbl)
    return @t if @t.match(/^[a-zA-Z0-9_]+$/)
    quote_with_dots(@t)
  end

  def quote_column(col)
    return col if col.match(/^[a-zA-Z0-9_]+$/)
    quote_with_dots(col)
  end

  def insert(tbl,cols,vals)
    tbl = quote_table(tbl)
    template = cols.map{|x| '?'}.join(",")
    template = "INSERT INTO #{tbl} VALUES(#{template})"
    sqlite_execute(template,vals)
  end

  def delete(tbl,cols,vals)
    tbl = quote_table(tbl)
    template = cols.map{|c| quote_column(c) + ' IS ?'}.join(" AND ")
    template = "DELETE FROM #{tbl} WHERE #{template}"
    sqlite_execute(template,vals)
  end
  
  def update(tbl,set_cols,set_vals,cond_cols,cond_vals)
    tbl = quote_table(tbl)
    conds = cond_cols.map{|c| quote_column(c) + ' IS ?'}.join(" AND ")
    sets = set_cols.map{|c| quote_column(c) + ' = ?'}.join(", ")
    template = "UPDATE #{tbl} SET #{sets} WHERE #{conds}"
    v = set_vals + cond_vals
    sqlite_execute(template,v)
  end

  def transaction(&block)
    # not yet mapped, not yet used
    block.call
  end

  def pragma(tbl,info)
    if tbl.include? '.'
      dbname, tbname, *ignore = tbl.split('.')
      dbname = quote_with_dots(dbname)
      tbname = quote_with_dots(tbname)
      query = "PRAGMA #{dbname}.#{info}(#{tbname})"
    else
      tbl = quote_with_dots(tbl)
      query = "PRAGMA #{info}(#{tbl})"
    end
    result = sqlite_execute(query,[])
    result
  end

  def part(row,n,name)
    row[n]
  end

  def columns(tbl)
    tbl = complete_table(tbl)
    @info[tbl] = pragma(tbl,"table_info") unless @info.has_key? tbl
    @info[tbl]
  end

  def column_names(tbl)
    columns(tbl).map{|c| part(c,1,"name")}
  end

  def fetch(sql,names)
    sqlite_execute(sql,[]).each do |row|
      yield row
    end
  end

  def primary_key(tbl)
    return @pk unless @pk.nil?
    cols = columns(tbl)
    cols = cols.select{|c| part(c,5,"pk").to_s=="1"}.map{|c| part(c,1,"name")}
    if cols.length == 0
      cols = pk_from_unique_index(tbl)
    end
    @pk = cols if cols.length>0
    cols
  end

  def pk_from_unique_index(tbl)
    pragma(tbl,"index_list").each do |row|
      if part(row,2,"unique").to_s == "1"
        idx = part(row,1,"name")
        return pragma(idx,"index_info").map{|r| part(r,2,"name")}
      end
    end
    nil
  end

  # copy the structure of an attached table, along with any indexes
  def copy_table_structure(rdb,tbl)
    template = "SELECT sql, type from X.sqlite_master WHERE tbl_name = ? ORDER BY type DESC"
    lsql = template.gsub('X',"main")
    rsql = template.gsub('X',quote_with_dots(rdb))
    args = [quote_with_dots(tbl)]
    lschema = sqlite_execute(lsql,args)
    rschema = sqlite_execute(rsql,args)
    if lschema.length>0
      return false
    end
    rschema.each{ |row| sqlite_execute(row[0],[]) }
    true
  end
end


# scraperwiki_sql_wrapper.rb


# Tweak sqlite wrapper slightly to match ScraperWiki's API
class ScraperwikiSqlWrapper < SqliteSqlWrapper
  def sqlite_execute(template,vals)
    @db.sqliteexecute(template,vals)["data"]
  end
end


# scraperwiki_utils.rb

def link_tables(watch_scraper,watch_tables)
  sql = ScraperwikiSqlWrapper.new(ScraperWiki)
  watch_tables.each { |tbl| sql.copy_table_structure(watch_scraper,tbl) }
end

class CoopyResult
  attr_accessor :html
end

def sync_table(watch_scraper,tbl,keys)
  sql = ScraperwikiSqlWrapper.new(ScraperWiki)
  sql.set_primary_key(keys) unless keys.nil? 
  cmp = SqlCompare.new(sql,"main.#{tbl}","#{watch_scraper}.#{tbl}")
  sinks = DiffOutputGroup.new
  render = DiffRenderHtml.new
  sinks << render
  sinks << DiffApplySql.new(sql,"main.#{tbl}")
  cmp.set_output(sinks)
  cmp.apply
  result = CoopyResult.new
  result.html = render.to_string
  result
end
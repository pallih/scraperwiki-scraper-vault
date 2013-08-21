# encoding: utf-8

require 'nokogiri'

html = ScraperWiki::scrape("http://ponpare.jp/")
html.force_encoding('cp932')
html = html.encode('utf-8')
html.gsub!(/.*<!DOCTYPE/im, '<!DOCTYPE')
p html

def print_dom_tree(elem, depth = 0)
  if elem.is_a?  Nokogiri::XML::Text
    puts "%s%s" % [".." * depth, elem.inner_text]
  else
    puts "%s%s" % [".." * depth, elem.node_name]
    elem.attributes.each do |a|
      puts "%s@%s=%s" %  [".." * (depth + 1), a[1].name, a[1].value]
    end
    elem.children.each do |e|
      print_dom_tree(e, depth + 1)
    end
  end
end

doc = Nokogiri::HTML html
#puts doc
#p doc.css("#areaNav")
doc.search("#areaNav").each do |v|
  print_dom_tree(v)
end

__END__

[:!, :!=, :!~, :%, :/, :<<, :<=>, :==, :===, :=~, :>, :[], :[]=, :__id__, :__send__, :accept, :add_child, :add_namespace, :add_namespace_definition, :add_next_sibling, :add_previous_sibling, :after, :all?, :ancestors, :any?, :at, :at_css, :at_xpath, :attr, :attribute, :attribute_nodes, :attribute_with_ns, :attributes, :before, :blank?, :cdata?, :child, :children, :children=, :chunk, :class, :clone, :collect, :collect_concat, :comment?, :content, :content=, :count, :create_external_subset, :create_internal_subset, :css, :css_path, :cycle, :decorate!, :default_namespace=, :define_singleton_method, :delete, :description, :detect, :display, :document, :drop, :drop_while, :dup, :each, :each_cons, :each_entry, :each_slice, :each_with_index, :each_with_object, :elem?, :element?, :element_children, :elements, :encode_special_chars, :entries, :enum_for, :eql?, :equal?, :extend, :external_subset, :find, :find_all, :find_index, :first, :first_element_child, :flat_map, :fragment, :fragment?, :freeze, :frozen?, :get_attribute, :grep, :group_by, :has_attribute?, :hash, :html?, :include?, :initialize_clone, :initialize_dup, :inject, :inner_html, :inner_html=, :inner_text, :inspect, :instance_eval, :instance_exec, :instance_of?, :instance_variable_defined?, :instance_variable_get, :instance_variable_set, :instance_variables, :internal_subset, :is_a?, :key?, :keys, :kind_of?, :last_element_child, :line, :map, :matches?, :max, :max_by, :member?, :method, :methods, :min, :min_by, :minmax, :minmax_by, :name, :name=, :namespace, :namespace=, :namespace_definitions, :namespace_scopes, :namespaced_key?, :namespaces, :next, :next=, :next_element, :next_sibling, :nil?, :node_name, :node_name=, :node_type, :none?, :object_id, :one?, :parent, :parent=, :parse, :partition, :path, :pointer_id, :pretty_print, :previous, :previous=, :previous_element, :previous_sibling, :private_methods, :protected_methods, :public_method, :public_methods, :public_send, :read_only?, :reduce, :reject, :remove, :remove_attribute, :replace, :require, :respond_to?, :respond_to_missing?, :reverse_each, :search, :select, :send, :serialize, :set_attribute, :singleton_class, :singleton_methods, :slice_before, :sort, :sort_by, :swap, :taint, :tainted?, :take, :take_while, :tap, :text, :text?, :to_a, :to_enum, :to_html, :to_json, :to_s, :to_str, :to_xhtml, :to_xml, :traverse, :trust, :type, :unlink, :untaint, :untrust, :untrusted?, :values, :write_html_to, :write_to, :write_xhtml_to, :write_xml_to, :xml?, :xpath, :zip]


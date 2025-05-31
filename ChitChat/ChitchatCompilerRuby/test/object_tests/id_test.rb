# .. means the enclosing directory, and ../.. means the parent directory
$:.unshift File.expand_path("../../", __FILE__)
require 'test_helper'
require 'interpreter'

class IdTest < Test::Unit::TestCase

  def test_base_class1
    code = <<-CODE
30
    CODE

    test_code = code
    assert_not_nil Interpreter.new.eval(test_code).ruby_value
  end

  def test_base_class2
    code = <<-CODE
x = 300
y = x.id
x.id - y
    CODE

    test_code = code
    assert_equal 0, Interpreter.new.eval(test_code).ruby_value
  end


end
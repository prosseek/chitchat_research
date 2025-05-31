# .. means the enclosing directory, and ../.. means the parent directory
$:.unshift File.expand_path("../../", __FILE__)
require 'test_helper'
require 'interpreter'

class ClassInitializerTest < Test::Unit::TestCase
  # This is the class code that is common to all nodes
  @@code = <<-CODE
class P
  @value = 0

  def initialize(value)
    @value = value
  end

  def hello2(x)
    @value + x
  end
end

p = P.new(123)
  CODE

  def test_base_class1
    code = <<-CODE
p.hello2(-123)
    CODE

    test_code = @@code + code
    assert_equal 0, Interpreter.new.eval(test_code, debug=false).ruby_value
  end

end
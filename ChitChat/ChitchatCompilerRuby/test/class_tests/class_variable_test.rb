# .. means the enclosing directory, and ../.. means the parent directory
$:.unshift File.expand_path("../../", __FILE__)
require 'test_helper'
require 'interpreter'

class ClassVariableTest < Test::Unit::TestCase
  # This is the class code that is common to all nodes
  @@code = <<-CODE
z = -10
def g(x)
  x + 10
end

class P
  @@k = 0
  @x = 10
  @value = 10

  def hello_p(x)
    @@k = @@k + 1
    z + @x + x + g(x) + @value  + @@k
  end
end

p = P.new
  CODE

  def test_base_class1
    code = <<-CODE
p.hello_p(-10)
    CODE

    test_code = @@code + code
    assert_equal 1, Interpreter.new.eval(test_code, debug=false).ruby_value
  end

  def test_base_class2
    code = <<-CODE
q = P.new
p.hello_p(-10)
q.hello_p(-10)
    CODE

    test_code = @@code + code
    assert_equal 2, Interpreter.new.eval(test_code, debug=false).ruby_value
  end

end
# .. means the enclosing directory, and ../.. means the parent directory
$:.unshift File.expand_path("../../", __FILE__)
require 'test_helper'
require 'interpreter'

class ClassInheritanceTest < Test::Unit::TestCase
  # This is the class code that is common to all nodes
  @@code = <<-CODE
class P
  def hello_p(x)
    x - 1
  end
end

class X < P
  def hello_x(x)
    x + 1
  end
end

class A < X
  def hello_a(x)
    hello_x(x) + 2
  end

  def b(x)
    "Hello, it's test to check what is going on"
    x + 10
  end
end
  CODE

  def test_base_class
    code = <<-CODE
p = P.new()
p.hello_p(0)
  CODE

    test_code = @@code + code
    assert_equal -1, Interpreter.new.eval(test_code).ruby_value
  end

  def test_child_class1
    code = <<-CODE
x = X.new()
x.hello_x(0)
    CODE

    test_code = @@code + code
    assert_equal 1, Interpreter.new.eval(test_code).ruby_value
  end

  def test_child_class2
    code = <<-CODE
x = X.new()
x.hello_p(0)
    CODE

    test_code = @@code + code
    assert_equal -1, Interpreter.new.eval(test_code).ruby_value
  end

  def test_child_class3
    code = <<-CODE
a = A.new()
a.hello_a(0)
    CODE

    test_code = @@code + code
    assert_equal 3, Interpreter.new.eval(test_code).ruby_value
  end

  def test_child_class4
    code = <<-CODE
a = A.new()
a.b(0)
    CODE

    test_code = @@code + code
    assert_equal 10, Interpreter.new.eval(test_code).ruby_value
  end

end
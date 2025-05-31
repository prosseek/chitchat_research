require_relative 'runtime/object'
require_relative 'runtime/class'
require_relative 'runtime/method'
require_relative 'runtime/context'
require_relative 'runtime/bootstrap'

# Object.new
Runtime['Class'].def :new do |receiver, arguments|
  receiver.new(arguments)
end

# print("hi")
Runtime['Object'].def :print do |_, arguments| # _ is a receiver
  puts arguments.first.ruby_value
  Runtime['nil']
end

# 1. it allocates a new id method in @runtime_class
# 2. it creates a method object that can be called.
Runtime['Object'].def :id do |receiver| # _ is a receiver
  v = receiver.id
  Runtime['Number'].new_with_value v
end

# Runtime["Object"].def :id do |receiver, arguments|
#   receiver.id
# end

# 1 + 2
# 1.+(2)
Runtime['Number'].def :+ do |receiver, arguments|
  a = receiver.ruby_value
  b = arguments.first.ruby_value
  Runtime['Number'].new_with_value a + b
end

Runtime['Number'].def :- do |receiver, arguments|
  a = receiver.ruby_value
  b = arguments.first.ruby_value
  Runtime['Number'].new_with_value a - b
end

# 1.<(2)
Runtime['Number'].def :< do |receiver, arguments|
  a = receiver.ruby_value
  b = arguments.first.ruby_value
  a < b ? Runtime['true'] : Runtime['false']
end


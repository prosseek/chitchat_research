# class LiteralNode < Struct.new(:value); end

# class AssignNode < Struct.new(:name, :value); end
# class ConstantNode < Struct.new(:name); end
# class DefNode < Struct.new(:name, :params, :body); end
# class ClassNode < Struct.new(:name, :body); end
# class IfNode  < Struct.new(:condition, :body, :else_body); end
# class WhileNode  < Struct.new(:condition, :body); end

# class LiteralNode
#   def show()
#     p "literalnode"
#     p self.value
#   end
# end
#
# # class CallNode < Struct.new(:receiver, :method, :arguments); end
# class CallNode
#   def show()
#     p "callnode"
#     p self.receiver, self.method, self.arguments
#   end
# end
#
# class AssignNode
#   def show()
#     p "assignnode"
#   end
# end
#
# class ConstantNode
#   def show()
#     p "constantnode"
#   end
# end
#
# class DefNode
#   def show()
#     p "defnode"
#   end
# end
#
# class ClassNode
#   def show()
#     p "classnode"
#   end
# end
#
# class IfNode
#   def show()
#     p "ifnode"
#   end
# end
#
# class WhileNode
#   def show()
#     p "whilenode"
#   end
# end

class Nodes
  
  def show()
    nodes.each_with_index do |node, index|
      p "#{index+1}: #{node}"
    end
  end
  
end  
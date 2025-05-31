class Nodes
  # This method is the "interpreter" part of our language. All nodes know how to eval
  # itself and returns the result of its evaluation by implementing the "eval" method.
  # The "context" variable is the environment in which the node is evaluated (local
  # variables, current class, etc.).
  def eval(context)
    return_value = nil
    nodes.each_with_index do |node, _|
      return_value = node.eval(context)
    end
    return_value || Runtime['nil']
  end
end

class NumberNode
  def eval(context)
    Runtime['Number'].new_with_value(value)
  end
end

class StringNode
  def eval(context)
    Runtime['String'].new_with_value(value)
  end
end

class TrueNode
  # noinspection RubyUnusedLocalVariable
  def eval(context)
    Runtime['true']
  end
end

class FalseNode
  # noinspection RubyUnusedLocalVariable
  def eval(context)
    Runtime['false']
  end
end

class NilNode
  # noinspection RubyUnusedLocalVariable
  def eval(context)
    Runtime['nil']
  end
end

class ConstantNode
  def eval(context)
    context[name] || raise("Constant not found #{name}")
  end
end

# Assign & Call is set and get variables
# When set the variables, @ and @@ should be checked to store them
# as instance variables (Object.instance_vars)
# or class variables in Runtime["__classVariables__"]

class AssignNode

  def eval(context)
    v = value.eval(context)
    context.variable_set(name, v)
  end
end

class CallNode
  # noinspection RubyArgCount
  def eval(context)
    # a, local var
    if receiver.nil? && arguments.empty?
      context.variable_get(method)
    else
      # receiver.print
      if receiver
        value = receiver.eval(context)
      else
        # print(...)
        value = context.current_self
      end

      if value
        evaluated_arguments = arguments.map { |arg| arg.eval(context) }
        value.send_message(method, evaluated_arguments)
      else
        raise("ERROR! value is null, method #{method}")
      end
    end
  end
end

class DefNode
  def eval(context)
    method = RMethod.new(params, body)
    context.current_class.runtime_methods[name] = method
  end
end

class ClassNode
  def eval(context)
    rclass = context[name]

    unless rclass # class was not defined
      parent_class = context[parent_name]
      if parent_class == nil
        parent_class = context['Object']
      end
      rclass = RClass.new(name, parent_class.name)
      context[name] = rclass
    end

    # class context means current_self == current_class
    class_context = Context.new(rclass, rclass)

    body.eval(class_context)

    rclass
  end
end

# noinspection RubyResolve
class IfNode
  def eval(context)
    ### Exercise
    # Here you have access to:
    #  condition: condition node that will determine if the body should be executed
    #       body: node to be executed if the condition is true
    #  else_body: node to be executed if the condition is false
    if condition.eval(context).ruby_value
      body.eval(context)
    elsif else_body
      else_body.eval(context)
    else
      Runtime['nil']
    end
  end
end

# noinspection RubyResolve
class WhileNode
  def eval(context)
    while condition.eval(context).ruby_value
      body.eval(context)
    end
  end
end

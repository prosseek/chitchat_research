# Represents the evaluation context, that tracks values that change depending on where 
# the code is evaluated.
# - "locals" holds local variables.
# - "current_self" is the object on which methods with no receivers are called,
#   eg.: print is like current_self.print
# - "current_class" is the class on which methods are defined with the "def" keyword.
class Context
  attr_reader :locals, :current_self, :current_class, :toplevel
  
  # We store constants as class variable (class variables start with @@ and instance
  # variables start with @ in Ruby) since they are globally accessible. If you want to
  # implement namespacing of constants, you could store it in the instance of this 
  # class.
  @@constants = {}
  
  def initialize(current_self, current_class=current_self.runtime_class)
    @locals = {}
    @current_self = current_self
    @current_class = current_class
    @toplevel = false
  end

  def setToplevel()
    @toplevel = true
  end

  # Shortcuts to access constants via Runtime["ConstantName"]
  def [](name)
    @@constants[name]
  end
  def []=(name, value)
    @@constants[name] = value
  end

  # in_class means the context is *not* in method, but in class
  # class_context = Context.new(rclass, rclass)
  def in_class()
    current_class == current_self && (not @toplevel)
  end

  def in_method()
    current_class != current_self && (not @toplevel)
  end

  # In bootstrap, we have Runtime = Context.new(Obzect.new)
  # So, in global context, the name of current context's object is "Object"
  def in_global()
    @toplevel
  end

  def variable_set(name, value)
    if name.start_with?("@")
      # It should be outside the global context
      if in_global
        raise "ERROR! @/@@ variable is used in global context"
      end

      # Check if the variable is class variable
      if name.start_with?("@@")
        the_name = current_class.name + "@@" + name
        @@constants[the_name] = value
      else
        # name starts with single "@"
        if in_class
          # when in class, it fills in the instance_vars in the class
          the_class = current_class
          the_class.add_instance_var(name, value)
        else
          # if in function body context
          the_object = current_self
          the_object.add_instance_var(name, value)
        end
      end
    else # local variable
      locals[name] = value
    end
  end

  def global_variable_get(name)
    @@constants["__toplevel__"].locals[name]
  end

  def variable_get(name)
    if name.start_with?("@")
      # It should be outside the global context
      if in_global
        raise "ERROR! @/@@ variable is used in global context"
      end

      # Check if the variable is class variable
      if name.start_with?("@@")
        the_name = current_class.name + "@@" + name
        @@constants[the_name]
      else
        # name starts with single "@"
        the_object = current_self
        value = the_object.get_instance_var(name)

        unless value
          the_class = current_class
          value = the_class.get_instance_var(name)
          unless value
            raise "ERROR! No #{name} found"
          end
        end
        value
      end
    else # local variable
      value = locals[name]
      unless value
        value = global_variable_get(name)
        unless value
          raise "No variable #{name} found"
        end
      end
      value
    end
  end
end

# Represents a class in the Ruby world. Classes are objects in runtime so they
# inherit from RObject.
class RClass < RObject
  attr_reader :name, :parent_name, :runtime_methods, :instance_vars

  # Creates a new class. Number is an instance of Class for example.
  def initialize(name = nil, parent_name = nil)
    @runtime_methods = {}

    # instance_vars in RClass has the map of variable name to default value
    # instance_vars in RObject has the assigned value from users, when the value is not in object, the value in the class
    # should be found
    @instance_vars = {}

    @parent_name = parent_name
    @name = name

    # Check if we're bootstrapping (launching the runtime). During this process the 
    # runtime is not fully initialized and core classes do not yet exists, so we defer 
    # using those once the language is bootstrapped.
    # This solves the chicken-or-the-egg problem with the Class class. We can 
    # initialize Class then set Class.class = Class.
    if defined?(Runtime)
      runtime_class = Runtime["Class"]
    else
      runtime_class = nil
    end
  
    super(runtime_class)
  end

  # Lookup a method
  def lookup(method_name)

    # Check if current class has the method
    method = @runtime_methods[method_name]

    # When the method is not found check the parent classes
    unless method
      current_class = self
      while true
        parent_name = current_class.parent_name
        parent_class = Runtime[parent_name]

        raise "Method not found: #{method_name}" if parent_class == nil
        method = parent_class.lookup(method_name)
        break if method != nil
      end
    end

    method
  end
  
  # Helper method to define a method on this class
  def def(name, &block)
    @runtime_methods[name.to_s] = block
  end

  # Helper method to add instance variables
  def add(name, default_value)
    @instance_vars[name] = default_value
  end

  def get(name)
    @instance_vars[name]
  end

  # Create a new instance of this class
  # Class's new makes an object
  def new(arguments = [])
    RObject.new(self, nil, arguments)
  end
  
  # Create an instance of this class that holds a Ruby value. Like a String, 
  # Number or true.
  def new_with_value(value)
    RObject.new(self, value)
  end
end
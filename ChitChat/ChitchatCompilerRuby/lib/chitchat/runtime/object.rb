# Represents an Awesome object instance in the Ruby world.
class RObject
  attr_accessor :runtime_class, :ruby_value, :id, :instance_vars

  # Each object have a class (named runtime_class to prevent errors with Ruby's class
  # method). Optionaly an object can hold a Ruby value (eg.: numbers and strings).
  def initialize(runtime_class, ruby_value=nil, arguments = [])
    # I don't use ruby's keyword argument
    # So, default value for ruby_value is set as self
    # I have this chage to provide arguments parameter without breaking existing code
    # When passing argument, use RObject.new(class, nil, arguments)
    if ruby_value == nil
      ruby_value = self
    end
    @runtime_class = runtime_class
    @ruby_value = ruby_value
    @arguments = arguments

    ## Not fully tested
    @instance_vars = {}
    @id = self.object_id

    if @arguments != []
      send_message("initialize", @arguments)
    end

  end

  # Call a method on the object.
  def send_message(method, arguments=[])
    # Like a typical Class-based runtime model, we store methods in the class of the
    # object.
    @runtime_class.lookup(method).call(self, arguments)
  end

  # Helper method to add instance variables
  def add_instance_var(name, default_value)
    @instance_vars[name] = default_value
  end

  def get_instance_var(name)
    @instance_vars[name]
  end

end
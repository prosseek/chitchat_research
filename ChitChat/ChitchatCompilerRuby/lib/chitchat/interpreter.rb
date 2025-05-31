$:.unshift File.expand_path("../", __FILE__)

require 'parser'
require 'runtime'
require 'internal'
require 'nodes_eval'

class Interpreter
  def initialize
    @parser = Parser.new
  end

  def eval(code, debug=false)
    nodes = @parser.parse(code)
    if debug
      nodes.show
    end
    nodes.eval(Runtime)
  end
end


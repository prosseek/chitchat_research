# coding: utf-8
lib = File.expand_path('../lib', __FILE__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)
require 'chitchat/version'

Gem::Specification.new do |spec|
  spec.name          = "chitchat"
  spec.version       = Chitchat::VERSION
  spec.authors       = ["smcho"]
  spec.email         = ["sm.cho@mac.com"]

  spec.summary       = "Good thing to know"
  spec.description   = "Compiler"
  spec.homepage      = "http://example.com"

  # Prevent pushing this gem to RubyGems.org by setting 'allowed_push_host', or
  # delete this section to allow pushing this gem to any host.
  if spec.respond_to?(:metadata)
    spec.metadata['allowed_push_host'] = "TODO: Set to 'http://mygemserver.com'"
  else
    raise "RubyGems 2.0 or newer is required to protect against public gem pushes."
  end

  spec.files         = `git ls-files -z`.split("\x0").reject { |f| f.match(%r{^(test|spec|features)/}) }
  spec.files         += ["lib/chitchat/parser.rb", "lib/chitchat/lexer.rb"]
  spec.bindir        = "bin"
  spec.executables   = "chitchat"
  spec.require_paths = ["lib"]

  spec.add_development_dependency "bundler", "~> 1.10"
  spec.add_development_dependency "rake", "~> 10.0"
  spec.add_development_dependency "minitest"
  spec.add_development_dependency "rspec"
  spec.add_development_dependency "racc", "1.4.13"
  spec.add_development_dependency "rexical", "1.0.5"
  spec.add_development_dependency "test-unit", "1.2.3"

end

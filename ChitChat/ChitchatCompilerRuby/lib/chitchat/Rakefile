require 'rake/testtask'

task :build do
  sh('rex tokens.rex -o lexer.rb')
  sh('racc grammar.y -o parser.rb')
end

task :bundle do
  sh('bundle')
end


# Rake::TestTask.new(:test) do |t|
#   t.libs << '.'
#   t.libs << 'test'
#   t.pattern = 'test/**_test.rb'
# end

task :default => :build
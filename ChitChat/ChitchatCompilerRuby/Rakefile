require "bundler/gem_tasks"
require "rake/testtask"

Rake::TestTask.new(:test) do |t|
  t.libs << "test"
  t.libs << "lib"
  t.test_files = FileList['test/**/*_test.rb']
end

task :build do
  sh('rex lib/chitchat/tokens.rex -o lib/chitchat/lexer.rb')
  sh('racc lib/chitchat/grammar.y -o lib/chitchat/parser.rb')
end

task :bundle do
  sh('bundle')
end

task :default => :test

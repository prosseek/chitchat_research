# ChitChat Compiler

Welcome to your new gem! In this directory, you'll find the files you need 
to be able to package up your Ruby library into a gem. 
Put your Ruby code in the file `lib/chitchat`. 
To experiment with that code, run `bin/console` for an interactive prompt.

TODO: Delete this and the text above, and describe your gem

## Build & Test 

If necessary, use git to synchronize the files in the local directory. 
In *.gemspec, it uses the git command ``git ls-files -z`.split("\x0")` to get the
list of files. Refer to <http://stackoverflow.com/questions/6256743/while-executing-gem-extconf-rb-are-not-files>

1. Execute 'rake build'  
    1. to generate lexer.rb and parser.rb code.
    2. to generate ChitChat-0.1.0.gem in the pkg directory.
2. Execute 'rake test' or just 'rake'
    1. to run the test code.   

## Bundle & Installation

execute `bundle` 

    Resolving dependencies...
    Using rake 10.4.2
    Using Chitchat 0.1.0 from source at `.`
    ...
    Using test-unit 1.2.3
    Using rspec 3.4.0
    Bundle complete! 8 Gemfile dependencies, 14 gems now installed.
    Use `bundle show [gemname]` to see where a bundled gem is installed.

The `Gemfile.lock` is created. 

### Install

execute `gem install pkg/chitchat-0.1.0.gem`

#### Installation location

`gem environment' shows the gem directory. 

    - GEM PATHS:
        - /Users/smcho/.rbenv/versions/2.2.3/lib/ruby/gems/2.2.0
        - /Users/smcho/.gem/ruby/2.2.0

You can find the installed gem in `/Users/smcho/.rbenv/versions/2.2.3/lib/ruby/gems/2.2.0/gems/chitchat-0.1.0`. 

## Usage

You can use `require` to use the installed gem. 

    smcho@macho ~> irb
    >> require 'chitchat'
    => true


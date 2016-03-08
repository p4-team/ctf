require_relative 'unholy'
include UnHoly
python_hi
puts ruby_hi
puts "Programming Skills: PRIMARILY RUBY AND PYTHON BUT I CAN USE ANY TYPE OF GEM TO CONTROL ANY TYPE OF SNAKE"
puts "give me your flag"
flag = gets.chomp!
arr = flag.unpack("V*")
is_key_correct? arr

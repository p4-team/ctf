require 'socket'
require 'shellwords'
server = TCPServer.new(9090)

while (connection = server.accept)
	Thread.new(connection) do |conn|
		conn.puts "gimme str 1"
		s1 = conn.gets.chomp
		conn.puts "gimme str 2"
		s2 = conn.gets.chomp
		exec = "python ./tlseorg.py --check #{Shellwords.shellescape s1} #{Shellwords.shellescape s2}"
		out = `#{exec}`
		puts out
		if out == "Success\n"
			conn.puts "FLAG"
		else
			conn.puts "failure"
		end
		conn.close
	end
end


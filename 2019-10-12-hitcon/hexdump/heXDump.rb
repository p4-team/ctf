#!/usr/bin/env ruby
# encoding: ascii-8bit
# frozen_string_literal: true

require 'English'
require 'fileutils'
require 'securerandom'

FLAG_PATH = File.join(ENV['HOME'], 'flag')
DEFAULT_MODE = "sha1sum %s | awk '{ print $1 }'"

def setup
  STDOUT.sync = 0
  STDIN.sync = 0
  @mode = DEFAULT_MODE
  @file = '/tmp/' + SecureRandom.hex
  FileUtils.touch(@file)
  @key = output("sha256sum #{FLAG_PATH} | awk '{ print $1 }'").strip
  raise if @key.size != 32 * 2
end

def menu
  <<~MENU
    1) write
    2) read
    3) change output mode
    0) quit
  MENU
end

def output(cmd)
  IO.popen(cmd, &:gets)
end

def write
  puts 'Data? (In hex format)'
  data = gets
  return false unless data && !data.empty? && data.size < 0x1000

  IO.popen("xxd -r -ps - #{@file}", 'r+') do |f|
    f.puts data
    f.close_write
  end
  return false unless $CHILD_STATUS.success?

  true
end

def read
  unless File.exist?(@file)
    puts 'Write something first plz.'
    return true
  end

  puts output(format(@mode, @file))
  true
end

def mode_menu
  <<~MODE
    Which mode?
    - SHA1
    - MD5
    - AES
  MODE
end

def change_mode
  puts mode_menu
  @mode = case gets.strip.downcase
          when 'sha1' then "sha1sum %s | awk '{ print $1 }'"
          when 'md5' then "md5sum %s | awk '{ print $1 }'"
          when 'aes' then "openssl enc -aes-256-ecb -in %s -K #{@key} | xxd -ps"
          else DEFAULT_MODE
          end
end

def secret
  FileUtils.cp(FLAG_PATH, @file)
  true
end

def main_loop
  puts menu
  case gets.to_i
  when 1 then write
  when 2 then read
  when 3 then change_mode
  when 1337 then secret
  else false
  end
end

setup
begin
  loop while main_loop
  puts 'See ya!'
ensure
  FileUtils.rm_f(@file)
end

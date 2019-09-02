require 'securerandom'
require 'openssl'

ROUNDS = 765
BITS = 128
PAIRS = 6

def encrypt(msg, key)
    enc = msg
    mask = (1 << BITS) - 1
    ROUNDS.times do
        enc = (enc + key) & mask
        enc = enc ^ key
    end
    enc
end

def decrypt(msg, key)
    enc = msg
    mask = (1 << BITS) - 1
    ROUNDS.times do
        enc = enc ^ key
        enc = (enc - key) & mask
    end
    enc
end

fail unless BITS % 8 == 0

flag = SecureRandom.bytes(BITS / 8).unpack1('H*').to_i(16)
key = SecureRandom.bytes(BITS / 8).unpack1('H*').to_i(16)

STDERR.puts "The flag: TWCTF{%x}" % flag
STDERR.puts "Key=%x" % key
STDOUT.puts "Encrypted flag: %x" % encrypt(flag, key)
fail unless decrypt(encrypt(flag, key), key) == flag # Decryption Check

PAIRS.times do |i|
    plain = SecureRandom.bytes(BITS / 8).unpack1('H*').to_i(16)
    enc = encrypt(plain, key)
    STDOUT.puts "Pair %d: plain=%x enc=%x" % [-~i, plain, enc]
end
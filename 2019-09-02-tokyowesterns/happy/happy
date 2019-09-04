#!/usr/bin/env ruby
require 'openssl/oaep'
require 'optparse'

class Key
    def initialize(attr)
        @attr = attr
    end

    def self.generate_key(bits, k)
        while true
            p = OpenSSL::BN::generate_prime(bits, true).to_i
            q = OpenSSL::BN::generate_prime(bits, true).to_i
            e = 65537
            next if e.gcd((p - 1) * (q - 1) * q ** (k - 1)) > 1
            d1 = e.pow((p - 1) / 2 - 2, (p - 1))
            fail unless d1 * e % (p - 1) == 1 
            d2 = e.pow(((q - 1) / 2 - 1) * (q - 1) * (k > 1 ? q ** (k - 2) : 1) - 1, q ** (k - 1) * (q - 1))
            fail unless d2 * e % (q ** (k - 1) * (q - 1)) == 1 
            cf = p.pow(q ** (k - 1) * (q - 1) - 1, q ** k)
            return Key.new({
                n: p * q ** k,
                e: e,
                p: p,
                q: q ** k,
                d1: d1,
                d2: d2,
                cf: cf,
            })
            break
        end
    end

    def private?
        @attr.key?(:d1) && @attr.key?(:d2) && @attr.key?(:p) && @attr.key?(:q)
    end

    def public?
        @attr.key?(:n) && @attr.key?(:e)
    end

    def public_key
        Key.new(@attr.reject{|k, v| [:p, :q, :d1, :d2, :ce].include?(k)})
    end

    def self.import(str)
        Key.new(Marshal.load(str))
    end

    def to_s
        Marshal.dump(@attr)
    end

    def public_encrypt(str, pad = true)
        raise StandardError.new('NotPublicKey') unless public?
        n, e = @attr[:n], @attr[:e]
        if pad
            msg = OpenSSL::PKCS1.add_oaep_mgf1(str, (n.to_s(16).size + 1) / 2)
        else
            msg = str
        end
        long_to_bytes(msg.unpack1('H*').to_i(16).pow(e, n))
    end

    def private_decrypt(str, pad = true)
        raise StandardError.new('NotPrivateKey') unless private?
        n, p, q, d1, d2, c = @attr[:n], @attr[:p], @attr[:q], @attr[:d1], @attr[:d2], @attr[:cf]
        enc = str.unpack1('H*').to_i(16)
        e1 = enc.pow(d1, p)
        e2 = enc.pow(d2, q)
        ret = long_to_bytes(e1 + p * ((c * (e2 - e1)) % q))
        ret = "\0" + ret while ret.size < (n.to_s(16).size + 1) / 2
        pad ? OpenSSL::PKCS1.check_oaep_mgf1(ret) : ret
    end

    private
    
    def long_to_bytes(l)
        r = '%x' % l
        r = '0' + r if r.size.odd?
        return [r].pack('H*')
    end
end

def main
    if ARGV[0] == 'keygen'
        if ARGV.size != 5
            STDERR.puts "Usage: happy keygen <bits> <k> <path_to_private_key> <path_to_public_key>"
            exit 1
        end
        bits = ARGV[1].to_i
        k = ARGV[2].to_i
        priv = ARGV[3]
        pub = ARGV[4]
        if bits < 700 || k < 1
            STDERR.puts "Invalid parameter"
            exit 1
        end
        key = Key.generate_key(bits, k)
        File.binwrite(ARGV[3], key.to_s)
        File.binwrite(ARGV[4], key.public_key.to_s)
    elsif ARGV[0] == 'encrypt'
        if ARGV.size != 4
            STDERR.puts "Usage: happy encrypt <path_to_key_file> <path_to_input> <path_to_output>"
            exit 1
        end
        key = Key.import(File.binread(ARGV[1]))
        File.binwrite(ARGV[3], key.public_encrypt(File.binread(ARGV[2])))
    elsif ARGV[0] == 'decrypt'
        if ARGV.size != 4
            STDERR.puts "Usage: happy decrypt <path_to_key_file> <path_to_input> <path_to_output>"
            exit 1
        end
        key = Key.import(File.binread(ARGV[1]))
        File.binwrite(ARGV[3], key.private_decrypt(File.binread(ARGV[2])))
    else
        STDERR.puts "Usage: happy keygen/encrypt/decrypt"
        exit 1
    end
end

main if __FILE__ == $0
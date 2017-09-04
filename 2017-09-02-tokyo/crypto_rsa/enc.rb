require 'json'

def extgcd(a,b)
  return [1,0] if b == 0
  y,x = extgcd(b, a % b)
  y -= (a/b)*x
  return [x,y]
end

def mod_inverse(a, mod)
  x,y = extgcd(a, mod)
  return x % mod
end

def check_prime(p, count = nil)
  return true if [2,3].include?(p)
  return false if p.even? || p < 2

  d, s = p - 1, 0
  d, s = d >> 1, s + 1 while d.even?

  count = [16, p.to_s(4).size].max unless count
  count.times do
    a = rand(2...(p - 1))
    return false if p.gcd(a) != 1
    if (x = mod_pow(a, d, p)) != 1
      return false unless (0...s).inject(false) do |res, r| 
        break true if(x == p - 1)
        x = x * x % p
        next false
      end
    end
  end
  return true
end

def mod_pow(a, n, mod)
  ret = 1
  while n > 0
    ret = (ret * a) % mod if n.odd?
    a = (a * a) % mod
    n >>= 1
  end
  ret
end

def next_prime(x)
  while !check_prime(x)
    x += 1
  end
  x
end

p = rand(2**1024)
q = 19 * p + rand(2**512)

p = next_prime(p)
q = next_prime(q)

e = 65537
d = mod_inverse(e, (p - 1) * (q - 1))

n = (p.to_i * q.to_i)

flag = File.binread('flag').unpack1("H*").to_i(16) * 256
while flag * 256 + 255 < n
  flag = flag * 256 + rand(256)
end

enc = mod_pow(flag, e, n)
dec = mod_pow(enc, d, n)
fail unless dec == flag
File.write('pubkey', [n, e].to_json)
File.write('flag.enc', enc)
File.write('privkey', [n, d].to_json)


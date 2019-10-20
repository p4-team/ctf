# Fileserver (web, 345p, 39 solved)

In the challenge we get access to a custom made http server.
We can easily look around and recover the [source code](fileserver.rb).

There are 2 problems here to solve:

1. We don't know the flag file name, and we know it's random and pretty long, so we need either RCE or directory listing
2. In order to do anything fancy, we need to bypass the bad_char check with some special characters

## Bad char check

The check is:

```ruby
def is_bad_path(path)
  bad_char = nil

  %w(* ? [ { \\).each do |char|
    if path.include? char
      bad_char = char
      break
    end
  end

  if bad_char.nil?
    false
  else
    # check if brackets are paired
    if bad_char == ?{
      path[path.index(bad_char)..].include? ?}
    elsif bad_char == ?[
      path[path.index(bad_char)..].include? ?]
    else
      true
    end
  end
end
```

What seems odd is that:

- It allows for `{}[]` as long as they're not paired
- It looks only at the first bad char it finds
- The loop, a bit confusingly, goes over the forbidden chars in order, and on the data! This means if you start your payload with `{` but you have `*` at the very end, it will first find the `*`

The last point can be used to break this protection -> the order of `{}` and `[]` is set in such a way that if we send payload `{[}` then the script will first find `[` and check if it's paired or not, and we're free to use as many `{}` as we want.

## Arbitrary file read

Remeber, this still has to be some valid path, so having `[` doesn't seem so great, but curly braces denote `alternative` in glob.
This means we can use path `/{[,p}ublic/index.html` and it will work just fine for us.

The server looks for path like:

```ruby
  payload=req.path[1..]
  matches = Dir.glob(payload)
```

So strips the first `/`, and the webserver strips any additional `/` we place, however if we do `/{[,/}` the inner one will not be stripped!
This way we gain arbitrary file read, since we can just send: `GET /{[,/}etc/passwd` (encoded as `GET /%7b%5b,/%7detc/passwd` of course).

## Listing directories

The last part is probably the hardest one, how to list the `/tmp/flags` directory to learn the flag file name?
We were considering first to use something like arbitrary file read payload we have with suffix `{a,b,c,d...}` multiplied by the number of characters in flag file name, but the GET request was waaay too long.

Now we need to focus on the:

```ruby
  if req.path.end_with? '/'
    if req.path.include? '.'
      raise BadRequest
    end

    path = ".#{req.path}*"
    files = Dir.glob(path)
    res['Content-Type'] = 'text/html'
    res.body = ERB.new(File.read('index.html.erb')).result(binding)
    next
  end
```

The server allows for directory listing, but it includes a `.` at the front, and we can't put any `.` ourselves so somehow bypass it with traversal.
So we can only list directories under current CWD, and we want to be higher.

After going through glob source code we fund a very interesting quirk, probably related to `CVE-2018-8780`.
In short `Dir.glob` doesn't handle nullbytes properly, and splits the arguments on the nullbyte and considers only the last part.
So if we send `GET /%00/tmp/flags/` it will cut away the `./%00` leaving us with `/tmp/flags/*`!

## Final payload

Finally we can do:

```python
    s = nc("fileserver.chal.seccon.jp", 9292)
    s.sendall("GET /%00/tmp/flags/ HTTP/1.0\r\nConnection: close\r\n\r\n")
    print(s.recv(9999))
    print(s.recv(9999))
```

To get the flag file name and then

```python
    s = nc("fileserver.chal.seccon.jp", 9292)
    s.sendall("GET /%7b%5b,/%7dtmp/flags/MMnHIU0fofiPdL1HlJkyQgDu4O8YNERR.txt HTTP/1.0\r\nConnection: close\r\n\r\n")
    print(s.recv(9999))
    print(s.recv(9999))
```

To read the flag `SECCON{You_are_the_Globbin'_Slayer}`

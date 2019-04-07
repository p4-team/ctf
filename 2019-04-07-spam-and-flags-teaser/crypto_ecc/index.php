 <?php

function point($x = 0, $y = 0){
    return array('x' => $x, 'y' => $y);
}

$P = gmp_init("0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF");
$A = gmp_init("0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC");
$B = gmp_init("0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B");
$N = gmp_init("0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551");

$SECRET_KEY = gmp_import(file_get_contents('secret_key.txt'));

$G = point(
    "0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296",
    "0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5"
);

function is_identity_element($p){
    return gmp_cmp($p['x'], 0) == 0 and gmp_cmp($p['y'], 0) == 0;
}

function decompress($x){
    global $P, $A, $B;
    $y2 = gmp_mod(gmp_add(gmp_mul(gmp_add(gmp_mul($x, $x), $A), $x), $B), $P);
    $potential_y = gmp_powm($y2, gmp_div(gmp_add($P, 1), 4), $P);
    if (gmp_cmp(gmp_mod(gmp_mul($potential_y, $potential_y), $P), $y2) !=0 )
        return point();
    return point($x, $potential_y);
}

function force_decompress($x){
    while(true){
        $result = decompress($x);
        if (!is_identity_element($result))
            return $result;
        $x = gmp_add($x, 1);
    }
}

function add_point($p, $q){
    global $P, $A;
    if (is_identity_element($p))
        return $q;
    if (is_identity_element($q))
        return $p;
    if ($p['x'] == $q['x']){
        if (gmp_cmp($p['y'], $q['y']) != 0)
            return point();
        $lambda = gmp_mod(gmp_mul(
            gmp_add(gmp_mul(3, gmp_mul($p['x'], $p['x'])), $A),
            gmp_invert(gmp_add($p['y'], $p['y']), $P)
        ), $P);
    }
    else
        $lambda = gmp_mod(gmp_mul(
            gmp_sub($q['y'], $p['y']),
            gmp_invert(gmp_sub($q['x'], $p['x']), $P)
        ), $P);
    $rx = gmp_mod(gmp_sub(gmp_mul($lambda, $lambda), gmp_add($p['x'], $q['x'])), $P);
    $ry = gmp_mod(gmp_sub(gmp_mul($lambda, gmp_sub($p['x'], $rx)), $p['y']), $P);
    return point($rx, $ry);
}

function multiply_point($p, $n){
    $n_as_bits = gmp_strval($n, 2);
    $result = point();
    foreach(str_split($n_as_bits) as $bit){
        $result = add_point($result, $result);
        $added = add_point($result, $p);
        if ($bit == '1')
            $result = $added;
    }
    return $result;
}

function selftest(){
    global $G, $N;

    print("Testing generator and order\n");
    $res = multiply_point($G, $N);
    print("X: " . gmp_strval($res['x'], 16) . "\n");
    print("Y: " . gmp_strval($res['y'], 16) . "\n");

    print("Testing decompression\n");
    $res = decompress($G['x']);
    print("Original Y:     " . gmp_strval($G['y'], 16) . "\n");
    print("Decompressed Y: " . gmp_strval($res['y'], 16) . "\n");
    $res = decompress(10);
    print("Invalid Decompressed point: " . gmp_strval($res['x'], 16) . " " . gmp_strval($res['y'], 16) . "\n");

}

function encrypt_db(){
    global $SECRET_KEY, $G;
    $db = explode("\n", file_get_contents("all_passwords.txt"));
    $db_fc = array();
    $counter = 0;
    foreach($db as $db_entry){
        if ($db_entry == "")
            continue;
        $first_char = $db_entry[0];
        if (!isset($db_fc[$first_char]))
            $db_fc[$first_char] = "";
        $point = force_decompress(gmp_import($db_entry));
        $point = multiply_point($point, $SECRET_KEY);
        $x = gmp_strval($point['x'], 16);
        $y = gmp_strval($point['y'], 16);
        $db_fc[$first_char] .= "['$x', '$y'],\n";
        ++$counter;
        if ($counter%100 == 0){
            print("$counter\n");
        }
    }
    foreach($db_fc as $k => $v){
        file_put_contents("pwdb/pw_${k}.db", "${v}[0,0]");
    }
}

function pw_result($pw_first, $encpw_x, $encpw_y){
    global $SECRET_KEY, $P;
    $fc = $pw_first[0];
    $db = file_get_contents("pwdb/pw_${fc}.db");
    $x = gmp_mod(gmp_init("0x$encpw_x"), $P);
    $y = gmp_mod(gmp_init("0x$encpw_y"), $P);
    $point = multiply_point(point($x, $y), $SECRET_KEY);
    $x = gmp_strval($point['x'], 16);
    $y = gmp_strval($point['y'], 16);
    print("continue_check({\n'x': '$x',\n'y': '$y',\n'pws': [$db]\n});");
}

function main_page(){
?>
<HTML>
<HEAD><TITLE>Have you been OWNED?</TITLE>
<SCRIPT type="application/javascript" src="BigInteger.js"></SCRIPT>
<SCRIPT type="application/javascript">

function point(x = 0, y = 0){
    if ((typeof x) == "string")
        x = bigInt(x, 16);
    if ((typeof y) == "string")
        y = bigInt(y, 16);
    return {'x': bigInt(x), 'y': bigInt(y)};
}

P = bigInt("FFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF", 16);
G = point(
    "6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296",
    "4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5"
);
A = bigInt("FFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC", 16);
B = bigInt("5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B", 16);
N = bigInt("FFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551", 16);

function is_identity_element(p){
    return p.x.eq(0) && p.y.eq(0);
}

function decompress(x){
    y2 = x.multiply(x).add(A).multiply(x).add(B).mod(P);
    potential_y = y2.modPow(P.add(1).divide(4), P);
    if (!potential_y.multiply(potential_y).mod(P).eq(y2))
        return point();
    return point(x, potential_y);
}

function force_decompress(x){
    while(true){
        result = decompress(x);
        if (!is_identity_element(result))
            return result;
        x = x.add(1);
    }
}

function add_point(p, q){
    var lambda;
    if (is_identity_element(p))
        return q;
    if (is_identity_element(q))
        return p;
    if (p.x.eq(q.x)){
        if (! p.y.eq(q.y))
            return point();
        lambda =
            p.x.multiply(p.x).multiply(3).add(A)
            .multiply(
                p.y.add(p.y).modInv(P)
            ).mod(P);
    }
    else
        lambda =
            q.y.subtract(p.y).add(P)
            .multiply(
                q.x.subtract(p.x).add(P).modInv(P)
            ).mod(P)
    var rx = lambda.multiply(lambda).subtract(p.x).subtract(q.x).add(P).mod(P);
    var ry = lambda.multiply(p.x.subtract(rx).add(P)).subtract(p.y).add(P).mod(P);
    return point(rx, ry);
}

function multiply_point(p, n){
    var n_as_bits = n.toArray(2).value;
    var result = point();
    for (index = 0; index < n_as_bits.length; ++index) {
        result = add_point(result, result);
        added = add_point(result, p);
        if (n_as_bits[index] == 1)
            result = added;
    }
    return result;
}

function selftest(){
    console.log("Running selftest");
    res = multiply_point(G, N.subtract(1));
    console.log("-G", ! is_identity_element(res));
    res = multiply_point(G, N);
    console.log("Identity", is_identity_element(res));
    console.log("Decompressed G", decompress(G.x).y.eq(G.y));
    console.log("Decompressed invalid", is_identity_element(decompress(bigInt(10))));
}

function to_hex(s) {
    var result = '';
    for(var i = 0; i < s.length; i++) {
        result += '' + s.charCodeAt(i).toString(16);
    }
    return result;
}

function check(){
    var s = document.createElement('script');
    var pw = document.getElementById('pw').value;
    var pw_first=pw[0];
    var pw_as_bigint = bigInt(to_hex(pw), 16).mod(P);
    var pw_as_point = force_decompress(pw_as_bigint);
    enc_key = bigInt.randBetween(P.divide(16), P);
    var encpw = multiply_point(pw_as_point, enc_key);
    s.setAttribute('src','?pw_first=' + pw_first + '&encpw_x=' + encpw.x.toString(16) + '&encpw_y=' + encpw.y.toString(16));
    document.head.appendChild(s);
}

function continue_check(p){
    var dec_key = enc_key.modInv(N);
    console.log("PW result from server ", p);
    var dec_pw = multiply_point(point(p.x, p.y), dec_key);
    var oh_no = false;
    for (i=0; i<p.pws.length; ++i){
        pw_point = point(p.pws[i][0], p.pws[i][1]);
        if (pw_point.x.eq(dec_pw.x) && pw_point.y.eq(dec_pw.y))
            oh_no = true;
    }
    if (oh_no){
        document.getElementById('result').innerHTML = "<span style='color:red;font-weight:bold'>!!! Password compromised !!!</span>";
    } else {
        document.getElementById('result').innerHTML = "<span style='color:green'>It's all good.</span>";
    }
}
selftest();
</SCRIPT>

</HEAD>
<BODY>
<H1>Have you been OWNED?</H1>
Did you know that the passwords for all 10000 users of <B>ourspace.com</B> was compromised?<BR>
Was your password leaked too? Find out by filling the form below!<BR><BR>
<INPUT type="password" name="pw" id="pw"><INPUT type="button" onclick="check()" value="Let's see"><BR><BR>
<SPAN id="result">...</SPAN><BR><BR>
<BR>
Scared to just send us your password? You should be otherwise, but with us, you are fully secured, with the latest "Elliptic Curve" cryptography!<BR>
We will never know your actual password, only the first character! And you will not know any other password either.<BR>
Still not convinced? <A HREF="?source=1">See the source of this page</A>
</BODY>
</HTML>


<?php
}

if(php_sapi_name() == "cli") {
    print("Welcome to CLI mode\n");
    selftest();
    encrypt_db();
} else{
    if (isset($_GET['pw_first']))
        pw_result($_GET['pw_first'], $_GET['encpw_x'], $_GET['encpw_y']);
    else if(isset($_GET['source']))
        show_source('index.php');
    else
        main_page();
}
?>

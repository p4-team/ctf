<?php
include 'common.php';

if(empty($_POST['imagekey'])) {
    header('Location: ?op=home');
    exit();
}

$imagekey = $_POST['imagekey'];
$im = load_image($imagekey);

$w = imagesx($im);
$h = imagesy($im);
if($w > MAX_IM_SIZE || $h > MAX_IM_SIZE)
    fatal("Invalid image dimensions.");

$nc = imagecolorstotal($im);
if($nc == 0 || $nc > 256)
    fatal("Invalid palette size.");


$data = json_decode($_POST['savedata'], true);
if($data === null)
    fatal("Invalid JSON data.");

if(!is_array($data['pal']) || !is_array($data['im']))
    fatal("Bad data.");

$newpal = $data['pal'];
$newim = $data['im'];
if(count($newpal) > 256 || count($newim) != ($w * $h))
    fatal("Bad data.");

for($i=0; $i<count($newpal); $i++) {
    list($cr, $cg, $cb) = sscanf($newpal[$i], "#%2x%2x%2x");
    if($i < $nc) {
        imagecolorset($im, $i, $cr, $cg, $cb);
    } else {
        imagecolorallocate($im, $cr, $cg, $cb);
    }
}

$i = 0;
for($y=0; $y<$h; $y++) {
    for($x=0; $x<$w; $x++) {
        imagesetpixel($im, $x, $y, $newim[$i]);
        $i++;
    }
}

save_image($im, $imagekey);

header("Location: ?op=edit&imagekey=$imagekey");
?>
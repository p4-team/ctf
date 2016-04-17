<?php
include 'common.php';

if(empty($_GET['imagekey'])) {
    header('Location: ?op=home');
    exit();
}

$imagekey = $_GET['imagekey'];
$im = load_image($imagekey);

$w = imagesx($im);
$h = imagesy($im);
if($w > MAX_IM_SIZE || $h > MAX_IM_SIZE)
    fatal("Invalid image dimensions.");

$nc = imagecolorstotal($im);
if($nc == 0 || $nc > 256)
    fatal("Invalid palette size.");
?>
<div class="article">
    <h2>Edit your Pixel Art!</h2>
    <div>
        <form id="ps-saveform" action="?op=save" method="POST">
            <input name="imagekey" type="hidden" value="<?=$imagekey;?>" />
            <input id="ps-savedata" name="savedata" type="hidden" />
            <input name="submit" type="submit" value="Save!" />
            <a href="uploads/<?=$imagekey;?>.png">View saved image</a>
        </form>
    </div>
</div>

<link rel="stylesheet" property="stylesheet" href="css/editor.css">
<div class="editor">
    <div class="pixels"><canvas id="ps-pixels" width="512" height="512">Please upgrade your browser!</canvas></div>
    <div class="palette">
        <canvas id="ps-palette" width="256" height="256">Please upgrade your browser!</canvas>
        <br />
        <input id="ps-palette-picker" type="color" />
    </div>
</div>

<script src="js/editor.js"></script>
<script>
<?php
echo "PixelShop.init_palette([";
for($i=0; $i<$nc; $i++) {
    $arr = imagecolorsforindex($im, $i);
    echo sprintf('"#%02x%02x%02x",', $arr['red'], $arr['green'], $arr['blue']);
}
echo ']);';
echo "PixelShop.init_pixels($w, $h, [";
for($y=0; $y<$h; $y++) {
    for($x=0; $x<$w; $x++) {
        echo imagecolorat($im, $x, $y), ',';
    }
}
echo ']);';
?>
</script>

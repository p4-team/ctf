<?php
include 'common.php';

if(isset($_POST['submit']) && isset($_POST['width']) && isset($_POST['height'])) {
    $width = (int)$_POST['width'];
    $height = (int)$_POST['height'];
    if($width <= 0 || $width > MAX_IM_SIZE) {
        fatal('Invalid width');
    } else if($height <= 0 || $height > MAX_IM_SIZE) {
        fatal('Invalid height');
    }

    $im = imagecreatetruecolor($width, $height);
    if(!$im) {
        fatal('Failed to create image.');
    }

    $bgcolor = imagecolorallocate($im, 255, 255, 255);
    imagefill($im, 0, 0, $bgcolor);
    imagetruecolortopalette($im, false, 256);
    imagesavealpha($im, false);

    $imagekey = create_image_key();
    save_image($im, $imagekey);
    imagedestroy($im);

    header("Location: ?op=edit&imagekey=$imagekey");
} else {
?>
<div class="article">
    <h2>Create your new pixel art!</h2>
    <form action="?op=new" method="POST">
        <label for="width">Image width (max <?=MAX_IM_SIZE;?>):</label>
        <input type="number" id="width" name="width" value="<?=MAX_IM_SIZE;?>" min="1" max="<?=MAX_IM_SIZE;?>" />
        <br />
        <label for="height">Image height (max <?=MAX_IM_SIZE;?>):</label>
        <input type="number" id="height" name="height" value="<?=MAX_IM_SIZE;?>" min="1" max="<?=MAX_IM_SIZE;?>" />
        <br />
        <input type="submit" name="submit" value="Create!" />
    </form>
</div><?php
}
?>
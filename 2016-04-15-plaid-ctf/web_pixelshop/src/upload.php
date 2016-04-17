<?php
include 'common.php';

if(isset($_POST['submit']) && isset($_FILES['image'])) {
    $fn = $_FILES['image']['tmp_name'];

    if(!is_uploaded_file($fn)) {
        fatal('uploaded file corrupted');
    }

    $iminfo = getimagesize($fn);
    if(!$iminfo) {
        fatal('input was not an image');
    }
    if($iminfo[0] > MAX_IM_SIZE || $iminfo[1] > MAX_IM_SIZE) {
        fatal('image too big');
    }

    $im = imagecreatefromstring(file_get_contents($fn));
    if(!$im) {
        fatal('could not load your image');
    }

    imagetruecolortopalette($im, false, 256);
    imagesavealpha($im, false);

    $imagekey = create_image_key();
    save_image($im, $imagekey);
    imagedestroy($im);

    header("Location: ?op=edit&imagekey=$imagekey");
} else {
?>
<div class="article">
    <h2>Upload your own pixel art</h2>
    <form enctype="multipart/form-data" action="?op=upload" method="POST">
        <label for="image">Image file (max <?=MAX_IM_SIZE;?>x<?=MAX_IM_SIZE;?>): </label>
        <input type="file" id="image" name="image" />
        <br />
        <input type="submit" name="submit" value="Upload!" />
    </form>
</div><?php
}
?>
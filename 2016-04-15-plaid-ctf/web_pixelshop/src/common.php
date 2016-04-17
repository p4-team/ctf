<?php
/* Stop hackers. */
if(!defined('FROM_INDEX')) die();

define('MAX_IM_SIZE', 32);

function create_image_key() {
    return sha1($_SERVER['REMOTE_ADDR'] . $_SERVER['HTTP_USER_AGENT'] . time() . mt_rand());
}

function save_image($im, $imagekey) {
    if(1 !== preg_match('/[0-9a-f]{40}/', $imagekey)) {
        fatal('Invalid image key.');
    }

    if(!imagepng($im, "uploads/{$imagekey}.png")) {
        fatal('Failed to save image.');
    }
}

function load_image($imagekey) {
    if(1 !== preg_match('/[0-9a-f]{40}/', $imagekey)) {
        fatal('Invalid image key.');
    }

    $im = imagecreatefrompng("uploads/{$imagekey}.png");
    if(!$im) {
        fatal('Failed to load image.');
    }
    return $im;
}
?>
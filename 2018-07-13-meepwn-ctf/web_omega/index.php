<?php
ob_start();
session_start();
?>
<html>
<style type="text/css">* {cursor: url(assets/maplcursor.cur), auto !important;}</style>
<head>
  <link rel="stylesheet" href="assets/omega_sector.css">
  <link rel="stylesheet" href="assets/tsu_effect.css">
</head>

<?php

ini_set("display_errors", 0);
include('secret.php');

$remote=$_SERVER['REQUEST_URI'];

if(strpos(urldecode($remote),'..'))
{
mapl_die();
}

if(!parse_url($remote, PHP_URL_HOST))
{
    $remote='http://'.$_SERVER['REMOTE_ADDR'].$_SERVER['REQUEST_URI'];
}
$whoareyou=parse_url($remote, PHP_URL_HOST);


if($whoareyou==="alien.somewhere.meepwn.team")
{
    if(!isset($_GET['alien']))
    {
        $wrong = <<<EOF
<h2 id="intro" class="neon">You will be driven to hidden-street place in omega sector which is only for alien! Please verify your credentials first to get into the taxi!</h2>
<h1 id="main" class="shadow">Are You ALIEN??</h1>
<form id="main">
    <button type="submit" class="button-success" name="alien" value="Yes">Yes</button>
    <button type="submit" class="button-error" name="alien" value="No">No</button>
</form>
<img src="assets/taxi.png" id="taxi" width="15%" height="20%" />
EOF;
        echo $wrong;
    }
    if(isset($_GET['alien']) and !empty($_GET['alien']))
    {
         if($_GET['alien']==='@!#$@!@@')
        {
            $_SESSION['auth']=hash('sha256', 'alien'.$salt);
            exit(header( "Location: alien_sector.php" ));
        }
        else
        {
            mapl_die();
        }
    }

}
elseif($whoareyou==="human.ludibrium.meepwn.team")
{
    
    if(!isset($_GET['human']))
    {
        echo "";
        $wrong = <<<EOF
<h2 id="intro" class="neon">hellu human, welcome to omega sector, please verify your credentials to get into the taxi!</h2>
<h1 id="main" class="shadow">Are You Human?</h1>
<form id="main">
    <button type="submit" class="button-success" name="human" value="Yes">Yes</button>
    <button type="submit" class="button-error" name="human" value="No">No</button>
</form>
<img src="assets/taxi.png" id="taxi" width="15%" height="20%" />
EOF;
        echo $wrong;
    }
    if(isset($_GET['human']) and !empty($_GET['human']))
    {
         if($_GET['human']==='Yes')
        {
            $_SESSION['auth']=hash('sha256', 'human'.$salt);
            exit(header( "Location: omega_sector.php" ));
        }
        else
        {
            mapl_die();
        }
    }

}
else
{
    echo '<h2 id="intro" class="neon">Seems like you are not belongs to this place, please comeback to ludibrium!</h2>';
    echo '<img src="assets/map.jpg" id="taxi" width="55%" height="55%" />';
    if(isset($_GET['is_debug']) and !empty($_GET['is_debug']) and $_GET['is_debug']==="1")
    {
        show_source(__FILE__);
    }
}

?>
<body background="assets/background.jpg" class="cenback">
</body>
<!-- is_debug=1 -->
<!-- All images/medias credit goes to nexon, wizet -->
</html>
<?php ob_end_flush(); ?> 
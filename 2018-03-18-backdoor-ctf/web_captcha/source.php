<?php
session_start();

function get_question(){
	$answer = array();
	foreach(file("xxxxxxxxx") as $line) {
   		array_push($answer, trim($line));
	}
	$random_index = rand(0, 999);
	$question = file_get_contents("xxxxxxxx/$random_index");
	$_SESSION['quesans'] = $answer[$random_index];
	return $question;
}

function bad_hacking_penalty(){
	$_SESSION['count'] = 0;
}

function handle_invalid_captcha_ans(){
	$_SESSION['count'] = 0;
}

function is_clean($input){
	if (preg_match("/SESSION/i", $input)){//no seesion variable alteration
		bad_hacking_penalty();
		return false;
	}
	if (preg_match('/(base64_|eval|system|shell_|exec|php_)/i', $input)){//no coomand injection 
		bad_hacking_penalty();
		return false;
	}
	if (preg_match('/(file|echo|die|print)/i', $input)){//no file access
		bad_hacking_penalty();
		return false;
	}
	if (preg_match("/(or|\|)/", $input)){//Be brave use AND
		bad_hacking_penalty();
		return false;
	}
	if (preg_match('/(flag)/i', $input)){//don't take shortcuts
		bad_hacking_penalty();
		return false;
	}
	//clean input
	return true;
}

function random_string(){
	$captcha_file = "xxxxxxxx";
	$random_index = rand(0, 999);
	$i = 1;
	foreach(file($captcha_file) as $line) {
   		if ($i == $random_index) return $line;
   		$i++;
	}
}

//current captcha to be verified against user input
$cur_captcha = $_SESSION['captcha'];
//set captcha for next try
$next_captcha = rtrim(random_string());
$_SESSION['captcha'] = $next_captcha;
$captcha_url = "xxxxxxxxx" . md5('xxxxxxxxxxxx' . $next_captcha);

$invalid_ans = 0;
$invalid_captcha = 0;
if (isset($_SESSION['count']) && isset($_POST['captcha']) && $_POST['captcha'] != ''){
	$user_captcha = $_POST['captcha'];
	if($cur_captcha === $user_captcha){
		$user_ans = $_POST['answer'];
		$real_ans = $_SESSION['quesans'];
			if (is_clean($user_ans)){
				(assert("'$real_ans' === '$user_ans'") and $_SESSION['count'] +=1) or (handle_invalid_captcha_ans() or $invalid_ans = 1);

			}else{
				die('Detected hacking attempt');
			}
	}else{
		handle_invalid_captcha_ans();
		$invalid_captcha = 1;
		}
}else{
	handle_invalid_captcha_ans();
}


if (!isset($_SESSION['count'])){
	$_SESSION['count'] = 0;
}

?>

<html>
<head>
	<title></title>
</head>
<body>
<div name="ques">
Can y0u print something out of this brain-fucking c0de?<br>
<?php echo htmlspecialchars(get_question());?>
</div>
<form method="post" action="index.php">
	Answer: <input type="text" placeholder="Answer the question" name="answer"> <br><br>
	<audio controls>
  		<source src=<?php echo $captcha_url;?> type="audio/mpeg">
	</audio><br>
	Captcha: <input type="text" placeholder="Enter the captcha " name="captcha">
	<button type="submit">Submit</button>
</form>
<?php
 if ($_SESSION['count'] == 0){
 	echo "e.g Type '" . $next_captcha ."' for the given captcha";
 }
 if ($_SESSION['count'] >= 500 ){
 	include 'xxxxxxxxxxxxxx';
 	echo $random_flag_name;
 }else{
 	echo '<br>You\'ve made ' . ($_SESSION['count']) . ' correct answers';
 }
 if($invalid_ans){
 	echo '<br><b>Wrong Answer</b>';
 }else if($invalid_captcha){
 	echo '<br><b>Wrong Captcha</b>';
 }
?>

</body>
</html>
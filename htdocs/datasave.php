<?php

// create short variable names

$notice = $_POST['notice'];

$DOCUMENT_ROOT = $_SERVER['DOCUMENT_ROOT'];

?>
<!DOCTYPE html>
<html >

<head>
<meta charset="UTF-8"/>
<title> 공지사항 저장 </title>

</head>

<body>

<h1>공지사항 저장 결과</h1>

<?php

 

echo "<p>입력한 공지사항 내용 : ".$notice."</p>";

 

$outputstring = $notice;


$fp = fopen("$DOCUMENT_ROOT/Annc/notification.txt", 'w');

 

flock($fp, LOCK_EX);

if (!$fp) {

echo "<p>공지사항 저장 실패. 재시도하세요.</p></body></html>";

exit;

}


fwrite($fp, $outputstring, strlen($outputstring));

flock($fp, LOCK_UN);

fclose($fp);

echo "<p>공지사항이 성공적으로 저장되었습니다.</p>";

?>
<a href="notice.html">공지사항 다시 쓰기</a>
<a href="index.html">메인 화면</a>
</body>

</html>
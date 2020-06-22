<?php
$result = "";

$t = getdate();
$y=$t['year'];
$m=$t['mon'];
$d=$t['mday'];



$fileURI = "C:/Bitnami\wampstack-7.4.6-1/apache2/htdocs/Logs/".$y."-".$m."-".$d.".txt";
$datas = @file($fileURI) or $result = "파일을 읽을 수 없습니다.";
if ($datas != null){
$i=count($datas);
$result = $datas[$i-1];

}
?>
<!DOCTYPE html>
<html lang="ko">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>현재 실내 상태 보기</title>
</head>
<body>
<h1>현재 실내 미세먼지 및 온습도</h1>
<p><?php echo $result; ?></p>
<a href="index.html">뒤로 가기</a>
</body>
</html>
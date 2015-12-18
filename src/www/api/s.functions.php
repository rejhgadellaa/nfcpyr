<?

// ---------------------------------------------------------------
// DATA

function getDataKeyByIdInData($id,$data,$key="id",$resDefault=-1) {
	if (!is_array($data)) { $data = array(); }
	if ($resDefault==-1) {
		$resDefault = count($data); // append
	}
	foreach($data as $k=>$v) {
		if ($v[$key] == $id) {
			return $k;
		}
	}
	return $resDefault;
}

function getDataByIdInData($id,$data,$key="id",$resDefault=array()) {
	if (!is_array($data)) { $data = array(); }
	foreach($data as $k=>$v) {
		if ($v[$key] == $id) {
			return $v;
		}
	}
	return $resDefault;
}

// ---------------------------------------------------------------
// RESPONSES

function ok($message,$result=array()) {
	global $usegz;
	$jsons = json_encode( array('ok'=>1, 'msg'=>$message, 'result'=>$result) );
	if ($usegz) {
		$jsons = gzencode(json_encode($json));
		header('Content-Encoding: gzip');
	}
	echo $jsons;
	die();
}

function error($message, $errcode=1) {
	global $usegz;
	$jsons =  json_encode( array('error'=>$errcode,'errormsg'=>$message) );
	if ($usegz) {
		$jsons = gzencode(json_encode($json));
		header('Content-Encoding: gzip');
	}
	echo $jsons;
	die();
}

// ---------------------------------------------------------------
// FILEIO

function rd($dir) {
	$filter = array(".","..","Thumbs.db");
	$od = @opendir($dir);
	while ($rd = @readdir($od)) {
		if (in_array($rd,$filter)) { continue; }
		$res[] = $rd;
	}
	return $res;
}

function fw($file,$data) {
	$fo = @fopen($file,"w");
	$fw = @fwrite($fo,$data);
	@fclose($fo);
	return $fw;
}

function fr($file) {
	$fo = @fopen($file,"r");
	$fr = @fread($fo,filesize($file));
	@fclose($fo);
	return $fr;
}

function fg($f) {

	$fo = @fopen($f, "r");
	if (!$fo) { @fclose($fo); return false; }
	while($fg = @fgets($fo)) { $buffer .= $fg; }
	@fclose($fo);
	if ($buffer) { return $buffer; }
	return false;
	/**/
	//return @file_get_contents($f);
}

?>
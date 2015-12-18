<?php

// Include config
require_once('s.config.php');
require_once('s.functions.php');

// Set header
header("Content-Type: application/json");
// header("Access-Control-Allow-Origin: *"); // TODO: Disable for security

// Get action
$action = $_GET["a"];
if (!$action) {
	echo json_encode( array('error'=>1,'errormsg'=>'Error: [api.php] ?a (action) not provided') );
	die();
}

// Get authtoken
$authkey = $_GET["authkey"];
if (!$authkey) {
	echo json_encode( array('error'=>1,'errormsg'=>'Error: [api.php] ?authkey not provided') );
	die();
}

// GZip..
$usegz = $_GET["gz"];

switch($action) {

    // -------------------------------
    // CHECK

    case "checkinout":
        // get vars
        $reader_id = $_GET["reader_id"];
        $username = $_GET["username"];
        $path_jsons = "data/data_{$authkey}.json";
        // check vars
        if (!$reader_id) { error("_GET[reader_id] not provided"); }
        if (!$username) { error("_GET[username] not provided"); }
        // get json
        $jsons = fr($path_jsons);
        if (!$jsons) { error("Could not read jsons"); }
        $json = json_decode($jsons,true);
        if (!$json) { error("Could not parse jsons"); }
        // do
        $checkedin = $json["checkins"][$reader_id][$username];
        $json["checkins"][$reader_id][$username] = !$checkedin;
        // write
        $jsons = json_encode($json);
        $fw = fw($path_jsons,$jsons);
        // ok
        ok("OK",$json["checkins"][$reader_id][$username]);
        break;

    case checkin:
        // get vars
        $reader_id = $_GET["reader_id"];
        $username = $_GET["username"];
        $path_jsons = "data/data_{$authkey}.json";
        // check vars
        if (!$reader_id) { error("_GET[reader_id] not provided"); }
        if (!$username) { error("_GET[username] not provided"); }
        // get json
        $jsons = fr($path_jsons);
        if (!$jsons) { error("Could not read jsons"); }
        $json = json_decode($jsons,true);
        if (!$json) { error("Could not parse jsons"); }
        // do
        $json["checkins"][$reader_id][$username] = true;
        // write
        $jsons = json_encode($json);
        $fw = fw($path_jsons,$jsons);
        // ok
        ok("OK",$json["checkins"][$reader_id][$username]);
        break;

    case checkout:
        // get vars
        $reader_id = $_GET["reader_id"];
        $username = $_GET["username"];
        $path_jsons = "data/data_{$authkey}.json";
        // check vars
        if (!$reader_id) { error("_GET[reader_id] not provided"); }
        if (!$username) { error("_GET[username] not provided"); }
        // get json
        $jsons = fr($path_jsons);
        if (!$jsons) { error("Could not read jsons"); }
        $json = json_decode($jsons,true);
        if (!$json) { error("Could not parse jsons"); }
        // do
        $json["checkins"][$reader_id][$username] = false;
        // write
        $jsons = json_encode($json);
        $fw = fw($path_jsons,$jsons);
        // ok
        ok("OK",$json["checkins"][$reader_id][$username]);
        break;

    // -------------------------------
    // USERS

    case "get_users":
        // get vars
        $path_jsons = "data/data_{$authkey}.json";
        // check vars
        // ..
        // check Authkey
        if (!file_exists($path_jsons)) {
            error("Invalid authkey",101);
        }
        // get json
        $jsons = fr($path_jsons);
        if (!$jsons) { $jsons = "{}"; } // fallback
        $json = json_decode($jsons,true);
        if (!$json) { error("Could not parse jsons"); }
        // do
        $result = $json["users"];
        if (!$result) { $result = array(); }
        // ok
        ok("OK",$result);
        break;

    case "add_users":
        // get vars
        $datas = urldecode($_GET["datas"]);
        $data = json_decode($datas,true);
        $path_jsons = "data/data_{$authkey}.json";
        // check vars
        if (!$datas) { error("_GET[datas] not provided"); }
        if (!$data) { error("Could not parse jsons datas"); }
        // check Authkey
        if (!file_exists($path_jsons)) {
            error("Invalid authkey",101);
        }
        // get json
        $jsons = fr($path_jsons);
        if (!$jsons) { $jsons = "{}"; } // fallback
        $json = json_decode($jsons,true);
        if (!$json) { error("Could not parse jsons"); }
        if (!$json["users"]) { $json["users"] = array(); }
        // do
        foreach ($data as $k => $userdata) {
            $username = $userdata["username"];
            $userKey = getDataKeyByIdInData($username,$json["users"],"username",-2);
            if ($userKey==-2) {
                // only add if not exists
                $json["users"][] = $userdata;
            }
        }
        // write
        $jsons = json_encode($json);
        $fw = fw($path_jsons,$jsons);
        // ok
        ok("OK",$json["users"]);
        break;

    // -------------------------------
    // READERS

    case "get_readers":
        // get vars
        $path_jsons = "data/data_{$authkey}.json";
        // check vars
        // ..
        // check Authkey
        if (!file_exists($path_jsons)) {
            error("Invalid authkey",101);
        }
        // get json
        $jsons = fr($path_jsons);
        if (!$jsons) { $jsons = "{}"; } // fallback
        $json = json_decode($jsons,true);
        if (!$json) { error("Could not parse jsons"); }
        // do
        $result = $json["readers"];
        if (!$result) { $result = array(); }
        // ok
        ok("OK",$result);
        break;

    case "update_reader":
        // get vars
		$reader_id = $_GET["reader_id"];
        // check vars
		if (!$reader_id) { error("_GET[reader_id] not provided"); }
		// continue in add_reader

	case "add_reader":
        // get vars
        $datas = urldecode($_GET["datas"]);
        $data = json_decode($datas,true);
        $path_jsons = "data/data_{$authkey}.json";
        // check vars
        if (!$datas) { error("_GET[datas] not provided"); }
        if (!$data) { error("Could not parse jsons datas"); }
        // check Authkey
        if (!file_exists($path_jsons)) {
            error("Invalid authkey",101);
        }
        // get json
        $jsons = fr($path_jsons);
        if (!$jsons) { $jsons = "{}"; } // fallback
        $json = json_decode($jsons,true);
        if (!$json) { error("Could not parse jsons"); }
        $readerKey = getDataKeyByIdInData($reader_id,$json["readers"]);
        $reader = $data;
        $json["readers"][$readerKey] = $reader;
        // write
        $jsons = json_encode($json);
        $fw = fw($path_jsons,$jsons);
        // ok
        ok("OK",$reader);
        break;

    // REGISTER READER
    case "register_reader_online":
        // get vars
        $reader_id = $_GET["reader_id"];
		$reader_local_ips = urldecode($_GET["reader_local_ips"]);
        $path_jsons = "data/data_{$authkey}.json";
        // check vars
        if (!$reader_id) { error("_GET[reader_id] not provided"); }
		if (!$reader_local_ips) { error("_GET[reader_local_ip] not provided"); }
        // check Authkey
        if (!file_exists($path_jsons)) {
            error("Invalid authkey",101);
        }
        // get json
        $jsons = fr($path_jsons);
        if (!$jsons) { error("Could not read jsons"); }
        $json = json_decode($jsons,true);
        if (!$json) { error("Could not parse jsons"); }
        // do
        $readerKey = getDataKeyByIdInData($reader_id,$json["readers"]);
        $reader = getDataByIdInData($reader_id,$json["readers"]);
        $reader["time_registered"] = time();
		$reader["ip_remote"] = $_SERVER['REMOTE_ADDR'];
		$reader["ips_local"] = json_decode($reader_local_ips,true);
        $json["readers"][$readerKey] = $reader;
        // write
        $jsons = json_encode($json);
        $fw = fw($path_jsons,$jsons);
        // ok
        ok("Reader registered: {$reader_id}", "OK");
        break;

    // -------------------------------
    // AUTH

	// GET_AUTHKEY
	case "get_authkey":
		// get vars
		$nfcpyr_id = $_GET["nfcpyr_id"];
		$nfcpyr_user = $_GET["nfcpyr_user"];
		$nfcpyr_pass = $_GET["nfcpyr_pass"];
        $path_auth_jsons = "data/data_authkeys.json";
        // get json
        $jsons = fr($path_auth_jsons);
        if (!$jsons) { $jsons = "[]"; }
        $json = json_decode($jsons,true);
		// do + result
		// -> find user + id
		foreach($json as $entry) {
			if ($entry["id"] == $nfcpyr_id
				&& $entry["user"] == $nfcpyr_user
				&& $entry["pass"] == $nfcpyr_pass
			) {
				ok("OK", $entry["authkey"]);
			}
		}
		error("Invalid credentials",102);
		die();

    // GET NEW AUTHKEY
    case "get_new_authkey":
        // get vars
		$nfcpyr_id = $_GET["nfcpyr_id"];
		$nfcpyr_user = $_GET["nfcpyr_user"];
		$nfcpyr_pass = $_GET["nfcpyr_pass"];
        $newauthkey = md5(uniqid());
        $path_jsons = "data/data_{$newauthkey}.json";
        // check vars
        if (!$nfcpyr_id) { error("_GET[nfcpyr_id] not provided"); }
        // make json
        $json = array();
        // do
        $json["nfcpyr_id"] = $nfcpyr_id;
        $json["readers"] = array();
        $json["checkins"] = array();
        // write
        $jsons = json_encode($json);
        $fw = fw($path_jsons,$jsons);
		// auth json..
		$path_auth_jsons = "data/data_authkeys.json";
        // check vars
        if (!$nfcpyr_id) { error("_GET[nfcpyr_id] not provided"); }
        if (!$nfcpyr_user) { error("_GET[nfcpyr_user] not provided"); }
        if (!$nfcpyr_pass) { error("_GET[nfcpyr_pass] not provided"); }
        // get json
        $jsons = fr($path_auth_jsons);
        if (!$jsons) { $jsons = "[]"; }
        $json = json_decode($jsons,true);
		// -> find user + id
		foreach($json as $entry) {
			if ($entry["id"] == $nfcpyr_id
				&& $entry["user"] == $nfcpyr_user
			) {
				error("Authkey for user and/or id already exists");
			}
		}
		// do
		$newentry = array();
		$newentry["id"] = $nfcpyr_id;
		$newentry["user"] = $nfcpyr_user;
		$newentry["pass"] = $nfcpyr_pass;
		$newentry["authkey"] = $newauthkey;
		$json[] = $newentry;
		// write
        $jsons = json_encode($json);
        $fw = fw($path_auth_jsons,$jsons);
        // ok
        ok("Authkey registered",$newauthkey);
        break;

    // -------------------------------
    // DEFAULT

    default:
        error("Action: $action: Illegal or not implemented");

}




?>
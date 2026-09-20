<?php
// PHP owns identity/session persistence. CLI commands deliberately use PHP sessions as the state store.
$root = $argv[1] ?? die("root\n"); $cmd=$argv[2] ?? '';
$sessionDir="$root/runtime/php-sessions"; @mkdir($sessionDir,0777,true); session_save_path($sessionDir);
if ($cmd==='new') { $user=$argv[3]??''; session_id(bin2hex(random_bytes(16))); session_start(); $_SESSION['user']=$user; session_write_close(); echo session_id(); exit(0); }
if ($cmd==='who') { $sid=$argv[3]??''; session_id($sid); session_start(); echo $_SESSION['user']??''; session_write_close(); exit(0); }
if ($cmd==='logout') { $sid=$argv[3]??''; session_id($sid); session_start(); $_SESSION=[]; session_destroy(); echo 'OK'; exit(0); }
if ($cmd==='read') { $sid=$argv[3]??''; $thread=$argv[4]??''; session_id($sid); session_start(); $_SESSION['read'][$thread]=time(); session_write_close(); echo "OK"; exit(0); }
exit(2);

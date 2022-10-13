let Oldone = '</style>'
let Newone = 'div.is_mb {visibility:hidden!important}';
let body = $response.body
.replace(Oldone, Newone);
$done({body});

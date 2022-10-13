let Oldone = '</style>'
let Newone = 'div.is_mb {display:block!important}';
let body = $response.body
.replace(Oldone, Newone);
$done({body});

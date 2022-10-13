let Oldone = '</style>'
let Newone = 'div.content {visibility:hidden!important}';
let body = $response.body
.replace(Oldone, Newone);
$done({body});

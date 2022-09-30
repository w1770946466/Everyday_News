let Oldone = '</style>'
let Newone = '#div.content{display:none!important}';
let body = $response.body
.replace(Oldone, Newone);
$done({body});

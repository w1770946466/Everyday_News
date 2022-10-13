let Oldone = '</style>'
let Newone = 'a#634fb69856b6,a#6347fb6988496 {display:none!important}';
let body = $response.body
.replace(Oldone, Newone);
$done({body});

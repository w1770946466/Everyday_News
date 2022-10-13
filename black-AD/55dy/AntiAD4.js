let Oldone = '</style>'
let Newone = 'img#634fb6988497,img#6347fb69856b7 {display:none!important}';
let body = $response.body
.replace(Oldone, Newone);
$done({body});

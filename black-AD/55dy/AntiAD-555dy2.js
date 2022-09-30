let Oldone = '</style>'
let Newone = 'a[href="https://75655128.com:9999"]{display:none!important}';
let body = $response.body
.replace(Oldone, Newone);
$done({body});

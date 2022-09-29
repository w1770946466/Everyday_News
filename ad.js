let Oldone = '</style>'
let Newone = 'a[href="https://tz.kefuyuming.vip/3663.html"]{display:none!important}</style>';
let body = $response.body
.replace(Oldone, Newone);
$done({body});

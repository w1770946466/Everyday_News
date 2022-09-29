let Oldone = '</style>'
let Newone = 'a[href="https://www.87604411.com:9999/?channelCode=007"]{display:none!important}\ra[href="https://tz.kefuyuming.vip/3663.html"]{display:none!important}</style>';
let body = $response.body
.replace(Oldone, Newone);
$done({body});

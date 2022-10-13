let Oldone = '</style>'
let Newone = 'a[href="https://www.03482072.com:9999/?channelCode=007"],a[href="https://50935410.com/?channelCode=838"] {display:none!important}';
let body = $response.body
.replace(Oldone, Newone);
$done({body});

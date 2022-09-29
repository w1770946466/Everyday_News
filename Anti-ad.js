let rHead = '<head>'
let newStyle = '<head><link rel=\"stylesheet\" href=\"https://limbopro.com/CSS/baidu.css\" type=\"text/css\">'
var rBody = '</body>'
var newJavaScript = '<script type="text/javascript" async="async" src="//limbopro.com/Adguard/baidu.js"></script>'
let body = $response.body
    .replace(rHead, newStyle)
    .replace(rBody, newJavaScript);
$done({ body });

let ele = '<head>';
let eleReplace = '<head><link rel="stylesheet" href="https://raw.githubusercontent.com/w1770946466/Everyday_News/main/black-AD/55dy/AntiAD-555dy.css" type="text/css" /><script type="text/javascript" async="async" src="https://raw.githubusercontent.com/w1770946466/Everyday_News/main/black-AD/55dy/AntiAD-555dy.js"></script>'
let body = $response.body
    .replace(ele, eleReplace)
$done({ body });

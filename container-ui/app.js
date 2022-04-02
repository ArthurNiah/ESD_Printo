var http = require('http');
var fs = require('fs');
var formidable= require('formidable');

http.createServer(function (req, res) {
if (req.url == '/home') {
    res.writeHead(200, {'Content-Type': 'text/html'});
    var html= fs.readFileSync('./home.html');
    res.write(html);
    return res.end();

} 

else if (req.url == '/requestor_login'){
    res.writeHead(200, {'Content-Type': 'text/html'});
    var html= fs.readFileSync('./requestor_login.html');
    res.write(html);
    return res.end();
}

else if (req.url == '/requestor_signup'){
    res.writeHead(200, {'Content-Type': 'text/html'});
    var html= fs.readFileSync('./requestor_signup.html');
    res.write(html);
    return res.end();
} 

else if (req.url == '/provider_login'){
    res.writeHead(200, {'Content-Type': 'text/html'});
    var html= fs.readFileSync('./provider_login.html');
    res.write(html);
    return res.end();
}

else if (req.url == '/provider_signup'){
    res.writeHead(200, {'Content-Type': 'text/html'});
    var html= fs.readFileSync('./provider_signup.html');
    res.write(html);
    return res.end();
}

else if (req.url == '/provider_home'){
    res.writeHead(200, {'Content-Type': 'text/html'});
    var html= fs.readFileSync('./provider_home.html');
    res.write(html);
    return res.end();
}

else if (req.url == '/requestor_home'){
    res.writeHead(200, {'Content-Type': 'text/html'});
    var html= fs.readFileSync('./requestor_home.html');
    res.write(html);
    return res.end();
}

else if (req.url == '/provider_signup_action'){
    var form = new formidable.IncomingForm();
    form.parse(req, function (err, fields, files) {
        console.log(fields);
    })
    res.end();
}

else if (req.url == '/requestor_signup_action'){
    var form = new formidable.IncomingForm();
    form.parse(req, function (err, fields, files) {
        console.log('fields', fields);
        
        info = JSON.stringify({
            'first_name': fields.first_name, 'last_name': fields.last_name,
            'username': fields.username, 'tele_id': fields.tele_id, 'chat_id': 2
        })

        const options = {
            hostname: 'localhost',
            port: 5005,
            path: '/register',
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            'Content-Length': info.length
            }
        }

        const req = http.request(options, res =>{
            console.log('statusCode:', res.StatusCode)
            console.log('headers:', res.headers)
            res.on('info', d => {
            process.stdout.write(d)
            })
        });

        req.on('error', error => {
            console.error(error)
        })
        
        req.write(info)


        var html= fs.readFileSync('./requestor_signup_action.html');
        res.write(html);
        res.end()
    

    })
}


}).listen(8081);



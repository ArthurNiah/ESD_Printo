const express= require('express')
const axios= require('axios')
const formidable= require('formidable')
const app= express()
var fs = require('fs');

app.use(express.json())

app.use(express.urlencoded())
app.use(express.static(__dirname+'/public'));

app.get('/home', (req, res)=>{
    // res.sendFile(__dirname + '/requestor_login.html')
    res.writeHead(200, {'Content-Type': 'text/html'});
    var dir= "./home.html";
    // console.log(dir)
    var html= fs.readFileSync(dir);
    res.write(html);
    return res.end();
})

app.get('/requestor_login', (req, res)=>{
    // res.sendFile(__dirname + '/requestor_login.html')
    res.writeHead(200, {'Content-Type': 'text/html'});
    var html= fs.readFileSync('./requestor_login.html');
    res.write(html);
    return res.end();
})

app.get('/requestor_signup', (req, res)=>{
    // res.sendFile(__dirname + '/requestor_login.html')
    res.writeHead(200, {'Content-Type': 'text/html'});
    var html= fs.readFileSync('./requestor_signup.html');
    res.write(html);
    return res.end();
})

app.post('/requestor_login_action', (req, res)=>{
    console.log(req.body)
    var username= req.body.username
    console.log(username)

    const getRequests = async() => {
        return await axios({
            url: 'http://requestor:5005/find_by_requestor_username/' + username
        })
    }
    
    (async()=>{
        const requests= await getRequests()
        console.log(requests.data)
        console.log(requests.data.data.requestor_id)
        requestor_id= requests.data.data.requestor_id
        first_name= requests.data.data.first_name
        res.redirect('/requestor_home' + '?requestor_id =' + requestor_id)
    })()

})

app.post('/requestor_signup_action', (req, res)=>{
    console.log(req.body)

    axios({
            method: 'post',
            url: 'http://requestor:5005/register',
            data: {'first_name': req.body.first_name, 'last_name': req.body.last_name, 
            'username': req.body.username, 'tele_id': req.body.tele_id, 'chat_id': req.body.chat_id
            }
        })  

    .then((response)=>{
        console.log(response)
    })

    res.writeHead(200, {'Content-Type': 'text/html'});
    var html= fs.readFileSync('./requestor_signup_action.html');
    res.write(html);
    return res.end();
})

app.get('/requestor_home', (req, res)=>{
    res.writeHead(200, {'Content-Type': 'text/html'});
    var html= fs.readFileSync('./requestor_home.html');
    res.write(html);
    return res.end();
})

app.get('/provider_login', (req, res)=>{
    // res.sendFile(__dirname + '/requestor_login.html')
    res.writeHead(200, {'Content-Type': 'text/html'});
    var html= fs.readFileSync('./provider_login.html');
    res.write(html);
    return res.end();
})

app.get('/provider_signup', (req, res)=>{
    // res.sendFile(__dirname + '/requestor_login.html')
    res.writeHead(200, {'Content-Type': 'text/html'});
    var html= fs.readFileSync('./provider_signup.html');
    res.write(html);
    return res.end();
})

app.post('/provider_login_action', (req, res)=>{
    console.log(req.body)
    var username= req.body.username
    console.log(username)
    const getRequests = async() => {
        return await axios({
            url: 'http://provider:5007/find_by_provider_username/' + username
        })
    }
    
    (async()=>{
        const requests= await getRequests()
        console.log('LOOK HERE', requests.data)
        provider_id= requests.data.data.provider_id
        res.redirect('/provider_home' + '?provider_id =' + provider_id)
    })() 


})

app.post('/provider_signup_action', (req, res)=>{

    axios({
            method: 'post',
            url: 'http://create_provider:5006/create_provider',
            data: {'first_name': req.body.first_name, 'last_name': req.body.last_name, 
            'username': req.body.username, 'tele_id': req.body.tele_id, 'chat_id': req.body.chat_id, 
            'location': req.body.location
            }
        })

    .then((response)=>{
        console.log(response)
    })

    res.writeHead(200, {'Content-Type': 'text/html'});
    var html= fs.readFileSync('./provider_signup_action.html');
    res.write(html);
    return res.end();
})

app.get('/provider_home', (req, res)=>{
    res.writeHead(200, {'Content-Type': 'text/html'});
    var html= fs.readFileSync('./provider_home.html');
    res.write(html);
    return res.end();
})

app.get('/fileuploadui', (req,res)=>{
    res.writeHead(200, {'Content-Type': 'text/html'});
    var html= fs.readFileSync('./request.html');
    res.write(html);
    return res.end();
})

app.post('/fileupload',(req,res)=>{
    console.log(req.body)
    var form= new formidable.IncomingForm();

    form.parse(req, function(err, fields, files){
        console.log(files)  
        file_name= files.filetoupload.originalFilename;
        mime_type= files.filetoupload.mimetype
        var info= JSON.stringify({
        'location': fields.location, 'requestor_id': fields.requestor_id, 'no_of_copies': fields.no_of_copies, 'color': fields.color, 'size': fields.size, 'single_or_double': fields.single_or_double, 
        'comments': fields.comments, 'file_name': file_name, 'mime_type': mime_type});
        
        console.log('info', info)

        axios({
            method: 'post',
            url: 'http://create_request:5001/create_request',
            data: {
                'location': fields.location, 'requestor_id': fields.requestor_id, 'no_of_copies': fields.no_of_copies, 'color': fields.color, 'size': fields.size, 'single_or_double': fields.single_or_double, 
                'comments': fields.comments, 'file_name': file_name, 'mime_type': mime_type}
        })

    
        .then((response)=>{
            console.log(response)
            var dir= __dirname + "/temp_files"
        console.log(dir, "LOOK HEREE!")
        if (!fs.existsSync(dir)){
        fs.mkdirSync(dir);
        }
        
        var oldpath = files.filetoupload.filepath;
        var newpath = dir + "/" + file_name;
        fs.rename(oldpath, newpath, function (err) {
        if (err) throw err;
        res.write('Your request has been posted!');
        res.end();
        })
    
    });

    res.redirect('/requestor_home' + '?requestor_id=' + fields.requestor_id)
    return res.end();
})

})
app.listen(3030, ()=>{
    console.log('Server started at http:localhost:3030')
})

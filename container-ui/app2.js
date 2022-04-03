const express= require('express')
const axios= require('axios')
const app= express()
var fs = require('fs');
app.use(express.json())

app.use(express.urlencoded())

app.use(express.static(__dirname+'/public'));

app.get('/home', (req, res)=>{
    // res.sendFile(__dirname + '/requestor_login.html')
    res.writeHead(200, {'Content-Type': 'text/html'});
    var html= fs.readFileSync('./home.html');
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

    const getRequests = async() => {
        return await axios({
            url: 'http://localhost:5005/find_by_requestor_username/' + username
        })
    }
    
    (async()=>{
        const requests= await getRequests()
        console.log(requests.data)
        console.log(requests.data.data.requestor_id)
        requestor_id= requests.data.data.requestor_id
        res.redirect('/requestor_home' + '?requestor_id =' + requestor_id)
    })()

})

app.post('/requestor_signup_action', (req, res)=>{
    console.log(req.body)

    axios({
            method: 'post',
            url: 'http://localhost:5005/register',
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
    // console.log(req.body)
    // var username= req.body.username

    // const getRequests = async() => {
    //     return await axios({
    //         url: 'http://localhost:5005/find_by_requestor_username/' + username
    //     })
    // }
    
    // (async()=>{
    //     const requests= await getRequests()
    //     console.log(requests.data)
    //     console.log(requests.data.data.requestor_id)
    //     requestor_id= requests.data.data.requestor_id
    //     res.redirect('/requestor_home' + '?requestor_id =' + requestor_id)
    // })()
    return res.end()

})

app.post('/provider_signup_action', (req, res)=>{
    console.log('AMONGUS', req.body)

    axios({
            method: 'post',
            url: 'http://localhost:5006/create_provider',
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

app.listen(3030, ()=>{
    console.log('Server started at http:localhost:3030')
})

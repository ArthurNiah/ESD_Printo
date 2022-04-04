var http = require('http');
var formidable = require('formidable');
var fs = require('fs');
const { serialize } = require('v8');
const { datacatalog } = require('googleapis/build/src/apis/datacatalog');

http.createServer(function (req, res) {
  if (req.url == '/fileupload') {
    var form = new formidable.IncomingForm();
    form.parse(req, function (err, fields, files) {
      console.log(files);
      console.log(fields)
      file_name= files.filetoupload.originalFilename;
      mime_type= files.filetoupload.mimetype
      var info= JSON.stringify({
          'location': fields.location, 'requestor_id': 2, 'no_of_copies': fields.no_of_copies, 'color': fields.color, 'size': fields.size, 'single_or_double': fields.single_or_double, 
          'comments': fields.comments, 'file_name': file_name, 'mime_type': mime_type

      });
      console.log(info)
      const options = {
        hostname: 'localhost',
        port: 5001,
        path: '/create_request',
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

      var dir= __dirname + "/temp_files"
      if (!fs.existsSync(dir)){
        fs.mkdirSync(dir);
      }
      
      var oldpath = files.filetoupload.filepath;
      var newpath = dir + "/" + file_name;
      fs.rename(oldpath, newpath, function (err) {
        if (err) throw err;
        res.write('Your request has been posted!');
        res.end();
      });
});

  } else if (req.url == '/fileuploadui'){
    res.writeHead(200, {'Content-Type': 'text/html'});
    var html= fs.readFileSync('./request.html');
    res.write(html);
    return res.end();
  }

}).listen(8080);


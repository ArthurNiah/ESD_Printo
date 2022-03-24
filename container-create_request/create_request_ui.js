var http = require('http');
var formidable = require('formidable');
var fs = require('fs');

http.createServer(function (req, res) {
  if (req.url == '/fileupload') {
    var form = new formidable.IncomingForm();
    form.parse(req, function (err, fields, files) {
      console.log(fields);
      file_name= files.filetoupload.originalFilename;
      console.log(file_name);
      var dir= __dirname + "/temp_files"
      if (!fs.existsSync(dir)){
        fs.mkdirSync(dir);
      }
      var oldpath = files.filetoupload.filepath;
      var newpath = dir + "/" + file_name;
      fs.rename(oldpath, newpath, function (err) {
        if (err) throw err;
        res.write('File uploaded and moved!');
        res.end();
      });
});

  } else {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write('<body>');
    res.write('<form action="fileupload" method="post" enctype="multipart/form-data">');
    res.write('<input type="text" name="test" id="test"><br>');
    res.write('<input type="file" name="filetoupload"><br>');
    res.write('<input type="submit">');
    res.write('</form>');
    res.write('</body>');
    return res.end();
  }

}).listen(8080);
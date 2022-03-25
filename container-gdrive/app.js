const { google } = require('googleapis');
const path = require('path');
const fs = require('fs');

const express = require('express');
const bodyParser = require("body-parser");
const app = express();
const PORT = 3000;

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const CLIENT_ID= '424859888376-hvknfsdtc9enfrf45ir85uelqm2flpih.apps.googleusercontent.com';
const CLIENT_SECRET= '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';
const REDIRECT_URI= 'https://developers.google.com/oauthplayground';

const REFRESH_TOKEN= '1//04gjUdg2qipG_CgYIARAAGAQSNwF-L9Ir5Bnw14xP-ZaB00tdDj3nOAbIxbeTXtCzlQGxNLCBPtrniqTaEJEMqfTYTt8FisPJOoY';

const oauth2Client = new google.auth.OAuth2(
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI
);

oauth2Client.setCredentials({refresh_token: REFRESH_TOKEN})

const drive= google.drive({
    version: 'v3',
    auth: oauth2Client
})


async function uploadFile(file_name){
    var dir= __dirname + "/temp_files";
    const filePath= path.join(dir, file_name);
    try{
        const response= await drive.files.create({
            requestBody: {
                name: file_name,
                MimeType: 'image/gif'
            },
            media: {
                mimeType: 'image/gif',
                body: fs.createReadStream(filePath)
            }
        });
        console.log(response.data);
    }
    catch(error){
    console.log(error.message)
    }
};


async function generatePublicURL(document_id){
    try{
        await drive.permissions.create({
            fileId: document_id,
            requestBody: {
                role:'reader',
                type:'anyone'
            }
        })
                
        const result = await drive.files.get({
            fileId: document_id,
            fields: 'webViewLink, webContentLink'
        })
        console.log(result.data);
    }
    catch (error){
        console.log(error.message)
    }
}

app.route('/get_document')
.get((req, res, next) => {
    res.send('GET request called');
    doc_id= req.body.doc_id
    generatePublicURL(doc_id)
})

app.route('/insert_document')
.post((req, res, next) => {
    res.send('POST request called');
    file_name= req.body.file_name
    uploadFile(file_name);
})

app.listen(PORT, function(err){
    if (err) console.log(err);
    console.log("Server listening on PORT", PORT);
});


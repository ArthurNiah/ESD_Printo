const { google } = require('googleapis');
const path = require('path');
const fs = require('fs');

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

const filePath= path.join(__dirname, 'popcat.gif')

async function uploadFile(){
    try{
        const response= await drive.files.create({
            requestBody: {
                name: 'popcat.gif',
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

//uploadFile();

async function generatePublicURL(){
    try{
        const fileId = '1pjesGTtP6OZvtid9x2fvXWCF-BPRWLFi';
        await drive.permissions.create({
            fileId: fileId,
            requestBody: {
                role:'reader',
                type:'anyone'
            }
        })

        const result = await drive.files.get({
            fileId: fileId,
            fields: 'webViewLink, webContentLink'
        })
        console.log(result.data);
    }
    catch (error){
        console.log(error.message)
    }
}

generatePublicURL()



const firebaseConfig = {
    apiKey: "AIzaSyC7yQVl6dBD-mSdBVbuzBQPZKH0l9xlmEo",
    authDomain: "uploader-x.firebaseapp.com",
    databaseURL: "https://uploader-x.firebaseio.com",
    projectId: "uploader-x",
    storageBucket: "uploader-x.appspot.com",
    messagingSenderId: "384994295110",
    appId: "1:384994295110:web:44cde3d349a828f85df947"
};
function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
       result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
 }
document.addEventListener('DOMContentLoaded', function() {
    const app = firebase.initializeApp(firebaseConfig);
    const db = app.database().ref('links/');
    var btn = document.getElementById('add');
    btn.addEventListener('click', function() {
        alert('hi')
        chrome.tabs.query({active: true, lastFocusedWindow: true},async (tabs) => {
            const x = await db.push({uid : makeid(10),url : tabs[0].url})
            alert('done')
        });
    }, false);
  }, false);
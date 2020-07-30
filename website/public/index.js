const firebaseConfig = {
    apiKey: "AIzaSyC7yQVl6dBD-mSdBVbuzBQPZKH0l9xlmEo",
    authDomain: "uploader-x.firebaseapp.com",
    databaseURL: "https://uploader-x.firebaseio.com",
    projectId: "uploader-x",
    storageBucket: "uploader-x.appspot.com",
    messagingSenderId: "384994295110",
    appId: "1:384994295110:web:44cde3d349a828f85df947"
};
const app = firebase.initializeApp(firebaseConfig);
const db = app.database()
const text = document.getElementById('data')
const links = db.ref('links/')

const remove = (x)=>{
    const e = links.child(x).remove().then(()=>{
        alert('Deleted !!!')
    }).catch((err) => {throw err})
}
links.on('value',(snap)=>{
    text.innerHTML = ""
    const data = snap.val()
    for(var key in data){
        //console.log(data[key]["url"])
        text.innerHTML = text.innerHTML + data[key]["url"]+`&nbsp;&nbsp; <button onclick="remove(this.id)" id="${key}"> Delete Link</button>` +"<br>"
    }
})
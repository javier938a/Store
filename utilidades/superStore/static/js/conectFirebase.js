  // Your web app's Firebase configuration
  var firebaseConfig = {
    apiKey: "AIzaSyAR9PUtdwzw0uBMLsWDXHxYtWTwc-2g9s4",
    authDomain: "superstore-8a.firebaseapp.com",
    databaseURL: "https://superstore-8a.firebaseio.com",
    projectId: "superstore-8a",
    storageBucket: "superstore-8a.appspot.com",
    messagingSenderId: "716148899925",
    appId: "1:716148899925:web:1eccc051bf03249485d4dc"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);

  let messaging = firebase.messaging();

  //primero tenemos que enlazar con el service worker
  navigator.serviceWorker
  .register('../serviceworker.js')
  .then(function(register){
    messaging.useServiceWorker(register);
    
    //solicitamos el permiso para recibir noificaciones del usuario
    messaging.requestPermission()
    .then(function(){
      console.log("El usuario ha aceptado recibir notificaciones");
      
      return messaging.getToken();//obteniendo el token de cada usuario
    })
    .then(function(token){
      console.log(token);
      //enviaremos el token hacia django para guardarlo en la db
      fetch('/superStore/guardar-token/',{
        method:'post',
        headers:{
          'content-type':'application/json',
          'accept':'application/json'
        },
        body:JSON.stringify({
          'token':token
        })
      }).then(function(resultado){
        console.log("se ha guardado el token");
      }).catch(function(e){
        console.log("no se a podido guaradr el token");
      });
    })
    .catch(function(e){
      console.log("El usuario no ha aceptado recibir notificaciones");
    });
  });

  

  //programamos la recepcion de las notificaciones push
  messaging.onMessage(function(payload){
    let data = payload.notification
    console.log(data);
    let title = data.title;
    let options = {
      body:data.body,
      icon:data.icon
    };
    let mensaje = new Notification(title, options);
  });
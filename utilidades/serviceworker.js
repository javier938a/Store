//service worker consta de dos partes
//--instalacion:hace cache de todas las url que nostros creamos convenientes
//--interceptacion:que intercepta cada una de las peticiones para ver si tiene que responder desde el servidor en cado de que haya internet
// o de el cache en caso que el usuario este de manera offline o sin conexion
var CACHE_NAME='superStore-cache1';
var urlsToCache=[
    '/superStore/',
    '/static/css/estilos.css',
    '/static/css/inicio_estilos.css',
];

self.addEventListener('install',function(event){
    event.waitUntil(
        caches.open(CACHE_NAME)
        .then(function(cache){
            console.log('Opened cache');
            return cache.addAll(urlsToCache);
        })
    );
});

self.addEventListener('fecth', function(event){
    event.respondWith(
        fetch(event.request)
        .then(function(result){
            return caches.open(CACHE_NAME)
            .then(function(c){
                c.puth(event.request.url, result.clone())
                return result;
            })
            .catch(function(e){
                return caches.match(event.request)
            })
        })
    );
});

//codigo para notificaciones push
importScripts('https://www.gstatic.com/firebasejs/7.17.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/7.17.1/firebase-messaging.js');

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
  messaging.setBackgroundMessageHandler(function(payload){
    let title = payload.title;
    let options = {
      body:'Se ha agregado nuevo producto'+payload.body,
      icon:payload.icon
    };
    self.registration.showNotification(title,options);
  });
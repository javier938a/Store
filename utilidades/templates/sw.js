self.addEventListener('push',function(event){
    const eventInfo = event.data.text();
    const data = JSON.parse(eventInfo);
    const head = data.head || 'Nuevo seguidor';
    const body = data.body || 'Este es un contenido predeterminado no hay notificaciones';

    event.waitUntil(
        self.registration.showNotification(head, {
            body: body,
            icon: 'https://i.imgur.com/MZM3K5w.png'
        })
    );
});
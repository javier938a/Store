$(document).ready(function(){
    url='ws://'+window.location.host+'/ws/notificacion/'+$("#id_mayorista").val()+'/';
    socket = new WebSocket(url);
    $("#btnSeguir").click(function(evt){
        evt.preventDefault();
        alert(url);
        socket.send(JSON.stringify({
            'message':'tienes un nuevo seguidor'
        }));
    });
    socket.onopen=function(e){
        alert("Conectado");
    }
    socket.onmessage=function(e){
        const data = JSON.parse(e.data)
        alert(data.message);
    }
});
$(document).ready(function(){
    //Socket a conectar
    url='ws://'+window.location.host+'/ws/notificacion/'+$("#id_mayorista").val()+'/';
    socket = new WebSocket(url);
    $("#send").click(function(evt){
        evt.preventDefault();
        //alert($("#mensaje").val());
        socket.send(JSON.stringify({
            'message':$("#mensaje").val()
        }));
        //sms_new = $("#mensaje").val();
        
        //$("#ver_sms").val(sms_new);
    });

    socket.onopen = function(evt){
        console.log("Conectando con el el socket a la espera de mensajes");
    }

    socket.onmessage = function(evt){
        const datos = JSON.parse(evt.data);
        $("#ver_sms").val(datos.message);

    }

    socket.onclose = function(evt){
        console.log("cerrado conexcion");
    }


    $(".contact").click(function(evt){
        evt.preventDefault();
        $("#sala_chat").css('display','block');//muetra la sala
    });
    $("#close").click(function(evt){
        evt.preventDefault();
        $("#sala_chat").css('display','none');//cierra la sala
    });




});
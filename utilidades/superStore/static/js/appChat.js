$(document).ready(function(){
    //Socket a conectar
    id = document.querySelector('meta[name="user"]').content;
    grupo = $("#id_mayorista").val()+'_Gr_';
    url='ws://'+window.location.host+'/ws/notificacion/'+grupo+'/';
    socket = new WebSocket(url);

    socket.onopen = function(evt){
        console.log("Conectando con el el socket a la espera de mensajes");
    }

    socket.onmessage = function(evt){
        const datos = JSON.parse(evt.data);
            $("#ver_sms").val($("#ver_sms").val()+'\n'+datos.message);     

        
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
        $("#mensaje").val('');
        $("#ver_sms").val('');
        $("#sala_chat").css('display','none');//cierra la sala
    });
  
    $("#send").on('click',function(evt){
        evt.preventDefault();
        socket.send(JSON.stringify({
            'message':$("#mensaje").val(),
        }));
        $("#mensaje").val('');
    });


});
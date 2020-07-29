
///importScripts('/static/js/csrf_scrip.js');
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$(document).ready(function(){
    $(".aniadir_favorito").submit(function(){
        boton = $("button",this)
        //alert("Holqqq");
        const csrftoken=getCookie('csrftoken');
        datos = {
            csrfmiddlewaretoken:csrftoken,
            'cliente_id':$("#cliente_id").val(),
        };
        //alert(datos.cliente_id);
        $.ajax({
            url:$(this).attr("action"),
            type:'GET',
            data:datos,
            dataType:'json',
            success:function(data){
                //alert(data.res);
                if(data.res==true){
                    //alert(boton.hasClass('btn-success'));
                    if(boton.hasClass('btn-success')==true){//verificando si el boton tiene btn-succes
                        boton.removeClass('btn-success');
                        boton.addClass('btn-primary');                           
                    }                    
                }else{
                    if(boton.hasClass('btn-primary')){//verificando si el boton esta en primary color
                        boton.removeClass('btn-primary');
                        boton.addClass('btn-success');                        
                    }
                }
            },
        });
        return false;
    });
    $("#categorias a.nav-link").hover(function(){
        active = $(this).hasClass("active");
        if(active==false){
            $(this).addClass("active");
        }else{
            $(this).removeClass("active");
        }
    });
   /* //reciviendo los socket
    var url = 'ws://'+window.location.host+'/ws/notificacion/'+$("#idprov").val()+'/';
    //alert(url);
    var socket = new WebSocket(url);
        socket.onopen = function(e){
            //alert("Conexion establecida!");
        }

        socket.onmessage = function(e){
            sms = JSON.parse(e.data);
            alert(sms.messaje);
        }
        socket.onclose = function(e){
            //alert("Se ha desconectado")
        }*/

        

});
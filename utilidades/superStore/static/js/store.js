
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
    $('.vDateField').datepicker({dateFormat: 'yy-mm-dd'});
    $.datepicker.setDefaults({
        showOn: "both",
        buttonImageOnly: true,
        buttonImage: "calendar.gif",
        buttonText: "Calendar"
      });
    $.datepicker.setDefaults( $.datepicker.regional['es'] );
    
    $("#categorias a.nav-link").hover(function(){
        active = $(this).hasClass("active");
        if(active==false){
            $(this).addClass("active");
        }else{
            $(this).removeClass("active");
        }
    });
   

    //listando los departamentos cuando el usuario seleccione un pais
    $("#paises").change(function(){
        $("#departamento").html('');
        $("#municipio").html('');
        const csrftoken = getCookie('csrftoken');
        id_pais = $(this).val();
        //alert(id_pais);
        url = '/superStore/depto/'+id_pais+''
        list_depto = '';
        $.ajax({
            type:'GET',
            url:url,
            data:{
                csrfmiddlewaretoken: csrftoken,
            },
            dataType:'json',
            success:function(data){
                departamentos = JSON.parse(data);//recividos los departamentos ahora es hora de listarlos
                console.log(departamentos);
                for(let depto in departamentos){
                    id = departamentos[depto].pk;
                    dep = departamentos[depto].fields.departamento;
                    iten = '<option value="'+id+'">'+dep+'</option>'
                    list_depto = list_depto+iten;
                }
                $("#departamento").append(list_depto);
            }
        });

    });
    $("#departamento").change(function(){
        $("#municipio").html('');
        const csrftoken = getCookie('csrftoken');
        id_depto = $(this).val();//obteniendo el id del departamento seleccionado
        url = '/superStore/depto/muni/'+id_depto+''
        //alert(url);
        mnp=''
        $.ajax({
            type:'GET',
            url:url,
            data:{
                csrfmiddlewaretoken: csrftoken,
            },
            dataType:'json',
            success:function(data){
                municipios = JSON.parse(data);
                console.log(municipios);
                for(let muni in municipios){
                    id = municipios[muni].pk;
                    munic = municipios[muni].fields.municipio;
                    item = '<option value="'+id+'">'+munic+'</option>';
                    mnp = mnp+item;
                }
                $("#municipio").append(mnp);
            }
        });
    });

    $("#municipio").change(function(){
        $("#barrioBcanton").html('');
        const csrftoken = getCookie('csrftoken');
        id_bc=$(this).val();
        url = 'depto/muni/barcant/'+id_bc+'';
        bacan='';
        $.ajax({
            type:'GET',
            url:url,
            data:{
                csrfmiddlewaretoken: csrftoken,                
            },
            dataType:'json',
            success:function(data){
                barrioBC = JSON.parse(data);
                console.log(barrioBC);
                for(let bc in barrioBC){
                    id = barrioBC[bc].pk;
                    b_c = barrioBC[bc].fields.barrio_canton;
                    iten = '<option value='+id+'>'+b_c+'</option>'
                    bacan = bacan + iten;
                }
                $("#barrioBcanton").append(bacan);
            }
        });
    });
    $("#salir_chat").on('click',function(evt){
        evt.preventDefault();
        //alert("Holaaa");
        $("#sala").css('display', 'none');
        $("#abrir_chat").css('display','block')
    });

    $("#abrir").on('click',function(evt){
        $("#usuario").html('');
        evt.preventDefault();
        console.log("Entro");
        //alert("Hola");
        $("#sala").css('display', 'block');
        $("#abrir_chat").css('display','none')
        let tipo_user = document.querySelector('meta[name="tipo_user"]').content;
        //alert(tipo_user);
        const csrftoken = getCookie('csrftoken');
        datos={
            csrfmiddlewaretoken: csrftoken,
        }    
        user_id=document.querySelector('meta[name="user_id"]').content;    
        if(tipo_user=="Cliente"){//listaria los vendedores
            let url = '/superStore/seguidores/sigues/'+user_id;
            //alert(url);
            $.ajax({
                type:"GET",
                url:url,
                data:datos,
                dataType:'json',
                success:function(data){
                    console.log(data);
                    for(i in data){
                        id = data[i].pk;
                        empresa=data[i].empresa;
                        console.log(id);
                        grupo=data[i].grupo;
                        ruta_img= data[i].foto_perfil;
                        item = '<div id="'+grupo+'">\
                                    <a class="chatear" href="#">\
                                        <div class="item-user">\
                                            <img src="/media/'+ruta_img+'" width="100px" height="100px" alt="">\
                                            <span>'+empresa+'</span>\
                                        </div>\
                                    </a>\
                                </div>';
                        $("#usuario").append(item);
                    }
                }
            });
        }else{
           let url = '/superStore/seguidores/seguidor/'+user_id;
           $.ajax({
               type:'GET',
               url:url,
               data:datos,
               dataType:'json',
               success:function(data){
                console.log(data);
                for(i in data){
                    id = data[i].pk;
                    cliente=data[i].cliente;
                    console.log(id);
                    grupo=data[i].grupo;
                    ruta_img = data[i].foto_perfil;
                    item = '<div id="'+grupo+'">\
                                <a class="chatear" href="#">\
                                    <div class="item-user">\
                                        <img src="/media/'+ruta_img+'" width="45px" height="45px" alt="">\
                                        <span>'+cliente+'</span>\
                                    </div>\
                                </a>\
                            </div>';                    
                    $("#usuario").append(item);
                }                  
               }
           }) 
        }
    });
    let n_chat=0;
    $(document).on('click','.close_chat', function(evt){
        $(".chat_privado").remove();
        n_chat = n_chat-1;
    });

    $(document).on('click','.chatear', function(evt){
        evt.preventDefault();
        //alert("Has dado click");
        n_chat++;
        alert(n_chat);
        chat = '<div id="chat_'+n_chat+'" class="chat_privado">\
                    <div class="chat_cabecera">\
                        <span>\
                            titulo\
                        </span>\
                        <a class="close_chat" href="#"><i class="far fa-times-circle"></i></a>\
                        <a class="minimize_chat" href="#"><i class="fas fa-window-minimize"></i></a>\
                    </div>\
                    <div class="chat_body">\
                        <div class="chat_vista">\
                            <div class="mensaje1">\
                                <div class="enca1">usuario 1</div>\
                                <div class="body1">\
                                    mensaje1\
                                </div>\
                            </div>\
                            <div class="mensaje2">\
                                <div class="enca2">usuario 2</div>\
                                <div class="body2">\
                                    Lorem ipsum dolor sit amet\
                                </div>\
                            </div>\
                        </div>\
                    </div>\
                    <div class="chat_sms">\
                        <form class="sendSms" action="" method="get">\
                            <textarea name="" id="" cols="18" rows="2">\
                            </textarea>\
                        </form>\
                    </div>\
                </div>';
            $("#chat-content").append(chat);

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
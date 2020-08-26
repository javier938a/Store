
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
                        //alert(grupo);
                        item = '<div>\
                                    <a id="op_'+grupo+'" class="chatear" href="'+empresa+'">\
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
                    //alert(grupo);
                    item = '<div>\
                                <a id="op_'+grupo+'" class="chatear" href="'+cliente+'">\
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
            //abriendo el socket
    //alert(url_chat);
    var socket = null; 
    var id_mensaje_cliente=0
    var id_mensaje_prove=0
    var n_chat=0;
    var posicion='';
    $(document).on('click','.chatear', function(evt){
        evt.preventDefault();
            n_chat=n_chat+1;
            alert(posicion);
        
        var url_chat = 'ws://'+window.location.host+'/ws/chat/'+$(this).attr('id').replace('op_','')+'/';
        socket = new WebSocket(url_chat);

        id=$(this).attr('id').replace('op_','');//obtengoel id que este caso seria el grupo al que corresponde el chat privado y le quito el prefijo op que no me sirve de nada
        socket.onopen = function(e){
            console.log("Iniciando coneccion con: "+id);
        }
        socket.onmessage = function(e){
            datos=JSON.parse(e.data);
            id_mensaje_cliente=datos.id_mensaje_cliente;
            id_mensaje_prove=datos.id_mensaje_prove;
            console.log('Mensaje cliente: '+id_mensaje_cliente+' Mensaje proveedor: '+id_mensaje_prove);
            
            if(datos.tipo_usuario=="Cliente"){
                mensaje1 = '<div class="contsms1">\
                                <div class="mensaje1">\
                                    <div class="enca1">'+datos.usuario+'</div>\
                                        <div class="body1">\
                                            '+datos.message+'\
                                        </div>\
                                </div>\
                                <div class="ladoIz"></div>\
                            </div>';
                                $('#view_chat_'+idchat+'').append(mensaje1);
            }else{
                mensaje2 = '<div class="contsms2">\
                                <div class="ladoDer"></div>\
                                <div class="mensaje2">\
                                    <div class="enca2">'+datos.usuario+'</div>\
                                        <div class="body2">\
                                            '+datos.message+'\
                                        </div>\
                                </div>\
                            </div>';
                            $('#view_chat_'+idchat+'').append(mensaje2);
            }     
            $('#view_chat_'+idchat+'').animate({scrollTop:1000000}, 1000000);      
        }
    
        socket.onclose = function(e){
            console.log("Terminando la coneccion con "+id);
        }

        idchat=$(this).attr('id').replace('op_','');
        cli_o_prove = $(this).attr('href');
        //alert(cli_o_prove);
        //alert(idchat);
 
        if(n_chat===1){
            posicion = 'pos-chat-1';
                
        }else if(n_chat===2){
            posicion = 'pos-chat-2';
        }else if(n_chat===3){
            posicion=' pos-chat-3';
        }else if(n_chat===4){
            posicion=' pos-chat-4';
        } 
  
        chat = '<div id="bz_'+idchat+'" class="chat_privado '+posicion+'">\
                    <div class="chat_cabecera">\
                        <span>\
                            '+cli_o_prove+'\
                        </span>\
                        <a id="cl_'+idchat+'" class="close_chat" href="#"><i class="far fa-times-circle"></i></a>\
                        <a class="minimize_chat" href="#"><i class="fas fa-window-minimize"></i></a>\
                    </div>\
                    <div id="vista_'+idchat+'" class="chat_body">\
                        <div id = "view_chat_'+idchat+'" class="chat_vista">\
                        \
                        </div>\
                    </div>\
                    <div class="chat_sms">\
                        <form id="form_'+idchat+'" class="sendSms" action="" method="get">\
                            <textarea id="text'+idchat+'" class="sms"  name="" id="" cols="18" rows="2"></textarea>\
                        </form>\
                    </div>\
                </div>';

        //recivir y cerrar socker

            $("#chat-content").append(chat);
    });


    $(document).on('keypress','.sendSms', function(e){
        //alert("Hola Mundo");
        if(e.which==13){
            idText = $(this).attr('id');
            texto = idText.replace('form_','#text')
            //alert($(texto).val());
            socket.send(JSON.stringify({
                'message':$(texto).val(),
                'id_mensaje_prove':id_mensaje_prove,
                'id_mensaje_cliente':id_mensaje_cliente,
            }));
           $(texto).val(''); 
                      
        }
    });
    $(document).on('click','.close_chat', function(evt){
        evt.preventDefault();
        n_chat=n_chat-1;//restando un numero cuando se cierre el chat

        alert(n_chat);
        id_bz = $(this).attr('id').replace('cl_','#bz_');

        if($(id_bz).hasClass('pos-chat-1')==true){
            posicion='pos-chat-1';
            n_chat=1;
            ////socket.onclose();
        }else if($(id_bz).hasClass('pos-chat-2')==true){
            posicion='pos-chat-2';
            n_chat=2;
        }else if($(id_bz).hasClass('pos-chat-3')==true){
            n_chat=3;
            posicion='pos-chat-3';
        }else if($(id_bz).hasClass('pos-chat-4')==true){
            n_chat=4;
            posicion='pos-chat-4';
        }

        $(id_bz).remove();
        //alert(id_bz);
        
    });


   /* //reciviendo los socket
    var url = 'ws://'+window.location.host+'/ws/chat/'+$("#idprov").val()+'/';
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
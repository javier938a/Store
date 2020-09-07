

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

function conversacion(message, id_mensaje_cliente, id_mensaje_prove,group,tipo_usuario){
        
    console.log('Mensaje cliente: '+id_mensaje_cliente+' Mensaje proveedor: '+id_mensaje_prove);
    if(tipo_usuario=="Cliente"){
        mensaje1 = '<div class="contsms1">\
                        <div class="mensaje1">\
                            <div class="enca1">'+datos.usuario+'</div>\
                                <div class="body1">\
                                    '+message+'\
                                </div>\
                        </div>\
                        <div class="ladoIz"></div>\
                    </div>';
                        $('#view_chat_'+group+'').append(mensaje1);
    }else{
        mensaje2 = '<div class="contsms2">\
                        <div class="ladoDer"></div>\
                        <div class="mensaje2">\
                            <div class="enca2">'+datos.usuario+'</div>\
                                <div class="body2">\
                                    '+message+'\
                                </div>\
                        </div>\
                    </div>';
                    $('#view_chat_'+group+'').append(mensaje2);
    }     
    $('#view_chat_'+group+'').animate({scrollTop:1000000}, 1000000);  
}

$(document).ready(function(){
    var user_meta = document.querySelector('meta[name="user"]');
    var conecciones = new Map();
    var posiciones = new Map();//asignara las posiciones asignadas
    var posicion='';
    if(user_meta!=null){
        user = user_meta.content;
        var url = 'ws://'+window.location.host+'/ws/noti/'+user+'/';
        var websocket = new WebSocket(url);

        websocket.onopen = function(e){
            console.log('conectado!!');
        }

        websocket.onmessage = function(e){
            datos = JSON.parse(e.data);
            grupo = datos.grupo;
            cli_o_prove='';
            usuario=datos.usuario;
            empresa = datos.empresa;
            //alert("usuario: "+usuario+" grupo: "+grupo+" empresa: "+empresa);
            tipo_user = document.querySelector('meta[name="tipo_user"]').content;
            if(tipo_user=="Cliente"){
                cli_o_prove = empresa;
            }else{
                cli_o_prove=usuario;
            }
            posicion = '';
            //alert(datos.grupo);
            if(conecciones.has(grupo)!=true){

                if(posiciones.has('pos1')!=true){
                    posicion = 'pos-chat-1';
                    posiciones.set('pos1', posicion);
                }else if(posiciones.has('pos2')!=true){
                    posicion = 'pos-chat-2';
                    posiciones.set('pos2',posicion);
                }else if(posiciones.has('pos3')!=true){
                    posicion = 'pos-chat-3';
                    posiciones.set('pos3',posicion);
                }else if(posiciones.has('pos4')!=true){
                    posicion = 'pos-chat-4';
                    posiciones.set('pos4',posicion);
                }
                chat = '<div id="bz_'+grupo+'" class="chat_privado '+posicion+'">\
                            <div class="chat_cabecera">\
                                <span>\
                                    '+cli_o_prove+'\
                                </span>\
                                <a id="cl_'+grupo+'" class="close_chat" href="#"><i class="far fa-times-circle"></i></a>\
                                <a id="min_'+grupo+'" class="min_chat" href="'+cli_o_prove+'/'+posicion+'"><i class="fas fa-window-minimize"></i></a>\
                            </div>\
                            <div id="vista_'+grupo+'" class="chat_body">\
                                <div id = "view_chat_'+grupo+'" class="chat_vista">\
                                    \
                                </div>\
                            </div>\
                            <div class="chat_sms">\
                                <form id="form_'+grupo+'" class="sendSms" action="" method="get">\
                                    <textarea id="text'+grupo+'" class="sms"  name="" id="" cols="18" rows="2"></textarea>\
                                    </form>\
                            </div>\
                        </div>';
                $("#chat-content").append(chat);//agregando la sala a la vista
                $('#bz_'+grupo).css('display','none');
                
                var url_chat = 'ws://'+window.location.host+'/ws/chat/'+grupo+'/';
                socket = new WebSocket(url_chat);
                conecciones.set(grupo, [usuario,socket,]);
                conecciones.get(grupo)[1].onopen = function(e){
                    console.log("Iniciando coneccion con: "+grupo);
                    
                }

                conecciones.get(grupo)[1].onmessage = function(e){
                    datos=JSON.parse(e.data);
                    id_mensaje_cliente=datos.id_mensaje_cliente;
                    id_mensaje_prove=datos.id_mensaje_prove;
                    group = datos.group;
                    $('#bz_'+grupo).css('display','block');
                    tipo_usuario=datos.tipo_usuario;
                    message = datos.message;
                    //llamando a la funcion de conversacion :)
                    conversacion(message,id_mensaje_cliente, id_mensaje_prove, group, tipo_usuario);
     
                    console.log(conecciones); 
                    console.log(posiciones);  
                }

                conecciones.get(grupo)[1].onclose = function(e){
                    console.log("Terminando la coneccion con "+grupo);
                }



            }else{
            
            }
            console.log('grupo: '+datos.grupo);
        }

        websocket.onclose = function(e){
            console.log('desconectando');
        }

    }
    
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
                        usuario = data[i].usuario;
                        console.log(id);
                        grupo=data[i].grupo;
                        ruta_img= data[i].foto_perfil;
                        //alert(usuario);
                        //alert(grupo);
                        item = '<div>\
                                    <a id="op_'+grupo+'" class="chatear" href="'+usuario+'/'+empresa+'">\
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
    var dic_pos = new Map();
    noti=null;
    $(document).on('click','.chatear', function(evt){
        evt.preventDefault();
        grupo = $(this).attr('id').replace('op_','');       
        user_href = $(this).attr('href');
        usuario='';
        cli_o_prove = '';
        if(user_href.indexOf('/')>0){
            cli_o_prove = user_href.substring(user_href.indexOf('/')+1,user_href.length);
            usuario = user_href.substring(0, user_href.indexOf('/'));
            //alert(usuario);
        }else{
            usuario = $(this).attr('href');
            cli_o_prove=usuario;
        } 
        url_noti = 'ws://'+window.location.host+'/ws/noti/'+usuario+'/';
        //alert(url_noti);
        var noti = new WebSocket(url_noti);

        noti.onopen = function(e){
            tipo_usuario = document.querySelector('meta[name="tipo_user"]').content;
            usuario=""
            if(tipo_usuario=="Proveedor"){
                usuario= document.querySelector('meta[name="user"]').content;
                empresa=document.querySelector('meta[name="empresa"]').content;
            }else{
                usuario=document.querySelector('meta[name="user"]').content;
                empresa=usuario;
            }

            noti.send(JSON.stringify({
                'grupo':grupo,
                'usuario':usuario,
                'empresa':empresa,
            }))
        }
        noti.onmessage = function(e){
            //alert(e.data);
        }
        noti.onclose = function(e){
            noti.close();
        }


        posicion = '';
        //alert('usuario: '+usuario);
        if(conecciones.has(grupo)!=true){
            n_chat=n_chat+1;
            if(posiciones.has('pos1')!=true){
                posicion = 'pos-chat-1';
                posiciones.set('pos1', posicion);
            }else if(posiciones.has('pos2')!=true){
                posicion = 'pos-chat-2';
                posiciones.set('pos2',posicion);
            }else if(posiciones.has('pos3')!=true){
                posicion = 'pos-chat-3';
                posiciones.set('pos3',posicion);
            }else if(posiciones.has('pos4')!=true){
                posicion = 'pos-chat-4';
                posiciones.set('pos4',posicion);
            }
            chat = '<div id="bz_'+grupo+'" class="chat_privado '+posicion+'">\
                        <div class="chat_cabecera">\
                            <span>\
                                '+cli_o_prove+'\
                            </span>\
                            <a id="cl_'+grupo+'" class="close_chat" href="#"><i class="far fa-times-circle"></i></a>\
                            <a id="min_'+grupo+'" class="min_chat" href="'+cli_o_prove+'/'+posicion+'"><i class="fas fa-window-minimize"></i></a>\
                        </div>\
                        <div id="vista_'+grupo+'" class="chat_body">\
                            <div id = "view_chat_'+grupo+'" class="chat_vista">\
                            \
                            </div>\
                        </div>\
                        <div class="chat_sms">\
                            <form id="form_'+grupo+'" class="sendSms" action="" method="get">\
                                <textarea id="text'+grupo+'" class="sms"  name="" id="" cols="18" rows="2"></textarea>\
                            </form>\
                        </div>\
                    </div>';
    
                $("#chat-content").append(chat);
                get_bandeja_entrada_cliente(grupo);
                //cargando el lista del chat
            //alert(posicion);
            var url_chat = 'ws://'+window.location.host+'/ws/chat/'+grupo+'/';
            socket = new WebSocket(url_chat);

            conecciones.set(grupo, [usuario,socket,]);
    
    
            id=$(this).attr('id').replace('op_','');//obtengoel id que este caso seria el grupo al que corresponde el chat privado y le quito el prefijo op que no me sirve de nada
            
            conecciones.get(grupo)[1].onopen = function(e){
                console.log("Iniciando coneccion con: "+id);
            }
            conecciones.get(grupo)[1].onmessage = function(e){
                datos=JSON.parse(e.data);
                id_mensaje_cliente=datos.id_mensaje_cliente;
                id_mensaje_prove=datos.id_mensaje_prove;
                group = datos.group;
                tipo_usuario=datos.tipo_usuario;
                message = datos.message;
                //llamando a la funcion de conversacion :)
                conversacion(message,id_mensaje_cliente, id_mensaje_prove, group, tipo_usuario);
 
                console.log(conecciones); 
                console.log(posiciones);  
            }
        
            conecciones.get(grupo)[1].onclose = function(e){
                console.log("Terminando la coneccion con "+id);
            }
            
    
        }else{
            alert("Ya existe un chat asociado al grupo!!");
        }

            
    });

    function get_bandeja_entrada_cliente(grupo){
        const csrftoken= getCookie('csrftoken');
        url = '/superStore/bde_cliente/'+grupo+'';
        $.ajax({
            type:'GET',
            url:url,
            data:{
                csrfmiddlewaretoken:csrftoken,
            },
            dataType:'json',
            success:function(R){
                console.log("Entro aqui al primer ajax")
                //console.log(R[0]);
                for(var i in R){
                   //console.log(R[i]);
                    id=R[i].id;
                    mayorista=R[i].mayorista;
                    cliente=R[i].cliente;
                    mensaje=R[i].mensaje;
                    fecha=R[i].fecha;
                    grupo=R[i].grupo;
                    mensaje1 = '<div class="contsms1">\
                                    <div class="mensaje1">\
                                        <div class="enca1">'+cliente+'</div>\
                                        <div class="body1">\
                                            '+mensaje+'\
                                        </div>\
                                    </div>\
                                    <div class="ladoIz"></div>\
                                </div>';
                    $('#view_chat_'+grupo+'').append(mensaje1);
                    respuesta=R[i].respuesta;
                        console.log('respuesta: '+respuesta);
                        for(var res in respuesta){
                            console.log("Entro al for: "+res)
                            id=respuesta[res].id;
                            mayorista=respuesta[res].mayorista;
                            cliente=respuesta[res].cliente;
                            mensaje=respuesta[res].mensaje;
                            fecha=respuesta[res].fecha;
                            grupo=respuesta[res].grupo;
                            //alert(grupo);
                            mensaje2 = '<div class="contsms2">\
                                            <div class="ladoDer"></div>\
                                                <div class="mensaje2">\
                                                <div class="enca2">'+mayorista+'</div>\
                                                <div class="body2">\
                                                    '+mensaje+'\
                                                </div>\
                                            </div>\
                                        </div>';
                            $('#view_chat_'+grupo+'').append(mensaje2);
    
                        }                                             
                }
            }
        });
    }

    $(document).on('keypress','.sendSms', function(e){
        //alert("Hola Mundo");
        if(e.which==13){
            idText = $(this).attr('id');
            texto = idText.replace('form_','#text')
            grupo = idText.replace('form_','');
            //alert("Hola Mundo! "+grupo);
            //alert($(texto).val());
            conecciones.get(grupo)[1].send(JSON.stringify({
                'message':$(texto).val(),
                'group':grupo,
            }));

           $(texto).val(''); 
           //noti.close();          
        }else{
            //console.log(noti);
            if(noti!=undefined){
                console.log("hellow "+String.parse(noti));
                noti.close();
            }
            
        }
    });



    $(document).on('click','.close_chat', function(evt){
        evt.preventDefault();
        
        //alert(n_chat);
        grupo = $(this).attr('id').replace('cl_','');
        id_bz = $(this).attr('id').replace('cl_','#bz_');

        if($(id_bz).hasClass('pos-chat-1')==true){
            posiciones.delete('pos1');
            ////socket.onclose();
        }else if($(id_bz).hasClass('pos-chat-2')==true){
            posiciones.delete('pos2');
        }else if($(id_bz).hasClass('pos-chat-3')==true){
            posiciones.delete('pos3');
        }else if($(id_bz).hasClass('pos-chat-4')==true){
            posiciones.delete('pos4');
        }
        conecciones.get(grupo)[1].close();//eliminando el grupo...
        conecciones.delete(grupo);//eliminando objeto socket y usuario
        $(id_bz).remove();
        //alert(id_bz);
        
    });
    $(document).on('click','.min_chat', function(e){
        e.preventDefault();
        idMinChat = $(this).attr('id');
        grupo = idMinChat.replace('min_','');
        chat=idMinChat.replace('min_','#bz_');
        enlace = $(this).attr('href');
        name= enlace.substring(0, enlace.indexOf('/'));
        pos_chat=enlace.substring(enlace.indexOf('/')+1,enlace.length);
        pos_abrir='';
        switch(pos_chat){
            case 'pos-chat-1':
                pos_abrir='pos-mini-1';
                break;
            case 'pos-chat-2':
                pos_abrir='pos-mini-2';
                break;
            case 'pos-chat-3':
                pos_abrir='pos-mini-3';
                break;
            case 'pos-chat-4':
                pos_abrir='pos-mini-4';
                break;            
        }

        min_chat = '<div id="maxi_'+grupo+'" class="open_chat '+pos_abrir+'">\
                        <a href="#" id="max_'+grupo+'" class="max_chat">\
                                '+name+'\
                        </a>\
                        <a class="close_min" id="cl_min_'+grupo+'" href="#"><span><i class="far fa-times-circle"></i></span></a>\
                    </div>';    
        $('#chat-content').append(min_chat);

        $(chat).css('display','none');

    });

    $(document).on('click','.max_chat', function(e){
        e.preventDefault();
        idMaxChat = $(this).attr('id');
        max_btn = idMaxChat.replace('max_','#maxi_');
        chat=idMaxChat.replace('max_','#bz_');
        $(chat).css('display','block');
        $(max_btn).remove();

    });

    $(document).on('click','.close_min',function(e){
        e.preventDefault();
        idBotonClose = $(this).attr('id');
        grupo=idBotonClose.replace('cl_min_','');
        idChat = idBotonClose.replace('cl_min_','#bz_');//obteniendo el id del chat maximizado oculto
        idChatMin = idBotonClose.replace('cl_min_','#maxi_')//obteniendo el id del chat minimizado

        if($(idChat).hasClass('pos-chat-1')==true){
            posiciones.delete('pos1');
            
            ////socket.onclose();
        }else if($(idChat).hasClass('pos-chat-2')==true){
            posiciones.delete('pos2');
            
        }else if($(idChat).hasClass('pos-chat-3')==true){
            posiciones.delete('pos3');
            
        }else if($(idChat).hasClass('pos-chat-4')==true){
            posiciones.delete('pos4');
            
        }
        conecciones.get(grupo)[1].close();//cerrando la coneccion del grupo...
        conecciones.delete(grupo);//eliminando objeto socket y usuario
        $(idChat).remove();//eliminando el chat del Dom
        $(idChatMin).remove();//eliminando el boton de maximizar chat
    });








    /*------------------------------------------------------------*/
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
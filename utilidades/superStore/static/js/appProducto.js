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
    //Listando los comentarios del producto
    id_prod_meta = document.querySelector('meta[name="prod_id"]');
    id_prod = id_prod_meta.content;
    
    $.ajax({
        type:'GET',
        url:'/superStore/producto/comentario/listarComent/'+id_prod,
        dataType:'json',
        success:function(data){
                if(data.length==0){
                    $("#comentar").css('display','block');//si el tamaño de los comentarios son igual a cero significa que no hay ningun comentario y se habilita el editor para escribir
                }else if(data.length>0){//si es mayor que cero significa que hay comentarios que escribir
                    for(let i in data){
                        if(i!=0){//valida que la variable i sea diferente de cero ya que en la casilla numero cero esta la comprobacion si el comentario del usuario logueado
                            console.log(i);
                            var puntaje = data[i].puntaje;
                            punt=''
                            console.log(data[i]);

                            
                            stars=""
                            if(data[i].puntaje==1){
                               stars='★';
                            }else if(data[i].puntaje==2){
                                stars='★★';
                            }else if(data[i].puntaje==3){
                                stars = '★★★';
                            }else if(data[i].puntaje==4){
                                stars = '★★★★';
                            }else if(data[i].puntaje==5){
                                stars = '★★★★★';
                            }
            
                          
                            sms ='<div class="msj" id="c'+data[i].id+'">\
                                    <h5 id="titCo">'+data[i].cliente+'</h5>\
                                    <span id="stars" style="color: orange;" id="s'+data[i].id+'">'+stars+'</span>\
                                     <p id="par'+data[i].id+'">\
                                        '+data[i].comentario+'\
                                    </p>\
                                    <div id="op_coment">\
                                        <a class="del_coment" id="cc'+data[i].id+'" href="/superStore/producto/comentario/'+data[i].id+'">Eliminar</a>\
                                        <button id="ccc'+data[i].id+'" class="editar_coment">Editar</button>\
                                    </div>\
                                  </div>';

                            $("#comentarios").append(sms);
                        }
                    }
                }
                if(data[0].existe==false){//si no existe mostrara el campo para agregar el comentario..
                    $("#comentar").css('display','block');
                }
                


        }
    });

        //alert("Ya esta cargado");
        //Eliminando los comentarios
        $(document).on('click','.del_coment',function(evt){
            evt.preventDefault();
            var conf = confirm("¿Esta seguro que desea eliminar el comentario?");
            if(conf==true){
                 url = $(this).attr('href');//obtiene el valor de href que es el url de cada comentario
                 btn = $(this).attr('id');//obtiene el valor del id del boton eliminar que "c + cid" que es el id de cada comentario
                 id_p = btn.substring(1,btn.length);//con substring eliminamos un "c" ya que en los p esta como "cid"
                 //alert(id_p);
                 $.ajax({
                     url:url,
                     type:'GET',
                     dataType:'json',
                     success:function(data){
                         if(data.res==true){//si se elimina el elemento 
                             $("#"+id_p).remove();//eliminamos el parrafo o el comentario de la lista en la pagina
                             $("#comentar").css('display','block');//mostramos para que de la opcion de comentar
                         }
                         
                     }
                 });
             }
        });
        ///editar comentario
        var ver = true;
        $(document).on('click', '.editar_coment', function(evt){
            evt.preventDefault();
            id = $(this).attr('id');
            idSub = id.substring(3,id.length);//obteniendo el id puro 
            idParrafo = id.substring(2,id.length)//deduciendo el id del parrafo 
            console.log('valor de ver; '+ver);
            if(ver===true){
                texto = $('#par'+idSub).text();//texto del comentario.
                $('#par'+idSub).html('');
                ver=false
                formedit = '<form class="comt" id="edit_com" action="/superStore/producto/comentario/editar_coment/'+idSub+'">\
                                <p class="clasificacion">\
                                    <input type="radio" name="puntaje" value="5" id="radio1">\
                                    <label for="radio1">★</label>\
                                    <input type="radio" name="puntaje" value="4" id="radio2">\
                                    <label for="radio2">★</label>\
                                    <input type="radio" name="puntaje" value="3" id="radio3">\
                                    <label for="radio3">★</label>\
                                    <input type="radio" name="puntaje" value="2" id="radio4">\
                                    <label for="radio4">★</label>\
                                    <input type="radio" name="puntaje" value="1" id="radio5" checked>\
                                    <label for="radio5">★</label>\
                                </p>\
                                <textarea name="coment" id="cmt" cols="100" rows="3">\
                                </textarea>\
                                <button class="btn btn-primary" type="submit">Comentar</button>\
                            </form>';
                $("#op_coment").css('display','none');//ocultando elementos
                $("#stars").css('display','none');
                $("#titCo").css('display','none');
                $('#'+idParrafo).append(formedit);//  agregando el formulario de edicion
                $("#cmt").append(texto);//agregando el texto del comentario anterior              
            }else{
                ver=true;
                $('#edit_com').remove();
            }
        });
        $(document).on('submit', "#edit_com", function(evt){
            evt.preventDefault();
            url = $(this).attr("action");
            const csrftoken = getCookie('csrftoken');
            id_prod_meta = document.querySelector('meta[name="prod_id"]');
            id_prod = id_prod_meta.content;//id del producto
            puntaje=$("input:radio[name=puntaje]:checked").val();
            comentario=document.getElementById('cmt').value.trim();
            $.ajax({
                type:'GET',
                url:url,
                data:{
                    csrfmiddlewaretoken:csrftoken,
                    'producto_id':id_prod,
                    'comentario':comentario,
                    'puntaje':puntaje,
                },
                success:function(data){
                    console.log(data[0].res);
                    if(data[0].res===true){
                        $("#edit_com").remove();
                        stars=""
                        if(data[1].puntaje==1){
                           stars='★';
                        }else if(data[1].puntaje==2){
                            stars='★★';
                        }else if(data[1].puntaje==3){
                            stars = '★★★';
                        }else if(data[1].puntaje==4){
                            stars = '★★★★';
                        }else if(data[1].puntaje==5){
                            stars = '★★★★★';
                        }

                        comenn = data[1].comentario; 
                        $("#s"+data[1].id).append(stars) ;
                        $("#par"+data[1].id).append(comenn);
                        $("#op_coment").css('display','block');//mostrando elementos elementos
                        $("#stars").css('display','block');
                        $("#titCo").css('display','block');
                    }
                }
            });
            
        });
    //alert(id_prod);
    $(".foto").hover(function(){
        var ubi = $(this).attr("src");
        //alert(ubi);
        $("#foto_producto").attr("src",ubi);
    })
    //formulario de comentario
    $("#comentar").submit(function(evt){//Enviando el formulario
        //alert($("#cmt").val());
        //Listando los comentarios del producto
        evt.preventDefault();
        const csrftoken = getCookie('csrftoken');
        id_prod_meta = document.querySelector('meta[name="prod_id"]');
        id_prod = id_prod_meta.content;
        datos={
            csrfmiddlewaretoken:csrftoken,
            'producto_id':id_prod,
            'coment':$("#cmt").val(),
            'puntaje':$("input:radio[name=puntaje]:checked").val()
        };
        $.ajax({
            type:'POST',
            url:$("#comentar").attr("action"),
            data:datos,
            dataType:"json",
            success:function(data){
                //verificando el puntaje para ver cuantas estrellas le corresponde a cada comentario
                stars=""
                if(data.puntaje==1){
                   stars='★';
                }else if(data.puntaje==2){
                    stars='★★';
                }else if(data.puntaje==3){
                    stars = '★★★';
                }else if(data.puntaje==4){
                    stars = '★★★★';
                }else if(data.puntaje==5){
                    stars = '★★★★★';
                }
                sms ='<div class="msj" id="c'+data.id+'">\
                        <h5 id="titCo">'+data.cliente+'</h5>\
                        <span id="stars" style="color: orange;" id="s'+data.id+'">'+stars+'</span>\
                        <p id="par'+data.id+'">\
                            '+data.comentario+'\
                        </p>\
                        <div id="op_coment">\
                            <a class="del_coment" id="cc'+data.id+'" href="/superStore/producto/comentario/'+data.id+'">Eliminar</a>\
                            <button id="ccc'+data.id+'" class="editar_coment">Editar</button>\
                        </div>\
                      </div>';
                //alert(parrafo);
                //datos = JSON.parse(data)
                //alert(data.id);
                //com=pp+'<br>'+data.comentario+'<br><a class="del_coment" id="cc'+data.id+'" href="/superStore/producto/comentario/'+data.id+' ">Eliminar</a>'
                //alert(sms);
                $("#comentarios").append(sms);
            
                $("#cmt").val('');//limpia el contenido del textview
                $("#comentar").css('display','none');
                //alert(comentario);
            }
        });     
    });
    //pestañas 
    $("#ver_perfil_tienda").click(function(evt){
        evt.preventDefault();
        if($("#ver_perfil_tienda").hasClass('active')==false){//verificando si existe la clase active
            $("#ver_perfil_tienda").addClass('active');
            $("#ver_detalle_producto").removeClass('active');
            $("#ver_tienda_prove").removeClass('active');
        }else{
            $("#ver_perfil_tienda").addClass('active');
        }
        $("#producto_detalle").css('display','none');//hace invisible el elemento producto detalle
        $("#perfil_tienda").css('display', 'block');//hace invisible el elemento tienda
        $("#ver_tienda").css('display','none');//ocultando el div de tienda
        //verificando si el cliente que ha ingresado es un seguidor del proveedor
        $.ajax({
            url:$("#ver_perfil_tienda").attr("href"),
            type:'GET',
            dataType:'json',
            success:function(data){
                //si el resultado es falso significa que no tiene amigos pero le agregara al boton el primary y mostrara el numero de seguidores
                if(data.res==false){
                    $("#btnSeguir").addClass('btn btn-primary');
                    $("#numero_amigos").html(data.numero_amigos);
                }else{//de lo contrario significa que tiene amigos y agregara el succes al boton y mostrara el numero de amigos 
                    $("#btnSeguir").addClass('btn btn-success');
                    $("#numero_amigos").html(data.numero_amigos);
                }
            }
        });
    });
    //al dar click en el boton seguir se agregara un nuevo seguidor al proveedor
    $("#btnSeguir").click(function(evt){
        evt.preventDefault();
        $.ajax({
            url:$("#btnSeguir").attr("href"),
            type:'GET',
            dataType:'json',
            success:function(data){
                if(data.res==true){
                    if($("#btnSeguir").hasClass("btn-primary")==true){//si el resultado da true se verifica si el boton tiene el color btn-primary si esta se elimina ese color y se agrega el success
                        $("#btnSeguir").removeClass("btn-primary");
                        $("#btnSeguir").addClass('btn-success');
                    }
                    $("#btnSeguir").addClass('btn btn-success');//si no esta primary se agrega succes y se actualiza el numero de amigos que se recibe del servidor
                    $("#numero_amigos").html(data.numero_amigos);
                }else{//si es falso el resultado significa que se elimino el seguidor
                    if($("#btnSeguir").hasClass('btn-success')==true){
                        $("#btnSeguir").removeClass("btn-success");
                        $("#btnSeguir").addClass('btn-primary');
                    }
                    $("#numero_amigos").html(data.numero_amigos);
                }
            }
        });
    });
    $("#ver_detalle_producto").click(function(evt){
        evt.preventDefault();
        if($("#ver_detalle_producto").hasClass('active')==false){
            $("#ver_detalle_producto").addClass('active');
            $("#ver_perfil_tienda").removeClass('active');
            $("#ver_tienda_prove").removeClass('active');
        }else{
            $("#ver_detalle_producto").removeClass("active");
        }
        $("#perfil_tienda").css('display','none');
        $("#producto_detalle").css('display','block');
        $("#ver_tienda").css('display','none');
        
    });

    $("#ver_tienda_prove").click(function(evt){
        evt.preventDefault();
        if($("#ver_tienda_prove").hasClass('active')==false){
            $("#ver_tienda_prove").addClass('active');
            $("#ver_detalle_producto").removeClass('active');
            $("#ver_perfil_tienda").removeClass('active');
        }else{
            $("#ver_tienda_prove").removeClass('active');
        }
        $("#producto_detalle").css('display','none');//hace invisible el elemento producto detalle
        $("#perfil_tienda").css('display','none');
        $("#ver_tienda").css('display','block');
        //despues de eso cargar los productos en la tienda
        vacio = null;
        const csrftoken = getCookie('csrftoken');
        $.ajax({
            url:$('#ver_tienda_prove').attr('href'),
            type:'POST',
            data:{
                csrfmiddlewaretoken:csrftoken,
                'id_prove':$('#mayo').val(),
            },
            success:function(data){
               //alert(data); 
               prod = JSON.parse(data);
               tmp = '';
               for(let i in prod){
                   var id = prod[i].pk;
                   var foto_producto1 = prod[i].fields.foto_producto1;
                   var url = prod[i].fields.url;
                   var producto = prod[i].fields.producto;
                   var precio_unitario = prod[i].fields.precio_unitario;
   
                   parte_tmp='<div class="col mb-4"><div class="card"><h5 class="card-title">'+producto+'</h5><a href="/superStore/producto/detalle_producto/'+url+'/'+id+'"><img class="img-fluid img-thumbnail" src="/media/'+foto_producto1+'" alt=""></a><div class="card-body"><h4 class="card-title">$'+precio_unitario+'</h4></div></div></div>';
                   tmp +=parte_tmp;
                   console.log(precio_unitario); 
               }
               
               $("#listado").html(tmp);
            }
        });
    });
    //formulario de buscar en la tienda
    $("#buscar").submit(function(){
        var clave = $("#clave").val();
        var prove = $("#prove").val();
        const csrftoken = getCookie("csrftoken");
        $.ajax({
            url:$("#buscar").attr('action'),
            type:$("#buscar").attr('method'),
            dataType: "json",
            data:{
                csrfmiddlewaretoken:csrftoken,
                'prove':prove,
                'clave':clave,
            },
            success:function(data){
                var prod = JSON.parse(data);
                tmp = '';
               

            for(let i in prod){//extrayendo todos los datos de los productos enpaquedados con joson
                var id = prod[i].pk;
                var foto_producto1 = prod[i].fields.foto_producto1;
                var url = prod[i].fields.mayorista;
                var producto = prod[i].fields.producto;
                var precio_unitario = prod[i].fields.precio_unitario;

                parte_tmp='<div class="col mb-4"><div class="card"><h5 class="card-title">'+producto+'</h5><a href="/superStore/producto/detalle_producto/'+url+'/'+id+'"><img class="img-fluid img-thumbnail" src="/media/'+foto_producto1+'"  alt=""></a><div class="card-body"><h4 class="card-title">$'+precio_unitario+'</h4></div></div></div>';
                tmp +=parte_tmp;
                console.log(precio_unitario); 
            }
            
            $("#listado").html(tmp);

                //alert(data[0].model);
            }
        });
        return false;
    });
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
                if(data.res==true){
                    //alert(boton.hasClass('btn-success'));
                    if(boton.hasClass('btn-primary')==true){//verificando si el boton tiene btn-succes
                        boton.addClass('btn-success');
                        boton.removeClass('btn-primary');                           
                    }                    
                }else{
                    if(boton.hasClass('btn-success')){//verificando si el boton esta en primary color
                        boton.addClass('btn-primary');
                        boton.removeClass('btn-success');                        
                    }
                }
            },
        });
        return false;
    });
});

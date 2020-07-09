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
    $(".foto").hover(function(){
        var ubi = $(this).attr("src");
        //alert(ubi);
        $("#foto_producto").attr("src",ubi);
    })
    //formulario de comentario
    $("#comentar").submit(function(evt){//Enviando el formulario
        const csrftoken = getCookie('csrftoken');
        //alert($("#cmt").val());
        evt.preventDefault();
        datos={
            csrfmiddlewaretoken:csrftoken,
            'producto_id':$("#prod_id").val(),
            'coment':$("#cmt").val(),
            'puntaje':$("input:radio[name=puntaje]:checked").val()
        };
        $.ajax({
            type:'POST',
            url:$("#comentar").attr("action"),
            data:datos,
            dataType:"json",
            success:function(data){
                if(data.res==true){
                    location.reload();//recarga la pagina para mostrar los comentarios
                    $("#cmt").val('');//limpia el contenido del textview
                }else{
                    alert("Hubo un error favor recarge o contacte con el desarrollador!!")
                }
            }
        });     
    });
    //Elimina el comentario
    $(".del_coment").click(function(evt){
        evt.preventDefault();
        var conf = confirm("¿Esta seguro que desea eliminar el comentario?");
        if(conf==true){
            url = $(this).attr('href');//obtiene el valor de href que es el url de cada comentario
            btn = $(this).attr('id');//obtiene el valor del id del boton eliminar que "c + cid" que es el id de cada comentario
            id_p = btn.substring(1,btn.length);//con substring eliminamos un "c" ya que en los p esta como "cid"
            $.ajax({
                url:url,
                type:'GET',
                dataType:'json',
                success:function(data){
                    if(data.res==true){//si se elimina el elemento 
                        $("#"+id_p).remove();//eliminamos el parrafo o el comentario de la lista en la pagina
   
                    }
                    
                }
            });
        }

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
                   var mayorista_id = prod[i].fields.mayorista;
                   var producto = prod[i].fields.producto;
                   var precio_unitario = prod[i].fields.precio_unitario;
   
                   parte_tmp='<div class="col mb-4"><div class="card"><h5 class="card-title">'+producto+'</h5><a href="/superStore/producto/detalle_producto/'+id+'"><img src="/media/'+foto_producto1+'" width="265em" height="200em" alt=""></a><div class="card-body"><h4 class="card-title">$'+precio_unitario+'</h4></div></div></div>';
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
                var mayorista_id = prod[i].fields.mayorista;
                var producto = prod[i].fields.producto;
                var precio_unitario = prod[i].fields.precio_unitario;

                parte_tmp='<div class="col mb-4"><div class="card"><h5 class="card-title">'+producto+'</h5><a href="/superStore/producto/detalle_producto/'+id+'"><img src="/media/'+foto_producto1+'" width="265em" height="200em" alt=""></a><div class="card-body"><h4 class="card-title">$'+precio_unitario+'</h4></div></div></div>';
                tmp +=parte_tmp;
                console.log(precio_unitario); 
            }
            
            $("#listado").html(tmp);

                //alert(data[0].model);
            }
        });
        return false;
    });
});

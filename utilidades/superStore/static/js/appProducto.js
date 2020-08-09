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

(function() {
    'use strict';
    window.addEventListener('load', function() {
       
      // Fetch all the forms we want to apply custom Bootstrap validation styles to
      var forms = document.getElementsByClassName('needs-validation');
      // Loop over them and prevent submission
      var validation = Array.prototype.filter.call(forms, function(form) {
        form.addEventListener('submit', function(event) {
          if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
          }

          form.classList.add('was-validated');
        }, false);
      });
    }, false);
  })();

$(document).ready(function () {
    //aplicando efecto lightbox a las miniaturas de imagenes
    $(document).on('click', '[data-toggle="lightbox"]', function(evt){
        evt.preventDefault();
        $(this).ekkoLightbox({
            alwaysShowClose:true,
            onShown:function(){
                console.log('Comprobando los eventos')
            },
        });
    });
    //Listando los comentarios del producto
    id_prod_meta = document.querySelector('meta[name="prod_id"]');//obteniendo el id del producto que lo almaceno en una etiqueta meta
    id_prod = id_prod_meta.content;
    var user_meta = document.querySelector('meta[name="name_user"]')

    if(user_meta==null){//si user_meta esta null significa que el usuario no ha iniciado secion
       var user=null //si es asi asignar el valor null a user para que no detecte usuario.
    }else{
        var user= user_meta.content;//de lo contrario significa que el usuario se ha logeado..
    }
    var opciones ='';
    $.ajax({
        type: 'GET',
        url: '/superStore/producto/comentario/listarComent/' + id_prod,
        dataType: 'json',
        success: function (data) {
            if (data.length == 0) {
                $("#comentar").css('display', 'block');//si el tamaño de los comentarios son igual a cero significa que no hay ningun comentario y se habilita el editor para escribir
            } else if (data.length > 0) {//si es mayor que cero significa que hay comentarios que escribir
                for (let i in data) {
                    if (i != 0) {//valida que la variable i sea diferente de cero ya que en la casilla numero cero esta la comprobacion si el comentario del usuario logueado
                        console.log(i);
                        var puntaje = data[i].puntaje;
                        punt = ''
                        console.log(data[i]);

                        stars = ""
                        if (data[i].puntaje == 1) {
                            stars = '★';
                        } else if (data[i].puntaje == 2) {
                            stars = '★★';
                        } else if (data[i].puntaje == 3) {
                            stars = '★★★';
                        } else if (data[i].puntaje == 4) {
                            stars = '★★★★';
                        } else if (data[i].puntaje == 5) {
                            stars = '★★★★★';
                        }
                    
                        if(user==data[i].cliente){//validando que no mmuestre los controles de edicion en los comentarios de otros usuarios..
                            opciones = '<div id="op_coment">\
                                            <a class="del_coment btn btn-danger" id="cc'+ data[i].id + '" href="/superStore/producto/comentario/' + data[i].id + '">Eliminar</a>\
                                            <button id="ccc'+ data[i].id + '" class="editar_coment btn btn-primary">Editar</button>\
                                        </div>';
                        }
                        //alert("valor de opciones "+opciones);
                        sms = '<div style="color: azure;" class="msj" id="c' + data[i].id + '">\
                                    <h5 id="titCo'+data[i].id+'">'+ data[i].cliente + '</h5>\
                                    <span id="stars'+data[i].id+'" style="color: orange;" id="s'+ data[i].id + '">' + stars + '</span>\
                                     <p id="par'+ data[i].id + '">\
                                        '+ data[i].comentario + '\
                                    </p>\
                                    <div clas="container" >\
                                    <div style="margin: 0; padding: 0; border:0;" class="row">\
                                    <div class="col-4 col-sm-4 col-md-4 col-lg-4 col-xl-4">\
                                        <div id="foto1'+data[i].id+'" class="card" style="width: 5rem;">\
                                            <a data-toggle="lightbox" data-gallery="galeria-'+data[i].id+'" href="/media/'+data[i].foto_prueba1+'">\
                                                <img class="img-thumbnail foto" src="/media/'+data[i].foto_prueba1+'" class="card-img-top" width="80px" height="80" alt="...">\
                                            </a>\
                                        </div>\
                                    </div>\
                                    <div style="margin-left: -85px;" class="col-4 col-sm-4 col-md-4 col-lg-4 col-xl-4">\
                                        <div id="foto2'+data[i].id+'" class="card" style="width: 5rem;">\
                                            <a data-toggle="lightbox" data-gallery="galeria-'+data[i].id+'" href="/media/'+data[i].foto_prueba2+'">\
                                                <img class="img-thumbnail foto" src="/media/'+data[i].foto_prueba2+'" class="card-img-top" width="80px" height="80" alt="...">\
                                            </a>\
                                        </div>\
                                    </div>\
                                    <div style="margin-left: -85px;" class="col-4 col-sm-4 col-md-4 col-lg-4 col-xl-4">\
                                        <div id="foto3'+data[i].id+'" class="card" style="width: 5rem;">\
                                            <a data-toggle="lightbox" data-gallery="galeria-'+data[i].id+'" href="/media/'+data[i].foto_prueba3+'" >\
                                                <img class="img-thumbnail foto" src="/media/'+data[i].foto_prueba3+'" class="card-img-top" width="80px" height="80" alt="...">\
                                            </a>\
                                        </div>\
                                    </div>\
                                </div>\
                                    </div>\
                                    '+opciones+'\
                                    <div fech'+data[i].id+'>Creado el: '+data[i].fecha_creacion+'</div>\
                                  </div>';

                        $("#comentarios").append(sms);
                        opciones='';//Borrando las opciones para que no quede inicializada en ella
                    }
                }
            }
            if (data[0].existe == false) {//si no existe mostrara el campo para agregar el comentario..
                if(user!=null){
                    $("#comentar").css('display', 'block');
                }                
            }



        }
    });

    //alert("Ya esta cargado");
    //Eliminando los comentarios
    $(document).on('click', '.del_coment', function (evt) {
        evt.preventDefault();
        var conf = confirm("¿Esta seguro que desea eliminar el comentario?");
        if (conf == true) {
            url = $(this).attr('href');//obtiene el valor de href que es el url de cada comentario
            btn = $(this).attr('id');//obtiene el valor del id del boton eliminar que "c + cid" que es el id de cada comentario
            id_p = btn.substring(1, btn.length);//con substring eliminamos un "c" ya que en los p esta como "cid"
            //alert(id_p);
            $.ajax({
                url: url,
                type: 'GET',
                dataType: 'json',
                success: function (data) {
                    if (data.res == true) {//si se elimina el elemento 
                        $("#" + id_p).remove();//eliminamos el parrafo o el comentario de la lista en la pagina
                        $("#comentar").css('display', 'block');//mostramos para que de la opcion de comentar
                    }

                }
            });
        }
    });
    ///editar comentario
    var ver = true;
    $(document).on('click', '.editar_coment', function (evt) {
        evt.preventDefault();
        id = $(this).attr('id');//obteniendo el id del boton precionado
        idSub = id.substring(3, id.length);//obteniendo el id puro 
        idParrafo = id.substring(2, id.length)//deduciendo el id del parrafo 
        console.log('valor de ver; ' + ver);
        texto = $('#par' + idSub).text();//Obteniendo el texto del comentario que esta en el parrafo que contiene el prefijo par y luego el id del comentario
        $('#par' + idSub).css('display','none');//ocultando el parrafo del comentario.
        formedit = '<form method="POST" class="needs-validation comt" id="edit_com" action="/superStore/producto/comentario/editar_coment" enctype="multipart/form-data">\
                        <input id="id_coment" type="hidden" name="id_coment" value="'+idSub+'">\
                        <h4>Puntaje<h4/>\
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
                            <div class="form-row" >\
                                <textarea class="form-control" styles=" text-align:left; " name="coment" id="cmt" cols="100" rows="3" required></textarea>\
                            </div>\
                            <div class="form-row" >\
                                <input class="form-control" type="file" accept="image/*"  name="foto_prueba1" id="foto_prueba1" required>\
                            </div>\
                            <div class="form-row" >\
                                <input class="form-control" type="file" accept="image/*"  name="foto_prueba2" id="foto_prueba2" required>\
                            </div>\
                            <div class="form-row" >\
                                <input class="form-control" type="file" accept="image/*"  name="foto_prueba3" id="foto_prueba3" required>\
                            </div>\
                            <button class="btn btn-primary" type="submit">Comentar</button>\
                            <a class="btn btn-success" id="closeForm" href="/close/'+idSub+'">Cancelar</a> \
                    </form>';
        $('#' + idParrafo).append(formedit);//  agregando el formulario de edicion a la etiqueta p donde esta el texto

        $("#cmt").append(texto);//agregando el texto el en textarea que se esta mostrando      

        $("#titCo"+idSub+"").css('display', 'none');//ocultando el titulo del comentario 

        $("#op_coment").css('display', 'none');//ocultando los botones

        $("#stars"+idSub+"").css('display', 'none');//ocultando las estrellas del puntaje
  
        $("#fech"+idSub).css('display','none');//ocultando el div de la fecha
        //ocultando los contenedores de imagenes..
        $("#foto1"+idSub+"").css('display', 'none');
        $("#foto2"+idSub+"").css('display', 'none');
        $("#foto3"+idSub+"").css('display', 'none');

        /*$('#par' + idSub).html('');//limpiando el parrafo para mostrar el formulario de comentario y tambien para poner el nuevo comentario 
        $("#stars"+idSub+"").html('');//limpiando donde estan las estrellas
        $("#titCo"+idSub+"").html('');//limpiando e titulo...
        //limpiando el contenedor de imagenes..  
        $("#foto1"+idSub+"").html('');
        $("#foto2"+idSub+"").html('');   
        $("#foto3"+idSub+"").html('');*/
    });
    $(document).on('click', "#closeForm", function(evt){//escuchando el evento de cancelar la edicion del comentario
        evt.preventDefault();
        idTag = $(this).attr('href');
        idc = idTag.substring(7,idTag.length);//id del comentario...
        $('#par' + idc).css('display','block');//desocultando el parrafo en donde esta el comentario modo texto
        //alert(idc);
        $("#edit_com").remove();//Se elimina el formulario de edicion...
        $("#op_coment").css('display', 'block');//ocultando los botones
        $("#stars"+idc+"").css('display', 'block');//ocultando las estrellas del puntaje
        $("#titCo"+idc+"").css('display', 'block');//ocultando el titulo del comentario   
        //ocultando los contenedores de imagenes..
        $("#foto1"+idc+"").css('display', 'block');
        $("#foto2"+idc+"").css('display', 'block');
        $("#foto3"+idc+"").css('display', 'block');
    })

    $(document).on('submit', "#edit_com", function (evt) {
        evt.preventDefault();
        url = $(this).attr("action");
        const csrftoken = getCookie('csrftoken');
        id_prod_meta = document.querySelector('meta[name="prod_id"]');
        id_prod = id_prod_meta.content;//id del producto
        puntaje = $("input:radio[name=puntaje]:checked").val();
        comentario = document.getElementById('cmt').value.trim();
        id_coment = $("#id_coment").val();
        var datosForm = new FormData();
        datosForm.append('csrfmiddlewaretoken', csrftoken);
        datosForm.append('producto_id',id_prod);
        datosForm.append('id_coment',id_coment);
        datosForm.append('comentario', comentario);
        datosForm.append('puntaje',puntaje);
        var foto_prueba1 = $("#foto_prueba1")[0].files[0];//obteniendo LAS IMAGENES
        var foto_prueba2 = $("#foto_prueba2")[0].files[0];
        var foto_prueba3 = $("#foto_prueba3")[0].files[0];
        datosForm.append('foto_prueba1',foto_prueba1);
        datosForm.append('foto_prueba2',foto_prueba2);
        datosForm.append('foto_prueba3',foto_prueba3);
        //alert(datosForm.get('id_coment'));
        $.ajax({
            type: 'POST',
            url: url,
            data: datosForm,
            contentType:false,
            processData:false,
            success: function (data) {
                console.log(data[0].res);
                if (data[0].res === true) {
                    $("#edit_com").remove();
                    stars = ""
                    if (data[1].puntaje == 1) {
                        stars = '★';
                    } else if (data[1].puntaje == 2) {
                        stars = '★★';
                    } else if (data[1].puntaje == 3) {
                        stars = '★★★';
                    } else if (data[1].puntaje == 4) {
                        stars = '★★★★';
                    } else if (data[1].puntaje == 5) {
                        stars = '★★★★★';
                    }
                    //limpiando los componentes del formulario..
                    $('#par' + data[1].id).html('');//limpiando el parrafo para mostrar el nuevo comentario
                    $("#stars"+data[1].id+"").html('');//limpiando donde estan las estrellas
                    $("#titCo"+data[1].id+"").html('');//limpiando e titulo...
                    $("#fech"+data[1].id+"").html('');//limpiando la anterior fecha..
                    //limpiando el contenedor de imagenes..  
                    $("#foto1"+data[1].id+"").html('');
                    $("#foto2"+data[1].id+"").html('');   
                    $("#foto3"+data[1].id+"").html('');
                    comenn = data[1].comentario;
                    $("#titCo"+data[1].id+"").append(data[1].cliente);//agregando el titulo que es el nombre del cliente
                    $("#stars" + data[1].id).append(stars);//agregando el puntaje en estrellas del comentario
                    $("#par" + data[1].id).append(comenn);//agregando el comentario
                    foto1 = '<img class="img-thumbnail foto" src="/media/'+data[1].foto_prueba1+'" class="card-img-top" width="80px" height="80" alt="...">';
                    foto2 = '<img class="img-thumbnail foto" src="/media/'+data[1].foto_prueba2+'" class="card-img-top" width="80px" height="80" alt="...">';
                    foto3 = '<img class="img-thumbnail foto" src="/media/'+data[1].foto_prueba3+'" class="card-img-top" width="80px" height="80" alt="...">';
                    //agregando las imagenes
                    $("#foto1"+data[1].id).append(foto1);
                    $("#foto2"+data[1].id).append(foto2);
                    $("#foto3"+data[1].id).append(foto3);
                    //agregando nueva fecha
                    $("#fech"+data[1].id).append('fecha de edicion '+data[1].fecha_creacion);
                    //mostrando las imagenes
                    $("#foto1"+data[1].id).css('display', 'block');//mostrando la nueva imagen o foto
                    $("#foto2"+data[1].id).css('display', 'block');
                    $("#foto3"+data[1].id).css('display', 'block');  
                    $('#par' + data[1].id).css('display','block');//mostrando el comentario
                    $("#op_coment").css('display', 'block');//mostrando los botones
                    $("#stars"+data[1].id+"").css('display', 'block');//mostrando el nuevo puntaje
                    $("#titCo"+data[1].id+"").css('display', 'block');//mostrando el titulo del comentario..
                }
            }
        });

    });
    //alert(id_prod);
    $(".foto").hover(function () {
        var ubi = $(this).attr("src");
        //alert(ubi);
            //aplicando el efecto lupa a la imagen seleccionada...
        $(".zoom").magnify({
            speed:200,
            src:ubi
        });

        $("#foto_producto").attr("src", ubi);
    })
    //formulario de comentario
    $("#comentar").submit(function (evt) {//Enviando el formulario
        //alert($("#cmt").val());
        //Listando los comentarios del producto
        evt.preventDefault();
        const csrftoken = getCookie('csrftoken');
        id_prod_meta = document.querySelector('meta[name="prod_id"]');
        id_prod = id_prod_meta.content;
        var datosForm = new FormData();
        //alert(csrfmiddlewaretoken);
        datosForm.append('csrfmiddlewaretoken',csrftoken);
        datosForm.append('producto_id', id_prod);
        datosForm.append('coment',$("#cmt").val());
        datosForm.append('puntaje',$("input:radio[name=puntaje]:checked").val());
        var foto_prueba1 = $("#foto_prueba1")[0].files[0];
        var foto_prueba2 = $("#foto_prueba2")[0].files[0];
        var foto_prueba3 = $("#foto_prueba3")[0].files[0];
        datosForm.append('foto_prueba1',foto_prueba1);
        datosForm.append('foto_prueba2',foto_prueba2);
        datosForm.append('foto_prueba3',foto_prueba3);
        datos = {
            'csrfmiddlewaretoken': csrftoken,
            'producto_id': id_prod,
            'coment': $("#cmt").val(),
            'puntaje': $("input:radio[name=puntaje]:checked").val()
        };
        $.ajax({
            type: 'POST',
            url: $("#comentar").attr("action"),
            data: datosForm,
            dataType: "json",
            contentType:false,
            processData:false,
            success: function (data) {
                //verificando el puntaje para ver cuantas estrellas le corresponde a cada comentario
                stars = ""
                if (data.puntaje == 1) {
                    stars = '★';
                } else if (data.puntaje == 2) {
                    stars = '★★';
                } else if (data.puntaje == 3) {
                    stars = '★★★';
                } else if (data.puntaje == 4) {
                    stars = '★★★★';
                } else if (data.puntaje == 5) {
                    stars = '★★★★★';
                }
                sms = '<div class="msj" id="c' + data.id + '">\
                        <h5 id="titCo'+data.id+'">'+ data.cliente + '</h5>\
                        <span id="stars'+data.id+'" style="color: orange;" id="s'+ data.id + '">' + stars + '</span>\
                        <p id="par'+ data.id + '">\
                            '+ data.comentario + '\
                        </p>\
                        <div clas="container" >\
                            <div style="margin: 0; padding: 0; border:0;" class="row">\
                                <div class="col-4 col-sm-4 col-md-4 col-lg-4 col-xl-4">\
                                    <div id="foto1'+data.id+'" class="card" style="width: 5rem;">\
                                        <a data-toggle="lightbox" data-gallery="galeria-'+data.id+'" href="/media/'+data.foto_prueba1+'">\
                                            <img class="img-thumbnail foto" src="/media/'+data.foto_prueba1+'" class="card-img-top" width="80px" height="80" alt="...">\
                                        </a>\
                                    </div>\
                                </div>\
                                <div style="margin-left: -85px;" class="col-4 col-sm-4 col-md-4 col-lg-4 col-xl-4">\
                                    <div id="foto2'+data.id+'" class="card" style="width: 5rem;">\
                                        <a data-toggle="lightbox" data-gallery="galeria-'+data.id+'" href="/media/'+data.foto_prueba2+'">\
                                            <img class="img-thumbnail foto" src="/media/'+data.foto_prueba2+'" class="card-img-top" width="80px" height="80" alt="...">\
                                        </a>\
                                    </div>\
                                </div>\
                                <div style="margin-left: -85px;" class="col-4 col-sm-4 col-md-4 col-lg-4 col-xl-4">\
                                    <div id="foto3'+data.id+'" class="card" style="width: 5rem;">\
                                        <a data-toggle="lightbox" data-gallery="galeria-'+data.id+'" href="/media/'+data.foto_prueba3+'">\
                                            <img class="img-thumbnail foto" src="/media/'+data.foto_prueba3+'" class="card-img-top" width="80px" height="80" alt="...">\
                                        </a>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>\
                        <div id="op_coment">\
                            <a class="del_coment btn btn-danger" id="cc'+ data.id + '" href="/superStore/producto/comentario/' + data.id + '">Eliminar</a>\
                            <button id="ccc'+ data.id + '" class="editar_coment btn btn-primary">Editar</button>\
                        </div>\
                        <div>Creado el: '+data.fecha_creacion+'</div>\
                      </div>';
                //alert(parrafo);
                //datos = JSON.parse(data)
                //alert(data.id);
                //com=pp+'<br>'+data.comentario+'<br><a class="del_coment" id="cc'+data.id+'" href="/superStore/producto/comentario/'+data.id+' ">Eliminar</a>'
                //alert(sms);
                $("#comentarios").append(sms);
                $("#no_coment").css('display','none');
                $("#cmt").val('');//limpia el contenido del textview
                $("#comentar").css('display', 'none');
                //alert(comentario);
            }
        });
    });
    //pestañas 
    $("#ver_perfil_tienda").click(function (evt) {
        evt.preventDefault();
        if ($("#ver_perfil_tienda").hasClass('active') == false) {//verificando si existe la clase active
            $("#ver_perfil_tienda").addClass('active');
            $("#ver_detalle_producto").removeClass('active');
            $("#ver_tienda_prove").removeClass('active');
        } else {
            $("#ver_perfil_tienda").addClass('active');
        }
        $("#producto_detalle").css('display', 'none');//hace invisible el elemento producto detalle
        $("#perfil_tienda").css('display', 'block');//hace invisible el elemento tienda
        $("#ver_tienda").css('display', 'none');//ocultando el div de tienda
        //verificando si el cliente que ha ingresado es un seguidor del proveedor
        $.ajax({
            url: $("#ver_perfil_tienda").attr("href"),
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                //si el resultado es falso significa que no tiene amigos pero le agregara al boton el primary y mostrara el numero de seguidores
                if (data.res == false) {
                    $("#btnSeguir").addClass('btn btn-primary');
                    $("#numero_amigos").html(data.numero_amigos);
                } else {//de lo contrario significa que tiene amigos y agregara el succes al boton y mostrara el numero de amigos 
                    $("#btnSeguir").addClass('btn btn-success');
                    $("#numero_amigos").html(data.numero_amigos);
                }
            }
        });
    });
    //al dar click en el boton seguir se agregara un nuevo seguidor al proveedor
    $("#btnSeguir").click(function (evt) {
        evt.preventDefault();
        $.ajax({
            url: $("#btnSeguir").attr("href"),
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                if (data.res == true) {
                    if ($("#btnSeguir").hasClass("btn-primary") == true) {//si el resultado da true se verifica si el boton tiene el color btn-primary si esta se elimina ese color y se agrega el success
                        $("#btnSeguir").removeClass("btn-primary");
                        $("#btnSeguir").addClass('btn-success');
                    }
                    $("#btnSeguir").addClass('btn btn-success');//si no esta primary se agrega succes y se actualiza el numero de amigos que se recibe del servidor
                    $("#numero_amigos").html(data.numero_amigos);
                } else {//si es falso el resultado significa que se elimino el seguidor
                    if ($("#btnSeguir").hasClass('btn-success') == true) {
                        $("#btnSeguir").removeClass("btn-success");
                        $("#btnSeguir").addClass('btn-primary');
                    }
                    $("#numero_amigos").html(data.numero_amigos);
                }
            }
        });
    });
    $("#ver_detalle_producto").click(function (evt) {
        evt.preventDefault();
        if ($("#ver_detalle_producto").hasClass('active') == false) {
            $("#ver_detalle_producto").addClass('active');
            $("#ver_perfil_tienda").removeClass('active');
            $("#ver_tienda_prove").removeClass('active');
        } else {
            $("#ver_detalle_producto").removeClass("active");
        }
        $("#perfil_tienda").css('display', 'none');
        $("#producto_detalle").css('display', 'block');
        $("#ver_tienda").css('display', 'none');

    });

    $("#ver_tienda_prove").click(function (evt) {
        evt.preventDefault();
        if ($("#ver_tienda_prove").hasClass('active') == false) {
            $("#ver_tienda_prove").addClass('active');
            $("#ver_detalle_producto").removeClass('active');
            $("#ver_perfil_tienda").removeClass('active');
        } else {
            $("#ver_tienda_prove").removeClass('active');
        }
        $("#producto_detalle").css('display', 'none');//hace invisible el elemento producto detalle
        $("#perfil_tienda").css('display', 'none');
        $("#ver_tienda").css('display', 'block');
        //despues de eso cargar los productos en la tienda
        vacio = null;
        const csrftoken = getCookie('csrftoken');
        $.ajax({
            url: $('#ver_tienda_prove').attr('href'),
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrftoken,
                'id_prove': $('#mayo').val(),
            },
            success: function (data) {
                //alert(data); 
                prod = JSON.parse(data);
                tmp = '';
                for (let i in prod) {
                    var id = prod[i].pk;
                    var foto_producto1 = prod[i].fields.foto_producto1;
                    var url = prod[i].fields.url;
                    var producto = prod[i].fields.producto;
                    var precio_unitario = prod[i].fields.precio_unitario;

                    parte_tmp = '<div class="col mb-4"><div class="card"><h5 class="card-title">' + producto + '</h5><a href="/superStore/producto/detalle_producto/' + url + '/' + id + '"><img class="img-fluid img-thumbnail" src="/media/' + foto_producto1 + '" alt=""></a><div class="card-body"><h4 class="card-title">$' + precio_unitario + '</h4></div></div></div>';
                    tmp += parte_tmp;
                    console.log(precio_unitario);
                }

                $("#listado").html(tmp);
            }
        });
    });
    //formulario de buscar en la tienda
    $("#buscar").submit(function () {
        var clave = $("#clave").val();
        var prove = $("#prove").val();
        const csrftoken = getCookie("csrftoken");
        $.ajax({
            url: $("#buscar").attr('action'),
            type: $("#buscar").attr('method'),
            dataType: "json",
            data: {
                csrfmiddlewaretoken: csrftoken,
                'prove': prove,
                'clave': clave,
            },
            success: function (data) {
                var prod = JSON.parse(data);
                tmp = '';


                for (let i in prod) {//extrayendo todos los datos de los productos enpaquedados con joson
                    var id = prod[i].pk;
                    var foto_producto1 = prod[i].fields.foto_producto1;
                    var url = prod[i].fields.mayorista;
                    var producto = prod[i].fields.producto;
                    var precio_unitario = prod[i].fields.precio_unitario;

                    parte_tmp = '<div class="col mb-4"><div class="card"><h5 class="card-title">' + producto + '</h5><a href="/superStore/producto/detalle_producto/' + url + '/' + id + '"><img class="img-fluid img-thumbnail" src="/media/' + foto_producto1 + '"  alt=""></a><div class="card-body"><h4 class="card-title">$' + precio_unitario + '</h4></div></div></div>';
                    tmp += parte_tmp;
                    console.log(precio_unitario);
                }

                $("#listado").html(tmp);

                //alert(data[0].model);
            }
        });
        return false;
    });
    $(".aniadir_favorito").submit(function () {
        boton = $("button", this)
        //alert("Holqqq");
        const csrftoken = getCookie('csrftoken');
        datos = {
            csrfmiddlewaretoken: csrftoken,
            'cliente_id': $("#cliente_id").val(),
        };
        //alert(datos.cliente_id);
        $.ajax({
            url: $(this).attr("action"),
            type: 'GET',
            data: datos,
            dataType: 'json',
            success: function (data) {
                if (data.res == true) {
                    //alert(boton.hasClass('btn-success'));
                    if (boton.hasClass('btn-primary') == true) {//verificando si el boton tiene btn-succes
                        boton.addClass('btn-success');
                        boton.removeClass('btn-primary');
                    }
                } else {
                    if (boton.hasClass('btn-success')) {//verificando si el boton esta en primary color
                        boton.addClass('btn-primary');
                        boton.removeClass('btn-success');
                    }
                }
            },
        });
        return false;
    });
});
